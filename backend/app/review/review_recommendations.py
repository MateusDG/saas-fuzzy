import argparse
import csv
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

from sqlalchemy.orm import Session

from ..core.database import SessionLocal, init_db
from ..db.models import Product, Store
from ..recommender import normalize_text, recommend_from_catalog
from ..recommender.relation_policy import get_relation_policy


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT = PROJECT_ROOT / "reports" / "recommendation_review.csv"
DEFAULT_STORE_SLUG = "kouzina"

REVIEW_COLUMNS = [
    "source_product_id",
    "source_name",
    "source_product_type",
    "source_category",
    "source_brand",
    "source_price",
    "source_availability_text",
    "recommended_product_id",
    "recommended_name",
    "recommended_product_type",
    "recommended_category",
    "recommended_brand",
    "recommended_price",
    "recommended_availability_text",
    "score",
    "reason",
    "source_url",
    "recommended_url",
    "recommended_image_url",
    "relation_class",
    "relation_type",
    "relation_policy_action",
    "validation_status",
    "requires_project_context",
    "requires_installation_check",
    "quote_policy",
    "quote_reason",
    "is_quote_only",
    "is_policy_demoted",
    "is_policy_blocked",
    "policy_notes",
    "reason_quality",
    "labels",
    "reviewer_rating",
    "reviewer_comment",
]


def resolve_output_path(output: Path) -> Path:
    if output.is_absolute():
        return output
    return PROJECT_ROOT / output


def format_optional(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, Decimal):
        return f"{value:.2f}"
    return str(value)


def bool_to_text(value: bool) -> str:
    return "true" if value else "false"


def classify_reason_quality(reason: str) -> str:
    normalized = normalize_text(reason)
    strong_markers = {
        "complementa funcionalmente",
        "relacao comum em projetos de cozinha",
    }
    medium_markers = {
        "depende do contexto",
        "sinal auxiliar",
        "editorial provisoria",
        "sob consulta",
    }

    if any(marker in normalized for marker in strong_markers):
        return "strong"
    if any(marker in normalized for marker in medium_markers):
        return "medium"
    return "generic"


def quote_reason_from_policy(quote_policy: str, is_quote_only: bool) -> str:
    if not is_quote_only:
        return ""

    mapping = {
        "allow_if_strong": "Produto sob consulta permitido quando a relacao for forte.",
        "allow_top3_with_context": "Produto sob consulta permitido no top-3 quando houver contexto.",
        "demote_if_top1": "Produto sob consulta deve ser rebaixado quando disputar top-1.",
        "block_if_weak": "Produto sob consulta deve ser bloqueado em relacoes fracas.",
        "review_only": "Produto sob consulta requer revisao manual nesta fase.",
    }
    return mapping.get(quote_policy, "Produto sob consulta requer revisao manual nesta fase.")


def build_labels(
    relation_class: str,
    relation_type: str,
    is_quote_only: bool,
    is_policy_demoted: bool,
    is_policy_blocked: bool,
    requires_project_context: bool,
    requires_installation_check: bool,
) -> str:
    labels = [relation_class, relation_type]
    if is_quote_only:
        labels.append("quote_only")
    if is_policy_demoted:
        labels.append("policy_demoted")
    if is_policy_blocked:
        labels.append("policy_blocked")
    if requires_project_context:
        labels.append("requires_project_context")
    if requires_installation_check:
        labels.append("requires_installation_check")
    return ",".join(label for label in labels if label)


def get_active_store_products(db: Session, store_slug: str = DEFAULT_STORE_SLUG) -> list[Product]:
    store = db.query(Store).filter(Store.slug == store_slug).one_or_none()
    if store is None:
        return []

    return (
        db.query(Product)
        .filter(Product.store_id == store.id, Product.active.is_(True))
        .order_by(Product.product_type, Product.external_id)
        .all()
    )


def filter_products_by_type(products: list[Product], product_type: str | None) -> list[Product]:
    if not product_type:
        return products

    normalized_filter = normalize_text(product_type)
    return [
        product
        for product in products
        if normalize_text(product.product_type) == normalized_filter
    ]


def sample_products_by_type(products: list[Product], limit: int) -> list[Product]:
    if limit <= 0:
        return []

    grouped_products: dict[str, list[Product]] = defaultdict(list)
    for product in products:
        group_key = normalize_text(product.product_type) or "sem tipo"
        grouped_products[group_key].append(product)

    for group in grouped_products.values():
        group.sort(key=lambda product: product.external_id)

    selected: list[Product] = []
    group_keys = sorted(grouped_products)
    while len(selected) < limit:
        added_product = False
        for group_key in group_keys:
            group = grouped_products[group_key]
            if not group:
                continue

            selected.append(group.pop(0))
            added_product = True
            if len(selected) >= limit:
                break

        if not added_product:
            break

    return selected


def build_review_rows(
    source_products: list[Product],
    all_products: list[Product],
    top_k: int,
) -> list[dict[str, object]]:
    products_by_external_id = {
        product.external_id: product
        for product in all_products
    }
    rows: list[dict[str, object]] = []

    for source_product in source_products:
        recommendations = recommend_from_catalog(source_product, all_products, limit=top_k)
        for recommendation in recommendations:
            recommended_product = products_by_external_id.get(recommendation.product_id)
            if recommended_product is None:
                continue

            policy = get_relation_policy(
                source_product.product_type,
                recommended_product.product_type,
            )
            is_quote_only = normalize_text(recommended_product.availability_text) == "sob consulta"
            is_policy_blocked = policy.is_blocked
            is_policy_demoted = policy.is_demoted
            quote_reason = quote_reason_from_policy(policy.quote_policy, is_quote_only)
            reason_quality = classify_reason_quality(recommendation.reason)
            labels = build_labels(
                relation_class=policy.relation_class,
                relation_type=policy.relation_type,
                is_quote_only=is_quote_only,
                is_policy_demoted=is_policy_demoted,
                is_policy_blocked=is_policy_blocked,
                requires_project_context=policy.requires_project_context,
                requires_installation_check=policy.requires_installation_check,
            )

            rows.append(
                {
                    "source_product_id": source_product.external_id,
                    "source_name": source_product.name,
                    "source_product_type": format_optional(source_product.product_type),
                    "source_category": format_optional(source_product.category),
                    "source_brand": format_optional(source_product.brand),
                    "source_price": format_optional(source_product.price),
                    "source_availability_text": format_optional(source_product.availability_text),
                    "recommended_product_id": recommended_product.external_id,
                    "recommended_name": recommended_product.name,
                    "recommended_product_type": format_optional(recommended_product.product_type),
                    "recommended_category": format_optional(recommended_product.category),
                    "recommended_brand": format_optional(recommended_product.brand),
                    "recommended_price": format_optional(recommended_product.price),
                    "recommended_availability_text": format_optional(
                        recommended_product.availability_text,
                    ),
                    "score": recommendation.score,
                    "reason": recommendation.reason,
                    "source_url": source_product.url,
                    "recommended_url": str(recommendation.url),
                    "recommended_image_url": (
                        str(recommendation.image_url)
                        if recommendation.image_url is not None
                        else ""
                    ),
                    "relation_class": policy.relation_class,
                    "relation_type": policy.relation_type,
                    "relation_policy_action": policy.default_action,
                    "validation_status": policy.validation_status,
                    "requires_project_context": bool_to_text(policy.requires_project_context),
                    "requires_installation_check": bool_to_text(policy.requires_installation_check),
                    "quote_policy": policy.quote_policy,
                    "quote_reason": quote_reason,
                    "is_quote_only": bool_to_text(is_quote_only),
                    "is_policy_demoted": bool_to_text(is_policy_demoted),
                    "is_policy_blocked": bool_to_text(is_policy_blocked),
                    "policy_notes": policy.notes,
                    "reason_quality": reason_quality,
                    "labels": labels,
                    "reviewer_rating": "",
                    "reviewer_comment": "",
                }
            )

    return rows


def write_review_csv(output_path: Path, rows: list[dict[str, object]]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=REVIEW_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def generate_review_csv(
    db: Session,
    output_path: Path = DEFAULT_OUTPUT,
    limit_products: int = 30,
    top_k: int = 4,
    product_type: str | None = None,
) -> tuple[int, int]:
    all_products = get_active_store_products(db)
    filtered_products = filter_products_by_type(all_products, product_type)
    source_products = sample_products_by_type(filtered_products, limit_products)
    rows = build_review_rows(source_products, all_products, top_k)
    write_review_csv(output_path, rows)
    return len(source_products), len(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a qualitative recommendation review CSV.",
    )
    parser.add_argument(
        "--limit-products",
        type=int,
        default=30,
        help="Maximum number of source products to include. Defaults to 30.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=4,
        help="Recommendations per source product. Defaults to 4.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output CSV path. Defaults to reports/recommendation_review.csv.",
    )
    parser.add_argument(
        "--product-type",
        type=str,
        default=None,
        help="Optional product_type filter, for example Churrasqueira.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_path = resolve_output_path(args.output)

    init_db()
    db = SessionLocal()
    try:
        source_count, row_count = generate_review_csv(
            db,
            output_path=output_path,
            limit_products=args.limit_products,
            top_k=args.top_k,
            product_type=args.product_type,
        )
    finally:
        db.close()

    print(
        "Generated "
        f"{row_count} recommendation review rows for {source_count} source products "
        f"at {output_path}"
    )


if __name__ == "__main__":
    main()
