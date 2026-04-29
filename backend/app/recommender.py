from .schemas import RecommendationItem


MOCK_RECOMMENDATIONS = [
    RecommendationItem(
        product_id="mock-001",
        name="Cooktop premium compativel",
        url="https://www.kouzinaclub.com.br/",
        image_url=None,
        price=9990.0,
        reason="Produto complementar para composicao de cozinha gourmet.",
        score=0.92,
    ),
    RecommendationItem(
        product_id="mock-002",
        name="Forno de embutir recomendado",
        url="https://www.kouzinaclub.com.br/",
        image_url=None,
        price=8490.0,
        reason="Combina com projetos de cozinha planejada.",
        score=0.85,
    ),
    RecommendationItem(
        product_id="mock-003",
        name="Adega climatizada compacta",
        url="https://www.kouzinaclub.com.br/",
        image_url=None,
        price=6990.0,
        reason="Opcao complementar para espaco gourmet premium.",
        score=0.78,
    ),
]


def get_mock_recommendations() -> list[RecommendationItem]:
    return MOCK_RECOMMENDATIONS

