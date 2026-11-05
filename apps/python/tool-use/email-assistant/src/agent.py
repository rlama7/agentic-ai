"""AISuite orchestration for the Gmail Email Assistant."""

import aisuite as ai

from .gmail_tools import (
    get_email as gmail_get_email,
)
from .gmail_tools import search_emails as gmail_search_emails
from .gmail_tools import (
    search_unread_from_sender as gmail_search,
)


def search_unread_from_sender(sender: str) -> list[dict]:
    """Find up to two unread Gmail messages from a sender.

    Args:
        sender: The sender's complete email address.
    """
    print("\n[TOOL START] search_unread_from_sender")
    print(f"[ARGUMENTS] sender={sender}")

    messages = gmail_search(sender=sender, max_results=2)

    print(f"[TOOL RESULT] {len(messages)} matching messages")
    print("[TOOL END]\n")

    return messages


def search_emails(query: str) -> list[dict]:
    """Search Gmail using keywords or Gmail search operators.

    Args:
        query: Gmail search expression, such as
        'subject:AI', 'is:unread', or 'newer_than:7d',
    """
    print("\n[TOOL START] search_emails")
    print(f"[ARGUMENTS] query={query}")

    # Reuse the Gmail API implementation
    messages = gmail_search_emails(
        query=query,
        max_results=3,
    )

    print(f"[TOOL RESULT] {len(messages)} matching messages")
    print("[TOOL END]\n")

    return messages


def get_email(message_id: str) -> dict:
    """Retrieve metadata for a Gmail message by its ID.

    Args:
        message_id: Gmail message ID returned by a search tool.
    """
    print("\n[TOOL START] get_email")
    print("[ARGUMENTS] message_id provided")

    # Reuse the existing Gmail API implementation.
    email = gmail_get_email(message_id)

    print("[TOOL RESULT] Message metadata retrieved")
    print("[TOOL END]\n")

    return email


def run_agent(request: str) -> str:
    """Run the Gmail assistant with two read-only tools."""

    client = ai.Client()

    response = client.chat.completions.create(
        model="openai:gpt-4.1",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a read-only Gmail assistant. "
                    "Use the provided tools to answer the user's request. "
                    "Search for matching messages before retrieving metadata. "
                    "Do not invent email contents or message details. "
                    "If no messages match, explain that clearly."
                ),
            },
            {"role": "user", "content": request},
        ],
        tools=[
            search_unread_from_sender,
            get_email,
            search_emails,
        ],
        max_turns=5,
    )

    return response.choices[0].message.content or ""
