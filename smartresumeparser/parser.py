import re
import os
import pandas as pd
import spacy
import csv

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# ---------- Extract Resume Details ----------

# Extract Name
def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            return ent.text
    return "Not Found"

# Extract Email
def extract_email(text):
    email = re.findall(r'\S+@\S+', text)
    return email[0] if email else "Not Found"

# Extract Phone Number
def extract_phone(text):
    phone = re.findall(r'\+?\d[\d\s\-]{8,}\d', text)
    return phone[0] if phone else "Not Found"

# Extract Skills from predefined list
def extract_skills(text):
    skills = ["Python", "Java", "SQL", "HTML", "CSS", "Flask"]
    found = [skill for skill in skills if skill.lower() in text.lower()]
    return found

# ---------- Parse Resume ----------
def parse_resume(text):
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text)
    }

# ---------- Save to CSV ----------
def save_to_csv(data, filename='data/resumes.csv'):
    # Create "data" directory if not exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Define CSV columns
    fieldnames = [
        "name", "email", "phone", "skills",
        "uploaded_at", "job_desc", "match_score"
    ]

    file_exists = os.path.isfile(filename)

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write header if file doesn't exist or is empty
        if not file_exists or os.stat(filename).st_size == 0:
            writer.writeheader()

        # Fill missing keys with empty string
        for field in fieldnames:
            if field not in data:
                data[field] = ""

        writer.writerow(data)