import streamlit as st
from utils import translate_text, detect_language


def text_translation_ui():
    st.subheader("📝 Text Translation")

    # -------------------------------
    # 🔹 Language + Context Selection
    # -------------------------------
    col1, col2 = st.columns(2)

    with col1:
        target_language = st.selectbox(
            "🌍 Target Language",
            ["English", "Hindi", "Telugu", "Spanish", "French"]
        )

    with col2:
        context = st.selectbox(
            "🎯 Tone / Context",
            ["Casual", "Professional", "Academic", "Travel"]
        )

    st.divider()

    # -------------------------------
    # 🔹 Chat Input
    # -------------------------------
    user_input = st.chat_input("Type your message...")

    # -------------------------------
    # 🔹 Session State
    # -------------------------------
    if "chat" not in st.session_state:
        st.session_state.chat = []

    # -------------------------------
    # 🔹 Process Input
    # -------------------------------
    if user_input:
        detected_language = detect_language(user_input)
        translation = translate_text(user_input, target_language, context)

        # Store only latest interaction (clean UI)
        st.session_state.chat = [{
            "user": user_input,
            "detected_language": detected_language,
            "translation": translation
        }]

    # -------------------------------
    # 🔹 Display Chat
    # -------------------------------
    if st.session_state.chat:
        entry = st.session_state.chat[-1]

        with st.chat_message("user"):
            st.write(f"{entry['user']} ({entry['detected_language']})")

        with st.chat_message("assistant"):
            st.write(entry["translation"])