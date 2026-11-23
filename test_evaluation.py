from groq_ai import evaluate_answer

question = "What is Python?"

answer = """
Python is a high-level programming language.
It is easy to learn and has simple syntax.
It is used in AI, machine learning and web development.
"""

domain = "Python"

result = evaluate_answer(
    question=question,
    answer=answer,
    domain=domain
)

print("\nINTERVIEW ANSWER EVALUATION\n")
print(result)