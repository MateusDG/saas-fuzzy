import type { LucideIcon } from "lucide-react";

export type StatusTone =
  | "done"
  | "active"
  | "planned"
  | "warning"
  | "blocked"
  | "neutral";

export interface FactCard {
  title: string;
  value: string;
  detail: string;
  tone: StatusTone;
}

export interface IconTextItem {
  icon: LucideIcon;
  title: string;
  description: string;
  tone?: StatusTone;
}

export interface TimelineItem {
  phase: string;
  title: string;
  status: string;
  tone: StatusTone;
  description: string;
  evidence: string;
}

export interface CommandGroup {
  title: string;
  description: string;
  commands: string[];
}
