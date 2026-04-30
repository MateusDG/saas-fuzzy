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

Retorna recomendacoes. Na Fase 3, a API tenta localizar o `product_id` no
catalogo importado e aplica o ranking v0 por regras nos candidatos ativos da
mesma loja.

Se o banco estiver vazio, indisponivel, sem candidatos ou se o produto atual nao
existir no catalogo, retorna o fallback mockado da Fase 1.

Parametros:

- `product_id`: opcional;
- `widget_id`: opcional.

Exemplo:

```text
GET /recommendations?product_id=mock-001&widget_id=product-page
```

Resposta:

```json
{
  "widget_title": "Complete seu projeto",
  "product_id": "mock-001",
  "recommendations": [
    {
      "product_id": "mock-002",
      "name": "Forno de embutir recomendado",
      "url": "https://www.kouzinaclub.com.br/",
      "image_url": null,
      "price": 8490.0,
      "reason": "Produto complementar ao item visualizado. Produto disponivel. Mesma voltagem do produto atual. Faixa de preco proxima. Mesma marca do produto atual. Faixa premium semelhante.",
      "score": 100.0
    }
  ]
}
```

Em respostas vindas do catalogo, `score` e a pontuacao bruta do ranking v0. Em
respostas de fallback, `score` continua sendo o valor mockado da Fase 1.
