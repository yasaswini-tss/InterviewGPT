
import streamlit as st
import pdfplumber
from io import BytesIO
from datetime import datetime

from rag_pipeline import retrieve_questions
from groq_ai import generate_interview_questions, evaluate_answer


# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="InterviewGPT | AI Interview Preparation",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# 2. PROFESSIONAL CSS
# ==================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #f5f7fb;
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background-color: #111827 !important;
}

[data-testid="stSidebar"] > div {
    background-color: #111827 !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] span {
    color: #f8fafc !important;
}

.brand {
    font-size: 27px;
    font-weight: 800;
    color: #ffffff !important;
    padding-top: 10px;
}

.brand span {
    color: #60a5fa !important;
}

.sidebar-caption {
    color: #cbd5e1 !important;
    font-size: 12px;
    margin-bottom: 20px;
}

/* SIDEBAR UPLOAD */

[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    background-color: #1e293b !important;
    border: 1px solid #475569 !important;
    border-radius: 10px;
    padding: 10px;
}

[data-testid="stSidebar"] [data-testid="stFileUploader"] * {
    color: #f8fafc !important;
}

/* PROJECT MODULE CARDS */

.module-card {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 11px 13px;
    margin: 8px 0;
    color: #f8fafc !important;
    font-size: 13px;
    font-weight: 600;
}

.module-card span {
    color: #f8fafc !important;
}

/* WELCOME BANNER */

.hero {
    background: linear-gradient(120deg, #172554, #2563eb);
    padding: 32px;
    border-radius: 18px;
    margin-bottom: 25px;
}

.hero h1 {
    color: #ffffff !important;
    font-size: 32px;
    font-weight: 800;
    margin-bottom: 10px;
}

.hero p {
    color: #dbeafe !important;
    font-size: 15px;
    margin-bottom: 0;
}

/* SECTION HEADINGS */

.section-heading {
    color: #172554 !important;
    font-size: 22px;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 15px;
}

/* MAIN CONTENT TEXT */

[data-testid="stAppViewContainer"] [data-testid="stMarkdownContainer"] p,
[data-testid="stAppViewContainer"] [data-testid="stMarkdownContainer"] li,
[data-testid="stAppViewContainer"] [data-testid="stMarkdownContainer"] h1,
[data-testid="stAppViewContainer"] [data-testid="stMarkdownContainer"] h2,
[data-testid="stAppViewContainer"] [data-testid="stMarkdownContainer"] h3,
[data-testid="stAppViewContainer"] [data-testid="stMarkdownContainer"] h4,
[data-testid="stAppViewContainer"] [data-testid="stMarkdownContainer"] strong {
    color: #111827 !important;
}

/* METRIC CARDS */

.metric-card {
    background-color: #ffffff;
    border: 1px solid #e5eaf2;
    border-radius: 14px;
    padding: 20px;
    min-height: 115px;
    box-shadow: 0 3px 12px rgba(15, 23, 42, 0.04);
}

.metric-label {
    color: #64748b !important;
    font-size: 13px;
    font-weight: 600;
}

.metric-value {
    color: #172554 !important;
    font-size: 27px;
    font-weight: 800;
    margin-top: 8px;
}

/* INFORMATION CARDS */

.info-card {
    background-color: #ffffff;
    border: 1px solid #e5eaf2;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 14px;
}

.info-card h3 {
    color: #172554 !important;
    font-size: 17px;
}

.info-card p {
    color: #64748b !important;
    font-size: 14px;
}

/* INPUT FIELDS */

.stTextArea textarea,
.stTextInput input {
    background-color: #ffffff !important;
    color: #111827 !important;
    border: 1px solid #cbd5e1 !important;
}

.stTextArea textarea::placeholder {
    color: #64748b !important;
}

.stSelectbox div[data-baseweb="select"] {
    background-color: #ffffff !important;
}

.stSelectbox div[data-baseweb="select"] * {
    color: #111827 !important;
}

/* MAIN NAVIGATION TABS */

.stTabs [data-baseweb="tab-list"] {
    background-color: #e2e8f0 !important;
    padding: 6px;
    border-radius: 12px;
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    background-color: #f8fafc !important;
    color: #334155 !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    padding: 10px 18px !important;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background-color: #2563eb !important;
    color: #ffffff !important;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] * {
    color: #ffffff !important;
}

.stTabs [data-baseweb="tab-highlight"] {
    background-color: #2563eb !important;
}

/* BUTTONS */

.stButton button,
.stFormSubmitButton button {
    border-radius: 9px;
    font-weight: 600;
    min-height: 42px;
}

/* PRIMARY BUTTON */

.stButton button[kind="primary"],
.stFormSubmitButton button[kind="primary"] {
    background-color: #2563eb !important;
    color: #ffffff !important;
    border: none !important;
}

.stButton button[kind="primary"]:hover,
.stFormSubmitButton button[kind="primary"]:hover {
    background-color: #1d4ed8 !important;
}

/* DOWNLOAD BUTTON */

.stDownloadButton button {
    background-color: #2563eb !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 9px !important;
    font-weight: 600;
    min-height: 42px;
}

.stDownloadButton button * {
    color: #ffffff !important;
}

.stDownloadButton button:hover {
    background-color: #1d4ed8 !important;
}

/* ALERTS */

.stAlert p {
    color: #111827 !important;
}

/* EVALUATION QUESTION AND ANSWER DISPLAY */

.evaluation-card {
    background-color: #ffffff;
    border: 1px solid #dbe3ee;
    border-radius: 12px;
    padding: 18px;
    margin: 12px 0;
}

.evaluation-card h4 {
    color: #1e3a8a !important;
    font-size: 15px;
    margin-bottom: 8px;
}

.evaluation-card p {
    color: #111827 !important;
    font-size: 14px;
    line-height: 1.7;
}

/* EXPANDERS */

[data-testid="stExpander"] {
    background-color: #ffffff;
    border: 1px solid #e5eaf2;
    border-radius: 10px;
}

/* FOOTER */

.footer {
    text-align: center;
    color: #64748b !important;
    font-size: 12px;
    padding: 25px 0 10px 0;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# 3. SESSION STATE
# ==================================================

if "interview_history" not in st.session_state:
    st.session_state.interview_history = []

if "generated_questions" not in st.session_state:
    st.session_state.generated_questions = ""

if "selected_domain" not in st.session_state:
    st.session_state.selected_domain = "Python"

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "resume_skills" not in st.session_state:
    st.session_state.resume_skills = []

if "latest_feedback" not in st.session_state:
    st.session_state.latest_feedback = ""


# ==================================================
# 4. SKILL EXTRACTION
# ==================================================

SKILL_LIST = [
    "Python", "Java", "C", "C++", "SQL",
    "Machine Learning", "Deep Learning",
    "Natural Language Processing", "NLP",
    "Transformers", "Generative AI", "RAG",
    "LangChain", "Streamlit", "TensorFlow",
    "PyTorch", "HTML", "CSS", "JavaScript",
    "Embedded Systems", "VLSI", "Verilog",
    "MATLAB", "Git", "GitHub"
]


def extract_skills(resume_text):

    found_skills = []
    resume_lower = resume_text.lower()

    for skill in SKILL_LIST:
        if skill.lower() in resume_lower:
            found_skills.append(skill)

    return sorted(set(found_skills))


# ==================================================
# 5. RESUME PDF EXTRACTION
# ==================================================

def extract_resume_text(uploaded_file):

    text = ""

    with pdfplumber.open(BytesIO(uploaded_file.getvalue())) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


# ==================================================
# 6. SIDEBAR
# ==================================================

with st.sidebar:

    st.markdown("""
    <div class="brand">Interview<span>GPT</span> 🎯</div>
    <div class="sidebar-caption">
        AI-Powered Interview Preparation
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 📄 Resume Analyzer")

    uploaded_resume = st.file_uploader(
        "Upload your resume",
        type=["pdf"]
    )

    if st.button("Analyze Resume", use_container_width=True):

        if uploaded_resume is None:

            st.warning("Please upload your resume first.")

        else:

            try:

                with st.spinner("Analyzing your resume..."):

                    resume_text = extract_resume_text(uploaded_resume)

                    if not resume_text.strip():

                        st.warning(
                            "No readable text found in the PDF."
                        )

                    else:

                        st.session_state.resume_text = resume_text

                        st.session_state.resume_skills = extract_skills(
                            resume_text
                        )

                        st.success("Resume analyzed successfully!")

            except Exception as error:

                st.error(f"Resume analysis failed: {error}")

    if st.session_state.resume_text:

        st.markdown("---")
        st.markdown("### Resume Results")

        st.write(
            f"Skills detected: {len(st.session_state.resume_skills)}"
        )

        if st.session_state.resume_skills:

            for skill in st.session_state.resume_skills:
                st.write(f"• {skill}")

        else:

            st.caption("No matching skills detected.")

    st.markdown("---")
    st.markdown("### 📌 Project Modules")

    st.markdown("""
    <div class="module-card"><span>🏠 &nbsp; Overview</span></div>
    <div class="module-card"><span>🎯 &nbsp; Interview Studio</span></div>
    <div class="module-card"><span>🤖 &nbsp; AI Evaluation</span></div>
    <div class="module-card"><span>📈 &nbsp; Evaluation History</span></div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Python | Streamlit | RAG | Groq AI")


# ==================================================
# 7. MAIN WELCOME BANNER
# ==================================================

st.markdown("""
<div class="hero">
    <h1>Welcome to InterviewGPT 👋</h1>
    <p>
        Prepare smarter. Practice technical interviews.
        Improve your answers with AI-powered feedback.
    </p>
</div>
""", unsafe_allow_html=True)


# ==================================================
# 8. DASHBOARD METRICS
# ==================================================

total_evaluations = len(
    st.session_state.interview_history
)

resume_status = (
    "Uploaded"
    if st.session_state.resume_text
    else "Not Uploaded"
)

metric1, metric2, metric3 = st.columns(3)

with metric1:

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">📝 Questions Generated</div>
        <div class="metric-value">
            {1 if st.session_state.generated_questions else 0}
        </div>
    </div>
    """, unsafe_allow_html=True)


with metric2:

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">📊 Answers Evaluated</div>
        <div class="metric-value">{total_evaluations}</div>
    </div>
    """, unsafe_allow_html=True)


with metric3:

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">📄 Resume Status</div>
        <div class="metric-value" style="font-size:21px;">
            {resume_status}
        </div>
    </div>
    """, unsafe_allow_html=True)


st.markdown(
    '<div class="section-heading">Your Interview Workspace</div>',
    unsafe_allow_html=True
)


# ==================================================
# 9. DASHBOARD TABS
# ==================================================

dashboard_tab, practice_tab, history_tab = st.tabs([
    "🏠 Overview",
    "🎯 Interview Studio",
    "📈 Evaluation History"
])


# ==================================================
# 10. OVERVIEW TAB
# ==================================================

with dashboard_tab:

    left_col, right_col = st.columns(2)

    with left_col:

        st.markdown("""
        <div class="info-card">
            <h3>🎯 Practice Technical Interviews</h3>
            <p>
                Select a technical domain and generate interview
                questions using your question bank and AI.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with right_col:

        st.markdown("""
        <div class="info-card">
            <h3>🤖 Get AI-Powered Feedback</h3>
            <p>
                Submit your answer to receive feedback on technical
                knowledge, strengths, weaknesses and missing concepts.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🚀 How to use InterviewGPT")

    st.markdown("""
    1. Upload your resume using the sidebar.
    2. Open the Interview Studio tab.
    3. Select a technical domain.
    4. Generate interview questions.
    5. Submit your answer for AI evaluation.
    6. View your feedback in Evaluation History.
    """)

    if st.session_state.resume_skills:

        st.markdown("### 💡 Skills Detected in Your Resume")

        st.write(", ".join(st.session_state.resume_skills))


# ==================================================
# 11. INTERVIEW STUDIO
# ==================================================

with practice_tab:

    st.markdown("### 🎯 Interview Practice")

    st.write(
        "Generate technical interview questions from your selected domain."
    )

    domains = [
        "Python",
        "SQL",
        "Machine Learning",
        "Deep Learning",
        "Natural Language Processing",
        "Transformers",
        "Generative AI",
        "RAG",
        "LangChain"
    ]

    selected_domain = st.selectbox(
        "Choose your technical domain",
        domains,
        index=domains.index(st.session_state.selected_domain)
        if st.session_state.selected_domain in domains else 0
    )

    number_of_questions = st.slider(
        "Number of questions",
        min_value=1,
        max_value=10,
        value=3
    )

    if st.button(
        "✨ Generate Interview Questions",
        type="primary",
        use_container_width=True
    ):

        try:

            with st.spinner(
                "Searching the question bank and generating questions..."
            ):

                retrieved_docs = retrieve_questions(
                    domain=selected_domain,
                    query=f"Important {selected_domain} interview questions",
                    k=number_of_questions
                )

                context = "\n".join(
                    [doc.page_content for doc in retrieved_docs]
                )

                if not context.strip():

                    st.warning(
                        "No questions were retrieved. "
                        "Check your RAG database."
                    )

                else:

                    generated = generate_interview_questions(
                        domain=selected_domain,
                        context=context,
                        number=number_of_questions
                    )

                    if generated:

                        st.session_state.generated_questions = generated

                        st.session_state.selected_domain = selected_domain

                    else:

                        st.warning(
                            "The AI did not return questions. Please try again."
                        )

        except Exception as error:

            st.error(
                f"Question generation failed: {error}"
            )

    if st.session_state.generated_questions:

        st.markdown("---")
        st.markdown("### 📝 Generated Interview Questions")

        st.info(
            f"Selected Domain: {st.session_state.selected_domain}"
        )

        st.markdown(
            st.session_state.generated_questions
        )

        st.download_button(
            label="⬇️ Download Questions",
            data=st.session_state.generated_questions,
            file_name="interview_questions.txt",
            mime="text/plain",
            use_container_width=True
        )

    # ANSWER EVALUATION

    st.markdown("---")
    st.markdown("### 🤖 AI Answer Evaluation")

    st.write(
        "Enter an interview question and your answer to receive AI feedback."
    )

    with st.form("answer_evaluation_form"):

        evaluation_domain = st.selectbox(
            "Select answer domain",
            domains
        )

        question = st.text_area(
            "Interview Question",
            placeholder="Enter your interview question...",
            height=100
        )

        answer = st.text_area(
            "Your Answer",
            placeholder="Type your answer here...",
            height=180
        )

        submitted = st.form_submit_button(
            "🚀 Evaluate My Answer",
            type="primary",
            use_container_width=True
        )

    if submitted:

        if not question.strip() or not answer.strip():

            st.warning(
                "Please enter both the question and your answer."
            )

        else:

            try:

                with st.spinner("AI is evaluating your answer..."):

                    feedback = evaluate_answer(
                        question=question,
                        answer=answer,
                        domain=evaluation_domain
                    )

                    history_item = {
                        "date": datetime.now().strftime(
                            "%d %b %Y, %I:%M %p"
                        ),
                        "domain": evaluation_domain,
                        "question": question,
                        "answer": answer,
                        "feedback": feedback
                    }

                    st.session_state.interview_history.append(
                        history_item
                    )

                    st.session_state.latest_feedback = feedback

                st.success("Answer evaluated successfully!")

            except Exception as error:

                st.error(
                    f"Answer evaluation failed: {error}"
                )

    if st.session_state.latest_feedback:

        st.markdown("---")
        st.markdown("### 📋 AI Evaluation Report")

        st.markdown(
            st.session_state.latest_feedback
        )


# ==================================================
# 12. EVALUATION HISTORY
# ==================================================

with history_tab:

    st.markdown("### 📈 Evaluation History")

    if st.session_state.interview_history:

        st.write(
            f"Total evaluations: "
            f"{len(st.session_state.interview_history)}"
        )

        for index, item in enumerate(
            reversed(st.session_state.interview_history),
            start=1
        ):

            with st.expander(
                f"Evaluation {index} | {item['domain']} | {item['date']}"
            ):

                st.markdown("**Interview Question**")

                st.markdown(
                    f'<div class="evaluation-card">'
                    f'<h4>Question</h4>'
                    f'<p>{item["question"]}</p>'
                    f'</div>',
                    unsafe_allow_html=True
                )

                st.markdown("**Your Answer**")

                st.markdown(
                    f'<div class="evaluation-card">'
                    f'<h4>Your Answer</h4>'
                    f'<p>{item["answer"]}</p>'
                    f'</div>',
                    unsafe_allow_html=True
                )

                st.markdown("**AI Feedback**")

                st.markdown(item["feedback"])

        if st.button("🗑️ Clear Evaluation History"):

            st.session_state.interview_history = []
            st.session_state.latest_feedback = ""

            st.rerun()

    else:

        st.info(
            "No evaluation history available. "
            "Complete an interview evaluation to see your history here."
        )


# ==================================================
# 13. FOOTER
# ==================================================

st.markdown("""
<div class="footer">
    InterviewGPT | AI-Powered Interview Preparation and Evaluation System
    <br><br>
    Built using Python • Streamlit • LangChain • ChromaDB • Groq AI
</div>
""", unsafe_allow_html=True)
