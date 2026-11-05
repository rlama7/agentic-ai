"""Controlled Gmail mark-as-read demonstration."""

from googleapiclient.errors import HttpError

from .gmail_tools import (
    get_email,
    mark_email_as_read,
    search_emails,
)


def main() -> None:
    """Preview and approve one Gmail message modification."""

    try:
        # Find a small number of unread inbox messages.
        messages = search_emails("in:inbox is:unread", max_results=3)

        if not messages:
            print("No unread inbox messages available.")
            return

        # Display candidates so the user can choose.
        for index, message in enumerate(messages, start=1):
            email = get_email(message["id"])
            print(f"{index}. {email['sender']}")
            print(f"   Subject: {email['subject']}")

        selection = input("\nSelect an email number (or Enter to cancel): ")

        if not selection.isdigit():
            print("Cancelled.")
            return

        index = int(selection) - 1

        if not 0 <= index < len(messages):
            print("Invalid selection. No changes made.")
            return

        selected_id = messages[index]["id"]
        selected_email = get_email(selected_id)

        print("\nProposed action: MARK AS READ")
        print(f"From: {selected_email['sender']}")
        print(f"Subject: {selected_email['subject']}")

        # Require explicit confirmation before modifying Gmail.
        confirmation = input("\nConfirm action? Type YES: ")

        if confirmation != "YES":
            print("Cancelled. No changes made.")
            return

        result = mark_email_as_read(selected_id)

        print(f"\nModification successful: {result['read']}")

    except (HttpError, ValueError, FileNotFoundError) as error:
        print(f"Gmail operation failed: {error}")


if __name__ == "__main__":
    main()
