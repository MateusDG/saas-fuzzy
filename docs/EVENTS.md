# Eventos Do Widget

Na Fase 1, os eventos sao validados pela API e nao sao persistidos.

## Eventos Permitidos

```text
page_view
product_view
recommendation_impression
recommendation_click
```

## Campos Coletados

- `event_type`;
- `anonymous_id`;
- `session_id`;
- `page_url`;
- `product_id`;
- `widget_id`;
- `recommended_product_id`;
- `metadata` nao sensivel.

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

