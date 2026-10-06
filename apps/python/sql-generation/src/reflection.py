import json
import pandas as pd

from src.llm_client import get_response

DEFAULT_MODEL = "gpt-4o-mini"


def reflect_on_sql(
    question: str,
    sql_query: str,
    result: pd.DataFrame,
    schema: str,
    model: str = DEFAULT_MODEL,
) -> tuple[bool, str, str]:
    result_text = result.to_markdown(index=False)

    prompt = f"""
You are a SQL reviewer and refiner.

Evaluate whether the SQL query and its actual execution result fully answer the user's question.

User question:
{question}

Database schema:
{schema}

SQL query:
{sql_query}

Actual SQL result:
{result_text}

Return STRICT JSON with exactly these fields:

{{
  "is_correct": true or false,
  "feedback": "brief explanation",
  "refined_sql": "final read-only SQLite SELECT query"
}}

Requirements:
- Set "is_correct" to true only if the result fully and meaningfully answers the user's question.
- If the result is incorrect, explain the issue briefly.
- If refinement is needed, provide and improved SQL query.
- Only use the transaction table.
- Only generate a SELECT query.
- Do not include markdown code fences.
"""

    content = get_response(prompt=prompt, model=model)

    try:
        parsed = json.loads(content)

        is_correct = bool(parsed.get("is_correct", False))

        feedback = str(parsed.get("feedback", "")).strip()

        refined_sql = str(parsed.get("refined_sql", sql_query)).strip()

        if not refined_sql:
            refined_sql = sql_query

        return is_correct, feedback, refined_sql
    except json.JSONDecodeError:
        return (False, f"Could not parse reflection response: {content}", sql_query)
