import aisuite as ai
from dotenv import load_dotenv

from src.tools import (
    generate_qr_code,
    get_current_time,
    get_weather_from_ip,
    write_txt_file,
)


def main() -> None:
    # Load OPENAI_API_KEY
    load_dotenv()

    # Initialize AISuite client
    client = ai.Client()

    # Request QR code generation using natural language
    messages = [
        {
            "role": "user",
            "content": (
                "Create a QR code that opens "
                "https://www.ratnalama.com. "
                "Use the logo lama-rock.png and "
                "save the QR code as lama_qr_code."
            ),
        }
    ]

    try:
        # Give the LLM access to all four tools
        response = client.chat.completions.create(
            model="openai:gpt-4o",
            messages=messages,
            tools=[
                get_current_time,
                get_weather_from_ip,
                write_txt_file,
                generate_qr_code,
            ],
            max_turns=5,
        )

        # Display final assistant response
        print("\n--- Final Assistant Response ---")
        print(response.choices[0].message.content)

    except Exception as error:
        print(f"QR code agent failed: {error}")


if __name__ == "__main__":
    main()
