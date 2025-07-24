# 📚 PDF to Audiobook Converter

A simple Streamlit web app to convert PDF files into audiobooks (MP3).  
Created as an internship project to make reading easier and more accessible.

---

## ✨ Features
- Upload PDF files and extract text automatically
- Convert text to speech in multiple languages (e.g., English, French)
- Choose slow or normal voice speed
- Download generated MP3 audio files
- See conversion history with file name, language, speed, date, and size
- Simple, user-friendly interface

---

## 📂 Project Structure
```
pdf_to_audiobook_project/
├── app.py                    # Main Streamlit application
├── conversion_history.csv    # Stores details of conversions
├── generated_audios/         # Folder where generated MP3 files are saved
├── static/                   # Contains static files (e.g., logo)
├── requirements.txt          # Python libraries needed
└── .gitignore                # Files/folders to ignore
```

---

## ⚙️ How to run locally

> Make sure Python is installed on your system.

1. Open command prompt or terminal.  
2. Change to your project folder:
```bash
cd path\to\pdf_to_audiobook_project
```

3. *(Optional)* Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate          # On Windows
# or
source venv/bin/activate      # On Linux/Mac
```

4. Install the required libraries:
```bash
pip install -r requirements.txt
```

5. Run the Streamlit app:
```bash
streamlit run app.py
```

Then open your browser and go to: [http://localhost:8501](http://localhost:8501)

---

## ✅ How to use
1. Upload a PDF file.
2. Choose language and voice speed.
3. Click **Convert to Audio**.
4. Download or play your MP3 file.
5. See details in **Conversion History**.

---

## 📦 Requirements
```
streamlit
gTTS
PyMuPDF
pandas
```

---

## ✏️ Author
**Renuga Devi M**  
Internship Project · 2025

---

## 🙏 Special thanks
- Streamlit – for easy web apps
- gTTS – Google Text-to-Speech
- PyMuPDF – PDF text extraction
- Python open-source community
