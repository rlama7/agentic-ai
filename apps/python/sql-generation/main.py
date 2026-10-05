from src.db import DB_PATH, get_transaction_count, get_schema, execute_sql


def main() -> None:
    transaction_count = get_transaction_count()
    schema = get_schema()

    query = """
    SELECT product_id, color, action, qty_delta, unit_price
    FROM transactions
    LIMIT 5;
    """

    result = execute_sql(query)

    print("SQL generation project environment ready")
    print(f"Database: {DB_PATH}")
    print(f"Transactions: {transaction_count}")

    print("\nSchema:")
    print(schema)

    print("\nQuery Result:")
    print(result)


if __name__ == "__main__":
    main()
