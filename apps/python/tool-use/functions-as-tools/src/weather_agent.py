import aisuite as ai
from dotenv import load_dotenv

from src.tools import get_current_time, get_weather_from_ip


def main() -> None:
    # Load API key from .env
    load_dotenv()

    # Initialize AISuite
    client = ai.Client()

    # Ask a question that requires weather information
    messages = [
        {
            "role": "user",
            "content": "Can you get the weather for my location?",
        }
    ]

    try:
        # Give the LLM access to both Python functions
        response = client.chat.completions.create(
            model="openai:gpt-4o",
            messages=messages,
            tools=[
                get_current_time,
                get_weather_from_ip,
            ],
            max_turns=5,
        )

        # Display the final answer
        print("\n--- Final Assistant Response ---")
        print(response.choices[0].message.content)

    except Exception as error:
        print(f"Weather agent failed: {error}")


if __name__ == "__main__":
    main()
