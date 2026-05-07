import { BookOpenText } from "lucide-react";
import { glossary } from "../data/glossary";
import { Section } from "./layout/Section";
import { SectionHeader } from "./layout/SectionHeader";

export function GlossaryPanel() {
  return (
    <Section id="glossario" className="section-light">
      <SectionHeader
        eyebrow="Glossario"
        title="Termos do projeto em linguagem simples"
        description="Uma ponte para pessoas leigas e uma referencia rapida para equipe tecnica e avaliacao academica."
      />

      <div className="glossary-grid">
        {glossary.map((item) => (
          <article className="glossary-card" key={item.term}>
            <BookOpenText aria-hidden="true" size={20} />
            <h3>{item.term}</h3>
            <p>{item.description}</p>
          </article>
        ))}
      </div>
    </Section>
  );
}
