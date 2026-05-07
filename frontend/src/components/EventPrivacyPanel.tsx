import { LockKeyhole, ShieldCheck } from "lucide-react";
import { privacyAllowed, privacyBlocked } from "../data/projectFacts";
import { Section } from "./layout/Section";
import { SectionHeader } from "./layout/SectionHeader";
import { StatusChip } from "./layout/StatusChip";

const events = [
  "page_view",
  "product_view",
  "recommendation_impression",
  "recommendation_click",
];

const futureEvents = [
  "quote_requested",
  "add_to_cart_clicked",
  "recommendation_dismissed",
  "session_ended",
];

export function EventPrivacyPanel() {
  return (
    <Section id="privacidade" className="section-light">
      <SectionHeader
        eyebrow="Eventos e LGPD"
        title="Medicao anonima sem dados pessoais"
        description="O backend aceita eventos tecnicos do widget e sanitiza metadata. As colunas analiticas preparam funil futuro, mas nao representam analise executada."
      />

      <div className="privacy-layout">
        <article className="privacy-block">
          <ShieldCheck aria-hidden="true" size={28} />
          <h3>Eventos atuais</h3>
          <p>Usados para medir carregamento, impressao e clique do widget.</p>
          <div className="pill-list">
            {events.map((event) => (
              <span key={event}>{event}</span>
            ))}
          </div>
        </article>

        <article className="privacy-block">
          <LockKeyhole aria-hidden="true" size={28} />
          <h3>Eventos futuros preparados</h3>
          <p>Existem como estrutura, nao como conclusao de funil real.</p>
          <div className="pill-list">
            {futureEvents.map((event) => (
              <span key={event}>{event}</span>
            ))}
          </div>
        </article>
      </div>

      <div className="privacy-columns">
        <article className="privacy-list allowed">
          <StatusChip tone="done">Permitido</StatusChip>
          <ul>
            {privacyAllowed.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </article>

        <article className="privacy-list blocked">
          <StatusChip tone="blocked">Proibido</StatusChip>
          <ul>
            {privacyBlocked.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </article>
      </div>
    </Section>
  );
}
