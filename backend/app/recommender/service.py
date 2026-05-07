from ..schemas import RecommendationItem
from .relation_policy import get_relation_policy
from .rules import is_complementary_type
from .scoring import score_candidate
from .types import ProductLike
from .utils import normalize_text


MOCK_RECOMMENDATIONS = [
    RecommendationItem(
        product_id="mock-001",
        name="Cooktop premium compativel",
        url="https://www.kouzinaclub.com.br/",
        image_url=None,
        price=9990.0,
        reason="Produto complementar para composicao de cozinha gourmet.",
        score=0.92,
    ),
    RecommendationItem(
        product_id="mock-002",
        name="Forno de embutir recomendado",
        url="https://www.kouzinaclub.com.br/",
        image_url=None,
        price=8490.0,
        reason="Combina com projetos de cozinha planejada.",
        score=0.85,
    ),
    RecommendationItem(
        product_id="mock-003",
        name="Adega climatizada compacta",
        url="https://www.kouzinaclub.com.br/",
        image_url=None,
        price=6990.0,
        reason="Opcao complementar para espaco gourmet premium.",
        score=0.78,
    ),
]


def get_mock_recommendations() -> list[RecommendationItem]:
    return MOCK_RECOMMENDATIONS


def product_to_recommendation_item(
    product: ProductLike,
    reason: str,
    score: float,
) -> RecommendationItem:
    return RecommendationItem(
        product_id=product.external_id,
        name=product.name,
        url=product.url,
        image_url=product.image_url,
        price=float(product.price) if product.price is not None else None,
        reason=reason,
        score=score,
    )


def recommend_from_catalog(
    current_product: ProductLike | None,
    candidates: list[ProductLike],
    limit: int = 4,
) -> list[RecommendationItem]:
    if current_product is None:
        return []

    ranked: list[tuple[ProductLike, float, str]] = []

    for candidate in candidates:
        score, reasons = score_candidate(current_product, candidate)
        if score <= -100:
            continue

        ranked.append((candidate, score, " ".join(reasons)))

    ranked.sort(key=lambda item: (-item[1], item[0].external_id))

    selected: list[tuple[ProductLike, float, str]] = []
    deferred: list[tuple[ProductLike, float, str]] = []
    weak_quote_count_top3 = 0

    for product, score, reason in ranked:
        if len(selected) >= limit:
            break

        policy = get_relation_policy(current_product.product_type, product.product_type)
        is_complementary = is_complementary_type(current_product.product_type, product.product_type)
        is_strong_relation = policy.relation_class in {"universal", "contextual"} or is_complementary
        is_quote_only = normalize_text(getattr(product, "availability_text", None)) == "sob consulta"

        if (
            len(selected) < 3
            and is_quote_only
            and not is_strong_relation
        ):
            if weak_quote_count_top3 >= 1:
                deferred.append((product, score, reason))
                continue
            weak_quote_count_top3 += 1

        selected.append((product, score, reason))

    if len(selected) < limit:
        for item in deferred:
            if len(selected) >= limit:
                break
            if len(selected) < 3:
                continue
            selected.append(item)

    return [
        product_to_recommendation_item(product, reason, score)
        for product, score, reason in selected[:limit]
    ]
