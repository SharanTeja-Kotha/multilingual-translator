import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
from gtts import gTTS
from utils import ask_ai
from googletrans import Translator
import io


# -------------------------------
# 🔥 SPEECH TO TEXT (FINAL STABLE)
# -------------------------------
def speech_to_text(audio_bytes, file_type="webm"):
    recognizer = sr.Recognizer()

    try:
        # ✅ Safe audio decoding
        if file_type in ["opus", "ogg"]:
            audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format="ogg")
        elif file_type == "webm":
            audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format="webm")
        elif file_type in ["mp3", "wav", "m4a"]:
            audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format=file_type)
        else:
            audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes))

        # Convert to WAV
        wav_buffer = io.BytesIO()
        audio_segment = audio_segment.set_frame_rate(16000).set_channels(1)
        audio_segment.export(wav_buffer, format="wav")
        wav_buffer.seek(0)

        with sr.AudioFile(wav_buffer) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.3)
            audio_data = recognizer.record(source)

        # 🔥 NO language forcing (IMPORTANT)
        text = recognizer.recognize_google(audio_data)

        return text.strip()

    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        st.error("Speech service unavailable")
        return None
    except Exception as e:
        st.error(f"Audio error: {str(e)}")
        return None


# -------------------------------
# 🔥 TRANSLATION (FINAL FIXED)
# -------------------------------
def translate_voice_text(text: str, target_language: str, context: str) -> str:
    lang_map = {
        "English": "en",
        "Hindi": "hi",
        "Telugu": "te",
        "Spanish": "es",
        "French": "fr"
    }

    translator = Translator()

    try:
        detected = translator.detect(text)
        src_lang = detected.lang
        dest_lang = lang_map.get(target_language, "en")

        # 🔥 If same language → skip translation
        if src_lang == dest_lang:
            translated = text
        else:
            translated = translator.translate(
                text,
                src=src_lang,
                dest=dest_lang
            ).text

        # 🔥 Tone improvement (SAFE)
        if translated and len(translated.split()) > 2:
            try:
                prompt = f"""
Rewrite the sentence in a {context} tone.

STRICT RULES:
- Do NOT change meaning
- Do NOT change language
- Keep sentence same, only tone adjust

Sentence: {translated}
"""
                improved = ask_ai(prompt)

                if improved:
                    translated = improved.strip().replace('"', '')
            except:
                pass

        return translated

    except Exception:
        return text  # fallback


# -------------------------------
# 🎤 UI
# -------------------------------
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

    # 🎤 MIC
    if audio:
        st.success("Audio recorded successfully ✅")

        text = speech_to_text(audio["bytes"], "webm")

        if text:
            st.success(f"📝 Speech:\n\n{text}")

            translated = translate_voice_text(text, target_language, context)
            st.success(f"🌐 Translation:\n\n{translated}")

            try:
                tts = gTTS(
                    text=translated,
                    lang=lang_code_map.get(target_language, "en")
                )

                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    tts.save(fp.name)
                    st.audio(fp.name)
            except:
                st.warning("Audio playback not available")

        else:
            st.error("❌ Could not understand audio")

    # 📁 FILE UPLOAD
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

        text = speech_to_text(audio_bytes, file_type)

        if text:
            st.success(f"📝 Detected Text:\n\n{text}")

            translated = translate_voice_text(text, target_language, context)
            st.success(f"🌐 Translation:\n\n{translated}")

            try:
                tts = gTTS(
                    text=translated,
                    lang=lang_code_map.get(target_language, "en")
                )

                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    tts.save(fp.name)
                    st.audio(fp.name)
            except:
                st.warning("Audio playback not available")

        else:
            st.error("❌ Could not process audio")