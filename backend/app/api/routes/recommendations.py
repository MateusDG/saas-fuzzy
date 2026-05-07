from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...database import get_db
from ...schemas import RecommendationResponse
from ...services.recommendation_service import get_recommendation_response


router = APIRouter()


@router.get("/recommendations", response_model=RecommendationResponse)
def get_recommendations(
    product_id: str | None = None,
    widget_id: str | None = None,
    db: Session = Depends(get_db),
) -> RecommendationResponse:
    return get_recommendation_response(product_id=product_id, db=db)
