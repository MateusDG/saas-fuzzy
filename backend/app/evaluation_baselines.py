from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping, Sequence


DEFAULT_EVENT_WEIGHTS: dict[str, float] = {
    "recommendation_impression": 1.0,
    "recommendation_click": 3.0,
    "recommendation_clicked": 3.0,
    "quote_requested": 4.0,
    "add_to_cart_clicked": 5.0,
    "purchase": 8.0,
}


def _weight_for_event(event_name: str, event_weights: Mapping[str, float]) -> float:
    return float(event_weights.get(event_name, 1.0))


def build_user_seen_items(
    interactions: Sequence[Mapping[str, str]],
    user_field: str = "user_id",
    item_field: str = "item_id",
) -> dict[str, set[str]]:
    seen: dict[str, set[str]] = defaultdict(set)
    for row in interactions:
        user_id = row.get(user_field, "").strip()
        item_id = row.get(item_field, "").strip()
        if not user_id or not item_id:
            continue
        seen[user_id].add(item_id)
    return dict(seen)


def build_item_popularity(
    interactions: Sequence[Mapping[str, str]],
    item_field: str = "item_id",
    event_field: str = "event_name",
    event_weights: Mapping[str, float] | None = None,
) -> dict[str, float]:
    weights = DEFAULT_EVENT_WEIGHTS if event_weights is None else event_weights
    popularity: dict[str, float] = defaultdict(float)

    for row in interactions:
        item_id = row.get(item_field, "").strip()
        if not item_id:
            continue
        event_name = row.get(event_field, "").strip().lower()
        popularity[item_id] += _weight_for_event(event_name, weights)

    return dict(popularity)


def popularity_ranking(popularity_scores: Mapping[str, float]) -> list[str]:
    return sorted(
        popularity_scores,
        key=lambda item_id: (-float(popularity_scores[item_id]), item_id),
    )


def recommend_popularity(
    ranked_items: Sequence[str],
    seen_items: Iterable[str],
    k: int,
) -> list[str]:
    if k <= 0:
        raise ValueError("k must be greater than zero")
    seen_set = {item_id for item_id in seen_items if item_id}
    return [item_id for item_id in ranked_items if item_id not in seen_set][:k]


def build_item_categories(
    items: Sequence[Mapping[str, str]],
    item_field: str = "item_id",
    category_field: str = "category",
) -> dict[str, str]:
    categories: dict[str, str] = {}
    for row in items:
        item_id = row.get(item_field, "").strip()
        category = row.get(category_field, "").strip()
        if not item_id or not category:
            continue
        categories[item_id] = category
    return categories


def build_user_top_category(
    interactions: Sequence[Mapping[str, str]],
    item_categories: Mapping[str, str],
    user_field: str = "user_id",
    item_field: str = "item_id",
    event_field: str = "event_name",
    event_weights: Mapping[str, float] | None = None,
) -> dict[str, str]:
    weights = DEFAULT_EVENT_WEIGHTS if event_weights is None else event_weights
    user_category_scores: dict[str, Counter[str]] = defaultdict(Counter)

    for row in interactions:
        user_id = row.get(user_field, "").strip()
        item_id = row.get(item_field, "").strip()
        if not user_id or not item_id:
            continue
        category = item_categories.get(item_id)
        if not category:
            continue
        event_name = row.get(event_field, "").strip().lower()
        user_category_scores[user_id][category] += _weight_for_event(event_name, weights)

    top_category: dict[str, str] = {}
    for user_id, scores in user_category_scores.items():
        if not scores:
            continue
        sorted_categories = sorted(scores, key=lambda cat: (-scores[cat], cat))
        top_category[user_id] = sorted_categories[0]

    return top_category


def recommend_by_category(
    user_id: str,
    user_top_category: Mapping[str, str],
    item_categories: Mapping[str, str],
    ranked_items: Sequence[str],
    seen_items: Iterable[str],
    k: int,
) -> list[str]:
    if k <= 0:
        raise ValueError("k must be greater than zero")

    seen_set = {item_id for item_id in seen_items if item_id}
    preferred_category = user_top_category.get(user_id)

    if not preferred_category:
        return recommend_popularity(ranked_items, seen_set, k)

    same_category = [
        item_id
        for item_id in ranked_items
        if item_categories.get(item_id) == preferred_category and item_id not in seen_set
    ]

    if len(same_category) >= k:
        return same_category[:k]

    fallback = [
        item_id for item_id in ranked_items
        if item_id not in seen_set and item_id not in same_category
    ]
    return (same_category + fallback)[:k]
