"""CLI entry point for the Agentic AI Email Assistant."""

from googleapiclient.errors import HttpError

from .gmail_tools import get_email, list_emails


def main() -> None:
    """Retrieve and display recent Gmail message metadata."""

    print("Agentic AI Email Assistant")
    print("Fetching Gmail message metadata...")

    try:
        # First retrieve a small list of message IDs.
        messages = list_emails(max_results=2)

        if not messages:
            print("No inbox messages found.")
            return

        # Retrieve metadata for each message ID.
        for message in messages:
            email = get_email(message["id"])

            print("\n--- Email ---")
            print(f"From: {email['sender']}")
            print(f"To: {email['recipient']}")
            print(f"Subject: {email['subject']}")
            print(f"Date: {email['date']}")

    except (FileNotFoundError, HttpError) as error:
        print(f"Gmail API error: {error}")


if __name__ == "__main__":
    main()
