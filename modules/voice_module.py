import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
from gtts import gTTS
from googletrans import Translator
from utils import ask_ai
import io


# -------------------------------
# SPEECH TO TEXT (STABLE)
# -------------------------------
def speech_to_text(audio_bytes, file_type="webm"):
    recognizer = sr.Recognizer()

    try:
        if file_type in ["opus", "ogg"]:
            audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format="ogg")
        elif file_type == "webm":
            audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format="webm")
        elif file_type in ["mp3", "wav", "m4a"]:
            audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format=file_type)
        else:
            audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes))

        # Normalize audio (IMPORTANT FIX)
        audio_segment = audio_segment.set_frame_rate(16000).set_channels(1)

        wav_buffer = io.BytesIO()
        audio_segment.export(wav_buffer, format="wav")
        wav_buffer.seek(0)

        with sr.AudioFile(wav_buffer) as source:
            recognizer.energy_threshold = 300
            recognizer.pause_threshold = 0.8
            audio_data = recognizer.record(source, duration=10)

        # AUTO DETECT LANGUAGE (NO FORCE)
        text = recognizer.recognize_google(audio_data)

        return text.strip()

    except:
        return None


# -------------------------------
# TRANSLATION (FORCED CORRECT)
# -------------------------------
def translate_voice_text(text, target_language, context):
    translator = Translator()

    lang_map = {
        "English": "en",
        "Hindi": "hi",
        "Telugu": "te",
        "Spanish": "es",
        "French": "fr"
    }

    try:
        detected = translator.detect(text)
        src = detected.lang
        dest = lang_map.get(target_language, "en")

        if src == dest:
            translated = text
        else:
            translated = translator.translate(text, src=src, dest=dest).text

        # Tone adjust (safe)
        if translated and len(translated.split()) > 2:
            try:
                prompt = f"""
Rewrite the sentence in a {context} tone.
Do not change meaning or language.

Sentence: {translated}
"""
                improved = ask_ai(prompt)
                if improved:
                    translated = improved.strip().replace('"', '')
            except:
                pass

        return translated

    except:
        return text


# -------------------------------
# UI
# -------------------------------
def voice_translation_ui():
    st.subheader("🎤 Voice Translator")

    target_language = st.selectbox(
        "Target Language",
        ["English", "Hindi", "Telugu", "Spanish", "French"]
    )

    context = st.selectbox(
        "Tone",
        ["Formal", "Casual"]
    )

    lang_code_map = {
        "English": "en",
        "Hindi": "hi",
        "Telugu": "te",
        "Spanish": "es",
        "French": "fr"
    }

    st.info("Click mic → Speak → Stop")

    audio = mic_recorder(
        start_prompt="🎙️ Start Recording",
        stop_prompt="⏹️ Stop Recording"
    )

    # ---------------- MIC ----------------
    if audio:
        st.success("Audio recorded successfully ✅")

        text = speech_to_text(audio["bytes"], "webm")

        if text:
            st.success(f"📝 Speech:\n\n{text}")

            translated = translate_voice_text(text, target_language, context)
            st.success(f"🌐 Translation:\n\n{translated}")

            try:
                tts = gTTS(text=translated, lang=lang_code_map[target_language])
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                    tts.save(f.name)
                    st.audio(f.name)
            except:
                st.warning("Audio output failed")

        else:
            st.error("❌ Could not understand audio")

    # ---------------- FILE ----------------
    st.divider()
    st.subheader("📁 Upload Audio File")

    uploaded_file = st.file_uploader(
        "Upload audio",
        type=["mp3", "wav", "m4a", "webm", "ogg", "opus"]
    )

    if uploaded_file:
        st.audio(uploaded_file)

        file_type = uploaded_file.name.split(".")[-1].lower()
        audio_bytes = uploaded_file.read()

        text = speech_to_text(audio_bytes, file_type)

        if text:
            st.success(f"📝 Detected Text:\n\n{text}")

            translated = translate_voice_text(text, target_language, context)
            st.success(f"🌐 Translation:\n\n{translated}")

            try:
                tts = gTTS(text=translated, lang=lang_code_map[target_language])
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                    tts.save(f.name)
                    st.audio(f.name)
            except:
                st.warning("Audio output failed")

        else:
            st.error("❌ Could not process audio")