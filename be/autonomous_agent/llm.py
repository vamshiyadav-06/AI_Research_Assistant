import json
import os
import re
from typing import Any, Dict, List

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

MODEL_NAME = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


class LLMError(RuntimeError):
    pass


class InvalidLLMJSONError(LLMError):
    pass


def _client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise LLMError("GROQ_API_KEY is not configured.")

    return Groq(api_key=api_key)


def call_llm(messages: List[Dict[str, str]], temperature: float = 0.2) -> str:
    response = _client().chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=temperature,
    )

    return response.choices[0].message.content.strip()


def extract_json(text: str) -> Dict[str, Any]:
    cleaned = text.strip()

    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?", "", cleaned, flags=re.IGNORECASE).strip()
        cleaned = re.sub(r"```$", "", cleaned).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)

        if not match:
            raise InvalidLLMJSONError("LLM response did not contain a JSON object.")

        try:
            return json.loads(match.group())
        except json.JSONDecodeError as exc:
            raise InvalidLLMJSONError(str(exc)) from exc


def call_json(messages: List[Dict[str, str]], temperature: float = 0.2) -> Dict[str, Any]:
    first_response = call_llm(messages, temperature=temperature)

    try:
        return extract_json(first_response)
    except InvalidLLMJSONError:
        retry_messages = messages + [
            {
                "role": "assistant",
                "content": first_response,
            },
            {
                "role": "user",
                "content": "The previous response was invalid. Return only valid JSON with no markdown.",
            },
        ]
        retry_response = call_llm(retry_messages, temperature=0)
        return extract_json(retry_response)
