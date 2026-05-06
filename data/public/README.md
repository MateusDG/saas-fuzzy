# Data Public - Guia Da Fase 5

## Objetivo

Esta pasta organiza datasets publicos usados na avaliacao academica offline da
Fase 5.

## Regra De Versionamento

Arquivos grandes de dataset publico nao devem ser commitados no Git.

Manter no repositorio apenas:

- documentacao;
- exemplos pequenos de schema (quando necessario);
- artefatos leves de configuracao.

## Estrutura Esperada

```text
data/public/
  README.md
  raw/
  processed/
```

### `raw/`

Coloque aqui os arquivos brutos baixados manualmente (fora do Git), por
exemplo:

- `interactions_raw.csv`
- `items_raw.csv`

### `processed/`

Coloque aqui os arquivos processados para execucao dos scripts offline, por
exemplo:

- `interactions_train.csv`
- `interactions_test.csv`
- `items.csv`

## Formatos Esperados

### `interactions_train.csv`

Colunas minimas:

- `user_id`
- `item_id`
- `event_name`

Colunas recomendadas:

- `timestamp`

### `interactions_test.csv`

Colunas minimas:

- `user_id`
- `item_id`

Colunas opcionais:

- `relevance` (quando ausente, o pipeline assume relevancia binaria = 1)
- `relation_policy_action`

### `items.csv`

Colunas minimas:

- `item_id`
- `category`

Colunas recomendadas:

- `brand`
- `environment`
- `price_band`

## Execucao Offline

Script principal:

```powershell
cd backend
python -m app.run_offline_evaluation --top-k 10
```

O script espera os CSVs em `data/public/processed/` por padrao.

## LGPD E Privacidade

- nao incluir dados pessoais identificaveis;
- nao usar dados reais de clientes Kouzina sem autorizacao formal e base legal;
- usar apenas dataset publico ou dados sinteticos de teste.
