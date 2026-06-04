from agent import Agent

agent = Agent()

tests = [
    ("(25 + 17) * 4", None),
    ("What is total sales?", "sales.xlsx"),
    ("What is the output?", "sample.py"),
    ("What is the capital of France?", None)
]

for question, file_name in tests:

    print()
    print("=" * 50)

    answer = agent.answer(
        question,
        file_name
    )

    print("ANSWER:", answer)