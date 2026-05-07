from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..db.models import Product
from ..recommender import get_mock_recommendations, recommend_from_catalog
from ..schemas import RecommendationResponse


def get_recommendation_response(
    product_id: str | None,
    db: Session,
) -> RecommendationResponse:
    try:
        if not product_id:
            raise LookupError("missing product_id")

        current_product = (
            db.query(Product)
            .filter(Product.external_id == product_id, Product.active.is_(True))
            .one_or_none()
        )
        if current_product is None:
            raise LookupError("current product not found")

        products = (
            db.query(Product)
            .filter(
                Product.store_id == current_product.store_id,
                Product.active.is_(True),
            )
            .all()
        )
        if len(products) <= 1:
            raise LookupError("insufficient candidates")

        recommendations = recommend_from_catalog(current_product, products, limit=4)
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
