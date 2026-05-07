import type { LucideIcon } from "lucide-react";
import type { StatusTone } from "../../types/project";

interface MetricCardProps {
  title: string;
  value: string;
  detail: string;
  icon?: LucideIcon;
  tone?: StatusTone;
}

export function MetricCard({
  title,
  value,
  detail,
  icon: Icon,
  tone = "neutral",
}: MetricCardProps) {
  return (
    <article className={`metric-card tone-${tone}`}>
      <div className="metric-card__top">
        <span>{title}</span>
        {Icon ? <Icon aria-hidden="true" size={18} /> : null}
      </div>
      <strong>{value}</strong>
      <p>{detail}</p>
    </article>
  );
}
