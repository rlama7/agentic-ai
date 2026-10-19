from src.llm_client import LLMClient
from src.reflection import reflect_on_draft


def main() -> None:
    draft = """
    Artificial intelligence is changing education.
    Students can use AI tools to understand difficult topics.
    Teachers can use AI to prepare lessons and provide
    personalized learning experiences.

    However, AI also creates challenges. Students may
    become too dependent on technology, and some AI
    systems can produce incorrect information.

    AI can improve education, but schools should
    consider both its benefits and risks.
    """

    try:
        client = LLMClient()

        print("Generating reflection feedback...\n")

        feedback = reflect_on_draft(
            draft=draft,
            client=client,
            model="openai:gpt-4o-mini",
        )

        print("=== REFLECTION FEEDBACK ===")
        print(feedback)

    except RuntimeError as error:
        print(f"Reflection failed: {error}")
        raise


if __name__ == "__main__":
    main()
