import streamlit as st
import pandas as pd
import os
from utils.auth import logout_user, login_user, signup_user
# Page config
st.set_page_config(
    page_title="Leaderboard - Mock Interviewer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide default Streamlit navigation
hide_st_style = """
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# Sidebar Navigation
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
# Leaderboard Main Section
# -------------------------------

st.title("🏆 Resume Leaderboard")

# Load resume scores
if os.path.exists('data/resume_scores.csv'):
    resume_scores = pd.read_csv('data/resume_scores.csv')

    if not resume_scores.empty:
        # Sort by Score (descending)
        leaderboard = resume_scores.sort_values(by='score', ascending=False).reset_index(drop=True)

        st.subheader("Top Performers:")
        st.table(leaderboard[['username', 'score', 'badges']])
    else:
        st.info("No resume evaluations have been done yet. Be the first one!")
else:
    st.info("Resume scores file not found. Please evaluate a resume first.")
