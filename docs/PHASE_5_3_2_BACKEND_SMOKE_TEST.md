# Fase 5.3.2 - Backend Smoke Test Com PostgreSQL Real

## 1. Objetivo Da Validacao

Registrar formalmente a validacao pos-refatoracao do backend apos a Fase 5.3.1,
com foco em:

- PostgreSQL real;
- migrations Alembic;
- seed;
- API;
- persistencia de eventos;
- recomendacoes v0 e fallback;
- wrappers antigos;
- testes automatizados.

Esta fase valida operacao e compatibilidade. Nao implementa novas features.

## 2. Contexto Da Refatoracao (Fase 5.3.1)

O backend foi reorganizado em pacotes:

- `core`
- `api/routes`
- `db`
- `schemas`
- `services`
- `recommender`
- `catalog`
- `review`
- `evaluation`

O contrato publico da API foi mantido.

## 3. Estado Do Banco Antes Da Migration

Estado inicial validado no ambiente local:

- PostgreSQL Docker ativo;
- banco local antigo sem tabela `alembic_version`;
- schema antigo compativel com `0001_initial_schema`.

Contagem validada no estado final do ambiente:

- `stores=1`
- `products=311`
- `events=10`

## 4. Justificativa Para `alembic stamp 0001_initial_schema`

Como o banco ja existia e o schema era compativel com a migration inicial, o
comando:

```powershell
python -m alembic stamp 0001_initial_schema
```

foi usado para marcar a baseline sem recriar objetos nem tentar reexecutar
DDL da `0001` em tabelas existentes.

Justificativa tecnica:

- evita conflito em banco legado ja provisionado;
- alinha historico Alembic com schema real;
- prepara caminho seguro para aplicar apenas deltas posteriores.

## 5. Resultado De `alembic upgrade head`

Comando executado:

```powershell
python -m alembic upgrade head
```

Resultado validado:

- upgrade concluido com sucesso;
- revisao final: `0002_add_event_analytics_columns`;
- estado Alembic final: `head`.

## 6. Colunas Analiticas Adicionadas Em `recommendation_events`

Conforme migration `0002_add_event_analytics_columns`, foram adicionadas
colunas opcionais:

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

Tambem foram criados indices auxiliares para consultas por tempo, tipo de
evento, sessao, produto e relacao.

## 7. Resultado Do Seed

Validacao registrada:

- comando legado `python -m app.seed` funcionando;
- carga de dados operacional apos migrations;
- estado consolidado no ambiente: `stores=1`, `products=311`.

## 8. Resultado Dos Endpoints (API Smoke)

Resultados registrados:

- `GET /health` -> `ok`;
- `POST /events` -> `received=true`;
- `GET /recommendations?product_id=mock-001` -> `4` recomendacoes;
- `GET /recommendations?product_id=missing-smoke` -> fallback com
  `mock-001`.

Comportamento esperado confirmado:

- API funcional apos refatoracao;
- ranking v0 funcional;
- fallback funcional;
- evento persistido com metadata sanitizada.

## 9. Resultado Dos Wrappers Antigos

Wrappers de compatibilidade validados com sucesso:

- `python -m app.seed`
- `python -m app.review_recommendations`
- `python -m app.export_review_pack`
- `python -m app.preprocess_amazon_reviews_2023 --help`
- `python -m app.run_offline_evaluation --top-k 5`
- `python -m app.run_offline_evaluation --top-k 10`
- `python -m app.freeze_v0_baseline`

## 10. Resultado Dos Testes

Suite validada:

- `56 passed`.

## 11. Artefatos Locais/ Ignorados Gerados

Artefatos gerados durante a validacao (nao versionados):

- `reports/recommendation_review_smoke.csv`
- `reports/recommendation_review_smoke.html`
- `reports/evaluation/metrics_summary.json`
- `reports/evaluation/per_user_metrics.csv`
- `C:\tmp\kouzina_v0_smoke.json`

Observacao:

- `C:\tmp\kouzina_v0_smoke.json` esta fora do repositorio.

## 12. Limitacoes

- Validacao de smoke test cobre operacao local e compatibilidade, nao teste de
  carga.
- Nao houve mudanca de regra no ranking v0.
- Nao houve mudanca na API publica.
- Nao inclui fuzzy, ontologia, recomendador hibrido nem Fase 5.4.
- Nao utiliza dados reais de cliente.

## 13. Conclusao

A Fase 5.3.2 validou que a refatoracao da Fase 5.3.1 permaneceu estavel com
PostgreSQL real, migrations Alembic, seed, API, eventos, recomendacoes,
fallback, wrappers antigos e testes automatizados.

O backend ficou pronto para seguir com evolucao controlada sem quebra de
compatibilidade operacional.

## 14. Proximo Passo Recomendado

Executar a proxima etapa planejada de forma controlada, mantendo:

- baseline v0 congelado;
- trilha de migrations como fonte de verdade para schema;
- wrappers legados ativos ate transicao completa de comandos;
- validacoes de smoke equivalentes em ambientes locais antes de cada fase nova.
