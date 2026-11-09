"""AISuite orchestration for the Gmail Email Assistant."""

import os

import aisuite as ai

from .approval import request_approval
from .gmail_tools import create_draft as gmail_create_draft
from .gmail_tools import (
    get_email as gmail_get_email,
)
from .gmail_tools import (
    mark_email_as_read as gmail_mark_email_as_read,
)
from .gmail_tools import mark_email_as_unread as gmail_mark_email_as_unread
from .gmail_tools import search_emails as gmail_search_emails
from .gmail_tools import (
    search_unread_from_sender as gmail_search,
)
from .privacy import mask_email


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


def mark_email_as_read(message_id: str) -> dict:
    """Mark as Gmail message as read only after explicit user approval.

    Args:
        message_id: Gmail message ID returned by a search tool.
    """
    print("\n[TOOL START] mark_email_as_read")

    # Validate before making any Gmail request.
    if not message_id.strip():
        raise ValueError("Message ID cannot be empty.")

    # Retrieve metadata so the user knows what will change.
    email = gmail_get_email(message_id)

    approved = request_approval(
        action="MARK AS READ",
        details={
            "From": email["sender"],
            "Subject": email["subject"],
        },
    )

    if not approved:
        print("[TOOL RESULT] Action cancelled")
        print("[TOOL END]\n")

        return {
            "status": "cancelled",
            "message": "User did not approve the modification.",
        }

    # Execute only after explicit approval
    result = gmail_mark_email_as_read(message_id)

    return {
        "status": "success" if result["read"] else "failed",
        "message_id": result["id"],
        "read": result["read"],
    }


def mark_email_as_unread(message_id: str) -> dict:
    """Mark a Gmail message as unread after explicit user approval.

    Args:
        message_id: Gmail message ID returned by a search tool.
    """
    print("\n[TOOL START] mark_email_as_unread")

    if not message_id.strip():
        raise ValueError("Message ID cannot be empty.")

    # Retrieve message metadata for the approval preview.
    email = gmail_get_email(message_id)

    approved = request_approval(
        action="MARK AS UNREAD",
        details={
            "From": email["sender"],
            "Subject": email["subject"],
            "Date": email["date"],
        },
    )

    if not approved:
        print("[TOOL RESULT] Action cancelled")
        print("[TOOL END]\n")

        return {
            "status": "cancelled",
            "message": "User did not approve the modification.",
        }

    # Only executed after explicit approval.
    result = gmail_mark_email_as_unread(message_id)

    print("[TOOL RESULT] Modification completed")
    print("[TOOL END]\n")

    return {
        "status": "success" if result["unread"] else "failed",
        "message_id": result["id"],
        "unread": result["unread"],
    }


def create_draft(recipient: str, subject: str, body: str) -> dict:
    """Create a Gmail draft after explicit user approval

    Args:
        recipient: Email address of the intended recipient.
        subject: Subject for the email draft.
        body: Plain-text content of the email draft.
    """
    print("\n[TOOL START] create_draft")
    print(f"[ARGUMENTS] recipient={mask_email(recipient)}")

    # Restrict draft creation to our configured test account.
    allowed_recipient = os.getenv("GMAIL_TEST_RECIPIENT", "").strip()

    if not allowed_recipient or (
        recipient.strip().casefold() != allowed_recipient.casefold()
    ):
        print("[TOOL RESULT] Recipient not authorized")
        print("[TOOL END]\n")

        return {
            "status": "denied",
            "message": "Recipient is not the configured test account.",
        }

    # Reuse our existing human approval mechanism.
    approved = request_approval(
        action="CREATE GMAIL DRAFT",
        details={
            "To": mask_email(recipient),
            "Subject": subject,
            "Body": body,
        },
    )

    if not approved:
        print("[TOOL RESULT] Draft creation cancelled")
        print("[TOOL END]\n")

        return {"status": "cancelled", "message": "User declined draft creation."}

    # Only save the draft after authorization.
    result = gmail_create_draft(recipient, subject, body)

    print("[TOOL RESULT] Draft created successfully")
    print("[TOOL END]\n")

    return {
        "status": "success",
        "draft_id": result["draft_id"],
        "message": "Draft saved in Gmail. Email not sent.",
    }


def run_agent(request: str) -> str:
    """Run the Gmail assistant with two read-only tools."""

    client = ai.Client()

    response = client.chat.completions.create(
        model="openai:gpt-4.1",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a Gmail email assistant. "
                    "Use the available tools to fulfill the user's request. "
                    "Search for messages before retrieving their metadata. "
                    "Only mark a message as read when explicitly requested. "
                    "The mark_email_as_read tool enforces user approval. "
                    "Never bypass or misrepresent the approval result. "
                    "If the user cancels, report that no modification was made. "
                    "Do not invent email details or claim actions succeeded "
                    "unless the tool confirms success."
                    "Only mark a message as unread when explicitly requested. "
                    "The mark_email_as_unread tool requires user approval. "
                    "Never report a modification as successful if approval "
                    "was denied or the tool failed. "
                    "Use short Gmail search phrases to discover candidate messages. "
                    "Do not use long quoted subjects or date filters unless necessary. "
                    "When a specific message is requested, use get_email to verify "
                    "its exact sender, subject, and date before "
                    "requesting modification. "
                    "If no exact match exists or multiple candidates remain ambiguous, "
                    "do not perform any modification. "
                    "Create an email draft only when the user explicitly requests one. "
                    "Provide a clear, concise subject and plain-text body. "
                    "The create_draft tool requires human approval. "
                    "Never claim a draft was saved unless the tool reports success. "
                    "Never send an email. "
                    "If draft creation is denied or cancelled, do not retry it "
                    "within the same request. "
                ),
            },
            {"role": "user", "content": request},
        ],
        tools=[
            search_unread_from_sender,
            search_emails,
            get_email,
            mark_email_as_read,
            mark_email_as_unread,
            create_draft,
        ],
        max_turns=6,
    )

    return response.choices[0].message.content or ""
