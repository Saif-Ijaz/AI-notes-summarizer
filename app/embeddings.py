import os
import uuid
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# --------------------------------------------------
# 1. PROJECT ROOT & CHROMA STORAGE PATH
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_store")

# --------------------------------------------------
# 2. INITIALIZE CHROMADB (PERSISTENT MODE)
# --------------------------------------------------

client = chromadb.Client(
    settings=Settings(
        persist_directory=CHROMA_PATH
    )
)

collection = client.get_or_create_collection(name="notes")

# --------------------------------------------------
# 3. LOAD EMBEDDING MODEL
# --------------------------------------------------

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# --------------------------------------------------
# 4. CHUNKING FUNCTION
# --------------------------------------------------

def chunk_text(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks

# --------------------------------------------------
# 5. STORE EMBEDDINGS (AUTO-PERSIST)
# --------------------------------------------------

def store_embeddings(text, doc_id):
    chunks = chunk_text(text)

    for chunk in chunks:
        chunk_id = f"{doc_id}_{uuid.uuid4()}"
        embedding = model.encode(chunk).tolist()

        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            ids=[chunk_id]
        )

    print("✅ Embeddings added (ChromaDB auto-persisted)")

# --------------------------------------------------
# 6. SEARCH FUNCTION
# --------------------------------------------------

def search_similar(query, top_k=3):
    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    if results and "documents" in results:
        return results["documents"][0]

    return []
