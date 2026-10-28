from datetime import datetime


def get_current_time() -> str:
    """
    Returns the current local time as a string.
    """

    return datetime.now().strftime("%H:%M:%S")
