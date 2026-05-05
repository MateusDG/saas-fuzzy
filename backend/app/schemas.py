from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator


AllowedEventType = Literal[
    "page_view",
    "product_view",
    "recommendation_impression",
    "recommendation_click",
    "recommendation_clicked",
    "widget_opened",
    "product_context_loaded",
    "recommendations_requested",
    "recommendations_rendered",
    "recommendation_expanded",
    "recommendation_dismissed",
    "quote_requested",
    "add_to_cart_clicked",
    "alternative_requested",
    "session_ended",
]


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


class EventIn(BaseModel):
    event_type: AllowedEventType | None = None
    event_name: AllowedEventType | None = None
    anonymous_id: str = Field(min_length=1, max_length=128)
    session_id: str | None = Field(default=None, max_length=128)
    page_url: str | None = Field(default=None, max_length=2048)
    product_id: str | None = Field(default=None, max_length=128)
    source_product_id: str | None = Field(default=None, max_length=128)
    source_product_type: str | None = Field(default=None, max_length=128)
    widget_id: str | None = Field(default=None, max_length=128)
    recommended_product_id: str | None = Field(default=None, max_length=128)
    recommended_product_type: str | None = Field(default=None, max_length=128)
    timestamp: datetime | None = None
    rank: int | None = Field(default=None, ge=0, le=100)
    score: float | None = None
    relation_class: str | None = Field(default=None, max_length=64)
    relation_type: str | None = Field(default=None, max_length=64)
    relation_policy_action: str | None = Field(default=None, max_length=64)
    validation_status: str | None = Field(default=None, max_length=64)
    is_quote_only: bool | None = None
    quote_reason: str | None = Field(default=None, max_length=255)
    environment: str | None = Field(default=None, max_length=128)
    brand: str | None = Field(default=None, max_length=128)
    price_band: str | None = Field(default=None, max_length=128)
    funnel_stage: str | None = Field(default=None, max_length=128)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_event_name(self) -> "EventIn":
        if not self.event_name and not self.event_type:
            raise ValueError("event_name or event_type must be provided")
        return self

    @property
    def resolved_event_name(self) -> AllowedEventType:
        return self.event_name or self.event_type  # type: ignore[return-value]


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
