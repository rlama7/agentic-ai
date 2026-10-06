from src.db import (
    DB_PATH,
    get_transaction_count,
    get_schema,
    execute_sql,
)

from src.sql_generator import generate_sql

# from src.llm_client import get_response

QUESTION = "Which color of product has the highest total sales?"


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

    # response = get_response("Reply with exactly: LLM client working")
    # print(response)

    schema = get_schema()

    sql_v1 = generate_sql(question=QUESTION, schema=schema)

    print("User Question:")
    print(QUESTION)

    print("\nGenerated SQL V1:")
    print(sql_v1)


if __name__ == "__main__":
    main()
