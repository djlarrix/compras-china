# Agentes de compra (shopping agents): directorio, riesgos y cómo elegir

Contenido:
1. Qué hace un agente y qué cobra de verdad
2. Estado del mercado a septiembre de 2026 (cierres y riesgos)
3. Directorio de agentes
4. Cómo elegir agente (en especial para Chile y Latinoamérica)
5. Cómo proteger tu dinero y tus paquetes
6. Servicios del agente: glosario práctico
7. Links: convertir entre agentes y plataformas
8. Herramientas de la comunidad (con cautela)
9. Agente, casilla o forwarder: qué usar al pasar a compra directa

Los datos de agentes cambian cada mes y muchas fuentes en internet son sitios de afiliados. Todo lo de abajo es orientativo a septiembre de 2026: **antes de recomendar un agente, verifica en la web su estado actual** (busca "<agente> shut down", "<agente> raid", reclamos recientes en Reddit/Trustpilot) y lee su página oficial de tarifas.

---

## 1. Qué hace un agente y qué cobra de verdad

Un agente compra por ti en plataformas chinas (Taobao, Tmall, Weidian, 1688, a veces JD, Xianyu, Pinduoduo), recibe en su bodega, te muestra fotos QC, guarda, consolida y te despacha al extranjero.

El costo real tiene **seis capas**; compara siempre el total:
1. **Comisión de servicio**: 0–10% del producto (muchos anuncian 0%).
2. **Recargo cambiario**: el tipo CNY/USD que usa el agente vs el de mercado. Puede ir de ~1% a más de 10% (una medición de jun-2026 encontró 11,44% en Oopbuy). Mídelo con `china_tools.py convertir 100 USD CNY --tc-agente <tasa del agente>`.
3. **Comisión del medio de pago**: PayPal ~3–4,4% + fijo; tarjetas 0–3%; transferencias y Wise más baratos.
4. **Flete interno en China** (vendedor → bodega): a veces gratis, a veces ¥5–15 por pedido.
5. **Flete internacional**: donde más varía el costo; los agentes ganan margen aquí. Revisa si cobran peso real o volumétrico y con qué divisor.
6. **Extras**: fotos adicionales, video, rehearsal, embalaje, seguro, almacenaje extendido, tarifa de declaración (ej. ¥8/paquete).

Un agente con "0% comisión" puede salir más caro que otro con 5% si su recargo cambiario o su flete son altos. Calcula el total por paquete (`china_tools.py lineas`) y por unidad (`china_tools.py costo`).

## 2. Estado del mercado a septiembre de 2026

El sector de agentes es inestable, en buena parte porque muchos crecieron vendiendo réplicas de marcas, lo que atrae acciones policiales:

| Agente | Qué pasó | Consecuencia para usuarios |
|---|---|---|
| **Pandabuy** | Redada policial en China (abril de 2024) impulsada por titulares de marcas; bodegas selladas, detenidos. Se apagó durante 2024–2025 | Saldos congelados, paquetes atrapados. No volverá |
| **CNFans** | Dejó de aceptar pedidos en **agosto de 2026**; Discord y Reddit cerrados | Cierre de negocio; los links de productos siguen sirviendo en otros agentes |
| **ACBuy / AllChinaBuy** (misma empresa, rebrand 2023) | Reportes de que dejó de aceptar pedidos en 2026 y de una filtración de datos en febrero | No usar |
| **Mulebuy** | Reportes **no confirmados** de redada en su bodega (agosto de 2026): ítems marcados como destruidos, soporte sin respuesta, subreddit privado. Sitio y pagos seguían operando al 10-ago | Riesgo alto: no cargar saldo; sacar paquetes |

Lecciones: (1) no dejes saldo ni paquetes detenidos en un agente; (2) guarda siempre el link original de la plataforma (no el del agente); (3) para mercadería legítima, prefiere agentes con años de trayectoria y términos publicados, o un forwarder/casilla orientado a importación formal.

## 3. Directorio de agentes

Cifras según páginas oficiales y reseñas de 2026; varias fuentes se contradicen (se indica). Verifica antes de usar.

| Agente | Estado (sept-2026) | Comisión | Almacenaje gratis | Fotos QC gratis | Notas |
|---|---|---|---|---|---|
| **Kakobuy** | Activo | No publicada; 0% en muchos pedidos de Taobao/Weidian (otras fuentes: 0–3% o planes 5–10%) | 100 días (+¥20 por 100 días) según una fuente; 180 según otra | ~3–7 HD | Desde 2023; recibió a los usuarios de Pandabuy. Logística consistente; críticas por manejo de disputas y compensaciones en cupones. Trustpilot 2,5/5 (74 reseñas, 2026). Pagos: PayPal, tarjetas, Google/Apple Pay, cripto. Acepta reenvío de paquetes comprados por ti |
| **Superbuy** | Activo | Oficial: **0%** en Taobao, Tmall, JD y 1688; ¥20 fijo en segunda mano (Xianyu); 10% (mín. ¥10, máx. ¥20) en otras plataformas | 90 días; luego ¥0,1/ítem/día; máx. 180 | ~3 | Uno de los más antiguos. Extras oficiales: fotos detalladas ¥2, inspección ¥6, video ¥20, vacío ¥17, caja de madera ¥250. Servicio de reenvío (forwarding) |
| **CSSBuy** | Activo | ~6% | 90 días desde "en bodega"; extensión ~¥15/pedido/mes | 2–3 | Antiguo; links `item-micro-` (Weidian) |
| **Sugargoo** | Activo | Fuentes contradictorias: 0% vs 5% desde mar-2026 | 90–100 días | ~5 (bien evaluadas) | Muchas líneas (rutas "tax free" para Europa); simulación de paquete previa al envío |
| **Hoobuy** | Activo | 0–3% | 90 días | ~6 HD | Muchos medios de pago |
| **Oopbuy** | Activo (desde 2024) | 0% + ¥8 por paquete (declaración) | 90 días | 6 HD (+¥1 c/u) | Recargo cambiario medido **11,44%** (jun-2026); seguro 3%. Trustpilot suspendió su puntaje por reseñas falsas |
| **Joyagoo** (ex Joyabuy, rebrand 31-mar-2025) | Activo | 0% | 90 días | HD (cantidad no publicada) | Trustpilot 4,6/5 (~2.900 reseñas, jul-2026); soporte ~24 h |
| **Lovegobuy** | Activo | 0–3% | ~60 días | 4–8 | Buen soporte según reseñas |
| **Litbuy** | Activo | ~4–7% según una fuente | — | 4–6 | Reseñas mixtas: pedidos no despachados y reembolsos demorados |
| **USFans** | Activo | 0% | — | — | Poca información independiente |
| Ootdbuy, Hipobuy, GTBuy, Vigorbuy, RizzitGO, Eastmallbuy, iTaobuy, LoongBuy, Pikobuy, Cnshopper, Alleurobuy, HubbuyCN, PonyBuy, Fishgoo, Basetao, Yoybuy, BDDbuy | Varios | Variable | Variable | Variable | Poca información independiente: tratarlos como no verificados; empezar con un pedido chico |
| **Mulebuy** | **Riesgo** | 0% | 90 días | 3–7 | Ver §2 |
| **CNFans** | **Cerrado** (ago-2026) | — | — | — | Ver §2 |
| **ACBuy / AllChinaBuy** | **Sin pedidos** (2026) | — | — | — | Ver §2 |
| **Pandabuy** | **Cerrado** (2024) | — | — | — | Ver §2 |

## 4. Cómo elegir agente

1. **Estado actual** (§2): descarta cerrados o con reportes de redada.
2. **Líneas a tu país**: muchos agentes optimizan líneas para EE.UU., Europa y Australia. Para Chile y Latinoamérica suele haber menos opciones (EMS, DHL/FedEx/UPS, alguna línea especial). Revisa en la calculadora del agente, con tu país, peso y medidas reales; los multicomparadores (p. ej. JadeShip, que incluye Chile) ayudan a ver varias a la vez.
3. **Costo total por paquete** con la misma caja en cada agente: `china_tools.py lineas` (llena `assets/lineas_envio.csv` con las tarifas que veas).
4. **Recargo cambiario y medio de pago** (§1).
5. **Qué productos acepta cada línea**: baterías, imanes, líquidos, cosméticos, alimentos; y si la línea incluye impuestos.
6. **Política de reclamos y seguro**: plazos para devolver al vendedor, qué cubre el seguro, si compensan en dinero o en cupones.
7. **Reputación reciente** (últimos 3–6 meses) en Reddit y Trustpilot, filtrando por tu país.
8. **Impuestos en Chile**: si el agente está inscrito en el SII como plataforma, cobra el IVA en la compra y no pagas arancel hasta USD 500; si no, pagas IVA + arancel al llegar. Revisa la lista vigente en sii.cl.

Para compras legítimas recurrentes, un agente con trayectoria larga (Superbuy, CSSBuy, Sugargoo) o un forwarder/casilla de importación suele ser más estable que los agentes nuevos centrados en "finds".

## 5. Cómo proteger tu dinero y tus paquetes

- **Carga saldo por pedido**, no por adelantado "por si acaso". Un saldo en un agente no tiene ninguna garantía si el agente cae.
- **Mueve los paquetes**: el almacenaje gratis sirve para consolidar, no para guardar mercadería semanas.
- **Paga con medios que permitan reclamar** (tarjeta de crédito, PayPal) en vez de cripto o transferencias sin respaldo.
- **Guarda evidencia**: capturas del historial de pedidos, del inventario en bodega y del saldo, periódicamente.
- **Guarda los links originales** (Taobao/Weidian/1688), nunca solo el link del agente: `china_tools.py enlace` los recupera.
- **No concentres todo** en un agente nuevo; ten un segundo agente probado.
- **Señales de alerta**: soporte que deja de responder, subreddit o Discord cerrados, cambios bruscos de tarifas, "mantenimiento" prolongado, ítems marcados como destruidos o confiscados. Ante eso: no cargues más saldo, pide el envío o el reembolso de inmediato y contacta al emisor de tu tarjeta/PayPal si no responden.

## 6. Servicios del agente: glosario práctico

- **Fotos QC / fotos de llegada**: fotos gratuitas del producto al llegar a la bodega. Pide extra: medidas con huincha, peso, detalle de costuras/logos/etiquetas, video funcionando (cuestan ¥1–20).
- **Devolución o cambio al vendedor**: solo dentro de China, en un plazo corto desde la llegada a bodega (a menudo 5–7 días) y con flete interno a tu cargo si el error no es del vendedor. Revisa las fotos QC apenas lleguen.
- **Rehearsal / simulación de paquete (预演包裹)**: por una tarifa baja, la bodega arma el paquete como si fuera a enviarlo y te da peso y medidas reales; así eliges la línea más barata con datos reales. Útil con 3+ ítems o productos voluminosos.
- **Consolidación**: juntar pedidos de varios vendedores en un solo paquete (ahorra flete).
- **Reducción de volumen**: quitar cajas de zapatos (300–500 g y mucho volumen cada una), empaque al vacío para ropa, retirar empaques innecesarios. Ojo: si vas a revender, la caja puede ser parte del producto.
- **Refuerzo**: esquineros, film, caja de madera para frágiles.
- **Seguro**: suele ser un porcentaje del valor declarado (~3–5%). Lee qué cubre (pérdida total, daño, retención aduanera) y si pagan en dinero o cupones.
- **Valor declarado**: algunos agentes proponen declarar menos. La responsabilidad ante la aduana es tuya: declara el valor real (ver `aduanas.md`).
- **Líneas "tax free" / con impuestos incluidos / IOSS**: el agente o su operador pagan los impuestos del destino; verifica que realmente se paguen a tu nombre y qué pasa si la aduana retiene el paquete.
- **Líneas para productos sensibles**: baterías, imanes, líquidos, polvos, cremas. Declara el contenido real al agente.
- **Almacenaje**: gratis 60–180 días según agente; luego cobro diario/mensual.
- **Reenvío (forwarding)**: el agente recibe paquetes que compraste tú mismo. Pide su dirección de bodega con tu código de cliente.

## 7. Links: convertir entre agentes y plataformas

`python3 scripts/china_tools.py enlace <link o texto compartido>`:
- Reconoce links de Taobao, Tmall, Weidian, 1688, JD, Xianyu/Goofish, Pinduoduo, Alibaba.com, AliExpress y de 25+ agentes (Kakobuy, Superbuy, Sugargoo, CSSBuy, Hoobuy, Oopbuy, Joyagoo/Joyabuy, Lovegobuy, Litbuy, USFans, Mulebuy, CNFans, ACBuy, RizzitGO, etc.), incluso dentro de texto compartido desde la app.
- Devuelve el **link original** de la plataforma y el link equivalente en cada agente activo (oculta los cerrados o en riesgo salvo con `--todos`; filtra con `--agentes kakobuy,superbuy`).
- Links cortos (`m.tb.cn`, `qr.1688.com`): usa `--resolver` para seguir la redirección (necesita internet); si falla, pide al usuario que abra el link y copie la URL completa.
- Los links generados no llevan códigos de afiliado.

Formatos de referencia (id = número del producto):
- Taobao/Tmall: `https://item.taobao.com/item.htm?id=<id>`
- Weidian: `https://weidian.com/item.html?itemID=<id>`
- 1688: `https://detail.1688.com/offer/<id>.html`
- Kakobuy: `https://www.kakobuy.com/item/details?url=<link original codificado>`
- Superbuy: `https://www.superbuy.com/en/page/buy/?url=<link original codificado>`
- CSSBuy: `item-micro-<id>` (Weidian), `item-<id>` (Taobao), `item-1688-<id>` (1688)
- Hoobuy: `/product/2/<id>` Weidian, `/product/1/<id>` Taobao, `/product/0/<id>` 1688

## 8. Herramientas de la comunidad (con cautela)

- **Buscadores de fotos QC** (p. ej. el QC finder de rep.tools): pegando el link de un producto muestran fotos reales de bodega de otros compradores del mismo artículo. Útil para juzgar calidad de cualquier producto antes de comprar.
- **Calculadoras de flete multi-agente** (p. ej. JadeShip, con Chile como destino) y calculadoras propias de cada agente.
- **Conversores de links** (el script de esta skill hace lo mismo sin afiliados).

Cautela: casi todos estos sitios viven de comisiones de afiliado y sus "spreadsheets" de "finds" son mayoritariamente réplicas de marcas. Úsalos como herramientas de datos, no como fuente de productos; esta skill no ayuda a buscar ni comprar réplicas.

## 9. Agente, casilla o forwarder: qué usar al pasar a compra directa

| Situación | Mejor opción |
|---|---|
| Compras pequeñas y variadas de Taobao/Weidian, uso personal | Agente de compra |
| Compraste tú en 1688 negociando con el vendedor, cantidades chicas–medianas | Servicio de reenvío de un agente, o casilla en China |
| Carga comercial (decenas de kg o m³), varios proveedores, reventa en Chile | Casilla/forwarder de importación con bodega en China y despacho en Chile (aéreo o marítimo consolidado), con factura y agente de aduana cuando corresponde |
| Contenedor o producción personalizada | Forwarder de carga + agente de aduana (+ sourcing agent si necesitas supervisión) |

Ejemplos en Chile (a septiembre de 2026, verificar condiciones): **Chibox Cargo** (casilla y bodega en China, bodega en Santiago, cotiza con la factura proforma de tu proveedor) y **WS Cargo** (bodegas en Yiwu y Guangzhou; marítimo consolidado publicado desde USD 300/m³, bajando a USD 260/m³ sobre 25 m³, con recargo de USD 100 bajo 5 m³, incluyendo trámites en China y Chile y entrega en la provincia de Santiago). Existen otras casillas; compara con al menos dos cotizaciones y revisa qué incluyen (impuestos, agente de aduana, desconsolidación, entrega).
