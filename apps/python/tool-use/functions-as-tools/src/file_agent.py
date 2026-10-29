import aisuite as ai
from dotenv import load_dotenv

from src.tools import (
    get_current_time,
    get_weather_from_ip,
    write_txt_file,
)


def main() -> None:
    # Load environment variables
    load_dotenv()

    # Initialize AISuite
    client = ai.Client()

    # Request that wires writing a file
    messages = [
        {
            "role": "user",
            "content": (
                "Create a text note called reminders.txt"
                "reminding me to call Daniel tomorrow at 7 PM."
            ),
        }
    ]

    try:
        # Allow the model to select from three available tools
        response = client.chat.completions.create(
            model="openai:gpt-4o",
            messages=messages,
            tools=[
                get_current_time,
                get_weather_from_ip,
                write_txt_file,
            ],
            max_turns=5,
        )

        # Print the final response
        print("\n--- Final Assistant Response ---")
        print(response.choices[0].message.content)

    except Exception as error:
        print(f"File agent failed: {error}")


if __name__ == "__main__":
    main()
