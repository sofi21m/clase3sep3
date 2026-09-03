import os
import time
from PIL import Image
import streamlit as st
from textblob import TextBlob
from gtts import gTTS
from deep_translator import GoogleTranslator

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Sentiméntmetro AI",
    page_icon="🎭",
    layout="centered"
)

# Estilos visuales
st.markdown("""
<style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
        color: #1E3A8A;
    }
    .result-box {
        padding: 20px;
        border-radius: 10px;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# --- FUNCIONES ---
def generar_audio_es(texto, filename="voz_resultado.mp3"):
    """Genera audio en español con gTTS"""
    try:
        if os.path.exists(filename):
            os.remove(filename)
        tts = gTTS(text=texto, lang='es', slow=False)
        tts.save(filename)
        return filename
    except Exception as e:
        return None

def obtener_imagen_sentimiento(polaridad):
    """Devuelve una imagen distinta según el sentimiento"""
    if polaridad > 0.05:
        return "https://img.freepik.com/vector-premium/emoticon-3d-lindo-sonriendo_1142-1262.jpg"
    elif polaridad < -0.05:
        return "https://img.freepik.com/vector-premium/emoticon-3d-lindo-llorando_1142-1256.jpg"
    else:
        return "https://img.freepik.com/vector-premium/emoticon-3d-lindo-pensando_1142-1264.jpg"

# --- INTERFAZ ---
st.markdown('<p class="big-font">🎭 Análisis de Sentimiento con Voz</p>', unsafe_allow_html=True)
st.caption("Escribe tu frase en español. Se traducirá internamente para analizar el sentimiento, cambiará la imagen y te hablará.")

text_input = st.text_area("Escribe la frase que deseas analizar:", placeholder="Ej: ¡Me encanta este lugar, la atención fue maravillosa!")

if text_input:
    with st.spinner('Traduciendo y analizando...'):
        try:
            # TRADUCCIÓN GARANTIZADA: Español -> Inglés usando deep-translator
            translated_text = GoogleTranslator(source='es', target='en').translate(text_input)
            
            # Análisis de sentimiento en inglés (donde TextBlob funciona bien)
            blob = TextBlob(translated_text)
            polarity = round(blob.sentiment.polarity, 2)
            subjectivity = round(blob.sentiment.subjectivity, 2)

            # Clasificación de sentimiento
            if polarity > 0.05:
                estado = "Positivo"
                emoji = "😊"
                color_box = "#D1FAE5"
                mensaje_voz = f"El sentimiento detectado es positivo. {text_input}"
            elif polarity < -0.05:
                estado = "Negativo"
                emoji = "😔"
                color_box = "#FEE2E2"
                mensaje_voz = f"El sentimiento detectado es negativo. {text_input}"
            else:
                estado = "Neutral"
                emoji = "😐"
                color_box = "#FEF3C7"
                mensaje_voz = f"El sentimiento detectado es neutral. {text_input}"

            st.divider()

            # Mapeo visual y de métricas
            col_img, col_info = st.columns([1, 2])

            with col_img:
                st.image(obtener_imagen_sentimiento(polarity), caption=f"Estado: {estado}", use_container_width=True)

            with col_info:
                st.subheader("Resultados")
                
                c1, c2 = st.columns(2)
                c1.metric("Polaridad", polarity)
                c2.metric("Subjetividad", f"{int(subjectivity*100)}%")

                st.markdown(f"""
                    <div class="result-box" style="background-color: {color_box};">
                        <h3 style="color: black; margin: 0;">Sentimiento {estado} {emoji}</h3>
                        <p style="color: black; margin-top: 5px;"><b>Traducción interna:</b> "<i>{translated_text}</i>"</p>
                    </div>
                """, unsafe_allow_html=True)

            # SECCIÓN DE AUDIO
            st.subheader("🔊 Escuchar Resultado")
            archivo_audio = generar_audio_es(mensaje_voz)
            
            if archivo_audio:
                st.audio(archivo_audio, format="audio/mp3")

        except Exception as e:
            st.error(f"Ocurrió un error con la traducción o el análisis: {e}")

else:
    st.info("Escribe una frase arriba para comenzar el análisis.")
