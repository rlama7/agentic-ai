"""Human approval controls for agent-initiaged actions."""


def request_approval(action: str, details: dict[str, str]) -> bool:
    """Require explicit CLI approval before executing an action."""

    print("\n[APPROVAL REQUIRED]")
    print(f"Proposed action: {action}")

    # Display relevant details so the user can review the action
    for field, value in details.items():
        print(f"{field}: {value}")

    try:
        # Only an exact YES grants approval
        response = input("\nType YES to approve: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nApproval interrupted.")
        return False
    return response == "YES"
