import sqlite3
from datetime import datetime

DB_NAME = "history.db"


def init_db():
    """Krijon tabelën nese s'ekziston ende - thirret njehere kur nis app-i."""
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
    """Ruan nje analize te re ne database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO analysis_history (resume_name, job_description, match_score, missing_skills, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (
        resume_name,
        job_description[:200],  # ruajme vetem nje pjese, jo gjithe tekstin
        match_score,
        ", ".join(missing_skills),
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))
    conn.commit()
    conn.close()


def get_all_history():
    """Kthen te gjitha analizat e ruajtura, me te fundit ne krye."""
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