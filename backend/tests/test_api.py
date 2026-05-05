from collections.abc import Generator
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models import Product, RecommendationEvent, Store
from app.recommender import recommend_from_catalog, score_candidate
from app.review_recommendations import REVIEW_COLUMNS, generate_review_csv
from app.seed import (
    infer_environment,
    infer_product_type,
    import_products_from_csv,
    normalize_brand,
    normalize_category,
    normalize_voltage,
)


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
        "availability_text": "Disponivel",
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
    assert saved_event.event_metadata["event_name"] == "recommendation_click"
    assert saved_event.event_metadata["source_product_id"] == "12345"
    assert saved_event.event_metadata["recommended_product_id"] == "mock-001"
    assert saved_event.event_metadata["score"] == 0.91
    assert "email" not in saved_event.event_metadata


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


def test_catalog_commercial_relationships_score_as_complementary() -> None:
    relationship_cases = [
        ("Cuba", "Misturador"),
        ("Misturador", "Cuba"),
        ("Acess\u00f3rio de Coifa", "Coifa"),
        ("Churrasqueira", "Cervejeira"),
        ("Churrasqueira", "Adega"),
        ("Churrasqueira", "Forno de Pizza"),
        ("Churrasqueira", "Queimador"),
        ("Coifa", "Acess\u00f3rio de Coifa"),
        ("Forno", "Gaveta Aquecida"),
        ("Refrigerador", "Freezer"),
        ("Rangetop", "Queimador"),
    ]

    for current_type, candidate_type in relationship_cases:
        current = make_product("current", product_type=current_type)
        complementary = make_product("complementary", product_type=candidate_type)
        unrelated = make_product("unrelated", product_type="Secadora")

        complementary_score, complementary_reasons = score_candidate(current, complementary)
        unrelated_score, _ = score_candidate(current, unrelated)

        assert complementary_score > unrelated_score
        assert "Complementa funcionalmente o produto atual." in complementary_reasons


def test_environment_is_not_treated_as_product_type_relationship() -> None:
    current = make_product("current", product_type="Micro-ondas")
    environment_as_type = make_product("environment", product_type="Cozinha Gourmet")

    _, reasons = score_candidate(current, environment_as_type)

    assert "Complementa funcionalmente o produto atual." not in reasons


def test_cuba_recommends_misturador_without_returning_current_product() -> None:
    current = make_product("cuba", product_type="Cuba")
    same_product = make_product("cuba", product_type="Cuba")
    misturador = make_product("misturador", product_type="Misturador")
    coifa = make_product("coifa", product_type="Coifa")

    recommendations = recommend_from_catalog(
        current,
        [same_product, coifa, misturador],
    )

    recommendation_ids = [item.product_id for item in recommendations]
    assert recommendation_ids[0] == "misturador"
    assert "cuba" not in recommendation_ids
    assert "Complementa funcionalmente o produto atual." in recommendations[0].reason


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


def test_forbidden_relation_is_blocked_by_policy() -> None:
    current = make_product("lavadora", product_type="Lavadora")
    forbidden = make_product("adega", product_type="Adega")

    score, reasons = score_candidate(current, forbidden)

    assert score <= -100
    assert "Relacao provisoriamente bloqueada pela politica editorial." in reasons


def test_weak_relation_is_demoted_by_policy() -> None:
    current = make_product("acessorio", product_type="Acessorio de Cozinha")
    weak_candidate = make_product("cuba", product_type="Cuba")

    weak_score, weak_reasons = score_candidate(current, weak_candidate)

    assert weak_score > -100
    assert "Relacao provisoria fraca; prioridade reduzida." in weak_reasons


def test_contextual_relation_is_marked_in_reason() -> None:
    current = make_product("adega", product_type="Adega")
    candidate = make_product("cervejeira", product_type="Cervejeira")

    _, reasons = score_candidate(current, candidate)

    assert "Pode fazer sentido em projeto gourmet, mas depende do contexto." in reasons


def test_universal_relation_receives_strong_reason() -> None:
    current = make_product("cooktop", product_type="Cooktop")
    candidate = make_product("coifa", product_type="Coifa")

    _, reasons = score_candidate(current, candidate)

    assert "Relacao comum em projetos de cozinha." in reasons


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


def test_recommendations_include_image_url_when_candidate_has_image(
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
        image_url="https://cdn.example.com/cooktop.jpg",
        product_type="Cooktop",
        price=Decimal("9500.00"),
    )
    create_db_product(
        db_session,
        store,
        "candidate-forno",
        image_url=None,
        product_type="Forno",
        price=Decimal("12000.00"),
    )
    db_session.commit()

    response = client.get("/recommendations", params={"product_id": "current-coifa"})

    assert response.status_code == 200
    payload = response.json()
    candidate = next(
        item
        for item in payload["recommendations"]
        if item["product_id"] == "candidate-cooktop"
    )
    assert candidate["image_url"] == "https://cdn.example.com/cooktop.jpg"
    assert candidate["url"] == "https://www.kouzinaclub.com.br/"
    assert candidate["reason"]
    assert isinstance(candidate["score"], float)


def test_review_recommendations_generates_expected_csv(
    db_session: Session,
    tmp_path: Path,
) -> None:
    store = create_store(db_session)
    create_db_product(
        db_session,
        store,
        "source-cuba",
        name="Cuba de teste",
        product_type="Cuba",
        category="Cozinha",
        brand="Franke",
        price=Decimal("4000.00"),
        url="https://www.kouzinaclub.com.br/cuba",
        image_url="https://cdn.example.com/cuba.jpg",
    )
    create_db_product(
        db_session,
        store,
        "recommended-misturador",
        name="Misturador de teste",
        product_type="Misturador",
        category="Cozinha",
        brand="Franke",
        price=Decimal("3500.00"),
        url="https://www.kouzinaclub.com.br/misturador",
        image_url="https://cdn.example.com/misturador.jpg",
    )
    create_db_product(
        db_session,
        store,
        "candidate-coifa",
        name="Coifa de teste",
        product_type="Coifa",
        category="Coifas",
        brand="Elettromec",
        price=Decimal("9000.00"),
        url="https://www.kouzinaclub.com.br/coifa",
        image_url="https://cdn.example.com/coifa.jpg",
    )
    db_session.commit()
    output_path = tmp_path / "recommendation_review.csv"

    source_count, row_count = generate_review_csv(
        db_session,
        output_path=output_path,
        limit_products=1,
        top_k=2,
        product_type="Cuba",
    )

    assert source_count == 1
    assert row_count == 2
    assert output_path.exists()

    import csv

    with output_path.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)

    assert reader.fieldnames == REVIEW_COLUMNS
    assert rows
    assert all(row["source_product_id"] != row["recommended_product_id"] for row in rows)
    assert all(row["score"] for row in rows)
    assert all(row["reason"] for row in rows)
    assert all(row["source_url"] for row in rows)
    assert all(row["recommended_url"] for row in rows)
    assert any(row["recommended_image_url"] for row in rows)
    assert rows[0]["recommended_product_id"] == "recommended-misturador"
    assert rows[0]["relation_class"]
    assert rows[0]["relation_type"]
    assert rows[0]["relation_policy_action"]
    assert rows[0]["validation_status"]
    assert rows[0]["requires_project_context"] in {"true", "false"}
    assert rows[0]["requires_installation_check"] in {"true", "false"}
    assert rows[0]["quote_policy"]
    assert "is_policy_demoted" in rows[0]
    assert "is_policy_blocked" in rows[0]
    assert rows[0]["reason_quality"]
    assert rows[0]["labels"]
    assert rows[0]["reviewer_rating"] == ""
    assert rows[0]["reviewer_comment"] == ""


def test_review_csv_marks_quote_policy_fields_for_sob_consulta(
    db_session: Session,
    tmp_path: Path,
) -> None:
    store = create_store(db_session)
    create_db_product(
        db_session,
        store,
        "source-cooktop",
        name="Cooktop de teste",
        product_type="Cooktop",
        category="Cozinha",
        brand="Franke",
        price=Decimal("9000.00"),
        availability_text="Disponivel",
    )
    create_db_product(
        db_session,
        store,
        "recommended-coifa-sob-consulta",
        name="Coifa sob consulta",
        product_type="Coifa",
        category="Coifas",
        brand="Franke",
        price=None,
        available=True,
        availability_text="Sob consulta",
    )
    db_session.commit()
    output_path = tmp_path / "recommendation_review_quote.csv"

    source_count, row_count = generate_review_csv(
        db_session,
        output_path=output_path,
        limit_products=1,
        top_k=1,
        product_type="Cooktop",
    )

    assert source_count == 1
    assert row_count == 1

    import csv

    with output_path.open("r", encoding="utf-8", newline="") as csv_file:
        row = next(csv.DictReader(csv_file))

    assert row["recommended_product_id"] == "recommended-coifa-sob-consulta"
    assert row["relation_class"] == "universal"
    assert row["quote_policy"] == "allow_if_strong"
    assert row["is_quote_only"] == "true"
    assert row["quote_reason"]
    assert "Produto sob consulta" in row["reason"]


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

    assert imported_count >= 30
    assert db_session.query(Store).count() == 1
    assert db_session.query(Product).count() == imported_count

    response = client.get("/recommendations", params={"product_id": "mock-001"})

    assert response.status_code == 200
    payload = response.json()
    recommendation_ids = [item["product_id"] for item in payload["recommendations"]]
    assert "mock-001" not in recommendation_ids
    assert recommendation_ids


def write_official_fixture(path: Path) -> None:
    header = [
        "C\u00f3digo categoria",
        "Nome produto",
        "Imagem principal",
        "Imagem 2",
        "Imagem 3",
        "Imagem 4",
        "Pre\u00e7o venda",
        "Marca",
        "Modelo",
        "Refer\u00eancia",
        "Endere\u00e7o do Produto (URL Tray)",
        "Imagens adicionais",
        "Nome categoria",
        "Caracter\u00edstica: Voltagem",
        "Caracter\u00edstica: Queimadores",
        "Caracter\u00edstica: Por Departamento",
    ]
    rows = [
        [
            "100",
            "Coifa Ilha 90cm Teste",
            "https://cdn.example.com/coifa-principal.jpg|https://cdn.example.com/coifa-principal-2.jpg",
            "https://cdn.example.com/coifa-2.jpg",
            "",
            "",
            "0.00",
            "Bert. Ital",
            "BI90",
            "REAL-001",
            "https://www.kouzinaclub.com.br/coifa-real",
            "https://cdn.example.com/coifa-extra.jpg|https://cdn.example.com/coifa-extra-2.jpg",
            "Coifas",
            "220v, 220v",
            "",
            "Cozinha",
        ],
        [
            "101",
            "Adega 45 Garrafas Built-in 60cm Teste",
            "",
            "https://cdn.example.com/adega-2.jpg",
            "",
            "",
            "",
            "Crissair",
            "AD45",
            "",
            "https://www.kouzinaclub.com.br/adega-real",
            "",
            "Adegas",
            "Bivolt",
            "",
            "Espa\u00e7o Gourmet",
        ],
        [
            "102",
            "Forno sem imagem 60cm Teste",
            "",
            "",
            "",
            "",
            "8500.00",
            "Elettromec",
            "FOR60",
            "REAL-003",
            "https://www.kouzinaclub.com.br/forno-sem-imagem",
            "",
            "Fornos",
            "220v",
            "",
            "Cozinha",
        ],
    ]
    lines = [";".join(header), *[";".join(row) for row in rows]]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8-sig")


def test_official_kouzina_csv_import_maps_expected_fields(
    db_session: Session,
    tmp_path: Path,
) -> None:
    official_csv = tmp_path / "products_kouzina_official.csv"
    write_official_fixture(official_csv)

    imported_count = import_products_from_csv(db_session, official_csv)

    assert imported_count == 3

    coifa = db_session.query(Product).filter(Product.external_id == "REAL-001").one()
    assert coifa.name == "Coifa Ilha 90cm Teste"
    assert coifa.url == "https://www.kouzinaclub.com.br/coifa-real"
    assert coifa.image_url == "https://cdn.example.com/coifa-principal.jpg"
    assert coifa.brand == "Bertazzoni It\u00e1lia"
    assert coifa.price is None
    assert coifa.available is True
    assert coifa.availability_text == "Sob consulta"
    assert coifa.voltage == "220v"
    assert coifa.width_cm == Decimal("90.00")
    assert coifa.installation_type == "Ilha"
    assert coifa.product_type == "Coifa"
    assert coifa.environment == "Cozinha Gourmet"
    assert coifa.premium_level == "Sob consulta"

    adega = db_session.query(Product).filter(Product.external_id == "kouzina-auto-2").one()
    assert adega.url == "https://www.kouzinaclub.com.br/adega-real"
    assert adega.image_url == "https://cdn.example.com/adega-2.jpg"
    assert adega.price is None
    assert adega.availability_text == "Pre\u00e7o n\u00e3o informado"
    assert adega.voltage == "bivolt"
    assert adega.installation_type == "Embutir"
    assert adega.product_type == "Adega"
    assert adega.environment == "Espa\u00e7o Gourmet"

    forno = db_session.query(Product).filter(Product.external_id == "REAL-003").one()
    assert forno.image_url is None
    assert forno.price == Decimal("8500.00")


def test_catalog_curadoria_infers_additional_product_types() -> None:
    cases = [
        ("Espa\u00e7o Gourmet", "Queimador Lateral \u00e0 G\u00e1s GLP Dual Burner", "Queimador"),
        ("Espa\u00e7o Gourmet", "Dispenser de \u00c1gua Sole Built-in 60cm 220v", "Dispenser de \u00c1gua"),
        ("Cozinha", "Kit Exaustor p/ Extractor Mythos", "Acess\u00f3rio de Coifa"),
        ("Cozinha", "Cafeteira de Embutir Mythos 45cm 220V", "Cafeteira"),
        ("Cozinha", "Cuba de Embutir Kubus Onyx Fragranite 62x42", "Cuba"),
        ("Cozinha", "Misturador Monocomando de Mesa A\u00e7o Inox", "Misturador"),
        ("Cozinha", "Set Azeite & Vinagre Cl\u00e1ssico 17 cm", "Acess\u00f3rio de Cozinha"),
        ("Fornos", "Forno de Pizza de Embutir", "Forno de Pizza"),
        ("Gavetas Refrigeradoras", "Gaveta Refrigerada 24 pol", "Gaveta Refrigerada"),
        ("Maquina de Gelo", "M\u00e1quina de Gelo Built-in", "M\u00e1quina de Gelo"),
    ]

    for category, name, expected_type in cases:
        assert infer_product_type(category, name) == expected_type


def test_catalog_curadoria_infers_environment_from_product_type() -> None:
    assert infer_environment("Cuba", None, None) == "Cozinha Gourmet"
    assert infer_environment("Misturador", None, None) == "Cozinha Gourmet"
    assert infer_environment("Queimador", None, None) == "Espa\u00e7o Gourmet"
    assert infer_environment("Forno de Pizza", None, None) == "Espa\u00e7o Gourmet"
    assert infer_environment("Gaveta Refrigerada", None, None) == "Refrigera\u00e7\u00e3o"
    assert infer_environment("Secadora", None, None) == "Lavanderia"


def test_catalog_curadoria_normalizes_brand_category_and_voltage() -> None:
    assert normalize_brand(" Bert.   Ital ") == "Bertazzoni It\u00e1lia"
    assert normalize_brand("Bertazzoni Italia") == "Bertazzoni It\u00e1lia"
    assert normalize_brand("  Franke   Premium  ") == "Franke Premium"
    assert normalize_brand("") is None

    assert normalize_category(" Espaco   Gourmet ") == "Espa\u00e7o Gourmet"
    assert normalize_category("Refrigeracao") == "Refrigera\u00e7\u00e3o"
    assert normalize_category("") is None

    assert normalize_voltage("220v, 220v") == "220v"
    assert normalize_voltage("127v, 127v") == "127v"
    assert normalize_voltage("Bivolt") == "bivolt"
    assert normalize_voltage("127v, 220v") == "bivolt"


def test_replace_products_keeps_events(
    db_session: Session,
    tmp_path: Path,
) -> None:
    store = create_store(db_session)
    create_db_product(db_session, store, "old-product")
    db_session.add(
        RecommendationEvent(
            store_id=store.id,
            event_type="page_view",
            anonymous_id="anon_123",
            session_id="sess_123",
            page_url="http://localhost:5500/demo.html",
            product_external_id="old-product",
            widget_id="product-page",
            recommended_product_external_id=None,
            event_metadata={},
        )
    )
    db_session.commit()
    official_csv = tmp_path / "products_kouzina_official.csv"
    write_official_fixture(official_csv)

    imported_count = import_products_from_csv(
        db_session,
        official_csv,
        replace_products=True,
    )

    assert imported_count == 3
    assert db_session.query(Product).filter(Product.external_id == "old-product").count() == 0
    assert db_session.query(RecommendationEvent).count() == 1


def test_recommender_ignores_close_price_when_price_is_null() -> None:
    current = make_product("current", product_type="Coifa", price=None)
    candidate = make_product(
        "candidate",
        product_type="Cooktop",
        price=Decimal("1000.00"),
    )

    _, reasons = score_candidate(current, candidate)

    assert "Faixa de preco proxima." not in reasons


def test_recommender_can_recommend_sob_consulta_product() -> None:
    current = make_product("current", product_type="Coifa", price=Decimal("1000.00"))
    candidate = make_product(
        "sob-consulta",
        product_type="Cooktop",
        price=None,
        available=True,
        availability_text="Sob consulta",
    )

    score, reasons = score_candidate(current, candidate)

    assert score > 0
    assert (
        "Produto sob consulta: recomendado apenas quando houver intencao consultiva."
        in reasons
    )
    assert "Produto indisponivel no catalogo." not in reasons


def test_sob_consulta_weak_relations_do_not_dominate_top3() -> None:
    current = make_product("current", product_type="Coifa", price=Decimal("10000.00"))
    strong_candidate = make_product(
        "strong-cooktop",
        product_type="Cooktop",
        availability_text="Disponivel",
        price=Decimal("9500.00"),
    )
    weak_quote_1 = make_product(
        "weak-quote-1",
        product_type="Acessorio de Cozinha",
        availability_text="Sob consulta",
        price=None,
    )
    weak_quote_2 = make_product(
        "weak-quote-2",
        product_type="Dispenser de Agua",
        availability_text="Sob consulta",
        price=None,
    )
    weak_quote_3 = make_product(
        "weak-quote-3",
        product_type="Conjugada",
        availability_text="Sob consulta",
        price=None,
    )

    recommendations = recommend_from_catalog(
        current,
        [current, strong_candidate, weak_quote_1, weak_quote_2, weak_quote_3],
        limit=4,
    )

    top3 = recommendations[:3]
    weak_quote_count = sum(
        1
        for item in top3
        if "Produto sob consulta fora de relacao forte: usar com cautela." in item.reason
    )
    assert weak_quote_count <= 1
    assert any(item.product_id == "strong-cooktop" for item in recommendations)


def test_events_accept_future_funnel_payload(client: TestClient, db_session: Session) -> None:
    response = client.post(
        "/events",
        json={
            "event_name": "recommendations_rendered",
            "anonymous_id": "anon_future_1",
            "session_id": "sess_future_1",
            "page_url": "http://localhost:5500/demo.html",
            "source_product_id": "source-001",
            "source_product_type": "Cooktop",
            "recommended_product_id": "recommended-001",
            "recommended_product_type": "Coifa",
            "rank": 1,
            "score": 92.0,
            "relation_class": "universal",
            "relation_type": "complement",
            "relation_policy_action": "boost",
            "validation_status": "agent_hypothesis",
            "is_quote_only": False,
            "quote_reason": "",
            "environment": "Cozinha Gourmet",
            "brand": "Franke",
            "price_band": "high",
            "funnel_stage": "rendered",
            "metadata": {"email": "blocked@example.com", "score": 91.5},
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["event_type"] == "recommendations_rendered"

    saved_event = db_session.query(RecommendationEvent).order_by(RecommendationEvent.id.desc()).first()
    assert saved_event is not None
    assert saved_event.product_external_id == "source-001"
    assert saved_event.recommended_product_external_id == "recommended-001"
    assert saved_event.event_metadata["event_name"] == "recommendations_rendered"
    assert saved_event.event_metadata["source_product_type"] == "Cooktop"
    assert saved_event.event_metadata["relation_class"] == "universal"
    assert saved_event.event_metadata["score"] == 92.0
    assert "email" not in saved_event.event_metadata


def test_events_require_event_type_or_event_name(client: TestClient) -> None:
    response = client.post(
        "/events",
        json={
            "anonymous_id": "anon_missing_event",
            "session_id": "sess_missing_event",
            "page_url": "http://localhost:5500/demo.html",
            "metadata": {},
        },
    )

    assert response.status_code == 422
