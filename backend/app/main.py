from datetime import UTC, datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .recommender import get_mock_recommendations
from .schemas import EventIn, EventResponse, HealthResponse, RecommendationResponse
from .settings import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="API minima para recomendacoes mockadas da Kouzina Reco.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service="kouzina-reco-api",
        version="0.1.0",
    )


@app.post("/events", response_model=EventResponse)
def create_event(event: EventIn) -> EventResponse:
    return EventResponse(
        received=True,
        event_type=event.event_type,
        timestamp=datetime.now(UTC),
    )


@app.get("/recommendations", response_model=RecommendationResponse)
def get_recommendations(
    product_id: str | None = None,
    widget_id: str | None = None,
) -> RecommendationResponse:
    return RecommendationResponse(
        widget_title="Complete seu projeto",
        product_id=product_id,
        recommendations=get_mock_recommendations(),
    )

