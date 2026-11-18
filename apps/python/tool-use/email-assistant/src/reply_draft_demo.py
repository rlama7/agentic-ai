"""Create a threaded Gmail reply draft with user approval."""

import os

from dotenv import load_dotenv
from googleapiclient.errors import HttpError

from .approval import request_approval
from .gmail_tools import (
    create_reply_draft,
    get_email_content,
    search_emails,
)
from .privacy import mask_email


def main() -> None:
    """Create an approved reply draft for the test message."""

    load_dotenv()

    allowed_sender = os.getenv("GMAIL_TEST_RECIPIENT", "").strip()

    if not allowed_sender:
        print("GMAIL_TEST_RECIPIENT is not configured.")
        return

    try:
        messages = search_emails(
            'subject:"Agentic AI - Body Retrieval Test"',
            max_results=5,
        )

        # Avoid selecting an ambiguous message automatically.
        matches = [get_email_content(item["id"]) for item in messages]
        matches = [
            email
            for email in matches
            if email["subject"] == "Agentic AI - Body Retrieval Test"
        ]

        if len(matches) != 1:
            print(f"Expected one exact test message; found {len(matches)}.")
            return

        original = matches[0]

        reply_body = (
            "Hello,\n\n"
            "Thank you for your test message. "
            "I successfully retrieved its content using "
            "the Gmail API.\n\n"
            "Best regards,\n"
            "Agentic AI Email Assistant"
        )

        approved = request_approval(
            action="CREATE THREADED REPLY DRAFT",
            details={
                "To": mask_email(allowed_sender),
                "Subject": f"Re: {original['subject']}",
                "Body": reply_body,
            },
        )

        if not approved:
            print("Reply draft cancelled.")
            return

        result = create_reply_draft(
            original_message_id=original["id"],
            reply_body=reply_body,
            allowed_sender=allowed_sender,
        )

        if result["thread_id"] != original["thread_id"]:
            print("Warning: Returned thread ID differs from original.")
            return

        print("Reply draft created in the original Gmail thread.")
        print("No email was sent.")

    except (HttpError, ValueError, FileNotFoundError) as error:
        print(f"Reply draft failed: {error}")


if __name__ == "__main__":
    main()
