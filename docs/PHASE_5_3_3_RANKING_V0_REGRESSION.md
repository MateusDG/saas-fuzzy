# Fase 5.3.3 - Regressao Do Ranking v0 Pos-Refatoracao

## 1. Objetivo

Validar que a reorganizacao do backend da Fase 5.3.1/5.3.2 nao alterou o
comportamento operacional do ranking v0:

- sem mudanca de pesos e guardrails;
- sem quebra de contrato do `GET /recommendations`;
- sem perda de fallback;
- sem perda de compatibilidade dos wrappers.

Esta fase nao implementa fuzzy, ontologia ou recomendador hibrido.

## 2. Comandos Executados

```powershell
git status --short
cd backend
python -m app.freeze_v0_baseline --limit-products 30 --top-k 4
python -m app.freeze_v0_baseline --limit-products 30 --top-k 4 --output reports/baselines/v0_baseline_post_refactor.json
python -m app.review.review_recommendations --limit-products 30 --top-k 4 --output reports/recommendation_review_regression.csv
python -m pytest
python -m app.review_recommendations --help
python -m app.export_review_pack --help
python -m app.run_offline_evaluation --help
```

## 3. Artefatos Gerados

- `reports/baselines/v0_baseline_snapshot.json`
- `reports/baselines/v0_baseline_post_refactor.json`
- `reports/recommendation_review_regression.csv` (ignorado por `.gitignore`)

## 4. Evidencias Da Regressao

### 4.1 Snapshot Controlado

- `source_products`: 30
- `recommendation_rows`: 120
- `fingerprint_sha256` (conteudo de linhas):
  `e1e8d8cf2f28f3499834a831e84cb75dacfff76746538ad49b304296e160ed42`
- Fingerprint igual entre snapshot padrao e snapshot `post_refactor`: `True`
- `self_recommendation_rows`: `0`

Observacao: o hash do arquivo JSON completo difere entre execucoes porque o
campo `generated_at` muda, mas o fingerprint canonico das linhas permaneceu
igual.

### 4.2 Guardrails E Politica De Relacao

No snapshot/regression review:

- `relation_class=universal`: 34
- `relation_class=contextual`: 36
- `relation_class=weak`: 46
- `blocked_rows`: 0 (itens bloqueados nao entram no ranking final)
- `policy_demoted_rows` no CSV de review: 50

Conclusao: os guardrails continuam aplicados na geracao final.

### 4.3 Reasons E Qualidade Textual

No `recommendation_review_regression.csv`:

- `review_rows`: 120
- `rows_without_reason`: 0
- `reason_quality_strong`: 102
- `reason_quality_medium`: 18
- `reason_quality_generic`: 0

Conclusao: as reasons continuam presentes e coerentes com a politica editorial.

### 4.4 Contrato Da API E Fallback

Com `python -m pytest`:

- `56 passed`.

A suite cobre:

- fallback quando catalogo esta vazio;
- fallback quando `product_id` nao existe;
- ausencia de auto-recomendacao;
- ordenacao por score;
- persistencia de eventos;
- contrato de resposta de recomendacoes.

Nao houve mudanca no endpoint publico:

- `GET /recommendations`
- `POST /events`
- `GET /health`

### 4.5 Wrappers Legados

Wrappers antigos continuam funcionais (ajuda de CLI carregada com sucesso):

- `python -m app.review_recommendations`
- `python -m app.export_review_pack`
- `python -m app.run_offline_evaluation`

## 5. Checagem Dos Pesos v0

A estrutura de score permanece no modulo `backend/app/recommender/scoring.py`
com pesos e penalidades ativos na mesma logica operacional da Fase 5.3.2,
incluindo:

- complementaridade funcional como eixo principal;
- penalidade para relacao fraca e sinais apenas auxiliares;
- bloqueio por politica `forbidden/block`;
- tratamento cauteloso para `Sob consulta`.

Nao foi aplicada nenhuma alteracao de peso nesta fase.

## 6. Riscos E Limitacoes

- Esta regressao valida estabilidade operacional local, nao resultado comercial
  em producao.
- O comando com `--output ../reports/...` escapa para um caminho acima do
  repositorio devido resolucao do script pelo `PROJECT_ROOT`; para manter
  artefato dentro do repo, usar `--output reports/...`.
- Sem fuzzy e sem ontologia nesta etapa, por escopo.

## 7. Conclusao

A regressao da Fase 5.3.3 foi aprovada:

- ranking v0 estavel;
- guardrails ativos;
- fallback ativo;
- contrato da API preservado;
- wrappers antigos preservados;
- suite automatizada verde (`56 passed`).
