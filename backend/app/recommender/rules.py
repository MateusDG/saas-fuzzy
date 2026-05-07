from .utils import normalize_text


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


def is_complementary_type(source_type: str | None, candidate_type: str | None) -> bool:
    normalized_source = normalize_text(source_type)
    normalized_candidate = normalize_text(candidate_type)
    return bool(
        normalized_candidate
        and normalized_candidate in COMPLEMENTARY_TYPES.get(normalized_source, set())
    )
