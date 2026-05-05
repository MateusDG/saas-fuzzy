from pathlib import Path
from types import SimpleNamespace

from app.recommender import score_candidate
from app.relation_policy import get_relation_policy, load_relation_policy


def make_product(external_id: str, product_type: str, **overrides):
    defaults = {
        "external_id": external_id,
        "name": f"Product {external_id}",
        "url": "https://www.kouzinaclub.com.br/",
        "image_url": None,
        "price": 1000.0,
        "available": True,
        "category": "Cozinha",
        "brand": "Elettromec",
        "voltage": "220V",
        "environment": "Cozinha Gourmet",
        "product_type": product_type,
        "premium_level": "Premium",
        "availability_text": "Preco informado",
    }
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


def test_load_relation_policy_returns_entries() -> None:
    policies = load_relation_policy()

    assert policies
    entry = get_relation_policy("Cuba", "Misturador", policies=policies)
    assert entry.relation_class == "universal"
    assert entry.default_action == "boost"
    assert entry.validation_status == "agent_hypothesis"


def test_load_relation_policy_fallback_when_file_missing(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing_relation_policy.csv"
    policies = load_relation_policy(missing_path)

    assert policies == {}
    fallback = get_relation_policy("TipoX", "TipoY", policies=policies)
    assert fallback.relation_class == "weak"
    assert fallback.default_action == "review"
    assert fallback.validation_status == "pending_client_data"


def test_get_relation_policy_handles_unknown_type_pair() -> None:
    entry = get_relation_policy("Unknown Source", "Unknown Target")

    assert entry.relation_type == "unknown"
    assert entry.default_action == "review"
    assert entry.source == "fallback"


def test_forbidden_pair_is_blocked_by_policy_in_scoring() -> None:
    current = make_product("lavadora", "Lavadora")
    candidate = make_product("adega", "Adega")

    score, reasons = score_candidate(current, candidate)

    assert score <= -100
    assert "Relacao provisoriamente bloqueada pela politica editorial." in reasons
