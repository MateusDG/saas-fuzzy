# MVP Kouzina Reco

## Objetivo

Entregar uma primeira versao local, simples e mensuravel do Kouzina Reco:

- API FastAPI minima;
- widget JavaScript puro;
- recomendacoes via catalogo inicial e ranking v0 por regras, com fallback mockado;
- eventos anonimos persistidos quando o banco esta disponivel;
- PostgreSQL preparado via Docker Compose.
- importacao local de catalogo oficial autorizado da Kouzina.

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

## Escopo da Fase 4

Inclui:

- catalogo ficticio de desenvolvimento com cerca de 30 produtos;
- variedade de categorias, marcas, voltagens, ambientes e disponibilidade;
- validacao mais realista do ranking v0.

## Escopo da Fase 4.2

Inclui:

- suporte a CSV oficial autorizado da Kouzina em UTF-8 com BOM e separador `;`;
- importacao opcional com `python -m app.seed --file <arquivo>`;
- substituicao do catalogo local com `--replace-products`, preservando eventos;
- tratamento de `Preco venda = 0.00` como `Sob consulta`;
- recomendador v0 operando sobre catalogo oficial autorizado local.

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
- catalogo oficial autorizado pode ser importado localmente sem coleta de dados pessoais;
- `demo.html` carrega o widget;
- widget renderiza recomendacoes;
- widget envia `page_view`;
- widget envia `recommendation_impression`;
- widget envia `recommendation_click`;
- nenhum dado pessoal e coletado.
