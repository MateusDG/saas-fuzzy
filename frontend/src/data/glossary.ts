export const glossary = [
  {
    term: "Widget",
    description:
      "Script JavaScript embutivel no site da Kouzina para exibir recomendacoes.",
  },
  {
    term: "Ranking v0",
    description:
      "Primeiro recomendador por regras comerciais explicaveis. Nao e fuzzy nem ontologia.",
  },
  {
    term: "Guardrails editoriais",
    description:
      "Regras de cautela para reduzir falsos positivos, rebaixar relacoes fracas e bloquear casos ruins.",
  },
  {
    term: "Reason",
    description:
      "Texto que explica por que um produto foi recomendado.",
  },
  {
    term: "Snapshot v0",
    description:
      "Arquivo congelado com recomendacoes e fingerprint para validar regressao do ranking.",
  },
  {
    term: "CTR",
    description:
      "Taxa de clique. Ainda nao existe como metrica real porque falta integracao controlada em producao.",
  },
  {
    term: "Baseline offline",
    description:
      "Comparacao academica inicial com dataset publico, antes de fuzzy e ontologia.",
  },
  {
    term: "Proxy premium",
    description:
      "Uso de percentil de preco para recortar produtos premium no dataset publico. Nao representa renda do consumidor.",
  },
];
