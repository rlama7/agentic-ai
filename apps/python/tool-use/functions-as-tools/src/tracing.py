from functools import wraps
from typing import Callable


def trace_tool(func: Callable) -> Callable:
    """Log tool execution while preserving function metadata."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"\n[TOOL START] {func.__name__}")
        print(f"[ARGUMENTS] args={args}, kwargs={kwargs}")

        try:
            # Execute the original Python function
            result = func(*args, **kwargs)

            print(f"[TOOL RESULT] {result}")
            print(f"[TOOL END] {func.__name__}")

            return result

        except Exception as error:
            print(f"[TOOL ERROR] {func.__name__}: {error}")
            raise

    return wrapper
