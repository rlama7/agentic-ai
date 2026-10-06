from dataclasses import dataclass

import pandas as pd

from src.db import execute_sql, get_schema, get_database_context
from src.reflection import reflect_on_sql
from src.sql_generator import generate_sql

MAX_ATTEMPTS = 3


@dataclass
class WorkflowAttempt:
    attempt: int
    sql: str
    result: pd.DataFrame
    is_correct: bool
    feedback: str


@dataclass
class WorkflowResult:
    question: str
    attempts: list[WorkflowAttempt]
    succeeded: bool


def run_sql_workflow(
    question: str,
    max_attempts: int = MAX_ATTEMPTS,
) -> WorkflowResult:
    schema = get_schema()
    database_context = get_database_context()

    current_sql = generate_sql(
        question=question, schema=schema, database_context=database_context
    )

    attempts: list[WorkflowAttempt] = []

    for attempt in range(1, max_attempts + 1):
        result = execute_sql(current_sql)

        # print(f"\n--- Attempt {attempt} ---")

        # print("\nSQL:")
        # print(current_sql)

        # result = execute_sql(current_sql)

        # print("\nResult:")
        # print(result)

        is_correct, feedback, refined_sql = reflect_on_sql(
            question=question,
            sql_query=current_sql,
            result=result,
            schema=schema,
            database_context=database_context,
        )

        attempts.append(
            WorkflowAttempt(
                attempt=attempt,
                sql=current_sql,
                result=result,
                is_correct=is_correct,
                feedback=feedback,
            )
        )

        # print("\nReflection Correct?:")
        # print(is_correct)

        # print("\nReflection Feedback:")
        # print(feedback)

        if is_correct:
            # print("\nWorkflow completed successfully."

            return WorkflowResult(
                question=question,
                attempts=attempts,
                succeeded=True,
            )

        current_sql = refined_sql

    print(
        f"\nWorkflow stopped after {max_attempts} attempts"
        "without a confirmed correct result."
    )
