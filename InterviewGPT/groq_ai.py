import os
from dotenv import load_dotenv
from groq import Groq

# Load API key from .env
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found. Check your .env file.")

# Connect to Groq
client = Groq(api_key=api_key)


def generate_interview_questions(domain, context, number=3):

    prompt = f"""
    You are an experienced technical interviewer.

    Technical domain: {domain}

    Retrieved context from the interview question bank:
    {context}

    Generate exactly {number} new interview questions
    related to {domain}.

    Requirements:
    1. Questions must be technically accurate.
    2. Questions must be suitable for students and beginners.
    3. Do not simply copy the retrieved questions.
    4. Include a mix of conceptual and practical questions.
    5. Number each question clearly.
    6. Do not provide answers.
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You are a professional technical interviewer."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.5,
        max_completion_tokens=1000
    )

    return response.choices[0].message.content
def evaluate_answer(question, answer, domain):

    prompt = f"""
    You are an experienced technical interviewer.

    Evaluate the candidate's interview answer.

    Technical Domain: {domain}

    Interview Question:
    {question}

    Candidate Answer:
    {answer}

    Evaluate the answer based on:

    1. Technical Knowledge
    2. Correctness
    3. Clarity and Communication
    4. Completeness

    Give your evaluation in this format:

    SCORE: Give a score out of 10.

    STRENGTHS:
    Mention what the candidate explained correctly.

    WEAKNESSES:
    Mention mistakes or areas that need improvement.

    MISSING CONCEPTS:
    Mention important concepts not covered.

    IMPROVED ANSWER:
    Provide a technically accurate and well-structured
    version of the answer.

    FINAL RECOMMENDATION:
    Give practical advice to improve the answer.

    Be constructive and beginner-friendly.
    Do not award marks for concepts that are incorrect.
    If the answer is empty or irrelevant, explain that clearly.
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You are a professional technical interview evaluator."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_completion_tokens=1500
    )

    return response.choices[0].message.content