import streamlit as st
import os
from extractor import extract_text_from_pdf
from matcher import calculate_match_score
from skills import find_missing_skills
from database import init_db, save_analysis, get_all_history

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False


def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])


def extract_resume_text(uploaded_file):
    file_ext = os.path.splitext(uploaded_file.name)[1].lower()
    temp_path = f"temp_resume{file_ext}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    if file_ext == ".pdf":
        text = extract_text_from_pdf(temp_path)
    elif file_ext == ".docx":
        if not DOCX_AVAILABLE:
            raise RuntimeError("python-docx nuk është instaluar.")
        text = extract_text_from_docx(temp_path)
    else:
        raise ValueError("Format i pambështetur. Përdor PDF ose DOCX.")

    os.remove(temp_path)
    return text


def render_pills(items, color, bg):
    if not items:
        return "<p style='color:#9ca3af;font-style:italic;font-size:0.9rem;'>Asnjë</p>"
    spans = "".join([
        f"<span style='display:inline-block;margin:3px 6px 3px 0;padding:5px 13px;"
        f"border-radius:20px;background:{bg};color:{color};font-size:0.85rem;"
        f"font-family:Inter,sans-serif;'>{s}</span>"
        for s in items
    ])
    return f"<div>{spans}</div>"


def render_score_gauge(score, subtitle):
    html = f"""
    <div style="display:flex;align-items:center;gap:1.8rem;margin:1.2rem 0 1.6rem 0;">
      <div style="position:relative;width:130px;height:130px;border-radius:50%;
          background:conic-gradient(#2F6F6B {score}%, #E4E1DA {score}% 100%);
          display:flex;align-items:center;justify-content:center;flex-shrink:0;">
        <div style="width:98px;height:98px;border-radius:50%;background:#FCFBF8;
            display:flex;align-items:center;justify-content:center;">
          <span style="font-family:'Source Serif 4',serif;font-size:1.7rem;
              font-weight:600;color:#23262B;">{score}%</span>
        </div>
      </div>
      <div style="max-width:280px;">
        <p style="font-family:Inter,sans-serif;color:#8A8F98;font-size:0.92rem;
            margin:0;line-height:1.4;">{subtitle}</p>
      </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_ledger_row(rank, name, score, missing_text):
    rank_html = f"{rank}. " if rank is not None else ""
    score_html = f"{score}%" if score is not None else "—"
    html = f"""
    <div style="display:flex;justify-content:space-between;align-items:baseline;
        padding:0.85rem 0;border-bottom:1px solid #E4E1DA;">
      <div>
        <span style="font-family:'Source Serif 4',serif;font-size:1.05rem;color:#23262B;">
            {rank_html}{name}</span><br/>
        <span style="font-family:Inter,sans-serif;font-size:0.8rem;color:#8A8F98;">{missing_text}</span>
      </div>
      <div style="font-family:'Source Serif 4',serif;font-size:1.25rem;
          color:#2F6F6B;white-space:nowrap;padding-left:1rem;">{score_html}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


init_db()
st.set_page_config(page_title="Resume Screener", layout="wide")

if os.path.exists("style.css"):
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ------------------- SIDEBAR -------------------
with st.sidebar:
    st.markdown(
        "<p style='font-family:Source Serif 4,serif;font-size:1.3rem;"
        "font-weight:600;margin-bottom:0;'>Resume Screener</p>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='font-family:Inter,sans-serif;font-size:0.82rem;color:#8A8F98;"
        "margin-top:0.2rem;'>Analizë semantike CV-je</p>",
        unsafe_allow_html=True
    )
    st.markdown("<hr>", unsafe_allow_html=True)
    page = st.radio("Navigimi", ["Analizë e vetme", "Krahaso disa CV", "Historiku"], label_visibility="collapsed")

st.title("Sa mirë përputhet CV-ja jote?")

# ------------------- FAQJA 1: Analizë e vetme -------------------
if page == "Analizë e vetme":
    uploaded_file = st.file_uploader("Ngarko CV-në (PDF ose DOCX)", type=["pdf", "docx"], key="single")
    job_description = st.text_area("Ngjit job description-in këtu", height=170, key="jd_single")

    if st.button("Analizo", key="btn_single"):
        if uploaded_file is None:
            st.warning("Ngarko një CV para se të vazhdosh.")
        elif job_description.strip() == "":
            st.warning("Shkruaj një job description para se të vazhdosh.")
        else:
            try:
                with st.spinner("Duke analizuar..."):
                    resume_text = extract_resume_text(uploaded_file)
                    if not resume_text.strip():
                        st.error("Nuk u gjet tekst i lexueshëm në këtë file.")
                        st.stop()

                    score = calculate_match_score(resume_text, job_description)
                    missing_skills, matched_skills = find_missing_skills(resume_text, job_description)
                    save_analysis(uploaded_file.name, job_description, score, missing_skills)

                st.markdown("<hr>", unsafe_allow_html=True)
                render_score_gauge(score, "Bazuar në ngjashmërinë kuptimore mes CV-së dhe job description-it, jo vetëm fjalë të njëjta.")

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Aftësi që përputhen**")
                    st.markdown(render_pills(matched_skills, "#2F6F6B", "#E4F0EE"), unsafe_allow_html=True)
                with col2:
                    st.markdown("**Aftësi që mungojnë**")
                    st.markdown(render_pills(missing_skills, "#B9793A", "#F6ECDF"), unsafe_allow_html=True)

                with st.expander("Shiko tekstin e nxjerrë nga CV-ja"):
                    st.text(resume_text)

            except Exception as e:
                st.error(f"Ndodhi një gabim gjatë përpunimit të file-it: {e}")

# ------------------- FAQJA 2: Batch ranking -------------------
elif page == "Krahaso disa CV":
    st.write("Ngarko disa CV njëherësh dhe shiko cili përputhet më mirë.")

    uploaded_files = st.file_uploader(
        "Ngarko disa CV (PDF ose DOCX)", type=["pdf", "docx"], accept_multiple_files=True, key="batch"
    )
    job_description_batch = st.text_area("Ngjit job description-in këtu", height=170, key="jd_batch")

    if st.button("Rendit CV-të", key="btn_batch"):
        if not uploaded_files:
            st.warning("Ngarko të paktën një CV.")
        elif job_description_batch.strip() == "":
            st.warning("Shkruaj një job description.")
        else:
            results = []
            with st.spinner(f"Duke analizuar {len(uploaded_files)} CV..."):
                for f in uploaded_files:
                    try:
                        text = extract_resume_text(f)
                        if not text.strip():
                            results.append((f.name, None, "File pa tekst të lexueshëm"))
                            continue
                        score = calculate_match_score(text, job_description_batch)
                        missing, matched = find_missing_skills(text, job_description_batch)
                        save_analysis(f.name, job_description_batch, score, missing)
                        results.append((f.name, score, f"Mungojnë: {', '.join(missing) if missing else 'asnjë'}"))
                    except Exception as e:
                        results.append((f.name, None, f"Gabim: {e}"))

            results.sort(key=lambda r: (r[1] is None, -(r[1] or 0)))

            st.markdown("<hr>", unsafe_allow_html=True)
            for rank, (name, score, note) in enumerate(results, start=1):
                render_ledger_row(rank, name, score, note)

# ------------------- FAQJA 3: Historiku -------------------
else:
    st.write("Të gjitha analizat e mëparshme, të ruajtura lokalisht.")
    st.markdown("<hr>", unsafe_allow_html=True)

    history = get_all_history()
    if history:
        for resume_name, match_score, missing, timestamp in history:
            note = f"{timestamp} · Mungonin: {missing}" if missing else timestamp
            render_ledger_row(None, resume_name, match_score, note)
    else:
        st.write("Ende s'ka analiza të ruajtura.")
