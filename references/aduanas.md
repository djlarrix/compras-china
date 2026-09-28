# Aduana e impuestos por país de destino

Contenido:
1. Principios comunes
2. Chile (detallado)
3. Perú
4. Colombia
5. Argentina
6. Ecuador
7. Uruguay
8. México
9. Estados Unidos
10. Unión Europea y España
11. Otros países: qué verificar
12. Código arancelario (HS)
13. Cálculo con el script

Resumen rápido para compras vía agente/courier desde China (verificar siempre):

| País | Franquicia / umbral | Qué se paga sobre eso | Preset del script |
|---|---|---|---|
| Chile | Sin franquicia desde 25-oct-2025. Plataformas inscritas en SII: IVA en la compra, sin arancel hasta USD 500 | Arancel 6% (0% con origen TLC) + IVA 19% | `chile`, `chile-tlc`, `chile-plataforma` |
| Perú | Hasta USD 200 FOB sin tributos (en revisión) | Ad valorem 0/6/11% + IGV 16% + IPM 2%; courier hasta USD 2.000 | `peru` |
| Colombia | Reglas de IVA en cambio (2025–2026) | Courier: arancel ~10% (origen sin TLC) + IVA 19% | `colombia` |
| Argentina | USD 400 FOB por envío, 5 envíos/año (jul-2026) | Excedente: régimen general (derechos + tasa estadística + IVA 21% + percepciones) | `argentina` |
| Ecuador | 4x4: ≤ 4 kg y ≤ USD 400 FOB | USD 20 fijos por paquete | `ecuador-4x4` |
| Uruguay | USD 800 al año en hasta 3 envíos (desde may-2026) | Luego, tasa sobre el valor (ver §7) | `generico` |
| México | Sin franquicia para origen sin tratado | Mensajería: tasa global 33,5% (hasta ~USD 2.500) | `mexico-courier` |
| EE.UU. | De minimis suspendido | Arancel MFN + Sección 301 (+ recargos vigentes) | `us` |
| UE / España | Envíos ≤ EUR 150: EUR 3 por línea arancelaria (jul-2026 a jul-2028) | + IVA (España 21%) | `eu`, `espana` |

**Advertencia**: las reglas de importación cambiaron mucho en 2025–2026 y siguen cambiando. Todo lo de abajo es una fotografía a **septiembre de 2026**. Antes de dar cifras al usuario, verifica en fuentes oficiales (aduana y servicio de impuestos del país) con una búsqueda web y cita la fecha. Si no puedes verificar, dilo.

---

## 1. Principios comunes

- **Valor en aduana**: la mayoría de los países cobra sobre **CIF** (producto + flete + seguro); EE.UU. cobra aranceles sobre el valor de transacción sin el flete internacional (≈FOB). El IVA/IGV normalmente se calcula sobre CIF + arancel.
- **Declara el valor real**. Subdeclarar es infracción aduanera o fraude: multas, retención, decomiso y antecedentes para futuras importaciones. La aduana compara con bases de precios y puede pedir la factura y el comprobante de pago. Los precios de 1688 son bajos y reales: úsalos.
- **Uso personal vs comercial**: muchas franquicias y regímenes simplificados son para uso personal; la reventa puede exigir importar formalmente, registro tributario y certificaciones.
- **Certificaciones**: electrónica, cosméticos, alimentos, juguetes y productos médicos suelen requerir autorización o certificación para vender, aunque pasen la aduana.
- **Tratados de libre comercio con China** (Chile, Perú, Costa Rica, Ecuador, entre otros en la región) pueden bajar el arancel a 0% con prueba de origen; el vendedor debe tramitarla en China.

## 2. Chile

### Compras en plataformas inscritas en el SII (hasta USD 500)
Desde el **25 de octubre de 2025** (Ley 21.713, de Cumplimiento Tributario):
- Las plataformas inscritas en el SII cobran el **IVA de 19% al momento de la compra** para bienes de hasta USD 500, y esas compras **no pagan arancel**. Al llegar no pagas nada más.
- Inscritas (a la fecha de la fuente): AliExpress, Amazon, Shein, Temu, Shopee y otras. La lista vigente está en el sitio del SII: revísala para saber si un agente o tienda está inscrito.
- Se **eliminó la franquicia de USD 41**: ya no existen compras chicas libres de impuestos.

### Compras directas o vía agentes/casillas no inscritos
Cuando la plataforma o el intermediario no cobró el IVA (típico de 1688 vía agente, forwarder o casilla, salvo que estén inscritos):
- Pagas al ingresar: **arancel ad valorem 6% sobre CIF** (0% si se acredita origen chino bajo el TLC, ver abajo) + **IVA 19% sobre (CIF + arancel)**.
- Los cobra el courier, Correos de Chile o el agente de aduana, más sus cargos de gestión.
- Ejemplo oficial de Aduana: CIF USD 1.000 → arancel USD 60 → IVA 19% × 1.060 = USD 201,40.
- **CIF** = valor de la mercadería (con flete interno en China) + flete internacional + seguro. Si no hay seguro contratado, Aduana puede aplicar un seguro presunto (tradicionalmente 2% del FOB; verificar).

### TLC Chile–China: arancel 0%
- La mayoría de los productos de origen chino tienen arancel 0% bajo el TLC, pero solo si se acredita el origen con **Certificado de Origen Form F** (lo emite la aduana china o el CCPIT; lo solicita el vendedor/exportador). Sin prueba de origen se cobra el 6%.
- En envíos courier pequeños, en la práctica suele cobrarse el 6% porque no viene el certificado; pregunta al courier/casilla si pueden aplicar la preferencia y qué documento necesitan. En importaciones medianas y grandes, pedir el Form F al proveedor casi siempre conviene (ahorra 6% del CIF). Pídelo **antes** del despacho: debe coincidir con la factura.

### Montos y trámite
- Hasta **USD 1.000 FOB**: el importador puede tramitar personalmente en forma simplificada.
- Vía empresas courier (envío de entrega rápida): hasta **USD 3.000 FOB** se despacha sin agente de aduana (declaración simplificada con pago simultáneo), siempre que el envío cumpla las condiciones.
- Sobre USD 1.000 FOB en carga normal (aérea/marítima), o sobre USD 3.000 por courier: **agente de aduana obligatorio**. Presupuesta sus honorarios y los gastos locales (desconsolidación, almacenaje, transporte).
- Chile exige el **RUT del destinatario** en los envíos.

### Importar para revender
- Importa con **RUT de empresa** o como persona con inicio de actividades: el IVA pagado en la importación es **crédito fiscal** que se descuenta del IVA de tus ventas. Con RUT personal sin giro, ese IVA es costo.
- Emite boleta/factura por las ventas; lleva los documentos de importación (DIN, factura del proveedor, comprobantes).
- Considera el costo de certificaciones al evaluar el negocio.

### Certificaciones y permisos frecuentes (para comercializar)
- **SEC** (Superintendencia de Electricidad y Combustibles): muchos productos eléctricos y a gas (cargadores, alargadores, ampolletas LED, electrodomésticos, herramientas eléctricas, estufas) requieren certificación; la responsabilidad es del importador. Revisa en sec.cl si tu producto está en la lista.
- **ISP** (Instituto de Salud Pública): cosméticos, medicamentos, dispositivos médicos: registro/autorización antes de vender.
- **SAG** (Servicio Agrícola y Ganadero): alimentos, semillas, plantas, productos animales, y embalajes de madera (deben tener tratamiento ISPM 15).
- **Seremi de Salud**: alimentos y algunos artículos de uso personal.
- **Juguetes**: sin certificación previa en aduana, pero deben cumplir normas de seguridad del Ministerio de Salud; lámparas con forma de juguete están prohibidas.
- **Equipos de radiofrecuencia** (algunos dispositivos inalámbricos): pueden requerir homologación de Subtel.
- **Falsificaciones**: Aduana retiene mercadería que infringe marcas (medidas en frontera); se pierde la mercadería.

### Paso a paso típico (compra directa en 1688 → Chile)
1. Confirma si el producto necesita certificación (SEC/ISP/SAG) y, si es para reventa, si importarás con RUT de empresa.
2. Compra en 1688 (o vía agente) y envía a la bodega del agente/casilla en China.
3. QC en bodega, consolidación, elige línea: courier/casilla (menos de ~USD 3.000 FOB) o carga con agente de aduana.
4. Entrega factura comercial con el valor real (y Form F si aplica), packing list, RUT del destinatario.
5. Paga en Chile arancel (6% o 0%) + IVA 19% + cargos del courier/agente, o verifica que ya estén incluidos si la línea es "con impuestos incluidos".
6. Recibe, revisa, guarda todos los documentos (sirven para el crédito fiscal y para reclamos).

## 3. Perú

- **Hasta USD 200 FOB** (valor de la mercadería, sin contar el flete) por envío: sin trámite ni tributos, por courier o Serpost ("Importa Fácil"). La SUNAT ha planteado cobrar IGV también a compras menores de USD 200 en plataformas (se mencionó el segundo semestre de 2026), sin norma publicada a la fecha de la fuente: **verificar**.
- **Courier (envíos de entrega rápida) hasta USD 2.000 FOB**: sobre USD 200 se pagan ad valorem (0%, 6% u 11% según partida), IGV 16% e IPM 2% (18% en conjunto) sobre CIF + ad valorem.
- **TLC Perú–China** (vigente desde 2010): muchos productos con arancel 0% acreditando el origen.
- Sobre USD 2.000 FOB: importación formal con agente de aduana.

## 4. Colombia

- Modalidad de **tráfico postal y envíos urgentes** (courier): hasta USD 2.000 por envío.
- Para mercadería de origen sin TLC (China), en envíos de hasta USD 200 se aplica un arancel del 10% y el IVA de 19%; sobre USD 200, arancel según la partida + IVA 19%.
- Las reglas de exclusión de IVA para envíos de bajo valor cambiaron en 2025–2026 (se reportó un umbral de USD 50 durante 2026 y ajustes por decreto): **verificar en la DIAN** antes de calcular.
- Uso comercial y montos mayores: importación ordinaria con agencia de aduanas.

## 5. Argentina

- **Decreto 604/2026 (17-jul-2026)** unificó correo postal y courier ("puerta a puerta"): **franquicia de USD 400 FOB por envío**, con un máximo de **5 envíos por persona al año**; dentro de la franquicia no se pagan derechos de importación ni tasa de estadística (sí tasas de servicio). Fuentes indican que dentro de la franquicia se paga IVA: verificar.
- El **excedente** sobre USD 400 tributa por el régimen general de importación para consumo (derechos según NCM, tasa de estadística, IVA 21% y percepciones). Se eliminó la alícuota única del 50%.
- Límite por envío del régimen courier: USD 3.000.
- Como las reglas son recientes, confirma la reglamentación vigente de ARCA.

## 6. Ecuador

- **Courier categoría B ("4x4")**: paquetes de hasta 4 kg y USD 400 FOB. Desde el 16-jun-2025 pagan una **tarifa fija de USD 20 por paquete**, además del flete y servicio del courier. El régimen perdió atractivo y varios couriers cerraron.
- Sobre esos límites: categorías con tributos normales (arancel según partida + IVA).
- Ecuador tiene TLC con China (2024): revisar preferencias en importaciones formales.

## 7. Uruguay

- Desde el **1-may-2026**: franquicia anual de **USD 800** por persona adulta, distribuida en hasta **3 envíos** al año.
- Agotada la franquicia, envíos de hasta USD 800 pueden ingresar pagando una tasa sobre el valor de la factura (reportada como 60%) y el IVA según corresponda: **verificar** en la Dirección Nacional de Aduanas antes de calcular.

## 8. México

- **Reforma arancelaria vigente desde el 1 de enero de 2026**: aumentó los aranceles de nación más favorecida (en general entre 5% y 50%) para numerosas fracciones de países sin tratado con México, lo que incluye a China.
- **Mensajería y paquetería (régimen simplificado)**: para envíos de origen sin tratado, se usa en general una **tasa global de 33,5%**, con un valor máximo de unos USD 2.500 para calificar.
- IVA general 16%. Importaciones comerciales formales requieren padrón de importadores y agente aduanal.
- Verifica en la ANAM y el SAT las tasas vigentes para tu fracción arancelaria.

## 9. Estados Unidos

- **De minimis (USD 800) suspendido**: todos los envíos comerciales de bajo valor pagan aranceles. CBP formalizó la suspensión indefinida por reglas provisionales en junio de 2026, y la ley ("One Big Beautiful Bill Act") deroga la exención a partir del 1 de julio de 2027.
- **Aranceles**: la Corte Suprema anuló los aranceles basados en IEEPA (20 de febrero de 2026; terminaron el 24 de febrero de 2026). Siguen los aranceles de la **Sección 301** sobre productos chinos (listas con tasas de 7,5% a 25% y más en categorías como vehículos eléctricos, semiconductores o acero), más el arancel general (MFN). Tras el fallo se aplicó un recargo temporal bajo la Sección 122; **verifica si sigue vigente**.
- Entradas formales sobre USD 2.500 requieren bono aduanero y normalmente un customs broker.
- Verifica tasas por código HTS en el sitio de USITC/CBP.

## 10. Unión Europea y España

- **Desde el 1 de julio de 2026**: se eliminó la exención de aranceles para envíos de hasta EUR 150 y se aplica un **arancel fijo temporal de EUR 3 por artículo** (por cada línea arancelaria distinta dentro del paquete) hasta el 1 de julio de 2028; después se aplicarán los aranceles normales.
- **IVA** en todas las importaciones desde julio de 2021 (España: 21% general); las plataformas con IOSS lo cobran al comprar.
- Sobre EUR 150: arancel normal según código TARIC + IVA.
- Muchos productos necesitan **marcado CE** y cumplir normas de seguridad (juguetes EN71, electrónica, etc.) para venderse.

## 11. Otros países: qué verificar

Para cualquier destino, busca en la web (fuentes oficiales primero) y responde:
1. ¿Existe franquicia o de minimis? ¿Para impuestos, aranceles o ambos? ¿Solo para uso personal?
2. ¿Hay régimen courier/simplificado? Límite de valor, tasa, número de envíos permitido por año.
3. Arancel para el código HS del producto y si hay **TLC con China** que lo reduzca (Perú, Costa Rica y Ecuador tienen TLC con China).
4. IVA/IGV y otros impuestos (percepciones, tasas estadísticas, impuestos internos).
5. ¿Se necesita registro de importador o agente de aduana desde cierto monto?
6. Productos restringidos y certificaciones necesarias para vender.
7. ¿Qué plataformas cobran impuestos en la compra en ese país?

Resume los resultados con la fecha de consulta y las fuentes.

## 12. Código arancelario (HS)

- El Sistema Armonizado tiene 6 dígitos comunes a todos los países; cada país agrega dígitos (Chile usa 8 en su Arancel Aduanero).
- El código define el arancel, las certificaciones y a veces la línea de envío. Puedes sugerir un código probable según la descripción del producto, pero **confírmalo con el agente de aduana o la aduana** si el monto es relevante.
- Pide al proveedor el código HS de exportación chino como referencia (los primeros 6 dígitos suelen coincidir).

## 13. Cálculo con el script

```
python3 scripts/china_tools.py costo --pais chile --precio-cny 12.8 --unidades 300 \
  --flete-china-cny 20 --pago-pct 3.5 --kg 30 --usd-kg 12 --gastos-locales-usd 25 \
  --tc auto --tc-local auto --precio-venta 9990
```

- `--tc auto` y `--tc-local auto` usan el tipo de cambio del día.
- Presets: `chile`, `chile-tlc`, `chile-plataforma`, `peru`, `colombia`, `argentina`, `ecuador-4x4`, `mexico-courier`, `us`, `eu`, `espana`, `generico`. Sobrescribe con `--arancel-pct`, `--iva-pct`, `--arancel-fijo-usd`, `--base fob|cif`.
- `--impuestos-incluidos` para líneas DDP; `--empresa` si importas con empresa (IVA como crédito fiscal).
- Los presets son aproximaciones de la regla general: el arancel real depende del código HS del producto.
