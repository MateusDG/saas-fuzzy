import argparse
import csv
import gzip
import json
from pathlib import Path

import pytest

from app.preprocess_amazon_reviews_2023 import preprocess


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as target:
        for row in rows:
            target.write(json.dumps(row, ensure_ascii=True) + "\n")


def _write_jsonl_gz(path: Path, rows: list[dict]) -> None:
    with gzip.open(path, "wt", encoding="utf-8") as target:
        for row in rows:
            target.write(json.dumps(row, ensure_ascii=True) + "\n")


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as source:
        return list(csv.DictReader(source))


def _sample_metadata_rows() -> list[dict]:
    return [
        {
            "parent_asin": "H1",
            "main_category": "Home & Kitchen",
            "categories": ["Home & Kitchen", "Cookware"],
            "title": "Home Item 1",
            "store": "Brand A",
            "average_rating": 4.5,
            "rating_number": 30,
            "price": 100.0,
        },
        {
            "parent_asin": "H2",
            "main_category": "Home & Kitchen",
            "categories": ["Home & Kitchen", "Cookware"],
            "title": "Home Item 2",
            "store": "Brand A",
            "average_rating": 4.6,
            "rating_number": 35,
            "price": 200.0,
        },
        {
            "parent_asin": "H3",
            "main_category": "Home & Kitchen",
            "categories": ["Home & Kitchen", "Cookware"],
            "title": "Home Item 3",
            "store": "Brand B",
            "average_rating": 4.7,
            "rating_number": 40,
            "price": 260.0,
        },
        {
            "parent_asin": "H4",
            "main_category": "Home & Kitchen",
            "categories": ["Home & Kitchen", "Cookware"],
            "title": "Home Item 4",
            "store": "Brand C",
            "average_rating": 4.8,
            "rating_number": 45,
            "price": 320.0,
        },
        {
            "parent_asin": "P1",
            "main_category": "Appliances",
            "categories": ["Appliances", "Small Appliances"],
            "title": "Appliance 1",
            "store": "Brand D",
            "average_rating": 4.1,
            "rating_number": 30,
            "price": 80.0,
        },
        {
            "parent_asin": "P2",
            "main_category": "Appliances",
            "categories": ["Appliances", "Small Appliances"],
            "title": "Appliance 2",
            "store": "Brand D",
            "average_rating": 4.2,
            "rating_number": 30,
            "price": 160.0,
        },
        {
            "parent_asin": "P3",
            "main_category": "Appliances",
            "categories": ["Appliances", "Small Appliances"],
            "title": "Appliance 3",
            "store": "Brand E",
            "average_rating": 4.6,
            "rating_number": 40,
            "price": 240.0,
        },
        {
            "parent_asin": "PX",
            "main_category": "Appliances",
            "categories": ["Appliances"],
            "title": "No Price",
            "store": "Brand F",
            "average_rating": 4.9,
            "rating_number": 50,
            "price": None,
        },
    ]


def _sample_review_rows() -> list[dict]:
    return [
        {"user_id": "u1", "parent_asin": "P3", "rating": 5.0, "timestamp": 1000, "verified_purchase": True},
        {"user_id": "u1", "parent_asin": "H4", "rating": 5.0, "timestamp": 2000, "verified_purchase": True},
        {"user_id": "u2", "parent_asin": "H4", "rating": 5.0, "timestamp": 1100, "verified_purchase": True},
        {"user_id": "u2", "parent_asin": "P3", "rating": 5.0, "timestamp": 2200, "verified_purchase": True},
        {"user_id": "u3", "parent_asin": "P3", "rating": 4.0, "timestamp": 1200, "verified_purchase": True},
        {"user_id": "u3", "parent_asin": "H4", "rating": 4.0, "timestamp": 2300, "verified_purchase": True},
        {"user_id": "u4", "parent_asin": "H1", "rating": 5.0, "timestamp": 1300, "verified_purchase": True},
        {"user_id": "u4", "parent_asin": "H2", "rating": 5.0, "timestamp": 2400, "verified_purchase": True},
        {"user_id": "u5", "parent_asin": "H4", "rating": 5.0, "timestamp": 2500, "verified_purchase": False},
    ]


def _build_args(tmp_path: Path, reviews_file: Path, metadata_file: Path) -> argparse.Namespace:
    return argparse.Namespace(
        reviews_file=reviews_file,
        metadata_file=metadata_file,
        output_dir=tmp_path / "processed",
        dataset_profile_output=tmp_path / "dataset_profile.json",
        categories=["Home_and_Kitchen", "Appliances"],
        premium_percentile=0.75,
        min_rating=4.0,
        min_item_interactions=2,
        min_user_interactions=2,
        require_verified_purchase=False,
        max_users=None,
        max_items=None,
        seed=42,
    )


def test_preprocess_generates_expected_outputs_from_jsonl(tmp_path: Path) -> None:
    reviews_file = tmp_path / "reviews.jsonl"
    metadata_file = tmp_path / "metadata.jsonl"
    _write_jsonl(reviews_file, _sample_review_rows())
    _write_jsonl(metadata_file, _sample_metadata_rows())

    args = _build_args(tmp_path, reviews_file, metadata_file)
    result = preprocess(args)

    train_rows = _read_csv(result["train_path"])
    test_rows = _read_csv(result["test_path"])
    items_rows = _read_csv(result["items_path"])

    assert {row["item_id"] for row in items_rows} == {"H4", "P3"}
    assert all(row["event_name"] == "positive_review" for row in train_rows)
    assert len(test_rows) == 3
    assert len(train_rows) == 3

    train_items_by_user = {}
    for row in train_rows:
        train_items_by_user.setdefault(row["user_id"], set()).add(row["item_id"])

    for row in test_rows:
        assert row["item_id"] not in train_items_by_user.get(row["user_id"], set())
        assert row["relevance"] == "1"

    profile = json.loads(Path(result["profile_path"]).read_text(encoding="utf-8"))
    assert profile["dataset"] == "Amazon Reviews 2023"
    assert profile["counts"]["users"] == 3
    assert profile["counts"]["items"] == 2
    assert profile["counts"]["items_removed_missing_price"] >= 1


def test_preprocess_supports_jsonl_gz_and_verified_filter(tmp_path: Path) -> None:
    reviews_file = tmp_path / "reviews.jsonl.gz"
    metadata_file = tmp_path / "metadata.jsonl.gz"
    _write_jsonl_gz(reviews_file, _sample_review_rows())
    _write_jsonl_gz(metadata_file, _sample_metadata_rows())

    args = _build_args(tmp_path, reviews_file, metadata_file)
    args.require_verified_purchase = True
    result = preprocess(args)

    train_rows = _read_csv(result["train_path"])
    test_rows = _read_csv(result["test_path"])
    assert train_rows
    assert test_rows
    assert all(row["user_id"] != "u5" for row in train_rows + test_rows)


def test_preprocess_missing_input_files_fails_with_clear_message(tmp_path: Path) -> None:
    args = _build_args(
        tmp_path=tmp_path,
        reviews_file=tmp_path / "missing_reviews.jsonl",
        metadata_file=tmp_path / "missing_metadata.jsonl",
    )

    with pytest.raises(FileNotFoundError, match="Missing required input file"):
        preprocess(args)
