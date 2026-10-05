import sqlite3
from pathlib import Path

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
