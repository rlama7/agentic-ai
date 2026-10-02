from pathlib import Path

from src.chart_generator import (
    execute_chart_code,
    extract_python_code,
    generate_chart_code,
)

from src.data_loader import load_and_prepare_data
from src.reflection import reflect_on_chart

DATA_PATH = Path("data/coffee_sales.csv")

INSTRUCTION = (
    "Create a plot comparing Q1 coffee sales in 2024 and 2025 "
    "using the coffee sales data."
)


def main() -> None:
    try:
        df = load_and_prepare_data(DATA_PATH)

        code_v1_response = generate_chart_code(
            instruction=INSTRUCTION,
            model="gpt-4o-mini",
            output_path="output/chart_v1.png",
        )
        code_v1 = extract_python_code(code_v1_response)

        print("Generated V1 code")
        print(code_v1)

        execute_chart_code(code_v1, df)

        print("Chart V1 generated successfully: output/chart_v1.png")
        feedback, code_v2 = reflect_on_chart(
            chart_path="output/chart_v1.png",
            instruction=INSTRUCTION,
            code_v1=code_v1,
            model="gpt-4o-mini",
            output_path_v2="output/chart_v2.png",
        )
        print()
        print("Reflection feedback:")
        print(feedback)
        print()
        print("Generated V2 Code:")
        print(code_v2)
        execute_chart_code(code_v2, df)
        print("Chart V2 generated successfully: output/chart_v2.png")

    except FileNotFoundError as error:
        print(f"File error: {error}")

    except ValueError as error:
        print(f"Validation error: {error}")

    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()
