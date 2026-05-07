import { Database, GitBranch, TableProperties } from "lucide-react";
import { databaseTables } from "../data/architecture";
import { Section } from "./layout/Section";
import { SectionHeader } from "./layout/SectionHeader";
import { StatusChip } from "./layout/StatusChip";

const migrations = [
  {
    file: "0001_initial_schema.py",
    detail: "Cria stores, products, manual_product_relations e recommendation_events.",
  },
  {
    file: "0002_add_event_analytics_columns.py",
    detail:
      "Adiciona colunas opcionais para funil futuro, relacao, score e validacao.",
  },
];

export function DatabasePanel() {
  return (
    <Section id="banco" className="section-dark">
      <SectionHeader
        eyebrow="PostgreSQL e Alembic"
        title="Banco preparado para catalogo, eventos e evolucao controlada"
        description="A Fase 5.3 introduziu Alembic sem remover o fallback local de create_all para desenvolvimento e testes."
      />

      <div className="db-overview">
        <article className="db-callout">
          <Database aria-hidden="true" size={30} />
          <h3>Modelo atual</h3>
          <p>
            O MVP ja persiste produtos e eventos anonimos. Relacoes manuais estao
            modeladas para curadoria futura, mas ainda nao comandam o ranking.
          </p>
        </article>

        <article className="db-callout">
          <GitBranch aria-hidden="true" size={30} />
          <h3>Migrations</h3>
          <p>
            Em ambiente controlado, a trilha recomendada e rodar `alembic
            upgrade head` antes de operar o backend.
          </p>
        </article>
      </div>

      <div className="table-map">
        {databaseTables.map((table) => (
          <article className="table-card" key={table.table}>
            <TableProperties aria-hidden="true" size={20} />
            <h3>{table.table}</h3>
            <p>{table.description}</p>
            <div className="field-list">
              {table.fields.map((field) => (
                <span key={field}>{field}</span>
              ))}
            </div>
          </article>
        ))}
      </div>

      <div className="migration-list" aria-label="Migrations principais">
        {migrations.map((migration) => (
          <article className="migration-item" key={migration.file}>
            <StatusChip tone="done">Alembic</StatusChip>
            <h3>{migration.file}</h3>
            <p>{migration.detail}</p>
          </article>
        ))}
      </div>
    </Section>
  );
}
