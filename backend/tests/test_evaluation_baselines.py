from app.evaluation_baselines import (
    build_item_categories,
    build_item_popularity,
    build_user_seen_items,
    build_user_top_category,
    popularity_ranking,
    recommend_by_category,
    recommend_popularity,
)


def test_popularity_baseline_build_and_recommend() -> None:
    interactions = [
        {"user_id": "u1", "item_id": "i1", "event_name": "recommendation_click"},
        {"user_id": "u2", "item_id": "i1", "event_name": "recommendation_impression"},
        {"user_id": "u2", "item_id": "i2", "event_name": "add_to_cart_clicked"},
    ]

    popularity = build_item_popularity(interactions)
    ranked = popularity_ranking(popularity)
    seen = {"i2"}
    recommendations = recommend_popularity(ranked, seen, 2)

    assert ranked[0] == "i2"
    assert recommendations[0] == "i1"
    assert "i2" not in recommendations


def test_category_baseline_prefers_user_top_category() -> None:
    items = [
        {"item_id": "i1", "category": "coifa"},
        {"item_id": "i2", "category": "cooktop"},
        {"item_id": "i3", "category": "coifa"},
        {"item_id": "i4", "category": "forno"},
    ]
    interactions = [
        {"user_id": "u1", "item_id": "i1", "event_name": "recommendation_click"},
        {"user_id": "u1", "item_id": "i3", "event_name": "recommendation_click"},
        {"user_id": "u1", "item_id": "i2", "event_name": "recommendation_impression"},
    ]

    item_categories = build_item_categories(items)
    user_top_category = build_user_top_category(interactions, item_categories)
    ranked = ["i2", "i3", "i1", "i4"]
    seen = {"i1"}
    recommendations = recommend_by_category(
        "u1",
        user_top_category,
        item_categories,
        ranked,
        seen,
        k=2,
    )

    assert user_top_category["u1"] == "coifa"
    assert recommendations[0] == "i3"


def test_category_baseline_falls_back_to_popularity_when_user_has_no_profile() -> None:
    ranked = ["i1", "i2", "i3"]
    recommendations = recommend_by_category(
        user_id="u-missing",
        user_top_category={},
        item_categories={"i1": "coifa", "i2": "forno", "i3": "cooktop"},
        ranked_items=ranked,
        seen_items={"i1"},
        k=2,
    )

    assert recommendations == ["i2", "i3"]


def test_build_user_seen_items() -> None:
    interactions = [
        {"user_id": "u1", "item_id": "i1"},
        {"user_id": "u1", "item_id": "i2"},
        {"user_id": "u2", "item_id": "i3"},
    ]
    seen = build_user_seen_items(interactions)

    assert seen["u1"] == {"i1", "i2"}
    assert seen["u2"] == {"i3"}
