# Modelo De Dados

Na Fase 2, a API conecta ao PostgreSQL usando `DATABASE_URL`, cria tabelas no
startup do MVP e permite importar produtos por CSV. Na Fase 4, o CSV ficticio
foi ampliado para cerca de 30 produtos seedados de desenvolvimento. Na Fase
4.2, o importador passou a aceitar tambem o catalogo oficial autorizado da
Kouzina em arquivo local.

## Dados Mockados

O arquivo `data/products_seed.csv` contem cerca de 30 produtos mockados ou
semi-realistas para desenvolvimento. Eles sao ficticios/coerentes com o nicho e
nao devem ser tratados como catalogo oficial coletado do site da Kouzina.

Colunas:

```text
external_id
name
url
image_url
category
subcategory
brand
price
available
availability_text
voltage
width_cm
installation_type
product_type
environment
premium_level
```

## Catalogo Oficial Autorizado

O arquivo oficial local esperado e:

```text
data/products_kouzina_official.csv
```

Ele deve estar em UTF-8 com BOM e usar separador `;`. Esse arquivo e ignorado
pelo Git porque contem um snapshot autorizado do catalogo real da Kouzina. Nao
deve ser commitado sem decisao explicita.

O importador detecta automaticamente o formato:

- se existir `external_id`, usa o formato interno;
- se existir `Nome produto`, usa o formato de exportacao oficial Kouzina.

Mapeamento principal da exportacao oficial:

- `Referencia` -> `external_id`; se vazia, gera `kouzina-auto-<numero-da-linha>`;
- `Nome produto` -> `name`;
- `Endereco do Produto (URL Tray)` -> `url`;
- `Imagens adicionais` -> `image_url`, usando a primeira URL;
- `Marca` -> `brand`;
- `Preco venda` -> `price`;
- `Nome categoria` -> `category` e `subcategory`;
- `Caracteristica: Voltagem` -> `voltage`.

Campos sem coluna direta sao inferidos:

- `width_cm` por padroes no nome, como `60cm` ou `90 cm`;
- `installation_type` por termos como `Embutir`, `Built-in`, `Ilha`,
  `Parede` e `Domino`;
- `product_type` por categoria e nome;
- `environment` por tipo, categoria e nome;
- `premium_level` por faixa de preco.

Regra comercial de preco:

- `Preco venda > 0`: salva `price`, `available=true` e
  `availability_text="Preco informado"`;
- `Preco venda = 0.00`: salva `price=null`, `available=true` e
  `availability_text="Sob consulta"`;
- `Preco venda` vazio: salva `price=null`, `available=true` e
  `availability_text="Preco nao informado"`.

## Tabelas Implementadas

### `stores`

Representa a loja. A Fase 2 cria uma loja padrao `kouzina`.

Campos principais:

- `id`;
- `slug`;
- `name`;
- `domain`;
- `public_key`;
- `created_at`.

### `products`

Representa produtos importados de `data/products_seed.csv` ou do catalogo
oficial autorizado local.

Campos principais:

- `store_id`;
- `external_id`;
- `name`;
- `url`;
- `image_url`;
- `category`;
- `subcategory`;
- `brand`;
- `price`;
- `available`;
- `availability_text`;
- `voltage`;
- `width_cm`;
- `installation_type`;
- `product_type`;
- `environment`;
- `premium_level`;
- `active`;
- `created_at`;
- `updated_at`.

Existe restricao unica por `store_id` e `external_id` para evitar duplicacao no
seed.

### `recommendation_events`

Representa eventos anonimos enviados pelo widget.

Campos principais:

- `event_type`;
- `anonymous_id`;
- `session_id`;
- `page_url`;
- `product_external_id`;
- `widget_id`;
- `recommended_product_external_id`;
- `metadata`;
- `created_at`.

### `manual_product_relations`

Tabela simples criada para relacoes manuais futuras entre produtos. A Fase 2
apenas cria a estrutura; ainda nao usa essa tabela no recomendador.

## Eventos

Na Fase 2, eventos sao recebidos, validados e salvos quando o banco esta
disponivel.

## Catalogo Seedado

O catalogo seedado cobre tipos usados pelo ranking v0:

- Coifa;
- Cooktop;
- Forno;
- Adega;
- Churrasqueira;
- Cervejeira;
- Frigobar;
- Domino.

Tambem inclui variacoes de marca, preco, voltagem, largura, instalacao,
ambiente, nivel premium e disponibilidade para validar as regras do
recomendador.

## Limitacoes Do Catalogo Oficial Local

- Alguns atributos continuam inferidos a partir do nome e da categoria.
- Alguns produtos podem nao ter imagem no arquivo exportado.
- Alguns produtos podem nao ter voltagem preenchida.
- Produtos `Sob consulta` nao devem ser tratados como baratos, pois `price`
  fica nulo.
- O suporte atual e importacao local autorizada por CSV; nao ha integracao Tray
  automatica nesta fase.
