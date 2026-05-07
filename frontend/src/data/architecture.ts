export const architectureNodes = [
  {
    label: "Site Kouzina",
    detail: "pagina de produto",
    tone: "site",
  },
  {
    label: "Widget JS",
    detail: "widget/kouzina-reco.js",
    tone: "widget",
  },
  {
    label: "FastAPI",
    detail: "health, events, recommendations",
    tone: "api",
  },
  {
    label: "Ranking v0",
    detail: "regras e guardrails",
    tone: "engine",
  },
  {
    label: "PostgreSQL",
    detail: "products e events",
    tone: "database",
  },
];

export const apiContracts = [
  {
    method: "GET",
    path: "/health",
    title: "Saude do servico",
    description: "Confirma que a API esta em execucao.",
    sample: '{ "status": "ok", "service": "kouzina-reco-api", "version": "0.1.0" }',
  },
  {
    method: "GET",
    path: "/recommendations",
    title: "Recomendacoes do widget",
    description:
      "Retorna cards com product_id, name, url, image_url, price, reason e score.",
    sample:
      '?product_id=119&widget_id=product-page -> { "widget_title": "Complete seu projeto", "recommendations": [...] }',
  },
  {
    method: "POST",
    path: "/events",
    title: "Eventos anonimos",
    description:
      "Valida e persiste eventos tecnicos do widget, sem dados pessoais.",
    sample:
      '{ "event_type": "recommendation_click", "anonymous_id": "anon_..." }',
  },
];

export const databaseTables = [
  {
    table: "stores",
    description: "Loja padrao, dominio e chave publica do widget.",
    fields: ["slug", "name", "domain", "public_key", "created_at"],
  },
  {
    table: "products",
    description: "Catalogo seedado ou autorizado local, com atributos comerciais.",
    fields: [
      "external_id",
      "name",
      "url",
      "image_url",
      "brand",
      "price",
      "product_type",
      "environment",
    ],
  },
  {
    table: "manual_product_relations",
    description: "Base futura para curadoria manual de relacoes.",
    fields: ["source_product_id", "target_product_id", "relation_type", "weight"],
  },
  {
    table: "recommendation_events",
    description:
      "Eventos anonimos e colunas opcionais para analise futura de funil.",
    fields: [
      "event_type",
      "anonymous_id",
      "session_id",
      "product_external_id",
      "recommended_product_external_id",
      "relation_class",
      "score",
    ],
  },
];

export const scoringRules = [
  { label: "Complementaridade funcional", value: 30, type: "positive" },
  { label: "Produto disponivel", value: 20, type: "positive" },
  { label: "Compatibilidade de voltagem", value: 15, type: "positive" },
  { label: "Faixa de preco semelhante", value: 12, type: "positive" },
  { label: "Mesma marca", value: 5, type: "positive" },
  { label: "Mesmo ambiente", value: 5, type: "positive" },
  { label: "Faixa premium semelhante", value: 3, type: "positive" },
  { label: "Relacao universal", value: 8, type: "positive" },
  { label: "Boost de politica", value: 4, type: "positive" },
  { label: "Mesmo produto", value: -100, type: "negative" },
  { label: "Relacao bloqueada", value: -100, type: "negative" },
  { label: "Produto indisponivel", value: -30, type: "negative" },
  { label: "Relacao fraca", value: -20, type: "negative" },
  { label: "Review/demote de politica", value: -8, type: "negative" },
];

export const relationPolicyCards = [
  {
    title: "Universal",
    description:
      "Relacoes sustentadas por funcao, uso ou instalacao, como cooktop e coifa.",
    detail: "Pode receber boost quando a politica permite.",
  },
  {
    title: "Contextual",
    description:
      "Faz sentido em projetos gourmet ou consultivos, mas depende de ambiente e contexto.",
    detail: "Aparece com cautela e reason explicita.",
  },
  {
    title: "Especifica Kouzina",
    description:
      "Pode ser editorial, comercial ou ligada ao mix local, sem virar verdade universal.",
    detail: "Precisa de validacao humana ou comportamento real.",
  },
  {
    title: "Fraca ou proibida",
    description:
      "Sinais auxiliares sem complementaridade real devem cair no ranking ou ser bloqueados.",
    detail: "Ajuda a reduzir falsos positivos antes de fuzzy.",
  },
];
