import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(page_title="Reel Auditor Pro", page_icon="🎬")
st.title("🎬 Reel Auditor Pro")

with st.sidebar:
    api_key = st.text_input("Ingresa tu Gemini API Key:", type="password")
    st.divider()
    st.caption("Versión: Gemini 3 Flash Engine")

def analizar_video(video_path, key):
    genai.configure(api_key=key)
    
    # Intentamos con la versión más moderna (Gemini 3)
    try:
        model = genai.GenerativeModel('gemini-3-flash')
    except:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

    with st.spinner("Procesando video con IA de última generación..."):
        # Subir el archivo
        video_file = genai.upload_file(path=video_path)
        
        # Esperar procesamiento
        while video_file.state.name == "PROCESSING":
            time.sleep(2)
            video_file = genai.get_file(video_file.name)

        prompt = """
        Actúa como un estratega de contenido viral. Analiza este video y genera:
        1. Una tabla comparativa con notas del 1 al 10 para: Estructura, Hook, CTA, Ritmo, Música, Mensaje y Subtítulos.
        2. Un párrafo de 'Sugerencias Pro' para mejorar la retención y el impacto.
        """
        
        response = model.generate_content([video_file, prompt])
        return response.text

archivo_video = st.file_uploader("Sube tu Reel", type=['mp4', 'mov'])

if archivo_video:
    st.video(archivo_video)
    
    if st.button("🚀 Iniciar Auditoría"):
        if not api_key:
            st.error("Falta la API Key en la barra lateral.")
        else:
            try:
                # Guardado temporal
                with open("temp_reel.mp4", "wb") as f:
                    f.write(archivo_video.getbuffer())
                
                resultado = analizar_video("temp_reel.mp4", api_key)
                st.success("¡Auditoría terminada!")
                st.markdown(resultado)
            except Exception as e:
                st.error(f"Error de conexión: {e}")
                st.info("Asegúrate de que tu API Key sea válida para modelos Gemini 3.")

if st.button("🔄 Limpiar y Nuevo Video"):
    st.rerun()
