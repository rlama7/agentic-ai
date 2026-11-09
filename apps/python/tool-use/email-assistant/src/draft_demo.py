"""Demonstrate creating a Gmail draft with human approval."""

from googleapiclient.errors import HttpError

from .approval import request_approval
from .gmail_tools import create_draft


def main() -> None:
    """Create one approved draft without sending it."""

    # Enter the dedicated Gmail test account address
    recipient = input("Test Gmail recipient: ").strip()

    subject = "Agentic AI Email Assistant - Draft Test"
    body = (
        "Hello,\n\n"
        "This is a test draft created using Python "
        "and the Gmail API.\n\n "
        "Best regards,\n"
        "Agentic AI Email Assistant"
    )

    approved = request_approval(
        action="CREATE GMAIL DRAFT",
        details={
            "To": recipient,
            "Subject": subject,
            "Body": body,
        },
    )

    if not approved:
        print("Draft creation cancelled.")
        return

    try:
        result = create_draft(recipient, subject, body)
        print(f"\nResult: {result['status']}")
        print("Draft saved successfully. No email was sent.")

    except (HttpError, ValueError) as error:
        print(f"Draft creation failed: {error}")


if __name__ == "__main__":
    main()
