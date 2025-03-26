#This file handles file uploads and text extraction from PDFs and DOCX files.

import os
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
import docx
import pdfplumber

def handle_file_upload(files):
    """
    Handles multiple resume file uploads and a single job description file.
    """
    resumes = files.getlist('resumes')  # Handle multiple resumes
    job_description_file = files['job_description']

    # Save job description
    job_description_path = os.path.join('uploads/job_descriptions', secure_filename(job_description_file.filename))
    job_description_file.save(job_description_path)

    # Save resumes
    resume_paths = []
    for resume in resumes:
        if resume and allowed_file(resume.filename):
            resume_path = os.path.join('uploads/resumes', secure_filename(resume.filename))
            resume.save(resume_path)
            resume_paths.append(resume_path)

    return resume_paths, job_description_path

def allowed_file(filename):
    """
    Checks if the file has an allowed extension.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'docx', 'txt'}
import re

def clean_text(text):
    """
    Cleans extracted text by removing extra spaces, special characters, and fixing format issues.
    """
    text = text.replace("\n", " ")  # Remove newlines
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special characters (optional)
    return text

def extract_text_from_file(file_path):
    """
    Extracts text from a file (PDF or DOCX).
    """
    if file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        text = extract_text_from_docx(file_path)
    elif file_path.endswith('.txt'):
        with open(file_path, 'r') as file:
            text = file.read()
    else:
        raise ValueError("Unsupported file format")

    text = clean_text(text)  # Clean the extracted text
    print(f"Extracted text from {file_path}:\n{text}\n")  # Debug statement
    return text

def extract_text_from_pdf(pdf_path):
    """
    Extract text from PDF using pdfplumber (better accuracy).
    """
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()


def extract_text_from_docx(docx_path):
    """
    Extracts text from a DOCX file.
    """
    doc = docx.Document(docx_path)
    text = '\n'.join([para.text for para in doc.paragraphs])
    return text