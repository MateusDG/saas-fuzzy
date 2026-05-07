import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { datasetBars, datasetProfile, offlineMetrics, preprocessingBars } from "../data/metrics";
import { Section } from "./layout/Section";
import { SectionHeader } from "./layout/SectionHeader";
import { MetricCard } from "./layout/MetricCard";

export function OfflineEvaluationPanel() {
  return (
    <Section id="avaliacao" className="section-light">
      <SectionHeader
        eyebrow="Avaliacao offline"
        title="Baseline academico com dados publicos"
        description="Os graficos usam resultados reais versionados da Fase 5.1. Eles nao representam comportamento de clientes Kouzina."
      />

      <div className="metric-grid">
        <MetricCard
          title="Dataset"
          value={datasetProfile.dataset}
          detail="Piloto controlado em Appliances"
          tone="planned"
        />
        <MetricCard
          title="Usuarios avaliados"
          value={datasetProfile.users.toLocaleString("pt-BR")}
          detail="Apos filtro minimo de interacoes"
          tone="done"
        />
        <MetricCard
          title="Itens finais"
          value={datasetProfile.items.toLocaleString("pt-BR")}
          detail="Catalogo publico filtrado"
          tone="done"
        />
        <MetricCard
          title="Status"
          value="pendente"
          detail="Sem validacao com cliente real"
          tone="warning"
        />
      </div>

      <div className="chart-grid">
        <article className="chart-panel">
          <h3>Metricas top-k dos baselines</h3>
          <p>
            Popularidade e conteudo/categoria ficaram equivalentes neste piloto
            porque o recorte usou uma unica categoria.
          </p>
          <div className="chart-box" aria-label="Grafico de Precision, Recall e nDCG">
            <ResponsiveContainer width="100%" height={320}>
              <BarChart data={offlineMetrics} margin={{ left: 6, right: 12 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="metric" tick={{ fontSize: 11 }} interval={0} />
                <YAxis tickFormatter={(value) => `${value}%`} />
                <Tooltip formatter={(value: number) => `${value.toFixed(4)}%`} />
                <Legend />
                <Bar dataKey="popularidade" name="Popularidade" fill="#8f4f2a" radius={[4, 4, 0, 0]} />
                <Bar dataKey="conteudo" name="Conteudo/Categoria" fill="#4f5a32" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </article>

        <article className="chart-panel">
          <h3>Recorte final do dataset</h3>
          <p>
            O perfil registra contagens apos filtros, split e proxy premium por
            percentil de preco.
          </p>
          <div className="chart-box" aria-label="Grafico de usuarios, itens e interacoes">
            <ResponsiveContainer width="100%" height={320}>
              <BarChart data={datasetBars} layout="vertical" margin={{ left: 40, right: 16 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey="name" type="category" width={120} tick={{ fontSize: 11 }} />
                <Tooltip formatter={(value: number) => value.toLocaleString("pt-BR")} />
                <Bar dataKey="value" name="Quantidade" fill="#7a1f3d" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </article>

        <article className="chart-panel chart-panel-wide">
          <h3>Filtros metodologicos</h3>
          <p>
            Itens removidos por preco ausente, baixa interacao e baixa avaliacao
            media. Esses filtros sao parte do protocolo, nao uma conclusao comercial.
          </p>
          <div className="chart-box" aria-label="Grafico de itens removidos no preprocessamento">
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={preprocessingBars} margin={{ left: 10, right: 16 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip formatter={(value: number) => value.toLocaleString("pt-BR")} />
                <Bar dataKey="value" name="Itens removidos" fill="#2f2a24" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </article>
      </div>
    </Section>
  );
}
