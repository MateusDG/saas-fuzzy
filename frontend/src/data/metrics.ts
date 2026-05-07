import type { RecommendationItem } from "../types/api";

export const datasetProfile = {
  dataset: "Amazon Reviews 2023",
  category: "Appliances",
  executedAt: "2026-05-06T15:31:55Z",
  validationStatus: "pending_client_data",
  users: 6651,
  items: 2798,
  trainInteractions: 7368,
  testInteractions: 6651,
  premiumItemsBeforeSplit: 4916,
  removedMissingPrice: 28083,
  removedLowInteractions: 15428,
  removedLowAverageRating: 25880,
  usersRemovedLowInteractions: 216476,
  p75: 48.9175,
  p90: 109.99,
};

export const datasetBars = [
  { name: "Usuarios avaliados", value: datasetProfile.users },
  { name: "Itens finais", value: datasetProfile.items },
  { name: "Interacoes treino", value: datasetProfile.trainInteractions },
  { name: "Interacoes teste", value: datasetProfile.testInteractions },
];

export const preprocessingBars = [
  { name: "Sem preco", value: datasetProfile.removedMissingPrice },
  { name: "Baixa interacao", value: datasetProfile.removedLowInteractions },
  { name: "Baixa avaliacao", value: datasetProfile.removedLowAverageRating },
];

export const offlineMetrics = [
  {
    metric: "Precision@5",
    popularidade: 1.0164,
    conteudo: 1.0164,
    explanation: "Percentual medio de acertos dentro dos 5 itens recomendados.",
  },
  {
    metric: "Recall@5",
    popularidade: 5.0819,
    conteudo: 5.0819,
    explanation: "Percentual de itens relevantes recuperados no top-5.",
  },
  {
    metric: "nDCG@5",
    popularidade: 3.1299,
    conteudo: 3.1299,
    explanation: "Qualidade do ranking considerando posicao dos acertos.",
  },
  {
    metric: "Precision@10",
    popularidade: 0.8976,
    conteudo: 0.8976,
    explanation: "Precision cai no top-10 porque mais itens entram na lista.",
  },
  {
    metric: "Recall@10",
    popularidade: 8.9761,
    conteudo: 8.9761,
    explanation: "Recall sobe no top-10 porque o sistema tenta mais itens.",
  },
  {
    metric: "nDCG@10",
    popularidade: 4.3978,
    conteudo: 4.3978,
    explanation: "Ganho ordenado no top-10 ainda e baseline inicial.",
  },
];

export const coverageMetrics = [
  { metric: "Cobertura@5", popularidade: 0.2502, conteudo: 0.2502 },
  { metric: "Cobertura@10", popularidade: 0.4289, conteudo: 0.4289 },
  { metric: "Diversidade@5", popularidade: 0, conteudo: 0 },
  { metric: "Diversidade@10", popularidade: 0, conteudo: 0 },
];

export const v0Regression = {
  sourceProducts: 30,
  recommendationRows: 120,
  fingerprint:
    "e1e8d8cf2f28f3499834a831e84cb75dacfff76746538ad49b304296e160ed42",
  postRefactorFingerprint:
    "e1e8d8cf2f28f3499834a831e84cb75dacfff76746538ad49b304296e160ed42",
  fingerprintsEqual: true,
  selfRecommendationRows: 0,
  blockedRows: 0,
  policyDemotedRows: 50,
  reasonQualityStrong: 102,
  reasonQualityMedium: 18,
  reasonQualityGeneric: 0,
};

export const relationClassData = [
  { name: "weak", label: "Fraca", value: 46 },
  { name: "contextual", label: "Contextual", value: 36 },
  { name: "universal", label: "Universal", value: 34 },
  { name: "kouzina_specific", label: "Especifica Kouzina", value: 4 },
];

export const policyActionData = [
  { name: "review", label: "Revisar", value: 43 },
  { name: "allow", label: "Permitir", value: 41 },
  { name: "boost", label: "Impulsionar", value: 29 },
  { name: "demote", label: "Rebaixar", value: 7 },
];

export const validationStatusData = [
  { name: "agent_hypothesis", label: "Hipotese de agentes", value: 81 },
  { name: "pending_client_data", label: "Pendente de dados reais", value: 39 },
];

export const sampleRecommendations: RecommendationItem[] = [
  {
    product_id: "3120",
    name: "Cooktop recomendado para composicao com forno",
    url: "https://www.kouzinaclub.com.br/",
    image_url: null,
    price: 28870,
    reason:
      "Complementa funcionalmente o produto atual. Compatibilidade de voltagem. Faixa de preco semelhante. Relacao comum em projetos de cozinha.",
    score: 97,
  },
  {
    product_id: "3014",
    name: "Coifa premium compativel com projeto gourmet",
    url: "https://www.kouzinaclub.com.br/",
    image_url: null,
    price: 26990,
    reason:
      "Complementa funcionalmente o produto atual. Produto disponivel. Mesmo ambiente de uso como sinal auxiliar.",
    score: 93,
  },
  {
    product_id: "2435",
    name: "Coifa de mesma suite visual",
    url: "https://www.kouzinaclub.com.br/",
    image_url: null,
    price: 24990,
    reason:
      "Mesma marca como sinal auxiliar de suite. Faixa premium semelhante. Relacao comum em projetos de cozinha.",
    score: 83,
  },
];
