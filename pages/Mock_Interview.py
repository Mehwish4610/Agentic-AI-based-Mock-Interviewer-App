# pages/3_Mock_Interview.py

import streamlit as st
import fitz
from utils.auth import logout_user
from utils.openai_helper import generate_interview_questions, evaluate_user_answer, read_aloud

# ----------------------------
# Streamlit App Starts
# ----------------------------

# Page Config
st.set_page_config(
    page_title="Mock Interview - Mock Interviewer",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide Streamlit Default Sidebar Nav
hide_st_style = """
    <style>
    [data-testid="stSidebarNav"] {display: none;}
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
    if st.button("📊 Leaderboard"):
        st.switch_page("pages/Leaderboard.py")
    if st.button("🚪 Logout"):
        logout_user()

# ----------------------------
# Mock Interview Section
# ----------------------------

st.title("🎤 Mock Interview (Single Page Setup + Questions)")

# Session State Initialization
if 'mock_started' not in st.session_state:
    st.session_state.mock_started = False

# If not started, show Setup Section
if not st.session_state.mock_started:
    uploaded_resume = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

    if uploaded_resume is not None:
        st.session_state.resume_bytes = uploaded_resume.read()

        job_role = st.selectbox(
            "Select the Job Role you're preparing for:",
            ["Data Analyst", "AI Developer", "Software Engineer", "Full Stack Developer", "Cloud Engineer"]
        )

        difficulty = st.radio(
            "Choose Difficulty Level:",
            ["Easy", "Medium", "Hard"]
        )

        round_type = st.radio(
            "Choose Round Type:",
            ["Technical", "HR", "Managerial", "General"]
        )

        if st.button("🚀 Start Mock Interview"):
            st.session_state.mock_job_role = job_role
            st.session_state.mock_difficulty = difficulty
            st.session_state.mock_round_type = round_type
            st.session_state.mock_started = True
            st.success("Starting your Mock Interview... 🚀")
            st.rerun()
    else:
        st.info("Please upload your resume first to start the mock interview.")

# ----------------------------
# Interview In Progress
# ----------------------------
else:
    resume_text = ""
    if 'resume_bytes' in st.session_state:
        doc = fitz.open(stream=st.session_state.resume_bytes, filetype="pdf")
        for page in doc:
            resume_text += page.get_text()

    if 'mock_questions' not in st.session_state:
        with st.spinner("Generating smart questions for you..."):
            questions_text = generate_interview_questions(
                resume_text,
                st.session_state.mock_job_role,
                st.session_state.mock_difficulty,
                st.session_state.mock_round_type
            )
            st.session_state.mock_questions = [q.strip() for q in questions_text.split('\n') if q.strip()]
            st.session_state.user_answers = []

    questions_list = st.session_state.mock_questions
    user_answers = st.session_state.user_answers

    st.subheader(f"📝 {st.session_state.mock_round_type} Round Questions for {st.session_state.mock_job_role} ({st.session_state.mock_difficulty} Level)")

    for idx, question in enumerate(questions_list, start=1):
        st.markdown(f"### Question {idx}: {question}")

        if st.button(f"🔊 Read Question {idx}", key=f"read_{idx}"):
            read_aloud(question)

        if idx > len(user_answers):
            answer = st.text_area(f"Your Answer to Q{idx}", key=f"answer_{idx}")
            if answer:
                user_answers.append(answer)

    st.session_state.user_answers = user_answers

    if len(user_answers) == len(questions_list):
        if st.button("🚀 Submit Interview"):
            st.success("Interview Submitted! Generating your feedback now...")

            total_score = 0
            st.subheader("📋 Your Interview Feedback:")

            for idx, (question, answer) in enumerate(zip(questions_list, user_answers), start=1):
                feedback = evaluate_user_answer(question, answer, st.session_state.mock_job_role, st.session_state.mock_difficulty)

                st.markdown(f"### Question {idx}: {question}")
                st.markdown(f"**Your Answer:** {answer}")
                st.markdown("**Agentic AI Feedback:**")
                st.markdown(feedback)

                try:
                    score_line = [line for line in feedback.split('\n') if "Score:" in line][0]
                    score_value = int(score_line.split(":")[1].strip().replace("/10", ""))
                    total_score += score_value
                except Exception:
                    st.error("⚡ Could not extract score properly.")

            overall_score = total_score / len(questions_list)
            st.success(f"🎯 Your Overall Interview Score: **{overall_score:.1f} / 10**")

            if overall_score >= 8:
                st.balloons()
                st.success("Excellent performance! 🚀 You're ready!")
            elif overall_score >= 6:
                st.info("Good attempt! Keep polishing your communication.")
            else:
                st.warning("Needs more practice. Focus on structuring answers clearly.")

            st.info("You can retake the mock interview to improve anytime.")

            # 🔄 Retake Interview Button
            if st.button("🔄 Retake Interview"):
                keys_to_clear = ["mock_started", "mock_job_role", "mock_difficulty", "mock_round_type", "mock_questions", "user_answers", "resume_bytes"]
                for key in keys_to_clear:
                    if key in st.session_state:
                        del st.session_state[key]
                st.success("Interview Reset! Starting fresh... 🔄")
                st.switch_page("pages/Mock_Interview.py")
