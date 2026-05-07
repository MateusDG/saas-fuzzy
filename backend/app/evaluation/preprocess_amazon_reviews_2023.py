import argparse
import csv
import gzip
import json
import math
import random
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from ..core.path_policy import resolve_project_path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "public" / "processed"
DEFAULT_PROFILE_PATH = PROJECT_ROOT / "reports" / "evaluation" / "dataset_profile.json"


@dataclass(frozen=True)
class ItemMetadata:
    item_id: str
    category: str
    title: str
    brand: str
    average_rating: float | None
    rating_number: int | None
    price: float | None


@dataclass(frozen=True)
class PositiveInteraction:
    user_id: str
    item_id: str
    timestamp: int


def resolve_path(path: Path, *, label: str) -> Path:
    return resolve_project_path(path, PROJECT_ROOT, label=label)


def to_project_relative_or_name(path: Path) -> str:
    resolved = path.resolve()
    project_root = PROJECT_ROOT.resolve()
    try:
        return str(resolved.relative_to(project_root)).replace("\\", "/")
    except ValueError:
        return resolved.name


def _normalize_tokens(value: str) -> set[str]:
    normalized = value.strip().lower().replace("&", " and ").replace("_", " ").replace("-", " ")
    tokens = re.findall(r"[a-z0-9]+", normalized)
    return {token for token in tokens if token and token != "and"}


def _open_jsonl(path: Path):
    if path.suffix.lower() == ".gz":
        return gzip.open(path, "rt", encoding="utf-8")
    return path.open("r", encoding="utf-8")


def iter_jsonl(path: Path) -> Any:
    with _open_jsonl(path) as source:
        for line_number, line in enumerate(source, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON at {path} line {line_number}") from exc


def _parse_float(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, (float, int)):
        parsed = float(value)
        return parsed if math.isfinite(parsed) else None
    if isinstance(value, str):
        cleaned = value.strip()
        if not cleaned:
            return None
        match = re.search(r"-?\d+(?:\.\d+)?", cleaned.replace(",", ""))
        if not match:
            return None
        try:
            parsed = float(match.group(0))
        except ValueError:
            return None
        return parsed if math.isfinite(parsed) else None
    return None


def _parse_int(value: Any) -> int | None:
    parsed = _parse_float(value)
    if parsed is None:
        return None
    return int(parsed)


def _parse_timestamp(value: Any) -> int | None:
    parsed = _parse_int(value)
    if parsed is None:
        return None
    if parsed <= 0:
        return None
    return parsed


def _parse_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if value is None:
        return None
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"true", "1", "yes", "y"}:
            return True
        if normalized in {"false", "0", "no", "n"}:
            return False
    if isinstance(value, (int, float)):
        return bool(value)
    return None


def _extract_item_id(payload: dict[str, Any]) -> str:
    for field_name in ("parent_asin", "asin", "item_id"):
        value = payload.get(field_name)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def _extract_user_id(payload: dict[str, Any]) -> str:
    for field_name in ("user_id", "reviewerID", "reviewer_id"):
        value = payload.get(field_name)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def _extract_brand(payload: dict[str, Any]) -> str:
    brand_candidate = payload.get("store")
    if isinstance(brand_candidate, str) and brand_candidate.strip():
        return brand_candidate.strip()

    details = payload.get("details")
    if isinstance(details, dict):
        for key_name in ("Brand", "brand"):
            value = details.get(key_name)
            if isinstance(value, str) and value.strip():
                return value.strip()

    for key_name in ("brand",):
        value = payload.get(key_name)
        if isinstance(value, str) and value.strip():
            return value.strip()

    return ""


def _extract_category_values(payload: dict[str, Any]) -> list[str]:
    categories: list[str] = []
    main_category = payload.get("main_category")
    if isinstance(main_category, str) and main_category.strip():
        categories.append(main_category.strip())

    raw_categories = payload.get("categories")
    if isinstance(raw_categories, list):
        for value in raw_categories:
            if isinstance(value, str) and value.strip():
                categories.append(value.strip())
    return categories


def _match_category(
    category_values: list[str],
    category_matchers: list[tuple[str, set[str]]],
) -> str | None:
    for category_value in category_values:
        value_tokens = _normalize_tokens(category_value)
        if not value_tokens:
            continue
        for category_name, matcher_tokens in category_matchers:
            if matcher_tokens and matcher_tokens.issubset(value_tokens):
                return category_name
    return None


def percentile(values: list[float], q: float) -> float:
    if not values:
        raise ValueError("Cannot compute percentile from an empty sequence")
    if q < 0 or q > 1:
        raise ValueError("Percentile q must be between 0 and 1")

    sorted_values = sorted(values)
    if len(sorted_values) == 1:
        return sorted_values[0]

    position = (len(sorted_values) - 1) * q
    lower = int(math.floor(position))
    upper = int(math.ceil(position))
    if lower == upper:
        return sorted_values[lower]

    weight = position - lower
    return sorted_values[lower] * (1.0 - weight) + sorted_values[upper] * weight


def classify_price_band(price: float | None, p75: float, p90: float) -> str:
    if price is None:
        return "unknown"
    if price < p75:
        return "standard"
    if price >= p90:
        return "ultra_premium"
    return "premium"


def validate_input_files(reviews_file: Path, metadata_file: Path) -> None:
    missing_paths = [path for path in (reviews_file, metadata_file) if not path.exists()]
    if not missing_paths:
        return
    missing_labels = ", ".join(str(path) for path in missing_paths)
    raise FileNotFoundError(f"Missing required input file(s): {missing_labels}")


def load_metadata_items(
    metadata_path: Path,
    categories: list[str],
    min_rating: float,
) -> tuple[dict[str, ItemMetadata], dict[str, int]]:
    category_matchers = [(name, _normalize_tokens(name)) for name in categories]
    stats = {
        "metadata_rows_total": 0,
        "metadata_rows_invalid_item": 0,
        "metadata_rows_outside_categories": 0,
        "items_removed_low_average_rating": 0,
    }
    items_by_id: dict[str, ItemMetadata] = {}

    for record in iter_jsonl(metadata_path):
        if not isinstance(record, dict):
            continue

        stats["metadata_rows_total"] += 1
        item_id = _extract_item_id(record)
        if not item_id:
            stats["metadata_rows_invalid_item"] += 1
            continue

        category = _match_category(_extract_category_values(record), category_matchers)
        if not category:
            stats["metadata_rows_outside_categories"] += 1
            continue

        average_rating = _parse_float(record.get("average_rating"))
        if average_rating is None or average_rating < min_rating:
            stats["items_removed_low_average_rating"] += 1
            continue

        rating_number = _parse_int(record.get("rating_number"))
        price = _parse_float(record.get("price"))
        if price is not None and price <= 0:
            price = None

        item = ItemMetadata(
            item_id=item_id,
            category=category,
            title=str(record.get("title") or "").strip(),
            brand=_extract_brand(record),
            average_rating=average_rating,
            rating_number=rating_number,
            price=price,
        )
        items_by_id[item_id] = item

    return items_by_id, stats


def load_positive_interactions(
    reviews_path: Path,
    allowed_item_ids: set[str],
    min_rating: float,
    require_verified_purchase: bool,
) -> tuple[list[PositiveInteraction], dict[str, int]]:
    stats = {
        "review_rows_total": 0,
        "review_rows_invalid": 0,
        "review_rows_filtered_by_item": 0,
        "review_rows_filtered_by_rating": 0,
        "review_rows_filtered_by_verified_purchase": 0,
    }
    interactions: list[PositiveInteraction] = []

    for record in iter_jsonl(reviews_path):
        if not isinstance(record, dict):
            continue
        stats["review_rows_total"] += 1

        item_id = _extract_item_id(record)
        user_id = _extract_user_id(record)
        rating = _parse_float(record.get("rating"))
        timestamp = _parse_timestamp(record.get("timestamp") or record.get("sort_timestamp"))
        if not item_id or not user_id or timestamp is None or rating is None:
            stats["review_rows_invalid"] += 1
            continue
        if item_id not in allowed_item_ids:
            stats["review_rows_filtered_by_item"] += 1
            continue
        if rating < min_rating:
            stats["review_rows_filtered_by_rating"] += 1
            continue
        if require_verified_purchase and not _parse_bool(record.get("verified_purchase")):
            stats["review_rows_filtered_by_verified_purchase"] += 1
            continue

        interactions.append(
            PositiveInteraction(
                user_id=user_id,
                item_id=item_id,
                timestamp=timestamp,
            )
        )

    return interactions, stats


def prepare_rows(
    interactions: list[PositiveInteraction],
    min_user_interactions: int,
    max_users: int | None,
    seed: int,
) -> tuple[list[dict[str, str]], list[dict[str, str]], set[str], dict[str, int]]:
    grouped_by_user: dict[str, list[PositiveInteraction]] = defaultdict(list)
    for interaction in interactions:
        grouped_by_user[interaction.user_id].append(interaction)

    prepared_by_user: dict[str, list[PositiveInteraction]] = {}
    removed_users_low_interactions = 0
    for user_id, user_interactions in grouped_by_user.items():
        sorted_rows = sorted(user_interactions, key=lambda row: (row.timestamp, row.item_id))
        if len(sorted_rows) < min_user_interactions:
            removed_users_low_interactions += 1
            continue
        prepared_by_user[user_id] = sorted_rows

    selected_users = sorted(prepared_by_user.keys())
    if max_users is not None and max_users > 0 and len(selected_users) > max_users:
        rng = random.Random(seed)
        selected_users = sorted(rng.sample(selected_users, k=max_users))

    train_rows: list[dict[str, str]] = []
    test_rows: list[dict[str, str]] = []
    used_item_ids: set[str] = set()
    removed_users_no_train_after_leakage_filter = 0

    for user_id in selected_users:
        ordered_events = prepared_by_user[user_id]
        test_event = ordered_events[-1]
        test_item = test_event.item_id
        train_items = [
            (event.item_id, event.timestamp)
            for event in ordered_events[:-1]
            if event.item_id != test_item
        ]
        if not train_items:
            removed_users_no_train_after_leakage_filter += 1
            continue

        emitted_train_items: set[str] = set()
        for train_item, train_timestamp in train_items:
            if train_item in emitted_train_items:
                continue
            emitted_train_items.add(train_item)
            used_item_ids.add(train_item)
            train_rows.append(
                {
                    "user_id": user_id,
                    "item_id": train_item,
                    "event_name": "positive_review",
                    "timestamp": str(train_timestamp),
                }
            )

        used_item_ids.add(test_item)
        test_rows.append(
            {
                "user_id": user_id,
                "item_id": test_item,
                "relevance": "1",
            }
        )

    stats = {
        "users_total": len(grouped_by_user),
        "users_removed_low_interactions": removed_users_low_interactions,
        "users_removed_no_train_after_leakage_filter": removed_users_no_train_after_leakage_filter,
        "users_evaluated": len({row["user_id"] for row in test_rows}),
    }
    return train_rows, test_rows, used_item_ids, stats


def write_csv_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Preprocess Amazon Reviews 2023 into Kouzina offline evaluation CSVs.",
    )
    parser.add_argument(
        "--reviews-file",
        type=Path,
        required=True,
        help="Path to reviews .jsonl or .jsonl.gz. Relative paths are resolved from repository root.",
    )
    parser.add_argument(
        "--metadata-file",
        type=Path,
        required=True,
        help="Path to metadata .jsonl or .jsonl.gz. Relative paths are resolved from repository root.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=(
            "Directory where interactions_train.csv, interactions_test.csv and items.csv will be written. "
            "Relative paths are resolved from repository root."
        ),
    )
    parser.add_argument(
        "--dataset-profile-output",
        type=Path,
        default=DEFAULT_PROFILE_PATH,
        help="Path to dataset profile JSON output. Relative paths are resolved from repository root.",
    )
    parser.add_argument(
        "--categories",
        nargs="+",
        default=["Home_and_Kitchen", "Appliances"],
        help="Target categories used for initial domain filtering.",
    )
    parser.add_argument(
        "--premium-percentile",
        type=float,
        default=0.75,
        help="Percentile threshold for premium cutoff (e.g., 0.75 for P75).",
    )
    parser.add_argument("--min-rating", type=float, default=4.0, help="Minimum rating for positive interactions.")
    parser.add_argument(
        "--min-item-interactions",
        type=int,
        default=20,
        help="Minimum item support (rating_number or observed positives).",
    )
    parser.add_argument(
        "--min-user-interactions",
        type=int,
        default=2,
        help="Minimum number of unique positive items per evaluated user.",
    )
    parser.add_argument(
        "--require-verified-purchase",
        action="store_true",
        help="When enabled, keeps only rows with verified_purchase=true.",
    )
    parser.add_argument("--max-users", type=int, default=None, help="Optional cap on number of evaluated users.")
    parser.add_argument("--max-items", type=int, default=None, help="Optional cap on number of kept premium items.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed used in capped sampling.")
    return parser.parse_args()


def preprocess(args: argparse.Namespace) -> dict[str, Any]:
    if args.premium_percentile <= 0 or args.premium_percentile > 1:
        raise ValueError("--premium-percentile must be > 0 and <= 1")
    if args.min_item_interactions <= 0:
        raise ValueError("--min-item-interactions must be greater than zero")
    if args.min_user_interactions < 2:
        raise ValueError("--min-user-interactions must be at least 2")

    reviews_path = resolve_path(args.reviews_file, label="input")
    metadata_path = resolve_path(args.metadata_file, label="input")
    output_dir = resolve_path(args.output_dir, label="output")
    dataset_profile_output = resolve_path(args.dataset_profile_output, label="output")
    validate_input_files(reviews_path, metadata_path)

    items_by_id, metadata_stats = load_metadata_items(
        metadata_path=metadata_path,
        categories=args.categories,
        min_rating=args.min_rating,
    )
    if not items_by_id:
        raise ValueError("No metadata items matched the selected categories and item quality filters.")

    interactions, review_stats = load_positive_interactions(
        reviews_path=reviews_path,
        allowed_item_ids=set(items_by_id.keys()),
        min_rating=args.min_rating,
        require_verified_purchase=args.require_verified_purchase,
    )
    if not interactions:
        raise ValueError("No positive interactions matched the configured filters.")

    item_positive_counts: dict[str, int] = defaultdict(int)
    for interaction in interactions:
        item_positive_counts[interaction.item_id] += 1

    eligible_items_before_percentile: dict[str, ItemMetadata] = {}
    removed_missing_price = 0
    removed_low_interactions = 0
    category_prices: dict[str, list[float]] = defaultdict(list)
    for item_id, item in items_by_id.items():
        if item.price is None:
            removed_missing_price += 1
            continue
        support_count = item.rating_number if item.rating_number is not None else item_positive_counts.get(item_id, 0)
        if support_count < args.min_item_interactions or item_positive_counts.get(item_id, 0) <= 0:
            removed_low_interactions += 1
            continue
        eligible_items_before_percentile[item_id] = item
        category_prices[item.category].append(item.price)

    if not eligible_items_before_percentile:
        raise ValueError("No items left after price and item interaction filters.")

    category_percentiles: dict[str, dict[str, float]] = {}
    for category_name, prices in category_prices.items():
        if not prices:
            continue
        p75 = percentile(prices, 0.75)
        p90 = percentile(prices, 0.9)
        premium_threshold = percentile(prices, args.premium_percentile)
        category_percentiles[category_name] = {
            "p75": p75,
            "p90": p90,
            "premium_threshold": premium_threshold,
        }

    premium_items: dict[str, dict[str, Any]] = {}
    for item_id, item in eligible_items_before_percentile.items():
        category_thresholds = category_percentiles.get(item.category)
        if not category_thresholds or item.price is None:
            continue

        premium_threshold = category_thresholds["premium_threshold"]
        price_band = classify_price_band(item.price, category_thresholds["p75"], category_thresholds["p90"])
        if item.price < premium_threshold:
            continue

        premium_items[item_id] = {
            "item_id": item.item_id,
            "category": item.category,
            "brand": item.brand,
            "price_band": price_band,
            "average_rating": item.average_rating,
            "rating_number": item.rating_number,
            "price": item.price,
            "title": item.title,
            "positive_interactions": item_positive_counts.get(item_id, 0),
        }

    if not premium_items:
        raise ValueError("No items matched the premium percentile cutoff in the selected categories.")

    premium_item_ids = set(premium_items.keys())
    if args.max_items is not None and args.max_items > 0 and len(premium_item_ids) > args.max_items:
        ranked_item_ids = sorted(
            premium_item_ids,
            key=lambda item_id: (-int(premium_items[item_id]["positive_interactions"]), item_id),
        )
        premium_item_ids = set(ranked_item_ids[: args.max_items])
        premium_items = {item_id: premium_items[item_id] for item_id in premium_item_ids}

    premium_interactions = [row for row in interactions if row.item_id in premium_item_ids]
    if not premium_interactions:
        raise ValueError("No interactions remained after applying premium item filters.")

    train_rows, test_rows, used_item_ids, user_stats = prepare_rows(
        interactions=premium_interactions,
        min_user_interactions=args.min_user_interactions,
        max_users=args.max_users,
        seed=args.seed,
    )
    if not train_rows or not test_rows:
        raise ValueError("No train/test rows were produced. Adjust filters to keep more users and items.")

    items_rows: list[dict[str, str]] = []
    for item_id in sorted(used_item_ids):
        item = premium_items.get(item_id)
        if item is None:
            continue
        items_rows.append(
            {
                "item_id": item["item_id"],
                "category": item["category"],
                "brand": str(item["brand"] or ""),
                "price_band": str(item["price_band"] or "unknown"),
                "average_rating": "" if item["average_rating"] is None else f"{float(item['average_rating']):.4f}",
                "rating_number": "" if item["rating_number"] is None else str(int(item["rating_number"])),
                "price": "" if item["price"] is None else f"{float(item['price']):.2f}",
                "title": str(item["title"] or ""),
            }
        )

    if not items_rows:
        raise ValueError("No items were left for items.csv after split filtering.")

    train_path = output_dir / "interactions_train.csv"
    test_path = output_dir / "interactions_test.csv"
    items_path = output_dir / "items.csv"

    write_csv_rows(
        train_path,
        fieldnames=["user_id", "item_id", "event_name", "timestamp"],
        rows=sorted(train_rows, key=lambda row: (row["user_id"], row["timestamp"], row["item_id"])),
    )
    write_csv_rows(
        test_path,
        fieldnames=["user_id", "item_id", "relevance"],
        rows=sorted(test_rows, key=lambda row: (row["user_id"], row["item_id"])),
    )
    write_csv_rows(
        items_path,
        fieldnames=[
            "item_id",
            "category",
            "brand",
            "price_band",
            "average_rating",
            "rating_number",
            "price",
            "title",
        ],
        rows=items_rows,
    )

    dataset_profile_output.parent.mkdir(parents=True, exist_ok=True)
    profile = {
        "dataset": "Amazon Reviews 2023",
        "executed_at_utc": datetime.now(UTC).isoformat(),
        "input_files": {
            "reviews_file": to_project_relative_or_name(reviews_path),
            "metadata_file": to_project_relative_or_name(metadata_path),
        },
        "categories_included": args.categories,
        "filters_applied": {
            "premium_percentile": args.premium_percentile,
            "min_rating": args.min_rating,
            "min_item_interactions": args.min_item_interactions,
            "min_user_interactions": args.min_user_interactions,
            "require_verified_purchase": bool(args.require_verified_purchase),
            "max_users": args.max_users,
            "max_items": args.max_items,
        },
        "percentile_thresholds_by_category": category_percentiles,
        "counts": {
            "users": user_stats["users_evaluated"],
            "items": len(items_rows),
            "train_interactions": len(train_rows),
            "test_interactions": len(test_rows),
            "premium_items_before_split": len(premium_items),
            "items_removed_missing_price": removed_missing_price,
            "items_removed_low_interactions": removed_low_interactions,
            "items_removed_low_average_rating": metadata_stats["items_removed_low_average_rating"],
            "users_removed_low_interactions": user_stats["users_removed_low_interactions"],
        },
        "seed": args.seed,
        "validation_status": "pending_client_data",
        "notes": [
            "Premium is treated as a product-level proxy (price percentile), not as consumer profile validation.",
            "This artifact is derived from offline public data preparation and remains pending real behavior validation.",
        ],
    }
    dataset_profile_output.write_text(json.dumps(profile, ensure_ascii=True, indent=2), encoding="utf-8")

    return {
        "train_path": train_path,
        "test_path": test_path,
        "items_path": items_path,
        "profile_path": dataset_profile_output,
        "profile": profile,
        "metadata_stats": metadata_stats,
        "review_stats": review_stats,
    }


def main() -> None:
    args = parse_args()
    try:
        result = preprocess(args)
    except (FileNotFoundError, ValueError) as exc:
        raise SystemExit(str(exc)) from exc

    print("Amazon Reviews 2023 preprocessing complete.")
    print(f"- {result['train_path']}")
    print(f"- {result['test_path']}")
    print(f"- {result['items_path']}")
    print(f"- {result['profile_path']}")


if __name__ == "__main__":
    main()
