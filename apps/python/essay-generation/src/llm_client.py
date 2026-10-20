import aisuite as ai
import openai
from dotenv import load_dotenv

from src.exceptions import (
    LLMAuthenticationError,
    LLMError,
    LLMRateLimitError,
    LLMResponseError,
    LLMServiceError,
)


def get_provider_error(error: Exception) -> Exception:
    """Find the underlying provider exception, if available."""
    current = error
    visited: set[int] = set()

    while id(current) not in visited:
        visited.add(id(current))

        if isinstance(current, openai.OpenAIError):
            return current

        next_error = current.__cause__ or current.__context__

        if not isinstance(next_error, Exception):
            break

        current = next_error

    return error


class LLMClient:
    def __init__(self) -> None:
        load_dotenv()
        self.client = ai.Client()

    def generate(
        self,
        prompt: str,
        model: str = "openai:gpt-4o",
        temperature: float = 1.0,
    ) -> str:
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
            )

        except Exception as error:
            provider_error = get_provider_error(error)

            if isinstance(
                provider_error,
                openai.AuthenticationError | openai.PermissionDeniedError,
            ):
                raise LLMAuthenticationError(
                    "LLM authentication or permission denied"
                ) from error

            if isinstance(
                provider_error,
                openai.RateLimitError,
            ):
                raise LLMRateLimitError("LLM rate limit exceeded") from error

            if isinstance(
                provider_error,
                openai.APIConnectionError
                | openai.APITimeoutError
                | openai.InternalServerError,
            ):
                raise LLMServiceError("LLM service temporarily unavailable") from error

            raise LLMError(f"LLM generation failed: {error}") from error

        try:
            content = response.choices[0].message.content

        except (AttributeError, IndexError, TypeError) as error:
            raise LLMResponseError(
                "LLM returned an invalid response structure"
            ) from error

        if not isinstance(content, str) or not content.strip():
            raise LLMResponseError("LLM returned an empty response")

        return content
