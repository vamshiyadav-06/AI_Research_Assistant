import os

from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File
from fastapi.middleware.cors import CORSMiddleware

from agent import run_agent

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

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
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