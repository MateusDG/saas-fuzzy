import {
  ArrowRight,
  Database,
  Gauge,
  MousePointerClick,
  Shield,
  Sparkles,
} from "lucide-react";
import { heroFacts } from "../data/projectFacts";
import { MetricCard } from "./layout/MetricCard";
import { StatusChip } from "./layout/StatusChip";

export function Hero() {
  return (
    <section className="hero" id="topo" aria-labelledby="hero-title">
      <div className="hero__content">
        <div className="hero__copy">
          <StatusChip tone="active">Fase 5.5</StatusChip>
          <p className="eyebrow">Mapa visual do funcionamento atual</p>
          <h1 id="hero-title">Kouzina Reco explicado de ponta a ponta</h1>
          <p className="hero__lead">
            Uma interface didatica para apresentar o projeto a avaliadores,
            professores, stakeholders, pessoas leigas, clientes futuros e equipe
            tecnica. Mostra o que ja existe, como funciona e o que ainda e
            futuro.
          </p>
          <div className="hero__actions" aria-label="Atalhos principais">
            <a className="button button-primary" href="#api">
              Testar API
              <ArrowRight aria-hidden="true" size={18} />
            </a>
            <a className="button button-secondary" href="#fluxo">
              Ver fluxo
              <ArrowRight aria-hidden="true" size={18} />
            </a>
          </div>
        </div>

        <div className="hero-visual" aria-label="Resumo visual do sistema">
          <div className="system-trace">
            <div className="trace-node trace-product">
              <Sparkles aria-hidden="true" size={24} />
              <span>Produto premium</span>
            </div>
            <div className="trace-line" aria-hidden="true" />
            <div className="trace-node trace-widget">
              <MousePointerClick aria-hidden="true" size={24} />
              <span>Widget JS</span>
            </div>
            <div className="trace-line" aria-hidden="true" />
            <div className="trace-node trace-api">
              <Gauge aria-hidden="true" size={24} />
              <span>Ranking v0</span>
            </div>
            <div className="trace-line" aria-hidden="true" />
            <div className="trace-node trace-db">
              <Database aria-hidden="true" size={24} />
              <span>PostgreSQL</span>
            </div>
          </div>
          <div className="privacy-ribbon">
            <Shield aria-hidden="true" size={18} />
            <span>Eventos anonimos, sem PII e sem funil real afirmado.</span>
          </div>
        </div>
      </div>

      <div className="hero-metrics" aria-label="Estado do projeto">
        {heroFacts.map((fact) => (
          <MetricCard
            key={fact.title}
            title={fact.title}
            value={fact.value}
            detail={fact.detail}
            tone={fact.tone}
          />
        ))}
      </div>
    </section>
  );
}
