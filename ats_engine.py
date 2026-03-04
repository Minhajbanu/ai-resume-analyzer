import re
COMMON_SKILLS = [
    "python", "java", "c++", "machine learning",
    "deep learning", "nlp", "sql", "data analysis",
    "tensorflow", "pytorch", "fastapi",
    "flask", "streamlit", "docker"
]

def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in COMMON_SKILLS:
        if skill in text:
            found_skills.append(skill)

    return found_skills
def extract_keywords(text):
    words = re.findall(r'\b\w+\b', text.lower())
    return set(words)

def keyword_match_score(resume_text, job_description):
    resume_words = extract_keywords(resume_text)
    job_words = extract_keywords(job_description)

    matched = resume_words.intersection(job_words)

    if len(job_words) == 0:
        return 0

    score = len(matched) / len(job_words)
    return score * 100