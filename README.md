# Herramienta de Sesgos y Equidad - UAI


Este es el repositorio de la herramienta de sesgos y equidad desarrollada por el equipo del proyecto de algoritmos éticos responsables del GobLab en la Universidad Adolfo Ibáñez.

## Descripción

Esta herramienta puede ser usada por cualquier persona de TI que desee analizar sesgos y equidad en un proceso de inteligencia artificial. La herramienta permite cargar datos del dataset y la salida del modelo, y luego analizar los sesgos y la equidad del modelo. La herramienta permite analizar sesgos en diferentes grupos de datos, y también permite analizar la equidad del modelo en base a diferentes métricas de equidad.

## Instalación

Para instalar la herramienta, se debe clonar el repositorio y luego instalar las dependencias necesarias. Para clonar el repositorio, se debe ejecutar el siguiente comando:

```bash
git clone https://github.com/GobLab-UAI/Herramienta_de_sesgos_y_equidad.git

```

Luego, se debe crear un ambiente virtual en python e instalar las dependencias necesarias. Para ello, se debe ejecutar el siguiente comando:

```bash
cd Herramienta_de_sesgos_y_equidad
python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```
Finalmente, se debe ejecutar el siguiente comando para iniciar la herramienta:

```bash
streamlit run app.py
```

>[!NOTE]
>
>Esta herramienta no almacena ni comparte tus datos, ya que todo el procesamiento se realiza en tu computadora y no se envía a ningún servidor externo.


## Uso de la herramienta

Para usar la herramienta, se debe cargar un archivo de datos y un archivo de salida del modelo. Luego, se debe seleccionar las columnas de datos y la columna de predicciones. Finalmente, se debe seleccionar las columnas de grupos y las métricas de equidad que se desean analizar.

## Paso 1: Cargar datos

Se pueden cargar archivos `.csv` o `.xlsx` con los datos y las predicciones del modelo. Para cargar los datos, se debe hacer clic en el botón `Cargar datos` y seleccionar el archivo con los datos. Luego debe escribir el nombre de la hoja que quiere cargar y como desea tratar los datos faltantes.

### Formato de los datos
Los datos que se cargan deben tener la siguiente estructura:

| Columna 1 | Columna 2 | ... | Real | Predicciones |
|---|---|---|---|---|
| Valor 1 | Valor 2 | ... | 1 | 1 |
| Valor 1 | Valor 2 | ... | 0 | 1 |

## Paso 2: Seleccionar columnas

En este paso se puede realizar la selección de algunas columnas del conjunto de datos a revisar.

## Paso 3: Seleccionar grupos

En este paso se puede realizar la selección de los grupos a revisar y ver la distribución de las categorías.

## Paso 4: Análisis de sesgos

Finalmente, en este paso se seleccionan las categorías de referencia y se entrengan las métricas de equidad.

## Agradecimientos

ANID + Subdirección de Investigación Aplicada/Concurso IDeA I+D 2023 + ID23I10357
