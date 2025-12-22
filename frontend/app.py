import streamlit as st
import requests

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

BACKEND_URL = "http://localhost:8000"

st.set_page_config(
    page_title="AI Notes Summarizer",
    page_icon="📘",
    layout="wide"
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("📘 AI Notes Summarizer")
st.sidebar.markdown("""
**Semester Project**

This application allows you to:
- Upload study notes (PDF)
- Generate AI-based summaries
- Ask questions from your notes
""")

st.sidebar.markdown("---")

uploaded_file = st.sidebar.file_uploader(
    "📂 Upload PDF Notes",
    type=["pdf"]
)

# --------------------------------------------------
# MAIN TITLE
# --------------------------------------------------

st.markdown(
    "<h1 style='text-align: center;'>AI Notes Summarizer & Q&A</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center; color: gray;'>Upload your notes, get instant summaries, and ask questions using AI</p>",
    unsafe_allow_html=True
)

st.markdown("---")

# --------------------------------------------------
# FILE UPLOAD & SUMMARY
# --------------------------------------------------

if uploaded_file:
    with st.spinner("📄 Processing document and generating summary..."):
        response = requests.post(
            f"{BACKEND_URL}/upload",
            files={"file": uploaded_file}
        )

    if response.status_code == 200:
        data = response.json()

        st.success("✅ Document processed successfully")

        st.markdown("###  Generated Summary")
        st.info(data.get("summary", "No summary available"))

    else:
        st.error("❌ Failed to process document. Check backend.")

else:
    st.warning("⬅️ Please upload a PDF from the sidebar to begin.")

# --------------------------------------------------
# QUESTION ANSWERING SECTION
# --------------------------------------------------

st.markdown("---")
st.markdown("##  Ask Questions From Notes ❓")

question = st.text_input(
    "Type your question below",
    placeholder="e.g. What is Git used for?"
)

if st.button("🔍 Get Answer"):
    if not question.strip():
        st.warning("⚠️ Please enter a question.")
    else:
        with st.spinner("🤖 Thinking..."):
            response = requests.post(
                f"{BACKEND_URL}/ask",
                params={"question": question}
            )

        if response.status_code == 200:
            answer = response.json().get("answer", "No answer returned")
            st.markdown("### 💡 Answer")
            st.success(answer)
        else:
            st.error("❌ Failed to get answer from backend.")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Built using FastAPI, Streamlit, Hugging Face & ChromaDB</p>",
    unsafe_allow_html=True
)
