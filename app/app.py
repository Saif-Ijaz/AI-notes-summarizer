import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from pypdf import PdfReader
import uuid

from summarizer import summarize_text
from embeddings import store_embeddings
from qa import answer_question
from database import notes_collection

st.set_page_config(page_title="AI Notes Summarizer", page_icon="📘", layout="wide")

st.sidebar.title("📘 AI Notes Summarizer")
st.sidebar.markdown("""
**Semester Project**

This application allows you to:
- Upload study notes (PDF)
- Generate AI-based summaries
- Ask questions from your notes
""")
st.sidebar.markdown("---")
uploaded_file = st.sidebar.file_uploader("📂 Upload PDF Notes", type=["pdf"])

st.markdown("<h1 style='text-align: center;'>AI Notes Summarizer &amp; Q&amp;A</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Upload your notes, get instant summaries, and ask questions using AI</p>", unsafe_allow_html=True)
st.markdown("---")

if uploaded_file:
    with st.spinner("📄 Processing document and generating summary..."):
        reader = PdfReader(uploaded_file)
        text = " ".join(page.extract_text() for page in reader.pages if page.extract_text())
        doc_id = str(uuid.uuid4())
        store_embeddings(text, doc_id)
        try:
            notes_collection.insert_one({"doc_id": doc_id, "text": text})
        except Exception as e:
            st.warning(f"MongoDB: {e}")
        summary = summarize_text(text)

    st.success("✅ Document processed successfully")
    st.markdown("### 📝 Generated Summary")
    if summary.startswith("⚠️"):
        st.error(summary)
    else:
        st.info(summary)
else:
    st.warning("⬅️ Please upload a PDF from the sidebar to begin.")

st.markdown("---")
st.markdown("## 💡 Ask Questions From Notes ❓")
question = st.text_input("Type your question below", placeholder="e.g. What is the main topic?")

if st.button("🔍 Get Answer"):
    if not question.strip():
        st.warning("⚠️ Please enter a question.")
    else:
        with st.spinner("🤖 Thinking..."):
            answer = answer_question(question)
        st.markdown("### 💡 Answer")
        if answer.startswith("⚠️"):
            st.error(answer)
        else:
            st.success(answer)

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Built using Streamlit, Groq AI, ChromaDB &amp; MongoDB</p>", unsafe_allow_html=True)
