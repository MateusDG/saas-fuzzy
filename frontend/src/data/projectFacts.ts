import {
  Activity,
  Boxes,
  BrainCircuit,
  ChartNoAxesCombined,
  CheckCircle2,
  Database,
  Gauge,
  GitCompareArrows,
  Lock,
  PlugZap,
  Server,
  ShieldCheck,
  Sparkles,
  Store,
  Workflow,
  XCircle,
} from "lucide-react";
import type { FactCard, IconTextItem } from "../types/project";

export const heroFacts: FactCard[] = [
  {
    title: "API",
    value: "FastAPI",
    detail: "health, eventos e recomendacoes",
    tone: "done",
  },
  {
    title: "Widget",
    value: "JavaScript puro",
    detail: "embutivel e independente do frontend visual",
    tone: "done",
  },
  {
    title: "Ranking",
    value: "v0 por regras",
    detail: "explicavel, com guardrails editoriais",
    tone: "active",
  },
  {
    title: "Academico",
    value: "baseline offline",
    detail: "Amazon Reviews 2023 / Appliances",
    tone: "planned",
  },
];

export const currentCapabilities: IconTextItem[] = [
  {
    icon: PlugZap,
    title: "Widget real",
    description:
      "O arquivo widget/kouzina-reco.js identifica contexto, chama a API, renderiza cards e envia eventos anonimos.",
    tone: "done",
  },
  {
    icon: Server,
    title: "API operacional",
    description:
      "GET /health, GET /recommendations e POST /events mantem o contrato publico atual.",
    tone: "done",
  },
  {
    icon: Database,
    title: "PostgreSQL preparado",
    description:
      "Produtos, lojas, relacoes manuais futuras e recommendation_events estao no modelo SQLAlchemy e Alembic.",
    tone: "done",
  },
  {
    icon: Gauge,
    title: "Ranking v0 explicavel",
    description:
      "O score combina complementaridade, disponibilidade, voltagem, preco, marca, ambiente e politica editorial.",
    tone: "active",
  },
  {
    icon: ShieldCheck,
    title: "Eventos anonimos",
    description:
      "A telemetria mede uso do widget sem coletar nome, email, CPF, telefone, endereco ou pagamento.",
    tone: "done",
  },
  {
    icon: ChartNoAxesCombined,
    title: "Avaliacao offline",
    description:
      "A Fase 5 registra protocolo, dataset publico, metricas e snapshots para comparacao academica futura.",
    tone: "planned",
  },
];

export const missingCapabilities: IconTextItem[] = [
  {
    icon: BrainCircuit,
    title: "Fuzzy nao implementado",
    description:
      "As variaveis fuzzy estao planejadas, mas ainda nao existem no motor de recomendacao.",
    tone: "blocked",
  },
  {
    icon: Boxes,
    title: "Ontologia nao implementada",
    description:
      "A ontologia formal ainda e fase futura. O v0 usa regras editoriais, nao raciocinio ontologico.",
    tone: "blocked",
  },
  {
    icon: Store,
    title: "Sem integracao Tray",
    description:
      "O catalogo oficial autorizado entra por CSV local. O widget nao consulta Tray diretamente.",
    tone: "blocked",
  },
  {
    icon: Activity,
    title: "Sem funil real",
    description:
      "Nao existe CTR real, conversao real ou validacao com clientes reais nesta fase.",
    tone: "warning",
  },
  {
    icon: Lock,
    title: "Sem login e painel",
    description:
      "Esta interface e uma apresentacao visual, nao uma ferramenta administrativa de producao.",
    tone: "neutral",
  },
  {
    icon: Sparkles,
    title: "Sem recomendador hibrido",
    description:
      "O hibrido ontologico-fuzzy depende de fases posteriores e de comparacao experimental.",
    tone: "blocked",
  },
];

export const widgetFlow: IconTextItem[] = [
  {
    icon: Store,
    title: "Produto no site",
    description:
      "A pagina informa o produto por data attribute, meta tag ou texto com codigo.",
  },
  {
    icon: PlugZap,
    title: "Widget inicializa",
    description:
      "O script cria anonymous_id em localStorage e session_id em sessionStorage.",
  },
  {
    icon: Workflow,
    title: "API recebe contexto",
    description:
      "GET /recommendations recebe product_id e widget_id, sem dados pessoais.",
  },
  {
    icon: Gauge,
    title: "Ranking v0 ordena",
    description:
      "O backend pontua candidatos do catalogo e aplica guardrails editoriais.",
  },
  {
    icon: CheckCircle2,
    title: "Cards aparecem",
    description:
      "O widget mostra nome, imagem, preco quando existe, score e motivo textual.",
  },
  {
    icon: Activity,
    title: "Eventos medem uso",
    description:
      "page_view, recommendation_impression e recommendation_click sao enviados.",
  },
];

export const privacyAllowed = [
  "anonymous_id",
  "session_id",
  "event_type",
  "page_url",
  "product_id",
  "widget_id",
  "recommended_product_id",
  "metadata tecnico nao sensivel",
];

export const privacyBlocked = [
  "nome",
  "CPF",
  "email",
  "telefone",
  "endereco",
  "dados de pagamento",
  "conteudo de formularios",
  "mensagens de WhatsApp",
];

export const backendRefactorItems: IconTextItem[] = [
  {
    icon: Workflow,
    title: "Rotas separadas",
    description:
      "backend/app/api/routes concentra health, events e recommendations.",
    tone: "done",
  },
  {
    icon: Database,
    title: "Core e banco",
    description:
      "backend/app/core organiza configuracao, database e politica de paths.",
    tone: "done",
  },
  {
    icon: Gauge,
    title: "Recommender isolado",
    description:
      "rules, scoring, explanations, relation_policy e service separam o v0.",
    tone: "done",
  },
  {
    icon: GitCompareArrows,
    title: "Wrappers preservados",
    description:
      "Comandos antigos seguem funcionando para seed, review, baseline e avaliacao.",
    tone: "active",
  },
];

export const finalBoundaries: IconTextItem[] = [
  {
    icon: CheckCircle2,
    title: "Esta tela explica",
    description:
      "Fluxo atual, componentes, dados anonimos, ranking v0, regressao e limites.",
    tone: "done",
  },
  {
    icon: XCircle,
    title: "Esta tela nao administra",
    description:
      "Nao salva configuracoes comerciais, nao altera banco e nao mexe no widget.",
    tone: "blocked",
  },
];
