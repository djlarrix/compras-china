# Prompt
tenía este link de cnfans https://cnfans.com/product/?shop_type=weidian&id=7234567890 y ya no me funciona, pásamelo a kakobuy y dime qué agente conviene ahora para mandar un paquete de unos 3 kilos a chile (una caja de 40x30x25)

# Respuesta (siguiendo la skill)

**No te funciona porque CNFans cerró**: dejó de aceptar pedidos en agosto de 2026. El producto no se perdió: es de Weidian, y el link original sirve en cualquier agente.

## Tus links
- **Original (guárdalo siempre):** https://weidian.com/item.html?itemID=7234567890
- **Kakobuy:** https://www.kakobuy.com/item/details?url=https%3A%2F%2Fweidian.com%2Fitem.html%3FitemID%3D7234567890
- Superbuy: https://www.superbuy.com/en/page/buy/?url=https%3A%2F%2Fweidian.com%2Fitem.html%3FitemID%3D7234567890
- Sugargoo: https://www.sugargoo.com/productDetail?productLink=https%3A%2F%2Fweidian.com%2Fitem.html%3FitemID%3D7234567890
- CSSBuy: https://www.cssbuy.com/item-micro-7234567890.html

## ¿Qué agente conviene ahora?
Estado a septiembre de 2026 (verifícalo antes de cargar saldo):
- **Evita**: CNFans (cerrado), ACBuy/AllChinaBuy (sin pedidos), **Mulebuy** (reportes no confirmados de una redada en su bodega en agosto).
- **Activos con trayectoria**: Kakobuy (el que ya conoces; buena logística, pero críticas en el manejo de disputas), Superbuy (0% de comisión oficial en Taobao, Tmall, JD y 1688; Weidian no figura entre las plataformas gratuitas de su tabla, así que probablemente pague 10% con tope de ¥20: verifícalo), Sugargoo y CSSBuy.

Lo que decide no es la comisión, es el **flete de tu caja**:
- 40×30×25 cm con 3 kg → peso volumétrico **6 kg** en courier (/5000), **5 kg** en líneas /6000 y 3,75 kg en líneas /8000. **Te cobrarán por volumen, no por los 3 kg.**
- Pide un **rehearsal** (simulación de paquete) y reduce el volumen: sin cajas, empaque al vacío si es ropa. Bajar a una caja de 35×25×20 cm deja el volumétrico en ~2,9 kg (/6000).
- Compara en la calculadora de Kakobuy y de Superbuy con destino **Chile**, tus medidas reales y la misma línea (por ejemplo EMS vs línea especial), y anota las tarifas en `assets/lineas_envio.csv`; `china_tools.py lineas` te ordena el costo total.
- Mide también el **recargo cambiario** de cada agente (`convertir 100 USD CNY --tc-agente <su tasa>`): hay agentes con 0% de comisión y más de 10% de recargo en el tipo de cambio.

## Aduana en Chile
Si el agente no está inscrito en el SII, al llegar pagas **6% de arancel + 19% de IVA** sobre el valor CIF (producto + flete + seguro). Ya no existe la franquicia de USD 41. Declara el valor real.

## Protege tu plata
Carga saldo solo para este pedido, paga con tarjeta o PayPal y no dejes el paquete guardado más de lo necesario.

## Siguiente acción
Abre el link de Kakobuy o Superbuy, revisa las fotos QC cuando llegue y pide el rehearsal antes de elegir la línea.
