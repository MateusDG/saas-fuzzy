# Roadmap Das Proximas Fases

## Contexto Atual

O projeto Kouzina Reco esta no estado pos-Fase 4.9.

O sistema atual entrega:

- API FastAPI com `GET /health`, `POST /events` e `GET /recommendations`;
- persistencia de produtos e eventos em PostgreSQL;
- importacao local de catalogo autorizado da Kouzina via CSV;
- widget JavaScript puro e demo local;
- ranking v0 por regras comerciais explicaveis;
- politica provisoria de relacoes em CSV;
- guardrails editoriais para reduzir falsos positivos;
- review pack CSV/HTML para auditoria qualitativa;
- estrutura de eventos preparada para analise futura.

O sistema atual ainda nao entrega:

- ontologia formal;
- motor fuzzy;
- recomendador hibrido final;
- avaliacao academica com dataset publico;
- comparacao experimental entre baselines;
- analise real de comportamento de clientes;
- validacao humana final com a Kouzina;
- deploy ou integracao real com site em producao.

## Alinhamento Com A Proposta Do TCC

A proposta do TCC tem como tema:

```text
Sistema de Recomendacao Baseado em Ontologias Fuzzy para Comercio Eletronico
```

O projeto nao fugiu do tema, mas ainda esta em uma etapa anterior ao nucleo
academico. O estado atual deve ser tratado como baseline operacional e
infraestrutura de apoio para chegar ao objetivo final.

O TCC so estara plenamente aderente quando houver:

- modelagem de ontologia do dominio de produtos;
- representacao gradual de preferencias e compatibilidades;
- motor fuzzy implementado;
- ranking hibrido comparavel ao baseline v0;
- avaliacao com metricas;
- dataset publico ou protocolo experimental reproduzivel;
- analise critica dos resultados.

## Principios Para As Proximas Fases

- Nao tratar hipoteses de agentes como validacao definitiva.
- Nao inventar dados de clientes.
- Nao simular CTR, conversao, funil ou receita como se fossem reais.
- Nao coletar PII.
- Nao usar dados de cliente sem autorizacao e base legal.
- Nao implementar fuzzy antes de definir protocolo de avaliacao.
- Nao formalizar ontologia sobre relacoes fracas sem curadoria.
- Manter o ranking v0 como baseline explicavel.
- Separar claramente produto comercial, experimento academico e validacao real.

## Visao Geral Das Fases

| Fase | Nome | Objetivo Principal | Resultado Esperado |
| --- | --- | --- | --- |
| 5 | Baseline academico e protocolo de avaliacao | Preparar experimento reproduzivel | Dataset, metricas e baselines definidos |
| 6 | Ontologia minima do dominio | Formalizar conhecimento semantico | Ontologia v1 e mapeamento catalogo-ontologia |
| 7 | Motor fuzzy v1 | Modelar gradualidade | `fuzzy_score` e explicacoes por regra |
| 8 | Recomendador hibrido | Combinar v0, ontologia e fuzzy | Ranking hibrido comparavel |
| 9 | Avaliacao experimental | Comparar modelos | Resultados, tabelas e analise critica |
| 10 | Telemetria real futura | Validar comportamento real | Eventos reais anonimos e analise posterior |
| 11 | Escrita e defesa | Consolidar TCC | Texto final, apendices e apresentacao |

## Fase 5 - Baseline Academico E Protocolo De Avaliacao

### Objetivo

Transformar o projeto atual em um experimento academico reproduzivel.

Antes de implementar ontologia ou fuzzy, esta fase deve definir como o sistema
sera avaliado e contra quais baselines ele sera comparado.

### Entregaveis

- `docs/EVALUATION_PROTOCOL.md`
- `docs/DATASET_SELECTION.md`
- `data/public/README.md`
- scripts ou notebooks para preparar dataset publico
- baseline de popularidade
- baseline por categoria/conteudo
- baseline v0 atual congelado

### Tarefas

1. Escolher dataset publico de e-commerce.
2. Documentar criterios de selecao do dataset.
3. Definir recorte minimo do dominio.
4. Definir train/test split.
5. Definir metricas offline.
6. Implementar baseline de popularidade.
7. Implementar baseline por similaridade de conteudo.
8. Congelar comportamento do v0 atual.
9. Criar protocolo de comparacao.

### Metricas Minimas

- `Precision@k`
- `Recall@k`
- `nDCG@k`
- cobertura de catalogo
- diversidade simples
- taxa de recomendacoes bloqueadas/rebaixadas por politica

### Fora De Escopo

- fuzzy;
- ontologia;
- deploy;
- dashboard;
- analise de cliente real.

### Criterio De Aceite

A Fase 5 termina quando for possivel rodar um experimento offline basico e
comparar pelo menos tres baselines:

- popularidade;
- conteudo simples;
- ranking v0.

## Fase 6 - Ontologia Minima Do Dominio

### Objetivo

Formalizar o conhecimento de dominio que hoje esta espalhado entre
`product_type`, `environment`, politica de relacoes e regras comerciais.

### Entregaveis

- `docs/ONTOLOGY.md`
- `ontology/kouzina_core.owl` ou estrutura equivalente
- `data/ontology_mapping_seed.csv`
- `backend/app/ontology_mapper.py`
- testes de mapeamento catalogo-ontologia

### Escopo Da Ontologia V1

Classes iniciais:

- `Produto`
- `Cooktop`
- `Coifa`
- `Forno`
- `Cuba`
- `Misturador`
- `Adega`
- `Cervejeira`
- `Frigobar`
- `Churrasqueira`
- `LavaLoucas`
- `Lavadora`
- `Secadora`
- `Ambiente`
- `CozinhaGourmet`
- `EspacoGourmet`
- `Lavanderia`
- `Refrigeracao`
- `AtributoTecnico`

Relacoes iniciais:

- `complementa`
- `substitui`
- `pertenceAoAmbiente`
- `temMarca`
- `temVoltagem`
- `temTipoInstalacao`
- `temFaixaPreco`
- `requerCompatibilidadeTecnica`
- `temPoliticaDeConsulta`

### Tarefas

1. Definir questoes de competencia da ontologia.
2. Criar taxonomia minima de produtos.
3. Mapear `product_type` para classes.
4. Mapear `environment` para classes de ambiente.
5. Mapear politica de relacoes para propriedades.
6. Separar relacoes universais de relacoes editoriais.
7. Criar validacao de consistencia simples.
8. Documentar limites da ontologia v1.

### Questoes De Competencia

- Quais produtos complementam funcionalmente um produto atual?
- Quais relacoes dependem de contexto de projeto?
- Quais relacoes pertencem ao dominio high-end de cozinha/gourmet?
- Quais produtos exigem cautela tecnica?
- Quais itens `Sob consulta` precisam de justificativa consultiva?

### Fora De Escopo

- ontologia grande;
- raciocinador complexo em runtime;
- personalizacao por usuario;
- fuzzy;
- integracao com site.

### Criterio De Aceite

A Fase 6 termina quando uma amostra do catalogo puder ser mapeada para classes
e relacoes semanticamente documentadas, sem alterar o contrato da API.

## Fase 7 - Motor Fuzzy V1

### Objetivo

Implementar uma primeira camada fuzzy simples e explicavel para representar
compatibilidade gradual.

O fuzzy deve entrar depois da ontologia minima porque as variaveis precisam de
significado semantico estavel.

### Entregaveis

- `docs/FUZZY_MODEL.md`
- `backend/app/fuzzy_engine.py`
- `backend/tests/test_fuzzy_engine.py`
- exemplos de entrada e saida
- explicacoes por variavel fuzzy

### Variaveis Fuzzy Iniciais

- `compatibilidade_tecnica`
- `afinidade_ambiente`
- `proximidade_preco`
- `similaridade_premium`
- `forca_relacao`
- `disponibilidade`
- `aceitabilidade_sob_consulta`

### Formula Inicial Sugerida

```text
fuzzy_score =
  0.30 * compatibilidade_tecnica +
  0.20 * forca_relacao +
  0.15 * afinidade_ambiente +
  0.15 * proximidade_preco +
  0.10 * disponibilidade +
  0.10 * aceitabilidade_sob_consulta
```

### Tarefas

1. Definir dominios de cada variavel.
2. Criar funcoes de pertinencia simples.
3. Implementar calculo fuzzy puro em Python.
4. Gerar explicacao textual das variaveis disparadas.
5. Testar casos fortes, contextuais, fracos e proibidos.
6. Comparar `fuzzy_score` com score v0 em amostra pequena.

### Fora De Escopo

- personalizacao complexa;
- deep learning;
- LLM no ranking;
- alteracao agressiva do widget;
- avaliacao online com clientes.

### Criterio De Aceite

A Fase 7 termina quando o motor fuzzy retorna score numerico, explicacao e
detalhamento das variaveis para pares de produtos conhecidos.

## Fase 8 - Recomendador Hibrido

### Objetivo

Combinar o baseline v0, a ontologia minima e o motor fuzzy em um ranking
hibrido explicavel.

### Entregaveis

- `backend/app/hybrid_recommender.py`
- `docs/HYBRID_RECOMMENDER.md`
- testes de comparacao v0 vs hibrido
- logs estruturados de explicacao

### Estrategia Inicial

O ranking hibrido deve manter a simplicidade operacional:

```text
hybrid_score =
  alpha * normalized_v0_score +
  beta * ontology_relation_score +
  gamma * fuzzy_score
```

Pesos iniciais sugeridos:

```text
alpha = 0.30
beta = 0.30
gamma = 0.40
```

Esses pesos nao devem ser tratados como resultado cientifico. Eles sao ponto
inicial para avaliacao.

### Tarefas

1. Normalizar score v0.
2. Criar score semantico baseado na ontologia.
3. Integrar `fuzzy_score`.
4. Preservar bloqueios de relacoes proibidas.
5. Preservar cautela para `Sob consulta`.
6. Gerar explicacao combinada.
7. Comparar ranking hibrido com v0.

### Criterio De Aceite

A Fase 8 termina quando o endpoint ou um modo experimental consegue gerar
recomendacoes hibridas sem quebrar o contrato existente da API.

## Fase 9 - Avaliacao Experimental

### Objetivo

Executar a comparacao academica entre modelos.

Esta fase deve responder se a camada ontologico-fuzzy melhora ou nao o
baseline atual.

### Modelos A Comparar

- popularidade;
- conteudo simples;
- ranking v0;
- ontologia sem fuzzy;
- fuzzy sem ontologia formal;
- hibrido ontologico-fuzzy.

### Entregaveis

- `docs/RESULTS.md`
- `docs/THREATS_TO_VALIDITY.md`
- notebooks ou scripts de avaliacao
- tabelas de metricas
- analise de ablation

### Perguntas De Pesquisa

- O hibrido melhora `Precision@k` em relacao ao v0?
- O hibrido melhora `nDCG@k` em relacao a baselines simples?
- A ontologia melhora cobertura e explicabilidade?
- O fuzzy reduz falsos positivos por marca/preco/ambiente?
- Produtos `Sob consulta` sao melhor controlados com fuzzy?
- Quais relacoes devem ser mantidas, rebaixadas ou removidas?

### Criterio De Aceite

A Fase 9 termina quando houver resultados reproduziveis, com tabelas,
interpretacao e limites metodologicos claros.

## Fase 10 - Telemetria Real Futura

### Objetivo

Validar comportamento real somente quando houver integracao controlada com o
site/widget e eventos suficientes.

Esta fase nao substitui a avaliacao academica offline; ela complementa a
validacao comercial.

### Eventos Relevantes

- `recommendation_impression`
- `recommendation_click`
- `recommendation_expanded`
- `recommendation_dismissed`
- `quote_requested`
- `add_to_cart_clicked`
- `alternative_requested`
- `session_ended`

### Metricas Futuras

- `impression_rate`
- `click_through_rate`
- `quote_request_rate`
- `add_to_cart_rate`
- `dismiss_rate`
- performance por `relation_class`
- performance por `relation_type`
- performance por posicao no carousel
- aceitacao de itens `Sob consulta`

### Regras

- usar somente sessoes anonimas;
- nao exigir login;
- nao coletar nome, email, telefone, CPF ou endereco;
- nao inferir conversao sem dado real;
- nao publicar conclusao com amostra insuficiente.

### Criterio De Aceite

A Fase 10 termina quando houver dados reais suficientes para uma analise
descritiva honesta, sem extrapolar causalidade.

## Fase 11 - Escrita Final Do TCC

### Objetivo

Consolidar o trabalho como pesquisa academica, nao apenas como MVP comercial.

### Estrutura Sugerida

1. Introducao
2. Problema e motivacao
3. Fundamentacao teorica
4. Trabalhos relacionados
5. Metodologia
6. Arquitetura do sistema
7. Ontologia proposta
8. Modelo fuzzy
9. Implementacao
10. Experimentos e resultados
11. Discussao
12. Ameacas a validade
13. Conclusao
14. Trabalhos futuros

### Pontos Que Devem Ficar Claros

- O v0 e baseline, nao contribuicao final.
- A reuniao simulada de agentes gerou hipoteses, nao validacao final.
- A Kouzina serve como dominio realista, nao como unica prova cientifica.
- A avaliacao principal precisa ser reproduzivel.
- O ganho do fuzzy deve ser medido, nao presumido.
- Se o hibrido nao superar algum baseline, isso deve ser discutido com rigor.

## Ordem Recomendada De Execucao

1. Criar `docs/EVALUATION_PROTOCOL.md`.
2. Escolher e documentar dataset publico.
3. Implementar baselines offline.
4. Congelar resultado do v0.
5. Criar ontologia minima.
6. Mapear catalogo para ontologia.
7. Implementar fuzzy v1.
8. Integrar ranking hibrido.
9. Rodar comparacao experimental.
10. Escrever resultados e limites.
11. Preparar validacao real futura, se houver tempo e autorizacao.

## Riscos Principais

| Risco | Impacto | Mitigacao |
| --- | --- | --- |
| Projeto ficar apenas no MVP comercial | Alto | Priorizar Fases 5 a 9 |
| Ontologia ficar grande demais | Alto | Escopo minimo e questoes de competencia |
| Fuzzy ser implementado sem avaliacao | Alto | Definir protocolo antes do motor fuzzy |
| Dataset publico nao encaixar no dominio | Medio | Documentar adaptacao e limites |
| Hibrido nao superar baseline | Medio | Fazer ablation e discutir trade-offs |
| Dados reais insuficientes | Medio | Separar validacao online de avaliacao academica |
| Uso indevido de dados pessoais | Alto | Manter LGPD e anonimato como regra |

## Definicao De Pronto Do TCC

O projeto pode ser considerado pronto para defesa quando entregar:

- baseline v0 documentado;
- dataset e protocolo reproduziveis;
- ontologia minima;
- motor fuzzy v1;
- recomendador hibrido;
- comparacao com baselines;
- metricas e resultados;
- discussao critica;
- codigo e documentos suficientes para reproducao.

## Proximo Passo Imediato

O proximo passo recomendado e iniciar a Fase 5 criando o protocolo de avaliacao
academica.

Arquivo sugerido:

```text
docs/EVALUATION_PROTOCOL.md
```

Esse documento deve ser criado antes de qualquer implementacao de ontologia ou
fuzzy, porque ele define o que sera considerado evidencia de sucesso.
