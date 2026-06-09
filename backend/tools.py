import pandas as pd
from ddgs import DDGS
import subprocess
from pypdf import PdfReader


# Search the web
def search_web(query):

    results = []

    with DDGS() as ddgs:

        for r in ddgs.text(
            query,
            max_results=5
        ):
            results.append(r["body"])

    return "\n".join(results)


# Read Excel file
def read_excel(filepath):

    df = pd.read_excel(
        filepath,
        engine="openpyxl"
    )

    return df.to_string()

# Execute Python file and return output
def read_python_file(filepath):

    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as file:

        code = file.read()

    return code

def calculator(expression):
    return eval(expression)

import pdfplumber

def read_pdf(file_path):

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text

    return text[:10000]

def analyze_leetcode(username):

        return f"""
    Username: {username}

    LeetCode integration coming next...
    """