# Amazon Reviews 2023 - Preprocessamento (Fase 5.1)

## Objetivo

Padronizar um recorte reproduzivel do dataset Amazon Reviews 2023 para executar
o pipeline offline da Fase 5 sem fuzzy, sem ontologia e sem dados reais de
clientes Kouzina.

Este preprocessamento gera os CSVs esperados por
`backend/app/run_offline_evaluation.py`:

- `interactions_train.csv`
- `interactions_test.csv`
- `items.csv`

Tambem gera um perfil leve da execucao em:

- `reports/evaluation/dataset_profile.json`

## Decisao De Recorte Inicial

Dataset principal: Amazon Reviews 2023.

Categorias de referencia para a Fase 5:

- `Home_and_Kitchen`
- `Appliances`

Execucao piloto atual (antes da Fase 5.2):

- somente `Appliances`.

Regra desta fase:

- "high-end" e tratado apenas como proxy de produto premium;
- nao representa renda, classe social ou perfil real de consumidor;
- continua pendente de validacao com comportamento real futuro.

## Arquivos Brutos Esperados

O script aceita arquivos locais `.jsonl` ou `.jsonl.gz`:

- reviews/interacoes;
- metadata de itens.

Campos esperados (quando disponiveis):

- reviews: `user_id`, `parent_asin`, `rating`, `timestamp`,
  `verified_purchase`;
- metadata: `parent_asin`, `main_category`, `categories`, `price`,
  `average_rating`, `rating_number`, `title`, `store`.

Nao ha download automatico no repositorio.

## Comando De Preprocessamento

Piloto atual (`Appliances`):

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

Comando generico (quando houver outras categorias locais):

```powershell
cd backend
python -m app.preprocess_amazon_reviews_2023 `
  --reviews-file ../data/public/raw/<reviews>.jsonl.gz `
  --metadata-file ../data/public/raw/<metadata>.jsonl.gz `
  --output-dir ../data/public/processed `
  --categories Home_and_Kitchen Appliances `
  --premium-percentile 0.75 `
  --min-rating 4 `
  --min-item-interactions 20 `
  --min-user-interactions 2
```

Opcoes uteis:

- `--require-verified-purchase`
- `--max-users`
- `--max-items`
- `--seed`

## Regras Aplicadas

1. Filtro por categoria (`Home_and_Kitchen`, `Appliances`).
2. Filtro de qualidade de item (`average_rating >= min_rating`).
3. Filtro de preco valido.
4. Filtro de suporte minimo por item (`rating_number` ou interacoes positivas).
5. Recorte premium por percentil de preco da propria categoria:
   - corte principal: `>= P75` (`--premium-percentile 0.75`);
   - `price_band`:
     - `unknown` (sem preco),
     - `standard` (< P75),
     - `premium` (P75 ate P90),
     - `ultra_premium` (>= P90).
6. Interacao positiva: `rating >= min_rating`.
7. Split temporal por usuario:
   - ultima interacao positiva vai para teste;
   - anteriores vao para treino;
   - cada usuario avaliado precisa de pelo menos 1 item no treino e 1 no teste;
   - sem vazamento do item de teste no treino do mesmo usuario.

## Estrutura De Saida

### `interactions_train.csv`

Colunas:

- `user_id`
- `item_id`
- `event_name`
- `timestamp`

### `interactions_test.csv`

Colunas:

- `user_id`
- `item_id`
- `relevance`

### `items.csv`

Colunas minimas:

- `item_id`
- `category`

Colunas adicionais:

- `brand`
- `price_band`
- `average_rating`
- `rating_number`
- `price`
- `title`

### `dataset_profile.json`

Inclui:

- dataset usado;
- data da execucao;
- categorias;
- filtros aplicados;
- percentis;
- contagens finais de usuarios/itens/interacoes;
- itens removidos por preco ausente;
- itens removidos por baixa interacao;
- seed;
- observacoes e limitacoes.

## Execucao Da Avaliacao Offline

Depois de gerar os CSVs:

```powershell
cd backend
python -m app.run_offline_evaluation --top-k 5
python -m app.run_offline_evaluation --top-k 10
```

## Limitacoes Metodologicas

- proxy premium por preco nao valida publico high-end real;
- categoria publica Amazon nao representa integralmente o dominio Kouzina;
- atributos tecnicos de cozinha premium podem estar ausentes no dataset publico;
- este recorte nao substitui validacao futura com telemetria real anonima.

## Versionamento

- arquivos grandes de dataset bruto/processado nao devem ser commitados;
- manter apenas codigo, documentacao e artefatos leves de configuracao.
