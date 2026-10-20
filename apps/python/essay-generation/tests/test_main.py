from pathlib import Path

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


def test_main_saves_workflow_results(
    tmp_path: Path,
) -> None:
    client = FakeLLMClient()

    result = main(
        topic="AI in Education",
        client=client,
        save_output=True,
        output_dir=tmp_path,
    )

    # Exactly one run directory should be created
    run_directories = list(tmp_path.iterdir())

    assert len(run_directories) == 1

    run_dir = run_directories[0]

    assert run_dir.is_dir()

    # Verify all three outputs were saved
    assert (run_dir / "draft.md").read_text(
        encoding="utf-8",
    ) == result.draft

    assert (run_dir / "reflection.md").read_text(
        encoding="utf-8",
    ) == result.feedback

    assert (run_dir / "revised.md").read_text(
        encoding="utf-8",
    ) == result.revised_draft

    assert client.calls == 3
