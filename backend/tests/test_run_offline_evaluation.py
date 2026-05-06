from app.run_offline_evaluation import evaluate


def test_evaluate_returns_summary_and_per_user_rows() -> None:
    interactions_train = [
        {"user_id": "u1", "item_id": "i1", "event_name": "recommendation_click"},
        {"user_id": "u1", "item_id": "i2", "event_name": "recommendation_impression"},
        {"user_id": "u2", "item_id": "i3", "event_name": "add_to_cart_clicked"},
        {"user_id": "u2", "item_id": "i1", "event_name": "recommendation_impression"},
    ]
    interactions_test = [
        {"user_id": "u1", "item_id": "i3", "relevance": "1"},
        {"user_id": "u2", "item_id": "i2", "relevance": "1"},
    ]
    items = [
        {"item_id": "i1", "category": "coifa"},
        {"item_id": "i2", "category": "cooktop"},
        {"item_id": "i3", "category": "forno"},
    ]

    summary, per_user_rows = evaluate(
        interactions_train=interactions_train,
        interactions_test=interactions_test,
        items=items,
        k=2,
    )

    assert summary["k"] == 2
    assert "popularity" in summary["baselines"]
    assert "content_category" in summary["baselines"]
    assert len(per_user_rows) == 4
