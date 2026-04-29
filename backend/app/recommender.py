from typing import Protocol

from .schemas import RecommendationItem


class ProductLike(Protocol):
    external_id: str
    name: str
    url: str
    image_url: str | None
    price: object
    available: bool
    category: str | None
    environment: str | None
    product_type: str | None


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
    limit: int = 3,
) -> list[RecommendationItem]:
    ranked: list[tuple[ProductLike, float, str]] = []

    for candidate in candidates:
        if current_product and candidate.external_id == current_product.external_id:
            continue

        score = 0.5
        reasons: list[str] = []

        if candidate.available:
            score += 0.2
            reasons.append("Produto disponivel no catalogo inicial.")

        if current_product and current_product.environment and candidate.environment == current_product.environment:
            score += 0.15
            reasons.append("Indicado para o mesmo ambiente do produto visualizado.")

        if current_product and current_product.category and candidate.category == current_product.category:
            score += 0.1
            reasons.append("Produto da mesma categoria principal.")

        if not reasons:
            reasons.append("Produto selecionado do catalogo inicial da Kouzina.")

        ranked.append((candidate, min(score, 0.99), " ".join(reasons)))

    ranked.sort(key=lambda item: item[1], reverse=True)
    return [
        product_to_recommendation_item(product, reason, score)
        for product, score, reason in ranked[:limit]
    ]
