# Recomendador v0

## Objetivo

O recomendador v0 cria uma primeira camada de ranking por regras para produtos
da Kouzina importados no PostgreSQL. Ele nao usa fuzzy, ontologia, machine
learning, LLM ou dados pessoais.

A meta desta fase e retornar produtos plausiveis para o widget, com score e
motivo textual, mantendo fallback mockado quando o catalogo nao for suficiente.
Na Fase 4, o CSV seedado passou a conter cerca de 30 produtos ficticios ou
semi-realistas para exercitar melhor essas regras. Na Fase 4.2, o mesmo
recomendador passou a operar tambem sobre catalogo oficial autorizado importado
localmente por CSV. Na Fase 4.5, as relacoes complementares foram ampliadas
com base nos tipos reais do catalogo oficial.

## Como funciona

O endpoint `GET /recommendations` recebe `product_id`, busca o produto atual por
`external_id` e seleciona candidatos ativos da mesma loja. O proprio produto
visualizado e excluido do retorno.

Cada candidato recebe uma pontuacao bruta:

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

A faixa de preco e considerada proxima quando a diferenca relativa entre o preco
do produto atual e o preco do candidato e menor ou igual a 30%. Se algum preco
estiver vazio, nulo, zerado, invalido ou sob consulta, essa regra nao pontua.

## Relacoes complementares

Relacoes comerciais/editoriais iniciais usadas no ranking:

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

Essas relacoes nao sao uma ontologia formal. Elas sao regras editoriais
iniciais para melhorar o comportamento comercial do ranking v0 com o catalogo
real autorizado. O codigo normaliza acentos, caixa e hifens para aceitar
variacoes como `Domino`, `Dominó`, `Micro-ondas` e `Lava-loucas`.

Ambientes como `Cozinha Gourmet` e `Espaco Gourmet` nao sao tratados como
`product_type`. Eles continuam entrando apenas no criterio auxiliar de mesmo
ambiente.

## Reasons

Cada recomendacao retorna uma explicacao curta baseada nas regras disparadas,
por exemplo:

```text
Produto complementar ao item visualizado.
Produto disponivel.
Produto sob consulta.
Mesma voltagem do produto atual.
Faixa de preco proxima.
Mesma marca do produto atual.
Indicado para o mesmo ambiente.
Faixa premium semelhante.
```

## Fallback seguro

A API retorna fallback mockado quando:

- o banco esta vazio ou indisponivel;
- `product_id` nao foi informado;
- o produto atual nao existe no catalogo;
- nao ha candidatos ativos suficientes para recomendar.

Isso preserva o funcionamento do widget e evita quebrar a pagina da loja.

## Catalogo Oficial Autorizado

Quando o banco recebe o arquivo `data/products_kouzina_official.csv`,
o ranking v0 usa os produtos reais autorizados da Kouzina. O algoritmo nao muda
o contrato da API: cada item recomendado continua retornando `product_id`,
`name`, `url`, `image_url`, `price`, `reason` e `score`.

Produtos com `Preco venda = 0.00` sao tratados como `Sob consulta`:

- `price` fica `null`;
- `available` permanece `true`;
- a regra de preco proximo nao e aplicada;
- o reason pode incluir `Produto sob consulta.`;
- o produto nao e penalizado como indisponivel.

## Limitacoes

- O catalogo pode ser seedado para desenvolvimento ou oficial autorizado local.
- Atributos ausentes no CSV oficial reduzem pontuacoes possiveis, por exemplo
  voltagem, imagem, largura e URL quando nao forem exportados.
- Nao ha relacoes manuais persistidas sendo usadas no ranking.
- Nao ha personalizacao por usuario.
- Nao ha calculo de CTR dentro do recomendador.
- O score e uma pontuacao por regras, nao uma probabilidade.
- URL e imagem nao entram na pontuacao; elas sao usadas apenas na resposta da
  API e no widget.
- As relacoes da Fase 4.5 ainda sao curadoria inicial e precisam de validacao
  qualitativa com a Kouzina.
- Fuzzy e ontologia continuam fora desta fase.

## Diferenca para fuzzy futuro

O v0 aplica regras discretas e somas fixas. A versao fuzzy futura deve
transformar criterios como compatibilidade tecnica, afinidade de ambiente,
proximidade de preco, similaridade premium e disponibilidade em graus de
pertinencia.

Fuzzy e ontologia continuam fora desta fase.

## Proximos passos

- Validar qualitativamente as novas relacoes com exemplos reais da Kouzina.
- Usar `manual_product_relations` para ajustes editoriais simples.
- Medir impressoes, cliques e CTR antes de qualquer camada fuzzy.
