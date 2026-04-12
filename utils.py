import os
from dotenv import load_dotenv
import groq
from googletrans import Translator

# Load environment variables
load_dotenv()

# Initialize clients
groq.api_key = os.getenv("GROQ_API_KEY")
translator = Translator()


# -------------------------------
# 🔹 Common Groq Function
# -------------------------------
def ask_ai(prompt: str) -> str:
    try:
        response = groq.ChatCompletion.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You improve sentences without changing meaning. "
                        "Return ONLY the final sentence. No explanation."
                    )
                },
                {"role": "user", "content": prompt}
            ]
        )

        return response["choices"][0]["message"]["content"].strip()

    except Exception:
        return ""


# -------------------------------
# 🔹 Translation Function (Optimized)
# -------------------------------
def translate_text(text: str, target_language: str, context: str) -> str:
    if not text.strip():
        return "Please enter some text."

    lang_map = {
        "English": "en",
        "Hindi": "hi",
        "Telugu": "te",
        "Spanish": "es",
        "French": "fr"
    }

    try:
        # Step 1: Detect source language (for future use / accuracy)
        detected_lang = translator.detect(text).lang

        # Step 2: Google Translate (main accurate translation)
        translated = translator.translate(
            text,
            dest=lang_map.get(target_language, "en")
        ).text

        # Step 3: Skip AI for very short inputs (better accuracy)
        if len(text.split()) <= 2:
            return translated

        # Step 4: Tone improvement using Groq
        prompt = f"""
Rewrite the sentence in a {context} tone.

STRICT RULES:
- Do NOT change meaning
- Do NOT add new words
- Do NOT translate again
- Keep same language
- Only slightly adjust tone

Sentence: {translated}
"""

        improved = ask_ai(prompt)

        # Step 5: Clean output
        return improved.strip().replace('"', '') if improved else translated

    except Exception:
        return translated if 'translated' in locals() else "Translation error"


# -------------------------------
# 🔹 Language Detection (Google)
# -------------------------------
def detect_language(text: str) -> str:
    if not text.strip():
        return "Unknown"

    try:
        detected = translator.detect(text)

        lang_map = {
            "en": "English",
            "hi": "Hindi",
            "te": "Telugu",
            "es": "Spanish",
            "fr": "French"
        }

        return lang_map.get(detected.lang, detected.lang)

    except Exception:
        return "Unknown"