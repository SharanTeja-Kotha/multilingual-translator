# 🌐 Multilingual Translation System

A real-time multilingual translation system that supports voice, text, and image inputs.  
The system converts input into text, translates it into the desired language, and provides both text and audio output.

---

## 🚀 Features

- Voice-to-text translation using Speech Recognition  
- Text-to-text translation using Google Translate API  
- Image-to-text extraction using OCR (Tesseract)  
- Real-time multilingual translation  
- Text-to-Speech output using gTTS  
- User-friendly interface using Streamlit  

---

## 🧠 System Workflow

Input (Voice / Text / Image)
        ↓
Speech Recognition / OCR
        ↓
Text Processing
        ↓
Google Translate API (Neural Machine Translation)
        ↓
Translated Output
        ↓
gTTS (Audio Output)

---

## 🛠️ Technologies Used

Programming Language:
- Python

Frontend:
- Streamlit

Libraries:
- speech_recognition
- pydub
- googletrans
- gTTS
- pytesseract
- OpenCV (optional)

APIs & Models:
- Google Speech Recognition API  
- Google Translate API (Neural Machine Translation)  
- gTTS (Google Text-to-Speech)  
- Tesseract OCR  

---

## 📦 Installation

1. Clone the repository
git clone https://github.com/SharanTeja-Kotha/multilingual-translator.git
cd multilingual-translator

2. Create virtual environment
python -m venv venv
source venv/bin/activate   (Mac/Linux)
venv\Scripts\activate      (Windows)

3. Install dependencies
pip install -r requirements.txt

---

## ▶️ Run the Application

python -m streamlit run app.py

---

## 📊 Use Cases

- Travel assistance  
- Education  
- Multilingual communication  
- Accessibility support  

---

## ⚠️ Limitations

- Requires internet connection  
- Accuracy depends on input quality  
- Depends on external APIs  

---

## 🔮 Future Scope

- Offline translation support  
- Gesture-based input system  
- Mobile application development  
- Improved AI models  

---

## 👨‍💻 Contributors

- Sharan Teja – Development & Implementation  
- Team Members – Documentation & Presentation  

---

## 📄 License

This project is developed for academic purposes.
