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

Coloque aqui os arquivos brutos baixados manualmente (fora do Git).

Para a Fase 5.1 (Amazon Reviews 2023), usar:

- arquivo de reviews/interacoes (`.jsonl` ou `.jsonl.gz`);
- arquivo de metadata de itens (`.jsonl` ou `.jsonl.gz`).

Piloto atual (executado localmente):

- `raw/Appliances.jsonl`
- `raw/meta_Appliances.jsonl`

Exemplos de nomes locais adicionais (etapas posteriores):

- `raw/Home_and_Kitchen.jsonl.gz`
- `raw/meta_Home_and_Kitchen.jsonl.gz`

O preprocessador aceita caminhos configuraveis por CLI, sem assumir nome fixo.

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

## Preprocessamento Amazon Reviews 2023

Comando base:

```powershell
cd backend
python -m app.preprocess_amazon_reviews_2023 `
  --reviews-file ../data/public/raw/Appliances.jsonl `
  --metadata-file ../data/public/raw/meta_Appliances.jsonl `
  --output-dir ../data/public/processed `
  --categories Appliances `
  --premium-percentile 0.75 `
  --min-rating 4 `
  --min-item-interactions 20 `
  --min-user-interactions 2
```

Saidas obrigatorias:

- `data/public/processed/interactions_train.csv`
- `data/public/processed/interactions_test.csv`
- `data/public/processed/items.csv`
- `reports/evaluation/dataset_profile.json`

Regra metodologica desta fase:

- premium e apenas proxy de produto (preco por percentil), nao perfil real de
  consumidor.

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
