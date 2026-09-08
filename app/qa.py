from groq import Groq
from config import GROQ_API_KEY
from embeddings import search_similar
from logger import logger

client = Groq(api_key=GROQ_API_KEY)

def answer_question(question):
    context_list = search_similar(question)
    context = " ".join(context_list)

    try:
        response = client.chat.completions.create(
            model="groq/compound-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Answer questions based only on the provided context from the user's notes."
                },
                {
                    "role": "user",
                    "content": f"Context from notes:\n{context}\n\nQuestion: {question}\n\nAnswer:"
                }
            ],
            max_tokens=300,
            temperature=0.5
        )
        answer = response.choices[0].message.content.strip()
        logger.info("Groq Q&A successful.")
        return answer

    except Exception as e:
        logger.error(f"Groq Q&A failed: {e}")
        return fallback_answer(context, question)


def fallback_answer(context, question):
    """
    Extractive fallback: return most relevant context
    """
    return (
        "⚠️ Answer extracted from notes:\n\n"
        + context[:500]
    )
