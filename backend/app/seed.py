import argparse
import csv
import re
from decimal import Decimal, InvalidOperation
from pathlib import Path
from unicodedata import normalize as unicode_normalize

from sqlalchemy.orm import Session

from .database import SessionLocal, init_db
from .models import ManualProductRelation, Product, Store
from .settings import get_settings


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PRODUCTS_CSV = PROJECT_ROOT / "data" / "products_seed.csv"
DEFAULT_STORE_SLUG = "kouzina"
DEFAULT_STORE_NAME = "Kouzina Club"
DEFAULT_STORE_DOMAIN = "https://www.kouzinaclub.com.br"
PRICE_INFORMED = "Pre\u00e7o informado"
PRICE_NOT_INFORMED = "Pre\u00e7o n\u00e3o informado"
SOB_CONSULTA = "Sob consulta"

CATEGORY_ALIASES = {
    "adegas": "Adegas",
    "cervejeiras": "Cervejeiras",
    "churrasqueiras": "Churrasqueiras",
    "coifas": "Coifas",
    "cooktops": "Cooktops",
    "cozinha": "Cozinha",
    "espaco gourmet": "Espa\u00e7o Gourmet",
    "fornos": "Fornos",
    "frigobar": "Frigobar",
    "gavetas refrigeradoras": "Gavetas Refrigeradoras",
    "lava loucas": "Lava-lou\u00e7as",
    "lavadoras": "Lavadoras",
    "micro ondas": "Micro-Ondas",
    "refrigeracao": "Refrigera\u00e7\u00e3o",
    "secadoras": "Secadoras",
}

PRODUCT_TYPE_RULES = [
    ({"forno de pizza", "pizza"}, "Forno de Pizza"),
    ({"gaveta refrigerada", "gavetas refrigeradoras"}, "Gaveta Refrigerada"),
    ({"maquina de gelo"}, "M\u00e1quina de Gelo"),
    ({"gaveta aquecida"}, "Gaveta Aquecida"),
    ({"lava loucas", "lava louca"}, "Lava-lou\u00e7as"),
    ({"micro ondas", "microondas"}, "Micro-ondas"),
    ({"queimador lateral", "side burner", "power burner", "dual burner"}, "Queimador"),
    ({"dispenser de agua"}, "Dispenser de \u00c1gua"),
    ({"kit exaustor", "kit filtragem", "depurador", "extractor"}, "Acess\u00f3rio de Coifa"),
    ({"cafeteira"}, "Cafeteira"),
    ({"misturador"}, "Misturador"),
    ({"cuba"}, "Cuba"),
    ({"set azeite", "azeite", "vinagre"}, "Acess\u00f3rio de Cozinha"),
    ({"churrasqueiras", "churrasqueira"}, "Churrasqueira"),
    ({"cervejeiras", "cervejeira"}, "Cervejeira"),
    ({"frigobar", "frigobares"}, "Frigobar"),
    ({"adegas", "adega"}, "Adega"),
    ({"coifas", "coifa"}, "Coifa"),
    ({"cooktops", "cooktop"}, "Cooktop"),
    ({"fornos", "forno"}, "Forno"),
    ({"domino", "dominos"}, "Domino"),
    ({"refrigeradores", "refrigerador", "refrigeracao"}, "Refrigerador"),
    ({"fogoes", "fogao"}, "Fog\u00e3o"),
    ({"rangertop", "rangetop"}, "Rangetop"),
    ({"freezer"}, "Freezer"),
    ({"secadoras", "secadora"}, "Secadora"),
    ({"lavadoras", "lavadora"}, "Lavadora"),
    ({"conjugadas", "conjugada"}, "Conjugada"),
]

KITCHEN_TYPES = {
    "acessorio de coifa",
    "acessorio de cozinha",
    "cafeteira",
    "coifa",
    "cooktop",
    "cuba",
    "domino",
    "fogao",
    "forno",
    "gaveta aquecida",
    "lava loucas",
    "micro ondas",
    "misturador",
    "rangetop",
}
GOURMET_TYPES = {
    "adega",
    "cervejeira",
    "churrasqueira",
    "dispenser de agua",
    "forno de pizza",
    "frigobar",
    "maquina de gelo",
    "queimador",
}
REFRIGERATION_TYPES = {"freezer", "gaveta refrigerada", "refrigerador"}
LAUNDRY_TYPES = {"conjugada", "lavadora", "secadora"}


def parse_optional_text(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = " ".join(value.strip().split())
    return stripped or None


def parse_bool(value: str | None) -> bool:
    if value is None:
        return True
    return value.strip().lower() in {"1", "true", "yes", "sim", "y"}


def parse_decimal(value: str | None) -> Decimal | None:
    value = parse_optional_text(value)
    if value is None:
        return None
    normalized_value = value.replace("R$", "").strip()
    if "," in normalized_value and "." in normalized_value:
        if normalized_value.rfind(",") > normalized_value.rfind("."):
            normalized_value = normalized_value.replace(".", "").replace(",", ".")
    else:
        normalized_value = normalized_value.replace(",", ".")
    try:
        return Decimal(normalized_value)
    except InvalidOperation:
        return None


def normalize_key(value: str | None) -> str:
    if not value:
        return ""

    normalized = unicode_normalize("NFKD", value.replace("\ufeff", ""))
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    return " ".join(ascii_text.lower().replace("-", " ").split())


def get_row_value(row: dict[str, str], *keys: str) -> str | None:
    normalized_row = {
        normalize_key(key): value
        for key, value in row.items()
        if key is not None
    }
    for key in keys:
        value = normalized_row.get(normalize_key(key))
        if parse_optional_text(value) is not None:
            return value
    return None


def detect_csv_delimiter(sample: str) -> str:
    first_line = sample.splitlines()[0] if sample.splitlines() else ""
    if first_line.count(";") > first_line.count(","):
        return ";"
    return ","


def detect_catalog_format(fieldnames: list[str] | None) -> str:
    normalized_headers = {normalize_key(fieldname) for fieldname in fieldnames or []}
    if "external_id" in normalized_headers:
        return "internal"
    if "nome produto" in normalized_headers:
        return "kouzina_official"
    raise ValueError("Unsupported products CSV format")


def first_image_url(value: str | None) -> str | None:
    value = parse_optional_text(value)
    if value is None:
        return None

    match = re.search(r"https?://[^\s,;|]+", value)
    if match:
        return match.group(0)

    first_value = re.split(r"[,;|]", value, maxsplit=1)[0]
    return parse_optional_text(first_value)


def normalize_brand(value: str | None) -> str | None:
    brand = parse_optional_text(value)
    if brand is None:
        return None
    normalized = normalize_key(brand)
    if normalized in {"bert. ital", "bertazzoni italia"}:
        return "Bertazzoni It\u00e1lia"
    return brand


def normalize_category(value: str | None) -> str | None:
    category = parse_optional_text(value)
    if category is None:
        return None
    return CATEGORY_ALIASES.get(normalize_key(category), category)


def normalize_voltage(value: str | None) -> str | None:
    value = parse_optional_text(value)
    if value is None:
        return None

    normalized = normalize_key(value)
    if "bivolt" in normalized:
        return "bivolt"

    voltages = re.findall(r"(127|110|220)\s*v", normalized)
    unique_voltages = list(dict.fromkeys(f"{voltage}v" for voltage in voltages))
    if len(unique_voltages) == 1:
        return unique_voltages[0]
    if unique_voltages:
        if "220v" in unique_voltages and any(voltage in unique_voltages for voltage in {"110v", "127v"}):
            return "bivolt"
        return ", ".join(unique_voltages)

    return " ".join(value.lower().split())


def extract_width_cm(name: str | None) -> Decimal | None:
    value = parse_optional_text(name)
    if value is None:
        return None

    match = re.search(r"(\d+(?:[,.]\d+)?)\s*cm", value, flags=re.IGNORECASE)
    if not match:
        return None
    return parse_decimal(match.group(1))


def infer_installation_type(name: str | None) -> str | None:
    normalized = normalize_key(name)
    if "embutir" in normalized or "built in" in normalized:
        return "Embutir"
    if "ilha" in normalized:
        return "Ilha"
    if "parede" in normalized:
        return "Parede"
    if "domino" in normalized:
        return "Domin\u00f3"
    return None


def text_has_any(value: str, terms: set[str]) -> bool:
    return any(term in value for term in terms)


def infer_product_type(category: str | None, name: str | None) -> str | None:
    normalized = normalize_key(f"{category or ''} {name or ''}")

    for terms, product_type in PRODUCT_TYPE_RULES:
        if text_has_any(normalized, terms):
            return product_type
    return None


def infer_environment(product_type: str | None, category: str | None, name: str | None) -> str | None:
    normalized_type = normalize_key(product_type)
    if normalized_type in KITCHEN_TYPES:
        return "Cozinha Gourmet"
    if normalized_type in GOURMET_TYPES:
        return "Espa\u00e7o Gourmet"
    if normalized_type in REFRIGERATION_TYPES:
        return "Refrigera\u00e7\u00e3o"
    if normalized_type in LAUNDRY_TYPES:
        return "Lavanderia"

    normalized = normalize_key(f"{product_type or ''} {category or ''} {name or ''}")

    if text_has_any(normalized, {"lavanderia", "lavadora", "secadora", "conjugada"}):
        return "Lavanderia"
    if text_has_any(
        normalized,
        {"refrigeracao", "refrigerador", "freezer", "gaveta refrigerada"},
    ):
        return "Refrigera\u00e7\u00e3o"
    if text_has_any(
        normalized,
        {
            "espaco gourmet",
            "adega",
            "cervejeira",
            "churrasqueira",
            "frigobar",
            "maquina de gelo",
            "forno de pizza",
        },
    ):
        return "Espa\u00e7o Gourmet"
    if text_has_any(
        normalized,
        {
            "cozinha",
            "cooktop",
            "coifa",
            "forno",
            "micro ondas",
            "lava loucas",
            "fogao",
            "domino",
            "rangetop",
            "gaveta aquecida",
        },
    ):
        return "Cozinha Gourmet"
    return None


def infer_premium_level(price: Decimal | None, availability_text: str | None) -> str | None:
    if price is None:
        if availability_text == SOB_CONSULTA:
            return SOB_CONSULTA
        return None
    if price <= Decimal("5000"):
        return "Premium"
    if price <= Decimal("20000"):
        return "Alto padr\u00e3o"
    if price <= Decimal("60000"):
        return "Luxo"
    return "Ultra premium"


def get_or_create_default_store(db: Session) -> Store:
    settings = get_settings()
    store = db.query(Store).filter(Store.slug == DEFAULT_STORE_SLUG).one_or_none()
    if store:
        return store

    store = Store(
        slug=DEFAULT_STORE_SLUG,
        name=DEFAULT_STORE_NAME,
        domain=DEFAULT_STORE_DOMAIN,
        public_key=settings.public_widget_key,
    )
    db.add(store)
    db.commit()
    db.refresh(store)
    return store


def product_values_from_internal_row(row: dict[str, str]) -> dict[str, object]:
    return {
        "external_id": parse_optional_text(row.get("external_id")) or "",
        "name": parse_optional_text(row.get("name")) or "Produto sem nome",
        "url": parse_optional_text(row.get("url")) or "https://www.kouzinaclub.com.br/",
        "image_url": parse_optional_text(row.get("image_url")),
        "category": parse_optional_text(row.get("category")),
        "subcategory": parse_optional_text(row.get("subcategory")),
        "brand": parse_optional_text(row.get("brand")),
        "price": parse_decimal(row.get("price")),
        "available": parse_bool(row.get("available")),
        "availability_text": parse_optional_text(row.get("availability_text")),
        "voltage": parse_optional_text(row.get("voltage")),
        "width_cm": parse_decimal(row.get("width_cm")),
        "installation_type": parse_optional_text(row.get("installation_type")),
        "product_type": parse_optional_text(row.get("product_type")),
        "environment": parse_optional_text(row.get("environment")),
        "premium_level": parse_optional_text(row.get("premium_level")),
        "active": True,
    }


def product_values_from_official_row(row: dict[str, str], row_number: int) -> dict[str, object]:
    name = parse_optional_text(get_row_value(row, "nome produto")) or "Produto sem nome"
    category = normalize_category(get_row_value(row, "nome categoria"))
    price = parse_decimal(get_row_value(row, "preco venda"))
    raw_price = parse_optional_text(get_row_value(row, "preco venda"))

    if raw_price is None:
        availability_text = PRICE_NOT_INFORMED
        price = None
    elif price is None:
        availability_text = PRICE_NOT_INFORMED
    elif price == Decimal("0"):
        availability_text = SOB_CONSULTA
        price = None
    else:
        availability_text = PRICE_INFORMED

    product_type = infer_product_type(category, name)
    environment = infer_environment(product_type, category, name)

    return {
        "external_id": (
            parse_optional_text(get_row_value(row, "referencia"))
            or f"kouzina-auto-{row_number}"
        ),
        "name": name,
        "url": (
            parse_optional_text(
                get_row_value(
                    row,
                    "endereco do produto (url tray)",
                    "endereco do produto url tray",
                    "url tray",
                    "url",
                )
            )
            or DEFAULT_STORE_DOMAIN
        ),
        "image_url": first_image_url(get_row_value(row, "imagens adicionais", "image_url")),
        "category": category,
        "subcategory": category,
        "brand": normalize_brand(get_row_value(row, "marca")),
        "price": price,
        "available": True,
        "availability_text": availability_text,
        "voltage": normalize_voltage(get_row_value(row, "caracteristica: voltagem", "voltagem")),
        "width_cm": extract_width_cm(name),
        "installation_type": infer_installation_type(name),
        "product_type": product_type,
        "environment": environment,
        "premium_level": infer_premium_level(price, availability_text),
        "active": True,
    }


def product_values_from_row(
    row: dict[str, str],
    catalog_format: str = "internal",
    row_number: int = 1,
) -> dict[str, object]:
    if catalog_format == "kouzina_official":
        return product_values_from_official_row(row, row_number)
    return product_values_from_internal_row(row)


def replace_store_products(db: Session, store: Store) -> None:
    db.query(ManualProductRelation).filter(ManualProductRelation.store_id == store.id).delete(
        synchronize_session=False,
    )
    db.query(Product).filter(Product.store_id == store.id).delete(synchronize_session=False)
    db.commit()


def import_products_from_csv(
    db: Session,
    csv_path: Path = DEFAULT_PRODUCTS_CSV,
    replace_products: bool = False,
) -> int:
    store = get_or_create_default_store(db)
    imported_count = 0
    csv_path = Path(csv_path)

    with csv_path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        sample = csv_file.read(4096)
        csv_file.seek(0)
        reader = csv.DictReader(csv_file, delimiter=detect_csv_delimiter(sample))
        catalog_format = detect_catalog_format(reader.fieldnames)

        if replace_products:
            replace_store_products(db, store)

        for row_number, row in enumerate(reader, start=1):
            values = product_values_from_row(row, catalog_format, row_number)
            external_id = values["external_id"]
            if not external_id:
                continue

            product = (
                db.query(Product)
                .filter(Product.store_id == store.id, Product.external_id == external_id)
                .one_or_none()
            )

            if product is None:
                product = Product(store_id=store.id, **values)
                db.add(product)
            else:
                for field, value in values.items():
                    setattr(product, field, value)

            imported_count += 1

    db.commit()
    return imported_count


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import Kouzina products into PostgreSQL.")
    parser.add_argument(
        "--file",
        type=Path,
        default=DEFAULT_PRODUCTS_CSV,
        help="CSV path. Defaults to data/products_seed.csv.",
    )
    parser.add_argument(
        "--replace-products",
        action="store_true",
        help="Remove products from the default store before importing. Events are preserved.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    init_db()
    db = SessionLocal()
    try:
        imported_count = import_products_from_csv(
            db,
            csv_path=args.file,
            replace_products=args.replace_products,
        )
        print(f"Imported or updated {imported_count} products from {args.file}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
