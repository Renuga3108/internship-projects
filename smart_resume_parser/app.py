from flask import Flask, render_template, request, redirect, send_file
from parser import parse_resume, save_to_csv
import fitz  # PyMuPDF
from datetime import datetime
import pandas as pd
import os

app = Flask(__name__)

# --- Calculate match score based on common words ---
def match_score(resume_text, job_desc):
    resume_words = set(resume_text.lower().split())
    job_words = set(job_desc.lower().split())
    matched = resume_words.intersection(job_words)
    return round(len(matched) / len(job_words) * 100, 2) if job_words else 0.0

# --- Extract text from uploaded PDF ---
def extract_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# --- Home: upload resume & analyze ---
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        resume_file = request.files['resume']
        text = extract_text_from_pdf(resume_file)

        parsed_data = parse_resume(text)

        name = request.form.get("name")
        parsed_data["name"] = name

        job_desc = request.form.get("job_desc")
        score = match_score(text, job_desc) if job_desc else 0.0

        # Color based on score
        if score >= 70:
            color = '#4caf50'  # green
        elif score >= 40:
            color = 'orange'
        else:
            color = 'red'

        # Format date nicely: e.g., "17 Jul 2025, 11:42 AM"
        parsed_data["uploaded_at"] = datetime.now().strftime("%d %b %Y, %I:%M %p")
        parsed_data["job_desc"] = job_desc
        parsed_data["match_score"] = score

        # Save to CSV
        save_to_csv(parsed_data)

        return render_template('result.html', data=parsed_data, score=score, color=color)

    return render_template('index.html')

# --- View all uploaded resumes ---
@app.route('/view_all')
def view_all():
    csv_path = 'data/resumes.csv'
    if not os.path.exists(csv_path) or os.stat(csv_path).st_size == 0:
        return render_template('view_all.html', resumes=[], message="No resumes found.")

    try:
        df = pd.read_csv(csv_path)
    except pd.errors.EmptyDataError:
        return render_template('view_all.html', resumes=[], message="CSV file is empty.")

    # Format skills list nicely if stored as list string
    if 'skills' in df.columns:
        df['skills'] = df['skills'].apply(
            lambda x: ', '.join(eval(x)) if isinstance(x, str) and x.startswith('[') else x
        )

    resumes = df.to_dict(orient='records')
    return render_template('view_all.html', resumes=resumes)

# --- Clear all resume data ---
@app.route('/clear', methods=['POST'])
def clear_resumes():
    with open('data/resumes.csv', 'w') as f:
        f.truncate()
    return redirect('/view_all')

# --- Download CSV ---
@app.route('/download_csv')
def download_csv():
    return send_file('data/resumes.csv', as_attachment=True)

# --- Run the app ---
if __name__ == '__main__':
    app.run(debug=True)
