import sqlite3
from pathlib import Path
from src.validator import validate_read_only_sql

import pandas as pd

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
