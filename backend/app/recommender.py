from typing import Protocol
from unicodedata import normalize as unicode_normalize

from .schemas import RecommendationItem


class ProductLike(Protocol):
    external_id: str
    name: str
    url: str
    image_url: str | None
    price: object
    available: bool
    category: str | None
    brand: str | None
    voltage: str | None
    environment: str | None
    product_type: str | None
    premium_level: str | None
    availability_text: str | None


COMPLEMENTARY_TYPES = {
    "coifa": {"cooktop", "forno", "domino"},
    "cooktop": {"coifa", "forno", "domino"},
    "adega": {"cervejeira", "frigobar", "churrasqueira"},
    "churrasqueira": {"adega", "cervejeira", "coifa", "cooktop"},
    "forno": {"cooktop", "coifa"},
}


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


def normalize_text(value: str | None) -> str:
    if not value:
        return ""

    normalized = unicode_normalize("NFKD", value)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    return " ".join(ascii_text.lower().split())


def values_match(left: str | None, right: str | None) -> bool:
    normalized_left = normalize_text(left)
    normalized_right = normalize_text(right)
    return bool(normalized_left and normalized_left == normalized_right)


def price_as_float(value: object) -> float | None:
    if value is None:
        return None

    try:
        price = float(value)
    except (TypeError, ValueError):
        return None

    if price <= 0:
        return None

    return price


def prices_are_close(current_price: object, candidate_price: object) -> bool:
    current = price_as_float(current_price)
    candidate = price_as_float(candidate_price)

    if current is None or candidate is None:
        return False

    relative_difference = abs(current - candidate) / current
    return relative_difference <= 0.30


def score_candidate(
    current_product: ProductLike,
    candidate: ProductLike,
) -> tuple[float, list[str]]:
    if candidate.external_id == current_product.external_id:
        return -100.0, ["Mesmo produto do item visualizado."]

    score = 0.0
    reasons: list[str] = []

    current_type = normalize_text(current_product.product_type)
    candidate_type = normalize_text(candidate.product_type)
    if candidate_type and candidate_type in COMPLEMENTARY_TYPES.get(current_type, set()):
        score += 30
        reasons.append("Produto complementar ao item visualizado.")

    is_sob_consulta = normalize_text(getattr(candidate, "availability_text", None)) == "sob consulta"
    if candidate.available:
        score += 20
        if is_sob_consulta:
            reasons.append("Produto sob consulta.")
        else:
            reasons.append("Produto disponivel.")
    else:
        score -= 30
        reasons.append("Produto indisponivel no catalogo.")

    if values_match(current_product.voltage, candidate.voltage):
        score += 15
        reasons.append("Mesma voltagem do produto atual.")

    if prices_are_close(current_product.price, candidate.price):
        score += 15
        reasons.append("Faixa de preco proxima.")

    if values_match(current_product.brand, candidate.brand):
        score += 10
        reasons.append("Mesma marca do produto atual.")

    if values_match(current_product.environment, candidate.environment):
        score += 10
        reasons.append("Indicado para o mesmo ambiente.")

    if values_match(current_product.premium_level, candidate.premium_level):
        score += 10
        reasons.append("Faixa premium semelhante.")

    if not reasons:
        reasons.append("Produto selecionado do catalogo da Kouzina.")

    return score, reasons


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
    return [
        product_to_recommendation_item(product, reason, score)
        for product, score, reason in ranked[:limit]
    ]
