import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
from gtts import gTTS
from utils import translate_text

def voice_translation_ui():
    st.subheader("🎤 Voice Translator (Final Stable Version)")

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

    st.info("Click mic → Speak clearly → Stop")

    audio = mic_recorder(
        start_prompt="🎙️ Start Recording",
        stop_prompt="⏹️ Stop Recording"
    )

    # ================= MIC =================
    if audio:
        st.success("Audio recorded successfully ✅")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as f:
            f.write(audio["bytes"])
            webm_path = f.name

        wav_path = webm_path.replace(".webm", ".wav")

        # ✅ NATURAL AUDIO (NO DISTORTION)
        sound = AudioSegment.from_file(webm_path, format="webm")
        sound.export(wav_path, format="wav")

        recognizer = sr.Recognizer()

        try:
            with sr.AudioFile(wav_path) as source:
                audio_data = recognizer.record(source)

            # ✅ AUTO DETECT (ORIGINAL WORKING BEHAVIOR)
            text = recognizer.recognize_google(audio_data)

            st.success(f"📝 Speech:\n\n{text}")

            translated = translate_text(text, target_language, context)
            st.success(f"🌐 Translation:\n\n{translated}")

            tts = gTTS(text=translated, lang=lang_code_map.get(target_language, "en"))

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                st.audio(fp.name)

        except sr.UnknownValueError:
            st.error("❌ Could not understand audio.")
        except sr.RequestError:
            st.error("❌ Speech service unavailable.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

    # ================= FILE =================
    st.divider()
    st.subheader("📁 Upload Audio File")

    uploaded_file = st.file_uploader(
        "Upload audio",
        type=["mp3", "wav", "m4a", "webm", "ogg", "opus"]
    )

    if uploaded_file:
        st.success("Audio uploaded successfully ✅")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".tmp") as temp_audio:
            temp_audio.write(uploaded_file.read())
            input_path = temp_audio.name

        wav_path = input_path + ".wav"
        file_type = uploaded_file.name.split(".")[-1].lower()

        try:
            if file_type == "opus":
                sound = AudioSegment.from_file(input_path, format="ogg")
            else:
                sound = AudioSegment.from_file(input_path)

            # ✅ NATURAL AUDIO
            sound.export(wav_path, format="wav")

        except Exception as e:
            st.error(f"Audio conversion failed: {str(e)}")
            return

        st.audio(wav_path)

        recognizer = sr.Recognizer()

        try:
            with sr.AudioFile(wav_path) as source:
                audio_data = recognizer.record(source)

            text = recognizer.recognize_google(audio_data)

            st.success(f"📝 Detected Text:\n\n{text}")

            translated = translate_text(text, target_language, context)
            st.success(f"🌐 Translation:\n\n{translated}")

            tts = gTTS(text=translated, lang=lang_code_map.get(target_language, "en"))

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                st.audio(fp.name)

        except Exception as e:
            st.error(f"Error: {str(e)}")