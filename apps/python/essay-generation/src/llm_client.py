import aisuite as ai
from dotenv import load_dotenv


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

            content = response.choices[0].message.content

            if not isinstance(content, str) or not content.strip():
                raise ValueError("LLM returned an empty response")

            return content

        except Exception as error:
            raise RuntimeError(f"LLM generation failed: {error}") from error
