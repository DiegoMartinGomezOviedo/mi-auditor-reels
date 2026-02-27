import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(page_title="Reel Auditor Pro", page_icon="🎬")
st.title("🎬 Reel Auditor Pro")

with st.sidebar:
    api_key = st.text_input("Ingresa tu Gemini API Key:", type="password")
    if st.button("🔍 Ver modelos disponibles (Diagnóstico)"):
        if api_key:
            genai.configure(api_key=api_key)
            models = [m.name for m in genai.list_models()]
            st.write(models)
        else:
            st.error("Pon tu API Key primero")

def analizar_video(video_path, key):
    genai.configure(api_key=key)
    
    # Probamos con el nombre técnico completo
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

    with st.spinner("Subiendo video..."):
        video_data = genai.upload_file(path=video_path)
        
        while video_data.state.name == "PROCESSING":
            time.sleep(3)
            video_data = genai.get_file(video_data.name)

        prompt = """
        Eres un experto mundial en Reels. Analiza este video.
        1. Dame una tabla de notas (1-10) para: Estructura, Hook, CTA, Ritmo, Música, Mensaje y Subtítulos.
        2. Dame una sugerencia de mejora para cada punto.
        """
        
        response = model.generate_content([prompt, video_data])
        return response.text

archivo_video = st.file_uploader("Sube tu Reel", type=['mp4', 'mov'])

if archivo_video:
    st.video(archivo_video)
    with open("temp_video.mp4", "wb") as f:
        f.write(archivo_video.read())

    if st.button("🚀 Evaluar mi Reel"):
        if not api_key:
            st.error("Falta la API Key.")
        else:
            try:
                resultado = analizar_video("temp_video.mp4", api_key)
                st.markdown("### 📊 Auditoría")
                st.write(resultado)
            except Exception as e:
                st.error(f"Error: {e}")
