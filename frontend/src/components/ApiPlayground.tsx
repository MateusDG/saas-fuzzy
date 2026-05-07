import { Send, Server, Sparkles, Trash2 } from "lucide-react";
import { useMemo, useState } from "react";
import { sampleRecommendations } from "../data/metrics";
import {
  ApiClientError,
  fetchHealth,
  fetchRecommendations,
  postEvent,
} from "../services/apiClient";
import type {
  ApiAction,
  ApiRequestState,
  RecommendationResponse,
} from "../types/api";
import { RecommendationCards } from "./RecommendationCards";
import { Section } from "./layout/Section";
import { SectionHeader } from "./layout/SectionHeader";
import { StatusChip } from "./layout/StatusChip";

function stringify(value: unknown): string {
  return JSON.stringify(value, null, 2);
}

function actionLabel(action: ApiAction): string {
  const labels: Record<ApiAction, string> = {
    health: "GET /health",
    recommendations: "GET /recommendations",
    event: "POST /events",
  };

  return labels[action];
}

export function ApiPlayground() {
  const [baseUrl, setBaseUrl] = useState("/api-local");
  const [productId, setProductId] = useState("119");
  const [widgetId, setWidgetId] = useState("product-page");
  const [state, setState] = useState<ApiRequestState>("idle");
  const [statusMessage, setStatusMessage] = useState("Aguardando teste");
  const [rawJson, setRawJson] = useState("Clique em um endpoint para ver a resposta JSON.");
  const [liveRecommendations, setLiveRecommendations] =
    useState<RecommendationResponse | null>(null);

  const statusTone = useMemo(() => {
    if (state === "success") return "done";
    if (state === "loading") return "active";
    if (state === "error") return "warning";
    return "neutral";
  }, [state]);

  async function runAction(action: ApiAction) {
    setState("loading");
    setStatusMessage(`Chamando ${actionLabel(action)}...`);
    setRawJson("Aguardando resposta da API local...");

    try {
      let data: unknown;

      if (action === "health") {
        data = await fetchHealth(baseUrl);
      } else if (action === "recommendations") {
        data = await fetchRecommendations(baseUrl, productId, widgetId);
        setLiveRecommendations(data as RecommendationResponse);
      } else {
        data = await postEvent(baseUrl, {
          event_type: "recommendation_click",
          anonymous_id: "frontend_visual_anon",
          session_id: "frontend_visual_session",
          page_url: window.location.href,
          product_id: productId || null,
          widget_id: widgetId || "product-page",
          recommended_product_id: "frontend-visual-test",
          metadata: {
            recommendation_count: 1,
            recommended_product_ids: ["frontend-visual-test"],
            source: "phase_5_5_frontend_visual",
          },
        });
      }

      setState("success");
      setStatusMessage(`${actionLabel(action)} respondeu com sucesso`);
      setRawJson(stringify(data));
    } catch (error) {
      const apiError = error as ApiClientError;
      setState("error");
      setStatusMessage("Nao foi possivel chamar a API");
      setRawJson(
        stringify({
          message:
            "Verifique se o backend esta rodando em http://localhost:8000. No modo dev, /api-local usa proxy do Vite para evitar CORS.",
          detail: apiError.message,
          status: apiError.status ?? null,
          response: apiError.body ?? null,
        }),
      );
    }
  }

  function clearOutput() {
    setState("idle");
    setStatusMessage("Aguardando teste");
    setRawJson("Clique em um endpoint para ver a resposta JSON.");
    setLiveRecommendations(null);
  }

  return (
    <Section id="api" className="section-dark">
      <SectionHeader
        eyebrow="Playground da API"
        title="Teste a API local e veja o JSON bruto"
        description="O testador usa dados tecnicos ficticios e nao coleta PII. Quando a API esta desligada, a tela mostra um erro claro e continua funcionando."
      />

      <div className="playground-grid">
        <form className="playground-form" onSubmit={(event) => event.preventDefault()}>
          <div className="form-row">
            <label htmlFor="api-base-url">Base da API</label>
            <input
              id="api-base-url"
              value={baseUrl}
              onChange={(event) => setBaseUrl(event.target.value)}
              aria-describedby="api-base-help"
            />
            <small id="api-base-help">
              Use `/api-local` no Vite ou `http://localhost:8000` com CORS configurado.
            </small>
          </div>

          <div className="form-grid">
            <div className="form-row">
              <label htmlFor="product-id">product_id</label>
              <input
                id="product-id"
                value={productId}
                onChange={(event) => setProductId(event.target.value)}
              />
            </div>
            <div className="form-row">
              <label htmlFor="widget-id">widget_id</label>
              <input
                id="widget-id"
                value={widgetId}
                onChange={(event) => setWidgetId(event.target.value)}
              />
            </div>
          </div>

          <div className="playground-actions" aria-label="Acoes de teste da API">
            <button
              className="button button-primary"
              type="button"
              disabled={state === "loading"}
              onClick={() => runAction("health")}
            >
              <Server aria-hidden="true" size={18} />
              Health
            </button>
            <button
              className="button button-secondary"
              type="button"
              disabled={state === "loading"}
              onClick={() => runAction("recommendations")}
            >
              <Sparkles aria-hidden="true" size={18} />
              Recomendacoes
            </button>
            <button
              className="button button-ghost"
              type="button"
              disabled={state === "loading"}
              onClick={() => runAction("event")}
            >
              <Send aria-hidden="true" size={18} />
              Evento
            </button>
          </div>
        </form>

        <aside className="json-console" aria-label="Resposta JSON da API">
          <div className="json-console__top">
            <StatusChip tone={statusTone}>{statusMessage}</StatusChip>
            <button className="icon-text-button" type="button" onClick={clearOutput}>
              <Trash2 aria-hidden="true" size={16} />
              Limpar
            </button>
          </div>
          <pre tabIndex={0} aria-live="polite">
            {rawJson}
          </pre>
        </aside>
      </div>

      <RecommendationCards
        title={
          liveRecommendations
            ? liveRecommendations.widget_title
            : "Exemplo congelado do ranking v0"
        }
        sourceLabel={liveRecommendations ? "Resposta da API" : "Snapshot ilustrativo"}
        items={liveRecommendations?.recommendations ?? sampleRecommendations}
      />
    </Section>
  );
}
