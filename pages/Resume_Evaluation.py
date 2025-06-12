
import streamlit as st
import pandas as pd
import os
from utils.resume_parser import extract_text_from_pdf, analyze_resume
from utils.badges import assign_badges
from utils.auth import check_credentials, logout_user,signup_user, login_user
from utils.resume_parser import agentic_resume_feedback

# Page config
st.set_page_config(
    page_title="Resume Evaluation - Mock Interviewer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide Streamlit's default sidebar nav
hide_st_style = """
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# Navigation sidebar
with st.sidebar:
    st.header("Navigation")
    if st.button("🏠 Home"):
        st.switch_page("app.py")
    if st.button("📄 Resume Evaluation"):
        st.switch_page("pages/Resume_Evaluation.py")
    if st.button("📝 Mock Interview"):
        st.switch_page("pages/Mock_Interview.py")
    if st.button("📊 Leaderboard"):
        st.switch_page("pages/Leaderboard.py")
    if st.button("🚪 Logout"):
        logout_user()

# -------------------------------
# Your main Resume Evaluation code comes here BELOW
# -------------------------------

st.title("📄 Resume Evaluation")

st.write("Upload your resume (PDF) and get it evaluated instantly!")

uploaded_file = st.file_uploader("Upload your Resume (PDF only)", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Analyzing your resume..."):
        text = extract_text_from_pdf(uploaded_file)
        analysis = analyze_resume(text)
        badges = assign_badges(analysis)

        # Simple scoring mechanism
        score = 50
        score += min(len(analysis['skills']) * 5, 25)
        score += min(analysis['experience_years'] * 5, 15)
        if "Master's" in analysis['education']:
            score += 10

        score = min(score, 100)

        st.success(f"✅ Your Resume Score: **{score} / 100**")
        st.write("🏅 Badges Earned:")
        for badge in badges:
            st.write(f"- {badge}")

        st.subheader("🔍 Analysis:")
        st.write("**Skills Found:**", ", ".join(analysis['skills']))
        st.write("**Experience (years):**", analysis['experience_years'])
        st.write("**Education Level:**", ", ".join(analysis['education']))
        # Ask for Job Role
        job_role = st.selectbox(
            "Select the Job Role you're targeting (for resume feedback):",
            ["Data Analyst", "AI Developer", "Software Engineer", "Full Stack Developer", "Cloud Engineer"]
        )

        if st.button("🔍 Get Advanced Resume Feedback"):
            agentic_feedback = agentic_resume_feedback(text, job_role)
            st.subheader("🤖 Agentic AI Feedback on your Resume:")
            st.write(agentic_feedback)

        # Save to leaderboard
        resume_scores = pd.read_csv('data/resume_scores.csv')
        new_entry = pd.DataFrame([[st.session_state.username, score, ", ".join(badges)]], columns=['username', 'score', 'badges'])
        resume_scores = pd.concat([resume_scores, new_entry], ignore_index=True)
        resume_scores.to_csv('data/resume_scores.csv', index=False)
