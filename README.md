# Kouzina Reco MVP

MVP comercial minimo de recomendacao para o site Kouzina Club.

Este repositorio implementa a base local das Fases 1, 2, 3, 4, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.9 e inicio da Fase 5:

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
- Politica provisoria de relacoes derivada da revisao dos agentes.
- Guardrails editoriais no ranking v0 para reduzir falsos positivos.
- Enriquecimento do review CSV/HTML com campos de politica provisoria.
- Preparacao de telemetria para analise futura de funil com dados reais.
- Protocolo inicial de avaliacao academica offline (Fase 5).
- Baselines offline de popularidade e conteudo/categoria (Fase 5).
- Congelamento do ranking v0 em snapshot com fingerprint (Fase 5).

Fora de escopo: fuzzy, ontologia, integracao Tray, painel, login, deploy,
ranking sofisticado, crawler, scraping e multi-loja completo.

## Fase 4.9

A Fase 4.9 trata as conclusoes da Fase 4.8 como hipoteses especialistas
provisorias. Nesta fase:

- nao houve validacao humana final com Kouzina;
- nao houve analise de comportamento real de clientes;
- nao existem conclusoes de funil, CTR ou conversao reais;
- o objetivo e preparar o baseline para coletar dados uteis no futuro.

Documentos da fase:

- `docs/PHASE_4_9_RELATION_POLICY_AND_TELEMETRY_PREP.md`
- `docs/RELATION_HYPOTHESES_PHASE_4_9.md`
- `docs/FUTURE_FUNNEL_ANALYTICS_PLAN.md`

## Fase 5

A Fase 5 cria a base academica reproduzivel do projeto, ainda sem ontologia e
sem fuzzy:

- protocolo de avaliacao offline;
- selecao e governanca de dataset publico;
- scripts de baseline simples;
- congelamento do comportamento do ranking v0.

Documentos da fase:

- `docs/EVALUATION_PROTOCOL.md`
- `docs/DATASET_SELECTION.md`
- `data/public/README.md`

## Estrutura

```text
backend/
  app/
    __init__.py
    evaluation_baselines.py
    evaluation_metrics.py
    freeze_v0_baseline.py
    main.py
    database.py
    export_review_pack.py
    models.py
    recommender.py
    review_recommendations.py
    run_offline_evaluation.py
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
  public/
    raw/
    processed/
    README.md
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

Eventos atuais de MVP:

```text
page_view
product_view
recommendation_impression
recommendation_click
```

Eventos preparados para funil futuro (sem analise nesta fase):

```text
widget_opened
product_context_loaded
recommendations_requested
recommendations_rendered
recommendation_expanded
recommendation_dismissed
quote_requested
add_to_cart_clicked
alternative_requested
session_ended
```

Os eventos sao validados, confirmados e salvos em `recommendation_events`.
A analise desses eventos continua pendente ate integracao real do widget/API ao
site e volume suficiente de sessoes reais.

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
semelhante, com guardrails editoriais provisorios da Fase 4.9. O proprio
produto visualizado nunca deve ser retornado.

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

## Proximas fases

Sem reuniao humana nesta etapa, a validacao real fica para quando houver
integracao de widget/API ao site e eventos reais suficientes.

Sequencia planejada:

1. consolidar telemetria real em producao controlada;
2. analisar funil com dados reais anonimos;
3. ajustar curadoria por comportamento observado;
4. preparar fase academica de baseline reproducivel (Fase 5);
5. evoluir para ontologia minima (Fase 6);
6. evoluir para fuzzy (Fase 7).

Detalhes:

- `docs/RELATION_POLICY.md`
- `docs/RECOMMENDATION_REVIEW.md`
- `docs/FUTURE_FUNNEL_ANALYTICS_PLAN.md`
- `docs/EVALUATION_PROTOCOL.md`
- `docs/DATASET_SELECTION.md`

## Rodar avaliacao offline (Fase 5)

Com os CSVs preparados em `data/public/processed/`:

```powershell
cd backend
python -m app.run_offline_evaluation --top-k 10
```

Saidas padrao:

- `reports/evaluation/metrics_summary.json`
- `reports/evaluation/per_user_metrics.csv`

## Congelar baseline v0 (Fase 5)

```powershell
cd backend
python -m app.freeze_v0_baseline --limit-products 30 --top-k 4
```

Saida padrao:

- `reports/baselines/v0_baseline_snapshot.json`

## Rodar testes

```powershell
cd backend
pytest
```
