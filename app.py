import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(page_title="Reel Auditor Pro", page_icon="🎬")
st.title("🎬 Reel Auditor Pro")

with st.sidebar:
    api_key = st.text_input("Ingresa tu Gemini API Key:", type="password")
    st.info("Configuración de nivel mundial lista.")

def analizar_video(video_path, key):
    genai.configure(api_key=key)
    
    # --- MEJORA: Buscar el modelo correcto automáticamente ---
    try:
        # Intentamos usar el nombre estándar más compatible
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    except:
        # Si falla, buscamos el primero que diga 'flash' en tu lista
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        flash_model = next((m for m in available_models if "flash" in m), "models/gemini-1.5-flash")
        model = genai.GenerativeModel(model_name=flash_model)
    # ---------------------------------------------------------

    with st.spinner("Subiendo video a la central de inteligencia..."):
        video_data = genai.upload_file(path=video_path)
        
        while video_data.state.name == "PROCESSING":
            time.sleep(3)
            video_data = genai.get_file(video_data.name)

        prompt = """
        Eres un experto mundial en Reels y TikTok. Analiza este video.
        Entrega una TABLA con notas del 1 al 10 para:
        1. Estructura, 2. Hook, 3. CTA, 4. Ritmo, 5. Música, 6. Mensaje, 7. Subtítulos.
        Luego, da un consejo clave para mejorar cada punto.
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
                st.markdown("### 📊 Auditoría Completada")
                st.write(resultado)
            except Exception as e:
                st.error(f"Error técnico: {e}")

if st.button("🔄 Nuevo Video"):
    st.rerun()
