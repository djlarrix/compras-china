# Logística: de la fábrica a tu puerta

Contenido:
1. El recorrido completo
2. Envío interno en China y marca de envío
3. Métodos internacionales: cuál elegir
4. Peso cobrable (volumétrico)
5. Embalaje y productos sensibles
6. Incoterms en simple
7. Calendario chino: cuándo no comprar
8. Envíos con agentes: líneas, rehearsal y cómo ahorrar
9. Casillas y forwarders para Chile

Tarifas orientativas de 2026; varían por temporada, combustible y país. Cotiza siempre al menos con 2–3 opciones.

---

## 1. El recorrido completo

Vendedor 1688 → (courier doméstico chino, 1–5 días) → bodega del agente / forwarder / casilla en China → recepción, fotos QC, consolidación, reembalaje → exportación → transporte internacional → aduana de destino → entrega local.

Cada tramo tiene costo y riesgo. Los errores más caros ocurren en los traspasos: bodega equivocada, caja sin marca, peso volumétrico no previsto, documentos incompletos en aduana.

## 2. Envío interno en China y marca de envío

- Los vendedores despachan con couriers baratos (中通 ZTO, 圆通 YTO, 韵达 Yunda, 申通 STO, 极兔 J&T); 顺丰 SF es más rápido y caro; para bultos pesados o voluminosos se usa 物流/快运 (德邦 Deppon, 安能, etc.).
- **Flete interno**: pide 包邮 o que te coticen el flete a la bodega. Elige una bodega del agente cerca del clúster (si compras en Yiwu, conviene bodega en Yiwu/Zhejiang; para Guangzhou/Shenzhen, bodega en Guangdong).
- **Dirección**: usa exactamente el formato que da el agente/forwarder (nombre del destinatario con tu **código de cliente**, teléfono, dirección). Un código faltante = paquete "huérfano" que se pierde en la bodega.
- **Marca de envío (唛头)**: pide que escriban tu código en cada caja. En pedidos de varios proveedores, pídeles también la guía (快递单号) y registra cuál corresponde a qué pedido.
- Evita **到付** (flete por pagar en destino) salvo que tu bodega lo acepte: algunas lo rechazan.

## 3. Métodos internacionales

| Método | Rango de peso típico | Tiempo típico a Latinoamérica | Costo orientativo | Notas |
|---|---|---|---|---|
| **Líneas del agente** (económicas / "especiales" / con impuestos incluidos) | 0,5–30 kg | 10–30 días | Variable por país y línea; revisa la calculadora del agente | Lo que ya conoces de Kakobuy. Revisa si cobran por peso real o volumétrico |
| **Courier express** (DHL, FedEx, UPS) | 0,5–70 kg | 3–10 días | Alto: a Chile del orden de USD 20–35 por kg efectivo con recargos | Rápido, tracking excelente; el courier hace la aduana de destino y cobra impuestos al entregar |
| **Línea dedicada / 专线, a menudo DDP (双清包税)** | 10–300 kg | 7–25 días aéreo | Intermedio | El forwarder cobra un precio por kg que incluye despacho e impuestos. Verifica que declaren el valor real y que la empresa sea seria |
| **Carga aérea** | 100 kg+ | 7–20 días | A Chile del orden de USD 7–11/kg + gastos locales | Necesita agente de aduana en destino si supera los umbrales |
| **Marítimo consolidado (LCL, 拼箱)** | ~1–15 m³ | 35–60 días puerta a puerta | Flete a Chile del orden de USD 700–1.100 por ~5 m³ + USD 600–900 de gastos locales (desconsolidación, agente de aduana, transporte) | Muy barato por unidad en volumen; costos fijos altos → no conviene para menos de ~1–2 m³ |
| **Contenedor completo (FCL, 整柜)** | 15–20 m³+ | 35–50 días | Por contenedor (20'/40') | Conviene cuando el LCL se acerca al costo del contenedor |

**Desconfía** de fletes marítimos a USD 0–5 por m³: el costo se recupera inflando gastos en destino. Pide cotización con todos los gastos de origen y destino detallados.

**Regla práctica para elegir**:
- Menos de ~20 kg y urgente → courier express o línea rápida del agente.
- Menos de ~30 kg y sin urgencia → línea económica del agente/casilla.
- 30–300 kg → línea dedicada aérea (DDP) o carga aérea; compara con LCL si no hay apuro.
- Más de ~2 m³ o mercadería pesada y barata → marítimo LCL; más de ~15 m³ → evalúa FCL.
- Siempre compara el **costo por unidad puesto en destino** (`china_tools.py costo`), no el precio por kg.

**Seguro**: en envíos de valor, contrata seguro de carga (a menudo ~1–3% del valor declarado en líneas de agentes; en carga, ~0,3–0,5% del valor CIF). Las líneas baratas pagan poco o nada por pérdida sin seguro.

## 4. Peso cobrable

Se cobra el **mayor** entre peso real y peso volumétrico:
- **Courier express**: largo × ancho × alto (cm) / **5000**.
- **Carga aérea (IATA)**: / **6000** (≈ 167 kg por m³).
- **Algunas líneas de agentes** usan /6000, /8000 o cobran solo peso real: revísalo.
- **Marítimo LCL**: se cobra por m³, con 1 m³ = 1.000 kg (lo que sea mayor).

Calcula:
```
python3 scripts/china_tools.py peso --largo 60 --ancho 40 --alto 40 --peso-real 12 --cajas 5
```

Productos livianos y voluminosos (almohadas, peluches, lámparas, juguetes grandes) se encarecen por volumen: piensa en compresión al vacío, desarmar, retirar cajas de zapatos, o marítimo.

## 5. Embalaje y productos sensibles

- **Reembalaje en la bodega del agente**: retirar cajas innecesarias baja el volumétrico, pero sin caja el producto puede dañarse o no ser vendible. Decide según si revendes (la caja importa) o no.
- **Refuerzo** (加固, esquineros, film) para objetos frágiles; **estructura de madera** (打木架) para vidrio/cerámica pesada. La madera sin tratamiento **ISPM 15** puede ser rechazada en destino (en Chile, control SAG).
- **Cajas master**: pide al proveedor que no pasen de 20–25 kg por caja y que sean de cartón resistente.
- **Carga sensible (敏感货)**: baterías (带电: necesitan MSDS y UN38.3), imanes (磁性), líquidos (液体), polvos (粉末), cremas, perfumes, cuchillos, productos con marca. No todas las líneas los aceptan; usar una línea equivocada = retención o devolución. Declara siempre el contenido real al agente.
- **Prohibidos**: armas y réplicas de armas, drogas, productos falsificados, y lo que prohíba tu país (en Chile, por ejemplo, ropa usada para comercio, ciertos productos de origen animal o vegetal sin autorización SAG). Revisa `aduanas.md`.

## 6. Incoterms en simple

| Término | El vendedor/forwarder se encarga hasta… | Tú pagas… |
|---|---|---|
| **EXW** (en fábrica) | Tener la mercadería lista en su fábrica | Todo lo demás |
| **FOB** (puerto de China) | Cargarla en el barco en el puerto chino | Flete internacional, seguro, aduana de destino |
| **CIF** (puerto de destino) | Flete y seguro hasta el puerto de destino | Descarga, aduana, impuestos, transporte local |
| **DAP** (en tu dirección, sin impuestos) | Entregar en tu dirección | Impuestos y trámites de importación |
| **DDP** (en tu dirección, todo pagado) | Todo, incluidos impuestos | Nada más (el precio los incluye) |

En 1688 casi siempre compras "precio en China + flete interno"; el resto lo organizas con agente/forwarder. En Alibaba.com te cotizan en FOB, CIF o DDP. Con DDP, confirma que el forwarder declara el valor real a tu nombre o a nombre de quién, porque la responsabilidad legal ante la aduana puede seguir siendo tuya.

## 7. Calendario chino: cuándo no comprar

- **Año Nuevo Chino (春节)**: el mayor cierre del año. 2027: **6 de febrero** (feriado oficial ~4–12 de febrero). En la práctica, las fábricas bajan el ritmo 2–4 semanas antes y tardan 2–4 semanas en volver a plena capacidad: 6–8 semanas de disrupción (aprox. mediados de enero a mediados de marzo de 2027). Haz pedidos de producción antes de noviembre–diciembre; despacha lo urgente antes de mediados de enero.
- **Semana Dorada (国庆节)**: 1–7 de octubre (2026: jueves 1 al miércoles 7 de octubre; días hábiles compensatorios el domingo 20 de septiembre y el sábado 10 de octubre). Oficinas, fábricas y muchos couriers paran; retrasos antes y después.
- **Festivales de compras**: **618** (junio) y **双11** (11 de noviembre): congestión de couriers domésticos y bodegas; también ofertas en Taobao/1688.
- **Otros feriados cortos (1–5 días)**: Qingming (abril), Día del Trabajo (1–5 de mayo), Barco del Dragón (junio), Medio Otoño (septiembre/octubre).
- **Temporada alta de fletes**: de agosto a diciembre (compras navideñas) suben tarifas y plazos, sobre todo marítimos. Reserva marítimo con 2 meses de anticipación en temporada alta.
- **Ferias**: Canton Fair (Guangzhou, abril y octubre) y feria de Yiwu (octubre): útiles para conocer fábricas en persona.

Si el usuario tiene una fecha límite (por ejemplo, vender en Navidad o en el Cyber), cuenta hacia atrás: producción + QC + tránsito + aduana + holgura de 1–2 semanas, y cruza con estos cierres.

## 8. Envíos con agentes: líneas, rehearsal y cómo ahorrar

- **Tipos de línea** que verás en un agente: courier express (DHL, FedEx, UPS; rápidos y caros, cobran impuestos al entregar), EMS (correo postal rápido), líneas económicas/postales (SAL, "small packet"), líneas especiales por país (a veces con impuestos incluidos o "tax free") y marítimo para paquetes grandes.
- **Qué comparar**: precio del primer tramo y de cada tramo adicional (normalmente 500 g), divisor volumétrico (o si cobran solo peso real), cargos fijos (declaración, combustible), tiempo real de tránsito a tu país, peso máximo, productos aceptados, si incluye impuestos y seguro.
- **Compara con datos**: llena `assets/lineas_envio.csv` con las tarifas que ves en la calculadora de cada agente o casilla y ejecuta:
```
python3 scripts/china_tools.py lineas assets/lineas_envio.csv --peso-real 4.2 --largo 45 --ancho 35 --alto 25
```
- **Rehearsal (simulación de paquete)**: pide que la bodega arme el paquete y te dé peso y medidas reales antes de elegir la línea; cuesta poco y evita sorpresas con el volumétrico.
- **Bajar el peso cobrable**: quitar cajas de zapatos (300–500 g y mucho volumen cada una), empacar ropa al vacío, retirar empaques innecesarios, consolidar en una caja bien llena. Si revendes, conserva los empaques que sean parte del producto.
- **Dividir o juntar**: a veces dos paquetes bajo un límite (peso o valor aduanero) salen más baratos que uno grande; otras veces consolidar ahorra el cargo fijo. Cuidado: dividir para eludir límites aduaneros puede considerarse fraccionamiento indebido.
- **Tiempos**: suma 1–4 días de preparación en bodega + tránsito + aduana del destino.

## 9. Casillas y forwarders para Chile

Para compras comerciales o directas en 1688 con destino Chile, una casilla/forwarder de importación suele convenir más que un agente de compra minorista:
- **Qué hacen**: te dan una dirección en China (a menudo Yiwu o Guangzhou), reciben de varios proveedores, consolidan, envían aéreo o marítimo y hacen la aduana en Chile; algunas entregan en Santiago.
- **Ejemplos** (verificar condiciones actuales): Chibox Cargo (casilla y bodega en China, bodega en Santiago; cotiza con la factura proforma del proveedor); WS Cargo (bodegas en Yiwu y Guangzhou; marítimo consolidado publicado desde USD 300/m³, USD 260/m³ sobre 25 m³, recargo de USD 100 bajo 5 m³, con trámites en China y Chile y entrega en la provincia de Santiago). Hay otras; pide al menos dos cotizaciones.
- **Qué preguntar**: ¿el precio incluye IVA y arancel o solo el flete? ¿incluye agente de aduana, desconsolidación, almacenaje, seguro y entrega? ¿mínimo cobrable? ¿cobran por peso o volumen? ¿aceptan baterías o cosméticos? ¿tiempo puerta a puerta? ¿emiten documentos a tu RUT para crédito fiscal?
- Compara el resultado con `china_tools.py costo` usando `--flete-usd` con la cotización y `--impuestos-incluidos` si la tarifa ya incluye tributos.
