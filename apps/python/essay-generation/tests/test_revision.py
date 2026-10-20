import pytest

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


def test_revise_draft_rejects_empty_draft() -> None:
    client = FakeLLMClient()
    with pytest.raises(
        ValueError,
        match="Original draft cannot be empty",
    ):
        revise_draft(
            original_draft="",
            reflection="Improve the introductionc.",
            client=client,
        )
        assert client.prompt == ""


def test_revise_draft_rejects_empty_reflection() -> None:
    client = FakeLLMClient()
    with pytest.raises(
        ValueError,
        match="Reflection feedback cannot be empty",
    ):
        revise_draft(
            original_draft="AI is transforming education.",
            reflection="         ",
            client=client,
        )
        assert client.prompt == ""


def test_revise_draft_uses_custom_model() -> None:
    client = FakeLLMClient()
    result = revise_draft(
        original_draft="AI is changing education.",
        reflection="Improve clarity and flow.",
        client=client,
        model="openai:gpt-4o-mini",
    )
    assert result == "This is the improved essay."
    assert client.model == "openai:gpt-4o-mini"
    assert client.temperature == 1.0
