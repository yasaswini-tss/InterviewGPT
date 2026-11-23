# InterviewGPT – AI-Powered Interview Preparation and Evaluation System

## Overview

InterviewGPT is an AI-powered interview preparation application designed to help students and job seekers practice technical interviews, generate domain-specific questions, and improve their answers through automated AI feedback.

The application combines Python, Streamlit, LangChain, ChromaDB, and Groq AI to provide an interactive interview preparation experience.

## Features

- **Resume Analyzer:** Upload a PDF resume and identify technical skills using keyword-based extraction.
- **AI Interview Question Generation:** Generate technical interview questions for selected domains.
- **RAG-Based Question Retrieval:** Retrieve relevant questions using vector search and ChromaDB.
- **AI Answer Evaluation:** Receive feedback on technical knowledge, strengths, weaknesses, missing concepts, and suggested improvements.
- **Evaluation History:** Review previous answer evaluations during the current application session.
- **Question Download:** Download generated interview questions as a text file.
- **Interactive Dashboard:** Navigate through the Overview, Interview Studio, and Evaluation History sections.

## Technical Domains

- Python
- SQL
- Machine Learning
- Deep Learning
- Natural Language Processing
- Transformers
- Generative AI
- Retrieval-Augmented Generation (RAG)
- LangChain

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Streamlit | Interactive web application |
| Groq API | AI question generation and answer evaluation |
| LangChain | RAG workflow and document handling |
| ChromaDB | Vector database |
| Hugging Face Sentence Transformers | Text embeddings |
| pdfplumber | PDF resume text extraction |

## Project Structure

```text
InterviewGPT/
│
├── app.py
├── rag_pipeline.py
├── groq_ai.py
├── test_groq.py
├── test_evaluation.py
├── requirements.txt
├── .gitignore
├── README.md
│
└── data/
    └── InterviewGPT_Question_Bank.pdf
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/yasaswinitss/InterviewGPT.git
cd InterviewGPT
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the Groq API key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Replace the placeholder with your own API key. Do not share or upload this file.

### 6. Run the application

```bash
streamlit run app.py
```

The application will open in your web browser.

## Application Workflow

1. Upload a resume in PDF format.
2. Analyze the resume to identify technical skills.
3. Select an interview domain.
4. Generate interview questions.
5. Submit an answer for AI evaluation.
6. Review the feedback and evaluation history.

## Future Enhancements

- Permanent evaluation history using SQLite.
- More advanced resume-based question personalization.
- Improved document-based RAG question retrieval.
- Structured performance analytics.
- Voice-based interview practice.
- Multi-round mock interviews.

## Project Status

Developed as a Generative AI internship project. The current version is a working prototype. Some features, including permanent history storage and advanced resume personalization, are planned for future enhancement.

## Author

**Yasaswini Sai Sri Theerdhala**

B.Tech – Electronics and Communication Engineering

## Acknowledgement

Developed as part of a Generative AI internship project with the aim of making technical interview preparation more interactive and accessible.