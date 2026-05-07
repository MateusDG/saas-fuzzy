import { backendRefactorItems } from "../data/projectFacts";
import { Section } from "./layout/Section";
import { SectionHeader } from "./layout/SectionHeader";
import { StatusChip } from "./layout/StatusChip";

const backendFolders = [
  "core",
  "api/routes",
  "db",
  "schemas",
  "services",
  "recommender",
  "catalog",
  "review",
  "evaluation",
];

export function BackendRefactorPanel() {
  return (
    <Section id="backend" className="section-dark">
      <SectionHeader
        eyebrow="Backend pos-Fase 5.3.1"
        title="Estrutura canonica para evoluir sem quebrar contrato"
        description="A organizacao atual separa rotas, banco, schemas, servicos, ranking, catalogo, review e avaliacao academica."
      />

      <div className="backend-layout">
        <div className="module-grid">
          {backendFolders.map((folder) => (
            <span key={folder}>{folder}</span>
          ))}
        </div>

        <div className="feature-grid compact">
          {backendRefactorItems.map((item) => (
            <article className="feature-card" key={item.title}>
              <item.icon aria-hidden="true" size={22} />
              <h4>{item.title}</h4>
              <p>{item.description}</p>
            </article>
          ))}
        </div>
      </div>

      <div className="compatibility-strip">
        <StatusChip tone="done">Contrato preservado</StatusChip>
        <span>GET /health</span>
        <span>POST /events</span>
        <span>GET /recommendations</span>
        <span>widget sem mudanca</span>
      </div>
    </Section>
  );
}
