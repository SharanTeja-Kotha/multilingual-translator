import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
from utils import translate_text
from streamlit_mic_recorder import mic_recorder
import io

# ---------------------------------------------------------------------------
# Phonetic correction map — Hindi / common misrecognitions
# Keys are what Google STT returns; values are the intended words.
# All matching is case-insensitive; output preserves the corrected casing.
# ---------------------------------------------------------------------------
_PHONETIC_CORRECTIONS: dict[str, str] = {
    # Relationship / greetings
    "by": "bhai",
    "bye": "bhai",
    "bi": "bhai",
    "buy": "bhai",
    "by bhai": "bhai",
    "namaste": "namaste",
    "namasthe": "namaste",
    "namaskar": "namaskar",
    # Common Hindi words misheard in English
    "acha": "achha",
    "acha ": "achha",
    "accha": "achha",
    "thik": "theek",
    "theek hay": "theek hai",
    "theek he": "theek hai",
    "theek hain": "theek hai",
    "kal": "kal",
    "abhi": "abhi",
    "matlab": "matlab",
    "yaar": "yaar",
    "yar": "yaar",
    "kya": "kya",
    "kia": "kya",
    "nahi": "nahi",
    "nai": "nahi",
    "nay": "nahi",
    "nehi": "nahi",
    "haan": "haan",
    "han": "haan",
    "hun": "haan",
    "aur": "aur",
    "or": "aur",
    "our": "aur",
    "woh": "woh",
    "wo": "woh",
    "vo": "woh",
    "main": "main",
    "mein": "main",
    "men": "main",
    "tum": "tum",
    "hum": "hum",
    "ham": "hum",
    "apna": "apna",
    "apne": "apne",
    "bohot": "bahut",
    "bahot": "bahut",
    "bohat": "bahut",
    "shukriya": "shukriya",
    "shukria": "shukriya",
    "sukria": "shukriya",
    "dhanyavaad": "dhanyavaad",
    "dhanywad": "dhanyavaad",
    "pyaar": "pyaar",
    "piyar": "pyaar",
    "pyar": "pyaar",
    "ghar": "ghar",
    "gar": "ghar",
    "ghur": "ghar",
    "paani": "paani",
    "pani": "paani",
    "khana": "khana",
    "kaana": "khana",
    "khaana": "khana",
    "baat": "baat",
    "bat": "baat",
    "baath": "baat",
    "samajh": "samajh",
    "samaj": "samajh",
    "zindagi": "zindagi",
    "jindagi": "zindagi",
    "jindegi": "zindagi",
    "dost": "dost",
    "doast": "dost",
    "mujhe": "mujhe",
    "muje": "mujhe",
    "mooje": "mujhe",
    "tumhe": "tumhe",
    "tumhare": "tumhare",
    "tumhari": "tumhari",
    "mera": "mera",
    "meri": "meri",
    "mere": "mere",
    "tera": "tera",
    "teri": "teri",
    "tere": "tere",
    "hamara": "hamara",
    "hamari": "hamari",
    "aaj": "aaj",
    "aj": "aaj",
    "kal ko": "kal",
    "parso": "parso",
    "abhi nahi": "abhi nahi",
    "thoda": "thoda",
    "thora": "thoda",
    "jaldi": "jaldi",
    "jaldee": "jaldi",
    "suno": "suno",
    "soono": "suno",
    "dekho": "dekho",
    "daikho": "dekho",
    "chalo": "chalo",
    "chalou": "chalo",
    "ruko": "ruko",
    "rooko": "ruko",
    "aao": "aao",
    "aow": "aao",
    "jao": "jao",
    "jaow": "jao",
    "bolo": "bolo",
    "bolow": "bolo",
    "sach": "sach",
    "such": "sach",
    "jhooth": "jhooth",
    "jhut": "jhooth",
    "mushkil": "mushkil",
    "mushkeel": "mushkil",
    "asaan": "aasaan",
    "aasan": "aasaan",
    "kaam": "kaam",
    "kam": "kaam",
    "paisa": "paisa",
    "pesa": "paisa",
    "paisaa": "paisa",
    "waqt": "waqt",
    "wakt": "waqt",
    "time nahi": "waqt nahi",
    "zyada": "zyada",
    "jyada": "zyada",
    "jayada": "zyada",
    "kam se kam": "kam se kam",
    "bilkul": "bilkul",
    "bilkool": "bilkul",
    "zaroor": "zaroor",
    "zarur": "zaroor",
    "shayad": "shayad",
    "shaayad": "shayad",
    "pata nahi": "pata nahi",
    "pta nahi": "pata nahi",
    "pata hai": "pata hai",
    "pta hai": "pata hai",
}


def _apply_phonetic_corrections(text: str) -> str:
    """
    Apply word-level and phrase-level phonetic corrections to STT output.

    Strategy:
    1. Try full-phrase match first (handles multi-word misrecognitions).
    2. Fall back to token-by-token correction for single words.
    Matching is case-insensitive; the corrected form is returned as-is.
    """
    if not text or not text.strip():
        return text

    normalised = text.strip()

    # Full-phrase match (longest phrases first to avoid partial clobbers)
    lower = normalised.lower()
    for wrong, right in sorted(_PHONETIC_CORRECTIONS.items(), key=lambda x: -len(x[0])):
        if lower == wrong.strip():
            return right

    # Token-level correction — only replaces tokens that are exact matches
    tokens = normalised.split()
    corrected_tokens = []
    for token in tokens:
        lookup = token.lower().strip(".,!?;:'\"")
        punctuation = token[len(lookup):]          # preserve trailing punctuation
        corrected_tokens.append(
            _PHONETIC_CORRECTIONS.get(lookup, token.lower()) + punctuation
        )
    return " ".join(corrected_tokens)


def _speech_to_text(audio_bytes: bytes) -> str | None:
    """Convert raw webm/wav audio bytes to corrected transcribed text."""
    recognizer = sr.Recognizer()
    try:
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes))
        wav_buffer = io.BytesIO()
        audio_segment.export(wav_buffer, format="wav")
        wav_buffer.seek(0)

        with sr.AudioFile(wav_buffer) as source:
            audio_data = recognizer.record(source)

        raw_text = recognizer.recognize_google(audio_data)
        return _apply_phonetic_corrections(raw_text)

    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        st.error(f"Speech recognition service error: {e}")
        return None
    except Exception as e:
        st.error(f"Audio processing error: {e}")
        return None


def voice_translation_ui():
    st.subheader("🎤 Voice Translation")

    from googletrans import LANGUAGES
    language_options = sorted(name.capitalize() for name in LANGUAGES.values())

    col1, col2 = st.columns(2)
    with col1:
        target_language = st.selectbox(
            "🌍 Target Language",
            language_options,
            index=language_options.index("English") if "English" in language_options else 0,
            key="voice_target_lang",
        )
    with col2:
        context = st.selectbox(
            "🎯 Tone / Context",
            ["Casual", "Professional", "Academic", "Travel"],
            key="voice_context",
        )

    st.divider()

    # ── Input mode tabs ────────────────────────────────────────────────────────
    tab_mic, tab_file = st.tabs(["🎙️ Microphone", "📁 Upload Audio"])

    # ── Mic tab ────────────────────────────────────────────────────────────────
    with tab_mic:
        st.caption("Press record, speak clearly, then stop.")
        audio = mic_recorder(
            start_prompt="⏺ Start Recording",
            stop_prompt="⏹ Stop Recording",
            key="mic_recorder",
        )

        if audio and audio.get("bytes"):
            with st.spinner("Transcribing…"):
                recognised_text = _speech_to_text(audio["bytes"])

            if recognised_text:
                st.success(f"🗣️ Recognised: **{recognised_text}**")
                with st.spinner("Translating…"):
                    translation = translate_text(recognised_text, target_language, context)
                with st.chat_message("assistant"):
                    st.write(translation)
            else:
                st.warning("Could not recognise speech. Please speak clearly and try again.")

    # ── File upload tab ────────────────────────────────────────────────────────
    with tab_file:
        uploaded_file = st.file_uploader(
            "Upload an audio file",
            type=["wav", "mp3", "webm", "ogg", "m4a"],
            key="voice_upload",
        )

        if uploaded_file is not None:
            st.audio(uploaded_file, format=uploaded_file.type)
            if st.button("🔄 Transcribe & Translate", key="voice_translate_btn"):
                with st.spinner("Transcribing…"):
                    recognised_text = _speech_to_text(uploaded_file.read())

                if recognised_text:
                    st.success(f"🗣️ Recognised: **{recognised_text}**")
                    with st.spinner("Translating…"):
                        translation = translate_text(recognised_text, target_language, context)
                    with st.chat_message("assistant"):
                        st.write(translation)
                else:
                    st.warning("Could not recognise speech in the uploaded file.")