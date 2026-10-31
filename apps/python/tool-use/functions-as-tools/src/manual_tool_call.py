import json

import aisuite as ai
from dotenv import load_dotenv

from src.tools import get_current_time


def main() -> None:
    # Load API credentials
    load_dotenv()

    client = ai.Client()

    messages = [{"role": "user", "content": "What time is it?"}]

    # Manually define the tool schema
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_time",
                "description": "Returns the current local time as a string.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
        }
    ]

    try:
        # Step 1: Ask the LLM to choose a tool
        response = client.chat.completions.create(
            model="openai:gpt-4o",
            messages=messages,
            tools=tools,
        )

        assistant_message = response.choices[0].message

        # Step 2: Inspect what the model requested
        print("\n--- LLM Tool Request ---")
        print(
            json.dumps(
                assistant_message.model_dump(),
                indent=2,
                default=str,
            )
        )

        # Step 3: Check whether the model requested a tool
        if not assistant_message.tool_calls:
            print("\nNo tool requested.")
            print(assistant_message.content)
            return

        # Preserve the assistant's tool-call message
        messages.append(assistant_message)

        # Step 4: Execute each requested, permitted tool
        for tool_call in assistant_message.tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            print(f"\nRequested tool: {function_name}")
            print(f"Arguments: {arguments}")

            # Explicit allowlist: execute only known functions
            if function_name == "get_current_time" and arguments == {}:
                result = get_current_time()
            else:
                result = "Error: Unknown tool or invalid arguments."

            print(f"Tool result: {result}")

            # Step 5: Return the result with its matching call ID
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result),
                }
            )

        # Step 6: Ask the LLM to produce the final response
        final_response = client.chat.completions.create(
            model="openai:gpt-4o",
            messages=messages,
            tools=tools,
            tool_choice="none",
        )

        print("\n--- Final Assistant Response ---")
        print(final_response.choices[0].message.content)

    except Exception as error:
        print(f"Manual tool calling failed: {error}")


if __name__ == "__main__":
    main()
