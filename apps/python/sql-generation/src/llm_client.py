import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_AI_KEY is not set.")

client = OpenAI(api_key=api_key)


def get_response(
    prompt: str,
    model: str = "gpt-4o-mini",
) -> str:
    try:
        response = client.responses.create(
            model=model,
            input=prompt,
        )

        print(f"called LLM model: {model}\n")

        return response.output_text.strip()
    except Exception as error:
        raise RuntimeError(f"LLM request failed: {error}") from error
