"""CLI entry point for the Agentic AI Email Assistant."""

import os

from dotenv import load_dotenv

from .agent import run_agent


def main() -> None:
    """Execute a natural-language Gmail request."""

    load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY is not configured.")
        return

    request = (
        "Find unread emails from no-reply@zoom.us and tell me how many were retrieved."
    )
    # request = (
    #     "Find upto 3 emails with AI in the subject and tell me how many you found."
    # )

    print("Agentic AI Email Assistant")
    print(f"[USER] {request}")

    try:
        result = run_agent(request)
        print(f"\n[AGENT RESPONSE] \n{result}")

    except Exception as error:
        print(f"Agent execution failed: {type(error).__name__}")
        raise


if __name__ == "__main__":
    main()
