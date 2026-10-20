from src.draft_generator import TextGenerator
from src.llm_client import LLMClient
from src.workflow import EssayResult, run_essay_workflow

DEFAULT_TOPIC = "The impact of artificial intelligence on education"


def main(
    topic: str = DEFAULT_TOPIC, client: TextGenerator | None = None
) -> EssayResult:
    if client is None:
        client = LLMClient()
    return run_essay_workflow(topic=topic, client=client)


if __name__ == "__main__":
    try:
        result = main()
        print("\n=== ORIGINAL DRAFT ===")
        print(result.draft)

        print("\n=== REFLECTION FEEDBACK ===")
        print(result.feedback)

        print("\n=== REVISED DRAFT ===")
        print(result.revised_draft)
    except (RuntimeError, ValueError) as error:
        print(f"Essay workflow failed: ${error}")
        raise
