# MVP Kouzina Reco

## Objetivo

Entregar uma primeira versao local, simples e mensuravel do Kouzina Reco:

- API FastAPI minima;
- widget JavaScript puro;
- recomendacoes mockadas;
- eventos anonimos mockados;
- PostgreSQL preparado via Docker Compose, ainda sem conexao com a API.

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

## Fora de escopo nesta fase

- banco persistente conectado;
- SQLAlchemy models completos;
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
- `/events` valida payload e confirma recebimento;
- `/recommendations` retorna recomendacoes mockadas;
- `demo.html` carrega o widget;
- widget renderiza recomendacoes;
- widget envia `page_view`;
- widget envia `recommendation_impression`;
- widget envia `recommendation_click`;
- nenhum dado pessoal e coletado.

