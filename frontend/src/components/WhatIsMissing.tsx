import { finalBoundaries, missingCapabilities } from "../data/projectFacts";
import { Section } from "./layout/Section";
import { SectionHeader } from "./layout/SectionHeader";
import { StatusChip } from "./layout/StatusChip";

export function WhatIsMissing() {
  return (
    <Section id="limites" className="section-warm">
      <SectionHeader
        eyebrow="Limites honestos"
        title="O que esta apresentacao nao deve afirmar"
        description="A interface foi desenhada para vender clareza, nao exagerar maturidade. Os limites sao parte da qualidade tecnica e academica."
      />

      <div className="boundary-grid">
        {finalBoundaries.map((item) => (
          <article className="boundary-card" key={item.title}>
            <item.icon aria-hidden="true" size={24} />
            <h3>{item.title}</h3>
            <p>{item.description}</p>
          </article>
        ))}
      </div>

      <div className="missing-list">
        {missingCapabilities.map((item) => (
          <div className="missing-row" key={item.title}>
            <StatusChip tone={item.tone}>{item.title}</StatusChip>
            <p>{item.description}</p>
          </div>
        ))}
      </div>
    </Section>
  );
}
