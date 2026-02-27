import streamlit as st
import google.generativeai as genai
import time

# Configuración de la página
st.set_page_config(page_title="Reel Auditor Pro", page_icon="🎬")
st.title("🎬 Reel Auditor Pro")
st.markdown("Sube tu video y recibe una evaluación de nivel mundial.")

# Barra lateral para la API Key y configuración
with st.sidebar:
    api_key = st.text_input("Ingresa tu Gemini API Key:", type="password")
    st.info("Esta clave es privada y solo se usa para procesar tu video.")

# El "Cerebro": Definimos qué evaluar
def analizar_video(video_file, key):
    genai.configure(api_key=key)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")
    
    # Subir el video a la nube de Google temporalmente
    with st.spinner("Subiendo y analizando video... (esto puede tardar un minuto)"):
        video_data = genai.upload_file(path=video_file)
        
        # Esperar a que el video se procese
        while video_data.state.name == "PROCESSING":
            time.sleep(2)
            video_data = genai.get_file(video_data.name)

        prompt = """
        Actúa como un estratega de contenido viral de Instagram y TikTok. 
        Analiza este video y devuelve una tabla con calificaciones del 1 al 10 para:
        1. Estructura del reel
        2. Hook (Gancho inicial)
        3. CTA (Llamado a la acción)
        4. Ritmo de la edición
        5. Música de fondo
        6. Mensaje claro
        7. Subtítulos (Legibilidad y ritmo)
        
        Debajo de la tabla, proporciona sugerencias BREVES y accionables para mejorar cada punto. 
        Sé estricto, califica como si fueras un mentor de alto nivel.
        """
        
        response = model.generate_content([prompt, video_data])
        return response.text

# Interfaz de usuario
archivo_video = st.file_uploader("Sube tu Reel (.mp4 o .mov)", type=['mp4', 'mov'])

if archivo_video:
    st.video(archivo_video)
    # Guardar temporalmente para que Gemini lo pueda leer
    with open("temp_video.mp4", "wb") as f:
        f.write(archivo_video.read())

    if st.button("🚀 Evaluar mi Reel"):
        if not api_key:
            st.error("Por favor, ingresa tu API Key en la barra lateral.")
        else:
            try:
                resultado = analizar_video("temp_video.mp4", api_key)
                st.markdown("### 📊 Resultado de la Auditoría")
                st.write(resultado)
            except Exception as e:
                st.error(f"Hubo un error: {e}")

if st.button("🔄 Reiniciar / Nuevo Video"):
    st.rerun()
