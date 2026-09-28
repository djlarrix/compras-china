#!/usr/bin/env python3
"""Herramientas para compras en China (sin dependencias, Python 3.8+).

Subcomandos:
  tc         Tipos de cambio del día (en vivo, con respaldo offline).
  convertir  Convierte montos entre monedas; mide el recargo cambiario de un agente.
  enlace     Identifica un link (Taobao, Tmall, Weidian, 1688, JD, Xianyu, agentes...)
             y lo convierte al formato de 25+ agentes.
  precios    Rango de precios de referencia y alerta de ofertas sospechosas.
  comparar   Puntaje y costo unitario de proveedores desde un CSV.
  peso       Peso volumétrico y cobrable (courier, aéreo, marítimo).
  lineas     Compara líneas de envío (agentes, casillas, couriers) para un paquete.
  costo      Costo puesto en destino con impuestos por país y margen de venta.
  aql        Plan de muestreo AQL (ISO 2859-1 / ANSI Z1.4, simple, normal).
  talla      Tallas de calzado, elección de talla de ropa y conversión 斤/kg.

Ayuda de cada uno:  python3 china_tools.py <subcomando> -h
En cualquier parámetro de tipo de cambio (--tc, --tc-local) puedes escribir "auto".
"""

import argparse
import csv
import json
import math
import os
import re
import statistics
import sys
import tempfile
import time
import urllib.parse
import urllib.request

VERSION = "2026-09-28"


def fmt(x, dec=2):
    return f"{x:,.{dec}f}"


def table(headers, rows):
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join("---" for _ in headers) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(out)


# =========================================================================== tipos de cambio

# Respaldo si no hay internet. Unidades de cada moneda por 1 USD (mid-market, 27-sep-2026).
SNAPSHOT_FECHA = "2026-09-27"
SNAPSHOT = {
    "USD": 1.0, "CNY": 6.7195, "CLP": 962.26, "MXN": 17.736, "ARS": 1523.97, "COP": 3334.28,
    "PEN": 3.3929, "EUR": 0.87836, "UYU": 40.063, "BRL": 5.1895, "GBP": 0.75559,
    "HKD": 7.8445, "BOB": 12.233, "PYG": 5923.87, "CAD": 1.4149, "AUD": 1.4258,
}
FUENTES_TC = [
    ("open.er-api.com", "https://open.er-api.com/v6/latest/USD"),
    ("fawazahmed0/currency-api (jsDelivr)",
     "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/usd.json"),
    ("fawazahmed0/currency-api (pages.dev)",
     "https://latest.currency-api.pages.dev/v1/currencies/usd.json"),
]
_CACHE_TTL = 6 * 3600


def _cache_path():
    base = os.path.join(os.path.expanduser("~"), ".cache", "compras-china")
    try:
        os.makedirs(base, exist_ok=True)
        test = os.path.join(base, ".w")
        open(test, "w").close()
        os.remove(test)
    except OSError:
        base = tempfile.gettempdir()
    return os.path.join(base, "tipos_de_cambio.json")


def _http_json(url, timeout=8):
    req = urllib.request.Request(url, headers={"User-Agent": "compras-china/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def obtener_tasas(offline=False, forzar=False):
    """Devuelve (tasas por USD, fuente, fecha). Usa caché de 6 h y respaldo offline."""
    path = _cache_path()
    if not offline and not forzar:
        try:
            with open(path, encoding="utf-8") as f:
                c = json.load(f)
            if time.time() - c["guardado"] < _CACHE_TTL:
                return c["tasas"], c["fuente"] + " (caché)", c["fecha"]
        except (OSError, ValueError, KeyError):
            pass
    if not offline:
        for nombre, url in FUENTES_TC:
            try:
                d = _http_json(url)
                if "rates" in d:
                    tasas = {k.upper(): float(v) for k, v in d["rates"].items()}
                    fecha = d.get("time_last_update_utc", "")[:16]
                else:
                    tasas = {k.upper(): float(v) for k, v in d["usd"].items()
                             if isinstance(v, (int, float))}
                    fecha = d.get("date", "")
                if tasas.get("CNY"):
                    try:
                        with open(path, "w", encoding="utf-8") as f:
                            json.dump({"tasas": tasas, "fuente": nombre, "fecha": fecha,
                                       "guardado": time.time()}, f)
                    except OSError:
                        pass
                    return tasas, nombre, fecha
            except Exception:
                continue
    return dict(SNAPSHOT), "respaldo offline (sin conexión)", SNAPSHOT_FECHA


def convertir_monto(monto, de, a, tasas):
    de, a = de.upper(), a.upper()
    if de not in tasas or a not in tasas:
        raise KeyError(f"Moneda no disponible: {de if de not in tasas else a}")
    return monto / tasas[de] * tasas[a]


def resolver_tc(valor, moneda, avisos):
    """Convierte 'auto' en unidades de `moneda` por USD; si es número, lo devuelve."""
    if valor is None:
        return None
    if str(valor).strip().lower() != "auto":
        return float(str(valor).replace(",", "."))
    tasas, fuente, fecha = obtener_tasas()
    if moneda.upper() not in tasas:
        sys.exit(f"No hay tipo de cambio para {moneda}.")
    avisos.append(f"Tipo de cambio {moneda}/USD = {fmt(tasas[moneda.upper()], 4)} "
                  f"({fuente}, {fecha}; valor de mercado, sin recargos).")
    return tasas[moneda.upper()]


def cmd_tc(a):
    tasas, fuente, fecha = obtener_tasas(offline=a.offline, forzar=a.forzar)
    monedas = [m.strip().upper() for m in a.monedas.split(",") if m.strip()]
    print(f"## Tipos de cambio — {fuente}, {fecha}\n")
    rows = []
    cny = tasas["CNY"]
    for m in monedas:
        if m not in tasas:
            rows.append([m, "—", "—", "—"])
            continue
        rows.append([m, fmt(tasas[m], 4), fmt(tasas[m] / cny, 4), fmt(100 * tasas[m] / cny, 2)])
    print(table(["Moneda", "por 1 USD", "por 1 CNY (¥)", "por ¥100"], rows))
    print("\n- Son tasas de mercado (mid-market). Bancos, PayPal y agentes cobran un diferencial "
          "(típicamente 1–5%): usa `convertir --recargo` para simularlo.")
    if "offline" in fuente:
        print("- ⚠️ Sin conexión: se usan valores de respaldo; verifica el tipo de cambio actual.")


def cmd_convertir(a):
    tasas, fuente, fecha = obtener_tasas(offline=a.offline)
    destinos = [d.strip().upper() for d in a.a.split(",")]
    print(f"## {fmt(a.monto)} {a.de.upper()} — {fuente}, {fecha}\n")
    rows = []
    for d in destinos:
        v = convertir_monto(a.monto, a.de, d, tasas)
        r = [d, fmt(v, 0 if v > 1000 else 2)]
        if a.recargo:
            r.append(fmt(v * (1 + a.recargo / 100), 0 if v > 1000 else 2))
        rows.append(r)
    hdr = ["Moneda", "Valor de mercado"] + ([f"Con recargo {fmt(a.recargo, 1)}%"] if a.recargo else [])
    print(table(hdr, rows))
    if a.tc_agente:
        mid = tasas["CNY"]
        rec = (mid / a.tc_agente - 1) * 100
        print(f"\n- Tu agente usa 1 USD = ¥{a.tc_agente}; el mercado, 1 USD = ¥{fmt(mid, 4)}. "
              f"Recargo cambiario efectivo: **{fmt(rec, 2)}%** "
              f"({'alto' if rec > 4 else 'razonable' if rec > 0 else 'a favor tuyo'}). "
              "Súmalo a la comisión para comparar agentes.")


# =========================================================================== enlaces

PLATAFORMAS = {
    "taobao": ("Taobao / Tmall", "https://item.taobao.com/item.htm?id={id}"),
    "weidian": ("Weidian (微店)", "https://weidian.com/item.html?itemID={id}"),
    "1688": ("1688", "https://detail.1688.com/offer/{id}.html"),
    "jd": ("JD.com (京东)", "https://item.jd.com/{id}.html"),
    "xianyu": ("Xianyu / Goofish (闲鱼)", "https://www.goofish.com/item?id={id}"),
    "pdd": ("Pinduoduo (拼多多)", "https://mobile.yangkeduo.com/goods.html?goods_id={id}"),
    "alibaba": ("Alibaba.com", "https://www.alibaba.com/product-detail/_{id}.html"),
    "aliexpress": ("AliExpress", "https://www.aliexpress.com/item/{id}.html"),
}

# Plantillas por agente (sin códigos de afiliado). {id} = id del producto.
# Fuente: formatos públicos de cada agente, recopilados en sept-2026. Estado según reportes.
AGENTES = {
    "Kakobuy": ("https://www.kakobuy.com/item/details?url={enc}", None),
    "Superbuy": ("https://www.superbuy.com/en/page/buy/?url={enc}", None),
    "Sugargoo": ("https://www.sugargoo.com/productDetail?productLink={enc}", None),
    "CSSBuy": ({"weidian": "https://www.cssbuy.com/item-micro-{id}.html",
                "taobao": "https://www.cssbuy.com/item-{id}.html",
                "1688": "https://www.cssbuy.com/item-1688-{id}.html"}, None),
    "Hoobuy": ({"weidian": "https://hoobuy.com/product/2/{id}", "taobao": "https://hoobuy.com/product/1/{id}",
                "1688": "https://hoobuy.com/product/0/{id}"}, None),
    "Oopbuy": ({"weidian": "https://oopbuy.com/goods/details?id={id}&channel=weidian",
                "taobao": "https://oopbuy.com/goods/details?id={id}&channel=taobao",
                "1688": "https://oopbuy.com/goods/details?id={id}&channel=1688"}, None),
    "Joyagoo (ex Joyabuy)": ({"weidian": "https://joyagoo.com/product/?shop_type=weidian&id={id}",
                              "taobao": "https://joyagoo.com/product/?shop_type=taobao&id={id}",
                              "1688": "https://joyagoo.com/product/?shop_type=ali_1688&id={id}"}, None),
    "Lovegobuy": ({"weidian": "https://www.lovegobuy.com/product?id={id}&shop_type=weidian",
                   "taobao": "https://www.lovegobuy.com/product?id={id}&shop_type=taobao",
                   "1688": "https://www.lovegobuy.com/product?id={id}&shop_type=ali_1688"}, None),
    "Litbuy": ({"weidian": "https://www.litbuy.com/product/weidian/{id}", "taobao": "https://www.litbuy.com/product/1/{id}",
                "1688": "https://www.litbuy.com/product/0/{id}"}, None),
    "USFans": ({"weidian": "https://usfans.com/product/3/{id}", "taobao": "https://usfans.com/product/2/{id}",
                "1688": "https://usfans.com/product/1/{id}"}, None),
    "Ootdbuy": ({"weidian": "https://www.ootdbuy.com/goods/details?id={id}&channel=weidian",
                 "taobao": "https://www.ootdbuy.com/goods/details?id={id}&channel=TAOBAO",
                 "1688": "https://www.ootdbuy.com/goods/details?id={id}&channel=1688"}, None),
    "Hipobuy": ({"weidian": "https://hipobuy.com/product/weidian/{id}", "taobao": "https://hipobuy.com/product/1/{id}",
                 "1688": "https://hipobuy.com/product/0/{id}.html"}, None),
    "GTBuy": ({"weidian": "https://www.gtbuy.com/product/weidian/{id}", "taobao": "https://www.gtbuy.com/product/1/{id}",
               "1688": "https://www.gtbuy.com/product/0/{id}"}, None),
    "Vigorbuy": ({"weidian": "https://vigorbuy.com/product/2/{id}", "taobao": "https://vigorbuy.com/product/1/{id}",
                  "1688": "https://vigorbuy.com/product/0/{id}"}, None),
    "RizzitGO": ({"weidian": "https://rizzitgo.com/detail-page?goodsId={id}&source=3",
                  "taobao": "https://rizzitgo.com/detail-page?goodsId={id}&source=1",
                  "1688": "https://rizzitgo.com/detail-page?goodsId={id}&source=2"}, None),
    "Eastmallbuy": ({"weidian": "https://www.eastmallbuy.com/index/weidian/itemID={id}",
                     "taobao": "https://www.eastmallbuy.com/taobaoID={id}",
                     "1688": "https://www.eastmallbuy.com/1688ID={id}"}, None),
    "iTaobuy": ("https://www.itaobuy.com/product-detail?url={enc}", None),
    "LoongBuy": ("https://www.loongbuy.com/product-details?url={enc}", None),
    "Pikobuy": ("https://www.pikobuy.com/product/detail?productUrl={enc}", None),
    "Cnshopper": ({"weidian": "https://cnshopper.com/goods/detail?keyword={id}&platform=weidian",
                   "taobao": "https://cnshopper.com/goods/detail?keyword={id}&platform=taobao",
                   "1688": "https://cnshopper.com/goods/detail?keyword={id}&platform=1688"}, None),
    "Alleurobuy": ({"weidian": "https://alleurobuy.com/index/detail-public?id={id}&type=weidian",
                    "taobao": "https://alleurobuy.com/index/detail-public?id={id}&type=tao",
                    "1688": "https://alleurobuy.com/index/detail-public?id={id}&type=ali"}, None),
    "Mulebuy": ({"weidian": "https://mulebuy.com/product/?shop_type=weidian&id={id}",
                 "taobao": "https://mulebuy.com/product/?shop_type=taobao&id={id}",
                 "1688": "https://mulebuy.com/product/?shop_type=ali_1688&id={id}"},
                "RIESGO: reportes (no confirmados) de redada en su bodega, ago-2026"),
    "CNFans": ({"weidian": "https://cnfans.com/product/?shop_type=weidian&id={id}",
                "taobao": "https://cnfans.com/product/?shop_type=taobao&id={id}",
                "1688": "https://cnfans.com/product/?shop_type=ali_1688&id={id}"},
               "CERRADO: dejó de aceptar pedidos en ago-2026"),
}
# Agentes que reciben la URL completa: sirven también para JD, Tmall, Xianyu, etc. (verificar soporte).
AGENTES_URL_COMPLETA = {"Kakobuy", "Superbuy", "Sugargoo", "iTaobuy", "LoongBuy", "Pikobuy"}

_CODIGOS_RUTA = {  # host -> código en /product/<código>/<id>
    "hoobuy.com": {"0": "1688", "1": "taobao", "2": "weidian"},
    "vigorbuy.com": {"0": "1688", "1": "taobao", "2": "weidian"},
    "usfans.com": {"1": "1688", "2": "taobao", "3": "weidian"},
    "litbuy.com": {"0": "1688", "1": "taobao", "weidian": "weidian"},
    "hipobuy.com": {"0": "1688", "1": "taobao", "weidian": "weidian"},
    "gtbuy.com": {"0": "1688", "1": "taobao", "weidian": "weidian"},
}
_ENVOLTORIOS = ("url", "producturl", "productlink", "goodsurl", "goods_url", "link", "itemurl")
_CORTOS = ("tb.cn", "qr.1688.com", "k.youshop10.com", "vdian.com", "3.cn", "u.jd.com", "yangkeduo.com/r")


def _norm_plat(s):
    s = (s or "").strip().lower()
    if s in ("weidian", "wd", "micro", "3", "vdian"):
        return "weidian"
    if s in ("taobao", "tao", "tb", "tmall", "1"):
        return "taobao"
    if s in ("ali_1688", "1688", "ali", "al", "alibaba", "2"):
        return "1688"
    return None


def resolver_corto(url, timeout=8):
    """Sigue redirecciones de links cortos (m.tb.cn, qr.1688.com...)."""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0)"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        final = r.geturl()
        cuerpo = r.read(200000).decode("utf-8", "ignore")
    if final != url:
        return final
    m = re.search(r"https?://[^'\"\s]*(?:item\.taobao|detail\.tmall|detail\.1688|weidian)\.com[^'\"\s]*", cuerpo)
    return m.group(0) if m else url


def analizar_enlace(raw, _prof=0):
    """Devuelve dict(plataforma, id, nota) o None."""
    raw = (raw or "").strip().strip("\"'<> ")
    if not raw or _prof > 3:
        return None
    m = re.search(r"https?://\S+", raw)  # texto compartido desde la app: extraer la URL
    if m and not raw.lower().startswith("http"):
        raw = m.group(0)
    if re.fullmatch(r"\d{6,}", raw):
        return {"plataforma": None, "id": raw, "nota": "Solo un número: no se sabe de qué plataforma es."}
    if not re.match(r"^https?://", raw, re.I):
        raw = "https://" + raw.lstrip("/")
    try:
        u = urllib.parse.urlparse(raw)
    except ValueError:
        return None
    host = u.netloc.lower().split(":")[0]
    host = re.sub(r"^(www|m|h5|world|detail|item|mobile)\.", "", host) if host.count(".") > 1 else host
    q = {k.lower(): v[0] for k, v in urllib.parse.parse_qs(u.query).items()}
    path = u.path

    for k in _ENVOLTORIOS:  # agentes que envuelven la URL original
        if k in q:
            dv = urllib.parse.unquote(q[k])
            if re.search(r"weidian|taobao|tmall|1688|jd\.com|goofish|yangkeduo", dv, re.I):
                r = analizar_enlace(dv, _prof + 1)
                if r:
                    return r

    full = u.netloc.lower()
    if "weidian.com" in full or "weidian.cn" in full or "koudai.com" in full:
        i = q.get("itemid") or q.get("id")
        if not i:
            mm = re.search(r"(\d{6,})", path)
            i = mm.group(1) if mm else None
        if i:
            return {"plataforma": "weidian", "id": i, "nota": ""}
    if re.search(r"(taobao|tmall)\.(com|hk)$", full):
        i = q.get("id")
        if not i:
            mm = re.search(r"(\d{8,})", path)
            i = mm.group(1) if mm else None
        if i:
            return {"plataforma": "taobao", "id": i, "nota": "Tmall" if "tmall" in full else ""}
    if full.endswith("1688.com") and "qr." not in full:
        mm = re.search(r"offer/(\d+)", path) or re.search(r"(\d{9,})", raw)
        i = q.get("offerid") or (mm.group(1) if mm else None)
        if i:
            return {"plataforma": "1688", "id": i, "nota": ""}
    if re.search(r"jd\.(com|hk)$", full):
        mm = re.search(r"/(?:product/)?(\d{5,})\.html", path) or re.search(r"(\d{6,})", path)
        if mm:
            return {"plataforma": "jd", "id": mm.group(1), "nota": ""}
    if "goofish.com" in full or "xianyu" in full:
        i = q.get("id") or q.get("itemid")
        if i:
            return {"plataforma": "xianyu", "id": i, "nota": ""}
    if "yangkeduo.com" in full or "pinduoduo.com" in full:
        i = q.get("goods_id")
        if i:
            return {"plataforma": "pdd", "id": i, "nota": ""}
    if full.endswith("alibaba.com"):
        mm = re.search(r"_(\d{8,})\.html", path)
        if mm:
            return {"plataforma": "alibaba", "id": mm.group(1), "nota": ""}
    if "aliexpress" in full:
        mm = re.search(r"/item/(\d+)\.html", path)
        if mm:
            return {"plataforma": "aliexpress", "id": mm.group(1), "nota": ""}

    base = host.replace("www.", "")
    for h, mapa in _CODIGOS_RUTA.items():
        if base.endswith(h):
            mm = re.search(r"/(?:product|goods)/([a-z0-9]+)/(\d{5,})", path, re.I)
            if mm and mapa.get(mm.group(1).lower()):
                return {"plataforma": mapa[mm.group(1).lower()], "id": mm.group(2), "nota": f"desde {h}"}
    if base.endswith("rizzitgo.com"):
        i = q.get("goodsid") or q.get("id")
        p = {"3": "weidian", "1": "taobao", "2": "1688"}.get(q.get("source", ""))
        if i and p:
            return {"plataforma": p, "id": i, "nota": "desde rizzitgo"}
    i = q.get("id") or q.get("itemid") or q.get("goodsid") or q.get("keyword") or q.get("tid")
    p = _norm_plat(q.get("shop_type") or q.get("shoptype") or q.get("channel") or q.get("platform")
                   or q.get("source") or q.get("type"))
    if i and p:
        return {"plataforma": p, "id": i, "nota": f"desde {base}"}
    for pat, p in ((r"item-micro-(\d+)", "weidian"), (r"item-1688-(\d+)", "1688"), (r"item-(\d{6,})", "taobao"),
                   (r"itemID[=/](\d+)", "weidian"), (r"taobaoID[=/](\d+)", "taobao"), (r"1688ID[=/](\d+)", "1688")):
        mm = re.search(pat, raw, re.I)
        if mm:
            return {"plataforma": p, "id": mm.group(1), "nota": f"desde {base}"}
    if any(c in full + path for c in _CORTOS):
        return {"plataforma": None, "id": None, "nota": "Link corto: usa --resolver para seguir la redirección.",
                "corto": raw}
    return None


def enlaces_agentes(plataforma, pid):
    canon = PLATAFORMAS[plataforma][1].format(id=pid)
    enc = urllib.parse.quote(canon, safe="")
    out = []
    for nombre, (tpl, estado) in AGENTES.items():
        if isinstance(tpl, dict):
            if plataforma not in tpl:
                continue
            link = tpl[plataforma].format(id=pid)
        else:
            if plataforma not in ("taobao", "weidian", "1688") and nombre not in AGENTES_URL_COMPLETA:
                continue
            link = tpl.format(enc=enc)
        out.append((nombre, link, estado))
    return canon, out


def cmd_enlace(a):
    raw = " ".join(a.link)
    r = analizar_enlace(raw)
    if r and r.get("corto") and a.resolver:
        try:
            dest = resolver_corto(r["corto"])
            r = analizar_enlace(dest) or r
        except Exception as e:
            print(f"- No se pudo resolver el link corto: {e}")
    if r and r["plataforma"] is None and a.plataforma:
        r["plataforma"] = _norm_plat(a.plataforma) or a.plataforma
    if not r or not r.get("plataforma") or not r.get("id"):
        nota = r["nota"] if r else "No reconocí el link."
        sys.exit(f"{nota} Pega el link completo del producto, o indica --plataforma taobao|weidian|1688 "
                 "si solo tienes el número.")
    plat, pid = r["plataforma"], r["id"]
    canon, lista = enlaces_agentes(plat, pid)
    print(f"## {PLATAFORMAS[plat][0]} — id {pid}" + (f" ({r['nota']})" if r["nota"] else "") + "\n")
    print(f"- Link original (guárdalo siempre; no depende de ningún agente): {canon}")
    if plat in ("jd", "xianyu", "pdd"):
        print("- Plataforma no estándar: solo algunos agentes la aceptan (Superbuy acepta JD y Xianyu; "
              "Xianyu cobra tarifa de segunda mano). Verifica antes de pagar.")
    if plat in ("alibaba", "aliexpress"):
        print("- Esta plataforma vende y despacha internacionalmente: no necesitas agente.")
        return
    filtro = [x.strip().lower() for x in a.agentes.split(",")] if a.agentes else None
    rows = []
    for nombre, link, estado in lista:
        if filtro and not any(f in nombre.lower() for f in filtro):
            continue
        if estado and not a.todos:
            continue
        rows.append([nombre, link, estado or "activo¹"])
    print()
    print(table(["Agente", "Link", "Estado"], rows))
    print("\n¹ Según reportes públicos a sept-2026. Los agentes abren y cierran seguido: verifica antes de "
          "cargar saldo y no dejes dinero ni paquetes detenidos mucho tiempo.")
    ocultos = [n for n, _, e in lista if e]
    if ocultos and not a.todos:
        print(f"\n- Ocultos por estado de riesgo o cierre: {', '.join(ocultos)} (usa --todos para verlos).")


# =========================================================================== precios

def cmd_precios(a):
    precios = sorted(a.precios)
    if len(precios) < 2:
        sys.exit("Necesito al menos 2 precios.")
    avisos = []
    tc = resolver_tc(a.tc, "CNY", avisos) if a.tc else None
    med = statistics.median(precios)
    q = statistics.quantiles(precios, n=4) if len(precios) >= 4 else [precios[0], med, precios[-1]]
    print(f"## Referencia de precios ({len(precios)} ofertas, {a.moneda})\n")
    print(table(["Mínimo", "P25", "Mediana", "P75", "Máximo", "Promedio"],
                [[fmt(precios[0]), fmt(q[0]), fmt(med), fmt(q[2]), fmt(precios[-1]),
                  fmt(statistics.mean(precios))]]))
    bajo = [p for p in precios if p < a.umbral_bajo * med]
    alto = [p for p in precios if p > a.umbral_alto * med]
    print()
    print(f"- Rango normal (P25–P75): {fmt(q[0])} – {fmt(q[2])} {a.moneda}")
    if bajo:
        print(f"- Sospechosamente baratas (< {int(a.umbral_bajo * 100)}% de la mediana): "
              + ", ".join(fmt(p) for p in bajo)
              + " → revisar material, especificación, cantidad o estafa.")
    if alto:
        print(f"- Caras (> {int(a.umbral_alto * 100)}% de la mediana): "
              + ", ".join(fmt(p) for p in alto)
              + " → ¿revendedor, mejor calidad o marca? Justifica o negocia.")
    if tc:
        print(f"- Mediana en USD: {fmt(med / tc)} · rango normal USD {fmt(q[0] / tc)} – {fmt(q[2] / tc)}")
    for n in avisos:
        print(f"- {n}")


# =========================================================================== comparar

INSIGNIA_PTS = {
    "super": 20, "superfabrica": 20, "超级工厂": 20,
    "verificada": 16, "深度验厂": 16, "验厂": 16,
    "solidez": 12, "实力商家": 12, "实力": 12,
    "cxt": 5, "诚信通": 5,
    "ninguna": 0, "": 0,
}
TIPO_PTS = {"fabrica": 10, "fábrica": 10, "工厂": 10,
            "revendedor": 3, "comercializadora": 3, "贸易": 3, "trader": 3,
            "desconocido": 0, "": 0}


def _num(v, default=0.0):
    try:
        return float(str(v).replace(",", ".").replace("%", "").strip())
    except (ValueError, TypeError):
        return default


def _si(v):
    return str(v).strip().lower() in ("si", "sí", "s", "yes", "y", "1", "true", "x")


def puntaje_proveedor(r, mediana, umbral_bajo=0.70):
    flags = []
    precio = _num(r.get("precio_cny"))
    ins = INSIGNIA_PTS.get(str(r.get("insignia", "")).strip().lower(), 0)
    tipo = TIPO_PTS.get(str(r.get("tipo", "")).strip().lower(), 0)
    anos = min(_num(r.get("anos")), 10) / 10 * 10
    recompra = min(_num(r.get("recompra_pct")), 50) / 50 * 15
    estrellas = max(0.0, min((_num(r.get("estrellas")) - 3) / 2, 1)) * 10
    resp_min = _num(r.get("respuesta_min"), 999)
    resp = 5 if resp_min <= 5 else 3 if resp_min <= 30 else 1 if resp_min <= 120 else 0
    muestra = 5 if _si(r.get("muestra_ok", "")) else 0
    video = 5 if _si(r.get("video_ok", "")) else 0
    if mediana and precio:
        ratio = precio / mediana
        if ratio < umbral_bajo:
            pp = 5
            flags.append("precio sospechoso")
        else:
            pp = 20 * max(0.0, min((1.3 - ratio) / 0.6, 1))
    else:
        pp = 0
        flags.append("sin precio")
    if _num(r.get("anos")) < 1:
        flags.append("tienda nueva")
    return ins + tipo + anos + recompra + estrellas + resp + muestra + video + pp, flags


def cmd_comparar(a):
    avisos = []
    tc = resolver_tc(a.tc, "CNY", avisos) if a.tc else None
    with open(a.csv, newline="", encoding="utf-8-sig") as f:
        filas = [r for r in csv.DictReader(f) if (r.get("proveedor") or "").strip()]
    if not filas:
        sys.exit("El CSV no tiene proveedores.")
    precios = [_num(r.get("precio_cny")) for r in filas if _num(r.get("precio_cny")) > 0]
    med = statistics.median(precios) if precios else 0
    res = []
    for r in filas:
        total, flags = puntaje_proveedor(r, med, a.umbral_bajo)
        moq = _num(r.get("moq"))
        if moq and a.unidades < moq:
            flags.append(f"MOQ {int(moq)} > {a.unidades}")
        precio = _num(r.get("precio_cny"))
        unit_cny = (precio * a.unidades + _num(r.get("flete_china_cny"))) / a.unidades if precio else 0
        res.append((total, r, unit_cny, flags))
    res.sort(key=lambda x: -x[0])
    print(f"## Comparación de proveedores (para {a.unidades} unidades)\n")
    headers = ["#", "Proveedor", "Tipo / insignia", "Precio ¥", "Costo unit. ¥ (c/flete China)"]
    if tc:
        headers.append("Costo unit. USD")
    headers += ["Puntaje /100", "Alertas"]
    rows = []
    for i, (total, r, unit, flags) in enumerate(res, 1):
        row = [i, r.get("proveedor", "").strip(),
               f"{r.get('tipo', '').strip() or '?'} / {r.get('insignia', '').strip() or '-'}",
               fmt(_num(r.get("precio_cny"))), fmt(unit)]
        if tc:
            row.append(fmt(unit / tc))
        row += [fmt(total, 0), "; ".join(flags) or "—"]
        rows.append(row)
    print(table(headers, rows))
    print("\nPuntaje = insignia (20) + tipo (10) + años (10) + recompra (15) + estrellas (10) + "
          "respuesta (5) + muestra (5) + video (5) + precio relativo (20). "
          "Es una ayuda: la muestra física y la verificación pesan más.")
    for n in avisos:
        print(f"- {n}")


# =========================================================================== peso

def peso_cobrable(largo, ancho, alto, peso_real, divisor, cajas=1):
    vol = largo * ancho * alto / divisor * cajas if divisor else 0.0
    real = peso_real * cajas
    return max(vol, real), vol, real


def cmd_peso(a):
    vol_cm3 = a.largo * a.ancho * a.alto
    cajas = a.cajas
    real_total = a.peso_real * cajas
    filas = []
    divisores = [("Courier express (DHL/FedEx/UPS)", 5000), ("Aéreo IATA / muchas líneas", 6000),
                 ("Algunas líneas económicas de agentes", 8000)]
    if a.divisor and a.divisor not in (5000, 6000, 8000):
        divisores.append(("Divisor personalizado", a.divisor))
    for nombre, d in divisores:
        cob, vol, _ = peso_cobrable(a.largo, a.ancho, a.alto, a.peso_real, d, cajas)
        filas.append([f"{nombre} (/{d})", fmt(vol), fmt(real_total), fmt(cob),
                      "volumen" if vol > real_total else "peso real"])
    print(f"## Peso cobrable — {cajas} caja(s) de {a.largo}×{a.ancho}×{a.alto} cm, "
          f"{a.peso_real} kg c/u\n")
    print(table(["Método", "Peso volumétrico kg", "Peso real kg", "Peso cobrable kg", "Manda"], filas))
    cbm = vol_cm3 / 1_000_000 * cajas
    wm = max(cbm, real_total / 1000)
    print(f"\n- Volumen total: {fmt(cbm, 3)} m³ (marítimo LCL cobra {fmt(wm, 3)} W/M; "
          f"1 m³ = 1.000 kg). Muchos consolidados cobran un mínimo de 1 m³.")
    dens = real_total / cbm if cbm else 0
    print(f"- Densidad: {fmt(dens, 0)} kg/m³ "
          f"({'liviano/voluminoso: el volumen encarece el aéreo; considera quitar cajas, vacío o marítimo' if dens < 167 else 'denso: en aéreo se cobra por peso real'}).")


# =========================================================================== líneas de envío

def costo_linea(fila, peso_real_kg, dims, tc):
    """Costo de una línea para un paquete. Devuelve dict o None si excede el peso máximo."""
    divisor = _num(fila.get("divisor"))
    largo, ancho, alto = dims if dims else (0, 0, 0)
    cob, vol, _ = peso_cobrable(largo, ancho, alto, peso_real_kg, divisor if dims else 0)
    g = cob * 1000
    primer = _num(fila.get("primer_peso_g"), 500) or 500
    cont = _num(fila.get("continuo_g"), 500) or 500
    costo = _num(fila.get("precio_primer"))
    if g > primer:
        costo += math.ceil((g - primer) / cont - 1e-9) * _num(fila.get("precio_continuo"))
    costo += _num(fila.get("cargo_fijo"))
    moneda = (fila.get("moneda") or "CNY").strip().upper()
    usd = costo / tc if moneda == "CNY" else costo
    maxkg = _num(fila.get("peso_max_kg"))
    return {"cobrable": cob, "volumen": vol, "costo": costo, "moneda": moneda, "usd": usd,
            "excede": bool(maxkg and cob > maxkg)}


def cmd_lineas(a):
    avisos = []
    tc = resolver_tc(a.tc, "CNY", avisos)
    dims = (a.largo, a.ancho, a.alto) if a.largo and a.ancho and a.alto else None
    with open(a.csv, newline="", encoding="utf-8-sig") as f:
        filas = [r for r in csv.DictReader(f) if (r.get("linea") or "").strip()]
    res = []
    for r in filas:
        c = costo_linea(r, a.peso_real, dims, tc)
        res.append((c, r))
    res.sort(key=lambda x: (x[0]["excede"], x[0]["usd"]))
    print(f"## Líneas de envío para {a.peso_real} kg"
          + (f", caja {a.largo}×{a.ancho}×{a.alto} cm" if dims else " (sin medidas: solo peso real)") + "\n")
    rows = []
    for c, r in res:
        rows.append([r.get("agente", ""), r.get("linea", ""), fmt(c["cobrable"]),
                     f"{fmt(c['costo'])} {c['moneda']}", fmt(c["usd"]), r.get("dias", ""),
                     "sí" if _si(r.get("impuestos_incluidos", "")) else "no",
                     ("⚠️ excede peso máx. " if c["excede"] else "") + (r.get("notas") or "")])
    print(table(["Agente", "Línea", "Kg cobrables", "Costo", "USD", "Días", "Impuestos incl.", "Notas"], rows))
    print("\n- Con impuestos incluidos no pagas al recibir; sin ellos, suma aranceles/IVA del país "
          "(`costo --flete-usd ...`). Revisa que la línea acepte tu tipo de producto (baterías, líquidos, marcas).")
    for n in avisos:
        print(f"- {n}")


# =========================================================================== costo

# nombre: (arancel_pct, iva_pct, base, moneda, nota, franquicia_total_usd, franquicia_arancel_usd, fijo_usd)
PRESETS = {
    "chile": (6.0, 19.0, "cif", "CLP",
              "Chile, compra directa/agente no inscrito en SII: arancel 6% s/CIF + IVA 19% s/(CIF+arancel).",
              0, 0, 0),
    "chile-tlc": (0.0, 19.0, "cif", "CLP",
                  "Chile con origen acreditado (Form F, TLC Chile–China): arancel 0% + IVA 19%.", 0, 0, 0),
    "chile-plataforma": (0.0, 19.0, "cif", "CLP",
                         "Chile, plataforma inscrita en SII, compra ≤ USD 500: IVA 19% cobrado en la compra, sin arancel.",
                         0, 0, 0),
    "peru": (6.0, 18.0, "cif", "PEN",
             "Perú: hasta USD 200 FOB sin tributos (SUNAT evalúa cobrar IGV; verificar). Sobre eso: ad valorem "
             "(0/6/11% según partida; 6% por defecto) + IGV 16% + IPM 2%. TLC Perú–China puede dejar el arancel en 0%.",
             200, 0, 0),
    "colombia": (10.0, 19.0, "cif", "COP",
                 "Colombia, tráfico postal/envíos urgentes de origen sin TLC: arancel 10% + IVA 19% (hasta USD 200; "
                 "sobre eso arancel según partida). Reglas de IVA cambiaron en 2025–2026: verificar en la DIAN.",
                 0, 0, 0),
    "argentina": (20.0, 21.0, "cif", "ARS",
                  "Argentina (Decreto 604/2026): franquicia USD 400 FOB por envío (5 envíos/año) exenta de derechos y "
                  "tasa estadística; el excedente paga el régimen general (derechos según NCM, 20% por defecto). "
                  "IVA 21% supuesto sobre el total: verificar.",
                  0, 400, 0),
    "ecuador-4x4": (0.0, 0.0, "cif", "USD",
                    "Ecuador, courier 4x4 (≤ 4 kg y ≤ USD 400 FOB): tarifa fija USD 20 por paquete desde jun-2025.",
                    0, 0, 20),
    "mexico-courier": (33.5, 0.0, "cif", "MXN",
                       "México, mensajería de origen sin tratado: tasa global 33,5% (incluye IVA), hasta ~USD 2.500. "
                       "Verificar vigencia.", 0, 0, 0),
    "us": (0.0, 0.0, "fob", "USD",
           "EE.UU.: sin de minimis. Indica --arancel-pct (MFN + Sección 301 + recargos vigentes). Sin IVA federal.",
           0, 0, 0),
    "eu": (0.0, 21.0, "cif", "EUR",
           "UE (IVA 21% por defecto): indica --arancel-pct, o --arancel-fijo-usd (≈ EUR 3 por línea arancelaria "
           "si el envío es ≤ EUR 150, desde jul-2026).", 0, 0, 0),
    "espana": (0.0, 21.0, "cif", "EUR",
               "España (UE): IVA 21%; envíos ≤ EUR 150: EUR 3 fijos por línea arancelaria (usa --arancel-fijo-usd), "
               "sobre eso arancel TARIC (--arancel-pct).", 0, 0, 0),
    "generico": (0.0, 0.0, "cif", "",
                 "Genérico: indica --arancel-pct, --iva-pct y --base.", 0, 0, 0),
}


def calcular_costo(a):
    """Devuelve un dict con el desglose. `a` es un Namespace de argparse (o compatible)."""
    p = PRESETS[a.pais]
    arancel_pct = a.arancel_pct if a.arancel_pct is not None else p[0]
    iva_pct = a.iva_pct if a.iva_pct is not None else p[1]
    base = a.base or p[2]
    moneda = a.moneda_local or p[3]
    franq_total, franq_arancel, fijo_preset = p[5], p[6], p[7]
    notas = [p[4]]
    tc = a.tc

    prod_cny = a.precio_cny * a.unidades + a.extras_cny
    flete_cn = a.flete_china_cny
    comision = prod_cny * a.comision_pct / 100
    sub = prod_cny + flete_cn + comision
    pago = sub * a.pago_pct / 100
    pagado_cn_usd = (sub + pago) / tc

    fob = (prod_cny + flete_cn) / tc
    if a.flete_usd is not None:
        flete_int = a.flete_usd
    elif a.kg is not None and a.usd_kg is not None:
        flete_int = a.kg * a.usd_kg + a.cargo_fijo_usd
    else:
        flete_int = 0.0
        notas.append("Sin flete internacional: indica --flete-usd o --kg y --usd-kg.")
    seguro_pagado = fob * a.seguro_pct / 100
    seguro_base = seguro_pagado
    if a.pais.startswith("chile") and a.seguro_pct == 0 and not a.impuestos_incluidos:
        seguro_base = fob * 0.02
        notas.append("Sin seguro contratado: se usa seguro presunto de 2% del FOB para la base "
                     "aduanera (verificar criterio vigente).")
    cif = fob + flete_int + seguro_base

    arancel = iva = 0.0
    if a.impuestos_incluidos:
        notas.append("Línea con impuestos incluidos (DDP): arancel e IVA en 0; confirma que el "
                     "forwarder declara el valor real.")
    elif franq_total and fob <= franq_total:
        notas.append(f"FOB ≤ USD {franq_total}: exento de tributos según el preset.")
    else:
        base_val = fob if base == "fob" else cif
        if franq_arancel:
            exceso = max(0.0, fob - franq_arancel)
            base_arancel = base_val * (exceso / fob) if fob else 0
            if exceso == 0:
                notas.append(f"FOB ≤ USD {franq_arancel}: sin derechos de importación (franquicia).")
        else:
            base_arancel = base_val
        arancel = base_arancel * arancel_pct / 100 + a.arancel_fijo_usd + fijo_preset
        if a.pais == "chile-plataforma":
            iva = (fob + flete_int) * iva_pct / 100
        else:
            iva = (cif + arancel) * iva_pct / 100

    total = pagado_cn_usd + flete_int + seguro_pagado + arancel + iva + a.gastos_locales_usd
    unit = total / a.unidades
    neto = total - iva if a.empresa else total
    return {
        "prod_cny": prod_cny, "flete_cn": flete_cn, "comision": comision, "pago": pago,
        "fob": fob, "cif": cif, "flete_int": flete_int, "seguro": seguro_pagado,
        "arancel": arancel, "iva": iva, "total": total, "unit": unit,
        "unit_neto": neto / a.unidades, "arancel_pct": arancel_pct, "iva_pct": iva_pct,
        "base": base, "moneda": moneda, "notas": notas,
    }


MONEDAS_SIN_DECIMALES = {"CLP", "COP", "ARS", "PYG", "UYU"}


def cmd_costo(a):
    avisos = []
    a.tc = resolver_tc(a.tc, "CNY", avisos)
    p = PRESETS[a.pais]
    moneda = a.moneda_local or p[3]
    tl = resolver_tc(a.tc_local, moneda or "USD", avisos) if a.tc_local else None
    c = calcular_costo(a)

    dec_local = 0 if (moneda or "").upper() in MONEDAS_SIN_DECIMALES else 2

    def row(nombre, usd):
        r = [nombre, fmt(usd)]
        if tl:
            r.append(fmt(usd * tl, dec_local))
        return r

    headers = ["Concepto", "USD"] + ([moneda or "Local"] if tl else [])
    rows = [
        row(f"Producto ({a.unidades} × ¥{fmt(a.precio_cny)}"
            + (f" + extras ¥{fmt(a.extras_cny)}" if a.extras_cny else "") + ")", c["prod_cny"] / a.tc),
        row("Flete interno China", c["flete_cn"] / a.tc),
        row(f"Comisión agente ({fmt(a.comision_pct, 1)}%)", c["comision"] / a.tc),
        row(f"Recargo medio de pago/cambio ({fmt(a.pago_pct, 1)}%)", c["pago"] / a.tc),
        row("Flete internacional", c["flete_int"]),
        row(f"Seguro ({fmt(a.seguro_pct, 1)}%)", c["seguro"]),
        row(f"Arancel ({fmt(c['arancel_pct'], 1)}% s/{c['base'].upper()}"
            + (f" + fijos" if (a.arancel_fijo_usd or p[7]) else "") + ")", c["arancel"]),
        row(f"IVA / impuesto ({fmt(c['iva_pct'], 1)}%)", c["iva"]),
        row("Gastos locales (agente, gestión, despacho)", a.gastos_locales_usd),
        row("**TOTAL**", c["total"]),
        row("**Por unidad**", c["unit"]),
    ]
    if a.empresa and c["iva"]:
        rows.append(row("Por unidad sin IVA (crédito fiscal, empresa)", c["unit_neto"]))
    print(f"## Costo puesto en destino — {a.pais} (TC {fmt(a.tc, 4)} CNY/USD"
          + (f", {fmt(tl, 2)} {moneda}/USD" if tl else "") + ")\n")
    print(table(headers, rows))
    print(f"\n- Valor FOB (mercadería + flete interno): USD {fmt(c['fob'])} · Valor CIF aduanero: USD {fmt(c['cif'])}")
    notas = c["notas"]
    fob = c["fob"]
    if a.pais.startswith("chile"):
        if a.pais == "chile-plataforma" and fob > 500:
            notas.append("El régimen de plataforma inscrita aplica a compras de hasta USD 500.")
        if fob > 3000:
            notas.append("FOB > USD 3.000: agente de aduana obligatorio (también por courier).")
        elif fob > 1000:
            notas.append("FOB > USD 1.000: agente de aduana obligatorio en carga normal; por courier "
                         "se puede despachar sin agente hasta USD 3.000.")
    if a.pais == "peru" and fob > 2000:
        notas.append("FOB > USD 2.000: excede el régimen courier; importación formal con agente de aduana.")
    if a.pais == "ecuador-4x4" and fob > 400:
        notas.append("FOB > USD 400: no califica para 4x4; aplica régimen general.")
    if a.pais == "mexico-courier" and fob > 2500:
        notas.append("FOB > USD 2.500: excede el régimen simplificado de mensajería.")
    if a.precio_venta is not None:
        if not tl and moneda not in ("USD", ""):
            notas.append("Para calcular margen en moneda local indica --tc-local (o 'auto').")
        else:
            factor = tl or 1.0
            iva_venta = a.iva_venta_pct if a.iva_venta_pct is not None else c["iva_pct"]
            if a.empresa:
                pv_neto = a.precio_venta / (1 + iva_venta / 100)
                costo_u = c["unit_neto"] * factor
            else:
                pv_neto = a.precio_venta
                costo_u = c["unit"] * factor
            margen = pv_neto - costo_u
            pct = margen / pv_neto * 100 if pv_neto else 0
            print(f"- Precio de venta {fmt(a.precio_venta, dec_local)} → "
                  f"{'neto de IVA ' + fmt(pv_neto, dec_local) + ', ' if a.empresa else ''}"
                  f"costo {fmt(costo_u, dec_local)}, margen bruto {fmt(margen, dec_local)} por unidad ({fmt(pct, 1)}%). "
                  f"Multiplicador precio/costo: {fmt(a.precio_venta / costo_u if costo_u else 0, 2)}×.")
            if pct < 40:
                notas.append("Margen bruto bajo 40%: poco colchón para comisiones de venta, envíos, "
                             "devoluciones y publicidad.")
    for n in notas + avisos:
        print(f"- {n}")


# =========================================================================== aql

LETRAS = "ABCDEFGHJKLMNPQR"
MUESTRAS = [2, 3, 5, 8, 13, 20, 32, 50, 80, 125, 200, 315, 500, 800, 1250, 2000]
NIVELES = {
    "I": [(8, "A"), (15, "A"), (25, "B"), (50, "C"), (90, "C"), (150, "D"), (280, "E"),
          (500, "F"), (1200, "G"), (3200, "H"), (10000, "J"), (35000, "K"), (150000, "L"),
          (500000, "M"), (float("inf"), "N")],
    "II": [(8, "A"), (15, "B"), (25, "C"), (50, "D"), (90, "E"), (150, "F"), (280, "G"),
           (500, "H"), (1200, "J"), (3200, "K"), (10000, "L"), (35000, "M"), (150000, "N"),
           (500000, "P"), (float("inf"), "Q")],
    "III": [(8, "B"), (15, "C"), (25, "D"), (50, "E"), (90, "F"), (150, "G"), (280, "H"),
            (500, "J"), (1200, "K"), (3200, "L"), (10000, "M"), (35000, "N"), (150000, "P"),
            (500000, "Q"), (float("inf"), "R")],
}
AQLS = [0.065, 0.10, 0.15, 0.25, 0.40, 0.65, 1.0, 1.5, 2.5, 4.0, 6.5]
SECUENCIA = [(0, 1), "up", "down", (1, 2), (2, 3), (3, 4), (5, 6), (7, 8), (10, 11), (14, 15), (21, 22)]


def plan_aql(letra_idx, aql):
    """Devuelve (letra, muestra, Ac, Re) resolviendo las flechas de la tabla II-A."""
    if aql not in AQLS:
        raise ValueError(f"AQL {aql} no soportado. Usa uno de {AQLS}")
    cero = AQLS.index(6.5) - AQLS.index(aql)
    i = letra_idx
    for _ in range(40):
        pos = i - cero
        if pos < 0:
            i += 1
            continue
        if pos >= len(SECUENCIA):
            i -= 1
            continue
        s = SECUENCIA[pos]
        if s == "down":
            i += 1
        elif s == "up":
            i -= 1
        else:
            i = max(0, min(i, len(LETRAS) - 1))
            return LETRAS[i], MUESTRAS[i], s[0], s[1]
    raise RuntimeError("No se pudo resolver el plan")


def letra_codigo(lote, nivel="II"):
    return next(l for lim, l in NIVELES[nivel] if lote <= lim)


def cmd_aql(a):
    letra = letra_codigo(a.lote, a.nivel)
    idx = LETRAS.index(letra)
    print(f"## Plan AQL — lote {a.lote:,} unidades, nivel general {a.nivel} "
          f"(letra de código {letra}, muestra base {MUESTRAS[idx]})\n")
    rows = [["Crítico", "0", MUESTRAS[idx], 0, 1]]
    for nombre, val in (("Mayor", a.mayor), ("Menor", a.menor)):
        l, n, ac, re_ = plan_aql(idx, val)
        rows.append([nombre, val, n, ac, re_])
    print(table(["Defecto", "AQL", "Unidades a revisar", "Acepta con ≤", "Rechaza con ≥"], rows))
    max_n = max(r[2] for r in rows)
    if max_n >= a.lote:
        print(f"\n- La muestra ({max_n}) iguala o supera el lote: revisar el 100% de las unidades.")
    print("\n- Crítico: cualquier defecto de seguridad o normativo rechaza el lote.")
    print("- Si un plan usa una muestra mayor que otro, se revisan las unidades del plan mayor "
          "y se aplican los números de aceptación de cada tipo de defecto.")


# =========================================================================== tallas

# EU (= 码 chino) -> largo de pie aprox. en mm (tabla china usual), US hombre, US mujer, UK. Aproximado.
ZAPATOS = [
    (35, 225, 3.5, 5.0, 2.5), (36, 230, 4.5, 6.0, 3.5), (37, 235, 5.0, 6.5, 4.0),
    (38, 240, 6.0, 7.5, 5.0), (39, 245, 6.5, 8.0, 5.5), (40, 250, 7.5, 9.0, 6.5),
    (41, 255, 8.0, 9.5, 7.0), (42, 260, 9.0, 10.5, 8.0), (43, 265, 9.5, 11.0, 8.5),
    (44, 270, 10.5, 12.0, 9.5), (45, 275, 11.0, 12.5, 10.0), (46, 280, 12.0, 13.5, 11.0),
    (47, 285, 13.0, None, 12.0),
]
HOLGURAS = {"ajustado": 4, "regular": 10, "holgado": 20}


def talla_zapato(eu=None, mm=None, us_h=None, us_m=None, uk=None):
    if mm is not None:
        cand = [z for z in ZAPATOS if z[1] >= mm]
        return cand[0] if cand else ZAPATOS[-1]
    for idx, val in ((0, eu), (2, us_h), (3, us_m), (4, uk)):
        if val is not None:
            return min((z for z in ZAPATOS if z[idx] is not None), key=lambda z: abs(z[idx] - val))
    return None


def elegir_talla_ropa(tabla, medida_cuerpo, holgura, plano=False):
    """tabla: {'M': 52, ...} medida de la prenda (plano = ancho en plano, se multiplica ×2)."""
    filas = []
    elegida = None
    for talla, v in tabla.items():
        circ = v * 2 if plano else v
        h = circ - medida_cuerpo
        filas.append((talla, circ, h))
        if elegida is None and h >= holgura:
            elegida = talla
    return elegida, filas


def cmd_talla(a):
    if a.modo == "zapato":
        z = talla_zapato(a.eu, a.pie_mm, a.us_hombre, a.us_mujer, a.uk)
        if not z:
            sys.exit("Indica --eu, --pie-mm, --us-hombre, --us-mujer o --uk.")
        print("## Talla de calzado (aproximada)\n")
        print(table(["EU / 码 chino", "Pie (mm, tabla china)", "US hombre", "US mujer", "UK"],
                    [[z[0], z[1], z[2], z[3] if z[3] else "—", z[4]]]))
        print("\n- En Chile y la mayoría de Latinoamérica se usa la numeración EU.")
        print("- Lo más seguro: mide tu pie (talón a punta, de pie, en mm) y compáralo con el 脚长 "
              "de la tabla del vendedor. Si la tabla da 内长 (largo interior), suma 5–10 mm a tu pie.")
        print("- Cada marca/horma varía; lee reseñas: 偏大 = talla grande, 偏小 = talla chica, 正码 = normal.")
    elif a.modo == "ropa":
        tabla = {}
        for par in a.tabla.split(","):
            t, v = par.split(":")
            tabla[t.strip()] = float(v)
        holg = HOLGURAS.get(a.calce, 10) if a.holgura is None else a.holgura
        el, filas = elegir_talla_ropa(tabla, a.medida, holg, a.plano)
        print(f"## Talla de ropa — tu medida {a.medida} cm, holgura deseada {holg} cm ({a.calce})\n")
        print(table(["Talla", "Contorno de la prenda (cm)", "Holgura resultante (cm)"],
                    [[t, fmt(c, 1), fmt(h, 1)] for t, c, h in filas]))
        if el:
            print(f"\n- Recomendación: **{el}**.")
        else:
            t, c, h = max(filas, key=lambda f: f[2])
            print(f"\n- Ninguna talla llega a {fmt(holg, 0)} cm de holgura. La más cercana es **{t}** "
                  f"({fmt(h, 1)} cm): pide una talla mayor si existe, o acepta {t} con un calce algo más justo.")
        print("- 平铺 = medida en plano (usa --plano: se multiplica ×2). Las tallas chinas suelen ser "
              "1–2 tallas menores que las latinoamericanas: guíate por centímetros, no por la letra.")
    elif a.modo == "peso":
        if a.jin is not None:
            print(f"- {fmt(a.jin, 1)} 斤 = {fmt(a.jin * 0.5, 1)} kg (1 斤 = 500 g; 1 两 = 50 g; 1 公斤 = 1 kg = 2 斤)")
        if a.kg is not None:
            print(f"- {fmt(a.kg, 1)} kg = {fmt(a.kg * 2, 1)} 斤")
        if a.jin is None and a.kg is None:
            sys.exit("Indica --jin o --kg.")


# =========================================================================== main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--version", action="version", version=VERSION)
    sub = ap.add_subparsers(dest="cmd")
    sub.required = True

    s = sub.add_parser("tc", help="Tipos de cambio del día")
    s.add_argument("--monedas", default="CNY,CLP,MXN,PEN,COP,ARS,UYU,EUR,BRL")
    s.add_argument("--offline", action="store_true", help="No consultar internet")
    s.add_argument("--forzar", action="store_true", help="Ignorar caché")
    s.set_defaults(func=cmd_tc)

    s = sub.add_parser("convertir", help="Convertir montos entre monedas")
    s.add_argument("monto", type=float)
    s.add_argument("de", help="Moneda origen (CNY, USD, CLP...)")
    s.add_argument("a", help="Moneda(s) destino, separadas por coma")
    s.add_argument("--recargo", type=float, default=0.0, help="Diferencial del medio de pago en %% (ej. 3.5)")
    s.add_argument("--tc-agente", type=float, help="CNY por USD que usa tu agente, para medir su recargo")
    s.add_argument("--offline", action="store_true")
    s.set_defaults(func=cmd_convertir)

    s = sub.add_parser("enlace", help="Identificar y convertir links entre plataformas y agentes")
    s.add_argument("link", nargs="+", help="Link o texto compartido desde la app")
    s.add_argument("--agentes", help="Filtrar agentes (ej. kakobuy,superbuy)")
    s.add_argument("--todos", action="store_true", help="Incluir agentes cerrados o en riesgo")
    s.add_argument("--resolver", action="store_true", help="Seguir links cortos (requiere internet)")
    s.add_argument("--plataforma", help="Si solo tienes el número: taobao|weidian|1688")
    s.set_defaults(func=cmd_enlace)

    s = sub.add_parser("precios", help="Rango de precios de referencia")
    s.add_argument("precios", nargs="+", type=float, help="Precios unitarios comparables")
    s.add_argument("--moneda", default="CNY")
    s.add_argument("--tc", help="CNY por USD o 'auto'")
    s.add_argument("--umbral-bajo", type=float, default=0.70, help="Fracción de la mediana (0.70)")
    s.add_argument("--umbral-alto", type=float, default=1.50, help="Fracción de la mediana (1.50)")
    s.set_defaults(func=cmd_precios)

    s = sub.add_parser("comparar", help="Puntaje de proveedores desde CSV")
    s.add_argument("csv", help="CSV con columnas de assets/comparador_proveedores.csv")
    s.add_argument("--unidades", type=int, required=True)
    s.add_argument("--tc", help="CNY por USD o 'auto'")
    s.add_argument("--umbral-bajo", type=float, default=0.70)
    s.set_defaults(func=cmd_comparar)

    s = sub.add_parser("peso", help="Peso volumétrico y cobrable")
    s.add_argument("--largo", type=float, required=True, help="cm")
    s.add_argument("--ancho", type=float, required=True, help="cm")
    s.add_argument("--alto", type=float, required=True, help="cm")
    s.add_argument("--peso-real", type=float, required=True, help="kg por caja")
    s.add_argument("--cajas", type=int, default=1)
    s.add_argument("--divisor", type=float, help="Divisor adicional (ej. 7000)")
    s.set_defaults(func=cmd_peso)

    s = sub.add_parser("lineas", help="Comparar líneas de envío para un paquete")
    s.add_argument("csv", help="CSV con columnas de assets/lineas_envio.csv")
    s.add_argument("--peso-real", type=float, required=True, help="kg del paquete")
    s.add_argument("--largo", type=float, help="cm")
    s.add_argument("--ancho", type=float, help="cm")
    s.add_argument("--alto", type=float, help="cm")
    s.add_argument("--tc", default="auto", help="CNY por USD o 'auto'")
    s.set_defaults(func=cmd_lineas)

    s = sub.add_parser("costo", help="Costo puesto en destino")
    s.add_argument("--pais", choices=sorted(PRESETS), default="chile")
    s.add_argument("--precio-cny", type=float, required=True, help="Precio unitario en CNY")
    s.add_argument("--unidades", type=int, required=True)
    s.add_argument("--tc", default="auto", help="CNY por USD, o 'auto' (por defecto)")
    s.add_argument("--extras-cny", type=float, default=0.0, help="Muestras, logo, molde, empaque (total)")
    s.add_argument("--flete-china-cny", type=float, default=0.0, help="Flete interno a la bodega (total)")
    s.add_argument("--comision-pct", type=float, default=0.0, help="Comisión del agente sobre producto")
    s.add_argument("--pago-pct", type=float, default=0.0,
                   help="Recargo del medio de pago + diferencial cambiario (PayPal ~3-5)")
    s.add_argument("--flete-usd", type=float, help="Flete internacional total en USD")
    s.add_argument("--kg", type=float, help="Kg cobrables (alternativa a --flete-usd)")
    s.add_argument("--usd-kg", type=float, help="USD por kg")
    s.add_argument("--cargo-fijo-usd", type=float, default=0.0, help="Cargo fijo del envío")
    s.add_argument("--seguro-pct", type=float, default=0.0, help="Seguro contratado, %% del FOB")
    s.add_argument("--arancel-pct", type=float, help="Sobrescribe el arancel del preset")
    s.add_argument("--arancel-fijo-usd", type=float, default=0.0, help="Arancel fijo (ej. EUR 3/línea UE)")
    s.add_argument("--iva-pct", type=float, help="Sobrescribe el IVA del preset")
    s.add_argument("--base", choices=["cif", "fob"], help="Base del arancel")
    s.add_argument("--impuestos-incluidos", action="store_true", help="Línea DDP con impuestos incluidos")
    s.add_argument("--gastos-locales-usd", type=float, default=0.0,
                   help="Agente de aduana, gestión courier, transporte local")
    s.add_argument("--tc-local", help="Moneda local por USD, o 'auto'")
    s.add_argument("--moneda-local", help="Código de la moneda local (CLP, MXN...)")
    s.add_argument("--precio-venta", type=float, help="Precio de venta unitario final en moneda local")
    s.add_argument("--iva-venta-pct", type=float, help="IVA de la venta (por defecto el del preset)")
    s.add_argument("--empresa", action="store_true",
                   help="Importa con empresa: el IVA de importación es crédito fiscal")
    s.set_defaults(func=cmd_costo)

    s = sub.add_parser("aql", help="Plan de muestreo AQL")
    s.add_argument("--lote", type=int, required=True, help="Unidades del lote")
    s.add_argument("--mayor", type=float, default=2.5)
    s.add_argument("--menor", type=float, default=4.0)
    s.add_argument("--nivel", choices=["I", "II", "III"], default="II")
    s.set_defaults(func=cmd_aql)

    s = sub.add_parser("talla", help="Tallas de calzado, ropa y 斤/kg")
    s.add_argument("modo", choices=["zapato", "ropa", "peso"])
    s.add_argument("--eu", type=float)
    s.add_argument("--pie-mm", type=float, help="Largo del pie en mm")
    s.add_argument("--us-hombre", type=float)
    s.add_argument("--us-mujer", type=float)
    s.add_argument("--uk", type=float)
    s.add_argument("--tabla", help="Medidas de la prenda por talla, ej. 'M:52,L:55,XL:58'")
    s.add_argument("--plano", action="store_true", help="La tabla es en plano (平铺): ×2")
    s.add_argument("--medida", type=float, help="Tu contorno corporal en cm (pecho, cintura...)")
    s.add_argument("--calce", choices=sorted(HOLGURAS), default="regular")
    s.add_argument("--holgura", type=float, help="Holgura en cm (sobrescribe --calce)")
    s.add_argument("--jin", type=float)
    s.add_argument("--kg", type=float)
    s.set_defaults(func=cmd_talla)

    a = ap.parse_args()
    if a.cmd == "talla" and a.modo == "ropa" and (not a.tabla or a.medida is None):
        ap.error("talla ropa requiere --tabla y --medida")
    a.func(a)


if __name__ == "__main__":
    main()
