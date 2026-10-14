import pytest

from src.draft_generator import generate_draft


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

        return "This is a generated essay draft."


def test_generate_draft_returns_essay() -> None:
    client = FakeLLMClient()

    result = generate_draft(
        topic="Artificial Intelligence in Education",
        client=client,
    )

    assert result == "This is a generated essay draft."


def test_generate_draft_includes_topic() -> None:
    client = FakeLLMClient()

    generate_draft(
        topic="Climate Change",
        client=client,
    )

    assert "Climate Change" in client.prompt


def test_generate_draft_uses_default_model() -> None:
    client = FakeLLMClient()

    generate_draft(
        topic="Artificial Intelligence",
        client=client,
    )

    assert client.model == "openai:gpt-4o"
    assert client.temperature == 1.0


def test_generate_draft_rejects_empty_topic() -> None:
    client = FakeLLMClient()

    with pytest.raises(ValueError):
        generate_draft(
            topic="   ",
            client=client,
        )

    assert client.prompt == ""
