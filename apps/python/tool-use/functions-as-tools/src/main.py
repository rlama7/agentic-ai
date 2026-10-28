import aisuite as ai
from dotenv import load_dotenv

from src.tools import get_current_time


def main() -> None:
    # Load OPENAI_API_KEY from the project's .env file
    load_dotenv()

    # Initialize the AISuite client
    client = ai.Client()

    # Define the user's request
    messages = [{"role": "user", "content": "What time is it?"}]

    try:
        # Let AISuite expose and execute our Python function
        response = client.chat.completions.create(
            model="openai:gpt-4o",
            messages=messages,
            tools=[get_current_time],
            max_turns=5,
        )

        # Display the final assistant response
        print(response.choices[0].message.content)

    except Exception as error:
        print(f"Tool calling failed: {error}")


if __name__ == "__main__":
    main()
