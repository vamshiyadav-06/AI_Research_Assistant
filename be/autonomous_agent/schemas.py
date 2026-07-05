from typing import Dict, List, Optional

from pydantic import BaseModel, Field


SUPPORTED_DOCUMENT_TYPES = {
    "Business Proposal",
    "Meeting Minutes",
    "Project Plan",
    "Technical Design",
    "Business Report",
    "SOP",
    "Product Specification",
    "Research Summary",
    "Implementation Plan",
}

DEFAULT_DOCUMENT_SECTIONS = [
    "Executive Summary",
    "Objectives",
    "Scope",
    "Implementation Plan",
    "Timeline",
    "Risks",
    "Recommendations",
    "Conclusion",
]


class AgentRequest(BaseModel):
    request: str = Field(...)


class PlannerOutput(BaseModel):
    document_type: str
    assumptions: List[str]
    required_sections: List[str]
    execution_plan: List[str]


class SectionContent(BaseModel):
    heading: str
    content: str


class ExecutorOutput(BaseModel):
    title: str
    sections: List[SectionContent]


class ReflectionOutput(BaseModel):
    needs_improvement: bool = False
    reflection: str = "No critical issues found."
    improvement_instructions: Optional[str] = None


class AgentResult(BaseModel):
    status: str
    execution_plan: List[str]
    assumptions: List[str]
    document_type: str
    document_path: str
    execution_time: str
    reflection: str


class AgentError(BaseModel):
    status: str = "error"
    message: str
    details: Optional[Dict[str, str]] = None
