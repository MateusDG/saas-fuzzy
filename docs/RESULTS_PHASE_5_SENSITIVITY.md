# Resultados Fase 5.3 - Sensibilidade Metodologica

## Objetivo

Comparar a sensibilidade dos baselines offline (popularidade e conteudo/categoria)
em variacoes controladas de:

1. compra verificada (`require_verified_purchase`);
2. recorte premium por preco (`premium_percentile`).

Escopo desta fase:

- dataset publico Amazon Reviews 2023;
- categoria unica `Appliances`;
- sem fuzzy;
- sem ontologia;
- sem recomendador hibrido;
- sem dados reais de clientes Kouzina.

Premissa metodologica:

- "high-end" continua sendo apenas proxy de produto premium por preco;
- nao representa renda, classe social, intencao consultiva ou perfil real de consumidor.

## Configuracoes Comparadas

- A (`p75_all`): `premium_percentile=0.75`, `require_verified_purchase=false`
- B (`p75_verified`): `premium_percentile=0.75`, `require_verified_purchase=true`
- C (`p90_all`): `premium_percentile=0.90`, `require_verified_purchase=false`
- D (`p90_verified`): `premium_percentile=0.90`, `require_verified_purchase=true` (opcional, executada)

## Tabela Comparativa

| Configuracao | premium_percentile | require_verified_purchase | usuarios avaliados | itens finais | interacoes treino | interacoes teste | itens premium | itens removidos sem preco | itens removidos baixa interacao | itens removidos baixa avaliacao media | usuarios removidos baixa interacao | Precision@5 | Recall@5 | nDCG@5 | Cobertura@5 | Diversidade@5 | Precision@10 | Recall@10 | nDCG@10 | Cobertura@10 | Diversidade@10 |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A (`p75_all`) | 0.75 | false | 6651 | 2798 | 7368 | 6651 | 4916 | 28083 | 15428 | 25880 | 216476 | 0.010164 | 0.050819 | 0.031299 | 0.002502 | 0.000000 | 0.008976 | 0.089761 | 0.043978 | 0.004289 | 0.000000 |
| B (`p75_verified`) | 0.75 | true | 6118 | 2662 | 6655 | 6118 | 4885 | 28083 | 15573 | 25880 | 210007 | 0.010690 | 0.053449 | 0.032967 | 0.002630 | 0.000000 | 0.010069 | 0.100686 | 0.048143 | 0.004508 | 0.000000 |
| C (`p90_all`) | 0.90 | false | 1664 | 842 | 1820 | 1664 | 1960 | 28083 | 15428 | 25880 | 88485 | 0.023317 | 0.116587 | 0.068468 | 0.008314 | 0.000000 | 0.020132 | 0.201322 | 0.096099 | 0.014252 | 0.000000 |
| D (`p90_verified`) | 0.90 | true | 1455 | 766 | 1519 | 1455 | 1977 | 28083 | 15573 | 25880 | 86451 | 0.025842 | 0.129210 | 0.077696 | 0.009138 | 0.000000 | 0.023780 | 0.237801 | 0.112616 | 0.015666 | 0.000000 |

Notas:

- as metricas acima sao de baseline de popularidade;
- baseline conteudo/categoria apresentou os mesmos valores em todas as configuracoes;
- isso ocorre porque o recorte usa categoria unica (`Appliances`).

## Interpretacao

### 1) Efeito de `require_verified_purchase=true`

Com `premium_percentile=0.75`:

- usuarios: 6651 -> 6118 (queda ~8.0%);
- itens: 2798 -> 2662 (queda ~4.9%).

Com `premium_percentile=0.90`:

- usuarios: 1664 -> 1455 (queda ~12.6%);
- itens: 842 -> 766 (queda ~9.0%).

Resumo: exigir compra verificada reduz volume do recorte, mas nao inviabilizou a avaliacao nesta execucao.

### 2) Efeito de `P90` (premium mais restrito)

Sem filtro de compra verificada:

- usuarios: 6651 -> 1664 (queda ~75.0%);
- itens: 2798 -> 842 (queda ~69.9%).

Com compra verificada:

- usuarios: 6118 -> 1455 (queda ~76.2%);
- itens: 2662 -> 766 (queda ~71.2%).

Resumo: `P90` reduz fortemente o catalogo e a base avaliada.

### 3) Variacao das metricas

As metricas agregadas aumentaram nas configuracoes mais restritivas (principalmente `P90`), mas essa melhora nao deve ser interpretada como ganho de modelagem.

Leitura correta nesta fase:

- o espaco de candidatos fica menor;
- o problema fica mais facil;
- Precision/Recall/nDCG podem subir por efeito de recorte, nao por modelo melhor.

### 4) Diversidade zero

`Diversidade@5` e `Diversidade@10` ficaram em `0.000000` em todas as configuracoes.

Isto e esperado no piloto atual porque:

- o recorte foi de categoria unica (`Appliances`);
- a metrica de diversidade simples depende de variacao de categoria.

## Limitacoes

- recorte restrito a uma categoria publica;
- proxy premium por preco nao valida publico high-end real;
- ausencia de validacao online com clientes;
- sem fuzzy, sem ontologia e sem recomendador hibrido nesta fase.

## Artefatos Locais Da Execucao

Foram gerados artefatos locais por configuracao em:

- `reports/evaluation/sensitivity/p75_all/`
- `reports/evaluation/sensitivity/p75_verified/`
- `reports/evaluation/sensitivity/p90_all/`
- `reports/evaluation/sensitivity/p90_verified/`

Esses artefatos estao configurados para permanecer locais (ignorados), com
`docs/RESULTS_PHASE_5_SENSITIVITY.md` como artefato textual principal versionavel.

## Proximos Passos Recomendados

1. Repetir a analise incluindo `Home_and_Kitchen` em execucao separada.
2. Incluir comparacao com snapshot congelado do ranking v0 no protocolo offline.
3. Revisar ameaças a validade antes de iniciar Fase 6.
