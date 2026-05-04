import csv
from pathlib import Path

from app.export_review_pack import generate_review_pack
from app.review_recommendations import REVIEW_COLUMNS


def write_review_csv(path: Path, rows: list[dict[str, str]], columns: list[str] | None = None) -> None:
    fieldnames = columns or REVIEW_COLUMNS
    with path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def valid_review_row(**overrides: str) -> dict[str, str]:
    row = {
        "source_product_id": "119",
        "source_name": "Churrasqueira de Embutir",
        "source_product_type": "Churrasqueira",
        "source_category": "Espaco Gourmet",
        "source_brand": "Coyote",
        "source_price": "",
        "source_availability_text": "Sob consulta",
        "recommended_product_id": "ADEGA-001",
        "recommended_name": "Adega climatizada",
        "recommended_product_type": "Adega",
        "recommended_category": "Adegas",
        "recommended_brand": "Elettromec",
        "recommended_price": "6990.00",
        "recommended_availability_text": "Preco informado",
        "score": "75.0",
        "reason": "Produto complementar ao item visualizado.",
        "source_url": "https://www.kouzinaclub.com.br/source",
        "recommended_url": "https://www.kouzinaclub.com.br/recommended",
        "recommended_image_url": "https://cdn.example.com/adega.jpg",
        "reviewer_rating": "",
        "reviewer_comment": "",
    }
    row.update(overrides)
    return row


def test_review_pack_generates_html_with_title_summary_and_rating_scale(tmp_path: Path) -> None:
    input_path = tmp_path / "recommendation_review.csv"
    output_path = tmp_path / "recommendation_review.html"
    write_review_csv(input_path, [valid_review_row()])

    stats = generate_review_pack(input_path=input_path, output_path=output_path)
    html = output_path.read_text(encoding="utf-8")

    assert stats.row_count == 1
    assert stats.source_product_count == 1
    assert output_path.exists()
    assert "Kouzina Reco — Revisão Qualitativa" in html
    assert "1 = ruim" in html
    assert "2 = fraca" in html
    assert "3 = aceitável" in html
    assert "4 = boa" in html
    assert "5 = excelente" in html
    assert "Esse produto realmente complementa o produto atual?" in html


def test_review_pack_escapes_html_in_names_and_comments(tmp_path: Path) -> None:
    input_path = tmp_path / "recommendation_review.csv"
    output_path = tmp_path / "recommendation_review.html"
    write_review_csv(
        input_path,
        [
            valid_review_row(
                source_name="<script>alert('x')</script>",
                recommended_name="<b>Adega</b>",
                reviewer_comment="<img src=x onerror=alert(1)>",
            )
        ],
    )

    generate_review_pack(input_path=input_path, output_path=output_path)
    html = output_path.read_text(encoding="utf-8")

    assert "<script>alert('x')</script>" not in html
    assert "<b>Adega</b>" not in html
    assert "<img src=x onerror=alert(1)>" not in html
    assert "&lt;script&gt;alert(&#x27;x&#x27;)&lt;/script&gt;" in html
    assert "&lt;b&gt;Adega&lt;/b&gt;" in html
    assert "&lt;img src=x onerror=alert(1)&gt;" in html


def test_review_pack_handles_empty_optional_fields(tmp_path: Path) -> None:
    input_path = tmp_path / "minimal_review.csv"
    output_path = tmp_path / "minimal_review.html"
    write_review_csv(
        input_path,
        [
            {
                "source_product_id": "SOURCE-001",
                "source_name": "Produto origem",
                "recommended_product_id": "REC-001",
                "recommended_name": "Produto recomendado",
                "score": "",
                "reason": "",
            }
        ],
        columns=[
            "source_product_id",
            "source_name",
            "recommended_product_id",
            "recommended_name",
            "score",
            "reason",
        ],
    )

    stats = generate_review_pack(input_path=input_path, output_path=output_path)
    html = output_path.read_text(encoding="utf-8")

    assert stats.row_count == 1
    assert "Nao informado" in html
    assert "Link ausente" in html
    assert "Sem imagem" in html
    assert "Sem explicacao registrada." in html


def test_review_pack_filters_by_limit_min_score_and_product_type(tmp_path: Path) -> None:
    input_path = tmp_path / "recommendation_review.csv"
    output_path = tmp_path / "recommendation_review.html"
    write_review_csv(
        input_path,
        [
            valid_review_row(recommended_product_id="LOW", score="20", recommended_name="Baixo"),
            valid_review_row(recommended_product_id="HIGH-1", score="90", recommended_name="Alto 1"),
            valid_review_row(recommended_product_id="OTHER", source_product_type="Coifa", score="95"),
            valid_review_row(recommended_product_id="HIGH-2", score="91", recommended_name="Alto 2"),
        ],
    )

    stats = generate_review_pack(
        input_path=input_path,
        output_path=output_path,
        limit=1,
        min_score=80,
        product_type="Churrasqueira",
    )
    html = output_path.read_text(encoding="utf-8")

    assert stats.row_count == 1
    assert "Alto 1" in html
    assert "Baixo" not in html
    assert "Coifa" not in html
    assert "Alto 2" not in html
