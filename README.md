# Kouzina Reco MVP

MVP comercial minimo de recomendacao para o site Kouzina Club.

Esta fase implementa somente a Fase 1 tecnica local:

- API FastAPI minima.
- `GET /health`.
- `POST /events` mockado, com validacao de payload.
- `GET /recommendations` mockado.
- Widget JavaScript puro.
- Demo local do widget.
- PostgreSQL preparado via Docker Compose, ainda sem conexao com a API.
- CSV com 3 produtos mockados.

Fora de escopo nesta fase: fuzzy, ontologia, integracao Tray, painel, login,
deploy, ranking real e persistencia no banco.

## Estrutura

```text
backend/
  app/
    __init__.py
    main.py
    recommender.py
    schemas.py
    settings.py
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

O banco fica preparado para fases futuras. A API da Fase 1 ainda nao conecta
nele.

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

Recomendacoes mockadas:

```bash
curl "http://localhost:8000/recommendations?product_id=12345&widget_id=product-page"
```

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

Os eventos sao validados e confirmados, mas ainda nao sao salvos em banco.

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

A Fase 2 deve conectar PostgreSQL, criar tabelas simples, salvar eventos e
preparar o catalogo inicial. Ranking real, fuzzy e ontologia continuam fora
ate as fases posteriores.
