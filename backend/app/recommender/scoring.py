from .explanations import add_reason
from .relation_policy import get_relation_policy
from .rules import is_complementary_type
from .types import ProductLike
from .utils import normalize_text, prices_are_close, values_match


def score_candidate(
    current_product: ProductLike,
    candidate: ProductLike,
) -> tuple[float, list[str]]:
    if candidate.external_id == current_product.external_id:
        return -100.0, ["Mesmo produto do item visualizado."]

    policy = get_relation_policy(current_product.product_type, candidate.product_type)
    if policy.is_blocked:
        return -100.0, ["Relacao provisoriamente bloqueada pela politica editorial."]

    score = 0.0
    reasons: list[str] = []
    soft_signal_points = 0.0

    is_complementary = is_complementary_type(current_product.product_type, candidate.product_type)
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
