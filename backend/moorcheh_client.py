import os
from moorcheh_sdk import MoorchehClient


MOORCHEH_API_KEY = os.getenv("MOORCHEH_API_KEY")
MOORCHEH_BASE_URL = "https://api.moorcheh.ai/v1"
MOORCHEH_NAMESPACE = "teacher-aide-memory-demo"


def get_moorcheh_client():
    if not MOORCHEH_API_KEY:
        raise ValueError("MOORCHEH_API_KEY is not set in environment variables.")

    client = MoorchehClient(
        api_key=MOORCHEH_API_KEY,
        base_url=MOORCHEH_BASE_URL
    )
    return client
