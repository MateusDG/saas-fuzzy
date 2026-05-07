import type { TimelineItem } from "../types/project";

export const timeline: TimelineItem[] = [
  {
    phase: "Fase 1",
    title: "Base tecnica local",
    status: "concluida",
    tone: "done",
    description:
      "API minima, widget local, demo HTML, eventos mockados e recomendacoes mockadas.",
    evidence: "GET /health, POST /events e GET /recommendations nasceram aqui.",
  },
  {
    phase: "Fase 2",
    title: "Persistencia e catalogo",
    status: "concluida",
    tone: "done",
    description:
      "PostgreSQL, modelos SQLAlchemy, seed idempotente e eventos persistidos.",
    evidence: "stores, products, manual_product_relations e recommendation_events.",
  },
  {
    phase: "Fase 3",
    title: "Ranking v0",
    status: "concluida",
    tone: "done",
    description:
      "Regras comerciais explicaveis passam a ordenar candidatos do catalogo.",
    evidence: "Cada recomendacao retorna reason textual e score.",
  },
  {
    phase: "Fase 4.2 a 4.9",
    title: "Catalogo autorizado e guardrails",
    status: "hipoteses provisiorias",
    tone: "active",
    description:
      "CSV oficial autorizado, imagens por URL, politica de relacoes e guardrails editoriais.",
    evidence: "Sem validacao final com cliente e sem funil real.",
  },
  {
    phase: "Fase 5.1",
    title: "Avaliacao offline",
    status: "baseline inicial",
    tone: "planned",
    description:
      "Protocolo academico, Amazon Reviews 2023 / Appliances e metricas top-k.",
    evidence: "Precision@k, Recall@k, nDCG@k, cobertura e diversidade.",
  },
  {
    phase: "Fase 5.3",
    title: "Backend auditado",
    status: "estavel",
    tone: "done",
    description:
      "Refatoracao em pacotes, Alembic, smoke test, regressao do v0 e paths seguros.",
    evidence: "60 testes passaram na ultima fase de paths.",
  },
  {
    phase: "Fase 5.5",
    title: "Frontend visual completo",
    status: "esta entrega",
    tone: "active",
    description:
      "Interface didatica para explicar o sistema, seus resultados offline e suas limitacoes.",
    evidence: "Vite, React, TypeScript, Recharts e playground da API.",
  },
  {
    phase: "Fases 6 a 8",
    title: "Ontologia, fuzzy e hibrido",
    status: "futuro",
    tone: "blocked",
    description:
      "Etapas academicas futuras, ainda fora do codigo operacional atual.",
    evidence: "Nao afirmar como implementado ate existir motor e comparacao.",
  },
];
