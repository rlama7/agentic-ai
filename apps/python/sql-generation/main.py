# from src.db import (
#     DB_PATH,
#     get_transaction_count,
#     get_schema,
#     execute_sql,
# )
from src.workflow import run_sql_workflow

# from src.sql_generator import generate_sql

# from src.reflection import reflect_on_sql

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

    # schema = get_schema()

    # Step 1: Generate SQL V1
    # sql_v1 = generate_sql(question=QUESTION, schema=schema)

    # Step 2: Execute V1
    # result_v1 = execute_sql(sql_v1)

    # Step 3: Reflect on V1
    # is_correct, feedback, sql_v2 = reflect_on_sql(
    #     question=QUESTION, sql_query=sql_v1, result=result_v1, schema=schema
    # )

    # Step 4: Execute V2 if refinement is needed

    # if is_correct:
    #     sql_v2 = sql_v1
    #     result_v2 = result_v1
    # else:
    #     result_v2 = execute_sql(sql_v2)

    workflow_result = run_sql_workflow(question=QUESTION)

    print("User Question:")
    print(QUESTION)

    for attempt in workflow_result.attempts:
        print(f"\n--- Attempt {attempt.attempt} ---")

        print("\nSQL:")
        print(attempt.sql)

        print("\nResult:")
        print(attempt.result)

        print("\nReflection Correct?:")
        print(attempt.is_correct)

        print("\nReflection Feedback:")
        print(attempt.feedback)

    print("\nWorkflow Success:")
    print(workflow_result.succeeded)

    # print("\nSQL V2:")
    # print(sql_v2)

    # print("\nV2 Result:")
    # print(result_v2)


if __name__ == "__main__":
    main()
