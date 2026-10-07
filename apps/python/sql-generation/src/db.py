import sqlite3
from pathlib import Path

import pandas as pd

from src.validator import validate_read_only_sql

DB_PATH = Path("data/products.db")


def get_transaction_count() -> int:
    conn = sqlite3.connect(DB_PATH)

    try:
        cursor = conn.execute("SELECT COUNT(*) FROM transactions")

        row = cursor.fetchone()

        if row is None:
            return 0
        return row[0]
    finally:
        conn.close()


def get_schema() -> str:
    conn = sqlite3.connect(DB_PATH)

    try:
        rows = conn.execute("PRAGMA table_info(transactions)").fetchall()

        columns = [f"{row[1]} ({row[2]})" for row in rows]

        return "table name: transactions\n" + "\n".join(columns)
    finally:
        conn.close()


def execute_sql(query: str) -> pd.DataFrame:
    is_valid, reason = validate_read_only_sql(query)

    if not is_valid:
        return pd.DataFrame({"error": [reason]})

    conn = sqlite3.connect(DB_PATH)

    try:
        return pd.read_sql_query(query, conn)
    except Exception as error:
        return pd.DataFrame({"error": [str(error)]})
    finally:
        conn.close()


def get_database_context() -> str:
    conn = sqlite3.connect(DB_PATH)

    try:
        action_rows = conn.execute("""
            SELECT DISTINCT action
            FROM transactions
            ORDER BY action;
            """).fetchall()

        actions = [row[0] for row in action_rows]

        return (
            "Database semantics:\n"
            f"- Valid action values: {', '.join(actions)}\n"
            "- For sale events, qty_delta is negative because inventory decreases.\n"
            "- For insert and restock events, qty_delta is positive.\n"
            "- For price_update events, qty_delta is 0.\n"
            "- Sales revene should us the positive magnitude of units sold."
        )
    finally:
        conn.close()
