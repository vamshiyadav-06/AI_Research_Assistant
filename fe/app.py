import os

import requests
import streamlit as st


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "https://ai-research-assistant-gdo1.onrender.com"
)

st.set_page_config(
    page_title="AI Research Assistant"
)

st.title(
    "AI Research Assistant"
)

st.write(
    "Search the web, read websites, analyze PDFs, and generate business documents."
)

research_tab, document_tab = st.tabs(
    [
        "Research",
        "Document Agent"
    ]
)

with research_tab:

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

with document_tab:

    document_request = st.text_area(
        "Describe the document you want",
        value="Prepare a business proposal for implementing AI customer support. No budget is available. Timeline is unknown. Decide reasonable assumptions yourself."
    )

    if st.button(
        "Generate Document"
    ):

        if document_request.strip():

            with st.spinner(
                "Planning, writing, reviewing, and creating the Word document..."
            ):

                response = requests.post(
                    f"{BACKEND_URL}/agent",
                    json={
                        "request": document_request
                    },
                    timeout=120
                )

                result = response.json()

                if response.status_code == 200:

                    st.success(
                        "Document generated successfully."
                    )

                    st.subheader(
                        "Document Path"
                    )

                    st.write(
                        result["document_path"]
                    )

                    st.subheader(
                        "Execution Plan"
                    )

                    st.write(
                        result["execution_plan"]
                    )

                    st.subheader(
                        "Assumptions"
                    )

                    st.write(
                        result["assumptions"]
                    )

                    st.subheader(
                        "Reflection"
                    )

                    st.write(
                        result["reflection"]
                    )

                else:

                    st.error(
                        result
                    )
