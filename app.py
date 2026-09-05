import streamlit as st
from extractor import extract_text_from_pdf
from matcher import calculate_match_score
from skills import find_missing_skills

st.set_page_config(page_title="Automated Resume Screener", page_icon="📄")

st.title("📄 Automated Resume Screener")
st.write("Ngarko CV-në dhe ngjit job description-in për të parë sa përputhen.")

uploaded_file = st.file_uploader("Ngarko CV-në (PDF)", type=["pdf"])
job_description = st.text_area("Ngjit Job Description këtu", height=200)

if st.button("Analizo"):
    if uploaded_file is None:
        st.warning("Të lutem ngarko një CV para se të vazhdosh.")
    elif job_description.strip() == "":
        st.warning("Të lutem shkruaj një job description para se të vazhdosh.")
    else:
        try:
            with st.spinner("Duke analizuar..."):
                with open("temp_resume.pdf", "wb") as f:
                    f.write(uploaded_file.getbuffer())

                resume_text = extract_text_from_pdf("temp_resume.pdf")

                if not resume_text.strip():
                    st.error("Nuk u gjet tekst i lexueshëm në këtë PDF. Provo një file tjetër.")
                    st.stop()

                score = calculate_match_score(resume_text, job_description)
                missing_skills, matched_skills = find_missing_skills(resume_text, job_description)

            st.success("Analiza u krye!")
            st.metric(label="Match Score", value=f"{score}%")

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("✅ Skills të përputhura")
                if matched_skills:
                    for skill in matched_skills:
                        st.write(f"- {skill}")
                else:
                    st.write("Asnjë skill i përbashkët i identifikuar.")

            with col2:
                st.subheader("⚠️ Skills që mungojnë")
                if missing_skills:
                    for skill in missing_skills:
                        st.write(f"- {skill}")
                else:
                    st.write("Asnjë skill kritik nuk mungon!")

            with st.expander("Shiko tekstin e nxjerrë nga CV-ja"):
                st.text(resume_text)

        except Exception as e:
            st.error(f"Ndodhi një gabim gjatë përpunimit të file-it: {e}")
