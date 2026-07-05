from .llm import call_json
from .schemas import ExecutorOutput, PlannerOutput, ReflectionOutput


def reflect_on_content(plan: PlannerOutput, content: ExecutorOutput) -> ReflectionOutput:
    messages = [
        {
            "role": "system",
            "content": """
You are a strict document quality reviewer.
Review for grammar, missing sections, business tone, logical consistency, and formatting readiness.
Return only valid JSON with:
needs_improvement: boolean
reflection: string
improvement_instructions: string or null
Use needs_improvement=false when there are no critical issues.
""".strip(),
        },
        {
            "role": "user",
            "content": f"""
Required sections:
{plan.required_sections}

Generated content:
{content.dict()}
""".strip(),
        },
    ]

    return ReflectionOutput(**call_json(messages, temperature=0))
