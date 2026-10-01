import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY is missing from the .env file")

client = OpenAI(api_key=api_key)


def get_response(model: str, prompt: str) -> str:

    response = client.responses.create(
        model=model,
        input=prompt,
    )

    return response.output_text
