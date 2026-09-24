import os
from pathlib import Path

import requests
import streamlit as st


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "https://ai-research-assistant-gdo1.onrender.com"
)


def read_api_response(response, action):

    try:
        result = response.json()
    except ValueError:
        response_text = response.text.strip()
        st.error(
            f"{action} failed with HTTP {response.status_code}. "
            f"Server response: {response_text or 'empty response'}"
        )
        return None

    if not response.ok:
        if isinstance(result, dict):
            error_message = result.get("detail") or result.get("message")
        else:
            error_message = result

        st.error(
            f"{action} failed with HTTP {response.status_code}: "
            f"{error_message or 'unknown server error'}"
        )
        return None

    return result


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
                    },
                    timeout=120
                )

                result = read_api_response(response, "Research request")

                if result is None:
                    st.stop()

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

                result = read_api_response(response, "Document request")

                if result is not None:

                    st.success(
                        "Document generated successfully."
                    )

                    document_path = result["document_path"]
                    document_name = Path(document_path).name
                    download_response = requests.get(
                        f"{BACKEND_URL}/download-document/{document_name}",
                        timeout=60
                    )

                    if download_response.status_code == 200:

                        st.download_button(
                            label="Download Word Document",
                            data=download_response.content,
                            file_name=document_name,
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )

                    else:

                        st.warning(
                            "Document was generated, but the download endpoint could not find the file."
                        )

                    st.subheader(
                        "Document Path"
                    )

                    st.write(
                        document_path
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
