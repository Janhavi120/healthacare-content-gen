# Healthcare-Content-Generator

# Overview
Healthcare Content Generator is an AI-powered medical documentation assistant that generates professional, specialty-specific medical reports using Google's Gemini AI.

# 🛠️ Technologies Used
# Frontend
1. Streamlit - Web application framework
2. HTML/CSS - Custom styling and UI components

# Backend
1. Python 3.8+ - Core programming language
2. LangChain - AI orchestration and prompt management
3. Google Gemini AI - Report generation model

# Libraries & Dependencies
1. langchain-google-genai - Google Gemini integration
2. google-generativeai - Gemini API wrapper
3. datetime - Timestamp management
4. json - History file handling

# Development Tools
1. Git - Version control
2. pip - Package management
3. VS Code - Recommended IDE

# APIs
1. Gemini 2.5 Flash - AI model for report generation

# ✨ Key Features
1. AI-Powered Reports: Generate structured medical reports instantly
2. Specialties: Cardiology, Neurology, Orthopedics, Pediatrics, etc.
3. History Management: Auto-save and access all previous reports
4. Clean UI: Blue & white theme with responsive design
5. Download Reports: Export as text files

# 🚀 Quick Setup
# 1. Clone & install
git clone <repo-url>
cd GenAI_healthcare
pip install -r requirements.txt

# 2. Add API key in model.py
GEMINI_API_KEY = "your-gemini-api-key"

# 3. Run
streamlit run app.py

# 🎯 Usage

1. Enter patient details (age, gender, symptoms)
2. Choose report type
3. Select specialty (Cardiologist, Neurologist, etc.)
4. Click Generate
5. View/download or auto-save to history

#  Requirements
1. Python 3.8+.
2. Google Gemini API key
3. Dependencies: streamlit, langchain, google-generativeai
