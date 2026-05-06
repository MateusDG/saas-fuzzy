# Protocolo De Avaliacao Academica - Fase 5

## Objetivo

Definir um protocolo offline, reproduzivel e auditavel para comparar baselines
do recomendador Kouzina Reco antes de ontologia, fuzzy e modelo hibrido.

Este protocolo prepara a base cientifica do TCC sem alterar o contrato da API
operacional e sem usar dados reais de clientes da Kouzina.

## Escopo Da Fase 5

Nesta fase, o foco e:

- padronizar entrada, processamento e saida da avaliacao offline;
- comparar baselines simples;
- congelar comportamento do ranking v0 atual;
- registrar metricas reproduziveis;
- documentar limites metodologicos.

Nao faz parte da Fase 5:

- ontologia formal;
- motor fuzzy;
- recomendador hibrido;
- validacao online com clientes reais;
- deploy;
- dashboard;
- inferencia causal de conversao.

## Tipos De Validacao

### Validacao Comercial

Avalia impacto de negocio em ambiente real (ex.: CTR, funil, receita assistida).
Depende de integracao com site e dados reais suficientes.

### Validacao Qualitativa

Avalia coerencia de recomendacoes por especialistas via review CSV/HTML.
Gera hipoteses e curadoria, mas nao substitui experimento academico.

### Avaliacao Offline Academica

Compara modelos em dataset publico ou conjunto reproduzivel, com metricas
padronizadas e protocolo fixo de treino/teste.

## Modelos A Comparar Na Fase 5

Baselines implementados nesta fase:

- baseline de popularidade (`app.evaluation_baselines`);
- baseline simples por conteudo/categoria (`app.evaluation_baselines`);
- baseline v0 congelado (snapshot do comportamento atual).

Modelos que ainda nao entram nesta fase:

- ontologia sem fuzzy;
- fuzzy sem ontologia;
- hibrido ontologico-fuzzy.

## Definicao De Top-k

O protocolo deve reportar no minimo:

- `k = 5`
- `k = 10`

Padrao inicial de execucao do script: `k = 10`.

## Definicao De Train/Test Split

Split recomendado (preferencial):

- split temporal por usuario:
  - treino: interacoes anteriores;
  - teste: interacoes mais recentes por usuario.

Fallback quando nao houver timestamp confiavel:

- split estratificado por usuario com semente fixa (`seed` documentado).

Regra minima:

- cada usuario avaliado precisa ter pelo menos 1 item relevante no teste;
- itens de teste nao devem vazar para treino no mesmo usuario.

## Metricas Minimas

Implementadas em `backend/app/evaluation_metrics.py`:

- `Precision@k`
- `Recall@k`
- `nDCG@k`
- cobertura de catalogo (`catalog_coverage`)
- diversidade simples (`simple_diversity`)
- taxa de recomendacoes bloqueadas/rebaixadas por politica
  (`policy_action_rates`)

Observacao:

- `policy_action_rates` depende da presenca opcional de
  `relation_policy_action` no conjunto de avaliacao.

## Formato Esperado De Entrada

### Interacoes De Treino (`interactions_train.csv`)

Colunas minimas:

- `user_id`
- `item_id`
- `event_name`

Colunas recomendadas:

- `timestamp`
- `source_product_type`
- `recommended_product_type`

### Interacoes De Teste (`interactions_test.csv`)

Colunas minimas:

- `user_id`
- `item_id`

Colunas opcionais:

- `relevance` (padrao binario = 1 quando ausente)
- `relation_policy_action`

### Itens (`items.csv`)

Colunas minimas:

- `item_id`
- `category`

Colunas recomendadas:

- `brand`
- `environment`
- `price_band`

## Formato Esperado De Saida

Gerado por `python -m app.run_offline_evaluation`:

- `reports/evaluation/metrics_summary.json`
- `reports/evaluation/per_user_metrics.csv`

Conteudo minimo:

- metricas agregadas por baseline;
- contagens de linhas/usuarios;
- metricas por usuario para auditoria.

## Congelamento Do Baseline v0

O comportamento do ranking v0 deve ser congelado com:

```powershell
cd backend
python -m app.freeze_v0_baseline
```

Saida padrao:

- `reports/baselines/v0_baseline_snapshot.json`

O snapshot inclui:

- configuracao usada no freeze (`limit_products`, `top_k`, filtro);
- recomendacoes geradas por produto de origem;
- metadados de politica de relacoes;
- fingerprint SHA-256 do conteudo.

## Ameaças Iniciais A Validade

- diferenca de dominio entre dataset publico e catalogo Kouzina;
- ruido de eventos implicitos usados como relevancia;
- sensibilidade a split temporal vs aleatorio;
- categoria como sinal simplificado de conteudo;
- ausencia de atributos tecnicos finos em parte dos datasets publicos;
- risco de superestimar baseline por vazamento de dados;
- baixa comparabilidade com comportamento real sem experimento online.

## O Que Nao Sera Concluido Nesta Fase

- prova de ganho ontologico-fuzzy;
- validacao com clientes reais;
- conclusao definitiva de impacto comercial;
- modelagem causal de conversao;
- recomendador final de producao.

## Comandos De Execucao

### Rodar avaliacao offline

```powershell
cd backend
python -m app.run_offline_evaluation --top-k 10
```

### Congelar baseline v0

```powershell
cd backend
python -m app.freeze_v0_baseline --limit-products 30 --top-k 4
```

## Criterio De Aceite Da Fase 5

A fase fica bem encaminhada quando:

- protocolo e dataset selection estiverem documentados;
- scripts offline executarem com CSVs locais preparados;
- baselines de popularidade e categoria estiverem testados;
- snapshot v0 puder ser gerado com fingerprint;
- testes do backend permanecerem verdes.
