# Web_data_house_pricing
En este repositorio incorporaremos los archivos que utilizaremos para la aplicación web en PythonAnywhere

## Descripción del proyecto

El conjunto de datos utilizado para este proyecto es House Pricing Dataset, disponible en Kaggle.
### Proceso de Análisis Exploratorio de Datos (EDA):

Antes de entrenar modelos, se estudió el tipo de variables que formaban el dataset y sus distribuciones. A partir de la información extraída, se procedió a la limpieza.

#### Limpieza de datos:

La primera etapa consistió en la limpieza y preparación de los datos. Los detalles de este proceso pueden consultarse en el notebook `rama_test.jpynb`. Aquí se eliminaron las columnas irrelevantes como por ejemplo `zipcode` o `ID`, a parte de otras que aportaban poca información.

Se estudió el target del modelo, `price`, y se apreció que tenía una distribución de cola larga, con la mayoría de valores concentrados por debajo del millón de dólares, mientras que unos pocos que pasaban los 7 millones de dólares. Para tratar los outliers, primero se transformó a escala logarítmica, por lo que aparecieron valores extremos tanto por arriba como por abajo de la distribución, por lo que se eliminaron ambos para poder tener una distribución más centralizada.

Por último, la variable categórica `condition` que registra el estado de la propiedad se ha tratado con un one-hot-encoding. Quedando así un dataset de 19 columnas y unas 21000 entradas.

### Entrenamiento del modelo

Para tratar de dar la mejor predicción posible teniendo en cuenta las limitaciones del servidor, se han estudiado diferentes modelos para tratar de dar con las condiciones óptimas.

En todos los modelos se comenzó empleando todas las variables del conjunto de datos tras la limpieza.

#### Modelo base - linear_model (baseline):

Se entrenó un modelo de regresión lineal con el objetivo de establecer una línea base de comparación.

#### Modelo XGBoost:
Se intentó aplicar un modelo XGBoost para mejorar el rendimiento, pero fue descartado debido a limitaciones de memoria en la plataforma PythonAnywhere.

#### Modelo final – Random Forest:

Dado el inconveniente anterior, se optó por utilizar un modelo de Random Forest que está incluido en la librería de `Scikit-Learn`, el cual fue seleccionado como modelo final del proyecto.

En el estudio del rendimiento del modelo, obtuvimos un error MAE de 78725.08, que representa un error de predicción del 15%.

Testeando el rendimiento del modelo y la importancia de las variables, se acabó descartando el one-hot-encoding de la varialbe `coindition` ya que el resultado de modificar esta variable no representaba ninguna variación apreciable en la predicción del precio de la vivienda. 

### Desarrollo web

