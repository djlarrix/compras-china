# Calidad: fichas, muestras, fotos QC e inspección

Contenido:
1. Cómo leer una ficha de 1688/Taobao para juzgar calidad
2. Trampas de calidad por categoría
3. Qué preguntarle al vendedor antes de comprar
4. Muestras y "muestra dorada"
5. Fotos y video QC (agente, forwarder o vendedor)
6. Inspección de terceros y AQL
7. Al recibir la mercadería

---

## 1. Cómo leer una ficha

Recorre la ficha en este orden y anota lo que encuentres:

1. **Tramos de precio (价格区间 / 起批量)**: qué precio corresponde a *tu* cantidad. El precio grande del encabezado suele ser el del tramo más alto o el del SKU más barato.
2. **SKU (规格 / 颜色 / 尺码)**: revisa el precio de cada variante; a veces solo la talla o color menos pedido tiene el precio anunciado.
3. **Atributos (商品属性 / 产品参数)**: material (材质), composición (成分/面料), gramaje (克重), medidas (尺寸), peso (重量), certificaciones, origen (产地). Si faltan o son vagos, pregúntalos (§3).
4. **Detalle (详情页)**: fotos de fábrica, proceso, cortes transversales, pruebas. Fotos genéricas o de estudio sin detalles = pedir fotos reales.
5. **Reseñas y 买家秀**: fotos reales de compradores; filtra por "有图" (con imagen) y por reseñas negativas (差评). Busca patrones.
6. **问大家 / 常见问题**: preguntas de otros compradores, a veces revelan problemas.
7. **Métricas de la tienda** (ver `proveedores.md` §2): tasa de recompra y puntaje de "品质体验" (experiencia de calidad) dicen mucho.
8. **Compara la misma foto en otras tiendas** (búsqueda por imagen): si otra tienda tiene más reseñas con fotos reales del mismo producto, aprovéchalas para juzgar calidad.
9. **Fotos QC de otros compradores**: los buscadores de fotos QC (ver `agentes.md` §8) muestran fotos reales de bodega del mismo link comprado por otros; es la mejor señal de calidad real antes de pagar.
10. **Reseñas fuera de la plataforma**: busca el producto en Xiaohongshu (小红书) con 测评 (prueba), 避雷 (advertencias) o 真实 (real); en Taobao/Tmall filtra reseñas 带图 (con foto) y 追评 (seguimiento tras semanas de uso).

Señales positivas: fotos reales de producción, especificaciones precisas, video del producto, tasa de recompra alta, reseñas con fotos coherentes con las del vendedor, 品质体验 alto.

Señales negativas: solo renders, especificaciones con "约" (aprox.) en todo, reseñas quejándose de 色差/做工/尺寸, precio muy bajo contra el rango (§5 de `proveedores.md`).

## 2. Trampas de calidad por categoría

Pide siempre la especificación exacta por escrito en el chat. Cuando el material importa, pide que confirmen que "大货和样品一致" (la producción será igual a la muestra).

| Categoría | Trampa típica | Qué pedir/verificar |
|---|---|---|
| **Acero inoxidable** (termos, cubiertos, joyería) | 201 o 202 vendido como 304; 304 vs 316 (más resistente a corrosión y apto quirúrgico) | Grado exacto (304/316L), certificado de material (材质证明/材质报告). El imán no es prueba confiable |
| **Algodón y telas** | "纯棉" que es mezcla; gramaje menor al anunciado | Composición en % (例: 100%棉), 克重 (g/m²), encogimiento (缩水率), solidez del color (色牢度) |
| **Cuero** | PU o cuero reconstituido como "真皮"; 二层皮 (descarne) como 头层 (flor) | 头层牛皮 vs 二层皮 vs PU/超纤; foto del canto y reverso |
| **Electrónica con batería** | mAh inflados (虚标), celdas recicladas | Capacidad real, marca de celdas, video de prueba de descarga, certificaciones (UN38.3 para transporte, MSDS) |
| **Cargadores, cables, enchufes** | Sin protecciones; cobre recubierto de aluminio (铜包铝, CCA) en vez de cobre (纯铜) | Certificaciones del destino (en Chile SEC), calibre y material del conductor, prueba de carga |
| **Plásticos y contacto con alimentos** | Plástico reciclado no apto; "sin BPA" sin respaldo | Tipo de plástico (PP, PC, Tritan, ABS), 食品级 (grado alimentario), informes (FDA/LFGB) |
| **Joyería y bisutería** | Chapado delgado que se pela; "plata 925" falsa; níquel (alergias) | Material base (不锈钢/铜/合金/925银), espesor del baño (电镀), 防过敏 (hipoalergénico) |
| **Ropa** | Tallas asiáticas (más chicas), diferencias de color | Tabla de medidas en cm (尺码表) por prenda, no tallas S/M/L; fotos con luz natural |
| **Muebles** | Aglomerado como "实木" (madera maciza); emisiones | 实木 vs 板材 (MDF/密度板), grado de emisión E0/E1, peso real y embalaje |
| **Juguetes** | Piezas pequeñas, pinturas con plomo | Edad recomendada, EN71/ASTM F963 si hay, olor fuerte = mala señal |
| **Cosmética** | Sin registro, vencimiento corto | Fecha de fabricación y vencimiento (保质期), fórmula/ingredientes; en Chile requiere registro ISP para vender |
| **Lentes de sol** | "UV400" sin respaldo | Prueba UV, material del lente (TAC polarizado, PC) |
| **Productos "iguales" más baratos** | Menos peso = menos material | Pide el peso neto por unidad (净重) y compáralo entre proveedores |

## 3. Qué preguntarle al vendedor antes de comprar

Plantillas en chino en `negociacion.md` §5. Lo mínimo:
- Material/composición exacta y gramaje/grosor/grado.
- Medidas y peso neto por unidad; peso y medidas de la caja individual y de la caja master (外箱尺寸, 毛重, 每箱数量).
- ¿Hay stock (现货) o se produce (需要生产)? ¿Plazo?
- Fotos y **video reales** del producto (实拍图/实拍视频), idealmente con una hoja con tu nombre o la fecha para confirmar que no son de internet.
- ¿El producto en bodega es igual al de las fotos? ¿La producción será igual a la muestra?
- Certificados que tengan (y para qué producto y empresa están emitidos).

## 4. Muestras y "muestra dorada"

- **Siempre muestras** si el pedido es de reventa o supera lo que estás dispuesto a perder. Pide muestras de 2–3 proveedores a la vez y compáralas lado a lado: ahorra semanas.
- Costo: muchos vendedores cobran la muestra y el flete interno; negocia que el costo se descuente del pedido grande (样品费可以抵扣货款).
- Envía las muestras a la bodega del agente y, si el monto lo justifica, trae las muestras a tu país por courier antes de comprar el volumen.
- Evalúa: medidas, peso, materiales, terminaciones, funcionamiento, empaque, olor, resistencia (uso intenso unos días).
- **Muestra dorada (封样)**: cuando apruebas una muestra, esa es la referencia contractual. Pide que el vendedor guarde una igual (封样留底), toma fotos detalladas y medidas, y deja por escrito en el chat: "大货必须和确认的样品一致" (la producción debe ser igual a la muestra confirmada).
- Muestra de producción (产前样 / 大货样): en pedidos personalizados, pide una muestra de la línea de producción antes del volumen, no solo una muestra artesanal.

## 5. Fotos y video QC

Cuando la mercadería llega a la bodega del agente/forwarder (o antes del despacho, al vendedor), pide:
1. Vista general de todas las unidades o de las cajas abiertas, y conteo.
2. Cada variante (color/talla) de frente y dorso.
3. **Medidas con huincha/pie de metro** en las dimensiones críticas (largo, ancho, alto, diámetro, largo de manga, etc.).
4. **Peso en balanza** de una unidad (compáralo con el de la muestra/ficha).
5. Primer plano de terminaciones: costuras, soldaduras, pegamentos, bordes, estampados, logos, cierres.
6. **Video funcional**: encender, cargar, abrir/cerrar, cierres, luces, sonido.
7. Etiquetas, manuales, empaque individual, caja master y marcas de envío.

Qué buscar al revisarlas: diferencia de color (色差), manchas, rayas, hilos sueltos, piezas faltantes, medidas fuera de tolerancia, logos torcidos, olor (preguntar), empaques dañados. Compara siempre contra la muestra dorada o la ficha. Si algo falla, reclama **antes** de confirmar la recepción en 1688 y antes del envío internacional: devolver dentro de China es barato; desde tu país casi imposible.

Si el agente ofrece fotos gratis limitadas, paga las extra en pedidos de reventa: es el seguro más barato que existe.

## 6. Inspección de terceros y AQL

**Cuándo contratarla**: pedidos de reventa de ~USD 2.000–3.000 hacia arriba, productos personalizados, electrónica, o proveedor nuevo. Por debajo de eso, las fotos/video QC detallados del agente suelen bastar.

**Tipos**:
- **PPI** (pre-producción): materiales y componentes antes de producir.
- **DUPRO** (durante producción, 20–50% avance): detecta problemas sistémicos a tiempo.
- **PSI** (pre-embarque, ≥80% empacado): la más común; muestreo aleatorio AQL.
- **CLC** (supervisión de carga de contenedor).
- **Auditoría de fábrica**: capacidad, procesos, condiciones.

**Costo orientativo 2026** (China, por día-hombre, en ciudades principales): empresas internacionales grandes (SGS, Bureau Veritas) ~USD 380–450; intermedias (QIMA, V-Trust) ~USD 250–320; firmas locales ~USD 180–280; QC remoto por video ~USD 120–180. Algunos agentes de compra/sourcing ofrecen inspecciones más baratas en su bodega.

**AQL (nivel de calidad aceptable)** — estándar ISO 2859-1 / ANSI Z1.4, nivel general II. Valores típicos para bienes de consumo:
- **Crítico: 0** (cualquier defecto que afecte la seguridad o incumpla normas rechaza el lote).
- **Mayor: 2,5** (el producto no se puede vender o falla en su función).
- **Menor: 4,0** (defecto leve que no impide la venta).

Calcula el plan con:
```
python3 scripts/china_tools.py aql --lote 1200 --mayor 2.5 --menor 4.0
```
Ejemplo: lote de 1.200 → letra J → muestra de 80 unidades; mayor 2,5: se acepta con ≤5 defectos mayores, se rechaza con 6; menor 4,0: acepta ≤7, rechaza con 8.

Entrega al inspector (o al agente) una **lista de verificación** con: especificaciones, medidas críticas y tolerancias, fotos de la muestra dorada, clasificación de defectos (qué es crítico/mayor/menor para este producto), pruebas funcionales, requisitos de empaque y etiquetado, cantidad por caja.

Deja acordado por escrito con el vendedor, **antes de pagar el saldo**, que el lote debe pasar la inspección y qué pasa si no (retrabajo a su costo, reposición, descuento).

## 7. Al recibir la mercadería

- Graba un **video continuo sin cortes** abriendo las cajas, desde la etiqueta de envío hasta el contenido: es la evidencia que piden las plataformas y agentes para reclamos.
- Cuenta, revisa una muestra representativa, prueba funcionamiento.
- Reclama rápido: en 1688 los plazos de reclamo tras la recepción son cortos (del orden de 48–72 horas para calidad o producto distinto en la recepción doméstica). Si la mercadería ya salió de China, el reclamo pasa a ser una negociación con el vendedor (reembolso parcial, reposición en el próximo pedido) — por eso el QC en China es tan importante.
- Registra el resultado en el archivo de proveedores.
