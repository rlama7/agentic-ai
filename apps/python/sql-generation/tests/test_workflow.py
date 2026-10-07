from unittest.mock import patch
from src.workflow import run_sql_workflow


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
