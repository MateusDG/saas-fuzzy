import argparse
import csv
import json
from pathlib import Path

from ..core.path_policy import resolve_project_path
from .evaluation_baselines import (
    build_item_categories,
    build_item_popularity,
    build_user_seen_items,
    build_user_top_category,
    popularity_ranking,
    recommend_by_category,
    recommend_popularity,
)
from .evaluation_metrics import (
    catalog_coverage,
    mean,
    ndcg_at_k,
    policy_action_rates,
    precision_at_k,
    recall_at_k,
    simple_diversity,
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_TRAIN = PROJECT_ROOT / "data" / "public" / "processed" / "interactions_train.csv"
DEFAULT_TEST = PROJECT_ROOT / "data" / "public" / "processed" / "interactions_test.csv"
DEFAULT_ITEMS = PROJECT_ROOT / "data" / "public" / "processed" / "items.csv"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "reports" / "evaluation"


def resolve_path(path: Path) -> Path:
    return resolve_project_path(path, PROJECT_ROOT, label="path")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        return [{key: value or "" for key, value in row.items()} for row in csv.DictReader(csv_file)]


def build_relevant_items_by_user(
    rows: list[dict[str, str]],
    user_field: str = "user_id",
    item_field: str = "item_id",
    relevance_field: str = "relevance",
) -> dict[str, set[str]]:
    relevant: dict[str, set[str]] = {}
    for row in rows:
        user_id = row.get(user_field, "").strip()
        item_id = row.get(item_field, "").strip()
        if not user_id or not item_id:
            continue

        relevance_raw = row.get(relevance_field, "").strip()
        relevance = 1.0
        if relevance_raw:
            try:
                relevance = float(relevance_raw)
            except ValueError:
                relevance = 0.0
        if relevance <= 0:
            continue

        relevant.setdefault(user_id, set()).add(item_id)

    return relevant


def _policy_actions_from_rows(rows: list[dict[str, str]]) -> list[str]:
    return [row.get("relation_policy_action", "").strip() for row in rows if row.get("relation_policy_action")]


def evaluate(
    interactions_train: list[dict[str, str]],
    interactions_test: list[dict[str, str]],
    items: list[dict[str, str]],
    k: int,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    popularity_scores = build_item_popularity(interactions_train)
    popularity_ranked = popularity_ranking(popularity_scores)
    item_categories = build_item_categories(items)
    user_seen_train = build_user_seen_items(interactions_train)
    user_top_category = build_user_top_category(interactions_train, item_categories)
    relevant_by_user = build_relevant_items_by_user(interactions_test)
    catalog_items = list(item_categories.keys())

    per_user_rows: list[dict[str, object]] = []
    recommendations_by_baseline: dict[str, list[list[str]]] = {
        "popularity": [],
        "content_category": [],
    }
    diversity_values: dict[str, list[float]] = {
        "popularity": [],
        "content_category": [],
    }

    for user_id, relevant_items in sorted(relevant_by_user.items()):
        seen_items = user_seen_train.get(user_id, set())

        baseline_recommendations = {
            "popularity": recommend_popularity(popularity_ranked, seen_items, k),
            "content_category": recommend_by_category(
                user_id,
                user_top_category,
                item_categories,
                popularity_ranked,
                seen_items,
                k,
            ),
        }

        for baseline_name, recommended in baseline_recommendations.items():
            recommendations_by_baseline[baseline_name].append(recommended)
            diversity = simple_diversity(recommended, item_categories, k)
            diversity_values[baseline_name].append(diversity)

            per_user_rows.append(
                {
                    "baseline": baseline_name,
                    "user_id": user_id,
                    "precision_at_k": precision_at_k(recommended, relevant_items, k),
                    "recall_at_k": recall_at_k(recommended, relevant_items, k),
                    "ndcg_at_k": ndcg_at_k(recommended, relevant_items, k),
                    "diversity_at_k": diversity,
                    "recommended_items": ",".join(recommended),
                    "relevant_items": ",".join(sorted(relevant_items)),
                }
            )

    summary: dict[str, object] = {
        "k": k,
        "counts": {
            "train_rows": len(interactions_train),
            "test_rows": len(interactions_test),
            "items_rows": len(items),
            "users_evaluated": len(relevant_by_user),
        },
        "baselines": {},
    }

    policy_rates = policy_action_rates(_policy_actions_from_rows(interactions_test))
    for baseline_name in ("popularity", "content_category"):
        baseline_rows = [row for row in per_user_rows if row["baseline"] == baseline_name]
        summary["baselines"][baseline_name] = {
            "precision_at_k": mean(row["precision_at_k"] for row in baseline_rows),
            "recall_at_k": mean(row["recall_at_k"] for row in baseline_rows),
            "ndcg_at_k": mean(row["ndcg_at_k"] for row in baseline_rows),
            "catalog_coverage": catalog_coverage(
                recommendations_by_baseline[baseline_name],
                catalog_items,
            ),
            "simple_diversity": mean(diversity_values[baseline_name]),
            "policy_blocked_rate": policy_rates["blocked_rate"],
            "policy_demoted_rate": policy_rates["demoted_rate"],
        }

    return summary, per_user_rows


def write_per_user_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "baseline",
        "user_id",
        "precision_at_k",
        "recall_at_k",
        "ndcg_at_k",
        "diversity_at_k",
        "recommended_items",
        "relevant_items",
    ]
    with path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run offline evaluation baselines over prepared CSV datasets.",
    )
    parser.add_argument(
        "--train",
        type=Path,
        default=DEFAULT_TRAIN,
        help="Train interactions CSV path. Relative paths are resolved from repository root.",
    )
    parser.add_argument(
        "--test",
        type=Path,
        default=DEFAULT_TEST,
        help="Test interactions CSV path. Relative paths are resolved from repository root.",
    )
    parser.add_argument(
        "--items",
        type=Path,
        default=DEFAULT_ITEMS,
        help="Items CSV path. Relative paths are resolved from repository root.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Output directory path. Relative paths are resolved from repository root.",
    )
    parser.add_argument("--top-k", type=int, default=10, help="Top-k cutoff for ranking metrics.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    train_path = resolve_path(args.train)
    test_path = resolve_path(args.test)
    items_path = resolve_path(args.items)
    output_dir = resolve_path(args.output_dir)

    interactions_train = read_csv_rows(train_path)
    interactions_test = read_csv_rows(test_path)
    items = read_csv_rows(items_path)

    summary, per_user_rows = evaluate(
        interactions_train=interactions_train,
        interactions_test=interactions_test,
        items=items,
        k=args.top_k,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = output_dir / "metrics_summary.json"
    per_user_path = output_dir / "per_user_metrics.csv"
    summary_path.write_text(json.dumps(summary, ensure_ascii=True, indent=2), encoding="utf-8")
    write_per_user_csv(per_user_path, per_user_rows)

    print(f"Offline evaluation written to {output_dir}")
    print(f"- {summary_path.name}")
    print(f"- {per_user_path.name}")


if __name__ == "__main__":
    main()
