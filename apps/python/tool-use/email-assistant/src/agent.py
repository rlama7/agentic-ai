"""AISuite orchestration for the Gmail Email Assistant."""

import aisuite as ai

from .gmail_tools import search_unread_from_sender as gmail_search


def search_unread_from_sender(sender: str) -> list[dict]:
    """
    Find up to two unread Gmail messages from a sender email address.

    Args:
        sender; The sender's comlete email address.
    """
    # Trace the tool invocation without exposing message contents.
    print("\n[TOOL START] search_unread_from_sender")
    print(f"[ARGUMENTS] sender={sender}")

    # Reuse the Gmail tool implemented during Phase 3.
    messages = gmail_search(sender=sender, max_results=2)

    print(f"[TOOL RESUlT] {len(messages)} matching message")
    print("[TOOL END]\n")

    return messages


def run_agent(request: str) -> str:
    """Run a read-noly Gmail agent with one registered tool."""

    client = ai.Client()

    response = client.chat.completions.create(
        model="openai:gpt-4.1",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a read-only Gmail assistant. "
                    "Use the available tool to search the user's Gmail. "
                    "Report the number of matching messages. "
                    "Do not invent email subjects or contents."
                ),
            },
            {"role": "user", "content": request},
        ],
        tools=[search_unread_from_sender],
        max_turns=3,
    )

    return response.choices[0].message.content or ""
