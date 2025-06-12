# 🎙️ AI-Powered Mock Interview Application

A fully interactive, AI-powered mock interview system built with Streamlit. This application allows users to upload their resumes, automatically generates interview questions based on their profiles, conducts interviews using speech-to-text, and provides detailed analysis and feedback — simulating a real interview experience.

---

## 🚀 Features

- 📄 **Resume Upload & Parsing**  
  Users can upload their resume to extract key information and skills.

- 🤖 **AI-Based Question Generation**  
  The app generates domain-specific questions based on the uploaded resume using natural language processing.

- 🎤 **Speech-to-Text Integration**  
  Supports voice-based mock interviews with real-time speech-to-text conversion.

- 📊 **Interview Analysis**  
  Tracks response quality, fluency, confidence metrics, and provides structured feedback.

- 🔐 **User-Friendly UI**  
  Built with Streamlit for a simple, interactive, and easy-to-use interface.

---

## 🧱 Tech Stack

| Technology      | Usage |
|------------------|-------|
| **Python**       | Core programming language |
| **Streamlit**    | Frontend framework for building interactive UI |
| **OpenAI / GPT APIs** | Used for generating interview questions |
| **SpeechRecognition** | Speech-to-text conversion |
| **PyDub / pyaudio** | Audio handling |
| **NLTK / Spacy (optional)** | Resume parsing and NLP |
| **Pandas / JSON** | Data storage and processing |

---

## 🖼️ Architecture Overview

**1️⃣ Resume Upload**
- User uploads their resume (PDF/TXT).

**2️⃣ Resume Parsing & Skill Extraction**
- Extract key skills, technologies, and experience from resume using NLP.

**3️⃣ AI Question Generation**
- Generate interview questions dynamically based on extracted resume content using OpenAI's GPT model.

**4️⃣ Mock Interview Session**
- User answers questions via speech input.
- Speech is transcribed using SpeechRecognition & PyDub.

**5️⃣ Response Analysis**
- Analyze transcribed answers for fluency, length, and keyword relevance.

**6️⃣ Interview Summary & Feedback**
- Display performance metrics, feedback, and areas of improvement.



## 🔧 Installation & Setup

1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/mock-interview-app.git
cd mock-interview-app
```
2️⃣ Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
```
3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
4️⃣ Set up OpenAI API Key (for question generation)

Create a .env file in the project root directory:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```
5️⃣ Run the Application
```bash
streamlit run mock_interview.py
```
## 🗃️ Project Folder Structure

```bash
mock-interview-app/
│
├── mock_interview.py           # Main Streamlit application
├── requirements.txt            # Dependencies
├── assets/                     # (Optional) For storing static files
├── utils/                      # (Optional) Helper functions, parsing modules, etc.
├── models/                     # (Optional) Model-related files
└── .env                        # API keys and environment variables
```
## 💡 How it Works

1. Upload your resume in PDF or text format.

2. Resume parser extracts skills, experiences, and keywords.

3. AI generates customized interview questions based on parsed data.

4. User starts mock interview using speech input.

5. Speech is transcribed in real-time.

6. The system analyzes the responses and generates a performance summary.


## 🚀 Future Enhancements

✅ Add scoring based on confidence, relevance, and fluency.

✅ Include video-based interview simulation.

✅ Support multiple interview domains.

✅ Integrate advanced analytics with dashboards.

✅ Store interview history for progress tracking.

✅ Improve question diversity using advanced LLM prompt engineering.

✅ Authentication system for multiple users.

## Authors

- [@Mehwish4610](https://www.github.com/Mehwish4610)


## Screenshots

![App Screenshot](https://github.com/Mehwish4610/Agentic-AI-based-Mock-Interviewer-App/blob/master/Screenshot%202025-06-12%20165700.png)

![App Screenshot](https://github.com/Mehwish4610/Agentic-AI-based-Mock-Interviewer-App/blob/master/Screenshot%202025-06-12%20165742.png)

![App Screenshot](https://github.com/Mehwish4610/Agentic-AI-based-Mock-Interviewer-App/blob/master/Screenshot%202025-06-12%20165819.png)

![App Screenshot](https://github.com/Mehwish4610/Agentic-AI-based-Mock-Interviewer-App/blob/master/Screenshot%202025-06-12%20165844.png)

![App Screenshot](https://github.com/Mehwish4610/Agentic-AI-based-Mock-Interviewer-App/blob/master/Screenshot%202025-06-12%20165903.png)

![App Screenshot](https://github.com/Mehwish4610/Agentic-AI-based-Mock-Interviewer-App/blob/master/Screenshot%202025-06-12%20165921.png)


