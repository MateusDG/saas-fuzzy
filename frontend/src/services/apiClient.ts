import type {
  EventPayload,
  EventResponse,
  HealthResponse,
  RecommendationResponse,
} from "../types/api";

export class ApiClientError extends Error {
  status?: number;
  body?: unknown;

  constructor(message: string, status?: number, body?: unknown) {
    super(message);
    this.name = "ApiClientError";
    this.status = status;
    this.body = body;
  }
}

function normalizeBaseUrl(baseUrl: string): string {
  const trimmed = baseUrl.trim() || "/api-local";
  return trimmed.replace(/\/+$/, "");
}

function buildUrl(baseUrl: string, path: string): string {
  return `${normalizeBaseUrl(baseUrl)}${path}`;
}

async function parseJson<T>(response: Response): Promise<T> {
  const text = await response.text();
  const body = text ? JSON.parse(text) : null;

  if (!response.ok) {
    throw new ApiClientError(`HTTP ${response.status}`, response.status, body);
  }

  return body as T;
}

export async function fetchHealth(baseUrl: string): Promise<HealthResponse> {
  const response = await fetch(buildUrl(baseUrl, "/health"));
  return parseJson<HealthResponse>(response);
}

export async function fetchRecommendations(
  baseUrl: string,
  productId: string,
  widgetId: string,
): Promise<RecommendationResponse> {
  const url = new URL(buildUrl(baseUrl, "/recommendations"), window.location.origin);

  if (productId.trim()) {
    url.searchParams.set("product_id", productId.trim());
  }

  if (widgetId.trim()) {
    url.searchParams.set("widget_id", widgetId.trim());
  }

  const response = await fetch(url.toString(), {
    headers: {
      "X-Kouzina-Public-Key": "kouzina_public_dev_key",
    },
  });

  return parseJson<RecommendationResponse>(response);
}

export async function postEvent(
  baseUrl: string,
  payload: EventPayload,
): Promise<EventResponse> {
  const response = await fetch(buildUrl(baseUrl, "/events"), {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Kouzina-Public-Key": "kouzina_public_dev_key",
    },
    body: JSON.stringify(payload),
  });

  return parseJson<EventResponse>(response);
}
