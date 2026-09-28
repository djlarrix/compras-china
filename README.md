# compras-china

Skill para Claude que actúa como **agente de compra, traductor, negociador, comparador y agente de envío** para comprar en China: 1688, Taobao, Tmall, Weidian, Pinduoduo, JD, Xianyu, Dewu y Alibaba.com, directo con fábricas o vía agentes (Kakobuy, Superbuy, CSSBuy, Sugargoo, Hoobuy, Oopbuy, Joyagoo y otros) y casillas. Escrita en español, con foco en Chile y Latinoamérica.

## Qué hace

- **Buscar y verificar proveedores**: palabras clave en chino, búsqueda por imagen, clústeres industriales, insignias y métricas de 1688, triage fábrica vs revendedor, banderas rojas.
- **Precios de referencia y comparación**: rango normal, ofertas sospechosas, puntaje de proveedores.
- **Traducir y negociar**: plantillas en chino con traducción, cómo leer las respuestas del vendedor, mensajes al agente en inglés y chino.
- **Calidad**: trampas por categoría, muestras y muestra dorada, fotos QC, inspección AQL.
- **Agentes**: directorio de 25+ agentes con su estado a septiembre de 2026 (cierres de Pandabuy, CNFans y ACBuy; riesgo en Mulebuy), costo real y cómo proteger tu saldo.
- **Links**: convierte cualquier link de plataforma o de agente al formato de 22 agentes activos y recupera el link original, sin códigos de afiliado.
- **Moneda**: tipo de cambio del día (CNY, CLP, MXN, PEN, COP, ARS, EUR…) y recargo real de PayPal o del agente.
- **Envío y aduana**: peso volumétrico, comparador de líneas, casillas para Chile, calendario chino, e impuestos para Chile, Perú, Colombia, Argentina, Ecuador, Uruguay, México, EE.UU. y UE/España.
- **Tallas**: ropa por centímetros (平铺), calzado y conversión 斤 ↔ kg.

No ayuda a comprar réplicas de marcas ni a subdeclarar en aduana.

## Instalación

**Claude Code** (terminal o app de escritorio):
```bash
git clone https://github.com/djlarrix/compras-china.git ~/.claude/skills/compras-china
```
Para actualizar: `git -C ~/.claude/skills/compras-china pull`.

**claude.ai**: descarga `compras-china.skill` de la sección Releases y súbelo en Configuración → Capacidades → Skills.

## Estructura

```
SKILL.md                 Instrucciones principales (roles, flujo, principios, herramientas)
references/              Guías que Claude lee según la tarea
  agentes.md             Directorio y riesgos de agentes, links, protección del saldo
  plataformas.md         1688, Taobao/Tmall, Weidian, PDD, JD, Xianyu, Dewu, VVIC, Yiwugo, Alibaba.com
  proveedores.md         Búsqueda, verificación, clústeres, precio de referencia
  negociacion.md         Estrategia y plantillas de mensajes (chino / inglés / español)
  calidad.md             Fichas, trampas por categoría, muestras, QC, AQL
  pagos.md               Medios de pago, estafas, reclamos, tipo de cambio
  logistica.md           Envío interno, líneas, peso cobrable, casillas, calendario chino
  aduanas.md             Impuestos por país
  tallas.md              Tallas y unidades chinas
  glosario.md            Glosario chino–español
scripts/china_tools.py   Calculadora sin dependencias (Python 3.8+)
assets/                  Plantillas: comparador de proveedores, líneas de envío, confirmación de pedido
evals/                   Pruebas unitarias y escenarios de prueba calificados
```

## Calculadora

```bash
python3 scripts/china_tools.py tc                                    # tipos de cambio del día
python3 scripts/china_tools.py convertir 850 CNY CLP,USD --recargo 3.5
python3 scripts/china_tools.py enlace "https://weidian.com/item.html?itemID=7234567890"
python3 scripts/china_tools.py costo --pais chile --precio-cny 12.8 --unidades 300 \
  --kg 30 --usd-kg 12 --tc auto --tc-local auto --precio-venta 9990
python3 scripts/china_tools.py lineas assets/lineas_envio.csv --peso-real 4.2 --largo 45 --ancho 35 --alto 25
python3 scripts/china_tools.py aql --lote 1200
python3 scripts/china_tools.py talla ropa --tabla "M:52,L:55,XL:58" --plano --medida 100
```

## Pruebas

```bash
python3 -m unittest evals/test_china_tools.py -v          # 28 pruebas: links, moneda, costos por país, AQL, líneas, tallas, CLI
python3 evals/escenarios/calificar.py evals/escenarios    # 6 escenarios reales, 52 criterios
```

## Advertencia

Aranceles, umbrales de impuestos, tarifas y el estado de los agentes cambian seguido. Los datos son una fotografía de **septiembre de 2026**; la skill está instruida para verificarlos en la web y decir la fecha del dato. Nada de esto es asesoría legal o tributaria.
