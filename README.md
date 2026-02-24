# 🍷 Análisis Estructural de Vinos – Dataset Vivino


## 📌 Descripción del Proyecto

Este proyecto construye un dataset académico estructurado de vinos disponibles en España utilizando el endpoint público explore de la API de Vivino (https://www.vivino.com/es/). La fecha del scrapping es 20/02/2025.

## 🎯 Objetivo

Analizar la relación entre las características estructurales del vino y su valoración por parte de los consumidores. El proyecto no pretende determinar la calidad objetiva del vino, sino estudiar patrones en datos de consumo reales.

## ❓ Preguntas de Investigación

¿Qué factores influyen en la calificación de los vinos españoles? <br>
¿Hay diferencias estructurales por región? <br>
¿Hay alguna característica que varíe según el tipo de uva? <br> 
¿Un precio más alto significa mejor puntuación?

## 🗂 Estructura del Proyecto

```bash
project/
├── main.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── scrapping.py
├── notebooks/
│   └── eda.ipynb
├── src/
│   ├── __init__.py
│   ├── io.py
│   ├── cleaning.py
│   ├── features.py
│   ├── viz.py
│   └── utils.py
├── graphs/
├── README.md
└── requirements.txt
```

## 📎 Dataset

En el archivo "vivino_all_types.csv", con 7965 filas y 17 columnas, podemos encontrar las siguientes variables:

- Variables estructurales del vino (style_body, style_acidity, intensity, tannin, sweetness)

- Ratings, número de reseñas (num_reviews) y precio (price)

- Información geográfica (country, region) y añada (year)

- Segmentación por tipo de vino (wine_name, winery, wine_type, style)

- Stock (variable ficticia para "ensuciar" un poco más el dataset)

## 🔧 Data Issues & Fixes

- Un solo país (lo cual es positivo porque solamente queremos analizar España), no nos aporta nada.

    -> Lo eliminamos del dataset porque es redundante.

- El estilo muchas veces dice "(España)" después de la cepa.

    -> Lo eliminamos para que quede mejor visualmente.

- El stock tiene que tener formato de integer y está en string, ya que tiene valores que no son númericos.

    -> Lista de equivalencias de números en string a integer y depuración.

- Valores faltantes en algunas columnas.

    -> Para los stocks, los completamos con "0" asumiendo que no hay de ese tipo de vino.  

- Hay un vino blanco al que no se le completaron algunos datos.

    -> Variables numéricas como promedio del grupo "Vinos Blancos de Ribera del Duero" y "style" como valor más frecuente.

- El nombre del vino muchas veces tiene su añada al final (ya tenemos esta información)

    -> Lo depuramos para que quede mejor visualmente.

## ▶️ Pipeline

raw → clean → features (export a `data/processed/`) → viz → (export a `graphs/`)

## 🚀 Cómo Ejecutar

- `pip install -r requirements.txt`
- Ejecutar pipeline: `python main.py`
- (Opcional) Abrir y ejecutar: `notebooks/eda.ipynb`

## 🔎 Hallazgos y Conclusión

Pudimos confirmar varios supuestos del mundo del vino con nuestro conjunto de datos. Por ejemplo, que hay cepas de vinos que están mucho más presentes en ciertas zonas que en otras (en gran parte gracias a lo que conocemos como Denominación de Orígen) O también, que cuánto más antiguo es un vino, más le suele gustar a la gente.

Sin embargo, nos podemos también llevar algunas sopresas. Que haya cepas más presentes en ciertas zonas no quiere decir que allí tengan la mejor puntuación (como el Verdejo en Castilla y León o Valencia comparadas a Rueda). 

También encontramos que no necesariamente a mayor precio, mayor puntuación. Esto da lugar a encontrar varias joyas ocultas: vinos infravalorados en relación precio/calidad.

## 🎁 Bonus: Simulador de Compra Optimizada de Vinos

Además del análisis y limpieza de datos, este proyecto incluye un **widget interactivo tipo CLI** que permite simular compras de vinos con restricciones presupuestarias y preferencias de usuario.  

### Funcionalidades principales

- **Presupuesto controlado:** el usuario define cuánto quiere gastar (máximo 100.000 €).  
- **Selección de tipos de vino:** se puede elegir uno, varios o todos los tipos disponibles (`Red`, `White`, `Rose`, `Dessert`, `Sparkling`, `Fortified`).  
- **Optimización inteligente:** el algoritmo selecciona los vinos que maximizan el **rating por euro**, priorizando también los que tienen más reseñas en caso de empate.  
- **Restricción de stock:** no se puede comprar más unidades de las disponibles en inventario (`stock`).  
- **Resumen detallado:** al finalizar, el simulador muestra:
  - Total gastado y presupuesto restante.
  - Unidades compradas por vino.
  - Distribución por tipo de vino.
- **Registro histórico:** cada simulación se guarda automáticamente en `budget_optimizer.log` con fecha, inputs y resultados completos, permitiendo revisar decisiones pasadas.  

### Cómo usarlo

1. Ejecutar el notebook `budget_optimizer.ipynb`.  
2. Seguir las instrucciones en la CLI para ingresar el presupuesto y seleccionar los tipos de vino.  
3. Revisar los resultados en pantalla y consultar `budget_optimizer.log` para ver el historial completo.  

## ⚠️ Aviso

Este proyecto tiene fines exclusivamente académicos y de demostración técnica. Esta prueba de concepto tiene algunas limitaciones. En primer lugar, la lista de vinos extraídos no necesariamente ofrece una visión completa y exhaustiva del vino español. En segundo lugar, los vinos que se muestran solo incluyen los que están disponibles actualmente para su compra. Por último, al tratarse de una base de datos de consumidores, los resultados de las valoraciones pueden no representar opiniones profesionales.

## 👨‍💻 Autor

Juan T. | Data Science