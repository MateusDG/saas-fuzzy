# Kouzina Reco MVP

MVP comercial minimo de recomendacao para o site Kouzina Club.

Este repositorio implementa a base local das Fases 1, 2, 3, 4, 4.2, 4.3, 4.4, 4.5, 4.6 e 4.7:

- API FastAPI minima.
- `GET /health`.
- `POST /events` com validacao de payload e persistencia em PostgreSQL.
- `GET /recommendations` usando catalogo importado e ranking v0 por regras, com fallback mockado.
- Widget JavaScript puro.
- Demo local do widget.
- PostgreSQL via Docker Compose.
- CSV seedado com cerca de 30 produtos mockados ou semi-realistas.
- Importacao local de catalogo oficial autorizado da Kouzina via CSV exportado.
- Curadoria de catalogo oficial para inferir tipo, ambiente, marca, categoria e voltagem.
- Suporte a URL Tray e imagem principal/adicional do catalogo oficial autorizado.
- Relacoes complementares comerciais iniciais para tipos reais do catalogo oficial.
- Relatorio CSV para revisao qualitativa das recomendacoes.
- Pacote HTML estatico para revisao visual das recomendacoes pela Kouzina.

Fora de escopo: fuzzy, ontologia, integracao Tray, painel, login, deploy,
ranking sofisticado, crawler, scraping e multi-loja completo.

## Estrutura

```text
backend/
  app/
    __init__.py
    main.py
    database.py
    export_review_pack.py
    models.py
    recommender.py
    review_recommendations.py
    schemas.py
    seed.py
    settings.py
  tests/
  Dockerfile
  requirements.txt
widget/
  demo.html
  kouzina-reco.js
data/
  products_seed.csv
  products_kouzina_official.csv  # local, ignorado pelo Git
docker-compose.yml
.env.example
```

## Configuracao local

Crie um `.env` local a partir do exemplo:

```bash
copy .env.example .env
```

No PowerShell, o comando equivalente tambem funciona:

```powershell
Copy-Item .env.example .env
```

## Rodar PostgreSQL

O banco e usado pelas Fases 2 e 3 para produtos, eventos e ranking v0.

```bash
docker compose up -d
```

## Rodar API local

No Windows PowerShell:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Em macOS/Linux:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

A API ficara em:

```text
http://localhost:8000
```

## Criar tabelas e importar produtos

A API tenta criar as tabelas no startup. Sem argumentos, o seed importa o
catalogo ficticio de desenvolvimento em `data/products_seed.csv`:

```powershell
cd backend
python -m app.seed
```

O seed cria a loja padrao Kouzina e importa `data/products_seed.csv`. A
importacao e idempotente por `external_id`, entao pode ser rodada mais de uma
vez sem duplicar produtos.

## Importar catalogo oficial autorizado

A Fase 4.2 adiciona suporte ao CSV oficial autorizado da Kouzina. Coloque o
arquivo local em:

```text
data/products_kouzina_official.csv
```

Esse arquivo nao deve ser versionado. O `.gitignore` ignora:

```text
data/products_kouzina_official.csv
data/products_kouzina_official.xlsx
data/raw/
```

O CSV oficial deve estar em UTF-8 com BOM, usar separador `;` e conter colunas
como `Nome produto`, `Preco venda`, `Referencia`, `Nome categoria`, marca,
voltagem, URL Tray e imagens. A Fase 4.4 suporta `Imagem principal`,
`Imagem 2`, `Imagem 3`, `Imagem 4`, `Imagens adicionais`, `Imagem` e
`image_url`. A leitura usa `utf-8-sig`; nao converta para Latin-1 ou
ISO-8859-1.

O importador salva apenas URLs. Ele nao baixa imagens e nao salva arquivo ou
binario no banco. Quando mais de uma imagem estiver disponivel, o sistema usa a
primeira URL valida seguindo a ordem das colunas acima.

Para importar sem apagar produtos existentes:

```powershell
cd backend
python -m app.seed --file ../data/products_kouzina_official.csv
```

Para substituir o catalogo da loja padrao antes de importar:

```powershell
cd backend
python -m app.seed --file ../data/products_kouzina_official.csv --replace-products
```

`--replace-products` remove produtos e relacoes manuais da loja `kouzina`, mas
preserva `recommendation_events`.

Regra comercial: no CSV oficial, `Preco venda` igual a `0.00` significa
`Sob consulta`. Nesse caso a API salva `price` como `null`, mantem
`available=true` e nao usa o produto como item barato na regra de preco
proximo.

## Testar API

Healthcheck:

```bash
curl http://localhost:8000/health
```

Resposta esperada:

```json
{
  "status": "ok",
  "service": "kouzina-reco-api",
  "version": "0.1.0"
}
```

Documentacao interativa:

```text
http://localhost:8000/docs
```

Recomendacoes com seed ficticio:

```bash
curl "http://localhost:8000/recommendations?product_id=mock-001&widget_id=product-page"
```

Recomendacoes com catalogo oficial importado:

```bash
curl "http://localhost:8000/recommendations?product_id=119&widget_id=product-page"
```

Quando houver produtos importados no banco e o `product_id` existir no catalogo,
a resposta usa o ranking v0 por regras. Se o banco estiver vazio, indisponivel
ou o produto atual nao existir, a API usa fallback mockado para manter o widget
funcionando.

Evento mockado no PowerShell:

```powershell
Invoke-RestMethod -Method Post -Uri http://localhost:8000/events -ContentType "application/json" -Body '{"event_type":"recommendation_click","anonymous_id":"anon_123","session_id":"sess_456","page_url":"http://localhost:5500/demo.html","product_id":"12345","widget_id":"product-page","recommended_product_id":"mock-001","metadata":{}}'
```

Evento mockado com curl:

```bash
curl -X POST http://localhost:8000/events \
  -H "Content-Type: application/json" \
  -d '{"event_type":"recommendation_click","anonymous_id":"anon_123","session_id":"sess_456","page_url":"http://localhost:5500/demo.html","product_id":"12345","widget_id":"product-page","recommended_product_id":"mock-001","metadata":{}}'
```

## Testar widget local

Com a API rodando em `http://localhost:8000`, abra outro terminal:

```bash
cd widget
python -m http.server 5500
```

Depois acesse:

```text
http://localhost:5500/demo.html
```

O widget deve:

- renderizar recomendacoes do catalogo quando o produto existir;
- exibir imagem quando a recomendacao tiver `image_url`;
- manter fallback mockado quando a API ou o catalogo nao estiverem disponiveis;
- enviar `page_view`;
- enviar `recommendation_impression`;
- enviar `recommendation_click` ao clicar em uma recomendacao;
- usar `localStorage` para `anonymous_id`;
- usar `sessionStorage` para `session_id`.

O `widget/demo.html` esta configurado para demonstrar um `product_id` real do
catalogo oficial autorizado (`119`). Se apenas o seed ficticio estiver
importado, a API usa fallback mockado para manter o demo funcional.

## Eventos permitidos

Nesta fase, a API aceita somente:

```text
page_view
product_view
recommendation_impression
recommendation_click
```

Os eventos sao validados, confirmados e salvos em `recommendation_events`
quando o banco esta disponivel.

## Privacidade

O MVP coleta somente dados anonimos e tecnicos:

- `anonymous_id`
- `session_id`
- `event_type`
- `page_url`
- `product_id`
- `widget_id`
- `recommended_product_id`
- `metadata` nao sensivel

Nao coletar nome, CPF, e-mail, telefone, endereco, dados de pagamento ou
conteudo de formularios.

## Recomendador v0

O recomendador v0 pontua candidatos por complementaridade de tipo, disponibilidade,
mesma voltagem, preco proximo, mesma marca, mesmo ambiente e nivel premium
semelhante. O proprio produto visualizado nunca deve ser retornado.

Quando o preco de um produto oficial estiver nulo ou como `Sob consulta`, a
regra de faixa de preco proxima nao pontua. Produtos sob consulta continuam
disponiveis para recomendacao.

Detalhes: `docs/RECOMMENDER.md`.
Qualidade do catalogo oficial: `docs/CATALOG_QUALITY.md`.

## Relatorio de revisao qualitativa

A Fase 4.6 gera um CSV para que a Kouzina revise manualmente se as
recomendacoes do ranking v0 fazem sentido comercial. O relatorio nao usa dados
pessoais e deve ser analisado antes de qualquer etapa de metricas, CTR, fuzzy ou
ontologia.

Com o banco rodando e o catalogo oficial importado:

```powershell
cd backend
python -m app.review_recommendations
```

Arquivo gerado:

```text
reports/recommendation_review.csv
```

Tambem e possivel filtrar por tipo:

```powershell
python -m app.review_recommendations --product-type Churrasqueira --top-k 4
```

Detalhes: `docs/RECOMMENDATION_REVIEW.md`.

## Pacote visual de revisao qualitativa

A Fase 4.7 transforma `reports/recommendation_review.csv` em um HTML local para
facilitar a reuniao com a Kouzina. O HTML e apenas visual: ele nao salva
avaliacoes, nao altera banco, nao altera ranking e nao chama API externa.

Depois de gerar o CSV:

```powershell
cd backend
python -m app.export_review_pack
```

Arquivo gerado:

```text
reports/recommendation_review.html
```

Abra esse arquivo no navegador. Use o HTML para discutir cada recomendacao e
registre o preenchimento oficial em `reviewer_rating` e `reviewer_comment` no
CSV ou em uma planilha copiada.

Filtros uteis:

```powershell
python -m app.export_review_pack --limit 120
python -m app.export_review_pack --min-score 70
python -m app.export_review_pack --product-type Churrasqueira
```

Esta etapa continua antes de CTR, fuzzy, ontologia e deploy.

## Proxima fase

A proxima fase recomendada e usar o pacote HTML em uma reuniao com a Kouzina,
preencher o CSV ou planilha de revisao e usar os comentarios para ajustar
curadoria editorial. Depois disso, medir impressoes, cliques e CTR. Fuzzy,
ontologia, Tray, painel, login e deploy continuam fora ate autorizacao
explicita em fases posteriores.

## Rodar testes

```powershell
cd backend
pytest
```
