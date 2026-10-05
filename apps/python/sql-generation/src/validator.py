def validate_read_only_sql(query: str) -> tuple[bool, str]:
    normalized_query = query.strip().lower()

    if not normalized_query:
        return False, "SQL query is empty."

    if not normalized_query.startswith("select"):
        return False, "Only SELECT queries are allowed."

    forbidden_keywords = (
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "create",
        "replace",
        "truncate",
        "attach",
        "detach",
        "pragma",
    )

    for keyword in forbidden_keywords:
        if keyword in normalized_query:
            return False, f"Forbidden SQL keyword detected: {keyword}"

    return True, ""
