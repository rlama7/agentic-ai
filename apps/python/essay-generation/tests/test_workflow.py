from src.workflow import run_essay_workflow


class FakeLLMClient:
    def __init__(self) -> None:
        self.calls: list[dict[str, str | float]] = []
        self.responses = [
            "Initial essay draft.",
            "Improve the introduction.",
            "Revised essay with better introduction.",
        ]

    def generate(
        self,
        prompt: str,
        model: str = "openai:gpt-4o",
        temperature: float = 1.0,
    ) -> str:
        self.calls.append(
            {
                "prompt": prompt,
                "model": model,
                "temperature": temperature,
            }
        )

        return self.responses[len(self.calls) - 1]


def test_workflow_executes_all_three_stages() -> None:
    client = FakeLLMClient()

    result = run_essay_workflow(
        topic="AI in Education",
        client=client,
    )

    assert result.topic == "AI in Education"
    assert result.draft == "Initial essay draft."
    assert result.feedback == "Improve the introduction."
    assert result.revised_draft == ("Revised essay with better introduction.")

    assert len(client.calls) == 3

    # Draft stage receives the topic
    assert "AI in Education" in client.calls[0]["prompt"]

    # Reflection stage receives the draft
    assert "Initial essay draft." in client.calls[1]["prompt"]

    # Revision receives both the draft and feedback
    assert "Initial essay draft." in client.calls[2]["prompt"]
    assert "Improve the introduction." in client.calls[2]["prompt"]

    # Verify model selection and execution order
    assert [call["model"] for call in client.calls] == [
        "openai:gpt-4o",
        "openai:o4-mini",
        "openai:gpt-4o",
    ]
