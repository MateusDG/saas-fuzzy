# Resultados Fase 5 Baseline (Template)

## Objetivo

Registrar os resultados da primeira execucao offline reproduzivel da Fase 5.1,
com dataset publico e baselines simples, sem fuzzy e sem ontologia.

## Status Atual

Template inicial. Preencher apos execucao real do preprocessamento e da
avaliacao offline com CSVs locais em `data/public/processed/`.

Se nao houver dados locais disponiveis, manter este arquivo como template e nao
inventar metricas.

## Dataset E Recorte

- Dataset: Amazon Reviews 2023
- Piloto atual: `Appliances`
- Recorte de referencia para expansao: `Home_and_Kitchen`, `Appliances`
- Regra premium (proxy): `price >= P75` por categoria
- Observacao: premium e proxy de produto, nao perfil real de consumidor

## Filtros Aplicados

- `min_rating`:
- `min_item_interactions`:
- `min_user_interactions`:
- `premium_percentile`:
- `require_verified_purchase`:
- `max_users`:
- `max_items`:
- `seed`:

## Estatisticas Do Dataset

- usuarios avaliados:
- itens finais:
- interacoes treino:
- interacoes teste:
- itens premium:
- itens removidos sem preco:
- itens removidos por baixa interacao:

Fonte: `reports/evaluation/dataset_profile.json`

## Baselines Comparados

- Popularidade
- Conteudo/Categoria
- v0 congelado (quando usado no protocolo comparativo)

## Metricas Top-k

### Top-5

- Precision@5:
- Recall@5:
- nDCG@5:
- Cobertura de catalogo:
- Diversidade simples:

### Top-10

- Precision@10:
- Recall@10:
- nDCG@10:
- Cobertura de catalogo:
- Diversidade simples:

## Interpretacao Cautelosa

- Nao concluir ganho academico sem comparacao completa entre baselines.
- Nao extrapolar para comportamento real de clientes Kouzina.
- Tratar resultados como baseline offline inicial.

## Limitacoes

- recorte por proxy premium;
- diferenca de dominio entre Amazon publico e catalogo Kouzina;
- ausencia de validacao online real nesta fase.

## Proximos Passos

1. Executar preprocessamento com recorte documentado.
2. Rodar `run_offline_evaluation` para `k=5` e `k=10`.
3. Atualizar este documento com resultados reais.
4. Revisar ameacas a validade antes de avancar para Fase 6.
