# Modelo De Dados

Na Fase 2, a API conecta ao PostgreSQL usando `DATABASE_URL`, cria tabelas no
startup do MVP e permite importar o catalogo inicial por CSV.

## Dados Mockados

O arquivo `data/products_seed.csv` contem 3 produtos mockados para documentar o
formato inicial do catalogo.

Colunas:

```text
external_id
name
url
image_url
category
subcategory
brand
price
available
availability_text
voltage
width_cm
installation_type
product_type
environment
premium_level
```

## Tabelas Implementadas

### `stores`

Representa a loja. A Fase 2 cria uma loja padrao `kouzina`.

Campos principais:

- `id`;
- `slug`;
- `name`;
- `domain`;
- `public_key`;
- `created_at`.

### `products`

Representa produtos importados de `data/products_seed.csv`.

Campos principais:

- `store_id`;
- `external_id`;
- `name`;
- `url`;
- `image_url`;
- `category`;
- `subcategory`;
- `brand`;
- `price`;
- `available`;
- `availability_text`;
- `voltage`;
- `width_cm`;
- `installation_type`;
- `product_type`;
- `environment`;
- `premium_level`;
- `active`;
- `created_at`;
- `updated_at`.

Existe restricao unica por `store_id` e `external_id` para evitar duplicacao no
seed.

### `recommendation_events`

Representa eventos anonimos enviados pelo widget.

Campos principais:

- `event_type`;
- `anonymous_id`;
- `session_id`;
- `page_url`;
- `product_external_id`;
- `widget_id`;
- `recommended_product_external_id`;
- `metadata`;
- `created_at`.

### `manual_product_relations`

Tabela simples criada para relacoes manuais futuras entre produtos. A Fase 2
apenas cria a estrutura; ainda nao usa essa tabela no recomendador.

## Eventos

Na Fase 2, eventos sao recebidos, validados e salvos quando o banco esta
disponivel.
