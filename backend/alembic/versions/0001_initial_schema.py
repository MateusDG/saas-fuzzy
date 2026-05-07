"""Initial schema for Kouzina Reco."""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "0001_initial_schema"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "stores",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("slug", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("domain", sa.String(length=255), nullable=True),
        sa.Column("public_key", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("public_key"),
        sa.UniqueConstraint("slug"),
    )
    op.create_index("ix_stores_id", "stores", ["id"], unique=False)
    op.create_index("ix_stores_slug", "stores", ["slug"], unique=True)

    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("store_id", sa.Integer(), nullable=False),
        sa.Column("external_id", sa.String(length=100), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("url", sa.Text(), nullable=False),
        sa.Column("image_url", sa.Text(), nullable=True),
        sa.Column("category", sa.String(length=255), nullable=True),
        sa.Column("subcategory", sa.String(length=255), nullable=True),
        sa.Column("brand", sa.String(length=255), nullable=True),
        sa.Column("price", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("promotional_price", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("available", sa.Boolean(), nullable=False),
        sa.Column("availability_text", sa.String(length=255), nullable=True),
        sa.Column("stock", sa.Integer(), nullable=True),
        sa.Column("voltage", sa.String(length=50), nullable=True),
        sa.Column("width_cm", sa.Numeric(precision=8, scale=2), nullable=True),
        sa.Column("installation_type", sa.String(length=100), nullable=True),
        sa.Column("product_type", sa.String(length=100), nullable=True),
        sa.Column("environment", sa.String(length=100), nullable=True),
        sa.Column("premium_level", sa.String(length=100), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["store_id"], ["stores.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("store_id", "external_id", name="uq_products_store_external_id"),
    )
    op.create_index("ix_products_active", "products", ["active"], unique=False)
    op.create_index("ix_products_available", "products", ["available"], unique=False)
    op.create_index("ix_products_category", "products", ["category"], unique=False)
    op.create_index("ix_products_external_id", "products", ["external_id"], unique=False)
    op.create_index("ix_products_id", "products", ["id"], unique=False)
    op.create_index("ix_products_store_id", "products", ["store_id"], unique=False)

    op.create_table(
        "manual_product_relations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("store_id", sa.Integer(), nullable=False),
        sa.Column("source_product_id", sa.Integer(), nullable=False),
        sa.Column("target_product_id", sa.Integer(), nullable=False),
        sa.Column("relation_type", sa.String(length=100), nullable=False),
        sa.Column("weight", sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["source_product_id"], ["products.id"]),
        sa.ForeignKeyConstraint(["store_id"], ["stores.id"]),
        sa.ForeignKeyConstraint(["target_product_id"], ["products.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_manual_product_relations_id", "manual_product_relations", ["id"], unique=False)
    op.create_index("ix_manual_product_relations_store_id", "manual_product_relations", ["store_id"], unique=False)

    op.create_table(
        "recommendation_events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("store_id", sa.Integer(), nullable=True),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column("anonymous_id", sa.String(length=255), nullable=True),
        sa.Column("session_id", sa.String(length=255), nullable=True),
        sa.Column("page_url", sa.Text(), nullable=True),
        sa.Column("product_external_id", sa.String(length=100), nullable=True),
        sa.Column("widget_id", sa.String(length=100), nullable=True),
        sa.Column("recommended_product_external_id", sa.String(length=100), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["store_id"], ["stores.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_recommendation_events_anonymous_id", "recommendation_events", ["anonymous_id"], unique=False)
    op.create_index("ix_recommendation_events_event_type", "recommendation_events", ["event_type"], unique=False)
    op.create_index("ix_recommendation_events_id", "recommendation_events", ["id"], unique=False)
    op.create_index(
        "ix_recommendation_events_product_external_id",
        "recommendation_events",
        ["product_external_id"],
        unique=False,
    )
    op.create_index(
        "ix_recommendation_events_recommended_product_external_id",
        "recommendation_events",
        ["recommended_product_external_id"],
        unique=False,
    )
    op.create_index("ix_recommendation_events_session_id", "recommendation_events", ["session_id"], unique=False)
    op.create_index("ix_recommendation_events_store_id", "recommendation_events", ["store_id"], unique=False)


def downgrade() -> None:
    op.drop_table("recommendation_events")
    op.drop_table("manual_product_relations")
    op.drop_table("products")
    op.drop_table("stores")
