import streamlit as st
from gtts import gTTS
import fitz  # PyMuPDF
import pandas as pd
from datetime import datetime
import os
import re

st.set_page_config(page_title="PDF to Audiobook Converter", page_icon="static/favicon.png", layout="centered")
HISTORY_CSV = "conversion_history.csv"
AUDIO_FOLDER = "generated_audios"
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# --- CSS ---
st.markdown("""
<style>
html, body, .block-container {
    background: linear-gradient(135deg, #2e2e2e, #4b4b4b);
    color: #eee;
}
.big-card {
    background: linear-gradient(90deg, #667eea, #764ba2);
    padding: 16px;
    border-radius: 16px;
    margin-bottom: 14px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.5);
    text-align: center;
}
.history-card {
    background: rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 8px 14px;
    margin-bottom: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.4);
}
.stButton>button {
    background: linear-gradient(90deg, #4ca1af, #2c3e50);
    color: white;
    border: none;
    padding: 7px 14px;
    border-radius: 6px;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #357f89, #22313f);
}
h1, h2, h3, h4, h5, h6 { color: #f8f8f8; margin-bottom: 0; }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="big-card">
  <h1>📚🔊 PDF to Audiobook Converter</h1>
  <p>Convert your PDFs into clear audio instantly</p>
</div>
""", unsafe_allow_html=True)

# --- Tabs ---
tab1, tab2 = st.tabs(["🎧 Convert", "ℹ️ About"])

with tab1:
    uploaded_file = st.file_uploader("📄 Upload PDF", type=["pdf"])

    # Many supported languages
    languages = {
        "en":"English 🇬🇧", "ta":"Tamil 🇮🇳", "ml":"Malayalam 🇮🇳", "hi":"Hindi 🇮🇳",
        "fr":"French 🇫🇷", "es":"Spanish 🇪🇸", "de":"German 🇩🇪", "it":"Italian 🇮🇹",
        "ja":"Japanese 🇯🇵", "ko":"Korean 🇰🇷", "ru":"Russian 🇷🇺", "ar":"Arabic 🇸🇦",
        "zh-cn":"Chinese 🇨🇳", "pt":"Portuguese 🇵🇹"
    }
    language = st.selectbox("🌐 Language", list(languages.keys()), format_func=lambda x: languages[x])

    slow_voice = st.checkbox("🐢 Slow voice")

    if uploaded_file:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            raw_text = " ".join(page.get_text() for page in doc)
        cleaned_text = re.sub(r'\s+', ' ', raw_text).strip()

        if not cleaned_text:
            st.warning("❗ No text found in PDF.")
        else:
            st.success("✅ Text extracted and cleaned!")

            if st.button("🔊 Convert to Audio"):
                filename_base = datetime.now().strftime('%Y%m%d%H%M%S') + "_" + uploaded_file.name.replace(' ','_')
                mp3_path = os.path.join(AUDIO_FOLDER, filename_base + ".mp3")
                with st.spinner("⏳ Generating audio..."):
                    gTTS(text=cleaned_text, lang=language, slow=slow_voice).save(mp3_path)
                file_size = os.path.getsize(mp3_path)//1024
                st.success(f"✅ Done! ({file_size} KB)")
                audio_bytes = open(mp3_path, 'rb').read()
                st.audio(audio_bytes, format="audio/mp3")
                st.download_button("⬇️ Download MP3", audio_bytes, file_name=os.path.basename(mp3_path), mime="audio/mpeg")

                new_row = pd.DataFrame([{
                    "filename": uploaded_file.name,
                    "language": languages[language],
                    "slow_voice": "Yes" if slow_voice else "No",
                    "date": datetime.now().strftime("%d %b %Y, %I:%M %p"),
                    "size_kb": f"{file_size} KB",
                    "audio_file": mp3_path
                }])
                if os.path.exists(HISTORY_CSV):
                    history = pd.read_csv(HISTORY_CSV)
                    history = pd.concat([history, new_row], ignore_index=True)
                else:
                    history = new_row
                history.to_csv(HISTORY_CSV, index=False)

    # --- History ---
    if os.path.exists(HISTORY_CSV):
        st.markdown("### 📜 Conversion History")
        df = pd.read_csv(HISTORY_CSV)
        for _, row in df.iterrows():
            st.markdown(f"""
            <div class="history-card">
                <strong>📄 {row['filename']}</strong><br>
                🗣️ {row['language']} | 🐢 Slow: {row['slow_voice']} | 💾 {row['size_kb']}<br>
                🕒 {row['date']}<br>
                <a href="{row['audio_file']}" download>⬇️ Download again</a>
            </div>
            """, unsafe_allow_html=True)

        if st.button("🗑️ Clear history"):
            os.remove(HISTORY_CSV)
            st.rerun()

with tab2:
    st.markdown("""
    ### ℹ️ About
    Convert PDF files into MP3 audiobooks using Google Text-to-Speech.
    - Supports many languages: English, Tamil, Malayalam, Hindi, French, Spanish, German, Italian, Japanese, Korean, Russian, Arabic, Chinese, Portuguese
    - Slow voice option
    - Keeps conversion history
    - Elegant gradient & modern design
    """)

st.markdown('<div style="text-align:center; color: #aaa; margin-top:12px;">Smart PDF to Audiobook Converter © 2025</div>', unsafe_allow_html=True)
