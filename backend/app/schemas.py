from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


AllowedEventType = Literal[
    "page_view",
    "product_view",
    "recommendation_impression",
    "recommendation_click",
]


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


class EventIn(BaseModel):
    event_type: AllowedEventType
    anonymous_id: str = Field(min_length=1, max_length=128)
    session_id: str | None = Field(default=None, max_length=128)
    page_url: str | None = Field(default=None, max_length=2048)
    product_id: str | None = Field(default=None, max_length=128)
    widget_id: str | None = Field(default=None, max_length=128)
    recommended_product_id: str | None = Field(default=None, max_length=128)
    metadata: dict[str, Any] = Field(default_factory=dict)


class EventResponse(BaseModel):
    received: bool
    event_type: AllowedEventType
    timestamp: datetime


class RecommendationItem(BaseModel):
    product_id: str
    name: str
    url: HttpUrl
    image_url: HttpUrl | None = None
    price: float | None = None
    reason: str
    score: float

    model_config = ConfigDict(json_encoders={HttpUrl: str})


class RecommendationResponse(BaseModel):
    widget_title: str
    product_id: str | None
    recommendations: list[RecommendationItem]

