# Revisao Qualitativa Das Recomendacoes

## Objetivo

A revisao qualitativa permite avaliar se o recomendador v0 faz sentido
comercialmente antes de qualquer etapa de metricas, CTR, fuzzy ou ontologia.

O processo gera um CSV com produtos de origem, recomendacoes geradas pelo
ranking v0 e campos vazios para avaliacao manual da Kouzina. A Fase 4.7
tambem gera um HTML estatico local para facilitar a reuniao de revisao.

Esta etapa nao usa dados pessoais, pedidos, checkout, pagamentos ou mensagens.
Ela opera somente sobre o catalogo importado e os atributos dos produtos.

## Como Gerar O Relatorio

Com o PostgreSQL rodando e o catalogo oficial importado:

```powershell
cd backend
python -m app.review_recommendations
```

O arquivo padrao gerado e:

```text
reports/recommendation_review.csv
```

Parametros disponiveis:

```powershell
python -m app.review_recommendations --limit-products 30
python -m app.review_recommendations --top-k 4
python -m app.review_recommendations --output reports/recommendation_review.csv
python -m app.review_recommendations --product-type Churrasqueira --top-k 4
```

## Como Gerar O Review Pack HTML

Depois de gerar o CSV, crie o pacote visual:

```powershell
python -m app.export_review_pack
```

Arquivos padrao:

```text
Entrada: reports/recommendation_review.csv
Saida:   reports/recommendation_review.html
```

Parametros disponiveis:

```powershell
python -m app.export_review_pack --input reports/recommendation_review.csv
python -m app.export_review_pack --output reports/recommendation_review.html
python -m app.export_review_pack --limit 120
python -m app.export_review_pack --min-score 70
python -m app.export_review_pack --product-type Churrasqueira
```

Abra localmente no navegador:

```text
reports/recommendation_review.html
```

O HTML nao depende de servidor web, nao altera banco, nao altera ranking, nao
chama API externa e nao baixa imagens. Ele usa somente URLs ja presentes no CSV
e escapa o conteudo textual antes de renderizar.

## Como Usar Na Reuniao

1. Gere `reports/recommendation_review.csv`.
2. Gere `reports/recommendation_review.html`.
3. Abra o HTML em um navegador durante a reuniao com a Kouzina.
4. Discuta cada card visualmente: produto de origem, recomendado, score e
   explicacao.
5. Registre a avaliacao oficial no CSV ou em uma planilha copiada.

O HTML e apenas visual. Ele nao salva `reviewer_rating` nem
`reviewer_comment`.

## Como Preencher

O CSV inclui duas colunas para revisao manual:

- `reviewer_rating`
- `reviewer_comment`

Escala sugerida para `reviewer_rating`:

- `1`: ruim
- `2`: fraca
- `3`: aceitavel
- `4`: boa
- `5`: excelente

Use `reviewer_comment` para registrar o motivo da avaliacao, ajustes desejados
ou produtos que deveriam aparecer antes.

## Perguntas Sugeridas

- Esse produto realmente complementa o produto atual?
- A recomendacao faz sentido comercial?
- Ha algum produto que deveria aparecer antes?
- Produto sob consulta deve ser mostrado nesse contexto?
- A explicacao esta clara?

## Colunas Do CSV

O relatorio inclui:

- dados do produto atual;
- dados do produto recomendado;
- `score`;
- `reason`;
- URLs dos produtos;
- `recommended_image_url`;
- campos vazios para avaliacao manual.

## Limitacoes

- O relatorio e uma amostra, nao uma avaliacao estatistica.
- O HTML da Fase 4.7 e um pacote visual estatico, nao um painel.
- Nao mede CTR, impressao ou clique.
- Nao altera o ranking automaticamente.
- Nao implementa fuzzy ou ontologia.
- A avaliacao manual deve ser usada para decidir proximos ajustes editoriais.
- Esta etapa vem antes de CTR, fuzzy, ontologia e deploy.
