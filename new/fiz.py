# import spacy
# import fitz  # PyMuPDF
# from thefuzz import process  # Fuzzy string matching

# def extract_text_from_pdf(pdf_path):
#     text = ""
#     doc = fitz.open(pdf_path)
#     for page in doc:
#         text += page.get_text("text") + "\n"
#     return text

# pdf_path = "C:/Users/ACER/Downloads/utils/Shahzad's cv (1).pdf" # Replace with your file path
# resume_text = extract_text_from_pdf(pdf_path)
# print(resume_text)  # View extracted text

# # Load English NLP model
# nlp = spacy.load("en_core_web_sm")

# # List of common skills
# skills_list = [
#     "Flutter", "Dart", "API integration", "Firebase", "Node.js",
#     "Flutter Bloc", "Express.js", "Provider", "Flutter Riverpod",
#     "GetX", "Video calling SDK", "Responsive design", "Communication skills"
# ]

# # Function to extract text from PDF
# def extract_text_from_pdf(pdf_path):
#     text = ""
#     doc = fitz.open(pdf_path)
#     for page in doc:
#         text += page.get_text("text") + "\n"
#     return text

# # Function to extract skills using fuzzy matching
# def extract_skills(text, skills_list, threshold=80):  # 80% match similarity
#     extracted_skills = set()
#     words = text.split()  # Split text into words

#     for word in words:
#         match, score = process.extractOne(word, skills_list)  # Find best match
#         if score >= threshold:  # If match score is high
#             extracted_skills.add(match)

#     return list(extracted_skills)

# # Run the skill extraction
# pdf_path = "C:/Users/ACER/Downloads/utils/Shahzad's cv (1).pdf"  # Replace with your file path
# resume_text = extract_text_from_pdf(pdf_path)
# skills_found = extract_skills(resume_text, skills_list)

# print("Extracted Skills:", skills_found)
import spacy
import random
from spacy.training.example import Example

# ✅ Load Pretrained spaCy Model
nlp = spacy.load("en_core_web_sm")

# ✅ Auto-Calculate Offsets for TRAIN_DATA
def get_entity_offsets(text, entities):
    entity_offsets = []
    for entity in entities:
        start = text.find(entity)
        if start != -1:
            entity_offsets.append((start, start + len(entity), "SKILL"))
    return entity_offsets

TRAIN_DATA = [
    ("I have experience in Flutter, Dart, and Firebase.", get_entity_offsets("I have experience in Flutter, Dart, and Firebase.", ["Flutter", "Dart", "Firebase"])),
    ("Worked with Node.js and Express.js.", get_entity_offsets("Worked with Node.js and Express.js.", ["Node.js", "Express.js"])),
    ("I am proficient in Python, SQL, and machine learning.", get_entity_offsets("I am proficient in Python, SQL, and machine learning.", ["Python", "SQL", "machine learning"])),
    ("My skills include Java, React, and cloud computing.", get_entity_offsets("My skills include Java, React, and cloud computing.", ["Java", "React", "cloud computing"])),
]

TRAIN_DATA = [(text, {"entities": entities}) for text, entities in TRAIN_DATA]

# ✅ Verify Entity Alignment
from spacy.training import offsets_to_biluo_tags
for text, annotations in TRAIN_DATA:
    doc = nlp.make_doc(text)
    biluo_tags = offsets_to_biluo_tags(doc, annotations["entities"])
    print(f"Text: {text}\nBILUO Tags: {biluo_tags}\n")

# ✅ Train NER Model
ner = nlp.get_pipe("ner")
for _, annotations in TRAIN_DATA:
    for ent in annotations["entities"]:
        ner.add_label(ent[2])

other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
with nlp.disable_pipes(*other_pipes):
    optimizer = nlp.initialize()
    for epoch in range(500):  # Train for 500 epochs
        print(f"Epoch {epoch + 1}...")
        random.shuffle(TRAIN_DATA)
        for text, annotations in TRAIN_DATA:
            example = Example.from_dict(nlp.make_doc(text), annotations)
            nlp.update([example], drop=0.3, losses={})

# ✅ Save Model
nlp.to_disk("skills_ner_model")
print("Training complete! Model saved as 'skills_ner_model'.")

# ✅ Load & Test Model
nlp_skill = spacy.load("skills_ner_model")

def extract_skills_spacy(text):
    doc = nlp_skill(text)
    skills = [ent.text for ent in doc.ents if ent.label_ == "SKILL"]
    return list(set(skills))

# Test with Resume
resume_text = "I have worked with Java,flutter, SQL, cloud computing, and machine learning."
skills_found = extract_skills_spacy(resume_text)
print("Extracted Skills:", skills_found)
