import spacy
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")

# Lista e skillsesh që do kërkojmë - mund ta zgjerosh sipas nevojës
SKILLS_LIST = [
    "Python", "Java", "JavaScript", "SQL", "FastAPI", "Flask", "Django",
    "React", "Node.js", "Git", "Docker", "Kubernetes", "AWS", "GCP", "Azure",
    "PostgreSQL", "MySQL", "MongoDB", "REST API", "Machine Learning", "NLP",
    "TensorFlow", "PyTorch", "scikit-learn", "pandas", "Agile", "Scrum",
    "Linux", "CI/CD", "HTML", "CSS", "TypeScript", "C++", "C#"
]

matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
patterns = [nlp.make_doc(skill) for skill in SKILLS_LIST]
matcher.add("SKILLS", patterns)


def extract_skills(text):
    """Gjen dhe kthen listën e skillsesh të identifikuara në një tekst."""
    doc = nlp(text)
    matches = matcher(doc)
    found_skills = set()
    for match_id, start, end in matches:
        found_skills.add(doc[start:end].text)
    return sorted(found_skills)


def find_missing_skills(resume_text, job_description):
    """Krahason skills e job description me ato të CV-së, kthen ato qe mungojne."""
    resume_skills = set(s.lower() for s in extract_skills(resume_text))
    job_skills = set(s.lower() for s in extract_skills(job_description))

    missing = job_skills - resume_skills
    matched = job_skills & resume_skills

    return sorted(missing), sorted(matched)


# Test
if __name__ == "__main__":
    sample_resume = "I have experience with Python, FastAPI, and SQL databases."
    sample_job = "We need Python, FastAPI, Docker, and AWS experience."

    missing, matched = find_missing_skills(sample_resume, sample_job)
    print(f"Matched skills: {matched}")
    print(f"Missing skills: {missing}")