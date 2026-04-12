import streamlit as st
import pytesseract
from PIL import Image
from utils import translate_text
import re
import numpy as np
import cv2

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

        try:
            # -------------------------------
            # 🔥 PREPROCESS IMAGE (KEY FIX)
            # -------------------------------
            img = np.array(image)

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # 🔥 VERY IMPORTANT: Resize (fixes cloud accuracy issue)
            gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

            # Noise reduction
            gray = cv2.bilateralFilter(gray, 9, 75, 75)

            # Threshold
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

            # -------------------------------
            # 🔹 OCR (IMPROVED CONFIG)
            # -------------------------------
            extracted_text = pytesseract.image_to_string(
                thresh,
                lang="eng",
                config="--oem 3 --psm 6"
            )

            # -------------------------------
            # 🔥 CLEAN TEXT
            # -------------------------------
            extracted_text = extracted_text.strip().replace("\x0c", "")
            extracted_text = re.sub(r'\s+', ' ', extracted_text)

            if not extracted_text:
                st.warning("No text detected ❌")
                return

            st.subheader("📝 Extracted Text")
            st.code(extracted_text)

            # -------------------------------
            # 🔹 TRANSLATE
            # -------------------------------
            translated = translate_text(extracted_text, target_language, context)

            st.subheader("🌐 Translation")
            st.success(translated)

        except Exception as e:
            st.error(f"Error: {str(e)}")