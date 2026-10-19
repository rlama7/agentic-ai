from src.draft_generator import TextGenerator


def revise_draft(
    original_draft: str,
    reflection: str,
    client: TextGenerator,
    model: str = "openai:gpt-4o",
) -> str:
    if not original_draft.strip():
        raise ValueError("Original draft cannot be empty")

    if not reflection.strip():
        raise ValueError("Reflection feedback cannot be empty")

    prompt = f"""
    You are an experienced essay writer and editor.

    Revise the original essay using the constructive
    feedback provided below.

    Revision requirements:
    1. Address the issues identified in the reflection.
    2. Improve structure and logical organization.
    3. Strengthen arguments with clear explanations.
    4. Improve clarity, coherence, and transitions.
    5. Maintain a professional writing style.
    6. Preserve the original topic and key ideas.
    7. Do not invent statistics, studies, or citations.
    8. Use only evidence already present in the draft,
       unless additional verified sources are provided.

    Original Essay:
    {original_draft}

    Reflection Feedback:
    {reflection}

    Return only the complete revised essay.
    Do not include additional commentary.
    """

    return client.generate(
        prompt=prompt,
        model=model,
        temperature=1.0,
    )
