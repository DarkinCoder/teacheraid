import os
from openai import OpenAI


DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"


def get_deepseek_client():
    if not DEEPSEEK_API_KEY:
        raise ValueError("DEEPSEEK_API_KEY is not set in environment variables.")

    return OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL,
    )
