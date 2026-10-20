from src.draft_generator import TextGenerator


def reflect_on_draft(
    draft: str,
    client: TextGenerator,
    model: str = "openai:o4-mini",
) -> str:
    if not draft.strip():
        raise ValueError("Essay draft cannot be empty")

    prompt = f"""
    You are an experienced essay editor and critical reviewer.

    Review the following essay and provide constructive feedback.

    Evaluate the essay based on these criteria:

    1. Structure:
       - Is the introduction clear and engaging?
       - Are the paragraphs logically organized?
       - Does the conclusion summarize the main ideas?

    2. Clarity:
       - Are the ideas clearly communicated?
       - Are any sentences confusing or ambiguous?

    3. Strength of Argument:
       - Are the arguments convincing?
       - Are claims supported by evidence or examples?
       - Are there gaps in reasoning?

    4. Writing Style:
       - Is the tone appropriate and consistent?
       - Are transitions smooth?
       - Are there readability issues?

    Provide actionable suggestions in paragraph form.

    Do not rewrite the essay.
    Only provide constructive feedback.

    Essay to review:
    {draft}
    """

    return client.generate(
        prompt=prompt,
        model=model,
        temperature=1.0,
    )
