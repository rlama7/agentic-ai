from pathlib import Path

from src.draft_generator import TextGenerator
from src.llm_client import LLMClient
from src.output_manager import create_run_directory, save_essay_result
from src.workflow import EssayResult, run_essay_workflow

DEFAULT_TOPIC = "The impact of artificial intelligence on education"
DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"


def main(
    topic: str = DEFAULT_TOPIC,
    client: TextGenerator | None = None,
    save_output: bool = False,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> EssayResult:
    if client is None:
        client = LLMClient()

    result = run_essay_workflow(topic=topic, client=client)

    if save_output:
        run_dir = create_run_directory(output_dir)

        save_essay_result(result=result, output_dir=run_dir)

        print(f"\nEssay files saved to: {run_dir}")

    return result


if __name__ == "__main__":
    try:
        result = main(save_output=True)
        print("\n=== ORIGINAL DRAFT ===")
        print(result.draft)

        print("\n=== REFLECTION FEEDBACK ===")
        print(result.feedback)

        print("\n=== REVISED DRAFT ===")
        print(result.revised_draft)
    except (RuntimeError, ValueError) as error:
        print(f"Essay workflow failed: ${error}")
        raise
