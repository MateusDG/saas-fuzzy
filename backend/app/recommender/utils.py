from unicodedata import normalize as unicode_normalize


def normalize_text(value: str | None) -> str:
    if not value:
        return ""

    normalized = unicode_normalize("NFKD", value)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    return " ".join(ascii_text.lower().replace("-", " ").split())


def values_match(left: str | None, right: str | None) -> bool:
    normalized_left = normalize_text(left)
    normalized_right = normalize_text(right)
    return bool(normalized_left and normalized_left == normalized_right)


def price_as_float(value: object) -> float | None:
    if value is None:
        return None

    try:
        price = float(value)
    except (TypeError, ValueError):
        return None

    if price <= 0:
        return None

    return price


def prices_are_close(current_price: object, candidate_price: object) -> bool:
    current = price_as_float(current_price)
    candidate = price_as_float(candidate_price)

    if current is None or candidate is None:
        return False

    relative_difference = abs(current - candidate) / current
    return relative_difference <= 0.30
