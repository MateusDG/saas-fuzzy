import { FileCheck2, FolderLock, ShieldAlert } from "lucide-react";
import { Section } from "./layout/Section";
import { SectionHeader } from "./layout/SectionHeader";
import { StatusChip } from "./layout/StatusChip";

const pathExamples = [
  {
    tone: "done" as const,
    icon: FileCheck2,
    title: "Recomendado",
    command: "reports/baselines/v0_baseline_path_test.json",
    detail: "Resolve a partir da raiz do repositorio.",
  },
  {
    tone: "active" as const,
    icon: FolderLock,
    title: "Legado normalizado",
    command: "../reports/baselines/v0_baseline_path_test.json",
    detail: "Um unico ../ inicial e normalizado para manter compatibilidade.",
  },
  {
    tone: "warning" as const,
    icon: ShieldAlert,
    title: "Bloqueado",
    command: "../../reports/baselines/v0_baseline_path_test.json",
    detail: "Tentativa de escapar da raiz do repo gera erro explicito.",
  },
];

export function PathPolicyPanel() {
  return (
    <Section id="paths" className="section-light">
      <SectionHeader
        eyebrow="Paths seguros"
        title="Scripts nao gravam fora do repositorio por acidente"
        description="A Fase 5.3.4 padronizou outputs de baseline, review e avaliacao para evitar escapes relativos perigosos."
      />

      <div className="path-grid">
        {pathExamples.map((item) => (
          <article className="path-card" key={item.title}>
            <item.icon aria-hidden="true" size={24} />
            <StatusChip tone={item.tone}>{item.title}</StatusChip>
            <code>{item.command}</code>
            <p>{item.detail}</p>
          </article>
        ))}
      </div>
    </Section>
  );
}
