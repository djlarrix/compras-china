# Tallas, medidas y unidades chinas

Contenido:
1. Regla de oro: centímetros, no letras
2. Leer una tabla de tallas china (尺码表)
3. Ropa: cómo elegir la talla
4. Calzado
5. Unidades chinas (斤, 两, 寸, 尺)
6. Frases para preguntar talla

---

## 1. Regla de oro

Las tallas chinas suelen ser **1–2 tallas más chicas** que las latinoamericanas o europeas, y varían entre vendedores. Nunca elijas por la letra (S/M/L): compara **tus medidas en centímetros** con la tabla del vendedor, y lee las reseñas sobre el calce.

Mide con una huincha, sobre ropa delgada:
- **Pecho (胸围)**: contorno en la parte más ancha.
- **Cintura (腰围)**: contorno en la parte más angosta (o donde usas el pantalón).
- **Cadera (臀围)**: contorno en la parte más ancha.
- **Hombros (肩宽)**: de punta a punta del hombro por la espalda.
- **Largo de manga (袖长)**, **largo de prenda (衣长)**, **largo de pantalón (裤长)**, **entrepierna (内长/裆)**.
- **Pie (脚长)**: de pie, talón contra la pared, hasta la punta del dedo más largo, en mm.

## 2. Leer una tabla de tallas china

| Término | Significado |
|---|---|
| 尺码表 / 尺码 | Tabla de tallas / talla |
| 平铺 | Medida en plano (prenda estirada sobre la mesa): multiplica por 2 para el contorno |
| 胸围 / 腰围 / 臀围 | Contorno de pecho / cintura / cadera (de la **prenda**, salvo que diga 身体 o 净) |
| 衣长 / 袖长 / 肩宽 / 裤长 | Largo de prenda / manga / ancho de hombros / largo de pantalón |
| 建议身高 / 建议体重 | Estatura / peso recomendados (el peso suele venir en **斤**: 120斤 = 60 kg) |
| 偏大 / 偏小 / 正码 | Talla grande / talla chica / talla normal |
| 修身 / 宽松 / oversize | Ajustado / holgado / extra holgado |
| 误差1-3cm | Tolerancia de medición de 1–3 cm |
| 弹力 / 无弹 | Con elasticidad / sin elasticidad |
| 均码 | Talla única |

Tallas numéricas chinas en ropa: suelen venir como estatura/contorno, p. ej. **170/88A** = estatura 170 cm / pecho 88 cm / contextura A (normal). Letras: Y (delgado), A (normal), B (algo robusto), C (robusto).

## 3. Ropa: cómo elegir la talla

La prenda debe medir más que tu cuerpo: esa diferencia es la **holgura**.

| Calce deseado | Holgura en pecho (aprox.) |
|---|---|
| Ajustado (修身) | 2–6 cm |
| Regular | 8–12 cm |
| Holgado / oversize (宽松) | 15–25 cm |

Con el script:
```
python3 scripts/china_tools.py talla ropa --tabla "M:52,L:55,XL:58,2XL:61" --plano --medida 100 --calce regular
```
(`--plano` si la tabla está en 平铺; `--holgura 6` para fijarla a mano.) Revisa también largo y hombros, y en pantalones la cintura (sin elasticidad, la cintura de la prenda debe ser ≥ tu cintura + 2–4 cm).

Si el vendedor solo da estatura y peso, pídele la tabla en centímetros (frase en §6).

## 4. Calzado

- Chile y la mayoría de Latinoamérica usan **numeración EU**; en China, 码 (talla) suele coincidir con EU y las tablas indican el largo del pie en mm.
- Tabla china usual (aproximada): 35 = 225 mm · 36 = 230 · 37 = 235 · 38 = 240 · 39 = 245 · 40 = 250 · 41 = 255 · 42 = 260 · 43 = 265 · 44 = 270 · 45 = 275 · 46 = 280.
- Si la tabla dice **脚长** (largo del pie), compárala directo con tu medida; si dice **内长** (largo interior del zapato), suma 5–10 mm a tu pie.
- Horma: **偏大** (grande, baja media talla), **偏小** (chica, sube media o una talla), **正码** (normal); **脚宽/脚背高** (pie ancho / empeine alto): muchos compradores suben una talla.
- Conversión rápida:
```
python3 scripts/china_tools.py talla zapato --pie-mm 262
python3 scripts/china_tools.py talla zapato --us-hombre 9.5
```
Las equivalencias US/UK son aproximadas y varían por marca.

## 5. Unidades chinas

| Unidad | Equivale a | Dónde aparece |
|---|---|---|
| 斤 (jīn) | 500 g | Peso corporal recomendado, alimentos, peso de productos |
| 两 (liǎng) | 50 g | Alimentos, té |
| 公斤 | 1 kg = 2 斤 | Pesos formales |
| 克 (g) / 克重 | gramo / gramaje (g/m²) | Telas, papel |
| 寸 | En TV y pantallas: pulgada (2,54 cm). En ropa (腰围2尺3): 市寸 = 3,33 cm | Pantallas, cintura tradicional |
| 尺 | 10 市寸 = 33,3 cm | Cintura de pantalones (2尺3 = 76,6 cm) |
| 码 | En ropa y zapatos: "talla" (no yarda) | Tallas |
| 米 / 厘米 / 毫米 | m / cm / mm | Medidas |
| 毫安 (mAh) | Capacidad de batería | Power banks |
| 瓦 (W) | Potencia | Electrónica |

`python3 scripts/china_tools.py talla peso --jin 130` → 65 kg.

## 6. Frases para preguntar talla

```
请问有详细的尺码表吗？麻烦发一下每个尺码的平铺尺寸（胸围、衣长、肩宽、袖长），单位厘米。
```
> ¿Tiene una tabla de tallas detallada? Por favor envíe las medidas en plano de cada talla (pecho, largo, hombros, manga) en centímetros.

```
我身高175cm，体重70公斤（140斤），胸围100cm，平时穿L码，想要宽松一点，建议穿哪个码？
```
> Mido 175 cm, peso 70 kg (140 斤), pecho 100 cm, normalmente uso L y lo quiero algo holgado. ¿Qué talla me recomienda?

```
这款鞋偏大还是偏小？我的脚长是262毫米，脚比较宽，穿哪个码合适？
```
> ¿Este zapato calza grande o chico? Mi pie mide 262 mm y es algo ancho, ¿qué talla me conviene?
