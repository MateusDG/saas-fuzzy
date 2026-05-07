import { widgetFlow } from "../data/projectFacts";
import { Section } from "./layout/Section";
import { SectionHeader } from "./layout/SectionHeader";

export function SystemFlow() {
  return (
    <Section id="fluxo" className="section-warm">
      <SectionHeader
        eyebrow="Fluxo operacional"
        title="Do produto no site ao evento anonimo"
        description="Este e o caminho do widget real. O frontend visual apenas explica o fluxo e testa a API local quando ela esta rodando."
      />

      <ol className="flow-list">
        {widgetFlow.map((step, index) => (
          <li key={step.title}>
            <span className="step-index">{String(index + 1).padStart(2, "0")}</span>
            <step.icon aria-hidden="true" size={24} />
            <h3>{step.title}</h3>
            <p>{step.description}</p>
          </li>
        ))}
      </ol>
    </Section>
  );
}
