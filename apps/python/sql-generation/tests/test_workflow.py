from unittest.mock import patch
from src.workflow import run_sql_workflow

QUESTION = "Which color has the highest total sales?"
MAX_ATTEMPTS = 3


def test_workflow_refines_until_correct() -> None:
    sql_v1 = """
    SELECT color, SUM(qty_delta * unit_price) AS total_sales
    FROM transactions
    WHERE action = 'sale'
    GROUP BY color
    ORDER BY total_sales DESC
    LIMIT 1;
    """

    sql_v2 = """
    SELECT color, SUM(-qty_delta * unit_price) AS total_sales
    FROM transactions
    WHERE action = 'sale'
    GROUP BY color
    ORDER BY total_sales DESC
    LIMIT 1;
    """

    with (
        patch(
            "src.workflow.generate_sql",
            return_value=sql_v1,
        ),
        patch(
            "src.workflow.reflect_on_sql",
            side_effect=[
                (
                    False,
                    "Total sales should not be negative.",
                    sql_v2,
                ),
                (
                    True,
                    "The query now correctly calculates total sales.",
                    sql_v2,
                ),
            ],
        ),
    ):
        result = run_sql_workflow(question="Which color has the highest total sales?")

        assert result.succeeded is True
        assert len(result.attempts) == 2

        assert result.attempts[0].sql.strip() == sql_v1.strip()
        assert result.attempts[1].sql.strip() == sql_v2.strip()


def test_workflow_stops_after_max_attempts() -> None:
    sql_v1 = """
  SELECT color
  FROM transactions
  WHERE action = 'sale'
  LIMIT 1;
  """

    sql_v2 = """
  SELECT color, qty_delta
  FROM transactions
  WHERE action = 'sale'
  LIMIT 1;
  """

    sql_v3 = """
  SELECT color, unit_price
  FROM transactions
  WHERE action = 'sale'
  LIMIT 1;
  """

    with (
        patch(
            "src.workflow.generate_sql",
            return_value=sql_v1,
        ),
        patch(
            "src.workflow.reflect_on_sql",
            side_effect=[
                (
                    False,
                    "Attempt 1 is incomplete.",
                    sql_v2,
                ),
                (
                    False,
                    "Attempt 2 is still incomplete.",
                    sql_v3,
                ),
                (
                    False,
                    "Attempt 3 is still incorrect.",
                    sql_v3,
                ),
            ],
        ),
    ):
        result = run_sql_workflow(
            question="Which color has the highest total sales?",
            max_attempts=3,
        )

    assert result.succeeded is False
    assert len(result.attempts) == 3

    assert result.attempts[0].sql.strip() == sql_v1.strip()
    assert result.attempts[1].sql.strip() == sql_v2.strip()
    assert result.attempts[2].sql.strip() == sql_v3.strip()

    assert all(attempt.is_correct is False for attempt in result.attempts)
