import os
import re
import logging

from dotenv import load_dotenv
from groq import Groq, GroqError

from tools.web_search import search_web
from tools.website_reader import read_website
from tools.pdf_reader import read_pdf

load_dotenv()

logger = logging.getLogger(__name__)

DEFAULT_MODELS = [
    "openai/gpt-oss-120b",
    "qwen/qwen3.8-27b",
    "openai/gpt-oss-20b",
    "allam-2-7b",
    "openai/gpt-oss-safeguard-20b",
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "deepseek-r1-distill-llama-70b",
    "moonshotai/kimi-k2-instruct",
]


def get_model_names():

    configured_models = os.getenv("GROQ_MODELS")

    if configured_models:
        return [
            model.strip()
            for model in configured_models.split(",")
            if model.strip()
        ]

    legacy_model = os.getenv("GROQ_MODEL")

    if legacy_model:
        return [legacy_model] + [
            model
            for model in DEFAULT_MODELS
            if model != legacy_model
        ]

    return DEFAULT_MODELS


def call_completion(messages, temperature=0):

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not configured.")

    client = Groq(api_key=api_key)
    last_error = None

    for model_name in get_model_names():
        try:
            return client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=temperature
            )
        except GroqError as exc:
            last_error = exc
            logger.warning("Groq model %s failed: %s", model_name, exc)

    raise RuntimeError(
        f"All configured Groq models failed. Last error: {last_error}"
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

    response = call_completion(
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

    response = call_completion(
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