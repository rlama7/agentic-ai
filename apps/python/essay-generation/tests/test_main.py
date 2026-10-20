from src.main import main
from src.workflow import EssayResult


class FakeLLMClient:
    def __init__(self) -> None:
        self.responses = iter(
            [
                "Initial essay draft.",
                "Improve the introduction.",
                "Revised essay.",
            ]
        )
        self.calls = 0

    def generate(
        self, prompt: str, model: str = "openai:gpt-4o", temperature: float = 1.0
    ) -> str:
        self.calls += 1
        return next(self.responses)


def test_main_executes_workflow() -> None:
    client = FakeLLMClient()

    result = main(
        topic="AI in Education",
        client=client,
    )
    assert isinstance(result, EssayResult)
    assert result.topic == "AI in Education"
    assert result.draft == "Initial essay draft."
    assert result.feedback == "Improve the introduction."
    assert result.revised_draft == "Revised essay."
    assert client.calls == 3
