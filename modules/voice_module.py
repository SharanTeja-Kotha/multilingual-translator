import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
from gtts import gTTS
from utils import translate_text
import io

def speech_to_text(audio_bytes, file_type="webm", target_language="English"):
    recognizer = sr.Recognizer()

    # 🔥 LANGUAGE MAP (CRITICAL FIX)
    speech_lang_map = {
        "English": "en-IN",
        "Hindi": "hi-IN",
        "Telugu": "te-IN",
        "Spanish": "es-ES",
        "French": "fr-FR"
    }

    try:
        # ✅ CORRECT AUDIO DECODING
        if file_type == "opus":
            audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format="ogg")
        elif file_type == "webm":
            audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format="webm")
        else:
            audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes))

        # convert to wav (NO distortion)
        wav_buffer = io.BytesIO()
        audio_segment.export(wav_buffer, format="wav")
        wav_buffer.seek(0)

        with sr.AudioFile(wav_buffer) as source:
            audio_data = recognizer.record(source)

        # 🔥 FINAL FIX: ALWAYS USE LANGUAGE HINT
        text = recognizer.recognize_google(
            audio_data,
            language=speech_lang_map.get(target_language, "en-IN")
        )

        return text

    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        st.error("Speech service unavailable")
        return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None


def voice_translation_ui():
    st.subheader("🎤 Voice Translator (Final Version)")

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

    # =====================================================
    # 🎤 MIC RECORDING
    # =====================================================
    if audio:
        st.success("Audio recorded successfully ✅")

        text = speech_to_text(
            audio["bytes"],
            file_type="webm",
            target_language=target_language
        )

        if text:
            st.success(f"📝 Speech:\n\n{text}")

            translated = translate_text(text, target_language, context)
            st.success(f"🌐 Translation:\n\n{translated}")

            tts = gTTS(
                text=translated,
                lang=lang_code_map.get(target_language, "en")
            )

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                st.audio(fp.name)
        else:
            st.error("❌ Could not understand audio")

    # =====================================================
    # 📁 FILE UPLOAD
    # =====================================================
    st.divider()
    st.subheader("📁 Upload Audio File")

    uploaded_file = st.file_uploader(
        "Upload audio (WhatsApp / Voice Note)",
        type=["mp3", "wav", "m4a", "webm", "ogg", "opus"]
    )

    if uploaded_file:
        st.success("Audio uploaded successfully ✅")
        st.audio(uploaded_file)

        file_type = uploaded_file.name.split(".")[-1].lower()
        audio_bytes = uploaded_file.read()

        text = speech_to_text(
            audio_bytes,
            file_type=file_type,
            target_language=target_language
        )

        if text:
            st.success(f"📝 Detected Text:\n\n{text}")

            translated = translate_text(text, target_language, context)
            st.success(f"🌐 Translation:\n\n{translated}")

            tts = gTTS(
                text=translated,
                lang=lang_code_map.get(target_language, "en")
            )

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                st.audio(fp.name)
        else:
            st.error("❌ Could not process audio")