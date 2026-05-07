# Estrutura Do Backend

## Objetivo

Registrar a organizacao do backend apos a Fase 5.3.1. A refatoracao separa API,
servicos, banco, schemas, recomendador, catalogo, review pack e avaliacao
academica sem alterar o contrato publico da API.

## Estrutura Canonica

```text
backend/app/
  main.py
  core/
    config.py
    database.py
  api/routes/
    health.py
    events.py
    recommendations.py
  db/
    models.py
  schemas/
    health.py
    events.py
    recommendations.py
  services/
    event_service.py
    recommendation_service.py
  recommender/
    rules.py
    utils.py
    scoring.py
    explanations.py
    relation_policy.py
    service.py
  catalog/
    seed.py
  review/
    review_recommendations.py
    export_review_pack.py
  evaluation/
    evaluation_baselines.py
    evaluation_metrics.py
    preprocess_amazon_reviews_2023.py
    run_offline_evaluation.py
```

## Wrappers De Compatibilidade

Estes comandos/imports antigos continuam disponiveis:

```powershell
python -m app.seed
python -m app.review_recommendations
python -m app.export_review_pack
python -m app.preprocess_amazon_reviews_2023
python -m app.run_offline_evaluation
```

Imports antigos tambem continuam funcionando:

- `app.database`
- `app.models`
- `app.settings`
- `app.recommender`
- `app.relation_policy`
- `app.evaluation_metrics`
- `app.evaluation_baselines`

## Comandos Recomendados

Rodar API:

```powershell
cd backend
uvicorn app.main:app --reload
```

Rodar seed:

```powershell
cd backend
python -m app.catalog.seed
```

Gerar review CSV:

```powershell
cd backend
python -m app.review.review_recommendations
```

Gerar review HTML:

```powershell
cd backend
python -m app.review.export_review_pack
```

Rodar avaliacao offline:

```powershell
cd backend
python -m app.evaluation.run_offline_evaluation --top-k 10
```

## Contrato Preservado

Endpoints publicos mantidos:

- `GET /health`
- `POST /events`
- `GET /recommendations`

O widget nao precisa mudar.

## Limites

- ranking v0 nao teve pesos alterados;
- fuzzy nao foi implementado;
- ontologia nao foi implementada;
- scripts academicos continuam separados da logica comercial.
