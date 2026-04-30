# MVP Kouzina Reco

## Objetivo

Entregar uma primeira versao local, simples e mensuravel do Kouzina Reco:

- API FastAPI minima;
- widget JavaScript puro;
- recomendacoes via catalogo inicial e ranking v0 por regras, com fallback mockado;
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

## Escopo da Fase 3

Inclui:

- recomendador v0 por regras semanticas simples;
- pontuacao por complementaridade, disponibilidade, voltagem, preco, marca,
  ambiente e nivel premium;
- exclusao do proprio produto visualizado;
- ordenacao por score decrescente;
- motivos textuais para cada recomendacao;
- fallback mockado quando o produto atual nao existir ou nao houver candidatos;
- testes do ranking e do endpoint `/recommendations`.

## Fora de escopo nesta fase

- ranking sofisticado;
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
- `/recommendations` retorna recomendacoes do catalogo ordenadas por ranking v0 ou fallback mockado;
- `demo.html` carrega o widget;
- widget renderiza recomendacoes;
- widget envia `page_view`;
- widget envia `recommendation_impression`;
- widget envia `recommendation_click`;
- nenhum dado pessoal e coletado.
