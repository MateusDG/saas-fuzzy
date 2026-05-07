import { ExternalLink, ImageOff, Sparkles } from "lucide-react";
import type { RecommendationItem } from "../types/api";
import { StatusChip } from "./layout/StatusChip";

interface RecommendationCardsProps {
  title: string;
  sourceLabel: string;
  items: RecommendationItem[];
  emptyMessage?: string;
}

function formatPrice(value: number | null): string {
  if (typeof value !== "number") {
    return "Sob consulta";
  }

  return value.toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL",
    maximumFractionDigits: 2,
  });
}

export function RecommendationCards({
  title,
  sourceLabel,
  items,
  emptyMessage = "Nenhuma recomendacao para mostrar.",
}: RecommendationCardsProps) {
  return (
    <div className="recommendation-panel">
      <div className="recommendation-panel__header">
        <div>
          <p className="eyebrow">Cards de recomendacao</p>
          <h3>{title}</h3>
        </div>
        <StatusChip tone={items.length ? "active" : "neutral"}>{sourceLabel}</StatusChip>
      </div>

      {items.length === 0 ? (
        <div className="empty-state">
          <Sparkles aria-hidden="true" size={24} />
          <p>{emptyMessage}</p>
        </div>
      ) : (
        <div className="recommendation-grid">
          {items.map((item) => (
            <article className="recommendation-card" key={item.product_id}>
              <div className="recommendation-card__media">
                {item.image_url ? (
                  <img src={item.image_url} alt="" loading="lazy" />
                ) : (
                  <ImageOff aria-hidden="true" size={28} />
                )}
              </div>
              <div className="recommendation-card__body">
                <span className="product-id">#{item.product_id}</span>
                <h4>{item.name}</h4>
                <strong>{formatPrice(item.price)}</strong>
                <p>{item.reason}</p>
                <div className="recommendation-card__footer">
                  <span>Score {item.score.toFixed(1)}</span>
                  <a href={item.url} target="_blank" rel="noreferrer">
                    Abrir
                    <ExternalLink aria-hidden="true" size={14} />
                  </a>
                </div>
              </div>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}
