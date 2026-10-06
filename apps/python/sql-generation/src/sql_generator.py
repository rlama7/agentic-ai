from src.llm_client import get_response

DEFAULT_MODEL = "gpt-4o-mini"


def generate_sql(
    question: str,
    schema: str,
    database_context: str,
    model: str = DEFAULT_MODEL,
) -> str:
    prompt = f"""
You are a SQL assistant.

Given the SQLite database schema, database semantics,
and the user's question, write one read-only SQL SELECT query
that answers the question.

Database schema:
{schema}

Database semantis:
{database_context}

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
