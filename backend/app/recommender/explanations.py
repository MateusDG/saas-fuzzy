def add_reason(reasons: list[str], message: str) -> None:
    if message and message not in reasons:
        reasons.append(message)
