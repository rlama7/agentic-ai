"""Gmail tools for the Email Assistant."""

from googleapiclient.discovery import build

from .gmail_auth import get_credentials


def list_emails(max_results: int = 5) -> list[dict]:
    """List recent Gmail inbox message IDs."""

    # Obtain authorized Gmail credentials.
    credentials = get_credentials()

    # Create the Gmail API client.
    service = build("gmail", "v1", credentials=credentials)

    # Fetch up to max_results messages from the inbox.
    response = (
        service.users()
        .messages()
        .list(
            userId="me",
            labelIds=["INBOX"],
            maxResults=max_results,
        )
        .execute()
    )

    # Gmail may omit "messages" when the inbox is empty.
    return response.get("messages", [])


def get_email(message_id: str) -> dict:
    """Retrieve Gmail message metadata by message ID."""

    # Reuse our existing OAuth credentials.
    credentials = get_credentials()

    # Build the authenticated Gmail API client.
    service = build("gmail", "v1", credentials=credentials)

    # Retrieve only the headers we need.
    message = (
        service.users()
        .messages()
        .get(
            userId="me",
            id=message_id,
            format="metadata",
            metadataHeaders=["From", "To", "Subject", "Date"],
        )
        .execute()
    )

    # Convert the header list into a dictionary.
    headers = {
        header["name"].lower(): header["value"]
        for header in message.get("payload", {}).get("headers", [])
    }

    # Return a compact structure for our future agent.
    return {
        "id": message["id"],
        "thread_id": message.get("threadId"),
        "sender": headers.get("from", ""),
        "recipient": headers.get("to", ""),
        "subject": headers.get("subject", ""),
        "date": headers.get("date", ""),
    }


def search_emails(query: str, max_results: int = 5) -> list[dict]:
    """Search Gmail message using Gmail search operators."""

    # Validate the search query before making an API request.
    if not query.strip():
        raise ValueError("Search query cannot be empty.")

    # Reuse our existing OAuth authentication.
    credentials = get_credentials()

    # Build the Gmail API client.
    service = build("gmail", "v1", credentials=credentials)

    # Ask Gmail to search messages matching the query.
    response = (
        service.users()
        .messages()
        .list(
            userId="me",
            q=query,
            maxResults=max_results,
        )
        .execute()
    )

    return response.get("messages", [])
