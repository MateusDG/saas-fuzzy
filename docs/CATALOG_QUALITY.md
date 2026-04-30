# Qualidade Do Catalogo

Resumo gerado na Fase 4.4 apos importar o arquivo oficial autorizado local
`data/products_kouzina_official.csv`.

Este relatorio descreve qualidade catalogal. Nao inclui dados pessoais,
pedidos, checkout, pagamento ou mensagens.

## Resumo

- Total de produtos importados: 281.
- Produtos com URL Tray: 281.
- Produtos sem URL Tray: 0.
- Produtos com imagem: 281.
- Produtos sem imagem: 0.
- Produtos com preco informado: 229.
- Produtos sob consulta (`Preco venda = 0.00`): 52.
- Produtos sem preco informado: 0.
- Produtos com voltagem: 229.
- Produtos sem voltagem: 52.
- Produtos com `product_type`: 281.
- Produtos sem `product_type`: 0.
- Produtos com `environment`: 281.
- Produtos sem `environment`: 0.
- Produtos sem categoria preenchida: 0.
- Produtos sem marca preenchida: 0.

## Suporte A URL E Imagens

- O CSV atualizado contem `Endereco do Produto (URL Tray)` e o importador salva
  esse valor em `products.url`.
- O CSV atualizado contem `Imagem principal`, `Imagem 2`, `Imagem 3` e
  `Imagem 4`.
- O sistema usa a primeira URL valida encontrada entre as colunas de imagem.
- As imagens sao armazenadas apenas como URL em `products.image_url`.
- O sistema nao baixa imagens, nao salva arquivo local e nao salva binario.

## Evolucao Da Curadoria

Antes da Fase 4.3:

- Produtos sem `product_type`: 25.
- Produtos sem `environment`: 0.

Depois da Fase 4.3 e com o CSV atualizado da Fase 4.4:

- Produtos sem `product_type`: 0.
- Produtos sem `environment`: 0.

Na Fase 4.5:

- Tipos novos como `Cuba`, `Misturador`, `Queimador`, `Acessorio de Coifa`,
  `Acessorio de Cozinha`, `Gaveta Aquecida`, `Micro-ondas`, `Lava-loucas`,
  `Refrigerador`, `Freezer`, `Cafeteira`, `Forno de Pizza`, `Maquina de Gelo`,
  `Cervejeira`, `Frigobar` e `Rangetop` passaram a ter relacoes
  complementares iniciais no recomendador v0.

## Tipos Inferidos Principais

- Coifa: 50.
- Cooktop: 38.
- Churrasqueira: 29.
- Forno: 26.
- Adega: 19.
- Refrigerador: 18.
- Micro-ondas: 17.
- Lava-loucas: 14.
- Cervejeira: 13.
- Cuba: 9.
- Gaveta Aquecida: 8.
- Queimador: 7.
- Fogao: 5.
- Frigobar: 5.
- Rangetop: 4.
- Misturador: 4.

## Ambientes

- Cozinha Gourmet: 182.
- Espaco Gourmet: 76.
- Refrigeracao: 20.
- Lavanderia: 3.

## Categorias Principais

- Cozinha: 57.
- Coifas: 39.
- Espaco Gourmet: 32.
- Cooktops: 29.
- Fornos: 18.
- Adegas: 15.
- Refrigeracao: 14.
- Lava-loucas: 12.
- Cervejeiras: 11.
- Micro-Ondas: 10.

## Marcas Principais

- Elettromec: 58.
- Franke: 43.
- Tecno: 41.
- Bertazzoni Italia: 39, incluindo normalizacao de `Bert. Ital`.
- Cuisinart: 22.
- Coyote: 21.
- Evol: 20.
- Gorenje: 12.
- Crissair: 11.
- Dinoxx: 6.

## Problemas Restantes

- Existem 52 produtos sem voltagem preenchida.
- Existem 52 produtos sob consulta; eles ficam com `price=null` e nao entram
  na regra de preco proximo.
- As relacoes complementares da Fase 4.5 ainda sao curadoria inicial. Elas
  devem ser revisadas com exemplos comerciais reais e, futuramente, podem ser
  refinadas por relacoes manuais ou metricas de clique.

## Fora De Escopo

Esta curadoria nao implementa fuzzy, ontologia, crawler, scraping, integracao
Tray automatica, painel, login ou deploy.
