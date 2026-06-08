import os

import requests
import streamlit as st

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://localhost:8000"
)

st.set_page_config(
    page_title="AI Research Assistant"
)

st.title(
    "🔎 AI Research Assistant"
)

st.write(
    "Search the web, read websites, and analyze PDFs."
)

uploaded_pdf = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_pdf:

    files = {
        "file": uploaded_pdf
    }

    response = requests.post(
        f"{BACKEND_URL}/upload-pdf",
        files=files
    )

    if response.status_code == 200:

        st.success(
            "PDF Uploaded Successfully"
        )

query = st.text_area(
    "Enter your question"
)

if st.button(
    "Research"
):

    if query.strip():

        with st.spinner(
            "Researching..."
        ):

            response = requests.post(
                f"{BACKEND_URL}/ask",
                json={
                    "query": query
                }
            )

            result = response.json()

            st.subheader(
                "Tool Used"
            )

            st.write(
                result["tool_used"]
            )

            st.subheader(
                "Answer"
            )

            st.write(
                result["answer"]
            )