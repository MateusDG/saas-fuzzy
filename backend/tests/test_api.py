from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models import Product, RecommendationEvent, Store
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
