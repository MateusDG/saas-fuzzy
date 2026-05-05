# Eventos Do Widget

Na Fase 2, os eventos sao validados pela API e persistidos em
`recommendation_events` quando o banco esta disponivel.

## Eventos Permitidos

Eventos atuais de MVP:

```text
page_view
product_view
recommendation_impression
recommendation_click
```

Eventos preparados para fase futura de funil (sem analise nesta etapa):

```text
widget_opened
product_context_loaded
recommendations_requested
recommendations_rendered
recommendation_expanded
recommendation_dismissed
quote_requested
add_to_cart_clicked
alternative_requested
session_ended
```

## Campos Coletados

- `event_type`;
- `event_name` (opcional, com fallback para `event_type`);
- `anonymous_id`;
- `session_id`;
- `page_url`;
- `product_id`;
- `source_product_id`;
- `source_product_type`;
- `widget_id`;
- `recommended_product_id`;
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
- `funnel_stage`;
- `metadata` nao sensivel.

Na persistencia, o backend mantem apenas chaves tecnicas permitidas em
`metadata`, como `score`, `recommendation_count` e `recommended_product_ids`.
Chaves fora dessa lista sao descartadas.

## Finalidade

- medir carregamento do widget;
- medir impressoes de recomendacoes;
- medir cliques em recomendacoes;
- apoiar evolucao futura do recomendador.

## Privacidade

Nao coletar:

- nome;
- CPF;
- e-mail;
- telefone;
- endereco;
- dados de pagamento;
- conteudo de formularios;
- mensagens de WhatsApp.

## Origem Dos Identificadores

- `anonymous_id`: criado pelo widget em `localStorage`;
- `session_id`: criado pelo widget em `sessionStorage`.

## Persistencia

Campos salvos em `recommendation_events`:

- `event_type`;
- `anonymous_id`;
- `session_id`;
- `page_url`;
- `product_external_id`;
- `widget_id`;
- `recommended_product_external_id`;
- `metadata`;
- `created_at`.
