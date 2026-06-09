from tools import (
    search_web,
    read_excel,
    read_python_file,
    calculator,
    read_pdf,
    analyze_leetcode
)

from groq import Groq
from dotenv import load_dotenv
import os
import re

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

SYSTEM_PROMPT = """
You are answering questions.

Rules:
- Return ONLY the answer.
- No explanations.
- No reasoning.
"""


def choose_tool(question, file_name):

    if file_name:

        if file_name.endswith(".xlsx"):
            return (
                "excel",
                "An Excel file was provided."
            )

        if file_name.endswith(".py"):
            return (
                "python",
                "A Python file was provided."
            )
        if file_name.endswith(".pdf"):
            return (
                "pdf",
                "A PDF file was provided."
            )

    if any(
        op in question
        for op in ["+", "-", "*", "/"]
    ):
        return (
            "calculator",
            "Math operators detected."
        )

    return (
        "web",
        "Using web search."
    )

def choose_tool_with_llm(question, file_name = None):

    prompt = f"""
You are a tool selector.

Available tools:

calculator
excel
python
pdf
web
leetcode
chat

Rules:

- Use calculator ONLY for math calculations.
Examples:
2+2
10*5
calculate 100/4

- Use excel when an Excel file is uploaded.

- Use python when a Python file is uploaded.

- Use pdf when a PDF file is uploaded.

- Use web for current events, news, latest information,
weather, sports, world updates.

- Use leetcode when the user asks about a LeetCode profile,
LeetCode statistics, coding profile analysis, contest rating,
or DSA roadmap based on LeetCode.

- Use chat for normal conversation, follow-up questions,
greetings, explanations, elaborations, and anything that
does not require a tool.

Question:
{question}

Uploaded File:
{file_name}

Return ONLY one word:

calculator
excel
python
pdf
web
leetcode
chat
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return (
        response
        .choices[0]
        .message
        .content
        .strip()
        .lower()
    )

class Agent:

    def answer(self, question, file_name=None):

        if re.fullmatch(r"[0-9+\-*/(). ]+", question):
            tool = "calculator"
        else:
            tool = choose_tool_with_llm(
                question,
                file_name
            )

        reason = f"Chosen by LLM: {tool}"

        print("Using tool:", tool)
        print("File received:", file_name)

        # Calculator
        if tool == "calculator":

            try:
                answer = str(
                    calculator(question)
                )

                return {
                    "tool": tool,
                    "reason": reason,
                    "answer": answer
                }

            except Exception:

                tool = "chat"

        file_context = ""
        web_context = ""

        # Excel
        if tool == "excel":

            file_context = read_excel(
                file_name
            )

        # Python
        elif tool == "python":

            file_context = read_python_file(
                file_name
            )

            print("PYTHON CONTENT:")
            print(file_context)

        # Web
        elif tool == "web":

            web_context = search_web(
                question
            )
        elif tool == "pdf":

            file_context = read_pdf(
                file_name
            )
        elif tool == "leetcode":

            words = question.split()

            username = words[-1]

            answer = analyze_leetcode(
                username
            )

            return {
                "tool": tool,
                "reason": reason,
                "answer": answer
            }
        elif tool == "chat":
            pass

        # Reverse text support
        if question.startswith("."):

            question = question[::-1]

        prompt = f"""
Question:
{question}

File Content:
{file_context}

Web Search Results:
{web_context}

Use the information provided.

Return ONLY the final answer.
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        answer = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

        return {
            "tool": tool,
            "reason": reason,
            "answer": answer
        }