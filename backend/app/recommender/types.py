from typing import Protocol


class ProductLike(Protocol):
    external_id: str
    name: str
    url: str
    image_url: str | None
    price: object
    available: bool
    category: str | None
    brand: str | None
    voltage: str | None
    environment: str | None
    product_type: str | None
    premium_level: str | None
    availability_text: str | None
