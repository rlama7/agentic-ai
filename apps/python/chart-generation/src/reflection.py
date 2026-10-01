import base64
import json
import re
from pathlib import Path

from openai import OpenAI

client = OpenAI()


def encode_image_base64(image_path: str | Path) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def reflect_on_chart(
    chart_path: str | Path,
    instruction: str,
    code_v1: str,
    model: str,
    output_path_v2: str,
) -> tuple[str, str]:
    image_base64 = encode_image_base64(chart_path)

    prompt = f"""
You are a data visualization expert.

Review the attached chart and the original Python code.

Original instruction:
{instruction}

Original code:
{code_v1}

Return your answer in exactly this format:

{{"feedback": "your critique here"}}

<execute_python>
# improved Pythong code here
</execute_python>

Requirements:
- Use pandas and matplotlib only,
- Assume the DataFrame already exists as 'df'.
- Improve clarity and comparison quality.
- Save the improved chart to '{output_path_v2}' with dpi=300.
- Do not call plt.show().
- Call plt.close().
- Include all required imports.
"""
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": prompt,
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{image_base64}",
                    },
                ],
            }
        ],
    )

    content = response.output_text

    feedback_match = re.search(r"\{.*?\}", content, re.DOTALL)

    if not feedback_match:
        raise ValueError("No feedback JSON found in model response")

    feedback_data = json.loads(feedback_match.group(0))
    feedback = feedback_data["feedback"]

    code_match = re.search(
        r"<execute_python>([\s\S]*?)</execute_python>",
        content,
    )

    if not code_match:
        raise ValueError("No <execute_python> block found in model response")

    code_v2 = code_match.group(1).strip()

    return feedback, code_v2
