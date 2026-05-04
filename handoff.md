# Review e Handoff do Projeto Kouzina Reco MVP

Data do handoff: 2026-05-03

Objetivo deste arquivo: registrar o que foi feito ate agora e orientar outro
CLI Codex a continuar o projeto sem reabrir escopos ja bloqueados.

## Estado Executivo

O projeto implementa o MVP local do Kouzina Reco: API FastAPI, PostgreSQL,
widget JavaScript, eventos anonimos, catalogo oficial autorizado importado e
recomendador v0 por regras comerciais.

Fases concluidas e validadas:

- Fase 1: API minima, widget local e fallback mockado.
- Fase 2: persistencia basica com PostgreSQL e seed.
- Fase 3: recomendador v0 por regras semanticas.
- Fase 3.1: demo local usando produto real do catalogo para exercitar ranking.
- Fase 4: ampliacao do seed ficticio para cerca de 30 produtos.
- Fase 4.2: suporte ao catalogo oficial autorizado local da Kouzina.
- Fase 4.2.1: padronizacao do nome canonico `data/products_kouzina_official.csv`.
- Fase 4.3: curadoria de catalogo e melhoria de inferencias.
- Fase 4.4: suporte completo a URL Tray e imagens do CSV oficial atualizado.
- Fase 4.5: ampliacao das relacoes complementares comerciais.
- Fase 4.6: relatorio CSV para revisao qualitativa das recomendacoes.
- Fase 4.7: pacote HTML estatico para revisao visual das recomendacoes.

Fora de escopo ate autorizacao explicita:

- fuzzy;
- ontologia;
- integracao Tray automatica;
- crawler;
- scraping;
- painel;
- login;
- deploy;
- app Tray;
- checkout tracking;
- coleta de dados pessoais;
- metricas e CTR automaticos;
- ranking por ML, LLM ou deep learning.

## Leitura Obrigatoria Para O Proximo Codex

Antes de alterar qualquer arquivo, ler nesta ordem:

1. `AGENTS.md`
2. `SKILL.md`
3. `README.md`
4. `docs/COMECAR.md`
5. `docs/API.md`
6. `docs/EVENTS.md`
7. `docs/DATA_MODEL.md`
8. `docs/RECOMMENDER.md`
9. `docs/CATALOG_QUALITY.md`
10. `docs/RECOMMENDATION_REVIEW.md`

`CLAUDE.md` deve ser tratado apenas como historico de Claude Code, nao como
fonte principal para Codex.

`docs/deep-research-report.md` e contexto academico e visao futura. Ele nao
autoriza implementar fuzzy, ontologia, crawler, scraping, painel, baselines,
deploy ou infraestrutura academica sem pedido explicito.

## Estado Atual Do Repositorio

Estrutura principal observada:

```text
backend/
  app/
    __init__.py
    database.py
    export_review_pack.py
    main.py
    models.py
    recommender.py
    review_recommendations.py
    schemas.py
    seed.py
    settings.py
  tests/
    test_api.py
  Dockerfile
  requirements.txt
data/
  products_seed.csv
  products_kouzina_official.csv
docs/
  API.md
  CATALOG_QUALITY.md
  COMECAR.md
  DATA_MODEL.md
  EVENTS.md
  MVP.md
  RECOMMENDATION_REVIEW.md
  RECOMMENDER.md
  TCC_NOTES.md
  deep-research-report.md
reports/
  .gitkeep
  recommendation_review.csv
  recommendation_review.html
  recommendation_review_churrasqueira.csv
widget/
  demo.html
  kouzina-reco.js
.gitignore
AGENTS.md
CLAUDE.md
README.md
SKILL.md
docker-compose.yml
handoff.md
```

Observacoes de workspace:

- `data/products_kouzina_official.csv` existe localmente e e ignorado pelo Git.
- `reports/*.csv`, `reports/*.xlsx` e `reports/*.html` sao ignorados pelo Git.
- `reports/.gitkeep` foi criado para manter a pasta no repositorio.
- `.env` existe localmente e e ignorado.
- `README.md` referencia `.env.example`, mas nesta inspecao o arquivo
  `.env.example` nao apareceu na raiz. Isso deve ser confirmado e corrigido em
  uma tarefa especifica, se o usuario autorizar.
- `git status --short` retornou avisos de permissao no global ignore do Git:
  `unable to access 'C:\Users\mateu/.config/git/ignore': Permission denied`.
  Nao houve listagem de alteracoes no stdout naquele comando. Rode novamente
  antes de qualquer nova fase.

## Arquitetura Atual

Fluxo local:

```text
widget/demo.html
  -> widget/kouzina-reco.js
  -> GET /recommendations
  -> POST /events
  -> FastAPI
  -> PostgreSQL
```

Componentes:

- Backend: Python, FastAPI, Pydantic, SQLAlchemy, PostgreSQL.
- Widget: JavaScript puro, sem React/Vue/Angular.
- Banco local: Docker Compose com PostgreSQL.
- Seed: CSV ficticio e CSV oficial autorizado local.
- Testes: pytest com SQLite temporario para testes unitarios/de API.
- Relatorio: CSV gerado em `reports/recommendation_review.csv` e HTML visual
  gerado em `reports/recommendation_review.html`.

## Contratos Da API

### GET /health

Resposta esperada:

```json
{
  "status": "ok",
  "service": "kouzina-reco-api",
  "version": "0.1.0"
}
```

### POST /events

Recebe eventos anonimos do widget e salva em `recommendation_events` quando o
banco esta disponivel.

Eventos permitidos:

```text
page_view
product_view
recommendation_impression
recommendation_click
```

Campos aceitos no payload:

```text
event_type
anonymous_id
session_id
page_url
product_id
widget_id
recommended_product_id
metadata
```

O backend filtra `metadata` por allowlist. Chaves sensiveis como e-mail sao
descartadas. Chaves tecnicas preservadas incluem:

```text
recommendation_count
recommended_product_ids
score
```

### GET /recommendations

Parametro principal:

```text
product_id
```

Tambem aceita:

```text
widget_id
```

Com catalogo importado e `product_id` existente, retorna recomendacoes reais do
banco ordenadas por score. Se o banco estiver vazio, indisponivel, sem
candidatos, ou se `product_id` nao existir, usa fallback mockado.

Cada item recomendado contem:

```text
product_id
name
url
image_url
price
reason
score
```

## Banco De Dados

Tabelas implementadas:

- `stores`
- `products`
- `recommendation_events`
- `manual_product_relations`

Detalhes importantes:

- A loja padrao e `kouzina`.
- `products` usa unicidade por `store_id` e `external_id`.
- `recommendation_events` persiste eventos anonimos.
- `manual_product_relations` existe, mas ainda nao e usada pelo recomendador.
- A API chama `init_db()` no startup para o MVP local.
- Ainda nao ha Alembic/migrations.

## Catalogos

### Seed Ficticio

Arquivo:

```text
data/products_seed.csv
```

Uso:

```powershell
cd backend
python -m app.seed
```

Caracteristicas:

- Catalogo ficticio de desenvolvimento.
- Cerca de 30 produtos.
- Serve para testar ranking sem depender do arquivo oficial.
- Nao deve ser confundido com catalogo real da Kouzina.

### Catalogo Oficial Autorizado

Arquivo canonico local:

```text
data/products_kouzina_official.csv
```

Caracteristicas:

- CSV autorizado pela Kouzina.
- Separador `;`.
- Encoding UTF-8 com BOM.
- Ignorado pelo Git.
- Nao deve ser commitado sem decisao explicita.
- Na ultima validacao registrada, importou 281 produtos.

Importacao:

```powershell
cd backend
python -m app.seed --file ..\data\products_kouzina_official.csv --replace-products
```

Mapeamentos relevantes:

- `Referencia` -> `external_id`.
- Referencia vazia -> `kouzina-auto-<numero-da-linha>`.
- `Nome produto` -> `name`.
- `Endereco do Produto (URL Tray)` -> `url`.
- `Imagem principal`, `Imagem 2`, `Imagem 3`, `Imagem 4`,
  `Imagens adicionais`, `Imagem` ou `image_url` -> `image_url`.
- Primeira URL valida de imagem e usada.
- Imagens sao apenas URLs; nao ha download nem binario salvo.
- `Preco venda` -> `price`, com regra especial para `0.00`.
- `Marca` -> `brand`, com normalizacao.
- `Nome categoria` -> `category` e `subcategory`.
- `Caracteristica: Voltagem` -> `voltage`.

Regra comercial de preco:

- `Preco venda > 0`: `price` preenchido, `available=true`,
  `availability_text="Preco informado"`.
- `Preco venda = 0.00`: `price=null`, `available=true`,
  `availability_text="Sob consulta"`.
- Preco vazio: `price=null`, `available=true`,
  `availability_text="Preco nao informado"`.

Produtos sob consulta:

- nao sao tratados como baratos;
- nao pontuam por faixa de preco proxima;
- continuam disponiveis para recomendacao;
- podem gerar reason `Produto sob consulta.`

Contagens validadas na Fase 4.4:

- Produtos importados: 281.
- Produtos com URL Tray: 281.
- Produtos com `image_url`: 281.
- Produtos sob consulta: 52.
- Produtos com preco informado: 229.
- Produtos com voltagem: 229.
- Produtos sem voltagem: 52.
- Produtos com `product_type`: 281.
- Produtos sem `product_type`: 0.
- Produtos com `environment`: 281.
- Produtos sem `environment`: 0.

## Curadoria Do Catalogo

A Fase 4.3 melhorou inferencias no importador:

- `product_type` vazio caiu de 25 para 0 no contexto daquela validacao.
- `environment` ficou preenchido para todos os produtos.
- Marcas como `Bert. Ital` e `Bertazzoni Italia` sao normalizadas para
  `Bertazzoni Italia` no relatorio e `Bertazzoni Italia/Italia com acento` no
  modelo, conforme encoding do arquivo.
- Voltagens repetidas como `220v, 220v` viram `220v`.
- Voltagens multiplas diferentes como `127v, 220v` viram `bivolt`.
- Categorias comuns sem acento sao padronizadas quando possivel.

Tipos inferidos e usados pelo recomendador incluem:

```text
Coifa
Cooktop
Forno
Adega
Churrasqueira
Cervejeira
Frigobar
Domino
Micro-ondas
Lava-loucas
Refrigerador
Fogao
Rangetop
Gaveta Aquecida
Gaveta Refrigerada
Freezer
Maquina de Gelo
Secadora
Lavadora
Conjugada
Cuba
Misturador
Queimador
Cafeteira
Acessorio de Coifa
Acessorio de Cozinha
Forno de Pizza
Dispenser de Agua
```

Ambientes:

```text
Cozinha Gourmet
Espaco Gourmet
Refrigeracao
Lavanderia
```

## Recomendador v0

Arquivo principal:

```text
backend/app/recommender.py
```

O recomendador e simples, deterministico e explicavel. Ele nao usa dados
pessoais, fuzzy, ontologia, machine learning, LLM ou deep learning.

Pesos atuais:

```text
-100 se for o mesmo produto
+30 se o tipo do candidato complementa o tipo do produto atual
+20 se o candidato esta disponivel
+15 se tem mesma voltagem
+15 se esta em faixa de preco proxima
+10 se tem mesma marca
+10 se pertence ao mesmo ambiente
+10 se tem nivel premium semelhante
-30 se estiver indisponivel
```

Ordenacao:

- score decrescente;
- desempate por `external_id`;
- o proprio produto nunca deve aparecer.

Relações complementares comerciais adicionadas ate a Fase 4.5:

```text
Cuba -> Misturador, Acessorio de Cozinha, Lava-loucas
Misturador -> Cuba, Acessorio de Cozinha
Coifa -> Cooktop, Forno, Domino, Acessorio de Coifa, Rangetop
Acessorio de Coifa -> Coifa
Cooktop -> Coifa, Forno, Domino
Domino -> Coifa, Cooktop, Forno
Forno -> Cooktop, Coifa, Micro-ondas, Gaveta Aquecida
Micro-ondas -> Forno, Cooktop, Gaveta Aquecida
Lava-loucas -> Cuba, Misturador, Acessorio de Cozinha
Adega -> Cervejeira, Frigobar, Churrasqueira, Forno de Pizza
Cervejeira -> Adega, Frigobar, Churrasqueira, Forno de Pizza, Maquina de Gelo
Frigobar -> Adega, Cervejeira, Churrasqueira
Churrasqueira -> Adega, Cervejeira, Coifa, Cooktop, Queimador, Forno de Pizza
Forno de Pizza -> Churrasqueira, Cervejeira, Adega
Refrigerador -> Freezer, Frigobar, Cervejeira, Maquina de Gelo
Freezer -> Refrigerador
Gaveta Aquecida -> Forno, Cooktop
Cafeteira -> Forno, Micro-ondas, Gaveta Aquecida
Queimador -> Churrasqueira, Cooktop, Rangetop
Rangetop -> Coifa, Forno, Queimador
Maquina de Gelo -> Cervejeira, Frigobar, Adega, Churrasqueira
Acessorio de Cozinha -> Cuba, Misturador, Lava-loucas
```

Limitacoes do recomendador:

- Relacoes sao comerciais/editoriais iniciais, nao ontologia formal.
- Nao ha personalizacao por usuario.
- Nao ha uso de historico individual.
- Nao ha uso de eventos para ajustar ranking ainda.
- URL e imagem nao entram na pontuacao.
- Produtos sob consulta nao pontuam por preco proximo.

## Widget

Arquivos:

```text
widget/kouzina-reco.js
widget/demo.html
```

Comportamento atual:

- JavaScript puro.
- Le `window.KouzinaReco`.
- Usa `localStorage` para `anonymous_id`.
- Usa `sessionStorage` para `session_id`.
- Detecta produto por `data-kouzina-product-id`, meta
  `product:retailer_item_id` ou texto `Codigo:`.
- Envia `page_view`.
- Chama `GET /recommendations`.
- Renderiza cards com nome, imagem, preco quando houver, reason e link.
- Envia `recommendation_impression`.
- Envia `recommendation_click` com `recommended_product_id`.
- Falha com `console.warn`, sem quebrar a pagina.
- Nao contem token secreto privado; usa apenas chave publica de desenvolvimento.

Demo atual:

```text
http://localhost:5500/demo.html
```

`widget/demo.html` usa `product_id` real oficial:

```text
119
```

Produto demonstrativo:

```text
Churrasqueira a Gas GLP de Embutir Inox 304
```

## Privacidade E LGPD

Dados permitidos:

```text
anonymous_id
session_id
event_type
page_url
product_id
widget_id
recommended_product_id
metadata tecnico nao sensivel
timestamp
```

Dados proibidos:

```text
nome
CPF
e-mail
telefone
endereco
dados de pagamento
conteudo de formularios
mensagens de WhatsApp
dados sensiveis
```

O MVP atual nao deve coletar dados pessoais. O backend filtra `metadata` para
evitar persistir chaves sensiveis.

## Relatorio De Revisao Qualitativa

Fase 4.6 criou:

```text
backend/app/review_recommendations.py
docs/RECOMMENDATION_REVIEW.md
reports/.gitkeep
```

Comando padrao:

```powershell
cd backend
python -m app.review_recommendations
```

Saida padrao:

```text
reports/recommendation_review.csv
```

Parametros:

```text
--limit-products
--top-k
--output
--product-type
```

Exemplo:

```powershell
python -m app.review_recommendations --product-type Churrasqueira --top-k 4
```

Colunas do CSV:

```text
source_product_id
source_name
source_product_type
source_category
source_brand
source_price
source_availability_text
recommended_product_id
recommended_name
recommended_product_type
recommended_category
recommended_brand
recommended_price
recommended_availability_text
score
reason
source_url
recommended_url
recommended_image_url
reviewer_rating
reviewer_comment
```

`reviewer_rating` e `reviewer_comment` ficam vazios para preenchimento manual.

Escala recomendada:

```text
1 = ruim
2 = fraca
3 = aceitavel
4 = boa
5 = excelente
```

Objetivo do relatorio:

- validar qualitativamente se a recomendacao complementa o produto atual;
- revisar se faz sentido comercial;
- identificar produtos que deveriam aparecer antes;
- avaliar se produtos sob consulta devem aparecer em certos contextos;
- avaliar se a explicacao esta clara.

## Pacote HTML De Revisao Qualitativa

Fase 4.7 criou:

```text
backend/app/export_review_pack.py
backend/tests/test_review_pack.py
```

Comando padrao:

```powershell
cd backend
python -m app.export_review_pack
```

Entrada padrao:

```text
reports/recommendation_review.csv
```

Saida padrao:

```text
reports/recommendation_review.html
```

Parametros:

```text
--input
--output
--limit
--min-score
--product-type
```

Objetivo do HTML:

- facilitar a reuniao de revisao com a Kouzina;
- mostrar origem, recomendado, imagem, score e reason em cards;
- mostrar escala de rating de 1 a 5;
- manter campos visuais para `reviewer_rating` e `reviewer_comment`;
- apoiar discussao comercial sem virar painel.

Limitacoes:

- o HTML e estatico e apenas visual;
- o preenchimento oficial continua no CSV ou em planilha copiada;
- nao altera banco;
- nao altera ranking;
- nao calcula CTR;
- nao chama API externa;
- nao baixa imagens;
- nao usa dados pessoais.

## Validacoes Registradas

Ultima validacao consolidada informada no projeto:

```text
python -m pytest
23 passed
```

Tambem foi validado:

```text
.\.venv\Scripts\python.exe -m pytest
23 passed
```

Importacao oficial validada:

```powershell
cd backend
.\.venv\Scripts\python.exe -m app.seed --file ..\data\products_kouzina_official.csv --replace-products
```

Resultado registrado:

```text
281 produtos importados
281 produtos com URL Tray
281 produtos com image_url
52 produtos sob consulta
229 produtos com preco informado
229 produtos com voltagem
52 produtos sem voltagem
0 produtos sem product_type
0 produtos sem environment
```

Relatorio qualitativo validado:

```powershell
.\.venv\Scripts\python.exe -m app.review_recommendations
```

Resultado registrado:

```text
Generated 120 recommendation review rows for 30 source products at reports/recommendation_review.csv
```

Relatorio filtrado validado:

```powershell
.\.venv\Scripts\python.exe -m app.review_recommendations --product-type Churrasqueira --top-k 4 --limit-products 2 --output reports/recommendation_review_churrasqueira.csv
```

Resultado registrado:

```text
Generated 8 recommendation review rows for 2 source products
```

Validacoes de recomendacao feitas em fases anteriores:

```text
119
3618
GW951X-BR
2477
2139
product_id de Cuba
product_id de Misturador
product_id de Churrasqueira
```

Para esses cenarios, foi confirmado:

- status 200;
- recomendacoes vindas do catalogo quando produto existe;
- fallback quando produto nao existe ou catalogo indisponivel;
- proprio produto ausente;
- ordenacao por score decrescente;
- reason presente;
- `url` presente quando disponivel;
- `image_url` presente quando disponivel;
- produtos sob consulta com `price=null` e sem pontuacao de preco proximo.

## Comandos Para Retomar Localmente

Subir banco:

```powershell
docker compose up -d
```

Entrar no backend:

```powershell
cd backend
```

Criar/ativar venv, se necessario:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Rodar testes:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Importar seed ficticio:

```powershell
.\.venv\Scripts\python.exe -m app.seed
```

Importar catalogo oficial autorizado:

```powershell
.\.venv\Scripts\python.exe -m app.seed --file ..\data\products_kouzina_official.csv --replace-products
```

Rodar API:

```powershell
uvicorn app.main:app --reload
```

Testar health:

```powershell
Invoke-RestMethod http://localhost:8000/health
```

Testar recomendacao oficial:

```powershell
Invoke-RestMethod "http://localhost:8000/recommendations?product_id=119&widget_id=product-page"
```

Servir widget:

```powershell
cd ..\widget
python -m http.server 5500
```

Abrir:

```text
http://localhost:5500/demo.html
```

Gerar relatorio qualitativo:

```powershell
cd ..\backend
.\.venv\Scripts\python.exe -m app.review_recommendations
```

Gerar pacote HTML de revisao:

```powershell
.\.venv\Scripts\python.exe -m app.export_review_pack
```

## Arquivos Criados Ou Alterados Por Fase

### Fase 1

- `backend/app/main.py`
- `backend/app/schemas.py`
- `backend/app/recommender.py`
- `backend/app/settings.py`
- `backend/Dockerfile`
- `backend/requirements.txt`
- `widget/kouzina-reco.js`
- `widget/demo.html`
- `data/products_seed.csv`
- `docker-compose.yml`
- `README.md`
- documentos em `docs/`

### Fase 2

- `backend/app/database.py`
- `backend/app/models.py`
- `backend/app/seed.py`
- `backend/app/main.py`
- `backend/app/recommender.py`
- `backend/tests/test_api.py`
- `docs/DATA_MODEL.md`
- `docs/API.md`
- `docs/EVENTS.md`
- `README.md`

### Fase 3

- `backend/app/recommender.py`
- `backend/app/main.py`
- `backend/tests/test_api.py`
- `docs/RECOMMENDER.md`
- `docs/MVP.md`
- `README.md`

### Fase 3.1

- `widget/demo.html`

### Fase 4

- `data/products_seed.csv`
- `docs/DATA_MODEL.md`
- `docs/RECOMMENDER.md`

### Fase 4.2 E 4.2.1

- `.gitignore`
- `README.md`
- `backend/app/seed.py`
- `backend/app/recommender.py`
- `backend/tests/test_api.py`
- `docs/API.md`
- `docs/DATA_MODEL.md`
- `docs/MVP.md`
- `docs/RECOMMENDER.md`
- `docs/CATALOG_QUALITY.md`
- `widget/demo.html`

### Fase 4.3

- `backend/app/seed.py`
- `backend/tests/test_api.py`
- `docs/CATALOG_QUALITY.md`
- `docs/DATA_MODEL.md`
- `docs/RECOMMENDER.md`

### Fase 4.4

- `backend/app/seed.py`
- `backend/tests/test_api.py`
- `docs/DATA_MODEL.md`
- `docs/CATALOG_QUALITY.md`
- `README.md`

### Fase 4.5

- `backend/app/recommender.py`
- `backend/tests/test_api.py`
- `docs/RECOMMENDER.md`
- `docs/CATALOG_QUALITY.md`

### Fase 4.6

- `.gitignore`
- `README.md`
- `backend/app/review_recommendations.py`
- `backend/tests/test_api.py`
- `docs/RECOMMENDATION_REVIEW.md`
- `reports/.gitkeep`

### Fase 4.7

- `.gitignore`
- `README.md`
- `backend/app/export_review_pack.py`
- `backend/tests/test_review_pack.py`
- `docs/RECOMMENDATION_REVIEW.md`
- `handoff.md`

## Decisoes Importantes

- `products_seed.csv` permanece como seed ficticio de desenvolvimento.
- `products_kouzina_official.csv` e o catalogo oficial autorizado local.
- O CSV oficial e ignorado pelo Git.
- `Preco venda = 0.00` significa `Sob consulta`.
- Produto sob consulta tem `price=null` e `available=true`.
- Produto sob consulta nao pontua por faixa de preco proxima.
- Nao baixar imagens do catalogo.
- Salvar somente URL de imagem em `products.image_url`.
- Nao usar URL ou imagem como criterio de ranking.
- Nao coletar dados pessoais.
- Nao expor token secreto no JavaScript.
- O widget deve falhar com `console.warn` e nao quebrar a pagina.
- O fallback mockado deve permanecer para proteger o demo/widget.
- Fuzzy e ontologia so entram depois de autorizacao explicita.
- A avaliacao qualitativa vem antes de metricas/CTR automaticos.

## Riscos, Limitacoes E Pontos De Atencao

- `.env.example` esta referenciado no README, mas nao foi encontrado nesta
  inspecao. Confirmar antes da proxima entrega operacional.
- Nao ha migrations Alembic; o MVP cria tabelas via `init_db()`.
- `manual_product_relations` existe, mas ainda nao influencia o ranking.
- Nao ha autenticacao real de `publicKey` no backend.
- Nao ha rate limiting.
- Nao ha deploy nem ambiente HTTPS publicado.
- Nao ha integracao Tray automatica.
- Nao ha painel para visualizar eventos.
- Nao ha calculo automatico de CTR ainda.
- Relatorios em `reports/*.csv` e `reports/*.html` sao gerados localmente e
  ignorados pelo Git.
- O arquivo oficial `data/products_kouzina_official.csv` e local; outro
  ambiente precisa receber esse arquivo manualmente.
- Alguns documentos exibem acentos quebrados dependendo do encoding do
  terminal, mas o projeto deve continuar tratando CSV oficial como UTF-8 com BOM.
- O comando Git pode emitir aviso de permissao no global ignore do usuario.

## Proximo Passo Recomendado

Nao avancar direto para fuzzy, ontologia ou deploy.

Proximo passo pratico:

1. Gerar `reports/recommendation_review.csv` com o catalogo oficial atual.
2. Gerar `reports/recommendation_review.html`.
3. Usar o HTML na reuniao de revisao com a Kouzina.
4. Preencher `reviewer_rating` e `reviewer_comment` no CSV ou planilha copiada.
5. Consolidar comentarios em ajustes editoriais.
6. Decidir se a proxima fase sera:
   - ajustes nas relacoes complementares;
   - uso de `manual_product_relations`;
   - criacao de relatorio de eventos/CTR;
   - ou preparacao controlada para teste em ambiente real.

Somente depois dessa revisao qualitativa faz sentido planejar metricas/CTR.
Fuzzy e ontologia continuam como fase academica posterior.

## Instrucao Para Outro CLI Codex

Antes de implementar qualquer nova tarefa:

- rode `git status`;
- confirme se o usuario quer apenas validacao, documentacao ou implementacao;
- leia os documentos obrigatorios listados no inicio deste arquivo;
- preserve `AGENTS.md`, `SKILL.md`, `CLAUDE.md` e os documentos existentes;
- nao altere o catalogo oficial sem pedido explicito;
- nao crie escopo novo fora da fase pedida;
- rode testes relevantes apos qualquer mudanca;
- registre comandos executados e resultados no fechamento.

Se a proxima tarefa mencionar Fase 5, fuzzy ou ontologia, confirme o escopo
com o usuario e mantenha a implementacao pequena, explicavel e documentada.
