from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from src.workflow import EssayResult


def create_run_directory(base_dir: Path) -> Path:
    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")

    run_id = uuid4().hex[:8]
    run_dir = base_dir / f"{timestamp}_{run_id}"

    run_dir.mkdir(
        parents=True,
        exist_ok=False,
    )

    return run_dir


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
