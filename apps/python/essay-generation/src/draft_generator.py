from typing import Protocol


class TextGenerator(Protocol):
    def generate(
        self,
        prompt: str,
        model: str = "openai:gpt-4o",
        temperature: float = 1.0,
    ) -> str: ...


def generate_draft(
    topic: str,
    client: TextGenerator,
    model: str = "openai:gpt-4o",
) -> str:
    if not topic.strip():
        raise ValueError("Essay topic cannot be empty")
    prompt = f"""
		Write a well-structured, informative essay about the following topic:

		Topic: {topic}

		Requirements:
		- Include an introduction, body, and conclusion.
		- Present clear arguments and supporting explanations.
		- Maintain a professional and engaging tone.
		- Use coherent paragraphs and logical transitions.
		- Aim for approximately 400 words.

		Return only the essay withou additional commentary.
		"""
    return client.generate(
        prompt=prompt,
        model=model,
        temperature=1.0,
    )
