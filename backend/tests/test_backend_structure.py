from pathlib import Path


def test_legacy_wrappers_keep_public_imports_available() -> None:
    from app.evaluation_baselines import recommend_popularity
    from app.evaluation_metrics import precision_at_k
    from app.export_review_pack import generate_review_pack
    from app.preprocess_amazon_reviews_2023 import preprocess
    from app.review_recommendations import generate_review_csv
    from app.run_offline_evaluation import evaluate
    from app.seed import import_products_from_csv

    assert callable(recommend_popularity)
    assert callable(precision_at_k)
    assert callable(generate_review_pack)
    assert callable(preprocess)
    assert callable(generate_review_csv)
    assert callable(evaluate)
    assert callable(import_products_from_csv)


def test_alembic_migrations_are_present() -> None:
    backend_root = Path(__file__).resolve().parents[1]

    assert (backend_root / "alembic.ini").exists()
    assert (backend_root / "alembic" / "env.py").exists()
    assert (backend_root / "alembic" / "versions" / "0001_initial_schema.py").exists()
    assert (backend_root / "alembic" / "versions" / "0002_add_event_analytics_columns.py").exists()
