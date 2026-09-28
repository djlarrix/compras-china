"""Pruebas de scripts/china_tools.py.  Ejecutar:  python3 -m unittest evals/test_china_tools.py -v
(desde la carpeta de la skill). No requieren internet: los tipos de cambio se pasan fijos."""

import argparse
import contextlib
import io
import os
import subprocess
import sys
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(AQUI, "..", "scripts", "china_tools.py")
sys.path.insert(0, os.path.join(AQUI, "..", "scripts"))
import china_tools as ct  # noqa: E402


def ns_costo(**kw):
    base = dict(pais="chile", precio_cny=10.0, unidades=100, tc=6.72, extras_cny=0.0, flete_china_cny=0.0,
                comision_pct=0.0, pago_pct=0.0, flete_usd=0.0, kg=None, usd_kg=None, cargo_fijo_usd=0.0,
                seguro_pct=0.0, arancel_pct=None, arancel_fijo_usd=0.0, iva_pct=None, base=None,
                impuestos_incluidos=False, gastos_locales_usd=0.0, tc_local=None, moneda_local=None,
                precio_venta=None, iva_venta_pct=None, empresa=False)
    base.update(kw)
    return argparse.Namespace(**base)


def run_cli(*args):
    r = subprocess.run([sys.executable, SCRIPT] + list(args), capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


class TestEnlaces(unittest.TestCase):
    casos = [
        ("https://weidian.com/item.html?itemID=7234567890&wfr=c", "weidian", "7234567890"),
        ("https://shop1234.v.weidian.com/item.html?itemID=5555555555", "weidian", "5555555555"),
        ("https://item.taobao.com/item.htm?spm=a1z10&id=712345678901", "taobao", "712345678901"),
        ("https://detail.tmall.com/item.htm?id=623456789012&skuId=1", "taobao", "623456789012"),
        ("https://detail.1688.com/offer/654321987654.html?spm=x", "1688", "654321987654"),
        ("https://item.jd.com/100012043978.html", "jd", "100012043978"),
        ("https://www.goofish.com/item?id=801234567890", "xianyu", "801234567890"),
        ("https://mobile.yangkeduo.com/goods.html?goods_id=412345678", "pdd", "412345678"),
        ("https://www.kakobuy.com/item/details?url=https%3A%2F%2Fweidian.com%2Fitem.html%3FitemID%3D7234567890&affcode=x",
         "weidian", "7234567890"),
        ("https://www.superbuy.com/en/page/buy/?url=https%3A%2F%2Fitem.taobao.com%2Fitem.htm%3Fid%3D712345678901",
         "taobao", "712345678901"),
        ("https://www.sugargoo.com/productDetail?productLink=https%3A%2F%2Fdetail.1688.com%2Foffer%2F654321987654.html",
         "1688", "654321987654"),
        ("https://cnfans.com/product/?shop_type=ali_1688&id=654321987654", "1688", "654321987654"),
        ("https://mulebuy.com/product/?shop_type=weidian&id=7234567890", "weidian", "7234567890"),
        ("https://joyabuy.com/product/?shop_type=taobao&id=712345678901", "taobao", "712345678901"),
        ("https://hoobuy.com/product/2/7234567890", "weidian", "7234567890"),
        ("https://hoobuy.com/product/0/654321987654", "1688", "654321987654"),
        ("https://usfans.com/product/3/7234567890", "weidian", "7234567890"),
        ("https://www.litbuy.com/product/1/712345678901", "taobao", "712345678901"),
        ("https://www.cssbuy.com/item-micro-7234567890.html", "weidian", "7234567890"),
        ("https://www.cssbuy.com/item-1688-654321987654.html", "1688", "654321987654"),
        ("https://www.cssbuy.com/item-712345678901.html", "taobao", "712345678901"),
        ("https://oopbuy.com/goods/details?id=712345678901&channel=taobao", "taobao", "712345678901"),
        ("https://rizzitgo.com/detail-page?goodsId=7234567890&source=3", "weidian", "7234567890"),
        ("https://www.acbuy.com/product?id=7234567890&source=WD", "weidian", "7234567890"),
        ("https://www.eastmallbuy.com/1688ID=654321987654", "1688", "654321987654"),
        ("weidian.com/item.html?itemID=7234567890", "weidian", "7234567890"),
    ]

    def test_analizar(self):
        for link, plat, pid in self.casos:
            with self.subTest(link=link):
                r = ct.analizar_enlace(link)
                self.assertIsNotNone(r)
                self.assertEqual(r["plataforma"], plat)
                self.assertEqual(r["id"], pid)

    def test_texto_compartido_con_link_corto(self):
        r = ct.analizar_enlace("【淘宝】https://m.tb.cn/h.5abcd?tk=xyz 「T恤」点击链接直接打开")
        self.assertIsNone(r["plataforma"])
        self.assertIn("corto", r)

    def test_numero_solo(self):
        r = ct.analizar_enlace("7234567890")
        self.assertIsNone(r["plataforma"])
        self.assertEqual(r["id"], "7234567890")

    def test_ida_y_vuelta(self):
        """Cada link generado para un agente debe volver a analizarse al mismo producto."""
        for plat, pid in (("weidian", "7234567890"), ("taobao", "712345678901"), ("1688", "654321987654")):
            canon, lista = ct.enlaces_agentes(plat, pid)
            self.assertGreaterEqual(len(lista), 20)
            for nombre, link, _ in lista:
                with self.subTest(agente=nombre, plataforma=plat):
                    r = ct.analizar_enlace(link)
                    self.assertIsNotNone(r, link)
                    self.assertEqual((r["plataforma"], r["id"]), (plat, pid), link)

    def test_sin_codigos_de_afiliado(self):
        for plat in ("weidian", "taobao", "1688"):
            _, lista = ct.enlaces_agentes(plat, "123456789")
            for _, link, _ in lista:
                self.assertNotIn("aff", link.lower())

    def test_agentes_cerrados_marcados(self):
        self.assertIn("CERRADO", ct.AGENTES["CNFans"][1])
        self.assertIn("RIESGO", ct.AGENTES["Mulebuy"][1])


class TestMoneda(unittest.TestCase):
    tasas = {"USD": 1.0, "CNY": 6.72, "CLP": 960.0}

    def test_convertir(self):
        self.assertAlmostEqual(ct.convertir_monto(672, "CNY", "USD", self.tasas), 100.0)
        self.assertAlmostEqual(ct.convertir_monto(100, "USD", "CLP", self.tasas), 96000.0)
        self.assertAlmostEqual(ct.convertir_monto(1, "CNY", "CLP", self.tasas), 960 / 6.72)

    def test_moneda_desconocida(self):
        with self.assertRaises(KeyError):
            ct.convertir_monto(1, "XXX", "USD", self.tasas)

    def test_resolver_tc_numero(self):
        self.assertEqual(ct.resolver_tc("6,8", "CNY", []), 6.8)

    def test_offline(self):
        tasas, fuente, fecha = ct.obtener_tasas(offline=True)
        self.assertIn("offline", fuente)
        self.assertGreater(tasas["CNY"], 5)
        self.assertGreater(tasas["CLP"], 500)


class TestCosto(unittest.TestCase):
    def test_chile_ejemplo_oficial_aduana(self):
        # CIF USD 1.000 → arancel 60 → IVA 201,40 (ejemplo de aduana.cl)
        c = ct.calcular_costo(ns_costo(precio_cny=6.72, unidades=1000, seguro_pct=1e-9))
        self.assertAlmostEqual(c["cif"], 1000.0, places=2)
        self.assertAlmostEqual(c["arancel"], 60.0, places=2)
        self.assertAlmostEqual(c["iva"], 201.40, places=2)

    def test_chile_seguro_presunto(self):
        c = ct.calcular_costo(ns_costo(precio_cny=6.72, unidades=1000))
        self.assertAlmostEqual(c["cif"], 1020.0, places=2)

    def test_chile_tlc_sin_arancel(self):
        c = ct.calcular_costo(ns_costo(pais="chile-tlc", precio_cny=6.72, unidades=1000, seguro_pct=1e-9))
        self.assertEqual(c["arancel"], 0)
        self.assertAlmostEqual(c["iva"], 190.0, places=2)

    def test_ddp(self):
        c = ct.calcular_costo(ns_costo(impuestos_incluidos=True, flete_usd=50))
        self.assertEqual(c["arancel"] + c["iva"], 0)

    def test_peru_franquicia(self):
        c = ct.calcular_costo(ns_costo(pais="peru", precio_cny=13.44, unidades=100))  # FOB 200
        self.assertEqual(c["arancel"] + c["iva"], 0)
        c = ct.calcular_costo(ns_costo(pais="peru", precio_cny=13.44, unidades=101))
        self.assertGreater(c["iva"], 0)

    def test_argentina_franquicia_400(self):
        c = ct.calcular_costo(ns_costo(pais="argentina", precio_cny=26.88, unidades=100))  # FOB 400
        self.assertEqual(c["arancel"], 0)
        self.assertGreater(c["iva"], 0)
        c = ct.calcular_costo(ns_costo(pais="argentina", precio_cny=53.76, unidades=100))  # FOB 800
        self.assertAlmostEqual(c["arancel"], 800 * 0.5 * 0.20, places=2)

    def test_ecuador_fijo(self):
        c = ct.calcular_costo(ns_costo(pais="ecuador-4x4", precio_cny=10, unidades=10))
        self.assertAlmostEqual(c["arancel"], 20.0)

    def test_empresa_descuenta_iva(self):
        c = ct.calcular_costo(ns_costo(empresa=True, flete_usd=100))
        self.assertAlmostEqual(c["unit_neto"] * 100, c["total"] - c["iva"], places=6)

    def test_totales_cuadran(self):
        c = ct.calcular_costo(ns_costo(pago_pct=3.5, comision_pct=5, flete_china_cny=30, flete_usd=80,
                                       seguro_pct=1, gastos_locales_usd=20))
        esperado = ((c["prod_cny"] + c["flete_cn"] + c["comision"] + c["pago"]) / 6.72 + c["flete_int"]
                    + c["seguro"] + c["arancel"] + c["iva"] + 20)
        self.assertAlmostEqual(c["total"], esperado, places=6)


class TestAQL(unittest.TestCase):
    # (lote, AQL) -> (muestra, Ac, Re), valores de ISO 2859-1 tabla II-A, nivel II
    casos = [
        (1200, 2.5, (80, 5, 6)), (1200, 4.0, (80, 7, 8)), (1200, 1.0, (80, 2, 3)),
        (500, 2.5, (50, 3, 4)), (500, 4.0, (50, 5, 6)), (3000, 2.5, (125, 7, 8)),
        (5000, 2.5, (200, 10, 11)), (100, 2.5, (20, 1, 2)), (100, 4.0, (20, 2, 3)),
        (60, 2.5, (20, 1, 2)), (40, 2.5, (5, 0, 1)), (60, 4.0, (13, 1, 2)),
        (20, 1.0, (13, 0, 1)), (20000, 2.5, (315, 14, 15)), (200, 0.65, (20, 0, 1)),
        (1200, 0.65, (80, 1, 2)), (1200, 6.5, (80, 10, 11)),
    ]

    def test_planes(self):
        for lote, aql, esperado in self.casos:
            with self.subTest(lote=lote, aql=aql):
                idx = ct.LETRAS.index(ct.letra_codigo(lote))
                _, n, ac, re_ = ct.plan_aql(idx, aql)
                self.assertEqual((n, ac, re_), esperado)

    def test_letras(self):
        self.assertEqual(ct.letra_codigo(1200), "J")
        self.assertEqual(ct.letra_codigo(1201), "K")
        self.assertEqual(ct.letra_codigo(8), "A")
        self.assertEqual(ct.letra_codigo(300, "I"), "F")
        self.assertEqual(ct.letra_codigo(300, "III"), "J")


class TestPesoYLineas(unittest.TestCase):
    def test_peso(self):
        cob, vol, real = ct.peso_cobrable(60, 40, 40, 12, 5000, 5)
        self.assertAlmostEqual(vol, 96.0)
        self.assertAlmostEqual(cob, 96.0)
        cob, vol, real = ct.peso_cobrable(20, 20, 20, 5, 6000)
        self.assertAlmostEqual(cob, 5.0)

    def test_linea_escalonada(self):
        fila = {"divisor": "8000", "primer_peso_g": "500", "precio_primer": "150", "continuo_g": "500",
                "precio_continuo": "55", "cargo_fijo": "0", "moneda": "CNY", "peso_max_kg": "20"}
        c = ct.costo_linea(fila, 4.2, (45, 35, 25), 6.72)
        self.assertAlmostEqual(c["cobrable"], 45 * 35 * 25 / 8000)
        self.assertEqual(c["costo"], 150 + 9 * 55)

    def test_linea_peso_real_y_usd(self):
        fila = {"divisor": "0", "primer_peso_g": "1000", "precio_primer": "12", "continuo_g": "1000",
                "precio_continuo": "12", "cargo_fijo": "5", "moneda": "USD", "peso_max_kg": "3"}
        c = ct.costo_linea(fila, 3.0, (100, 100, 100), 6.72)
        self.assertEqual(c["costo"], 12 + 2 * 12 + 5)
        self.assertFalse(c["excede"])
        c = ct.costo_linea(fila, 3.5, None, 6.72)
        self.assertTrue(c["excede"])


class TestTallas(unittest.TestCase):
    def test_zapato(self):
        self.assertEqual(ct.talla_zapato(eu=40)[1], 250)
        self.assertEqual(ct.talla_zapato(mm=262)[0], 43)
        self.assertEqual(ct.talla_zapato(mm=250)[0], 40)
        self.assertEqual(ct.talla_zapato(us_h=9)[0], 42)

    def test_ropa(self):
        el, _ = ct.elegir_talla_ropa({"M": 52, "L": 55, "XL": 58}, 100, 10, plano=True)
        self.assertEqual(el, "L")
        el, _ = ct.elegir_talla_ropa({"M": 104, "L": 110}, 100, 20)
        self.assertIsNone(el)


class TestPuntaje(unittest.TestCase):
    def test_sospechoso_y_orden(self):
        buena = {"tipo": "fabrica", "insignia": "super", "anos": "8", "recompra_pct": "38", "estrellas": "4.8",
                 "respuesta_min": "3", "muestra_ok": "si", "video_ok": "si", "precio_cny": "13.5"}
        mala = {"tipo": "desconocido", "insignia": "ninguna", "anos": "0.5", "recompra_pct": "5",
                "estrellas": "4.9", "respuesta_min": "60", "muestra_ok": "no", "video_ok": "no", "precio_cny": "8.2"}
        pb, fb = ct.puntaje_proveedor(buena, 12.8)
        pm, fm = ct.puntaje_proveedor(mala, 12.8)
        self.assertGreater(pb, pm)
        self.assertIn("precio sospechoso", fm)
        self.assertIn("tienda nueva", fm)
        self.assertLessEqual(pb, 100)


class TestCLI(unittest.TestCase):
    """Cada subcomando corre de punta a punta sin errores (modo sin internet donde aplica)."""

    def test_subcomandos(self):
        csvp = os.path.join(AQUI, "..", "assets", "comparador_proveedores.csv")
        lin = os.path.join(AQUI, "..", "assets", "lineas_envio.csv")
        comandos = [
            ["tc", "--offline"],
            ["convertir", "100", "CNY", "CLP,USD", "--offline", "--recargo", "3"],
            ["enlace", "https://weidian.com/item.html?itemID=7234567890"],
            ["precios", "12.5", "13", "11.8", "14.2", "8.1", "--tc", "6.7"],
            ["comparar", csvp, "--unidades", "300", "--tc", "6.7"],
            ["peso", "--largo", "60", "--ancho", "40", "--alto", "40", "--peso-real", "12"],
            ["lineas", lin, "--peso-real", "4.2", "--largo", "45", "--ancho", "35", "--alto", "25", "--tc", "6.7"],
            ["costo", "--precio-cny", "12.8", "--unidades", "300", "--tc", "6.7", "--flete-usd", "300",
             "--tc-local", "960", "--precio-venta", "9990"],
            ["aql", "--lote", "1200"],
            ["talla", "zapato", "--eu", "42"],
            ["talla", "ropa", "--tabla", "M:52,L:55", "--plano", "--medida", "98"],
            ["talla", "peso", "--jin", "120"],
        ]
        for c in comandos:
            with self.subTest(cmd=" ".join(c[:2])):
                code, out = run_cli(*c)
                self.assertEqual(code, 0, out)
                self.assertTrue(out.strip())


if __name__ == "__main__":
    unittest.main()
