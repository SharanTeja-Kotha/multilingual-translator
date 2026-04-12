import streamlit as st
import pytesseract
from PIL import Image
from utils import translate_text
import re  # ✅ NEW

def image_translation_ui():
    st.subheader("🖼️ Image Translator (OCR + AI)")

    COMMON_LANGUAGES = ["English", "Hindi", "Telugu", "Spanish", "French"]

    col1, col2 = st.columns(2)

    with col1:
        target_language = st.selectbox("🌍 Target Language", COMMON_LANGUAGES)

    with col2:
        context = st.selectbox("🎯 Tone", ["Formal", "Casual"])

    st.divider()

    uploaded_image = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])
    camera_image = st.camera_input("Take a picture")

    image = None

    if uploaded_image:
        image = Image.open(uploaded_image).convert("RGB")
    elif camera_image:
        image = Image.open(camera_image).convert("RGB")

    if image:
        st.image(image, use_container_width=True)

        # 🔹 OCR
        extracted_text = pytesseract.image_to_string(image)

        # 🔥 CLEAN TEXT (THIS FIXES YOUR ERROR)
        extracted_text = extracted_text.strip().replace("\x0c", "")
        extracted_text = re.sub(r'\s+', ' ', extracted_text)

        if extracted_text:
            st.success(f"📝 Extracted:\n\n{extracted_text}")

            # 🔹 Translation (NOW WILL WORK)
            translated = translate_text(extracted_text, target_language, context)

            st.success(f"🌐 Translation:\n\n{translated}")
        else:
            st.warning("No text detected")