from contextlib import asynccontextmanager
from datetime import UTC, datetime

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from .database import get_db, init_db
from .models import Product, RecommendationEvent, Store
from .recommender import get_mock_recommendations, recommend_from_catalog
from .schemas import EventIn, EventResponse, HealthResponse, RecommendationResponse
from .settings import get_settings

settings = get_settings()

SAFE_METADATA_KEYS = {
    "recommendation_count",
    "recommended_product_ids",
    "score",
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        init_db()
    except SQLAlchemyError as exc:
        print(f"[KouzinaReco] database startup skipped: {exc}")
    yield


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="API minima para recomendacoes mockadas da Kouzina Reco.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


def sanitize_metadata(metadata: dict) -> dict:
    return {
        key: value
        for key, value in metadata.items()
        if key in SAFE_METADATA_KEYS
    }


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service="kouzina-reco-api",
        version="0.1.0",
    )


@app.post("/events", response_model=EventResponse)
def create_event(event: EventIn, db: Session = Depends(get_db)) -> EventResponse:
    timestamp = datetime.now(UTC)

    try:
        store = db.query(Store).filter(Store.slug == "kouzina").one_or_none()
        recommendation_event = RecommendationEvent(
            store_id=store.id if store else None,
            event_type=event.event_type,
            anonymous_id=event.anonymous_id,
            session_id=event.session_id,
            page_url=event.page_url,
            product_external_id=event.product_id,
            widget_id=event.widget_id,
            recommended_product_external_id=event.recommended_product_id,
            event_metadata=sanitize_metadata(event.metadata),
        )
        db.add(recommendation_event)
        db.commit()
        db.refresh(recommendation_event)
        timestamp = recommendation_event.created_at
    except SQLAlchemyError as exc:
        db.rollback()
        print(f"[KouzinaReco] event persistence skipped: {exc}")

    return EventResponse(
        received=True,
        event_type=event.event_type,
        timestamp=timestamp,
    )


@app.get("/recommendations", response_model=RecommendationResponse)
def get_recommendations(
    product_id: str | None = None,
    widget_id: str | None = None,
    db: Session = Depends(get_db),
) -> RecommendationResponse:
    try:
        products = db.query(Product).filter(Product.active.is_(True)).all()
        if not products:
            raise LookupError("empty catalog")

        current_product = None
        if product_id:
            current_product = (
                db.query(Product)
                .filter(Product.external_id == product_id, Product.active.is_(True))
                .one_or_none()
            )

        recommendations = recommend_from_catalog(current_product, products)
        if recommendations:
            return RecommendationResponse(
                widget_title="Complete seu projeto",
                product_id=product_id,
                recommendations=recommendations,
            )
    except (SQLAlchemyError, LookupError) as exc:
        print(f"[KouzinaReco] recommendation fallback used: {exc}")

    return RecommendationResponse(
        widget_title="Complete seu projeto",
        product_id=product_id,
        recommendations=get_mock_recommendations(),
    )
