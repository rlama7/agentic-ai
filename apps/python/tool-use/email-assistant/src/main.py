"""CLI entry point for the Agentic AI Email Assistant."""

from dotenv import load_dotenv


def main() -> None:
    """Initialize the local email assistant CLI."""

    # Load environment variables from the local .env file.
    load_dotenv()

    print("Agentic AI Email Assistant")
    print("Environment initialized successfully.")
    print("Gmail integration: Not configured yet.")


if __name__ == "__main__":
    main()
