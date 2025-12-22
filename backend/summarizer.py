import requests
from config import HF_API_TOKEN
from logger import logger

API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"
HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}

def summarize_text(text):
    payload = {
        "inputs": text[:2000],  # limit input size
        "parameters": {
            "max_length": 150,
            "min_length": 60
        }
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)

    logger.info(f"HF status: {response.status_code}")
    logger.info(f"HF response: {response.text}")

    try:
        result = response.json()

        if isinstance(result, dict) and "error" in result:
            return f"⚠️ {result['error']}"

        if isinstance(result, list) and "summary_text" in result[0]:
            return result[0]["summary_text"]

        return "⚠️ Summary could not be generated."

    except Exception as e:
        logger.error(e)
        return "⚠️ Hugging Face response error."
