import { ApiPlayground } from "./components/ApiPlayground";
import { ArchitectureMap } from "./components/ArchitectureMap";
import { BackendRefactorPanel } from "./components/BackendRefactorPanel";
import { CommandsPanel } from "./components/CommandsPanel";
import { DatabasePanel } from "./components/DatabasePanel";
import { EventPrivacyPanel } from "./components/EventPrivacyPanel";
import { Footer } from "./components/Footer";
import { GlossaryPanel } from "./components/GlossaryPanel";
import { Hero } from "./components/Hero";
import { OfflineEvaluationPanel } from "./components/OfflineEvaluationPanel";
import { PathPolicyPanel } from "./components/PathPolicyPanel";
import { PhaseTimeline } from "./components/PhaseTimeline";
import { ProjectOverview } from "./components/ProjectOverview";
import { RankingExplainer } from "./components/RankingExplainer";
import { RegressionPanel } from "./components/RegressionPanel";
import { SystemFlow } from "./components/SystemFlow";
import { WhatIsMissing } from "./components/WhatIsMissing";
import { AppShell } from "./components/layout/AppShell";

export function App() {
  return (
    <AppShell>
      <Hero />
      <ProjectOverview />
      <PhaseTimeline />
      <SystemFlow />
      <ArchitectureMap />
      <ApiPlayground />
      <RankingExplainer />
      <EventPrivacyPanel />
      <DatabasePanel />
      <OfflineEvaluationPanel />
      <RegressionPanel />
      <BackendRefactorPanel />
      <PathPolicyPanel />
      <WhatIsMissing />
      <CommandsPanel />
      <GlossaryPanel />
      <Footer />
    </AppShell>
  );
}
