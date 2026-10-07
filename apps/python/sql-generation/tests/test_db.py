from src.db import (
    execute_sql,
    get_database_context,
    get_schema,
)


def test_get_schema_contains_transaction_table() -> None:
    schema = get_schema()

    assert "table name: transactions" in schema
    assert "qty_delta (INTEGER)" in schema
    assert "unit_price (REAL)" in schema


def test_execute_sql_returns_rows_for_safe_query() -> None:
    result = execute_sql("""
        SELECT color, action, qty_delta
        FROM transactions
        LIMIT 5;
        """)
    assert result.empty is False
    assert "color" in result.columns
    assert "action" in result.columns
    assert "qty_delta" in result.columns


def test_execute_sql_rejects_unsafe_query() -> None:
    result = execute_sql("DELETE FROM transactions;")
    assert "error" in result.columns
    assert result.iloc[0]["error"] == "Only SELECT queries are allowed."
