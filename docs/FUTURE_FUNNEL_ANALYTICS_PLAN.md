# Plano Futuro De Analise De Funil

## Status Deste Documento

Este documento e um plano futuro.

Nao representa analise executada.
Nao usa dados reais de cliente nesta fase.
Nao afirma validacao humana final.

## Quando A Analise Deve Comecar

A analise de funil deve iniciar somente depois de:

- integracao da API/widget ao site real;
- coleta consistente de eventos anonimos;
- volume minimo de sessoes e interacoes;
- revisao de qualidade dos eventos coletados.

## Metricas Futuras

- `impression_rate`
- `click_through_rate`
- `quote_request_rate`
- `add_to_cart_rate`
- `dismiss_rate`
- conversao por `relation_class`
- conversao por `relation_type`
- aceitacao de produtos `Sob consulta`
- rejeicao de relacoes fracas
- performance por ambiente
- performance por marca
- performance por faixa de preco
- performance por posicao no carousel
- comparacao entre score v0 e comportamento real

## Perguntas De Pesquisa Futuras

- Relacoes universais performam melhor que contextuais?
- Produtos `Sob consulta` geram mais orcamento ou mais rejeicao?
- Marca pesa mais que complementaridade no publico high-end?
- Ambiente pesa mais que categoria?
- Relacoes gourmet geram mais clique?
- Recomendacoes tecnicas convertem melhor que recomendacoes editoriais?
- O score v0 prediz interesse real?
- Quais relacoes devem virar ontologia?
- Quais relacoes devem virar regra fuzzy?
- Quais relacoes devem ser removidas?

## Estrutura Minima De Dados Esperada

Eventos anonimos por sessao com:

- contexto do produto de origem;
- itens recomendados exibidos;
- posicao/rank e score;
- classe e tipo de relacao;
- acao do usuario (impressao, clique, dismiss, quote, add-to-cart).

Sem PII e sem login obrigatorio.

## Preparacao Tecnica Da Fase 5.3.1

A tabela `recommendation_events` foi preparada com colunas opcionais para:

- `event_name`;
- `source_product_type`;
- `recommended_product_type`;
- `rank`;
- `score`;
- `relation_class`;
- `relation_type`;
- `relation_policy_action`;
- `validation_status`;
- `is_quote_only`;
- `quote_reason`;
- `environment`;
- `brand`;
- `price_band`;
- `funnel_stage`.

Esses campos facilitam consultas futuras, mas este documento continua sendo um
plano. Nenhuma analise real de funil foi executada nesta fase.

## Criterios De Qualidade Antes Da Analise

- sem lacunas graves de tracking;
- consistencia de nomenclatura de evento;
- baixa taxa de evento invalido;
- rastreabilidade por `session_id` anonimo;
- campos de relacao preenchidos.

## Entregas Futuras Possiveis

- relatorio offline de funil por relacao;
- matriz de risco de falso positivo por tipo;
- comparacao de baseline v0 com sinais comportamentais;
- priorizacao de ajustes editoriais;
- insumos para Fase 6 (ontologia) e Fase 7 (fuzzy).

## Fora De Escopo Deste Documento

- resultados simulados de conversao;
- estimativa ficticia de CTR;
- conclusao causal sem dados reais;
- dashboard implementado nesta fase.
