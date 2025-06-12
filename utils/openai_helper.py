# utils/openai_helper.py

import os
import requests
import tempfile
import pygame
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

# -----------------------
# Load environment variables
# -----------------------
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Initialize OpenAI Client
client = OpenAI(api_key=OPENAI_API_KEY)

# -----------------------
# Functions
# -----------------------

def ask_gpt(prompt, temperature=0.7, max_tokens=500):
    """Send a prompt to GPT-4 and return the response."""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content.strip()

def generate_interview_questions(resume_text, job_role, difficulty, round_type):
    """Generate 5 mock interview questions based on user's resume and selected options."""
    prompt = f"""
You are an expert interviewer AI.

You are preparing a {round_type} round mock interview for a candidate applying for a {job_role} role.

Here is their resume content:
{resume_text}

The difficulty level should be {difficulty}.

Generate 5 smart, clear, role-specific questions:
- Ask meaningful questions related to their resume
- Cover both technical and behavioral aspects (if relevant)
- Difficulty should match the selected level
- Keep each question in 1-2 lines
- Number the questions 1 to 5

Return only the questions, nothing else.
"""
    questions = ask_gpt(prompt, temperature=0.7, max_tokens=600)
    return questions

def evaluate_user_answer(question, answer, job_role, difficulty):
    """Evaluate user's answer contextually and give feedback."""
    prompt = f"""
You are a professional interview coach AI.

A candidate answered an interview question for a {job_role} role.

Question:
{question}

Candidate's Answer:
{answer}

Difficulty Level: {difficulty}

Evaluate the answer based on:
- Clarity
- Relevance
- Technical Accuracy
- Communication skills

Give:
- A Score out of 10
- 2-3 specific improvement tips
- Be honest but constructive

Answer Format:
Score: X/10
Improvement Tips:
- Tip 1
- Tip 2
- Tip 3
"""
    feedback = ask_gpt(prompt, temperature=0.5, max_tokens=500)
    return feedback

def read_aloud(text):
    """Use ElevenLabs API to read aloud the given text."""
    url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM/stream"  # Rachel's voice id

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }

    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            # Save audio temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
                tmpfile.write(response.content)
                tmpfile_path = tmpfile.name

            # Initialize mixer
            pygame.mixer.init()

            # Load and Play
            pygame.mixer.music.load(tmpfile_path)
            pygame.mixer.music.play()

            # Wait until playback finishes
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            # Stop and Quit mixer
            pygame.mixer.music.stop()
            pygame.mixer.quit()

            # Delete temp audio file
            os.remove(tmpfile_path)

        else:
            st.error(f"Failed to fetch audio from ElevenLabs. Status: {response.status_code}")

    except Exception as e:
        st.error(f"An error occurred during reading aloud: {e}")
