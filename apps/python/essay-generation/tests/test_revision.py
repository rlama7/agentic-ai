from src.revision import revise_draft


class FakeLLMClient:
    def __init__(self) -> None:
        self.prompt = ""
        self.model = ""
        self.temperature = 0.0

    def generate(
        self,
        prompt: str,
        model: str = "openai:gpt-4o",
        temperature: float = 1.0,
    ) -> str:
        self.prompt = prompt
        self.model = model
        self.temperature = temperature

        return "This is the improved essay."


def test_revise_draft_returns_revised_essay() -> None:
    client = FakeLLMClient()

    original_draft = "AI is changing education."
    reflection = "Add examples and improve clarity."

    result = revise_draft(
        original_draft=original_draft,
        reflection=reflection,
        client=client,
    )

    assert result == "This is the improved essay."
    assert original_draft in client.prompt
    assert reflection in client.prompt
    assert client.model == "openai:gpt-4o"
    assert client.temperature == 1.0
