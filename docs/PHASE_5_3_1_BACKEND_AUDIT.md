# Fase 5.3.1 - Auditoria Técnica Do Backend

## Objetivo

Revisar o backend apos o piloto offline com Amazon Reviews 2023 / `Appliances`,
organizar a estrutura interna e preparar o banco para evolucao com migrations.

Esta fase nao implementa fuzzy, ontologia, recomendador hibrido, deploy ou nova
analise de dados.

## Estrutura Atual Apos Refatoracao

O backend foi separado em:

- `core`: configuracao e banco;
- `api/routes`: endpoints FastAPI;
- `db`: modelos SQLAlchemy;
- `schemas`: contratos Pydantic;
- `services`: regras de aplicacao dos endpoints;
- `recommender`: ranking v0 por regras, politica e explicacoes;
- `catalog`: importacao/normalizacao de catalogo;
- `review`: CSV/HTML de revisao qualitativa;
- `evaluation`: scripts academicos offline.

## Problemas Encontrados

- `main.py` concentrava endpoints, persistencia de eventos e fallback de recomendacao.
- `schemas.py` misturava contratos de health, eventos e recomendacoes.
- `recommender.py` concentrava regras, scoring, helpers e conversao de resposta.
- scripts de review e avaliacao ficavam no mesmo nivel dos modulos comerciais.
- o schema de eventos aceitava campos analiticos no payload/metadata, mas a tabela
  ainda nao possuia colunas dedicadas para consultas futuras.
- nao havia Alembic configurado para evolucao segura do banco.

## Decisoes De Refatoracao

- `main.py` ficou responsavel por criar app, CORS, lifespan e registrar routers.
- endpoints foram movidos para `api/routes`.
- persistencia/sanitizacao de eventos foi movida para `services/event_service.py`.
- busca de produto, candidatos e fallback mockado foram movidos para
  `services/recommendation_service.py`.
- schemas foram separados por dominio.
- recomendador v0 foi separado em regras, helpers, scoring, explicacoes e service.
- review pack e avaliacao academica foram isolados em pacotes proprios.
- wrappers antigos foram mantidos para preservar comandos e imports.
- Alembic foi adicionado com migration inicial e migration de colunas analiticas.

## O Que Foi Mantido Intacto

- endpoints publicos;
- formato de resposta de `/recommendations`;
- nomes de eventos aceitos;
- pesos e guardrails do ranking v0;
- widget;
- scripts antigos via wrappers;
- separacao entre benchmark publico e catalogo Kouzina.

## O Que Foi Movido

- `database.py` -> `core/database.py`
- `settings.py` -> `core/config.py`
- `models.py` -> `db/models.py`
- `seed.py` -> `catalog/seed.py`
- `review_recommendations.py` -> `review/review_recommendations.py`
- `export_review_pack.py` -> `review/export_review_pack.py`
- `evaluation_*`, preprocessamento e avaliacao -> `evaluation/`
- `relation_policy.py` -> `recommender/relation_policy.py`
- `recommender.py` -> pacote `recommender/`

## Banco De Dados

Foram adicionados:

- `backend/alembic.ini`
- `backend/alembic/env.py`
- `0001_initial_schema.py`
- `0002_add_event_analytics_columns.py`

`recommendation_events` agora possui colunas opcionais para futura analise de
funil, mantendo `metadata` JSON sanitizado.

## Riscos

- bancos locais existentes precisam rodar `alembic upgrade head` para receber
  as novas colunas;
- `create_all` nao altera tabelas ja existentes;
- os wrappers devem ser removidos somente em fase futura, depois de atualizar
  documentacao e automacoes.

## Testes Executados

- `python -m compileall app` - OK
- `python -m pytest` - 56 passed
- `python -m alembic history` - migrations reconhecidas

## Proximos Passos

1. Rodar `alembic upgrade head` em ambiente local controlado.
2. Confirmar seed e API com PostgreSQL local.
3. Manter Fase 5.4 separada para `Home_and_Kitchen`.
4. Antes da Fase 6, revisar se o snapshot v0 e os baselines offline seguem
   reproduziveis.
