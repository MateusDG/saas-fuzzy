# MVP Kouzina Reco

## Objetivo

Entregar uma primeira versao local, simples e mensuravel do Kouzina Reco:

- API FastAPI minima;
- widget JavaScript puro;
- recomendacoes via catalogo inicial, com fallback mockado;
- eventos anonimos persistidos quando o banco esta disponivel;
- PostgreSQL preparado via Docker Compose.

## Escopo da Fase 1 tecnica local

Inclui:

- `GET /health`;
- `POST /events`;
- `GET /recommendations`;
- `widget/kouzina-reco.js`;
- `widget/demo.html`;
- `docker-compose.yml`;
- `.env.example`;
- `data/products_seed.csv` com 3 produtos mockados.

## Escopo da Fase 2

Inclui:

- conexao da API ao PostgreSQL;
- tabelas `stores`, `products`, `recommendation_events` e `manual_product_relations`;
- seed idempotente do catalogo inicial;
- persistencia de eventos anonimos;
- recomendacoes usando produtos do banco quando houver catalogo;
- fallback mockado quando o banco estiver vazio ou indisponivel;
- testes basicos.

## Fora de escopo nesta fase

- ranking real;
- fuzzy;
- ontologia;
- integracao Tray;
- painel;
- login;
- deploy;
- coleta de dados pessoais.

## Criterios de sucesso

- API roda localmente;
- `/health` responde;
- `/events` valida payload e salva evento quando o banco esta disponivel;
- `/recommendations` retorna recomendacoes do catalogo ou fallback mockado;
- `demo.html` carrega o widget;
- widget renderiza recomendacoes;
- widget envia `page_view`;
- widget envia `recommendation_impression`;
- widget envia `recommendation_click`;
- nenhum dado pessoal e coletado.
