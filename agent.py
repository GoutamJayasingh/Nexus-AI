from tools import (
    search_web,
    read_excel,
    execute_python,
    calculator,
    read_pdf
)

from groq import Groq
from dotenv import load_dotenv
import os

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

        tool = choose_tool_with_llm(
        question,
        file_name
    )

        reason = f"Chosen by LLM: {tool}"

        print("Using tool:", tool)

        # Calculator
        if tool == "calculator":

            answer = str(
                calculator(question)
            )

            return {
                "tool": tool,
                "reason": reason,
                "answer": answer
            }

        file_context = ""
        web_context = ""

        # Excel
        if tool == "excel":

            file_context = read_excel(
                file_name
            )

        # Python
        elif tool == "python":

            file_context = execute_python(
                file_name
            )

        # Web
        elif tool == "web":

            web_context = search_web(
                question
            )
        elif tool == "pdf":

            file_context = read_pdf(
                file_name
            )

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