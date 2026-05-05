from typing import Protocol
from unicodedata import normalize as unicode_normalize

from .relation_policy import get_relation_policy
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
    return " ".join(ascii_text.lower().replace("-", " ").split())


RAW_COMPLEMENTARY_TYPES = {
    "Cuba": {"Misturador", "Acessorio de Cozinha", "Lava-loucas"},
    "Misturador": {"Cuba", "Acessorio de Cozinha"},
    "Coifa": {"Cooktop", "Forno", "Domino", "Acessorio de Coifa", "Rangetop"},
    "Acessorio de Coifa": {"Coifa"},
    "Cooktop": {"Coifa", "Forno", "Domino"},
    "Domino": {"Coifa", "Cooktop", "Forno"},
    "Forno": {"Cooktop", "Coifa", "Micro-ondas", "Gaveta Aquecida"},
    "Micro-ondas": {"Forno", "Cooktop", "Gaveta Aquecida"},
    "Lava-loucas": {"Cuba", "Misturador", "Acessorio de Cozinha"},
    "Adega": {"Cervejeira", "Frigobar", "Churrasqueira", "Forno de Pizza"},
    "Cervejeira": {
        "Adega",
        "Frigobar",
        "Churrasqueira",
        "Forno de Pizza",
        "Maquina de Gelo",
    },
    "Frigobar": {"Adega", "Cervejeira", "Churrasqueira"},
    "Churrasqueira": {
        "Adega",
        "Cervejeira",
        "Coifa",
        "Cooktop",
        "Queimador",
        "Forno de Pizza",
    },
    "Forno de Pizza": {"Churrasqueira", "Cervejeira", "Adega"},
    "Refrigerador": {"Freezer", "Frigobar", "Cervejeira", "Maquina de Gelo"},
    "Freezer": {"Refrigerador"},
    "Gaveta Aquecida": {"Forno", "Cooktop"},
    "Cafeteira": {"Forno", "Micro-ondas", "Gaveta Aquecida"},
    "Queimador": {"Churrasqueira", "Cooktop", "Rangetop"},
    "Rangetop": {"Coifa", "Forno", "Queimador"},
    "Maquina de Gelo": {"Cervejeira", "Frigobar", "Adega", "Churrasqueira"},
    "Acessorio de Cozinha": {"Cuba", "Misturador", "Lava-loucas"},
}

COMPLEMENTARY_TYPES = {
    normalize_text(source): {normalize_text(target) for target in targets}
    for source, targets in RAW_COMPLEMENTARY_TYPES.items()
}


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
    def add_reason(reasons: list[str], message: str) -> None:
        if message and message not in reasons:
            reasons.append(message)

    if candidate.external_id == current_product.external_id:
        return -100.0, ["Mesmo produto do item visualizado."]

    policy = get_relation_policy(current_product.product_type, candidate.product_type)
    if policy.is_blocked:
        return -100.0, ["Relacao provisoriamente bloqueada pela politica editorial."]

    score = 0.0
    reasons: list[str] = []
    soft_signal_points = 0.0

    current_type = normalize_text(current_product.product_type)
    candidate_type = normalize_text(candidate.product_type)
    is_complementary = bool(
        candidate_type and candidate_type in COMPLEMENTARY_TYPES.get(current_type, set())
    )
    if is_complementary:
        score += 30
        add_reason(reasons, "Complementa funcionalmente o produto atual.")
    elif policy.reason_template:
        add_reason(reasons, policy.reason_template)

    is_sob_consulta = normalize_text(getattr(candidate, "availability_text", None)) == "sob consulta"
    if candidate.available:
        if is_sob_consulta:
            score += 8
            add_reason(
                reasons,
                "Produto sob consulta: recomendado apenas quando houver intencao consultiva.",
            )
        else:
            score += 20
            add_reason(reasons, "Produto disponivel no catalogo.")
    else:
        score -= 30
        add_reason(reasons, "Produto indisponivel no catalogo.")

    if values_match(current_product.voltage, candidate.voltage):
        score += 15
        add_reason(reasons, "Compatibilidade de voltagem com o produto atual.")

    if prices_are_close(current_product.price, candidate.price) and not is_sob_consulta:
        score += 12
        soft_signal_points += 12
        add_reason(reasons, "Faixa de preco semelhante ao produto atual.")

    if values_match(current_product.brand, candidate.brand):
        score += 5
        soft_signal_points += 5
        add_reason(reasons, "Mesma marca, como sinal auxiliar de suite.")

    if values_match(current_product.environment, candidate.environment):
        score += 5
        soft_signal_points += 5
        add_reason(reasons, "Mesmo ambiente de uso, como sinal auxiliar.")

    if values_match(current_product.premium_level, candidate.premium_level) and not is_sob_consulta:
        score += 3
        soft_signal_points += 3
        add_reason(reasons, "Faixa premium semelhante, como sinal auxiliar.")

    if policy.relation_class == "universal":
        score += 8
        add_reason(reasons, "Relacao comum em projetos de cozinha.")
    elif policy.relation_class == "contextual":
        add_reason(reasons, "Pode fazer sentido em projeto gourmet, mas depende do contexto.")
    elif policy.relation_class == "kouzina_specific":
        score -= 5
        add_reason(
            reasons,
            "Relacao editorial provisoria, pendente de validacao por comportamento real.",
        )
    elif policy.relation_class == "weak":
        score -= 20
        add_reason(reasons, "Relacao provisoria fraca; prioridade reduzida.")

    if policy.default_action == "boost":
        score += 4
    elif policy.default_action in {"demote", "review"}:
        score -= 8

    if not is_complementary and soft_signal_points >= 10:
        score -= 12
        add_reason(
            reasons,
            "Relacao fraca baseada apenas em sinais auxiliares; prioridade reduzida.",
        )

    if is_sob_consulta and not is_complementary and policy.relation_class not in {"universal", "contextual"}:
        score -= 10
        add_reason(
            reasons,
            "Produto sob consulta fora de relacao forte: usar com cautela.",
        )

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

    current_type = normalize_text(current_product.product_type)
    selected: list[tuple[ProductLike, float, str]] = []
    deferred: list[tuple[ProductLike, float, str]] = []
    weak_quote_count_top3 = 0

    for product, score, reason in ranked:
        if len(selected) >= limit:
            break

        policy = get_relation_policy(current_product.product_type, product.product_type)
        candidate_type = normalize_text(product.product_type)
        is_complementary = bool(
            candidate_type and candidate_type in COMPLEMENTARY_TYPES.get(current_type, set())
        )
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
