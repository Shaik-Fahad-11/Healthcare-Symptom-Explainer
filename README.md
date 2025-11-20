# 🏥 Healthcare Symptom Explainer (MediSimplify)

A full-stack, AI-powered healthcare assistant that simplifies complex medical symptoms for patients. It utilizes **Google's Gemini 2.5 Flash** model for multimodal analysis (Text & Vision), generates professional PDF reports for doctors, and includes a secure authentication system with an admin dashboard.

⚠️ **MEDICAL DISCLAIMER**:  
This application is for **informational purposes only**. It is **NOT a diagnostic tool**. Always consult a certified medical professional for health concerns.

## ✨ Key Features

- 🧠 **Intelligent Chat**: Context-aware AI that remembers conversation history to provide relevant answers.
- 👁️ **Computer Vision**: Users can upload images of visible symptoms (rashes, swelling) for AI analysis.
- 🗣️ **Voice Interaction**: Integrated Speech-to-Text allows users to speak their symptoms directly via the browser API.
- 📄 **Professional PDF Reports**: Generates a structured, beautifully formatted PDF summary of the consultation (including embedded images) to share with doctors.
- 🔐 **Secure Authentication**: User Signup and Login system featuring a modern Glassmorphism UI.
- 📊 **Admin Analytics**: A dedicated dashboard to track user growth, conversation stats, and trending symptom keywords using NLP.
- 🌍 **Multi-Language**: Automatically detects the user's language and responds accordingly.

## 📂 Project Structure
HEALTHCARE-SYMPTOM-EXPLAINER/
├── static/
│   ├── favicon.ico          # Application Favicon
│   ├── script.js            # Frontend Logic (Voice, API calls, UI)
│   └── style.css            # Glassmorphism & Responsive Styling
├── templates/
│   ├── dashboard.html       # Admin Analytics Dashboard
│   ├── index.html           # Main Chat Interface
│   ├── login.html           # User Login Page
│   ├── no_conversation.html # Fallback template
│   └── signup.html          # User Signup Page
├── .env                     # Secrets (API Keys, DB URL - GitIgnored)
├── .gitignore               # Git exclusions
├── app.py                   # Main Flask Application & Backend Logic
├── Procfile                 # Production startup command (Gunicorn)
├── README.md                # Project Documentation
├── requirements.txt         # Python Dependencies
└── schema.sql               # Database Schema Definitions

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3 (Glassmorphism), Vanilla JavaScript (Web Speech API)
- **Backend**: Python (Flask)
- **Database**: PostgreSQL (via Neon Serverless)
- **AI Model**: Google Gemini 2.5 Flash (via `google-generativeai`)
- **PDF Generation**: ReportLab (Structure, Table styles, Image embedding)
- **Authentication**: Flask-Login, Werkzeug Security

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/healthcare-symptom-explainer.git
cd healthcare-symptom-explainer '''
### 2. Create Virtual Environment
