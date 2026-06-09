import pandas as pd
from ddgs import DDGS
import subprocess
from pypdf import PdfReader
import requests

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

    url = "https://leetcode.com/graphql"

    query = """
    query getUserProfile($username: String!) {
      matchedUser(username: $username) {
        username

        submitStats {
          acSubmissionNum {
            difficulty
            count
          }
        }
      }
    }
    """

    response = requests.post(
        url,
        json={
            "query": query,
            "variables": {
                "username": username
            }
        }
    )

    data = response.json()

    stats = (
        data["data"]
        ["matchedUser"]
        ["submitStats"]
        ["acSubmissionNum"]
    )

    total = stats[0]["count"]
    easy = stats[1]["count"]
    medium = stats[2]["count"]
    hard = stats[3]["count"]

    return f"""
Username: {username}

Total Solved: {total}
Easy: {easy}
Medium: {medium}
Hard: {hard}
"""