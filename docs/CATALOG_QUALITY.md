# Qualidade Do Catalogo

Resumo gerado na Fase 4.3 apos importar o arquivo oficial autorizado local
`data/products_kouzina_official.csv`.

Este relatorio descreve qualidade catalogal. Nao inclui dados pessoais,
pedidos, checkout, pagamento ou mensagens.

## Resumo

- Total de produtos importados: 318.
- Produtos com preco informado: 228.
- Produtos sob consulta (`Preco venda = 0.00`): 53.
- Produtos sem preco informado: 37.
- Produtos com imagem: 0.
- Produtos com voltagem: 228.
- Produtos sem voltagem: 90.
- Produtos com `product_type`: 318.
- Produtos sem `product_type`: 0.
- Produtos com `environment`: 318.
- Produtos sem `environment`: 0.

## Evolucao Da Curadoria

Antes da Fase 4.3:

- Produtos sem `product_type`: 25.
- Produtos sem `environment`: 0.

Depois da Fase 4.3:

- Produtos sem `product_type`: 0.
- Produtos sem `environment`: 0.

## Tipos Inferidos Principais

- Coifa: 52.
- Forno: 47.
- Cooktop: 38.
- Churrasqueira: 31.
- Adega: 24.
- Refrigerador: 19.
- Micro-ondas: 17.
- Cervejeira: 16.
- Lava-loucas: 14.
- Cuba: 9.
- Gaveta Aquecida: 8.
- Fogao: 7.
- Queimador: 7.
- Frigobar: 5.
- Rangetop: 4.
- Misturador: 4.

## Ambientes

- Cozinha Gourmet: 207.
- Espaco Gourmet: 87.
- Refrigeracao: 21.
- Lavanderia: 3.

## Categorias Principais

- Cozinha: 56.
- Coifas: 39.
- Sem categoria preenchida: 37.
- Espaco Gourmet: 32.
- Cooktops: 29.
- Fornos: 18.
- Adegas: 15.
- Refrigeracao: 14.
- Lava-loucas: 12.
- Cervejeiras: 11.
- Micro-Ondas: 10.
- Churrasqueiras: 8.

## Marcas Principais

- Elettromec: 58.
- Franke: 42.
- Tecno: 41.
- Bertazzoni Itália: 39, incluindo normalizacao de `Bert. Ital`.
- Marca vazia: 37.
- Cuisinart: 22.
- Coyote: 21.
- Evol: 20.
- Gorenje: 12.
- Crissair: 11.
- Dinoxx: 6.
- Speed Queen: 3.

## Exemplos Corrigidos

- `1522`: Queimador Lateral -> `product_type=Queimador`,
  `environment=Espaco Gourmet`.
- `2965`: Dispenser de Agua -> `product_type=Dispenser de Água`,
  `environment=Espaco Gourmet`.
- `2483`: Kit Exaustor -> `product_type=Acessório de Coifa`,
  `environment=Cozinha Gourmet`.
- `2749`: Cafeteira -> `product_type=Cafeteira`,
  `environment=Cozinha Gourmet`.
- `527`: Cuba -> `product_type=Cuba`, `environment=Cozinha Gourmet`.
- `3231`: Misturador -> `product_type=Misturador`,
  `environment=Cozinha Gourmet`.
- `02.19.0339090`: Set Azeite & Vinagre ->
  `product_type=Acessório de Cozinha`, `environment=Cozinha Gourmet`.

## Problemas Restantes

- O arquivo oficial disponivel nao tem as colunas `Endereco do Produto (URL Tray)`
  e `Imagens adicionais`; por isso `url` usa fallback seguro e `image_url` ficou
  vazio nesta validacao.
- Existem 37 produtos sem categoria preenchida.
- Existem 37 produtos sem marca preenchida.
- Existem 37 produtos sem preco informado.
- Existem 90 produtos sem voltagem preenchida.
- Alguns tipos novos, como `Cuba`, `Misturador`, `Queimador` e
  `Acessório de Coifa`, ainda nao possuem relacoes complementares especificas
  no recomendador v0.

## Fora De Escopo

Esta curadoria nao implementa fuzzy, ontologia, crawler, scraping, integracao
Tray automatica, painel, login ou deploy.
