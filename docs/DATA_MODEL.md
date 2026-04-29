# Modelo De Dados

Na Fase 1 tecnica local, o banco PostgreSQL e preparado via Docker Compose, mas
a API ainda nao conecta nem cria tabelas.

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

## Tabelas Futuras

Estas tabelas pertencem a Fase 2 ou posterior e ainda nao foram implementadas:

- `stores`;
- `products`;
- `manual_product_relations`;
- `recommendation_events`.

## Eventos

Na Fase 1, eventos sao recebidos e validados, mas nao sao salvos.

