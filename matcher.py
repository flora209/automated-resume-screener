from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Ngarkojmë modelin - kjo ndodh vetëm një herë, jo çdo herë që thërrasim funksionin
model = SentenceTransformer('all-MiniLM-L6-v2')


def get_embedding(text):
    """Kthen tekstin në një vektor numrash që përfaqëson kuptimin e tij."""
    embedding = model.encode(text)
    return embedding


def calculate_match_score(resume_text, job_description):
    """Krahason CV-në me job description dhe kthen një score 0-100%."""
    # Kthejmë të dy tekstet në vektorë
    resume_embedding = get_embedding(resume_text).reshape(1, -1)
    job_embedding = get_embedding(job_description).reshape(1, -1)

    # Llogarisim ngjashmërinë mes tyre
    similarity = cosine_similarity(resume_embedding, job_embedding)[0][0]

    # E kthejmë në përqindje (0-100)
    score = round(similarity * 100, 2)
    return score


# Test
if __name__ == "__main__":
    sample_resume = """
    Software Engineer with 3 years of experience in Python development.
    Led a team of 4 developers on multiple backend projects.
    Strong background in REST APIs, databases, and cloud deployment.
    """

    sample_job = """
    We are looking for a Backend Developer with team leadership experience.
    Must be proficient in Python and have knowledge of API design and databases.
    """

    match_score = calculate_match_score(sample_resume, sample_job)
    print(f"Match Score: {match_score}%")
    