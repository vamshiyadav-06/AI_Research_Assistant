import os
import re

from dotenv import load_dotenv
from groq import Groq

from tools.web_search import search_web
from tools.website_reader import read_website
from tools.pdf_reader import read_pdf

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL_NAME = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-120b"
)

PDF_PATH = "uploads/latest.pdf"


def choose_tool(query):

    prompt = f"""
You are a tool-selection agent.

Available Tools:

1. web_search
   Use when user needs latest information,
   news, facts, research.

2. website_reader
   Use when user provides a URL.

3. pdf_reader
   Use when user asks about an uploaded PDF.

Return ONLY one of:

web_search
website_reader
pdf_reader

Query:
{query}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()


def run_agent(query):

    tool = choose_tool(query)

    context = ""

    if tool == "website_reader":

        url_match = re.search(
            r"https?://\S+",
            query
        )

        if not url_match:
            return {
                "tool_used": tool,
                "answer": "No URL found."
            }

        url = url_match.group()

        context = read_website(url)

    elif tool == "pdf_reader":

        if not os.path.exists(PDF_PATH):

            return {
                "tool_used": tool,
                "answer": "Please upload a PDF first."
            }

        context = read_pdf(PDF_PATH)

    else:

        tool = "web_search"

        context = search_web(query)

    final_prompt = f"""
You are an AI Research Assistant.

User Query:
{query}

Tool Used:
{tool}

Tool Result:
{context}

Generate a clear,
well-structured answer.
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": final_prompt
            }
        ]
    )

    return {
        "tool_used": tool,
        "answer": response.choices[0].message.content
    }