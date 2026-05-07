# Migrações De Banco

## Objetivo

Introduzir Alembic como trilha controlada de evolucao do schema sem remover o
fallback local de `create_all` usado em testes e desenvolvimento simples.

## Arquivos

```text
backend/alembic.ini
backend/alembic/env.py
backend/alembic/versions/0001_initial_schema.py
backend/alembic/versions/0002_add_event_analytics_columns.py
```

## Comando Recomendado

```powershell
cd backend
alembic upgrade head
```

O Alembic usa `DATABASE_URL`/`.env` via `app.core.config.get_settings()`.

## Fallback Local

`init_db()` ainda chama `Base.metadata.create_all()` para ambiente local/teste.
Esse fallback cria tabelas ausentes, mas nao substitui migrations em ambientes
controlados e nao deve ser usado como mecanismo principal de alteracao de schema.

## Migrations Criadas

### `0001_initial_schema`

Cria o schema base:

- `stores`
- `products`
- `manual_product_relations`
- `recommendation_events`

### `0002_add_event_analytics_columns`

Adiciona campos opcionais em `recommendation_events`:

- `event_name`
- `source_product_type`
- `recommended_product_type`
- `rank`
- `score`
- `relation_class`
- `relation_type`
- `relation_policy_action`
- `validation_status`
- `is_quote_only`
- `quote_reason`
- `environment`
- `brand`
- `price_band`
- `funnel_stage`

Tambem cria indices para consultas futuras por tempo, sessao, produto e relacao.

## Politica De Dados

- `metadata` JSON continua existindo para campos extras sanitizados.
- Nenhum dado pessoal deve ser coletado.
- A estrutura prepara analise futura, mas nao executa analise de funil nesta fase.
