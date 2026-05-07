# Resultados Fase 5.4 - Sensibilidade Metodologica

## Objetivo

Comparar a sensibilidade dos baselines offline em variacoes controladas do
recorte Amazon Reviews 2023 / `Appliances`, sem fuzzy, sem ontologia e sem
recomendador hibrido.

Variaveis avaliadas:

- compra verificada (`require_verified_purchase`);
- percentil premium (`premium_percentile`);
- volume de usuarios, itens e interacoes;
- impacto nas metricas top-k.

## Premissa Metodologica

"High-end" continua sendo apenas proxy de produto premium por preco. O recorte
nao representa renda, classe social, intencao consultiva, publico high-end real
ou comportamento de clientes Kouzina.

Esta analise usa dataset publico offline. Nao ha dado real de cliente, CTR real
ou conversao real nesta fase.

## Execucao

- Data da reexecucao: 2026-05-07
- Dataset: Amazon Reviews 2023
- Categoria: `Appliances`
- Interacao positiva: `rating >= 4`
- Filtro de qualidade: `average_rating >= 4.0`
- Suporte minimo: `rating_number >= 20` ou equivalente disponivel
- Split: temporal por usuario, ultima interacao positiva no teste
- `min_user_interactions`: `2`
- `seed`: `42`

## Configuracoes Comparadas

- A (`p75_all`): `premium_percentile=0.75`, `require_verified_purchase=false`
- B (`p75_verified`): `premium_percentile=0.75`, `require_verified_purchase=true`
- C (`p90_all`): `premium_percentile=0.90`, `require_verified_purchase=false`
- D (`p90_verified`): `premium_percentile=0.90`, `require_verified_purchase=true`

A configuracao D foi executada porque o volume final permaneceu suficiente:
`1455` usuarios avaliados e `766` itens finais.

## Tabela Comparativa

Metricas abaixo referem-se ao baseline de popularidade. O baseline
conteudo/categoria teve os mesmos valores em todas as configuracoes porque o
recorte usa uma unica categoria (`Appliances`).

| Configuracao | premium_percentile | require_verified_purchase | usuarios avaliados | itens finais | interacoes treino | interacoes teste | itens premium | itens removidos sem preco | itens removidos baixa interacao | itens removidos baixa avaliacao media | usuarios removidos baixa interacao | Precision@5 | Recall@5 | nDCG@5 | Cobertura@5 | Diversidade@5 | Precision@10 | Recall@10 | nDCG@10 | Cobertura@10 | Diversidade@10 |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A (`p75_all`) | 0.75 | false | 6651 | 2798 | 7368 | 6651 | 4916 | 28083 | 15428 | 25880 | 216476 | 0.010164 | 0.050819 | 0.031299 | 0.002502 | 0.000000 | 0.008976 | 0.089761 | 0.043978 | 0.004289 | 0.000000 |
| B (`p75_verified`) | 0.75 | true | 6118 | 2662 | 6655 | 6118 | 4885 | 28083 | 15573 | 25880 | 210007 | 0.010690 | 0.053449 | 0.032967 | 0.002630 | 0.000000 | 0.010069 | 0.100686 | 0.048143 | 0.004508 | 0.000000 |
| C (`p90_all`) | 0.90 | false | 1664 | 842 | 1820 | 1664 | 1960 | 28083 | 15428 | 25880 | 88485 | 0.023317 | 0.116587 | 0.068468 | 0.008314 | 0.000000 | 0.020132 | 0.201322 | 0.096099 | 0.014252 | 0.000000 |
| D (`p90_verified`) | 0.90 | true | 1455 | 766 | 1519 | 1455 | 1977 | 28083 | 15573 | 25880 | 86451 | 0.025842 | 0.129210 | 0.077696 | 0.009138 | 0.000000 | 0.023780 | 0.237801 | 0.112616 | 0.015666 | 0.000000 |

## Interpretacao

### Compra Verificada

Com `premium_percentile=0.75`, exigir compra verificada reduziu:

- usuarios: `6651 -> 6118` (queda aproximada de 8.0%);
- itens: `2798 -> 2662` (queda aproximada de 4.9%).

Com `premium_percentile=0.90`, exigir compra verificada reduziu:

- usuarios: `1664 -> 1455` (queda aproximada de 12.6%);
- itens: `842 -> 766` (queda aproximada de 9.0%).

Leitura: `require_verified_purchase=true` reduz o volume, mas nao inviabiliza
o benchmark neste recorte.

### Premium Mais Restrito

Sem filtro de compra verificada, trocar P75 por P90 reduziu:

- usuarios: `6651 -> 1664` (queda aproximada de 75.0%);
- itens: `2798 -> 842` (queda aproximada de 69.9%).

Com compra verificada, trocar P75 por P90 reduziu:

- usuarios: `6118 -> 1455` (queda aproximada de 76.2%);
- itens: `2662 -> 766` (queda aproximada de 71.2%).

Leitura: P90 torna o recorte muito mais restrito e altera fortemente o tamanho
do problema.

### Metricas Top-k

As metricas aumentam nas configuracoes mais restritivas, principalmente P90.
Isso nao deve ser interpretado como ganho de modelo.

Leitura correta nesta fase:

- o espaco de candidatos diminui;
- a base avaliada fica mais concentrada;
- Precision, Recall e nDCG podem subir por efeito do recorte.

### Diversidade

`Diversidade@5` e `Diversidade@10` ficaram em `0.000000` em todas as
configuracoes.

Isso e esperado porque:

- o piloto usa uma unica categoria (`Appliances`);
- a metrica simples de diversidade depende de variacao de categoria.

### Conteudo/Categoria

O baseline conteudo/categoria ficou igual ao de popularidade em todas as
configuracoes. Neste recorte, todos os itens pertencem a `Appliances`, entao o
sinal de categoria nao cria ordenacao adicional relevante.

## Artefatos Locais

Artefatos locais gerados por configuracao:

- `data/public/processed/sensitivity/p75_all/`
- `data/public/processed/sensitivity/p75_verified/`
- `data/public/processed/sensitivity/p90_all/`
- `data/public/processed/sensitivity/p90_verified/`
- `reports/evaluation/sensitivity/p75_all/`
- `reports/evaluation/sensitivity/p75_verified/`
- `reports/evaluation/sensitivity/p90_all/`
- `reports/evaluation/sensitivity/p90_verified/`

Esses arquivos permanecem locais e ignorados pelo Git. O artefato versionavel
principal desta fase e este documento.

## Limitacoes

- recorte restrito a `Appliances`;
- proxy premium por preco nao valida publico high-end real;
- dataset publico Amazon nao representa o catalogo Kouzina;
- sem validacao online, sem CTR real e sem conversao real;
- sem fuzzy, sem ontologia e sem recomendador hibrido.

## Proximos Passos

1. Repetir a analise com `Home_and_Kitchen` em fase separada, sem misturar
   conclusoes com `Appliances`.
2. Comparar posteriormente com o snapshot congelado do ranking v0 dentro do
   protocolo offline.
3. Revisar ameacas a validade antes de iniciar Fase 6.
