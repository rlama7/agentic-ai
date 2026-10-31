import aisuite as ai
from dotenv import load_dotenv

from src.tools import (
    generate_qr_code,
    get_current_time,
    get_weather_from_ip,
    write_txt_file,
)
from src.tracing import trace_tool


# AISuite's final response does not expose
# ntermediate history through resposne.message in the # installed version
def print_tool_trace(response) -> None:
    """Print tool calls and results from the AISuite response."""

    print("\n--- Tool Execution Trace ---")

    # AISuite may expose intermediate turns in response.messages
    history = getattr(response, "messages", None)

    if history is None:
        print("Intermediate tool history is not available.")
        return

    for message in history:
        role = (
            message.get("role")
            if isinstance(message, dict)
            else getattr(message, "role", None)
        )

        if role == "assistant":
            tool_calls = (
                message.get("tool_calls")
                if isinstance(message, dict)
                else getattr(message, "tool_calls", None)
            )

            for call in tool_calls or []:
                function = (
                    call.get("function")
                    if isinstance(call, dict)
                    else getattr(call, "function", None)
                )

                name = (
                    function.get("name")
                    if isinstance(function, dict)
                    else getattr(function, "name", None)
                )

                arguments = (
                    function.get("arguments")
                    if isinstance(function, dict)
                    else getattr(function, "arguments", None)
                )

                print(f"\nLLM requested: {name}")
                print(f"Arguments: {arguments}")

        elif role == "tool":
            content = (
                message.get("content")
                if isinstance(message, dict)
                else getattr(message, "content", None)
            )

            print(f"Tool returned: {content}")


def main() -> None:
    """Demonstrate multi-tool orchestration using AISuite."""

    # Load the OpenAI API key
    load_dotenv()

    # Initialize the OpenAI API key
    client = ai.Client()

    # this request requires multiple tools
    prompt = (
        "Create a QR code linking to https://www.ratnalama.com "
        "using the logo lama-rock.png "
        "Save the QR code as lama_multi_qr "
        "Also create a text file named weather_report.txt "
        "containing my current weather (temperature, high, low) "
        "and the current local time when the weather was retrieved. "
        "Retrieve the weather and time before writing the note."
    )

    messages = [
        {
            "role": "user",
            "content": prompt,
        }
    ]

    # Make all four tools available to the LLM
    tools = [
        trace_tool(get_current_time),
        trace_tool(get_weather_from_ip),
        trace_tool(write_txt_file),
        trace_tool(generate_qr_code),
    ]

    try:
        # AISuite automatically handles tool orchestration
        response = client.chat.completions.create(
            model="openai:gpt-4o",
            messages=messages,
            tools=tools,
            max_turns=10,
        )

        # Tool traces
        print_tool_trace(response)

        # Display the final response
        print("\n--- Final Assistant Response ---")
        print(response.choices[0].message.content)

    except Exception as error:
        print(f"Multi-tool orchestration failed: {error}")


if __name__ == "__main__":
    main()
