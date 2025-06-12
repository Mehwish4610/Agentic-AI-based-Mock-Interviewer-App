import streamlit as st
import pandas as pd
import os

USER_FILE = 'data/users.csv'

def logout_user():
    """Logout the user and send back to Login page."""
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.success("Logged out successfully!")
    st.switch_page("app.py") 

# Ensure users.csv always has the correct header
def ensure_user_file():
    if not os.path.exists(USER_FILE) or os.path.getsize(USER_FILE) == 0:
        df = pd.DataFrame(columns=['username', 'password'])
        df.to_csv(USER_FILE, index=False)

def signup_user(username, password):
    ensure_user_file()
    users = pd.read_csv(USER_FILE)

    username = username.strip()
    password = password.strip()

    if username in users['username'].values:
        return False
    else:
        new_user = pd.DataFrame([[username, password]], columns=['username', 'password'])
        users = pd.concat([users, new_user], ignore_index=True)
        users.to_csv(USER_FILE, index=False)
        return True

def login_user(username, password):
    ensure_user_file()
    users = pd.read_csv(USER_FILE)

    username = username.strip()
    password = password.strip()

    # Force username and password columns to string, then strip
    users['username'] = users['username'].astype(str).str.strip()
    users['password'] = users['password'].astype(str).str.strip()

    if username not in users['username'].values:
        return "not_registered"

    user_record = users[(users['username'] == username) & (users['password'] == password)]

    if not user_record.empty:
        return "success"
    else:
        return "invalid_password"


def check_credentials():
    return os.path.exists(USER_FILE)
