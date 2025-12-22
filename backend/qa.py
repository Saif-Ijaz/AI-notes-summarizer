import requests
from config import HF_API_TOKEN
from embeddings import search_similar
from logger import logger

API_URL = "https://router.huggingface.co/hf-inference/models/google/flan-t5-large"
HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}

def answer_question(question):
    context_list = search_similar(question)
    context = " ".join(context_list)

    prompt = f"""
    Answer the question using the context below.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json={"inputs": prompt},
            timeout=45
        )

        logger.info(f"Q&A status: {response.status_code}")
        logger.info(f"Q&A raw response: {response.text}")

        # If response is empty → fallback
        if not response.text or response.text.strip() == "":
            return fallback_answer(context, question)

        result = response.json()

        if isinstance(result, dict) and "error" in result:
            return fallback_answer(context, question)

        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]

        return fallback_answer(context, question)

    except Exception as e:
        logger.error(f"Q&A failed: {e}")
        return fallback_answer(context, question)


def fallback_answer(context, question):
    """
    Extractive fallback: return most relevant context
    """
    return (
        "⚠️ Answer extracted from notes:\n\n"
        + context[:500]
    )
