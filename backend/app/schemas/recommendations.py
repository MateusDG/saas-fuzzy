from pydantic import BaseModel, ConfigDict, HttpUrl


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
