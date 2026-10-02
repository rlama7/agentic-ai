from src.llm_client import get_response


def generate_chart_code(
    instruction: str,
    model: str,
    output_path: str,
) -> str:
    prompt = f"""
You are a data visualization expert.

Return your answer strictly in this format:

<execute_python>
# valid Python code here
</execute_python>

Do not add explanations. Return only the tags and Python code.

The code should create a visualization from a pandas DataFrame named 'df'
with these columns:

- date (datetime64)
- time (string, HH:MM)
- cash_type (string: 'card' or 'cash')
- card (string)
- price (number)
- coffee_name (string)
- quarter (integer, 1-4)
- month (integer, 1-12)
- year (integer)

User instruction:
{instruction}

Requirements:
1. Assume the DataFrame is already available as 'df'.
2. Use matplotlib for plotting.
3. Add a clear title and axis labels.
4. Add a legend when appropriate.
5. Save the figure to '{output_path}' with dpi=300.
6. Do not call plt.show().
7. Call plt.close() when finished.
8. Include all necessary Python imports.
9. Use the existing 'year' and 'quarter' columns for filtering.

Return only the code wrapped in <execute_python> tags.
"""

    return get_response(model, prompt)


import re
from typing import Any


def extract_python_code(response: str) -> str:
    match = re.search(
        r"<execute_python>([\s\S]*?)</execute_python>",
        response,
    )
    if not match:
        raise ValueError("No <execute_python block found in model response")

    return match.group(1).strip()


def execute_chart_code(
    code: str,
    df: Any,
) -> None:
    exec_globals = {
        "df": df,
    }

    # NOTE:
    # This executes LLM-generate Python code directly.
    # Acceptable for this demo, but production system should
    # sandbox or validated generated code before execution
    exec(code, exec_globals)

## Acknowledgement:
This project is a local, modular