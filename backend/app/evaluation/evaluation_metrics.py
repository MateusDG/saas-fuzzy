import math
from collections.abc import Iterable, Mapping, Sequence


def _validate_k(k: int) -> None:
    if k <= 0:
        raise ValueError("k must be greater than zero")


def _unique_relevant(relevant_items: Iterable[str]) -> set[str]:
    return {item for item in relevant_items if item}


def precision_at_k(recommended: Sequence[str], relevant_items: Iterable[str], k: int) -> float:
    _validate_k(k)
    relevant_set = _unique_relevant(relevant_items)
    if not relevant_set:
        return 0.0

    top_k = [item for item in recommended[:k] if item]
    hits = len(set(top_k).intersection(relevant_set))
    return hits / float(k)


def recall_at_k(recommended: Sequence[str], relevant_items: Iterable[str], k: int) -> float:
    _validate_k(k)
    relevant_set = _unique_relevant(relevant_items)
    if not relevant_set:
        return 0.0

    top_k = [item for item in recommended[:k] if item]
    hits = len(set(top_k).intersection(relevant_set))
    return hits / float(len(relevant_set))


def dcg_at_k(
    recommended: Sequence[str],
    relevance_by_item: Mapping[str, float],
    k: int,
) -> float:
    _validate_k(k)
    score = 0.0
    for position, item_id in enumerate(recommended[:k]):
        relevance = float(relevance_by_item.get(item_id, 0.0))
        if relevance <= 0:
            continue
        score += relevance / math.log2(position + 2)
    return score


def ndcg_at_k(
    recommended: Sequence[str],
    relevant_items: Iterable[str],
    k: int,
    relevance_by_item: Mapping[str, float] | None = None,
) -> float:
    _validate_k(k)
    relevant_set = _unique_relevant(relevant_items)
    if not relevant_set:
        return 0.0

    if relevance_by_item is None:
        relevance_by_item = {item_id: 1.0 for item_id in relevant_set}

    observed_dcg = dcg_at_k(recommended, relevance_by_item, k)
    ideal_relevances = sorted(
        (float(relevance_by_item.get(item_id, 0.0)) for item_id in relevant_set),
        reverse=True,
    )[:k]

    ideal_dcg = 0.0
    for position, relevance in enumerate(ideal_relevances):
        if relevance <= 0:
            continue
        ideal_dcg += relevance / math.log2(position + 2)

    if ideal_dcg == 0.0:
        return 0.0
    return observed_dcg / ideal_dcg


def catalog_coverage(
    recommendation_lists: Sequence[Sequence[str]],
    catalog_items: Iterable[str],
) -> float:
    catalog_set = _unique_relevant(catalog_items)
    if not catalog_set:
        return 0.0

    recommended_union: set[str] = set()
    for recommendation_list in recommendation_lists:
        recommended_union.update(item for item in recommendation_list if item)

    return len(recommended_union.intersection(catalog_set)) / float(len(catalog_set))


def simple_diversity(
    recommendations: Sequence[str],
    item_categories: Mapping[str, str | None],
    k: int,
) -> float:
    _validate_k(k)
    top_k = [item for item in recommendations[:k] if item]
    if len(top_k) < 2:
        return 0.0

    different_pairs = 0
    total_pairs = 0
    for i in range(len(top_k)):
        for j in range(i + 1, len(top_k)):
            total_pairs += 1
            category_i = item_categories.get(top_k[i])
            category_j = item_categories.get(top_k[j])
            if category_i != category_j:
                different_pairs += 1

    if total_pairs == 0:
        return 0.0
    return different_pairs / float(total_pairs)


def policy_action_rates(policy_actions: Iterable[str]) -> dict[str, float]:
    actions = [action.strip().lower() for action in policy_actions if action and action.strip()]
    if not actions:
        return {"blocked_rate": 0.0, "demoted_rate": 0.0}

    blocked = sum(1 for action in actions if action == "block")
    demoted = sum(1 for action in actions if action in {"demote", "review"})
    total = len(actions)
    return {
        "blocked_rate": blocked / float(total),
        "demoted_rate": demoted / float(total),
    }


def mean(values: Iterable[float]) -> float:
    values_list = [float(value) for value in values]
    if not values_list:
        return 0.0
    return sum(values_list) / float(len(values_list))
