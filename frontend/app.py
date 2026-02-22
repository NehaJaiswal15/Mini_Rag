import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Personal Knowledge Assistant",
    page_icon="📄",
    layout="centered"
)

st.title("Personal Knowledge Assistant")
st.caption("Ask questions from your own documents using AI")

st.divider()

st.subheader("Upload document")

uploaded_file = st.file_uploader(
    "Select a PDF file",
    type=["pdf"],
    label_visibility="collapsed"
)

if uploaded_file:
    col1, col2 = st.columns([1, 3])

    with col1:
        upload_clicked = st.button("Upload")

    if upload_clicked:
        files = {
            "file": (uploaded_file.name, uploaded_file, "application/pdf")
        }

        with st.spinner("Uploading file..."):
            response = requests.post(
                f"{BACKEND_URL}/upload",
                files=files
            )

        if response.status_code == 200:
            st.success("File uploaded successfully")
            st.session_state["filename"] = uploaded_file.name
        else:
            st.error("Upload failed")

if "filename" in st.session_state:
    st.divider()
    st.subheader("Prepare document")

    st.write(
        f"**Selected file:** `{st.session_state['filename']}`"
    )

    if st.button("Create embeddings"):
        with st.spinner("Processing document..."):
            response = requests.post(
                f"{BACKEND_URL}/index/{st.session_state['filename']}"
            )

        if response.status_code == 200:
            st.success("Document indexed and ready for questions")
            st.session_state["indexed"] = True
        else:
            st.error("Indexing failed")

if st.session_state.get("indexed"):
    st.divider()
    st.subheader("Ask a question")

    question = st.text_input(
        "Enter your question",
        placeholder="e.g. What is this document about?"
    )

    if st.button("Ask"):
        if not question.strip():
            st.warning("Please enter a question")
        else:
            with st.spinner("Thinking..."):
                response = requests.post(
                    f"{BACKEND_URL}/ask",
                    params={"question": question}
                )

            if response.status_code == 200:
                answer = response.json()["answer"]

                st.markdown("**Answer**")
                st.write(answer)
            else:
                st.error("Failed to get answer")
st.divider()
st.caption(
    "Built with FastAPI, ChromaDB, OpenAI, and Streamlit"
)