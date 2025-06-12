import streamlit as st
import pandas as pd
import os
from utils.auth import signup_user, login_user, check_credentials, logout_user


# Hide the default Streamlit navigation menu when user is not logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.set_page_config(
        page_title="Mock Interviewer - Login",
        page_icon="🔐",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                [data-testid="stSidebarNav"] {display: none;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
else:
    st.set_page_config(
        page_title="Mock Interviewer",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# Hide Streamlit's default sidebar navigation
hide_st_style = """
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# Create data folder if not exists
if not os.path.exists('data'):
    os.makedirs('data')

def login_signup_page():
    st.title("🔐 Welcome to Mock Interviewer")

    with st.sidebar:
        st.header("Account")
        choice = st.radio("Login or Sign Up", ["Login", "Sign Up"])

    # Handle signup success flag
    if 'signup_successful' not in st.session_state:
        st.session_state.signup_successful = False

    if choice == "Sign Up":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')

        if st.button("Sign Up"):
            if signup_user(new_user, new_password):
                st.session_state.signup_successful = True
                st.rerun()
            else:
                st.error("Username already exists. Try a different one.")

    elif choice == "Login":
        st.subheader("Login to your account")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')

        if st.button("Login"):
            login_status = login_user(username, password)

            if login_status == "success":
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome {username}!")
                st.rerun()
            elif login_status == "invalid_password":
                st.error("❌ Invalid credentials. Please try again.")
            elif login_status == "not_registered":
                st.error("❌ You are not registered. Please Sign Up first.")

    # AFTER the radio button
    if st.session_state.signup_successful:
        st.success("✅ Account created successfully! Please login.")
        st.session_state.signup_successful = False  # Reset flag after showing


def home_page():
    st.title(f"🏡 Hello, {st.session_state.username}!")
    st.subheader("What would you like to do?")

    with st.sidebar:
        st.header("Navigation")
        if st.button("🏠 Home"):
            st.rerun()
        if st.button("📄 Resume Evaluation"):
            st.switch_page("pages/Resume_Evaluation.py")
        if st.button("📝 Mock Interview"):
            st.switch_page("pages/Mock_Interview.py")
        if st.button("📊 Leaderboard"):
            st.switch_page("pages/Leaderboard.py")
        if st.button("🚪 Logout"):
            logout_user()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📄👩🏻‍🎓 Resume Evaluation"):
            st.switch_page("pages/Resume_Evaluation.py")

    with col2:
        if st.button("📝👩🏻‍🎓 Mock Interview"):
            st.switch_page("pages/Mock_Interview.py")

    if st.button("📊 View Leaderboard"):
        st.switch_page("pages/Leaderboard.py")

# Main App Flow
if not st.session_state.logged_in:
    login_signup_page()
else:
    home_page()
