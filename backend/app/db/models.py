from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Index, Integer, JSON, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..core.database import Base


def utc_now() -> datetime:
    return datetime.now(UTC)


class Store(Base):
    __tablename__ = "stores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    domain: Mapped[str | None] = mapped_column(String(255), nullable=True)
    public_key: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    products: Mapped[list["Product"]] = relationship(back_populates="store")
    events: Mapped[list["RecommendationEvent"]] = relationship(back_populates="store")


class Product(Base):
    __tablename__ = "products"
    __table_args__ = (
        UniqueConstraint("store_id", "external_id", name="uq_products_store_external_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"), nullable=False, index=True)
    external_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    subcategory: Mapped[str | None] = mapped_column(String(255), nullable=True)
    brand: Mapped[str | None] = mapped_column(String(255), nullable=True)
    price: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    promotional_price: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    availability_text: Mapped[str | None] = mapped_column(String(255), nullable=True)
    stock: Mapped[int | None] = mapped_column(Integer, nullable=True)
    voltage: Mapped[str | None] = mapped_column(String(50), nullable=True)
    width_cm: Mapped[Decimal | None] = mapped_column(Numeric(8, 2), nullable=True)
    installation_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    product_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    environment: Mapped[str | None] = mapped_column(String(100), nullable=True)
    premium_level: Mapped[str | None] = mapped_column(String(100), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )

    store: Mapped[Store] = relationship(back_populates="products")


class ManualProductRelation(Base):
    __tablename__ = "manual_product_relations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"), nullable=False, index=True)
    source_product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    target_product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    relation_type: Mapped[str] = mapped_column(String(100), nullable=False)
    weight: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("1.0"), nullable=False)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)


class RecommendationEvent(Base):
    __tablename__ = "recommendation_events"
    __table_args__ = (
        Index("ix_recommendation_events_created_at", "created_at"),
        Index("ix_recommendation_events_event_type_created_at", "event_type", "created_at"),
        Index("ix_recommendation_events_session_created_at", "session_id", "created_at"),
        Index("ix_recommendation_events_product_created_at", "product_external_id", "created_at"),
        Index(
            "ix_recommendation_events_recommended_product_created_at",
            "recommended_product_external_id",
            "created_at",
        ),
        Index("ix_recommendation_events_relation_class_created_at", "relation_class", "created_at"),
        Index("ix_recommendation_events_relation_type_created_at", "relation_type", "created_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    store_id: Mapped[int | None] = mapped_column(ForeignKey("stores.id"), nullable=True, index=True)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    event_name: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    anonymous_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    session_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    page_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    product_external_id: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    widget_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    recommended_product_external_id: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    source_product_type: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    recommended_product_type: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    rank: Mapped[int | None] = mapped_column(Integer, nullable=True)
    score: Mapped[float | None] = mapped_column(Float, nullable=True)
    relation_class: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    relation_type: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    relation_policy_action: Mapped[str | None] = mapped_column(String(64), nullable=True)
    validation_status: Mapped[str | None] = mapped_column(String(64), nullable=True)
    is_quote_only: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    quote_reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
    environment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    brand: Mapped[str | None] = mapped_column(String(128), nullable=True)
    price_band: Mapped[str | None] = mapped_column(String(128), nullable=True)
    funnel_stage: Mapped[str | None] = mapped_column(String(128), nullable=True)
    event_metadata: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    store: Mapped[Store | None] = relationship(back_populates="events")
