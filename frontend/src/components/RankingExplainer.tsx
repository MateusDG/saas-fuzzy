import { AlertTriangle, CheckCircle2, Gauge } from "lucide-react";
import { scoringRules, relationPolicyCards } from "../data/architecture";
import { Section } from "./layout/Section";
import { SectionHeader } from "./layout/SectionHeader";
import { StatusChip } from "./layout/StatusChip";

function widthForScore(value: number): string {
  const max = value < 0 ? 100 : 30;
  return `${Math.min(Math.abs(value) / max, 1) * 100}%`;
}

export function RankingExplainer() {
  return (
    <Section id="ranking" className="section-warm">
      <SectionHeader
        eyebrow="Ranking v0"
        title="Regras comerciais explicaveis antes de fuzzy"
        description="O score atual e uma soma de sinais comerciais e tecnicos. Ele nao e probabilidade, nao usa ML e nao usa ontologia formal."
      />

      <div className="ranking-layout">
        <div className="score-board" aria-label="Pontuacao do ranking v0">
          {scoringRules.map((rule) => (
            <div className={`score-line score-line-${rule.type}`} key={rule.label}>
              <span className="score-line__label">{rule.label}</span>
              <span className="score-line__track">
                <span style={{ width: widthForScore(rule.value) }} />
              </span>
              <strong>{rule.value > 0 ? `+${rule.value}` : rule.value}</strong>
            </div>
          ))}
        </div>

        <aside className="ranking-note">
          <Gauge aria-hidden="true" size={28} />
          <h3>Como ler o v0</h3>
          <p>
            A complementaridade funcional e o eixo principal. Marca, ambiente,
            preco e premium sao sinais auxiliares. Se esses sinais aparecem sem
            relacao forte, o guardrail reduz a prioridade.
          </p>
          <div className="note-list">
            <span>
              <CheckCircle2 aria-hidden="true" size={16} />
              cada card precisa de reason
            </span>
            <span>
              <AlertTriangle aria-hidden="true" size={16} />
              hipoteses ainda pendem de validacao real
            </span>
          </div>
        </aside>
      </div>

      <div className="policy-grid" aria-label="Classes da politica de relacoes">
        {relationPolicyCards.map((card) => (
          <article className="policy-card" key={card.title}>
            <StatusChip
              tone={
                card.title === "Fraca ou proibida"
                  ? "warning"
                  : card.title === "Universal"
                    ? "done"
                    : "active"
              }
            >
              {card.title}
            </StatusChip>
            <p>{card.description}</p>
            <small>{card.detail}</small>
          </article>
        ))}
      </div>
    </Section>
  );
}
