"""CLI entry point for the Agentic AI Email Assistant."""

from googleapiclient.errors import HttpError

from .gmail_tools import get_email, search_unread_from_sender


def main() -> None:
    """Search unread messages from a specified sender."""

    sender = "no-reply@zoom.us"

    print("Agentic AI Email Assistant")

    # Search for unread messages in the test Gmail account.
    # query = "from:zoom.us"
    # query = "is:unread"
    print(f"Searching unread emails from: {sender}")

    try:
        # First retrieve a small list of message IDs.
        # messages = search_emails(query, max_results=3)
        # messages = list_emails(max_results=2)

        # Find unread messages matching the sender
        messages = search_unread_from_sender(
            sender=sender,
            max_results=3,
        )

        if not messages:
            print("No unread messages found.")
            return

        print(f"Found {len(messages)} matching messages.")

        # Retrieve metadata for each message ID.
        for message in messages:
            email = get_email(message["id"])

            print("\n--- Email ---")
            print(f"From: {email['sender']}")
            # print(f"To: {email['recipient']}")
            print(f"Subject: {email['subject']}")
            print(f"Date: {email['date']}")

    except (FileNotFoundError, HttpError) as error:
        print(f"Gmail Search error: {error}")


if __name__ == "__main__":
    main()
