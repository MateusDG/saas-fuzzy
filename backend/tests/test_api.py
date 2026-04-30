from collections.abc import Generator
from decimal import Decimal
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models import Product, RecommendationEvent, Store
from app.recommender import recommend_from_catalog, score_candidate
from app.seed import import_products_from_csv


@pytest.fixture()
def db_session(tmp_path) -> Generator[Session, None, None]:
    engine = create_engine(
        f"sqlite:///{tmp_path / 'test.db'}",
        connect_args={"check_same_thread": False},
    )
    TestingSessionLocal = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def make_product(external_id: str, **overrides):
    defaults = {
        "external_id": external_id,
        "name": f"Product {external_id}",
        "url": "https://www.kouzinaclub.com.br/",
        "image_url": None,
        "price": Decimal("1000.00"),
        "available": True,
        "category": "Cozinha",
        "brand": "Elettromec",
        "voltage": "220V",
        "environment": "Cozinha Gourmet",
        "product_type": "Coifa",
        "premium_level": "Premium",
    }
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


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
        "product_type": "Coifa",
        "environment": "Cozinha Gourmet",
        "premium_level": "Premium",
        "active": True,
    }
    defaults.update(overrides)
    product = Product(**defaults)
    db_session.add(product)
    return product


def test_health(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "kouzina-reco-api",
        "version": "0.1.0",
    }


def test_events_saves_recommendation_event(client: TestClient, db_session: Session) -> None:
    response = client.post(
        "/events",
        json={
            "event_type": "recommendation_click",
            "anonymous_id": "anon_123",
            "session_id": "sess_456",
            "page_url": "http://localhost:5500/demo.html",
            "product_id": "12345",
            "widget_id": "product-page",
            "recommended_product_id": "mock-001",
            "metadata": {"score": 0.91, "email": "cliente@example.com"},
        },
    )

    assert response.status_code == 200
    assert response.json()["received"] is True

    saved_event = db_session.query(RecommendationEvent).one()
    assert saved_event.event_type == "recommendation_click"
    assert saved_event.anonymous_id == "anon_123"
    assert saved_event.product_external_id == "12345"
    assert saved_event.recommended_product_external_id == "mock-001"
    assert saved_event.event_metadata == {"score": 0.91}


def test_recommendations_fallback_when_catalog_is_empty(client: TestClient) -> None:
    response = client.get("/recommendations", params={"product_id": "12345"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["widget_title"] == "Complete seu projeto"
    assert payload["recommendations"][0]["product_id"] == "mock-001"


def test_recommender_does_not_return_current_product() -> None:
    current = make_product("current", product_type="Coifa")
    same_product = make_product("current", product_type="Coifa")
    candidate = make_product("candidate", product_type="Cooktop")

    recommendations = recommend_from_catalog(current, [current, same_product, candidate])

    recommendation_ids = [item.product_id for item in recommendations]
    assert recommendation_ids == ["candidate"]


def test_complementary_candidate_scores_higher() -> None:
    current = make_product("current", product_type="Coifa")
    complementary = make_product("cooktop", product_type="Cooktop")
    unrelated = make_product("adega", product_type="Adega")

    complementary_score, _ = score_candidate(current, complementary)
    unrelated_score, _ = score_candidate(current, unrelated)

    assert complementary_score > unrelated_score


def test_unavailable_candidate_is_penalized() -> None:
    current = make_product("current", product_type="Coifa")
    available = make_product("available", product_type="Cooktop", available=True)
    unavailable = make_product("unavailable", product_type="Cooktop", available=False)

    available_score, _ = score_candidate(current, available)
    unavailable_score, _ = score_candidate(current, unavailable)

    assert unavailable_score < available_score


def test_same_voltage_increases_score() -> None:
    current = make_product("current", voltage="220V")
    same_voltage = make_product("same-voltage", voltage="220V")
    different_voltage = make_product("different-voltage", voltage="110V")

    same_voltage_score, _ = score_candidate(current, same_voltage)
    different_voltage_score, _ = score_candidate(current, different_voltage)

    assert same_voltage_score > different_voltage_score


def test_close_price_increases_score() -> None:
    current = make_product("current", price=Decimal("1000.00"))
    close_price = make_product("close-price", price=Decimal("1200.00"))
    far_price = make_product("far-price", price=Decimal("2000.00"))

    close_price_score, _ = score_candidate(current, close_price)
    far_price_score, _ = score_candidate(current, far_price)

    assert close_price_score > far_price_score


def test_recommendations_are_sorted_by_score(
    client: TestClient,
    db_session: Session,
) -> None:
    store = create_store(db_session)
    create_db_product(
        db_session,
        store,
        "current-coifa",
        product_type="Coifa",
        price=Decimal("10000.00"),
    )
    create_db_product(
        db_session,
        store,
        "candidate-cooktop",
        product_type="Cooktop",
        price=Decimal("9000.00"),
    )
    create_db_product(
        db_session,
        store,
        "candidate-adega",
        brand="Crissair",
        voltage="110V",
        product_type="Adega",
        environment="Espaco Gourmet",
        premium_level="Intermediario",
        price=Decimal("30000.00"),
    )
    db_session.commit()

    response = client.get("/recommendations", params={"product_id": "current-coifa"})

    assert response.status_code == 200
    payload = response.json()
    scores = [item["score"] for item in payload["recommendations"]]
    recommendation_ids = [item["product_id"] for item in payload["recommendations"]]
    assert recommendation_ids[0] == "candidate-cooktop"
    assert scores == sorted(scores, reverse=True)


def test_recommendations_fallback_when_current_product_is_missing(
    client: TestClient,
    db_session: Session,
) -> None:
    store = create_store(db_session)
    create_db_product(db_session, store, "catalog-product")
    db_session.commit()

    response = client.get("/recommendations", params={"product_id": "missing-product"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["recommendations"][0]["product_id"] == "mock-001"


def test_seed_imports_csv_and_recommendations_use_catalog(
    client: TestClient,
    db_session: Session,
) -> None:
    imported_count = import_products_from_csv(db_session)

    assert imported_count == 3
    assert db_session.query(Store).count() == 1
    assert db_session.query(Product).count() == 3

    response = client.get("/recommendations", params={"product_id": "mock-001"})

    assert response.status_code == 200
    payload = response.json()
    recommendation_ids = [item["product_id"] for item in payload["recommendations"]]
    assert "mock-001" not in recommendation_ids
    assert recommendation_ids
