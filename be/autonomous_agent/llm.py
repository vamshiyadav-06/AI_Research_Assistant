import json
import os
import re
from typing import Any, Dict, List

from dotenv import load_dotenv
from groq import Groq, GroqError

load_dotenv()

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


def get_model_names() -> List[str]:

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
    last_error = None

    for model_name in get_model_names():
        try:
            response = _client().chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=temperature,
            )
            return response.choices[0].message.content.strip()
        except GroqError as exc:
            last_error = exc

    raise LLMError(
        f"All configured Groq models failed. Last error: {last_error}"
    ) from last_error


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
