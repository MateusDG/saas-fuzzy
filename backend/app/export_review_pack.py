import argparse
import csv
from collections import Counter
from dataclasses import dataclass
from html import escape
from pathlib import Path
from unicodedata import normalize as unicode_normalize


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = PROJECT_ROOT / "reports" / "recommendation_review.csv"
DEFAULT_OUTPUT = PROJECT_ROOT / "reports" / "recommendation_review.html"


@dataclass(frozen=True)
class ReviewPackStats:
    row_count: int
    source_product_count: int
    product_type_count: int
    output_path: Path


def resolve_project_path(path: Path) -> Path:
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(PROJECT_ROOT))
    except ValueError:
        return path.name


def normalize_text(value: str | None) -> str:
    if not value:
        return ""

    normalized = unicode_normalize("NFKD", value)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    return " ".join(ascii_text.lower().replace("-", " ").split())


def row_value(row: dict[str, str], key: str) -> str:
    value = row.get(key, "")
    if value is None:
        return ""
    return str(value).strip()


def html_text(value: object) -> str:
    if value is None:
        return ""
    return escape(str(value), quote=True)


def safe_url(value: str) -> str:
    cleaned = value.strip()
    if cleaned.startswith(("http://", "https://")):
        return escape(cleaned, quote=True)
    return ""


def parse_score(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def format_price(value: str, availability_text: str) -> str:
    if value:
        return f"R$ {html_text(value)}"
    if normalize_text(availability_text) == "sob consulta":
        return "Sob consulta"
    return "Nao informado"


def read_review_rows(input_path: Path) -> list[dict[str, str]]:
    with input_path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        return [
            {key: value or "" for key, value in row.items() if key is not None}
            for row in reader
        ]


def filter_review_rows(
    rows: list[dict[str, str]],
    limit: int,
    min_score: float | None = None,
    product_type: str | None = None,
) -> list[dict[str, str]]:
    normalized_product_type = normalize_text(product_type)
    filtered: list[dict[str, str]] = []

    for row in rows:
        if normalized_product_type and normalize_text(row_value(row, "source_product_type")) != normalized_product_type:
            continue

        score = parse_score(row_value(row, "score"))
        if min_score is not None and (score is None or score < min_score):
            continue

        filtered.append(row)
        if limit > 0 and len(filtered) >= limit:
            break

    return filtered


def summarize_rows(rows: list[dict[str, str]]) -> tuple[int, int]:
    source_ids = {
        row_value(row, "source_product_id")
        for row in rows
        if row_value(row, "source_product_id")
    }
    product_types = {
        row_value(row, "source_product_type")
        for row in rows
        if row_value(row, "source_product_type")
    }
    return len(source_ids), len(product_types)


def product_type_summary(rows: list[dict[str, str]]) -> str:
    counts = Counter(
        row_value(row, "source_product_type") or "Sem tipo"
        for row in rows
    )
    if not counts:
        return "<p class=\"muted\">Nenhum tipo de produto encontrado no filtro atual.</p>"

    items = []
    for product_type, count in counts.most_common():
        items.append(
            "<span class=\"pill\">"
            f"{html_text(product_type)} <strong>{count}</strong>"
            "</span>"
        )
    return "\n".join(items)


def link_html(url: str, label: str) -> str:
    safe = safe_url(url)
    if not safe:
        return "<span class=\"link-disabled\">Link ausente</span>"
    return f"<a class=\"link-button\" href=\"{safe}\" target=\"_blank\" rel=\"noopener noreferrer\">{html_text(label)}</a>"


def image_html(row: dict[str, str]) -> str:
    image_url = safe_url(row_value(row, "recommended_image_url"))
    name = html_text(row_value(row, "recommended_name") or "Produto recomendado")
    if not image_url:
        return "<div class=\"image-placeholder\">Sem imagem</div>"
    return f"<img src=\"{image_url}\" alt=\"{name}\" loading=\"lazy\">"


def render_product_meta(prefix: str, row: dict[str, str]) -> str:
    price = format_price(
        row_value(row, f"{prefix}_price"),
        row_value(row, f"{prefix}_availability_text"),
    )
    return (
        "<dl class=\"meta-grid\">"
        f"<div><dt>Tipo</dt><dd>{html_text(row_value(row, f'{prefix}_product_type') or 'Nao informado')}</dd></div>"
        f"<div><dt>Categoria</dt><dd>{html_text(row_value(row, f'{prefix}_category') or 'Nao informada')}</dd></div>"
        f"<div><dt>Marca</dt><dd>{html_text(row_value(row, f'{prefix}_brand') or 'Nao informada')}</dd></div>"
        f"<div><dt>Preco</dt><dd>{price}</dd></div>"
        "</dl>"
    )


def render_review_card(row: dict[str, str], index: int) -> str:
    score = row_value(row, "score") or "sem score"
    reviewer_rating = row_value(row, "reviewer_rating")
    reviewer_comment = row_value(row, "reviewer_comment")

    return f"""
      <article class="review-card">
        <div class="card-index">#{index:03d}</div>
        <section class="product-column source">
          <p class="column-label">Produto de origem</p>
          <h2>{html_text(row_value(row, "source_name") or "Produto sem nome")}</h2>
          {render_product_meta("source", row)}
          <div class="link-row">
            {link_html(row_value(row, "source_url"), "Abrir produto de origem")}
          </div>
        </section>
        <section class="product-column recommended">
          <p class="column-label">Produto recomendado</p>
          <div class="recommended-layout">
            <div class="product-image">
              {image_html(row)}
            </div>
            <div>
              <h2>{html_text(row_value(row, "recommended_name") or "Produto sem nome")}</h2>
              {render_product_meta("recommended", row)}
            </div>
          </div>
          <div class="link-row">
            {link_html(row_value(row, "recommended_url"), "Abrir recomendado")}
          </div>
        </section>
        <section class="score-column">
          <div class="score-box">
            <span>Score</span>
            <strong>{html_text(score)}</strong>
          </div>
          <div class="reason-box">
            <span>Reason</span>
            <p>{html_text(row_value(row, "reason") or "Sem explicacao registrada.")}</p>
          </div>
          <div class="review-fields" aria-label="Campos visuais de revisao">
            <div>
              <span>reviewer_rating</span>
              <p>{html_text(reviewer_rating)}</p>
            </div>
            <div>
              <span>reviewer_comment</span>
              <p>{html_text(reviewer_comment)}</p>
            </div>
          </div>
        </section>
      </article>
    """


def render_cards(rows: list[dict[str, str]]) -> str:
    if not rows:
        return """
          <section class="empty-state">
            <h2>Nenhuma recomendacao encontrada</h2>
            <p>Verifique o CSV de entrada ou ajuste os filtros de score e tipo de produto.</p>
          </section>
        """

    return "\n".join(
        render_review_card(row, index)
        for index, row in enumerate(rows, start=1)
    )


def build_review_pack_html(
    rows: list[dict[str, str]],
    input_path: Path,
    min_score: float | None = None,
    product_type: str | None = None,
) -> str:
    source_product_count, product_type_count = summarize_rows(rows)
    filters = []
    if product_type:
        filters.append(f"Tipo de produto: {html_text(product_type)}")
    if min_score is not None:
        filters.append(f"Score minimo: {min_score:g}")
    filter_text = " | ".join(filters) if filters else "Sem filtros adicionais"

    return f"""<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Kouzina Reco — Revisão Qualitativa</title>
    <style>
      :root {{
        --espresso: #1b0f0a;
        --espresso-soft: #2c1710;
        --cream: #fff4dd;
        --cream-strong: #f2d7a5;
        --porcelain: #fffaf0;
        --copper: #b8632f;
        --olive: #53612b;
        --olive-deep: #2d3718;
        --wine: #4b0f23;
        --wine-bright: #7a1e39;
        --amber: #f0b13f;
        --line: rgba(184, 99, 47, 0.34);
      }}

      * {{
        box-sizing: border-box;
      }}

      body {{
        margin: 0;
        background:
          radial-gradient(circle at 12% 4%, rgba(240, 177, 63, 0.24), transparent 30rem),
          radial-gradient(circle at 90% 10%, rgba(75, 15, 35, 0.22), transparent 32rem),
          linear-gradient(135deg, var(--cream), #efd2a1);
        color: var(--espresso);
        font-family: "Segoe UI", Arial, sans-serif;
        line-height: 1.55;
      }}

      body::before {{
        position: fixed;
        inset: 0;
        z-index: -1;
        content: "";
        background-image:
          linear-gradient(90deg, rgba(75, 15, 35, 0.045) 1px, transparent 1px),
          linear-gradient(0deg, rgba(83, 97, 43, 0.05) 1px, transparent 1px);
        background-size: 44px 44px;
      }}

      main {{
        width: min(1180px, calc(100% - 32px));
        margin: 0 auto;
        padding: 40px 0 64px;
      }}

      .hero {{
        display: grid;
        gap: 22px;
        border: 1px solid var(--line);
        border-radius: 24px;
        padding: clamp(24px, 5vw, 54px);
        background: rgba(255, 250, 240, 0.88);
        box-shadow: 0 24px 70px rgba(36, 15, 8, 0.18);
      }}

      .eyebrow,
      .column-label,
      .scale-label {{
        margin: 0;
        color: var(--wine-bright);
        font-size: 0.78rem;
        font-weight: 900;
        letter-spacing: 0.14em;
        text-transform: uppercase;
      }}

      h1,
      h2,
      h3 {{
        margin: 0;
        font-family: Georgia, "Times New Roman", serif;
        line-height: 1.08;
      }}

      h1 {{
        max-width: 860px;
        font-size: clamp(2.7rem, 7vw, 6.3rem);
      }}

      h2 {{
        font-size: clamp(1.28rem, 2.2vw, 2rem);
      }}

      .lead {{
        max-width: 860px;
        margin: 0;
        color: var(--espresso-soft);
        font-size: 1.12rem;
      }}

      .summary-grid,
      .instruction-grid {{
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 14px;
        margin-top: 20px;
      }}

      .summary-card,
      .instruction-card,
      .questions,
      .review-card,
      .empty-state {{
        border: 1px solid var(--line);
        border-radius: 18px;
        background: rgba(255, 250, 240, 0.9);
        box-shadow: 0 16px 42px rgba(58, 22, 10, 0.14);
      }}

      .summary-card,
      .instruction-card {{
        padding: 18px;
      }}

      .summary-card span {{
        color: var(--wine);
        font-weight: 900;
      }}

      .summary-card strong {{
        display: block;
        margin-top: 8px;
        font-family: Georgia, "Times New Roman", serif;
        font-size: 2.3rem;
      }}

      .pills {{
        display: flex;
        flex-wrap: wrap;
        gap: 9px;
        margin-top: 18px;
      }}

      .pill,
      .rating-pill {{
        display: inline-flex;
        gap: 7px;
        align-items: center;
        border-radius: 999px;
        padding: 8px 12px;
        background: var(--espresso);
        color: var(--cream);
        font-weight: 800;
      }}

      .rating-scale {{
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 14px;
      }}

      .rating-pill {{
        background: var(--wine);
      }}

      .questions {{
        margin: 22px 0;
        padding: 22px;
        background: rgba(45, 55, 24, 0.94);
        color: var(--porcelain);
      }}

      .questions h2 {{
        color: var(--porcelain);
      }}

      .questions ul {{
        display: grid;
        gap: 8px;
        margin: 16px 0 0;
        padding-left: 20px;
      }}

      .cards {{
        display: grid;
        gap: 18px;
      }}

      .review-card {{
        position: relative;
        display: grid;
        grid-template-columns: 0.36fr 1fr 1.1fr 0.72fr;
        gap: 16px;
        padding: 18px;
      }}

      .card-index {{
        display: grid;
        place-items: center;
        border-radius: 18px;
        background: var(--espresso);
        color: var(--amber);
        font-family: Georgia, "Times New Roman", serif;
        font-size: 1.35rem;
        font-weight: 900;
      }}

      .product-column,
      .score-column {{
        min-width: 0;
      }}

      .recommended-layout {{
        display: grid;
        grid-template-columns: 132px minmax(0, 1fr);
        gap: 14px;
        align-items: start;
      }}

      .product-image {{
        overflow: hidden;
        aspect-ratio: 1 / 1;
        border: 1px solid rgba(184, 99, 47, 0.32);
        border-radius: 18px;
        background: var(--cream-strong);
      }}

      .product-image img {{
        display: block;
        width: 100%;
        height: 100%;
        object-fit: cover;
      }}

      .image-placeholder {{
        display: grid;
        width: 100%;
        height: 100%;
        place-items: center;
        padding: 12px;
        color: var(--espresso-soft);
        font-weight: 900;
        text-align: center;
      }}

      .meta-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin: 14px 0 0;
      }}

      .meta-grid div {{
        border-radius: 14px;
        padding: 9px 10px;
        background: rgba(242, 215, 165, 0.62);
      }}

      dt {{
        color: var(--wine);
        font-size: 0.72rem;
        font-weight: 900;
        letter-spacing: 0.08em;
        text-transform: uppercase;
      }}

      dd {{
        margin: 3px 0 0;
        overflow-wrap: anywhere;
        font-weight: 800;
      }}

      .link-row {{
        display: flex;
        flex-wrap: wrap;
        gap: 9px;
        margin-top: 14px;
      }}

      .link-button,
      .link-disabled {{
        display: inline-flex;
        border-radius: 999px;
        padding: 9px 12px;
        font-size: 0.9rem;
        font-weight: 900;
        text-decoration: none;
      }}

      .link-button {{
        background: var(--wine);
        color: var(--porcelain);
      }}

      .link-disabled {{
        background: var(--cream-strong);
        color: var(--espresso-soft);
      }}

      .score-box,
      .reason-box,
      .review-fields div {{
        border-radius: 18px;
        padding: 12px;
        background: var(--espresso);
        color: var(--cream);
      }}

      .score-box strong {{
        display: block;
        color: var(--amber);
        font-size: 2rem;
      }}

      .score-box span,
      .reason-box span,
      .review-fields span {{
        color: var(--amber);
        font-size: 0.78rem;
        font-weight: 900;
        letter-spacing: 0.08em;
        text-transform: uppercase;
      }}

      .reason-box {{
        margin-top: 10px;
      }}

      .reason-box p,
      .review-fields p {{
        margin: 8px 0 0;
      }}

      .review-fields {{
        display: grid;
        gap: 10px;
        margin-top: 10px;
      }}

      .review-fields p {{
        min-height: 34px;
        border-bottom: 1px solid rgba(255, 244, 221, 0.35);
      }}

      .muted {{
        color: var(--espresso-soft);
      }}

      .empty-state {{
        padding: 28px;
      }}

      footer {{
        width: min(1180px, calc(100% - 32px));
        margin: 0 auto;
        padding: 0 0 36px;
        color: var(--espresso-soft);
      }}

      @media (max-width: 980px) {{
        .summary-grid,
        .instruction-grid {{
          grid-template-columns: repeat(2, minmax(0, 1fr));
        }}

        .review-card {{
          grid-template-columns: 1fr;
        }}

        .card-index {{
          min-height: 54px;
        }}
      }}

      @media (max-width: 640px) {{
        main {{
          width: min(100% - 20px, 1180px);
          padding-top: 18px;
        }}

        .summary-grid,
        .instruction-grid,
        .meta-grid,
        .recommended-layout {{
          grid-template-columns: 1fr;
        }}
      }}
    </style>
  </head>
  <body>
    <main>
      <section class="hero">
        <p class="eyebrow">Fase 4.7 | Review Pack local</p>
        <h1>Kouzina Reco — Revisão Qualitativa</h1>
        <p class="lead">
          Pacote visual gerado a partir de {html_text(display_path(input_path))}. Use este HTML para discutir recomendacoes com a Kouzina.
          O preenchimento oficial continua no CSV ou em uma planilha copiada.
        </p>
        <div class="summary-grid" aria-label="Resumo do pacote">
          <div class="summary-card"><span>Linhas exibidas</span><strong>{len(rows)}</strong></div>
          <div class="summary-card"><span>Produtos de origem</span><strong>{source_product_count}</strong></div>
          <div class="summary-card"><span>Tipos de produto</span><strong>{product_type_count}</strong></div>
          <div class="summary-card"><span>Filtros</span><p>{filter_text}</p></div>
        </div>
        <div class="pills" aria-label="Resumo por tipo de produto">
          {product_type_summary(rows)}
        </div>
      </section>

      <section class="instruction-grid" aria-label="Instrucoes para revisao">
        <article class="instruction-card">
          <h2>Como revisar</h2>
          <p>Abra cada card, compare origem e recomendado, avalie o motivo textual e registre rating/comentario na planilha.</p>
        </article>
        <article class="instruction-card">
          <h2>HTML visual</h2>
          <p>Este arquivo nao grava respostas, nao altera banco e nao recalcula ranking.</p>
        </article>
        <article class="instruction-card">
          <p class="scale-label">Escala de rating</p>
          <div class="rating-scale">
            <span class="rating-pill">1 = ruim</span>
            <span class="rating-pill">2 = fraca</span>
            <span class="rating-pill">3 = aceitável</span>
            <span class="rating-pill">4 = boa</span>
            <span class="rating-pill">5 = excelente</span>
          </div>
        </article>
        <article class="instruction-card">
          <h2>Privacidade</h2>
          <p>O pacote usa somente catalogo, score e reason. Nao inclui pedidos, checkout, pagamento ou dados pessoais.</p>
        </article>
      </section>

      <section class="questions" aria-label="Perguntas sugeridas">
        <h2>Perguntas para a Kouzina</h2>
        <ul>
          <li>Esse produto realmente complementa o produto atual?</li>
          <li>A recomendação faz sentido comercial?</li>
          <li>Há algum produto que deveria aparecer antes?</li>
          <li>Produto sob consulta deve aparecer nesse contexto?</li>
          <li>A explicação está clara?</li>
        </ul>
      </section>

      <section class="cards" aria-label="Cards de recomendacao para revisao">
        {render_cards(rows)}
      </section>
    </main>
    <footer>
      <p>Gerado localmente. Etapa anterior a CTR, fuzzy, ontologia e deploy.</p>
    </footer>
  </body>
</html>
"""


def generate_review_pack(
    input_path: Path = DEFAULT_INPUT,
    output_path: Path = DEFAULT_OUTPUT,
    limit: int = 120,
    min_score: float | None = None,
    product_type: str | None = None,
) -> ReviewPackStats:
    input_path = resolve_project_path(input_path)
    output_path = resolve_project_path(output_path)
    rows = filter_review_rows(
        read_review_rows(input_path),
        limit=limit,
        min_score=min_score,
        product_type=product_type,
    )
    html = build_review_pack_html(
        rows,
        input_path=input_path,
        min_score=min_score,
        product_type=product_type,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")

    source_product_count, product_type_count = summarize_rows(rows)
    return ReviewPackStats(
        row_count=len(rows),
        source_product_count=source_product_count,
        product_type_count=product_type_count,
        output_path=output_path,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a static qualitative recommendation review HTML pack.",
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help="Input CSV path. Defaults to reports/recommendation_review.csv.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output HTML path. Defaults to reports/recommendation_review.html.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=120,
        help="Maximum number of recommendation rows to include. Defaults to 120.",
    )
    parser.add_argument(
        "--min-score",
        type=float,
        default=None,
        help="Optional minimum score filter.",
    )
    parser.add_argument(
        "--product-type",
        type=str,
        default=None,
        help="Optional source product_type filter, for example Churrasqueira.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    stats = generate_review_pack(
        input_path=args.input,
        output_path=args.output,
        limit=args.limit,
        min_score=args.min_score,
        product_type=args.product_type,
    )
    print(
        "Generated review pack with "
        f"{stats.row_count} rows, {stats.source_product_count} source products "
        f"and {stats.product_type_count} product types at {stats.output_path}"
    )


if __name__ == "__main__":
    main()
