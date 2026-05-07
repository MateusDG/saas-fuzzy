import { Copy, Terminal } from "lucide-react";
import { commandGroups } from "../data/commands";
import { Section } from "./layout/Section";
import { SectionHeader } from "./layout/SectionHeader";

export function CommandsPanel() {
  return (
    <Section id="comandos" className="section-dark">
      <SectionHeader
        eyebrow="Execucao local"
        title="Comandos para demonstrar o projeto"
        description="Os blocos abaixo ajudam a apresentar API, widget, frontend visual e avaliacao offline sem misturar responsabilidades."
      />

      <div className="command-grid">
        {commandGroups.map((group) => (
          <article className="command-card" key={group.title}>
            <Terminal aria-hidden="true" size={22} />
            <h3>{group.title}</h3>
            <p>{group.description}</p>
            <div className="command-list">
              {group.commands.map((command) => (
                <code key={command}>
                  <Copy aria-hidden="true" size={14} />
                  {command}
                </code>
              ))}
            </div>
          </article>
        ))}
      </div>
    </Section>
  );
}
