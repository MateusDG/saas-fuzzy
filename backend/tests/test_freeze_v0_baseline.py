from collections.abc import Generator
from decimal import Decimal
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base
from app.freeze_v0_baseline import freeze_v0_baseline
from app.models import Product, Store


def create_store(db_session: Session) -> Store:
    store = Store(
        slug="kouzina",
        name="Kouzina Club",
        domain="https://www.kouzinaclub.com.br",
        public_key="kouzina_public_dev_key",
    )
    db_session.add(store)
    db_session.flush()
    return store


def create_db_product(
    db_session: Session,
    store: Store,
    external_id: str,
    product_type: str,
    **overrides,
) -> Product:
    defaults = {
        "store_id": store.id,
        "external_id": external_id,
        "name": f"Product {external_id}",
        "url": "https://www.kouzinaclub.com.br/",
        "image_url": None,
        "category": "Cozinha",
        "subcategory": "Teste",
        "brand": "Elettromec",
        "price": Decimal("1000.00"),
        "available": True,
        "availability_text": "Disponivel",
        "voltage": "220V",
        "width_cm": Decimal("60.00"),
        "installation_type": "Embutir",
        "product_type": product_type,
        "environment": "Cozinha Gourmet",
        "premium_level": "Premium",
        "active": True,
    }
    defaults.update(overrides)
    product = Product(**defaults)
    db_session.add(product)
    return product


@pytest.fixture()
def db_session(tmp_path: Path) -> Generator[Session, None, None]:
    engine = create_engine(
        f"sqlite:///{tmp_path / 'freeze_test.db'}",
        connect_args={"check_same_thread": False},
    )
    testing_session_local = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )
    Base.metadata.create_all(bind=engine)
    db = testing_session_local()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


def test_freeze_v0_baseline_generates_snapshot(db_session: Session, tmp_path: Path) -> None:
    store = create_store(db_session)
    create_db_product(db_session, store, "source-coifa", "Coifa", price=Decimal("10000.00"))
    create_db_product(db_session, store, "candidate-cooktop", "Cooktop", price=Decimal("9500.00"))
    create_db_product(db_session, store, "candidate-forno", "Forno", price=Decimal("9000.00"))
    db_session.commit()

    output_path = tmp_path / "v0_snapshot.json"
    stats = freeze_v0_baseline(
        db_session,
        output_path=output_path,
        limit_products=1,
        top_k=2,
    )

    assert stats.source_products == 1
    assert stats.recommendation_rows == 2
    assert len(stats.fingerprint) == 64
    assert output_path.exists()
