import {
  Bar,
  BarChart,
  Cell,
  Legend,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import {
  policyActionData,
  relationClassData,
  v0Regression,
  validationStatusData,
} from "../data/metrics";
import { Section } from "./layout/Section";
import { SectionHeader } from "./layout/SectionHeader";
import { MetricCard } from "./layout/MetricCard";
import { StatusChip } from "./layout/StatusChip";

const relationColors = ["#7a1f3d", "#8f4f2a", "#4f5a32", "#c79a43"];
const policyColors = ["#2f2a24", "#4f5a32", "#8f4f2a", "#b8652f"];

export function RegressionPanel() {
  return (
    <Section id="regressao" className="section-warm">
      <SectionHeader
        eyebrow="Regressao do ranking"
        title="O v0 ficou estavel depois da refatoracao"
        description="A Fase 5.3.3 comparou snapshots e manteve o fingerprint canonico das linhas, sem alterar ranking, API publica ou widget."
      />

      <div className="metric-grid">
        <MetricCard
          title="Produtos origem"
          value={String(v0Regression.sourceProducts)}
          detail="amostra do snapshot v0"
          tone="done"
        />
        <MetricCard
          title="Linhas recomendadas"
          value={String(v0Regression.recommendationRows)}
          detail="top-k 4 para cada origem"
          tone="done"
        />
        <MetricCard
          title="Auto-recomendacoes"
          value={String(v0Regression.selfRecommendationRows)}
          detail="o proprio produto nao voltou"
          tone="done"
        />
        <MetricCard
          title="Reasons genericas"
          value={String(v0Regression.reasonQualityGeneric)}
          detail="0 no review de regressao"
          tone="done"
        />
      </div>

      <div className="fingerprint-panel">
        <div>
          <StatusChip tone={v0Regression.fingerprintsEqual ? "done" : "warning"}>
            fingerprint igual
          </StatusChip>
          <h3>SHA-256 canonico</h3>
          <code>{v0Regression.fingerprint}</code>
        </div>
        <p>
          O hash do arquivo completo pode mudar por causa de `generated_at`, mas
          o fingerprint canonico das linhas permaneceu igual entre snapshot e
          pos-refatoracao.
        </p>
      </div>

      <div className="chart-grid">
        <article className="chart-panel">
          <h3>Classes de relacao no snapshot</h3>
          <p>Mostra a mistura de relacoes universais, contextuais e fracas ainda pendentes.</p>
          <div className="chart-box">
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={relationClassData}
                  dataKey="value"
                  nameKey="label"
                  innerRadius={58}
                  outerRadius={98}
                  paddingAngle={3}
                >
                  {relationClassData.map((entry, index) => (
                    <Cell key={entry.name} fill={relationColors[index % relationColors.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </article>

        <article className="chart-panel">
          <h3>Acoes da politica provisoria</h3>
          <p>Os guardrails permitem, impulsionam, pedem revisao ou rebaixam relacoes.</p>
          <div className="chart-box">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={policyActionData}>
                <XAxis dataKey="label" tick={{ fontSize: 11 }} />
                <YAxis allowDecimals={false} />
                <Tooltip />
                <Bar dataKey="value" name="Linhas" radius={[4, 4, 0, 0]}>
                  {policyActionData.map((entry, index) => (
                    <Cell key={entry.name} fill={policyColors[index % policyColors.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </article>

        <article className="chart-panel chart-panel-wide">
          <h3>Status de validacao</h3>
          <p>
            A maior parte ainda vem de hipoteses de agentes. Outra parte ja esta
            explicitamente marcada como pendente de dados reais.
          </p>
          <div className="chart-box">
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={validationStatusData} layout="vertical" margin={{ left: 80 }}>
                <XAxis type="number" allowDecimals={false} />
                <YAxis dataKey="label" type="category" width={170} tick={{ fontSize: 11 }} />
                <Tooltip />
                <Bar dataKey="value" name="Linhas" fill="#8f4f2a" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </article>
      </div>
    </Section>
  );
}
