"""CLI entry point for the Agentic AI Email Assistant."""

import os

from dotenv import load_dotenv

from .agent import run_agent
from .privacy import mask_email


def main() -> None:
    """Execute a natural-language Gmail request."""

    load_dotenv()

    recipient = os.getenv("GMAIL_TEST_RECIPIENT", "").strip()

    if not recipient:
        print("Error: GMAIL_TEST_RECIPIENT is not configured.")
        return

    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY is not configured.")
        return

    request = (
        f"Create a Gmail draft addressed to {recipient}. "
        "Write a short, professional email introducing my "
        "Agentic AI Email Assistant project. "
        "Mention that it uses Python, AISuite, and the Gmail API "
        "to demonstrate LLM tool calling and human approval. "
        "Keep the message under 100 words. "
        "Save it as a draft only. Do not send it."
    )

    # request = (
    #     "Find emails from no-reply@zoom.us with "
    #     "'Missed the Webinar' in the subject. "
    #     "Retrieve the metadata and identify the email "
    #     "whose exact subject is "
    #     "'Missed the Webinar? Watch the Replay | "
    #     "Exclusive AI Webinar Deals Close Today at 4:00 PM ET' "
    #     "and whose Date header is November 2, 2026. "
    #     "Mark only that message as unread. "
    #     "Do not modify any other messages."
    # )

    # request = (
    #     "Find upto 3 emails with AI in the subject and tell me how many you found."
    # )

    print("Agentic AI Email Assistant")
    print(f"[USER] {request.replace(recipient, mask_email(recipient))}")

    try:
        result = run_agent(request)
        print(f"\n[AGENT RESPONSE] \n{result}")

    except Exception as error:
        print(f"Agent execution failed: {type(error).__name__}")
        raise


if __name__ == "__main__":
    main()
