"""Privacy utilities for safe CLI logging."""


def mask_email(email: str) -> str:
    """Mask the local part of an email while preserving its domain."""

    # Split on the final @ to separate local part and domain.
    local, separator, domain = email.strip().rpartition("@")

    # Avoid exposing malformed email addresses
    if not separator or not local or not domain:
        return "***"

    # Show only the first two characters of the local part.
    return f"{local[:2]}***@{domain}"
