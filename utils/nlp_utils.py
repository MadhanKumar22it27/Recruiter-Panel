# This file handles NLP tasks like skill extraction and scoring.
import spacy
import re
from models.dataset_skills.skills_db import SKILLS_DB
# Load pre-trained NER model
nlp = spacy.load("en_core_web_sm")

def extract_skills(text):
    """
    Extracts skills from the given text by performing case-insensitive matching with word boundaries
    to prevent substring mismatches.
    """
    text = text.lower()  # Normalize text to lowercase

    # Remove special characters (except spaces)
    clean_text = re.sub(r'[^a-z0-9\s]', '', text)

    # Extract skills using word boundaries to prevent false positives
    skills_found = [skill for skill in SKILLS_DB if re.search(rf'\b{re.escape(skill.lower())}\b', clean_text)]

    print(f"Extracted skills: {skills_found}")  # Debug output
    return skills_found

def calculate_score(resume_skills, job_skills):
    """
    Calculates skill match score based on job skills only.
    """
    if not job_skills:
        return 0  # Avoid division by zero
    
    matched_skills = set(resume_skills).intersection(set(job_skills))
    match_count = len(matched_skills)
    

    score = (match_count / len(job_skills)) * 100
    
    print(f"Matching Skills: {matched_skills}")
    print(f"Resume Skills: {resume_skills}, Job Skills: {job_skills}")
    print(f"Calculated Score: {round(score, 2)}%")
    
    return round(score, 2)

