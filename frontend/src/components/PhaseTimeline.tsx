import { timeline } from "../data/timeline";
import { Section } from "./layout/Section";
import { SectionHeader } from "./layout/SectionHeader";
import { StatusChip } from "./layout/StatusChip";

export function PhaseTimeline() {
  return (
    <Section id="timeline" className="section-dark">
      <SectionHeader
        eyebrow="Linha do tempo"
        title="Do MVP local ao baseline academico"
        description="A Fase 5.5 nao muda o motor de recomendacao. Ela organiza a narrativa visual do estado pos-refatoracao."
      />

      <div className="timeline-rail" aria-label="Linha do tempo das fases">
        {timeline.map((item) => (
          <article className="timeline-item" key={`${item.phase}-${item.title}`}>
            <div className="timeline-item__marker" aria-hidden="true" />
            <div className="timeline-item__body">
              <div className="timeline-item__top">
                <span>{item.phase}</span>
                <StatusChip tone={item.tone}>{item.status}</StatusChip>
              </div>
              <h3>{item.title}</h3>
              <p>{item.description}</p>
              <small>{item.evidence}</small>
            </div>
          </article>
        ))}
      </div>
    </Section>
  );
}
