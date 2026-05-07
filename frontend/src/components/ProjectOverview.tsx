import { currentCapabilities, missingCapabilities } from "../data/projectFacts";
import { Section } from "./layout/Section";
import { SectionHeader } from "./layout/SectionHeader";
import { StatusChip } from "./layout/StatusChip";

export function ProjectOverview() {
  return (
    <Section id="visao" className="section-light">
      <SectionHeader
        eyebrow="Estado atual"
        title="O que existe hoje e o que ainda nao existe"
        description="A apresentacao separa claramente produto operacional, experimento academico e etapas futuras para nao confundir MVP com promessa."
      />

      <div className="split-grid">
        <div>
          <div className="inline-heading">
            <StatusChip tone="done">Existe</StatusChip>
            <h3>Base funcional e mensuravel</h3>
          </div>
          <div className="feature-grid">
            {currentCapabilities.map((item) => (
              <article className="feature-card" key={item.title}>
                <item.icon aria-hidden="true" size={22} />
                <h4>{item.title}</h4>
                <p>{item.description}</p>
              </article>
            ))}
          </div>
        </div>

        <div>
          <div className="inline-heading">
            <StatusChip tone="blocked">Nao existe</StatusChip>
            <h3>Limites declarados</h3>
          </div>
          <div className="feature-grid">
            {missingCapabilities.map((item) => (
              <article className="feature-card feature-card-muted" key={item.title}>
                <item.icon aria-hidden="true" size={22} />
                <h4>{item.title}</h4>
                <p>{item.description}</p>
              </article>
            ))}
          </div>
        </div>
      </div>
    </Section>
  );
}
