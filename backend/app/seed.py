import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path

from sqlalchemy.orm import Session

from .database import SessionLocal, init_db
from .models import Product, Store
from .settings import get_settings


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PRODUCTS_CSV = PROJECT_ROOT / "data" / "products_seed.csv"
DEFAULT_STORE_SLUG = "kouzina"
DEFAULT_STORE_NAME = "Kouzina Club"
DEFAULT_STORE_DOMAIN = "https://www.kouzinaclub.com.br"


def parse_optional_text(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


def parse_bool(value: str | None) -> bool:
    if value is None:
        return True
    return value.strip().lower() in {"1", "true", "yes", "sim", "y"}


def parse_decimal(value: str | None) -> Decimal | None:
    value = parse_optional_text(value)
    if value is None:
        return None
    try:
        return Decimal(value.replace(",", "."))
    except InvalidOperation:
        return None


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


def product_values_from_row(row: dict[str, str]) -> dict[str, object]:
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


def import_products_from_csv(db: Session, csv_path: Path = DEFAULT_PRODUCTS_CSV) -> int:
    store = get_or_create_default_store(db)
    imported_count = 0

    with csv_path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            values = product_values_from_row(row)
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


def main() -> None:
    init_db()
    db = SessionLocal()
    try:
        imported_count = import_products_from_csv(db)
        print(f"Imported or updated {imported_count} products from {DEFAULT_PRODUCTS_CSV}")
    finally:
        db.close()


if __name__ == "__main__":
    main()

