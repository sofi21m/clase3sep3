import streamlit as st
from textblob import TextBlob
from googletrans import Translator
from gtts import gTTS
import os
import time

# 1. CONFIGURACIÓN DE PÁGINA (Mejora visual instantánea)
st.set_page_config(
    page_title="Sentiméntmetro AI",
    page_icon="🎙️",
    layout="centered"
)

# 2. ESTILOS CSS PERSONALIZADOS (Para darle un toque "bonito")
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .big-font {
        font-size:30px !important;
        font-weight: bold;
        color: #1E3A8A;
    }
    .result-box {
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Instanciar herramientas
translator = Translator()

# --- FUNCIONES CLAVE ---
def generar_audio_es(texto, filename="vozimprovisada.mp3"):
    """Genera un archivo de audio en español y devuelve el nombre"""
    try:
        # Eliminamos el archivo anterior si existe para no acumular basura
        if os.path.exists(filename):
            os.remove(filename)
        
        tts = gTTS(text=texto, lang='es', slow=False)
        tts.save(filename)
        return filename
    except Exception as e:
        st.error(f"Error generando audio: {e}")
        return None

def obtener_imagen_sentimiento(polaridad):
    """Devuelve una URL de imagen diferente según el ánimo"""
    if polaridad > 0.1:
        # Imagen Feliz (Un paisaje soleado o emoji 3D feliz)
        return "https://img.freepik.com/vector-premium/emoticon-3d-lindo-sonriendo_1142-1262.jpg"
    elif polaridad < -0.1:
        # Imagen Triste (Nubes de lluvia o emoji 3D triste)
        return "https://img.freepik.com/vector-premium/emoticon-3d-lindo-llorando_1142-1256.jpg"
    else:
        # Imagen Neutral (Un robot pensante o emoji 3D neutral)
        return "https://img.freepik.com/vector-premium/emoticon-3d-lindo-pensando_1142-1264.jpg"

# --- INTERFAZ PRINCIPAL ---

st.markdown('<p class="big-font">🎙️ Sentiméntmetro AI con Voz</p>', unsafe_allow_html=True)
st.caption("Escribe tu frase en español. La IA la analizará, cambiará la imagen y te dirá el resultado en voz alta.")

# Entrada de texto más limpia
text_input = st.text_area("¿Qué tienes en mente?", placeholder="Ej: Hoy es un día maravilloso para aprender algo nuevo...")

st.divider()

if text_input:
    with st.spinner('🤖 Nuestra IA está leyendo y pensando...'):
        time.sleep(1) # Simulación de pensamiento para dar mejor UX

        # 1. Traducción y Análisis
        translation = translator.translate(text_input, src="es", dest="en")
        trans_text = translation.text
        blob = TextBlob(trans_text)
        
        polarity = round(blob.sentiment.polarity, 2)
        subjectivity = round(blob.sentiment.subjectivity, 2)

        # 2. Lógica de Resultado e Imagen Dinámica
        if polarity > 0.1:
            estado = "Positivo"
            emoji = "😊"
            color_box = "#D1FAE5" # Verde claro
            mensaje_voz = f"He detectado un sentimiento positivo en tu frase. ¡Qué alegría!"
        elif polarity < -0.1:
            estado = "Negativo"
            emoji = "😔"
            color_box = "#FEE2E2" # Rojo claro
            mensaje_voz = f"Tu frase parece tener un tono negativo. Espero que todo mejore."
        else:
            estado = "Neutral"
            emoji = "😐"
            color_box = "#FEF3C7" # Amarillo claro
            mensaje_voz = f"El análisis muestra un sentimiento neutral, bastante equilibrado."

        # --- MOSTRAR RESULTADOS REFORMADOS ---
        
        col_img, col_info = st.columns([1, 2])

        with col_img:
            # CAMBIO DE IMAGEN DINÁMICO
            url_dinamica = obtener_imagen_sentimiento(polarity)
            st.image(url_dinamica, caption=f"Estado: {estado}", use_container_width=True)

        with col_info:
            st.subheader("Análisis Detallado")
            
            # Métricas bonitas
            c1, c2 = st.columns(2)
            c1.metric("Polaridad", polarity, help="Rango: -1 (Muy Triste) a 1 (Muy Feliz)")
            c2.metric("Subjetividad", f"{int(subjectivity*100)}%", help="Rango: 0% (Hechos) a 100% (Opinión)")

            # Caja de resultado con color
            st.markdown(f"""
                <div class="result-box" style="background-color: {color_box}; border: 1px solid {color_box};">
                    <h3 style="color: black; margin: 0;">Sentimiento {estado} {emoji}</h3>
                    <p style="color: black;">La IA ha interpretado tu frase como {estado}.</p>
                </div>
            """, unsafe_allow_html=True)

        # --- SECCIÓN DE VOZ ---
        st.write("---")
        st.subheader("🔊 Escucha el Análisis")
        
        archivo_audio = generar_audio_es(mensaje_voz)
        
        if archivo_audio:
            # Reproductor de audio automático
            st.audio(archivo_audio, format="audio/mp3", start_time=0)
            st.success("¡Dale al Play para escuchar la voz de la IA!")

else:
    # Estado inicial: Imagen por defecto
    st.image("https://img.freepik.com/vector-premium/ilustracion-vectorial-concepto-analisis-sentimientos_675567-3316.jpg", use_container_width=True, caption="Esperando tu frase...")
    st.info("Escribe arriba y presiona Ctrl+Enter para empezar.")
