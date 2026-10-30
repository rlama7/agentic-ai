import aisuite as ai
from dotenv import load_dotenv

from src.tools import (
    generate_qr_code,
    get_current_time,
    get_weather_from_ip,
    write_txt_file,
)


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
        get_current_time,
        get_weather_from_ip,
        write_txt_file,
        generate_qr_code,
    ]

    try:
        # AISuite automatically handles tool orchestration
        response = client.chat.completions.create(
            model="openai:gpt-4o",
            messages=messages,
            tools=tools,
            max_turns=10,
        )

        # Display the final response
        print("\n--- Final Assistant Response ---")
        print(response.choices[0].message.content)

    except Exception as error:
        print(f"Multi-tool orchestration failed: {error}")


if __name__ == "__main__":
    main()
