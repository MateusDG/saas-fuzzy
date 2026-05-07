export interface HealthResponse {
  status: string;
  service: string;
  version: string;
  timestamp?: string;
}

export interface RecommendationItem {
  product_id: string;
  name: string;
  url: string;
  image_url: string | null;
  price: number | null;
  reason: string;
  score: number;
}

export interface RecommendationResponse {
  widget_title: string;
  product_id: string | null;
  recommendations: RecommendationItem[];
}

export interface EventPayload {
  event_type: string;
  anonymous_id: string;
  session_id?: string | null;
  page_url?: string | null;
  product_id?: string | null;
  widget_id?: string | null;
  recommended_product_id?: string | null;
  metadata?: Record<string, unknown>;
}

export interface EventResponse {
  received: boolean;
  event_type: string;
  timestamp: string;
}

export type ApiAction = "health" | "recommendations" | "event";

export type ApiRequestState = "idle" | "loading" | "success" | "error";
