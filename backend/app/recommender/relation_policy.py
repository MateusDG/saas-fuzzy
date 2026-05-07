import csv
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from unicodedata import normalize as unicode_normalize


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_POLICY_PATH = PROJECT_ROOT / "data" / "relation_policy_seed.csv"


@dataclass(frozen=True)
class RelationPolicyEntry:
    source_type: str
    recommended_type: str
    relation_class: str
    relation_type: str
    default_action: str
    strength: str
    requires_project_context: bool
    requires_installation_check: bool
    quote_policy: str
    reason_template: str
    source: str
    validation_status: str
    notes: str

    @property
    def is_blocked(self) -> bool:
        return self.default_action == "block" or self.relation_class == "forbidden"

    @property
    def is_demoted(self) -> bool:
        return self.default_action in {"demote", "review"} or self.relation_class == "weak"


def normalize_text(value: str | None) -> str:
    if not value:
        return ""

    normalized = unicode_normalize("NFKD", value)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    return " ".join(ascii_text.lower().replace("-", " ").split())


def parse_bool(value: str | None) -> bool:
    normalized = normalize_text(value)
    return normalized in {"1", "true", "yes", "sim"}


def resolve_policy_path(path: Path | None = None) -> Path:
    if path is None:
        return DEFAULT_POLICY_PATH
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


def fallback_policy(source_type: str | None, recommended_type: str | None) -> RelationPolicyEntry:
    return RelationPolicyEntry(
        source_type=source_type or "",
        recommended_type=recommended_type or "",
        relation_class="weak",
        relation_type="unknown",
        default_action="review",
        strength="low",
        requires_project_context=False,
        requires_installation_check=False,
        quote_policy="review_only",
        reason_template="Relacao provisoria sem politica explicita; revisar na curadoria.",
        source="fallback",
        validation_status="pending_client_data",
        notes="Tipo sem politica registrada. Nao validado por cliente ainda.",
    )


def _row_to_policy_entry(row: dict[str, str]) -> RelationPolicyEntry:
    return RelationPolicyEntry(
        source_type=row.get("source_type", "").strip(),
        recommended_type=row.get("recommended_type", "").strip(),
        relation_class=row.get("relation_class", "").strip() or "weak",
        relation_type=row.get("relation_type", "").strip() or "unknown",
        default_action=row.get("default_action", "").strip() or "review",
        strength=row.get("strength", "").strip() or "low",
        requires_project_context=parse_bool(row.get("requires_project_context", "")),
        requires_installation_check=parse_bool(row.get("requires_installation_check", "")),
        quote_policy=row.get("quote_policy", "").strip() or "review_only",
        reason_template=row.get("reason_template", "").strip(),
        source=row.get("source", "").strip() or "phase_4_8_agent_meeting",
        validation_status=row.get("validation_status", "").strip() or "agent_hypothesis",
        notes=row.get("notes", "").strip(),
    )


@lru_cache(maxsize=8)
def _load_relation_policy_cached(policy_path: str) -> dict[tuple[str, str], RelationPolicyEntry]:
    path = Path(policy_path)
    if not path.exists():
        return {}

    with path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        policies: dict[tuple[str, str], RelationPolicyEntry] = {}
        for row in reader:
            entry = _row_to_policy_entry(row)
            key = (
                normalize_text(entry.source_type),
                normalize_text(entry.recommended_type),
            )
            if not key[0] or not key[1]:
                continue
            policies[key] = entry
        return policies


def load_relation_policy(path: Path | None = None) -> dict[tuple[str, str], RelationPolicyEntry]:
    resolved = resolve_policy_path(path)
    return _load_relation_policy_cached(str(resolved))


def get_relation_policy(
    source_type: str | None,
    recommended_type: str | None,
    policies: dict[tuple[str, str], RelationPolicyEntry] | None = None,
) -> RelationPolicyEntry:
    key = (normalize_text(source_type), normalize_text(recommended_type))

    if policies is None:
        policies = load_relation_policy()

    if not key[0] or not key[1]:
        return fallback_policy(source_type, recommended_type)

    return policies.get(key, fallback_policy(source_type, recommended_type))
