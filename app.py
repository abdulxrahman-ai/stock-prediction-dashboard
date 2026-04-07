import streamlit as st
import re

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.markdown(
    """
    <style>
    html {
        scroll-behavior: smooth;
    }

    .main {
        animation: fadeInPage 0.8s ease-in-out;
    }

    @keyframes fadeInPage {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .fade-section {
        animation: fadeUp 0.7s ease both;
    }

    .fade-delay-1 {
        animation-delay: 0.08s;
    }

    .fade-delay-2 {
        animation-delay: 0.16s;
    }

    .fade-delay-3 {
        animation-delay: 0.24s;
    }

    .fade-delay-4 {
        animation-delay: 0.32s;
    }

    .fade-delay-5 {
        animation-delay: 0.4s;
    }

    @keyframes fadeUp {
        from {
            opacity: 0;
            transform: translateY(18px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    div[data-testid="stMetric"] {
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 18px;
        padding: 14px 10px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        background: rgba(255, 255, 255, 0.02);
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 14px 32px rgba(15, 23, 42, 0.10);
    }

    div.stButton > button {
        transition: all 0.25s ease;
        border-radius: 12px;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.12);
    }

    div[data-testid="stTextArea"] textarea {
        transition: all 0.25s ease;
        border-radius: 12px;
    }

    div[data-testid="stTextArea"] textarea:focus {
        box-shadow: 0 0 0 1px rgba(100, 116, 139, 0.35);
    }

    div[data-testid="stProgressBar"] > div > div {
        transition: width 0.6s ease-in-out;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

SKILLS = [
    "python", "sql", "machine learning", "deep learning", "nlp",
    "pandas", "numpy", "tensorflow", "pytorch", "fastapi",
    "streamlit", "data analysis", "power bi", "tableau",
    "excel", "aws", "docker", "git", "api"
]

def analyze_resume(resume, jd):
    resume = resume.lower()
    jd = jd.lower()

    matched = [s for s in SKILLS if s in resume]
    missing = [s for s in SKILLS if s in jd and s not in resume]

    score = min(95, 50 + len(matched) * 3 - len(missing) * 2)

    strengths = []
    improvements = []

    if matched:
        strengths.append(f"Strong skills detected: {', '.join(matched[:5])}")

    if "project" in resume:
        strengths.append("Projects section detected — good for technical roles")

    if not strengths:
        strengths.append("Basic resume structure present")

    if missing:
        improvements.append(f"Add these skills: {', '.join(missing[:5])}")

    improvements.append("Add measurable achievements (%, numbers)")
    improvements.append("Use more action verbs (built, developed, created)")

    return score, matched, missing, strengths, improvements


st.markdown('<div class="fade-section fade-delay-1">', unsafe_allow_html=True)
st.title("AI Resume Analyzer")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="fade-section fade-delay-2">', unsafe_allow_html=True)
st.write("Upload your resume or paste text to analyze.")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="fade-section fade-delay-3">', unsafe_allow_html=True)
resume_text = st.text_area("Paste Resume Text")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="fade-section fade-delay-4">', unsafe_allow_html=True)
job_description = st.text_area(
    "Paste Job Description",
    value="Looking for AI/ML Engineer with Python, ML, SQL, FastAPI"
)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="fade-section fade-delay-5">', unsafe_allow_html=True)
analyze_clicked = st.button("Analyze Resume")
st.markdown('</div>', unsafe_allow_html=True)

if analyze_clicked:

    if not resume_text.strip():
        st.warning("Please paste resume text")
    else:
        score, matched, missing, strengths, improvements = analyze_resume(resume_text, job_description)

        st.markdown('<div class="fade-section">', unsafe_allow_html=True)
        st.subheader("Results")
        st.markdown('</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown('<div class="fade-section fade-delay-1">', unsafe_allow_html=True)
            st.metric("Score", f"{score}%")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="fade-section fade-delay-2">', unsafe_allow_html=True)
            st.metric("Matched Skills", len(matched))
            st.markdown('</div>', unsafe_allow_html=True)

        with col3:
            st.markdown('<div class="fade-section fade-delay-3">', unsafe_allow_html=True)
            st.metric("Missing Skills", len(missing))
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="fade-section fade-delay-2">', unsafe_allow_html=True)
        st.progress(score / 100)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="fade-section fade-delay-2">', unsafe_allow_html=True)
        st.subheader("Matched Skills")
        st.write(matched)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="fade-section fade-delay-3">', unsafe_allow_html=True)
        st.subheader("Missing Skills")
        st.write(missing)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="fade-section fade-delay-4">', unsafe_allow_html=True)
        st.subheader("Strengths")
        for s in strengths:
            st.success(s)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="fade-section fade-delay-5">', unsafe_allow_html=True)
        st.subheader("Improvements")
        for i in improvements:
            st.warning(i)
        st.markdown('</div>', unsafe_allow_html=True)
