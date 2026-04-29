# API Kouzina Reco

Base local:

```text
http://localhost:8000
```

## GET /health

Retorna o status da API.

Resposta:

```json
{
  "status": "ok",
  "service": "kouzina-reco-api",
  "version": "0.1.0"
}
```

## POST /events

Recebe eventos anonimos do widget. Na Fase 2, o payload e validado e salvo em
`recommendation_events` quando o banco esta disponivel.

Payload:

```json
{
  "event_type": "recommendation_click",
  "anonymous_id": "anon_123",
  "session_id": "sess_456",
  "page_url": "http://localhost:5500/demo.html",
  "product_id": "12345",
  "widget_id": "product-page",
  "recommended_product_id": "mock-001",
  "metadata": {}
}
```

Resposta:

```json
{
  "received": true,
  "event_type": "recommendation_click",
  "timestamp": "2026-04-29T00:00:00Z"
}
```

Eventos aceitos:

```text
page_view
product_view
recommendation_impression
recommendation_click
```

## GET /recommendations

Retorna recomendacoes. Na Fase 2, a API tenta usar produtos importados no banco.
Se o banco estiver vazio ou indisponivel, retorna o fallback mockado da Fase 1.

Parametros:

- `product_id`: opcional;
- `widget_id`: opcional.

Exemplo:

```text
GET /recommendations?product_id=12345&widget_id=product-page
```

Resposta:

```json
{
  "widget_title": "Complete seu projeto",
  "product_id": "12345",
  "recommendations": [
    {
      "product_id": "mock-001",
      "name": "Cooktop premium compativel",
      "url": "https://www.kouzinaclub.com.br/",
      "image_url": null,
      "price": 9990.0,
      "reason": "Produto complementar para composicao de cozinha gourmet.",
      "score": 0.92
    }
  ]
}
```
