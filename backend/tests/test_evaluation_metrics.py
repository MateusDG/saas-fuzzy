from app.evaluation_metrics import (
    catalog_coverage,
    dcg_at_k,
    ndcg_at_k,
    policy_action_rates,
    precision_at_k,
    recall_at_k,
    simple_diversity,
)


def test_precision_and_recall_at_k() -> None:
    recommended = ["a", "b", "c", "d"]
    relevant = {"b", "d", "x"}

    assert precision_at_k(recommended, relevant, 3) == 1.0 / 3.0
    assert recall_at_k(recommended, relevant, 3) == 1.0 / 3.0


def test_dcg_and_ndcg_at_k() -> None:
    recommended = ["a", "b", "c"]
    relevance = {"a": 3.0, "b": 2.0, "c": 1.0}

    observed_dcg = dcg_at_k(recommended, relevance, 3)
    ideal_ndcg = ndcg_at_k(recommended, relevance.keys(), 3, relevance_by_item=relevance)

    assert observed_dcg > 0
    assert ideal_ndcg == 1.0


def test_catalog_coverage() -> None:
    recommendation_lists = [["a", "b"], ["b", "c"]]
    catalog = {"a", "b", "c", "d"}

    assert catalog_coverage(recommendation_lists, catalog) == 0.75


def test_simple_diversity() -> None:
    recommendations = ["a", "b", "c"]
    categories = {
        "a": "coifa",
        "b": "coifa",
        "c": "cooktop",
    }

    diversity = simple_diversity(recommendations, categories, 3)
    assert diversity == 2.0 / 3.0


def test_policy_action_rates() -> None:
    actions = ["boost", "block", "demote", "review", "allow"]
    rates = policy_action_rates(actions)

    assert rates["blocked_rate"] == 0.2
    assert rates["demoted_rate"] == 0.4
