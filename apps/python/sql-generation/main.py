from src.db import DB_PATH, get_transaction_count


def main() -> None:
    transaction_count = get_transaction_count()

    print("SQL generation project environment ready")
    print(f"Database: {DB_PATH}")
    print(f"Transactions: {transaction_count}")


if __name__ == "__main__":
    main()
