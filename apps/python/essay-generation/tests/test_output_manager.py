from pathlib import Path

import pytest

from src.output_manager import save_essay_result
from src.workflow import EssayResult


def test_save_result(tmp_path: Path) -> None:
    result = EssayResult(
        topic="AI in Education",
        draft="Initial essay draft.",
        feedback="Improve the introduction.",
        revised_draft="Improved essay.",
    )
    output_dir = tmp_path / "essay_output"
    save_essay_result(
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


def test_save_result_overwrites_existing_files(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "essay_output"
    output_dir.mkdir()

    # Create an Existing draft file
    draft_path = output_dir / "draft.md"
    draft_path.write_text(
        "Old essay draft.",
        encoding="utf-8",
    )
    result = EssayResult(
        topic="AI in Education",
        draft="New essay draft.",
        feedback="Improve clarity.",
        revised_draft="Improved essay.",
    )
    save_essay_result(
        result=result,
        output_dir=output_dir,
    )
    assert (
        draft_path.read_text(
            encoding="utf-8",
        )
        == "New essay draft."
    )


def test_save_result_rejects_file_as_directory(
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "essay_output"

    # Create a file instead of a directory
    output_path.write_text(
        "Existing file.",
        encoding="utf-8",
    )
    result = EssayResult(
        topic="AI in Education.",
        draft="Initial draft.",
        feedback="Improve structure.",
        revised_draft="Revised draft.",
    )
    with pytest.raises(OSError):
        save_essay_result(
            result=result,
            output_dir=output_path,
        )

    # Existin file should remain unchanged
    assert (
        output_path.read_text(
            encoding="utf-8",
        )
        == "Existing file."
    )


def test_save_result_preserves_unicode(
    tmp_path: Path,
) -> None:
    result = EssayResult(
        topic="Multilingual Education",
        draft="Education connects culture. शिक्षा",
        feedback="Improve clarity. 日本語",
        revised_draft="Learning across cultures. 🌍",
    )
    output_dir = tmp_path / "unicode_output"

    save_essay_result(
        result=result,
        output_dir=output_dir,
    )

    assert (output_dir / "draft.md").read_text(
        encoding="utf-8",
    ) == result.draft

    assert (output_dir / "reflection.md").read_text(
        encoding="utf-8",
    ) == result.feedback

    assert (output_dir / "revised.md").read_text(
        encoding="utf-8",
    ) == result.revised_draft
