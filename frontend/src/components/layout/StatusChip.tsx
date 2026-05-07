import type { StatusTone } from "../../types/project";

interface StatusChipProps {
  children: React.ReactNode;
  tone?: StatusTone;
}

export function StatusChip({ children, tone = "neutral" }: StatusChipProps) {
  return <span className={`status-chip status-${tone}`}>{children}</span>;
}
