import pandas as pd
from PIL import Image
import streamlit as st
from textblob import TextBlob
from googletrans import Translator

# Configuración de página con título, ícono y diseño centrado
st.set_page_config(
    page_title="Análisis de Sentimiento",
    page_icon="🎭",
    layout="centered"
)

# Estilo visual general
st.title("🎭 Análisis de Sentimiento")
st.caption("Analiza la carga emocional y objetividad de tus frases en tiempo real.")

# Carga de imagen con manejo de excepción por si no existe la ruta
try:
    image = Image.open('emoticones.jpg')
    st.image(image, use_container_width=True)
except FileNotFoundError:
    pass

translator = Translator()

# Barra lateral informativa estructurada
with st.sidebar:
    st.header("📊 Guía de Métricas")
    st.markdown("""
    **Polaridad:** Indica si el texto es positivo, negativo o neutral.
    * **-1.0 a -0.1:** Negativo 😔
    * **-0.1 a 0.1:** Neutral 😐
    * **0.1 a 1.0:** Positivo 😊
    
    ---
    
    **Subjetividad:** Mide si el texto es factual o una opinión.
    * **0.0:** Completamente objetivo (hechos).
    * **1.0:** Completamente subjetivo (opiniones).
    """)

st.divider()

# Sección principal para entrada de texto
st.subheader("Ingresa tu texto")
text = st.text_area(
    label="Escribe la frase que deseas analizar:",
    placeholder="Ejemplo: ¡El servicio al cliente fue increíble y la comida estuvo deliciosa!",
    height=100
)

# Procesamiento y presentación de resultados
if text:
    try:
        # Traducción y análisis
        translation = translator.translate(text, src="es", dest="en")
        trans_text = translation.text
        blob = TextBlob(trans_text)
        
        polarity = round(blob.sentiment.polarity, 2)
        subjectivity = round(blob.sentiment.subjectivity, 2)

        st.subheader("Resultados del Análisis")
        
        # Tarjetas visuales de métricas
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Polaridad", value=polarity)
        with col2:
            st.metric(label="Subjetividad", value=f"{int(subjectivity * 100)}%")

        # Clasificación con cajas de color
        if polarity > 0.05:
            st.success(f"**Resultado:** Sentimiento Positivo 😊 (Traducción: *\"{trans_text}\"*)")
        elif polarity < -0.05:
            st.error(f"**Resultado:** Sentimiento Negativo 😔 (Traducción: *\"{trans_text}\"*)")
        else:
            st.info(f"**Resultado:** Sentimiento Neutral 😐 (Traducción: *\"{trans_text}\"*)")

    except Exception as e:
        st.warning("Ocurrió un error al traducir o analizar el texto. Por favor, intenta de nuevo.")
