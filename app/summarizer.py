from groq import Groq
from config import GROQ_API_KEY
from logger import logger

client = Groq(api_key=GROQ_API_KEY)

def summarize_text(text):
    try:
        response = client.chat.completions.create(
            model="groq/compound-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes notes clearly and concisely."
                },
                {
                    "role": "user",
                    "content": f"Please summarize the following text in 3-5 sentences:\n\n{text[:3000]}"
                }
            ],
            max_tokens=300,
            temperature=0.5
        )
        summary = response.choices[0].message.content.strip()
        logger.info("Groq summarization successful.")
        return summary

    except Exception as e:
        logger.error(f"Groq summarizer error: {e}")
        return "⚠️ Summary could not be generated."
