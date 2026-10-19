from dataclasses import dataclass

from src.draft_generator import TextGenerator, generate_draft
from src.reflection import reflect_on_draft
from src.revision import revise_draft


@dataclass
class EssayResult:
    topic: str
    draft: str
    feedback: str
    revised_draft: str


def run_essay_workflow(
    topic: str,
    client: TextGenerator,
) -> EssayResult:
    if not topic.strip():
        raise ValueError("Essay topic cannot be empty")

    # Step 1. Generate the initial essay
    draft = generate_draft(
        topic=topic,
        client=client,
    )

    # Step 2. Analyze the draft
    feedback = reflect_on_draft(
        draft=draft,
        client=client,
    )

    # Step 3. Revise using the reflection
    revised_draft = revise_draft(
        original_draft=draft,
        reflection=feedback,
        client=client,
    )

    return EssayResult(
        topic=topic,
        draft=draft,
        feedback=feedback,
        revised_draft=revised_draft,
    )
