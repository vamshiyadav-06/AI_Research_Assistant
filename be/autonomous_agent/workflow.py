import logging
import time

from .document_generator import generate_word_document
from .executor import generate_content
from .planner import create_plan
from .reflection import reflect_on_content
from .schemas import AgentResult

logger = logging.getLogger(__name__)


def run_autonomous_agent(user_request: str) -> AgentResult:
    started_at = time.perf_counter()

    logger.info("Received autonomous agent request")

    plan = create_plan(user_request)
    logger.info("Generated execution plan: %s", plan.execution_plan)

    content = generate_content(user_request, plan)
    reflection = reflect_on_content(plan, content)
    logger.info("Reflection completed: %s", reflection.reflection)

    if reflection.needs_improvement and reflection.improvement_instructions:
        content = generate_content(
            user_request,
            plan,
            improvement_instructions=reflection.improvement_instructions,
        )

    document_path = generate_word_document(plan, content)
    logger.info("Document generated: %s", document_path)

    execution_time = f"{time.perf_counter() - started_at:.1f} sec"
    logger.info("Execution completed in %s", execution_time)

    return AgentResult(
        status="completed",
        execution_plan=plan.execution_plan,
        assumptions=plan.assumptions,
        document_type=plan.document_type,
        document_path=document_path,
        execution_time=execution_time,
        reflection=reflection.reflection,
    )
