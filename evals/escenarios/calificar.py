"""Califica las respuestas de escenario contra criterios objetivos (regex) y escribe grading.json.
Uso: python3 evals/escenarios/calificar.py evals/escenarios"""
import json
import re
import sys
from pathlib import Path

AQUI = Path(sys.argv[1])
CJK = r"(?m)^(?=(?:[^\n]*?[\u4e00-\u9fff]){15})[^\n]+$"  # una línea con 15+ caracteres chinos

CRITERIOS = {
    "eval-1-termos-chile": [
        ("Incluye mensaje en chino listo para copiar", CJK),
        ("Pide acero 304 y certificado de material", r"304.*材质证明|材质证明.*304"),
        ("Apunta al clúster correcto (Yongkang)", r"Yongkang|永康"),
        ("Da referencia de precio con mediana y alerta de oferta sospechosa", r"mediana.*sospech|sospech.*mediana"),
        ("Compara aéreo vs marítimo con costo por unidad en CLP", r"Por unidad.*\$7\.4\d\d.*\$4\.2\d\d"),
        ("Calcula margen contra el precio de venta", r"Margen.*25,7%.*57,3%"),
        ("Menciona Form F / TLC para arancel 0%", r"Form F"),
        ("Incluye IVA 19% y arancel 6%", r"IVA 19%|19%.*IVA"),
        ("Plan AQL correcto para 300 (50 unidades, Ac 3 mayor)", r"50 unidades.*≤3"),
        ("Advierte contacto con alimentos / grado alimentario", r"食品级|grado alimentario"),
        ("Considera el calendario chino (Semana Dorada)", r"Semana Dorada"),
        ("Termina con siguiente acción", r"Siguiente acción"),
    ],
    "eval-2-responder-vendedor": [
        ("Traduce el mensaje del vendedor", r"Traducción"),
        ("Interpreta 已经是最低价了 como posición inicial", r"最低价.*posición inicial"),
        ("Explica 包邮 y la muestra no reembolsable", r"包邮.*(muestra|样品)"),
        ("Respuesta en chino lista para copiar", CJK),
        ("Traduce su propia respuesta al español", r"> Entiendo, jefe"),
        ("Propone contrapartidas (volumen, repuestos, muestra descontable)", r"repuesto.*descont|descont.*repuesto"),
        ("Recomienda 改价 y dejar evidencia en el chat de 1688", r"改价.*1688|1688.*改价"),
        ("Da meta de precio realista con cálculo", r"12,5"),
    ],
    "eval-3-comparar-mochilas": [
        ("Tabla comparativa con puntaje", r"\| Puntaje \|"),
        ("Descarta la tienda nueva por precio sospechoso", r"Descarta la tienda nueva"),
        ("Recomienda muestras de 2 proveedores", r"muestras a Baigou y a Guangzhou"),
        ("Pago dentro de 1688 para mantener custodia", r"dentro de 1688"),
        ("Si hay transferencia: cuenta de empresa y 30/70", r"cuenta de empresa.*30%"),
        ("Menciona no confirmar recepción / 延长收货", r"延长收货"),
        ("Plan AQL correcto para 500 (50 unidades)", r"revisar 50 mochilas"),
        ("Menciona Trade Assurance como alternativa", r"Trade Assurance"),
    ],
    "eval-4-link-cnfans": [
        ("Explica que CNFans cerró", r"CNFans cerró"),
        ("Entrega el link original de Weidian", r"https://weidian\.com/item\.html\?itemID=7234567890"),
        ("Entrega link correcto de Kakobuy",
         re.escape("https://www.kakobuy.com/item/details?url=https%3A%2F%2Fweidian.com%2Fitem.html%3FitemID%3D7234567890")),
        ("Advierte riesgo de Mulebuy", r"Mulebuy"),
        ("Calcula peso volumétrico (6 kg /5000)", r"6 kg"),
        ("Recomienda rehearsal / reducir volumen", r"rehearsal"),
        ("Menciona recargo cambiario del agente", r"recargo cambiario"),
        ("Aduana Chile: 6% + 19% y fin de franquicia USD 41", r"6% de arancel \+ 19% de IVA.*USD 41"),
        ("Consejo de proteger saldo", r"Carga saldo solo"),
    ],
    "eval-5-talla-y-pesos": [
        ("Convierte ¥89 a CLP con tipo del día", r"\$12\.745"),
        ("Muestra monto con recargo", r"\$13\.255"),
        ("Explica 平铺 ×2", r"平铺.*doble"),
        ("Tabla de holgura por talla", r"\| XL \| 116"),
        ("Recomienda XL/2XL con razonamiento de holgura", r"2XL"),
        ("Pregunta al vendedor en chino", CJK),
        ("Menciona 偏小 en reseñas", r"偏小"),
    ],
    "eval-6-peru-fundas": [
        ("Aplica umbral USD 200 FOB de Perú", r"USD 200"),
        ("Concluye sin tributos para 150 unidades", r"no pagas tributos"),
        ("Costo por funda en soles", r"S/ 4,35"),
        ("Escenario sobre umbral con ad valorem + IGV 16% + IPM 2%", r"IGV 16%.*IPM 2%"),
        ("Menciona TLC Perú–China", r"TLC Perú–China"),
        ("Advierte cambio pendiente de SUNAT", r"SUNAT ha planteado"),
        ("Advierte sobre fraccionamiento", r"fraccionamiento"),
        ("Tipo de cambio con fecha", r"28-sep-2026"),
    ],
}

total_ok = total = 0
resumen = []
for carpeta, criterios in CRITERIOS.items():
    texto = (AQUI / carpeta / "respuesta.md").read_text(encoding="utf-8")
    exps = []
    for nombre, patron in criterios:
        m = re.search(patron, texto, re.S)
        exps.append({"text": nombre, "passed": bool(m),
                     "evidence": (m.group(0)[:120].replace("\n", " ") if m else "no encontrado")})
    ok = sum(e["passed"] for e in exps)
    total_ok += ok
    total += len(exps)
    (AQUI / carpeta / "grading.json").write_text(json.dumps({"expectations": exps}, ensure_ascii=False, indent=2),
                                                  encoding="utf-8")
    resumen.append((carpeta, ok, len(exps), [e["text"] for e in exps if not e["passed"]]))

for c, ok, n, fallas in resumen:
    print(f"{c}: {ok}/{n}" + (f"  FALLAS: {fallas}" if fallas else ""))
print(f"TOTAL: {total_ok}/{total} ({100 * total_ok / total:.0f}%)")
sys.exit(0 if total_ok == total else 1)
