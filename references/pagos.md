# Pagos, protección, estafas y reclamos

Contenido:
1. Métodos de pago y qué protección conservas
2. Qué método usar según monto y confianza
3. Estructuras de pago para producción
4. Estafas frecuentes y cómo evitarlas
5. Reclamos y posventa (1688, agente, Alibaba.com)
6. Tipo de cambio: cuánto pierdes al convertir
7. Saldo en agentes: el riesgo que nadie menciona

Los métodos de pago para extranjeros cambian seguido (comisiones, límites, países habilitados). Datos a septiembre de 2026: verifica en la web antes de dar cifras exactas.

---

## 1. Métodos de pago

| Método | Cómo funciona | Costo orientativo | Protección |
|---|---|---|---|
| **Vía agente** (Kakobuy, etc.) | Le pagas al agente (PayPal, tarjeta, Wise, etc.) y él paga al vendedor en CNY | Comisión del agente (0–10%) + recargo del medio de pago (PayPal ~3–4%) | La del agente: reembolso si el vendedor no despacha, gestiona devoluciones dentro de China |
| **App 1688 Global con tarjeta** Visa/Mastercard | Pagas el pedido de 1688 en la app internacional | Recargos de conversión/tarjeta; revisar el total antes de pagar | Pago dentro de 1688 (flujo de reclamo de la plataforma, en chino) |
| **Alipay con tarjeta extranjera** | Alipay acepta Visa/Mastercard de extranjeros con verificación de pasaporte y rostro | Alipay cobra ~3% sobre transacciones de más de ¥200 con tarjeta extranjera, más el recargo de tu banco. Límites por transacción y anuales para extranjeros | Si pagas un pedido de 1688/Taobao con Alipay, el dinero queda en custodia hasta confirmar la recepción |
| **WorldFirst (World Account)** conectado a 1688 | Cargas USD/EUR, conviertes a CNY y pagas pedidos de 1688 | Del orden de 0,8–2% | Pago dentro de 1688 |
| **找人代付** (pago por un tercero) | Generas un link de pago del pedido y alguien en China con Alipay lo paga; tú le devuelves el dinero | Lo que acuerdes con esa persona | Pago dentro de 1688. Solo con alguien de total confianza |
| **Wise u otro envío a Alipay/WeChat del vendedor** | Transferencia a la billetera personal del vendedor | Bajo | **Ninguna.** Además, solo cuentas personales de Wise y con límites por destinatario |
| **Transferencia bancaria (T/T)** a cuenta de empresa | Swift en USD o CNY a la cuenta de la empresa | Comisión bancaria fija + diferencial cambiario | **Ninguna** más allá del contrato. Solo con proveedor verificado |
| **Alibaba.com Trade Assurance** | Pagas en Alibaba.com (tarjeta, T/T, etc.) | Según medio de pago | Escrow con reclamo en inglés, hasta el límite de cobertura del proveedor |
| **Western Union, cripto, tarjetas de regalo** | — | — | **Ninguna.** Señal de alerta; no recomendado |

**Idea central**: mientras el dinero pase por la custodia de la plataforma (1688/Alipay, Trade Assurance o el agente), existe un reclamo posible. Fuera de la plataforma, tu única protección es haber verificado bien al proveedor y el contrato.

## 2. Qué método usar según monto y confianza

| Situación | Recomendación |
|---|---|
| Compras pequeñas, muchos vendedores, primera vez | Agente (peldaño 1–2 de `plataformas.md` §4) |
| Negociaste con un vendedor de 1688 y quieres ahorrar comisión | Pagar el pedido de 1688 tú mismo dentro de la plataforma (1688 Global / Alipay / WorldFirst) y enviarlo a la bodega de tu agente o casilla |
| Muestras | Dentro de la plataforma o por el agente. No vale la pena el riesgo de pagar fuera por montos pequeños |
| Pedido grande con fábrica nueva | Alibaba.com Trade Assurance, o dentro de 1688; si es fuera, T/T a cuenta de empresa verificada con 30% anticipo y saldo tras inspección |
| Proveedor con historial de varias compras exitosas contigo | T/T a cuenta de empresa (más barato) si el ahorro compensa perder la protección |

Antes de pagar, revisa siempre: total con flete, cantidad, variantes, precio ajustado (改价) y dirección de entrega correcta.

## 3. Estructuras de pago para producción

- **Stock en 1688 (现货)**: pago total dentro de la plataforma; el vendedor cobra cuando confirmas la recepción (o se autoconfirma).
- **Producción personalizada**: lo típico es **30% anticipo (定金) + 70% saldo (尾款)** antes del despacho, idealmente tras inspección aprobada. Algunas fábricas piden 50/50 en pedidos chicos.
- **Moldes (开模费)**: suele pagarse aparte y al inicio; pregunta si se reembolsa con volumen y deja por escrito que **el molde es tuyo**.
- **Nunca 100% por adelantado** en producción con un proveedor nuevo fuera de la plataforma.
- Pide **factura proforma (PI / 形式发票)** con datos de la empresa, precio, cantidad, especificaciones, plazos, condiciones de pago y de calidad. Guarda el comprobante bancario (MT103 en transferencias Swift).

## 4. Estafas frecuentes

| Estafa | Cómo se ve | Defensa |
|---|---|---|
| **Cambio de cuenta bancaria** | "Nuestra cuenta cambió, pague a esta nueva" (a veces desde el correo real hackeado del proveedor), cuenta a nombre parecido pero distinto | Confirmar por un canal independiente (videollamada, chat de la plataforma); el titular debe coincidir exactamente con la licencia |
| **Cuenta personal** | Piden pagar a la cuenta de una persona "por impuestos" o "es más rápido" | No en pedidos grandes. Cuenta de empresa o pago dentro de la plataforma |
| **Fábrica fantasma** | Fotos robadas, precio irresistible, sin licencia verificable | Triage de `proveedores.md` §3; videollamada; muestra |
| **Muestra buena, producción mala** (bait and switch) | La muestra es impecable; el volumen usa otro material | Muestra dorada, cláusula escrita, inspección antes del saldo |
| **Despacho falso** (虚假发货 / 空包) | Marcan "enviado" con un número de seguimiento que no avanza, para cumplir el plazo | Revisa el tracking; reclama antes de que corra la autoconfirmación |
| **Faltantes** | Cajas con menos unidades | Conteo en la bodega del agente; foto de cajas abiertas |
| **SKU trampa** | Precio de portada que corresponde a una variante mínima | Revisar precio de cada SKU y el total del pedido |
| **Flete o "impuestos" sorpresa** | Tras pagar, piden más por flete, embalaje o impuestos | Todo incluido y confirmado por escrito antes de pagar |
| **Sacar la conversación de la plataforma** | Insisten en WeChat/WhatsApp y pago directo desde el principio | Mantener lo contractual en la plataforma |

## 5. Reclamos y posventa

### En 1688 (si pagaste dentro de la plataforma)
- Desde el pedido: **申请售后** → elegir 仅退款 (solo reembolso) o 退货退款 (devolver y reembolsar). Desde marzo de 2025, 1688 eliminó el "solo reembolso" automático sin devolución; ahora depende del caso y del historial del comprador.
- Plazos cortos tras la recepción (del orden de 48 h para calidad y 72 h para producto distinto, según la guía oficial de 1688). No dejes pasar la autoconfirmación de recepción; pide extensión (延长收货) si la mercadería está en revisión.
- **Evidencia que pesa**: número de pedido, SKU, comprobante de pago; video continuo de apertura; fotos comparando con la ficha/acuerdo; **el chat de 旺旺** (1688 no reconoce WeChat ni QQ como evidencia); informes de inspección.
- **No devuelvas nada** hasta que el vendedor o la plataforma aprueben la devolución.
- Si el vendedor no resuelve, pide la intervención de la plataforma (平台介入).
- Si compraste vía agente, el agente gestiona el reclamo por ti: dale fotos y descripción precisa.

### En Alibaba.com (Trade Assurance)
- Abre la disputa dentro del plazo (para cobertura post-entrega, del orden de 15 días desde que la mercadería se libera en aduana).
- Si el proveedor no responde o no hay acuerdo, escala a Alibaba, que decide según la evidencia (orden de compra con especificaciones, informes de inspección, fotos).

### Fuera de plataforma
- Tu palanca es la relación y los pagos pendientes (por eso el saldo después de la inspección).
- Negocia reposición en el próximo pedido, reembolso parcial o reenvío.
- En montos grandes, un abogado en China o el agente de sourcing pueden presionar; los juicios son lentos y caros, por eso la prevención importa más.

## 6. Tipo de cambio: cuánto pierdes al convertir

Cada conversión de moneda tiene un diferencial frente al tipo de mercado:
- **Tarjeta de crédito chilena en CNY o USD**: el banco convierte con su tasa + comisión por compra internacional; revisa tu estado de cuenta.
- **PayPal**: comisión de la transacción + su propio tipo de cambio (a menudo 3–4% sobre el mercado). Si puedes elegir, paga en la moneda que te convenga comparando ambas opciones.
- **Agentes**: fijan su propia tasa CNY/USD; la diferencia con el mercado es un cobro escondido (de ~1% a más de 10% según mediciones de 2026).
- **Alipay con tarjeta extranjera**: 3% sobre pagos de más de ¥200 + la conversión de tu banco.
- **Wise / WorldFirst**: diferencial bajo (≈0,5–2%), bueno para montos grandes.

Cómo medirlo:
```
python3 scripts/china_tools.py tc                                  # tipos del día
python3 scripts/china_tools.py convertir 850 CNY CLP,USD --recargo 3.5
python3 scripts/china_tools.py convertir 100 USD CNY --tc-agente 6.45   # recargo real del agente
```
Suma el recargo cambiario a la comisión del agente y del medio de pago para comparar el costo real (en `costo`, usa `--pago-pct`).

## 7. Saldo en agentes: el riesgo que nadie menciona

El saldo que cargas en un agente no está protegido como un depósito bancario. Cuando un agente cae (Pandabuy en 2024; CNFans cerró en agosto de 2026; ACBuy dejó de aceptar pedidos; Mulebuy con reportes de redada en agosto de 2026) los saldos y paquetes pueden quedar atrapados. Reglas:
- Carga solo lo que vas a gastar en el pedido actual.
- Paga con tarjeta de crédito o PayPal (permiten reclamar) antes que con cripto o transferencias.
- No dejes paquetes guardados más de lo necesario.
- Guarda capturas del saldo, pedidos e inventario.
- Detalle y señales de alerta en `agentes.md` §5.
