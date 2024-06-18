import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import sklearn
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

import smtplib
import ssl
from email.message import EmailMessage
 
 
col1, col2, col3 = st.columns(3)

# Mostrar la primera imagen en la primera columna
with col1:
    st.write("")
    st.image("_statics/Logo_herramientas_algoritmos.png")
with col2:
    #st.image("_statics/UAI.png")
    pass
    
# Mostrar la segunda imagen en la segunda columna
with col3:
    st.image("_statics/Goblab.png")




st.title('Herramienta para medición de sesgos y equidad')
st.markdown(f"<h3 style='text-align: left; color: black;'>V.2.0.0</h3>", unsafe_allow_html=True)

st.write("""
    Esta herramienta es un apoyo para la medición de sesgos en los modelos de ciencia de datos de clasificación binaria. Su objetivo es medir las tasas de disparidad en las variables protegidas de un conjunto de datos, para utilizar este análisis en la creación modelos de ciencias de datos más equitativos y responsables con la ciudadanía. Para la medición de sesgos se utilizan 4 métricas: tasa de falsos positivos, tasa de falsos negativos, tasa de falsa omisión y tasa de falso descubrimiento. 
    
    La herramienta está desarrollada en Python, y se espera que los usuarios sean científicos de datos o posiciones afines. 
    Debe ser utilizada en la fase de desarrollo del piloto, durante la etapa de evaluación de las métricas del modelo de ciencia de datos. 
         
    Para más información sobre las fases, consultar la Guía Permitido Innovar (https://www.lab.gob.cl/permitido-innovar).  
    
    Para utilizar la herramienta, es necesario contar con el conjunto de datos en formato *.xsls* o *.csv* Como requisito mínimo, este conjunto de datos debe contener una columna para las predicciones que generó el modelo (binario), una columna para los valores reales (binario), y las columnas de las variables protegidas. A partir de esto, se seleccionan las variables protegidas del proyecto y se calcula la matriz de confusión y métricas de medición de sesgos. 
         
    La elección de las variables protegidas es realizada por el usuario de la herramienta y se debe llevar a cabo en conformidad con la legislación chilena actual (Ley N° 20.609), que establece la no discriminación arbitraria para las siguientes variables protegidas: la raza o etnia, el sexo, la nacionalidad, la situación socioeconómica, el idioma, la ideología u opinión política, la religión o creencia, la sindicación o participación en organizaciones gremiales o la falta de ellas, la maternidad, la lactancia materna y el amamantamiento, la orientación sexual, la identidad y expresión de género, el estado civil, la edad, la filiación, la apariencia personal y la enfermedad o discapacidad. 
    
    El flujo de la herramienta de medición de sesgos y equidad está basado en Aequitas (2019, Ghani).
""")


# Método para enviar un correo electrónico
def send_feedback_email(feedback):
    try:
        # Configura los detalles del correo electrónico
        msg = EmailMessage()
        msg['Subject'] = 'Nuevo feedback para la Model UAI'
        msg['From'] = 'jspinad@gmail.com'
        msg['To'] = 'goblab@uai.cl'
        msg.set_content(feedback)

        context = ssl.create_default_context()

        # Configura los parámetros del servidor SMTP y envía el correo electrónico
        with smtplib.SMTP_SSL('smtp.gmail.com', 465,context=context) as smtp:
            smtp.login('jspinad@gmail.com', 'caar kfqv zjoo isfn')
            smtp.sendmail("jspinad@gmail.com","goblab@uai.cl",msg.as_string())
        
        st.success("¡Feedback enviado con éxito!")
    except Exception as e:
        st.error("Error al enviar el feedback.")
        st.error(e)

def preparar_seccion_html(clave, valor, prefijo="", sufijo=""):
    """Devuelve una cadena HTML para la sección si el valor no está vacío, de lo contrario devuelve una cadena vacía."""
    if valor:  # Verifica si el valor existe y no está vacío
        return f"{prefijo}{clave}: {valor}{sufijo}"
    return ""


st.sidebar.title("Feedback")
# Crea un formulario para el feedback
with st.sidebar.form(key='feedback_form', clear_on_submit=True):
    feedback = st.text_area("💬 Si tienes alguna sugerencia o comentario, deja tu feedback aquí:",key="feedback")
    submit_button = st.form_submit_button(label='Enviar Feedback 🚀 ')

    if submit_button and feedback:
        send_feedback_email(feedback)
        

file_uploaded = st.file_uploader('Upload a file', type=['csv', 'xlsx'])

if file_uploaded is not None:

    df = pd.DataFrame()
    if file_uploaded.name.endswith('csv'):
        sep = st.text_input('¿Cual es el separador de tu archivo?, si es una coma, déjalo vacío')
        df = pd.read_csv(file_uploaded,sep=sep)
    elif file_uploaded.name.endswith('xlsx'):
        sheet_name = st.text_input('¿Cual es el nombre de la hoja donde está tu archivo?, si solo hay una déjalo en blanco',value=None)
        if sheet_name is None:
            sheet_name = 0
        na_values = st.selectbox('¿Cómo se deben tratar los valores NaN? ', [" ",'0',None,np.nan],index=0)

    #button = st.button('Analyze')
    #if button:

        df = pd.read_excel(file_uploaded, keep_default_na=False, sheet_name=sheet_name, na_values=[na_values])

    st.write("Este es el dataset que se ha cargado:")
    st.write(df.head())
    st.write("---")
    cols = st.multiselect('Selecciona las columnas que quieres analizar', df.columns)
    sub_df = df[cols]
    st.write(df[cols])

    real_column = st.selectbox('Selecciona el nombre de la columna que contiene los valores reales', df.columns)
    prediction_column = st.selectbox('Selecciona el nombre de la columna que contiene las predicciones de tu modelo', df.columns)

    col1, col2 = st.columns(2)
    with col1:
        # Contamos la frecuencia de cada etiqueta
        st.write('Distribución de las etiquetas reales')
        category_counts = sub_df[real_column].value_counts()

        # Creamos un gráfico de torta
        fig, ax = plt.subplots()
        ax.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Asegura que el gráfico de torta sea circular.

        # Mostramos el gráfico en Streamlit
        st.pyplot(fig)
    
    with col2:
        # Contamos la frecuencia de cada etiqueta
        st.write('Distribución de las etiquetas predichas')
        category_counts = sub_df[prediction_column].value_counts()

        # Creamos un gráfico de torta
        fig, ax = plt.subplots()
        ax.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')

        st.pyplot(fig)

    st.write('---')

    label = st.selectbox('Seleccione la columna a analizar en equidad', sub_df.columns)

    unique_values = sub_df[label].unique()
    st.write('Valores únicos de la columna seleccionada:', unique_values)

    col3, col4 = st.columns(2)

    with col3:
        category = st.radio('Seleccione la categoría de referencia', unique_values)
        sub_df_hombres = sub_df[sub_df[label] == category]
        st.write(sub_df_hombres)        

        matriz_1 = sklearn.metrics.confusion_matrix(sub_df_hombres[real_column], sub_df_hombres[prediction_column])

        plt.figure(figsize=(10, 8))  # Puedes ajustar el tamaño según tus necesidades
        sns.heatmap(matriz_1,
            xticklabels=["POSITIVA", "NEGATIVA"],
            yticklabels=["POSITIVA", "NEGATIVA"],
            cmap='coolwarm',  # Elige el mapa de colores que prefieras
            annot=True,  # Muestra los valores de correlación}
            linewidths=.5,
            fmt='g')  # Ajusta el espaciado entre las celdas si es necesario
        plt.title(f"Matriz de confusión para la categoría {category}")

        st.pyplot(plt)
    
    with col4:
        category2 = st.radio('Seleccione categoría a comparar ', unique_values)
        sub_df_mujeres = sub_df[sub_df[label] == category2]
        st.write(sub_df_mujeres)

        matriz_2 = sklearn.metrics.confusion_matrix(sub_df_mujeres[real_column], sub_df_mujeres[prediction_column])

        plt.figure(figsize=(10, 8))  # Puedes ajustar el tamaño según tus necesidades
        sns.heatmap(matriz_2,
            xticklabels=["POSITIVA", "NEGATIVA"],
            yticklabels=["POSITIVA", "NEGATIVA"],
            cmap='coolwarm',  # Elige el mapa de colores que prefieras
            annot=True,  # Muestra los valores de correlación}
            linewidths=.5,
            fmt='g')  # Ajusta el espaciado entre las celdas si es necesario
        plt.title(f"Matriz de confusión para la categoría {category2}")

        st.pyplot(plt)
    
    st.write('---')

    #Obtener TP, TN, FP, FN hombres 
    tn1, fp1, fn1, tp1 = matriz_1.ravel()

    tn2, fp2, fn2, tp2 = matriz_2.ravel()

    #False positive rate
    #Hombres
    #st.write("Tasa de falsos positivos para la categoría ", category)
    
    fpr_1 = fp1/(fp1+tn1)
    #st.write(fpr_1)
    #Mujeres 
    #st.write("Tasa de falsos positivos para la categoría ", category2)
    fpr_2 =fp2/(fp2+tn2)
    #st.write(fpr_2)
    #False negative rate 
    #Hombres 
    #st.write("Tasa de falsos negativos para la categoría ", category)
    fnr_1 = fn1/(tp1+fn1)
    #st.write(fnr_1)
    #Mujeres 
    #st.write("Tasa de falsos negativos para la categoría ", category2)
    fnr_2 = fn2/(tp2+fn2)
    #st.write(fnr_2)
    #False omission rate 
    #Hombres 
    #st.write("Tasa de falsas omisiones para la categoría ", category)
    fomr_1 = fn1/(tn1+fn1)
    #st.write(fomr_1)
    #Mujeres 
    #st.write("Tasa de falsas omisiones para la categoría ", category2)
    fomr_2 = fn2/(tn2+fn2)
    #st.write(fomr_2)
    #False discovery rate
    #Hombres
    #st.write("Tasa de falsos descubrimientos para la categoría ", category)
    fdr_1 = fp1/(tp1+fp1)
    #st.write(fdr_1)
    #Mujeres
    #st.write("Tasa de falsos descubrimientos para la categoría ", category2)
    fdr_2 = fp2/(tp2+fp2)
    #st.write(fdr_2)

    #Tabla métricas 
    #resumir datos
    metricas = {'Tasa de falsos positivos': [fpr_1, fpr_2], 
                'Tasa de falsos negativos':[fnr_1, fnr_2],
                'Tasa de falsa omisión':[fomr_1, fomr_2], 
                'Tasa de falso descubrimiento':[fdr_1, fdr_2]}

    #crear dataframe

    st.write(f'Métricas de sesgo por columna {label}')
    df_metricas = pd.DataFrame(metricas)
    df_metricas.index = unique_values
    st.write(df_metricas)

    st.write('---')

    #Significa que la proporción de falsos positivos entre hombres es aproximadamente un 10% mayor
    #que la proporción de falsos positivos entre mujeres.
    #Interpretando esto, puedes decir que, en relación con las mujeres, los hombres tienen una tasa 
    #ligeramente más alta de falsos positivos. Esto implica que en el contexto de tu análisis, 
    #hay una mayor proporción de casos donde la prueba o el modelo indica incorrectamente la presencia
    #de la condición o la variable de interés en hombres en comparación con mujeres.

    st.write(f"Tasa falsos positivos categoria {category2}/{category}",fpr_2/fpr_1)

    #significa que la proporción de falsos negativos entre hombres es aproximadamente el 90% de la proporción 
    #de falsos negativos entre mujeres.
    #Interpretando esto, puedes decir que, en relación con las mujeres, los hombres tienen una tasa ligeramente 
    #más baja de falsos negativos. Específicamente, en el contexto en el que estás trabajando, los hombres tienen 
    #menos casos donde la prueba o el modelo fallan en identificar correctamente la condición o la variable de 
    #interés en comparación con las mujeres.
    st.write(f"Tasa falsos negativos categoria {category2}/{category}",fnr_2/fnr_1)
    

    #significa que la proporción de falsas omisiones entre hombres es aproximadamente un 18% mayor que
    #la proporción de falsas omisiones entre mujeres.
    #Esto implica que en el contexto de tu análisis, hay una mayor proporción de casos donde 
    #la prueba o el modelo no indica la presencia de la condición o la variable de interés 
    #en hombres en comparación con mujeres, cuando en realidad debería haber sido detectada.

    st.write(f"Tasa de falsas omisiones categoria {category2}/{category}",fomr_2/fomr_1)
    

    #significa que la proporción de falsos descubrimientos entre hombres es aproximadamente un 4% 
    #menor que la proporción de falsos descubrimientos entre mujeres.
    #Esto implica que en el contexto de tu análisis, hay una menor proporción de casos donde se 
    #hace un descubrimiento erróneo (por ejemplo, una asociación entre variables) en hombres en 
    #comparación con mujeres.
    st.write(f"Tasa de falsos descubrimientos categoria {category2}/{category}",fdr_2/fdr_1)

    st.write('---')

    #Umbral de decision
    umbral = st.slider('Selecciona el umbral de decisión', min_value=0.0, max_value=1.0, value=0.1, step=0.1)

    #Comparación False Positive Rate
    fair_fpr = False

    if ((1-umbral)<=(fpr_2/fpr_1)<=(1/(1-umbral))):
        fair_fpr = True

    #Comparación False Negative Rate
    fair_fnr = False

    if ((1-umbral)<=(fnr_2/fnr_1)<=(1/(1-umbral))):
        fair_fnr = True

    #Comparación False Omission Rate
    fair_fomr = False

    if ((1-umbral)<=(fomr_2/fomr_1)<=(1/(1-umbral))):
        fair_fomr = True
    
    #Comparación False Discovery Rate
    fair_fdr = False

    if ((1-umbral)<=(fdr_2/fdr_1)<=(1/(1-umbral))):
        fair_fdr = True

    st.write('---')
    #Resumen disparidades 
    st.write('Resumen disparidades')
    #resumir datos
    disparidades = {'Tasa de falsos positivos': ['REF', fair_fpr], 
                    'Tasa de falsos negativos':['REF', fair_fnr],
                    'Tasa de falsa omisión':['REF', fair_fomr], 
                    'Tasa de falso descubrimiento':['REF', fair_fdr]}

    #crear dataframe
    df_disparidades = pd.DataFrame(disparidades)
    df_disparidades.index = [category, category2]
    st.write(df_disparidades)

    st.write('---')

    #Resumen comparación
    st.write('Resumen comparación') 
    #resumir datos
    comparacion = {'Tasa de falsos positivos': ['REF', fpr_2/fpr_1], 
                'Tasa de falsos negativos':['REF', fnr_2/fnr_1],
                'Tasa de falsa omisión':['REF', fomr_2/fomr_1], 
                'Tasa de falso descubrimiento':['REF', fdr_2/fdr_1]}

    #crear dataframe
    df_comparacion = pd.DataFrame(comparacion)
    df_comparacion.index = [category, category2]
    st.write(df_comparacion)

st.sidebar.title("Agradecimientos")
st.sidebar.image("_statics/ANID.png",width=100)
st.sidebar.write("Subdirección de Investigación Aplicada/Concurso IDeA I+D 2023 proyecto ID23I10357")
# Dividir la página en dos columnas

#st.sidebar.image("_statics/BidLab.png",width=100)

st.sidebar.subheader("Exención de responsabilidad")
st.sidebar.caption("""La herramienta de medición de sesgos y equidad estadística es un recurso diseñado para evaluar el desempeño de los modelos de ciencia de datos e IA en términos de equidad. La  herramienta pretende asistir en la identificación de sesgos potenciales, pero no asegura el correcto funcionamiento o eficacia de los sistemas evaluados con ella. La herramienta está diseñada como un soporte para quienes deben tomar decisiones respecto del desempeño de los modelos, con el fin de fomentar prácticas más justas y equitativas en la ciencia de datos.

La Universidad Adolfo Ibáñez (UAI) no es responsable de ningún tipo de daño directo, indirecto, incidental, especial o consecuente, ni de pérdidas de beneficios que puedan surgir directa o indirectamente de la aplicación de la herramienta, en el uso o la confianza en los resultados obtenidos a través de ésta. 

El empleo de las herramientas desarrolladas por la Universidad  no implica ni constituye un sello ni certificado de aprobación por parte de esta,  respecto al cumplimiento, legal,  ético o funcional de un algoritmo de inteligencia artificial. 

Aquellos interesados en ser considerados  como un caso de éxito mediante el uso de estas herramientas de IA responsable deben inscribirse en los pilotos a través del formulario https://algoritmospublicos.cl/quiero_participar. Es importante destacar que el uso de nuestras. """)

