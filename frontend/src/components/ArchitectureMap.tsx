import { ArrowRight, Database, Gauge, Globe2, PlugZap, Server } from "lucide-react";
import { apiContracts, architectureNodes, databaseTables } from "../data/architecture";
import { Section } from "./layout/Section";
import { SectionHeader } from "./layout/SectionHeader";
import { StatusChip } from "./layout/StatusChip";

const nodeIcons = [Globe2, PlugZap, Server, Gauge, Database];

export function ArchitectureMap() {
  return (
    <Section id="arquitetura" className="section-light">
      <SectionHeader
        eyebrow="Arquitetura"
        title="Como as pecas conversam sem mudar o contrato publico"
        description="O widget chama a API. A API usa catalogo e ranking v0 quando possivel, ou fallback mockado quando falta contexto."
      />

      <div className="architecture-chain" role="img" aria-label="Fluxo site, widget, API, ranking e banco">
        {architectureNodes.map((node, index) => {
          const Icon = nodeIcons[index];
          return (
            <div className="chain-fragment" key={node.label}>
              <article className={`chain-node chain-node-${node.tone}`}>
                <Icon aria-hidden="true" size={24} />
                <strong>{node.label}</strong>
                <span>{node.detail}</span>
              </article>
              {index < architectureNodes.length - 1 ? (
                <ArrowRight className="chain-arrow" aria-hidden="true" size={22} />
              ) : null}
            </div>
          );
        })}
      </div>

      <div className="contract-grid">
        {apiContracts.map((contract) => (
          <article className="contract-card" key={contract.path}>
            <StatusChip tone={contract.method === "POST" ? "active" : "done"}>
              {contract.method}
            </StatusChip>
            <h3>{contract.path}</h3>
            <p>{contract.description}</p>
            <code>{contract.sample}</code>
          </article>
        ))}
      </div>

      <div className="table-map" aria-label="Tabelas principais">
        {databaseTables.map((table) => (
          <article className="table-card" key={table.table}>
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
    </Section>
  );
}
