import os
import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi import File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from agent import run_agent
from autonomous_agent import run_autonomous_agent
from autonomous_agent.llm import InvalidLLMJSONError, LLMError
from autonomous_agent.schemas import AgentError, AgentRequest, AgentResult

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Research Assistant"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
GENERATED_DOCS_FOLDER = "generated_docs"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)
os.makedirs(
    GENERATED_DOCS_FOLDER,
    exist_ok=True
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request,
    exc: RequestValidationError
):

    return JSONResponse(
        status_code=400,
        content={
            "status": "error",
            "message": "Invalid request input.",
            "details": {
                "error": str(exc)
            }
        }
    )


@app.get("/")
def home():

    return {
        "message": "AI Research Assistant Running"
    }


@app.post("/upload-pdf")
async def upload_pdf(
    file: UploadFile = File(...)
):

    path = f"{UPLOAD_FOLDER}/latest.pdf"

    with open(path, "wb") as pdf_file:

        pdf_file.write(
            await file.read()
        )

    return {
        "message": "PDF Uploaded Successfully"
    }


@app.post("/ask")
async def ask(
    payload: dict
):

    query = payload.get(
        "query",
        ""
    )

    result = run_agent(query)

    return result


@app.post("/agent", response_model=AgentResult)
async def agent(
    payload: AgentRequest
):

    request_text = payload.request.strip()

    if len(request_text) < 5:
        raise HTTPException(
            status_code=400,
            detail="Request must contain at least 5 characters."
        )

    try:
        return run_autonomous_agent(request_text)
    except InvalidLLMJSONError as exc:
        logger.exception("Planner or generator returned invalid JSON")
        raise HTTPException(
            status_code=502,
            detail=AgentError(
                message="The LLM returned invalid JSON after retry.",
                details={"error": str(exc)}
            ).dict()
        )
    except LLMError as exc:
        logger.exception("LLM configuration or execution failed")
        raise HTTPException(
            status_code=500,
            detail=AgentError(
                message=str(exc)
            ).dict()
        )
    except ValidationError as exc:
        logger.exception("LLM response did not match the expected schema")
        raise HTTPException(
            status_code=502,
            detail=AgentError(
                message="The LLM response did not match the expected agent schema.",
                details={"error": str(exc)}
            ).dict()
        )


@app.get("/download-document/{filename}")
async def download_document(
    filename: str
):

    safe_filename = Path(filename).name
    file_path = Path(GENERATED_DOCS_FOLDER) / safe_filename

    if safe_filename != filename or not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    return FileResponse(
        path=file_path,
        filename=safe_filename,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
