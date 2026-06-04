import pandas as pd
from ddgs import DDGS
import subprocess


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


# Read Python source code
def read_python_file(filepath):

    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as f:

        return f.read()


# Execute Python file and return output
def execute_python(filepath):

    result = subprocess.run(
        ["python", filepath],
        capture_output=True,
        text=True
    )

    return result.stdout.strip()

def calculator(expression):
    return eval(expression)

import pdfplumber

def read_pdf(filepath):

    text = ""

    with pdfplumber.open(filepath) as pdf:

        for page in pdf.pages:

            text += page.extract_text()

    return text