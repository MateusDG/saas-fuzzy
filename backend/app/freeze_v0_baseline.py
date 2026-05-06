import argparse
import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from sqlalchemy.orm import Session

from .database import SessionLocal, init_db
from .relation_policy import get_relation_policy
from .recommender import normalize_text, recommend_from_catalog
from .review_recommendations import (
    filter_products_by_type,
    get_active_store_products,
    sample_products_by_type,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = PROJECT_ROOT / "reports" / "baselines" / "v0_baseline_snapshot.json"


@dataclass(frozen=True)
class FreezeStats:
    source_products: int
    recommendation_rows: int
    fingerprint: str
    output_path: Path


def resolve_output_path(output: Path) -> Path:
    if output.is_absolute():
        return output
    return PROJECT_ROOT / output


def _item_price(value: object) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def build_v0_snapshot_rows(
    source_products: list,
    all_products: list,
    top_k: int,
) -> list[dict[str, object]]:
    products_by_external_id = {product.external_id: product for product in all_products}
    rows: list[dict[str, object]] = []

    for source in source_products:
        recommendations = recommend_from_catalog(source, all_products, limit=top_k)
        for rank, recommendation in enumerate(recommendations, start=1):
            recommended = products_by_external_id.get(recommendation.product_id)
            if recommended is None:
                continue

            policy = get_relation_policy(source.product_type, recommended.product_type)
            rows.append(
                {
                    "source_product_id": source.external_id,
                    "source_product_type": source.product_type or "",
                    "recommended_product_id": recommended.external_id,
                    "recommended_product_type": recommended.product_type or "",
                    "rank": rank,
                    "score": float(recommendation.score),
                    "reason": recommendation.reason,
                    "relation_class": policy.relation_class,
                    "relation_type": policy.relation_type,
                    "relation_policy_action": policy.default_action,
                    "validation_status": policy.validation_status,
                    "is_quote_only": (
                        normalize_text(getattr(recommended, "availability_text", None)) == "sob consulta"
                    ),
                    "recommended_price": _item_price(recommended.price),
                }
            )

    rows.sort(
        key=lambda row: (
            str(row["source_product_id"]),
            int(row["rank"]),
            str(row["recommended_product_id"]),
        )
    )
    return rows


def _fingerprint_rows(rows: list[dict[str, object]]) -> str:
    canonical = json.dumps(rows, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def freeze_v0_baseline(
    db: Session,
    output_path: Path = DEFAULT_OUTPUT,
    limit_products: int = 30,
    top_k: int = 4,
    product_type: str | None = None,
) -> FreezeStats:
    all_products = get_active_store_products(db)
    filtered_products = filter_products_by_type(all_products, product_type)
    source_products = sample_products_by_type(filtered_products, limit_products)

    rows = build_v0_snapshot_rows(source_products, all_products, top_k=top_k)
    fingerprint = _fingerprint_rows(rows)

    payload = {
        "snapshot_name": "kouzina_reco_v0_baseline",
        "snapshot_version": "phase_5_baseline_v0",
        "generated_at": datetime.now(UTC).isoformat(),
        "source": {
            "ranking": "v0_rules_with_phase_4_9_policy_guardrails",
            "limit_products": limit_products,
            "top_k": top_k,
            "product_type_filter": product_type,
        },
        "counts": {
            "source_products": len(source_products),
            "recommendation_rows": len(rows),
        },
        "fingerprint_sha256": fingerprint,
        "rows": rows,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2),
        encoding="utf-8",
    )

    return FreezeStats(
        source_products=len(source_products),
        recommendation_rows=len(rows),
        fingerprint=fingerprint,
        output_path=output_path,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Freeze the current v0 recommender behavior into a baseline snapshot.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output JSON path. Defaults to reports/baselines/v0_baseline_snapshot.json.",
    )
    parser.add_argument(
        "--limit-products",
        type=int,
        default=30,
        help="Maximum number of source products to include in snapshot.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=4,
        help="Recommendations per source product in snapshot.",
    )
    parser.add_argument(
        "--product-type",
        type=str,
        default=None,
        help="Optional source product_type filter.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_path = resolve_output_path(args.output)

    init_db()
    db = SessionLocal()
    try:
        stats = freeze_v0_baseline(
            db,
            output_path=output_path,
            limit_products=args.limit_products,
            top_k=args.top_k,
            product_type=args.product_type,
        )
    finally:
        db.close()

    print(
        "Frozen v0 baseline with "
        f"{stats.source_products} source products and {stats.recommendation_rows} rows "
        f"at {stats.output_path} (fingerprint={stats.fingerprint})"
    )


if __name__ == "__main__":
    main()
