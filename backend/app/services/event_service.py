from datetime import UTC, datetime

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..db.models import RecommendationEvent, Store
from ..schemas import EventIn, EventResponse


SAFE_METADATA_KEYS = {
    "event_name",
    "timestamp",
    "source_product_id",
    "source_product_type",
    "recommended_product_id",
    "recommended_product_type",
    "rank",
    "recommendation_count",
    "recommended_product_ids",
    "score",
    "relation_class",
    "relation_type",
    "relation_policy_action",
    "validation_status",
    "is_quote_only",
    "quote_reason",
    "environment",
    "brand",
    "price_band",
    "funnel_stage",
}


def sanitize_metadata(metadata: dict) -> dict:
    return {
        key: value
        for key, value in metadata.items()
        if key in SAFE_METADATA_KEYS
    }


def build_event_metadata(event: EventIn) -> dict:
    metadata = sanitize_metadata(event.metadata)
    event_data = {
        "event_name": event.resolved_event_name,
        "timestamp": event.timestamp.isoformat() if event.timestamp else None,
        "source_product_id": event.source_product_id or event.product_id,
        "source_product_type": event.source_product_type,
        "recommended_product_id": event.recommended_product_id,
        "recommended_product_type": event.recommended_product_type,
        "rank": event.rank,
        "score": event.score,
        "relation_class": event.relation_class,
        "relation_type": event.relation_type,
        "relation_policy_action": event.relation_policy_action,
        "validation_status": event.validation_status,
        "is_quote_only": event.is_quote_only,
        "quote_reason": event.quote_reason,
        "environment": event.environment,
        "brand": event.brand,
        "price_band": event.price_band,
        "funnel_stage": event.funnel_stage,
    }
    metadata.update({key: value for key, value in event_data.items() if value is not None})
    return sanitize_metadata(metadata)


def create_event(event: EventIn, db: Session) -> EventResponse:
    timestamp = datetime.now(UTC)
    resolved_event_name = event.resolved_event_name

    try:
        store = db.query(Store).filter(Store.slug == "kouzina").one_or_none()
        recommendation_event = RecommendationEvent(
            store_id=store.id if store else None,
            event_type=resolved_event_name,
            event_name=resolved_event_name,
            anonymous_id=event.anonymous_id,
            session_id=event.session_id,
            page_url=event.page_url,
            product_external_id=event.source_product_id or event.product_id,
            widget_id=event.widget_id,
            recommended_product_external_id=event.recommended_product_id,
            source_product_type=event.source_product_type,
            recommended_product_type=event.recommended_product_type,
            rank=event.rank,
            score=event.score,
            relation_class=event.relation_class,
            relation_type=event.relation_type,
            relation_policy_action=event.relation_policy_action,
            validation_status=event.validation_status,
            is_quote_only=event.is_quote_only,
            quote_reason=event.quote_reason,
            environment=event.environment,
            brand=event.brand,
            price_band=event.price_band,
            funnel_stage=event.funnel_stage,
            event_metadata=build_event_metadata(event),
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
        event_type=resolved_event_name,
        timestamp=timestamp,
    )
