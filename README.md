🏥 Healthcare Symptom Explainer (MediSimplify)
==============================================

A full-stack, AI-powered healthcare assistant that simplifies complex medical symptoms for patients. It utilizes Google's **Gemini 2.5 Flash** model for multimodal analysis (Text & Vision), generates professional PDF reports for doctors, and includes a secure authentication system with an admin dashboard.

> **⚠️ MEDICAL DISCLAIMER:** This application is for informational purposes only. It is NOT a diagnostic tool. Always consult a certified medical professional for health concerns.

✨ Key Features
--------------

*   **🧠 Intelligent Chat:** Context-aware AI that remembers conversation history to provide relevant answers.
    
*   **👁️ Computer Vision:** Users can upload images of visible symptoms (rashes, swelling) for AI analysis.
    
*   **🗣️ Voice Interaction:** Integrated Speech-to-Text allows users to speak their symptoms directly via the browser API.
    
*   **📄 Professional PDF Reports:** Generates a structured, beautifully formatted PDF summary of the consultation (including embedded images) to share with doctors.
    
*   **🔐 Secure Authentication:** User Signup and Login system featuring a modern Glassmorphism UI.
    
*   **📊 Admin Analytics:** A dedicated dashboard to track user growth, conversation stats, and trending symptom keywords using NLP.
    
*   **🌍 Multi-Language:** Automatically detects the user's language and responds accordingly.
    

📂 Project Structure
--------------------

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   HEALTHCARE-SYMPTOM-EXPLAINER/  ├── static/  │   ├── favicon.ico          # Application Favicon  │   ├── script.js            # Frontend Logic (Voice, API calls, UI)  │   └── style.css            # Glassmorphism & Responsive Styling  ├── templates/  │   ├── dashboard.html       # Admin Analytics Dashboard  │   ├── index.html           # Main Chat Interface  │   ├── login.html           # User Login Page  │   ├── no_conversation.html # Fallback template  │   └── signup.html          # User Signup Page  ├── .env                     # Secrets (API Keys, DB URL - GitIgnored)  ├── .gitignore               # Git exclusions  ├── app.py                   # Main Flask Application & Backend Logic  ├── Procfile                 # Production startup command (Gunicorn)  ├── README.md                # Project Documentation  ├── requirements.txt         # Python Dependencies  └── schema.sql               # Database Schema Definitions   `

🛠️ Tech Stack
--------------

*   **Frontend:** HTML5, CSS3 (Glassmorphism), Vanilla JavaScript (Web Speech API).
    
*   **Backend:** Python (Flask).
    
*   **Database:** PostgreSQL (via Neon Serverless).
    
*   **AI Model:** Google Gemini 2.5 Flash (via google-generativeai).
    
*   **PDF Generation:** ReportLab (Structure, Table styles, Image embedding).
    
*   **Authentication:** Flask-Login, Werkzeug Security.
    

🚀 Installation & Setup
-----------------------

### 1\. Clone the Repository

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   git clone [https://github.com/your-username/healthcare-symptom-explainer.git](https://github.com/your-username/healthcare-symptom-explainer.git)  cd healthcare-symptom-explainer   `

### 2\. Create Virtual Environment

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   # Windows  python -m venv venv  venv\Scripts\activate  # Mac/Linux  python3 -m venv venv  source venv/bin/activate   `

### 3\. Install Dependencies

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pip install -r requirements.txt   `

### 4\. Configure Environment Variables

Create a .env file in the root directory and add your secrets:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   GEMINI_API_KEY=your_google_gemini_key  DATABASE_URL=postgresql://user:password@ep-xyz.region.neon.tech/dbname?sslmode=require  SECRET_KEY=your_complex_random_secret_key   `

### 5\. Initialize Database

Run the queries found in schema.sql using your Neon SQL Editor to create the users and chat\_logs tables.

### 6\. Run the Application

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python app.py   `

Visit http://localhost:5000 in your browser.

🗄️ Database Schema (schema.sql)
--------------------------------

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   -- Users Table  CREATE TABLE IF NOT EXISTS users (      id SERIAL PRIMARY KEY,      username TEXT UNIQUE NOT NULL,      password_hash TEXT NOT NULL,      is_admin BOOLEAN DEFAULT FALSE  );  -- Chat Logs Table (With Image Support)  CREATE TABLE IF NOT EXISTS chat_logs (      id SERIAL PRIMARY KEY,      session_id TEXT,      user_id INTEGER REFERENCES users(id),      user_input TEXT NOT NULL,      ai_response TEXT NOT NULL,      has_image BOOLEAN DEFAULT FALSE,      image_data BYTEA, -- Stores raw image bytes      timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP  );   `

🛡️ Admin Dashboard Access
--------------------------

To view the analytics dashboard (/admin):

1.  Sign up for a regular user account via the app.
    
2.  Access your Database (Neon) SQL Editor.
    
3.  UPDATE users SET is\_admin = TRUE WHERE username = 'your\_username';
    
4.  Logout and Login again. You will see the **Admin Dashboard** button in the sidebar.
    

☁️ Deployment
-------------

This project includes a Procfile for easy deployment to platforms like **Render** or **Heroku**.

1.  **Build Command:** pip install -r requirements.txt
    
2.  **Start Command:** gunicorn app:app
    
3.  **Environment Variables:** Add your keys from .env to the deployment dashboard.
    

🤝 License
----------

Distributed under the MIT License.
