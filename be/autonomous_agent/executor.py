from typing import Optional

from .llm import call_json
from .schemas import ExecutorOutput, PlannerOutput


def generate_content(
    user_request: str,
    plan: PlannerOutput,
    improvement_instructions: Optional[str] = None,
) -> ExecutorOutput:
    feedback = ""

    if improvement_instructions:
        feedback = f"\nAddress this reflection feedback: {improvement_instructions}"

    messages = [
        {
            "role": "system",
            "content": """
You are a senior business writer and AI implementation consultant.
Generate complete, professional content for each requested section.
Use a concise business tone with actionable detail.
Return only valid JSON with:
title: string
sections: array of objects with heading and content.
Do not omit any required section.
""".strip(),
        },
        {
            "role": "user",
            "content": f"""
User request:
{user_request}

Document type:
{plan.document_type}

Assumptions:
{plan.assumptions}

Required sections:
{plan.required_sections}
{feedback}
""".strip(),
        },
    ]

    return ExecutorOutput(**call_json(messages, temperature=0.3))
