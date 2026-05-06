# Resultados Fase 5 Baseline (Piloto Real)

## Objetivo

Registrar os resultados da primeira execucao offline reproduzivel da Fase 5.1,
com dataset publico e baselines simples, sem fuzzy e sem ontologia.

## Status Atual

Execucao real concluida em 2026-05-06, com preprocessamento local de
`Appliances` e avaliacao offline para `top-k 5` e `top-k 10`.

## Dataset E Recorte

- Dataset: Amazon Reviews 2023
- Piloto atual: `Appliances`
- Recorte de referencia para expansao: `Home_and_Kitchen`, `Appliances`
- Regra premium (proxy): `price >= P75` por categoria
- Observacao: premium e proxy de produto, nao perfil real de consumidor

## Filtros Aplicados

- `min_rating`: `4.0`
- `min_item_interactions`: `20`
- `min_user_interactions`: `2`
- `premium_percentile`: `0.75` (`P75`)
- `require_verified_purchase`: `false`
- `max_users`: `null`
- `max_items`: `null`
- `seed`: `42`

## Estatisticas Do Dataset

- usuarios avaliados: `6651`
- itens finais: `2798`
- interacoes treino: `7368`
- interacoes teste: `6651`
- itens premium antes do filtro final de split: `4916`
- itens removidos sem preco: `28083`
- itens removidos por baixa interacao: `15428`
- itens removidos por baixa avaliacao media: `25880`

Fonte: `reports/evaluation/dataset_profile.json`

## Baselines Comparados

- Popularidade
- Conteudo/Categoria
- v0 congelado (quando usado no protocolo comparativo)

## Metricas Top-k

### Top-5

Popularidade:

- Precision@5: `0.010164`
- Recall@5: `0.050819`
- nDCG@5: `0.031299`
- Cobertura de catalogo: `0.002502`
- Diversidade simples: `0.000000`

Conteudo/Categoria:

- Precision@5: `0.010164`
- Recall@5: `0.050819`
- nDCG@5: `0.031299`
- Cobertura de catalogo: `0.002502`
- Diversidade simples: `0.000000`

### Top-10

Popularidade:

- Precision@10: `0.008976`
- Recall@10: `0.089761`
- nDCG@10: `0.043978`
- Cobertura de catalogo: `0.004289`
- Diversidade simples: `0.000000`

Conteudo/Categoria:

- Precision@10: `0.008976`
- Recall@10: `0.089761`
- nDCG@10: `0.043978`
- Cobertura de catalogo: `0.004289`
- Diversidade simples: `0.000000`

## Interpretacao Cautelosa

- Nao concluir ganho academico sem comparacao completa entre baselines.
- Nao extrapolar para comportamento real de clientes Kouzina.
- Tratar resultados como baseline offline inicial.
- Como o recorte usa uma unica categoria (`Appliances`), o baseline por
  categoria ficou equivalente ao baseline de popularidade neste piloto.

## Limitacoes

- recorte por proxy premium;
- diferenca de dominio entre Amazon publico e catalogo Kouzina;
- ausencia de validacao online real nesta fase.

## Proximos Passos

1. Rodar nova iteracao com `require_verified_purchase=true` para sensibilidade
   metodologica.
2. Comparar piloto `Appliances` com recorte futuro que inclua
   `Home_and_Kitchen` (sem misturar conclusoes).
3. Preparar baseline comparativo com snapshot v0 congelado no protocolo.
4. Revisar ameacas a validade antes de qualquer decisao sobre Fase 6.
