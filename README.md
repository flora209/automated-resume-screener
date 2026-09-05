# 📄 Automated Resume Screener (ARS)

An NLP-powered tool that compares a resume against a job description using **semantic similarity** (not just keyword matching), and highlights which required skills are missing from the resume.

Built as an engineering learning project based on requirements from Cadmus Software.

---

## 🚀 What It Does

1. **Upload a resume (PDF)** and paste in a job description
2. The app extracts clean text from the PDF
3. Both texts are converted into vector embeddings that capture *meaning*, not just words
4. A **cosine similarity score (0–100%)** is calculated to show how well the resume matches the job
5. The app identifies which required skills are present in the resume and which are **missing**

---

## 🧠 Why Semantic Matching (Not Keyword Matching)?

A resume that says *"led a team of developers"* should match a job description asking for *"team leadership experience"* — even though the exact words are different. Traditional keyword search would miss this. This tool uses **Sentence-Transformers** to convert text into vectors that represent meaning, so it can catch these matches.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Text Extraction | `pdfminer.six` |
| NLP / Skill Detection | `spaCy` (PhraseMatcher) |
| Semantic Embeddings | `sentence-transformers` (`all-MiniLM-L6-v2`) |
| Similarity Scoring | `scikit-learn` (cosine similarity) |
| Frontend / UI | `Streamlit` |
| Backend Language | Python 3.10+ |

---

## 📂 Project Structure

```
├── extractor.py   # Extracts raw text from uploaded PDF resumes
├── matcher.py     # Converts text to embeddings & calculates match score
├── skills.py      # Detects matched/missing skills using spaCy PhraseMatcher
├── app.py         # Streamlit UI that ties everything together
└── .gitignore
```

---

## ⚙️ How to Run Locally

1. Clone the repository
```bash
git clone https://github.com/flora209/automated-resume-screener.git
cd automated-resume-screener
```

2. Install dependencies
```bash
pip install fastapi uvicorn python-multipart pdfminer.six PyPDF2 python-docx spacy sentence-transformers scikit-learn streamlit
python -m spacy download en_core_web_sm
```

3. Run the app
```bash
python -m streamlit run app.py
```

4. Open the local URL shown in the terminal (usually `http://localhost:8501`)

---

## ✨ Features

- ✅ PDF resume parsing
- ✅ Semantic (meaning-based) match scoring, not just keyword overlap
- ✅ Skill gap analysis — see exactly what's missing from a resume
- ✅ Simple, interactive web interface
- ✅ Error handling for corrupted or unreadable files

---

## 🔭 Possible Future Improvements

- Support `.docx` resumes in addition to PDF
- Rank multiple resumes at once against a single job description
- Expand the skills list or auto-detect skills without a hardcoded list
- Deploy live via Streamlit Community Cloud

---

## 👤 Author

Built by [flora209](https://github.com/flora209) as a hands-on project to learn NLP, semantic search, and full-stack Python development.