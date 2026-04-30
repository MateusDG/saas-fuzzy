# Recomendador v0

## Objetivo

O recomendador v0 cria uma primeira camada de ranking por regras para produtos
da Kouzina importados no PostgreSQL. Ele nao usa fuzzy, ontologia, machine
learning, LLM ou dados pessoais.

A meta desta fase e retornar produtos plausiveis para o widget, com score e
motivo textual, mantendo fallback mockado quando o catalogo nao for suficiente.

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
estiver vazio, zerado ou invalido, essa regra nao pontua.

## Relacoes complementares

Relacoes iniciais usadas no ranking:

```text
Coifa -> Cooktop, Forno, Domino
Cooktop -> Coifa, Forno, Domino
Adega -> Cervejeira, Frigobar, Churrasqueira
Churrasqueira -> Adega, Cervejeira, Coifa, Cooktop
Forno -> Cooktop, Coifa
```

O codigo normaliza acentos e caixa para aceitar `Domino` e a forma acentuada no
catalogo.

## Reasons

Cada recomendacao retorna uma explicacao curta baseada nas regras disparadas,
por exemplo:

```text
Produto complementar ao item visualizado.
Produto disponivel.
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

## Limitacoes

- O catalogo atual ainda e pequeno.
- Nao ha relacoes manuais persistidas sendo usadas no ranking.
- Nao ha personalizacao por usuario.
- Nao ha calculo de CTR dentro do recomendador.
- O score e uma pontuacao por regras, nao uma probabilidade.

## Diferenca para fuzzy futuro

O v0 aplica regras discretas e somas fixas. A versao fuzzy futura deve
transformar criterios como compatibilidade tecnica, afinidade de ambiente,
proximidade de preco, similaridade premium e disponibilidade em graus de
pertinencia.

Fuzzy e ontologia continuam fora desta fase.

## Proximos passos

- Ampliar `data/products_seed.csv` para 30 a 50 produtos reais ou semi-reais.
- Revisar pesos com exemplos reais da Kouzina.
- Usar `manual_product_relations` para ajustes editoriais simples.
- Medir impressoes, cliques e CTR antes de qualquer camada fuzzy.
