from pathlib import Path

from src.output_manager import save_ssay_result
from src.workflow import EssayResult


def test_save_result(tmp_path: Path) -> None:
    result = EssayResult(
        topic="AI in Education",
        draft="Initial essay draft.",
        feedback="Improve the introduction.",
        revised_draft="Improved essay.",
    )
    output_dir = tmp_path / "essay_output"
    save_ssay_result(
        result=result,
        output_dir=output_dir,
    )
    assert (output_dir / "draft.md").read_text(
        encoding="utf-8"
    ) == "Initial essay draft."
    assert (output_dir / "reflection.md").read_text(
        encoding="utf-8"
    ) == "Improve the introduction."
    assert (output_dir / "revised.md").read_text(encoding="utf-8") == "Improved essay."
