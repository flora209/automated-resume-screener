import sqlite3
from datetime import datetime

DB_NAME = "history.db"


def init_db():
    """Krijon tabelën nëse s'ekziston ende - thirret njëherë kur nis app-i."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_name TEXT,
            job_description TEXT,
            match_score REAL,
            missing_skills TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_analysis(resume_name, job_description, match_score, missing_skills):
    """Ruan një analizë të re në database."""
    # Sigurohemi qe match_score eshte float normal Python, jo numpy.float32
    match_score = float(match_score)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO analysis_history (resume_name, job_description, match_score, missing_skills, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (
        resume_name,
        job_description[:200],
        match_score,
        ", ".join(missing_skills),
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))
    conn.commit()
    conn.close()


def get_all_history():
    """Kthen të gjitha analizat e ruajtura, me të fundit në krye."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT resume_name, match_score, missing_skills, timestamp FROM analysis_history ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


# Test
if __name__ == "__main__":
    init_db()
    save_analysis("test_cv.pdf", "Sample job description text here", 73.5, ["docker", "aws"])
    history = get_all_history()
    for row in history:
        print(row)