from flask import Flask, request, render_template, send_file
import os
from utils.file_utils import handle_file_upload, extract_text_from_file
from utils.nlp_utils import extract_skills, calculate_score
from utils.pdf_utils import generate_pdf

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['REPORTS_FOLDER'] = 'reports'
  
@app.route('/') 
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    resumes, job_description_path = handle_file_upload(request.files)

    # Extract text from job description
    job_description_text = extract_text_from_file(job_description_path)
    job_skills = extract_skills(job_description_text)
    print(f"Job Description Skills: {job_skills}")  

    # Evaluate resumes
    candidates = []
    for resume_path in resumes:
        resume_text = extract_text_from_file(resume_path)
        resume_skills = extract_skills(resume_text)
        score = calculate_score(resume_skills, job_skills)
        candidates.append({
            'name': os.path.basename(resume_path),
            'skills': resume_skills,
            'score': score
        })

    # Generate PDF report
    report_path = os.path.join(app.config['REPORTS_FOLDER'], 'candidate_report.pdf')
    generate_pdf(candidates, report_path)

    return send_file(report_path, as_attachment=True)

if __name__ == '__main__':
    # Create uploads folder structure if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'] + '/resumes', exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'] + '/job_descriptions', exist_ok=True)
    app.run(debug=True)