from pathlib import Path

from src.workflow import EssayResult


def save_essay_result(
    result: EssayResult,
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    files = {
        "draft.md": result.draft,
        "reflection.md": result.feedback,
        "revised.md": result.revised_draft,
    }
    for filename, content in files.items():
        file_path = output_dir / filename
        file_path.write_text(
            content,
            encoding="utf-8",
        )
