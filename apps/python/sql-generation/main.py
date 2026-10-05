from src.db import (
    DB_PATH,
    get_transaction_count,
    get_schema,
    execute_sql,
)

from src.llm_client import get_response


def main() -> None:
    # safe_query = """
    # SELECT product_id, color, action, qty_delta, unit_price
    # FROM transactions
    # LIMIT 5;
    # """

    # unsafe_query = """
    # DELETE FROM transactions;
    # """

    # safe_result = execute_sql(safe_query)
    # unsafe_result = execute_sql(unsafe_query)

    # print("\nSafe Query Result:")
    # print(safe_result)

    # print("\nUnsafe Query Result:")
    # print(unsafe_result)

    response = get_response("Reply with exactly: LLM client working")

    print(response)


if __name__ == "__main__":
    main()
