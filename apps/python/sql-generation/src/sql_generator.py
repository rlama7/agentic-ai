from src.llm_client import get_response

DEFAULT_MODEL = "gpt-4o-mini"


def generate_sql(
    question: str,
    schema: str,
    model: str = DEFAULT_MODEL,
) -> str:
    prompt = f"""
You are a SQL assistant.

Given the SQLite database schema and the user's question,
write one read-only SQL SELECT query tha answers the question.

Database schema:
{schema}

User question:
{question}

Requirements:
- Use SQLite syntax.
- Only query the transactions table.
- Return a SELECT query only.
- Do not include markdown code fences.
- Do not include explanations.

Return SQL only.
"""
    return get_response(
        prompt=prompt,
        model=model,
    )
