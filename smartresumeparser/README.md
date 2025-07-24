Smart Resume Parser

The Smart Resume Parser is a web application that helps parse multiple resumes (PDF format) and automatically extracts important fields like:
- Name
- Email
- Phone number
- Skills
- Match Score based on a given job description

It also displays all uploaded resumes in a searchable, sortable table, and supports downloading the data as CSV.

---

 Features
✅ Parse and extract key details from resume PDFs  
✅ Show match score highlighting how well each resume fits the job description  
✅ Upload new resumes and view results instantly  
✅ Export results as CSV  
✅ Toggle dark mode  
✅ Pagination and search

---

 Tools & Libraries Used
- Python
- Flask (or Streamlit, whichever you used)
- pandas
- PyMuPDF (or pdfminer)
- Regex
- Bootstrap / HTML templates (for UI)

---

 How to Run
```bash
pip install -r requirements.txt
python app.py

---

Then open your browser and go to:
http://127.0.0.1:5000

