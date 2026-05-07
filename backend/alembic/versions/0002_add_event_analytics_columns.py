"""Add optional analytics columns to recommendation events."""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "0002_add_event_analytics_columns"
down_revision: str | None = "0001_initial_schema"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("recommendation_events", sa.Column("event_name", sa.String(length=100), nullable=True))
    op.add_column("recommendation_events", sa.Column("source_product_type", sa.String(length=128), nullable=True))
    op.add_column("recommendation_events", sa.Column("recommended_product_type", sa.String(length=128), nullable=True))
    op.add_column("recommendation_events", sa.Column("rank", sa.Integer(), nullable=True))
    op.add_column("recommendation_events", sa.Column("score", sa.Float(), nullable=True))
    op.add_column("recommendation_events", sa.Column("relation_class", sa.String(length=64), nullable=True))
    op.add_column("recommendation_events", sa.Column("relation_type", sa.String(length=64), nullable=True))
    op.add_column("recommendation_events", sa.Column("relation_policy_action", sa.String(length=64), nullable=True))
    op.add_column("recommendation_events", sa.Column("validation_status", sa.String(length=64), nullable=True))
    op.add_column("recommendation_events", sa.Column("is_quote_only", sa.Boolean(), nullable=True))
    op.add_column("recommendation_events", sa.Column("quote_reason", sa.String(length=255), nullable=True))
    op.add_column("recommendation_events", sa.Column("environment", sa.String(length=128), nullable=True))
    op.add_column("recommendation_events", sa.Column("brand", sa.String(length=128), nullable=True))
    op.add_column("recommendation_events", sa.Column("price_band", sa.String(length=128), nullable=True))
    op.add_column("recommendation_events", sa.Column("funnel_stage", sa.String(length=128), nullable=True))

    op.create_index("ix_recommendation_events_event_name", "recommendation_events", ["event_name"], unique=False)
    op.create_index("ix_recommendation_events_source_product_type", "recommendation_events", ["source_product_type"], unique=False)
    op.create_index(
        "ix_recommendation_events_recommended_product_type",
        "recommendation_events",
        ["recommended_product_type"],
        unique=False,
    )
    op.create_index("ix_recommendation_events_relation_class", "recommendation_events", ["relation_class"], unique=False)
    op.create_index("ix_recommendation_events_relation_type", "recommendation_events", ["relation_type"], unique=False)
    op.create_index("ix_recommendation_events_created_at", "recommendation_events", ["created_at"], unique=False)
    op.create_index(
        "ix_recommendation_events_event_type_created_at",
        "recommendation_events",
        ["event_type", "created_at"],
        unique=False,
    )
    op.create_index(
        "ix_recommendation_events_session_created_at",
        "recommendation_events",
        ["session_id", "created_at"],
        unique=False,
    )
    op.create_index(
        "ix_recommendation_events_product_created_at",
        "recommendation_events",
        ["product_external_id", "created_at"],
        unique=False,
    )
    op.create_index(
        "ix_recommendation_events_recommended_product_created_at",
        "recommendation_events",
        ["recommended_product_external_id", "created_at"],
        unique=False,
    )
    op.create_index(
        "ix_recommendation_events_relation_class_created_at",
        "recommendation_events",
        ["relation_class", "created_at"],
        unique=False,
    )
    op.create_index(
        "ix_recommendation_events_relation_type_created_at",
        "recommendation_events",
        ["relation_type", "created_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_recommendation_events_relation_type_created_at", table_name="recommendation_events")
    op.drop_index("ix_recommendation_events_relation_class_created_at", table_name="recommendation_events")
    op.drop_index("ix_recommendation_events_recommended_product_created_at", table_name="recommendation_events")
    op.drop_index("ix_recommendation_events_product_created_at", table_name="recommendation_events")
    op.drop_index("ix_recommendation_events_session_created_at", table_name="recommendation_events")
    op.drop_index("ix_recommendation_events_event_type_created_at", table_name="recommendation_events")
    op.drop_index("ix_recommendation_events_created_at", table_name="recommendation_events")
    op.drop_index("ix_recommendation_events_relation_type", table_name="recommendation_events")
    op.drop_index("ix_recommendation_events_relation_class", table_name="recommendation_events")
    op.drop_index("ix_recommendation_events_recommended_product_type", table_name="recommendation_events")
    op.drop_index("ix_recommendation_events_source_product_type", table_name="recommendation_events")
    op.drop_index("ix_recommendation_events_event_name", table_name="recommendation_events")

    op.drop_column("recommendation_events", "funnel_stage")
    op.drop_column("recommendation_events", "price_band")
    op.drop_column("recommendation_events", "brand")
    op.drop_column("recommendation_events", "environment")
    op.drop_column("recommendation_events", "quote_reason")
    op.drop_column("recommendation_events", "is_quote_only")
    op.drop_column("recommendation_events", "validation_status")
    op.drop_column("recommendation_events", "relation_policy_action")
    op.drop_column("recommendation_events", "relation_type")
    op.drop_column("recommendation_events", "relation_class")
    op.drop_column("recommendation_events", "score")
    op.drop_column("recommendation_events", "rank")
    op.drop_column("recommendation_events", "recommended_product_type")
    op.drop_column("recommendation_events", "source_product_type")
    op.drop_column("recommendation_events", "event_name")
