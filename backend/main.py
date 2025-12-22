from fastapi import FastAPI, UploadFile, File
from pypdf import PdfReader
import uuid

from summarizer import summarize_text
from embeddings import store_embeddings
from qa import answer_question
from database import notes_collection

app = FastAPI()

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    reader = PdfReader(file.file)
    text = " ".join(page.extract_text() for page in reader.pages)

    summary = summarize_text(text)
    doc_id = str(uuid.uuid4())

    store_embeddings(text, doc_id)

    notes_collection.insert_one({
        "doc_id": doc_id,
        "text": text,
        "summary": summary
    })

    return {"summary": summary}

@app.post("/ask")
async def ask(question: str):
    return {"answer": answer_question(question)}
