import pytest

from src.reflection import reflect_on_draft


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

        return "The essay needs a clearer thesis statement."


def test_reflect_on_draft_returns_feedback() -> None:
    client = FakeLLMClient()

    draft = (
        "Artificial intelligence is changing education. "
        "It offers many opportunities and challenges."
    )

    result = reflect_on_draft(
        draft=draft,
        client=client,
    )

    assert result == "The essay needs a clearer thesis statement."
    assert draft in client.prompt
    assert client.model == "openai:o4-mini"
    assert client.temperature == 1.0


def test_reflect_on_draft_rejects_empty_draft() -> None:
    client = FakeLLMClient()

    with pytest.raises(ValueError, match="Essay draft cannot be empty"):
        reflect_on_draft(draft="", client=client)

    assert client.prompt == ""


def test_relect_on_draft_rejects_whitespace_draft() -> None:
    client = FakeLLMClient()

    with pytest.raises(
        ValueError,
        match="Essay draft cannot be empty",
    ):
        reflect_on_draft(
            draft="         ",
            client=client,
        )

    assert client.prompt == ""
