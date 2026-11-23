from groq_ai import generate_interview_questions

result = generate_interview_questions(
    domain="Python",
    context="Python lists, tuples, dictionaries and functions.",
    number=3
)

print("\nGenerated Interview Questions:\n")
print(result)