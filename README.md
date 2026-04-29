# Kouzina Reco MVP

MVP comercial minimo de recomendacao para o site Kouzina Club.

Este repositório implementa a base local das Fases 1 e 2:

- API FastAPI minima.
- `GET /health`.
- `POST /events` com validacao de payload e persistencia em PostgreSQL.
- `GET /recommendations` usando catalogo importado, com fallback mockado.
- Widget JavaScript puro.
- Demo local do widget.
- PostgreSQL via Docker Compose.
- CSV com 3 produtos mockados.

Fora de escopo: fuzzy, ontologia, integracao Tray, painel, login, deploy,
ranking sofisticado, crawler, scraping e multi-loja completo.

## Estrutura

```text
backend/
  app/
    __init__.py
    main.py
    database.py
    models.py
    recommender.py
    schemas.py
    seed.py
    settings.py
  tests/
  Dockerfile
  requirements.txt
widget/
  demo.html
  kouzina-reco.js
data/
  products_seed.csv
docker-compose.yml
.env.example
```

## Configuracao local

Crie um `.env` local a partir do exemplo:

```bash
copy .env.example .env
```

No PowerShell, o comando equivalente tambem funciona:

```powershell
Copy-Item .env.example .env
```

## Rodar PostgreSQL

O banco e usado pela Fase 2 para produtos e eventos.

```bash
docker compose up -d
```

## Rodar API local

No Windows PowerShell:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Em macOS/Linux:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

A API ficara em:

```text
http://localhost:8000
```

## Criar tabelas e importar produtos

A API tenta criar as tabelas no startup. Para importar o catalogo inicial:

```powershell
cd backend
python -m app.seed
```

O seed cria a loja padrao Kouzina e importa `data/products_seed.csv`. A
importacao e idempotente por `external_id`, entao pode ser rodada mais de uma
vez sem duplicar produtos.

## Testar API

Healthcheck:

```bash
curl http://localhost:8000/health
```

Resposta esperada:

```json
{
  "status": "ok",
  "service": "kouzina-reco-api",
  "version": "0.1.0"
}
```

Documentacao interativa:

```text
http://localhost:8000/docs
```

Recomendacoes:

```bash
curl "http://localhost:8000/recommendations?product_id=12345&widget_id=product-page"
```

Quando houver produtos importados no banco, a resposta usa o catalogo. Se o
banco estiver vazio ou indisponivel, a API usa fallback mockado para manter o
widget funcionando.

Evento mockado no PowerShell:

```powershell
Invoke-RestMethod -Method Post -Uri http://localhost:8000/events -ContentType "application/json" -Body '{"event_type":"recommendation_click","anonymous_id":"anon_123","session_id":"sess_456","page_url":"http://localhost:5500/demo.html","product_id":"12345","widget_id":"product-page","recommended_product_id":"mock-001","metadata":{}}'
```

Evento mockado com curl:

```bash
curl -X POST http://localhost:8000/events \
  -H "Content-Type: application/json" \
  -d '{"event_type":"recommendation_click","anonymous_id":"anon_123","session_id":"sess_456","page_url":"http://localhost:5500/demo.html","product_id":"12345","widget_id":"product-page","recommended_product_id":"mock-001","metadata":{}}'
```

## Testar widget local

Com a API rodando em `http://localhost:8000`, abra outro terminal:

```bash
cd widget
python -m http.server 5500
```

Depois acesse:

```text
http://localhost:5500/demo.html
```

O widget deve:

- renderizar recomendacoes mockadas;
- enviar `page_view`;
- enviar `recommendation_impression`;
- enviar `recommendation_click` ao clicar em uma recomendacao;
- usar `localStorage` para `anonymous_id`;
- usar `sessionStorage` para `session_id`.

## Eventos permitidos

Nesta fase, a API aceita somente:

```text
page_view
product_view
recommendation_impression
recommendation_click
```

Os eventos sao validados, confirmados e salvos em `recommendation_events`
quando o banco esta disponivel.

## Privacidade

O MVP coleta somente dados anonimos e tecnicos:

- `anonymous_id`
- `session_id`
- `event_type`
- `page_url`
- `product_id`
- `widget_id`
- `recommended_product_id`
- `metadata` nao sensivel

Nao coletar nome, CPF, e-mail, telefone, endereco, dados de pagamento ou
conteudo de formularios.

## Proxima fase

A proxima fase deve evoluir o catalogo e o recomendador v0 por regras. Fuzzy,
ontologia, Tray, painel, login e deploy continuam fora ate fases posteriores.

## Rodar testes

```powershell
cd backend
pytest
```
