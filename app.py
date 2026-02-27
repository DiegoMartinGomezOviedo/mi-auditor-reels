import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(page_title="Reel Auditor Pro", page_icon="🎬")
st.title("🎬 Reel Auditor Pro")

with st.sidebar:
    api_key = st.text_input("Ingresa tu Gemini API Key:", type="password")
    st.info("Tip: Si copiaste la clave de la foto, asegúrate de que no falte ningún caracter.")

def analizar_video(video_path, key):
    # FORZAMOS LA VERSIÓN ESTABLE Y COMUNICACIÓN SIMPLE
    genai.configure(api_key=key, transport='rest') 
    
    # Probamos con el nombre más compatible de todos
    model = genai.GenerativeModel('gemini-1.5-flash')

    with st.spinner("Analizando video... Esto puede tardar 30-60 segundos."):
        video_data = genai.upload_file(path=video_path)
        
        while video_data.state.name == "PROCESSING":
            time.sleep(2)
            video_data = genai.get_file(video_data.name)

        prompt = """
        Actúa como un experto en marketing de contenidos. Analiza este video y devuelve:
        1. Una tabla con calificaciones (1-10) para: Estructura, Hook, CTA, Ritmo, Música, Mensaje y Subtítulos.
        2. Un párrafo con sugerencias clave para mejorar el rendimiento del reel.
        """
        
        # Usamos un bloque try por si el modelo falla, intentar el siguiente
        try:
            response = model.generate_content([video_data, prompt])
            return response.text
        except:
            # Si falla el anterior, intentamos con la versión Pro (que también suele estar libre)
            model_pro = genai.GenerativeModel('gemini-1.5-pro')
            response = model_pro.generate_content([video_data, prompt])
            return response.text

archivo_video = st.file_uploader("Sube tu Reel", type=['mp4', 'mov'])

if archivo_video:
    st.video(archivo_video)
    if st.button("🚀 Iniciar Evaluación"):
        if not api_key:
            st.error("Por favor, ingresa la API Key a la izquierda.")
        else:
            try:
                with open("temp_video.mp4", "wb") as f:
                    f.write(archivo_video.getbuffer())
                
                resultado = analizar_video("temp_video.mp4", api_key)
                st.success("¡Análisis Terminado!")
                st.markdown(resultado)
            except Exception as e:
                st.error(f"Error: {e}")
