from src.validator import validate_read_only_sql


def test_allows_select_query() -> None:
    is_valid, reason = validate_read_only_sql("SELECT * FROM transactions;")

    assert is_valid is True
    assert reason == ""


def test_rejects_delete_query() -> None:
    is_valid, reason = validate_read_only_sql("DELETE FROM transactions;")

    assert is_valid is False
    assert reason == "Only SELECT queries are allowed."


def test_rejects_empty_query() -> None:
    is_valid, reason = validate_read_only_sql("")

    assert is_valid is False
    assert reason == "SQL query is empty."
