# Qualidade Do Catalogo

Resumo gerado na Fase 4.2 apos importar o arquivo oficial autorizado local
disponivel em `data/products_kouzina_official.csv`.

## Resumo

- Total de produtos importados: 318.
- Produtos com preco informado: 228.
- Produtos sob consulta (`Preco venda = 0.00`): 53.
- Produtos com preco nao informado: 37.
- Produtos com imagem: 0.
- Produtos com voltagem: 228.

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

## Marcas Principais

- Elettromec: 58.
- Franke: 42.
- Tecno: 41.
- Bertazzoni Italia: 39, incluindo normalizacao de `Bert. Ital`.
- Marca vazia: 37.
- Cuisinart: 22.
- Coyote: 21.
- Evol: 20.
- Gorenje: 12.
- Crissair: 11.

## Tipos Inferidos Principais

- Coifa: 52.
- Forno: 48.
- Cooktop: 38.
- Churrasqueira: 31.
- Tipo vazio: 25.
- Adega: 24.
- Refrigerador: 19.
- Micro-ondas: 17.
- Cervejeira: 16.
- Lava-loucas: 14.

## Problemas Encontrados

- O arquivo oficial disponivel nao tem as colunas `Endereco do Produto (URL Tray)`
  e `Imagens adicionais`; por isso `url` usa fallback seguro e `image_url` ficou
  vazio nessa validacao.
- Existem 37 produtos sem categoria e marca preenchidas.
- Existem 37 produtos sem preco informado.
- Existem 90 produtos sem voltagem preenchida.
- Existem 25 produtos cujo tipo nao foi inferido pelas regras atuais.

## Limitacoes

Este resumo descreve qualidade catalogal, nao comportamento de clientes. Nenhum
dado pessoal, pedido, checkout, pagamento ou mensagem foi importado.
