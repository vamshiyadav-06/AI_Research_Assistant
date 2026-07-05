from .llm import call_json
from .schemas import DEFAULT_DOCUMENT_SECTIONS, PlannerOutput, SUPPORTED_DOCUMENT_TYPES


def create_plan(user_request: str) -> PlannerOutput:
    supported_types = ", ".join(sorted(SUPPORTED_DOCUMENT_TYPES))
    messages = [
        {
            "role": "system",
            "content": f"""
You are an autonomous business-document planning agent.
Choose exactly one supported document type from: {supported_types}.
Make reasonable assumptions when the request omits details.
Return only valid JSON with these keys:
document_type, assumptions, required_sections, execution_plan.
required_sections and execution_plan must be arrays of strings.
""".strip(),
        },
        {
            "role": "user",
            "content": user_request,
        },
    ]

    plan = PlannerOutput(**call_json(messages, temperature=0.1))

    if plan.document_type not in SUPPORTED_DOCUMENT_TYPES:
        plan.document_type = "Business Report"

    existing_sections = {section.lower(): section for section in plan.required_sections}
    for section in DEFAULT_DOCUMENT_SECTIONS:
        if section.lower() not in existing_sections:
            plan.required_sections.append(section)

    return plan
