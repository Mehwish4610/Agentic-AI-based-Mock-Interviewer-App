import fitz  # PyMuPDF
import re
from utils.openai_helper import ask_gpt

def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def analyze_resume(text):
    # Normalize text
    text_lower = text.lower().replace('\n', ' ').replace('\r', ' ').strip()

    # Skills extraction
    skills_keywords = [
        "python", "machine learning", "deep learning", "data analysis", "communication",
        "leadership", "project management", "java", "sql", "react", "node.js", "aws",
        "docker", "html", "css", "kubernetes", "gcp", "fastapi", "langchain",
        "javascript", "c++", "linux", "tensorflow", "pandas"
    ]

    found_skills = []
    for skill in skills_keywords:
        if skill in text_lower:
            found_skills.append(skill.capitalize())

    # Experience extraction
    experience_years = 0
    exp_match = re.findall(r"(\d+)\s*(years|yrs)\s*(of)?\s*(experience|exp)", text_lower)
    if exp_match:
        numbers = [int(num[0]) for num in exp_match]
        experience_years = max(numbers) if numbers else 0

    # Education extraction
    # Clean text more deeply
    text_clean = text.lower().replace('\n', ' ').replace('\r', ' ').replace('.', '').replace('-', ' ').strip()

    bachelors_keywords = [
        "btech", "bachelor of technology", "bachelor of engineering",
        "bachelor of science", "be", "bsc"
    ]
    masters_keywords = [
        "mtech", "master of technology", "master of engineering",
        "msc", "mba", "master of science", "master of business administration"
    ]

    education = []

    for degree in bachelors_keywords:
        if degree in text_clean:
            education.append("Bachelor's")
            break

    for degree in masters_keywords:
        if degree in text_clean:
            education.append("Master's")
            break

    return {
        "skills": found_skills,
        "experience_years": experience_years,
        "education": education
    }

def agentic_resume_feedback(resume_text, job_role):
    """Analyze resume deeply and suggest missing skills, improvements."""
    prompt = f"""
You are a career expert AI.
A candidate has uploaded their resume.

Resume Content:
{resume_text}

They are applying for the role of {job_role}.

Analyze their resume and:
- List 5 important missing skills or certifications (if any) for this role.
- Suggest 3 specific improvements to make the resume stronger.
- Be honest but constructive.

Give your answer structured as:
- Missing Skills:
- Resume Improvement Suggestions:
"""
    feedback = ask_gpt(prompt)
    return feedback
