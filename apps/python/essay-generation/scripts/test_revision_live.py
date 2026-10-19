from src.llm_client import LLMClient
from src.reflection import reflect_on_draft
from src.revision import revise_draft


def main() -> None:
    original_draft = """
		Artificial intelligence is changing education.
		Students can use AI tools to understand difficult topics.
		Teachers can use AI to perpare lessons and provide
		personalized learning experiences.

		However, AI also creates challenges. Students may
		become too dependent on technology, and some AI
		systems can produce incorrect information.

		AI can improve education, but schools should
		consider both its benefits and risks.
	"""

    try:
        client = LLMClient()

        # Step 1: Generate reflection feedback
        print("Generating reflection feedback...\n")

        feedback = reflect_on_draft(
            draft=original_draft,
            client=client,
            model="openai:o4-mini",
        )

        # Step 2: Revise the original essay
        print("Revising essay using feedback...\n")

        revised_draft = revise_draft(
            original_draft=original_draft,
            reflection=feedback,
            client=client,
            model="openai:gpt-4o",
        )

        # Step 3: Display the results
        print("=== ORIGINAL DRAFT ===")
        print(original_draft)

        print("\n=== REFELECTION FEEDBACK ===")
        print(feedback)

        print("\n=== REVISED DRAFT ===")
        print(revised_draft)

    except RuntimeError as error:
        print(f"Essay revision failed: {error}")
        raise


if __name__ == "__main__":
    main()
