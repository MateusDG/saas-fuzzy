# Fase 5.5 - Frontend Visual Completo Do Kouzina Reco

## Objetivo

Criar uma interface didatica, visual e interativa para explicar o funcionamento
atual do Kouzina Reco para avaliador de TCC, professor, stakeholder, pessoa
leiga, futuro cliente e equipe tecnica.

Esta fase nao cria painel administrativo, nao altera widget, nao altera API
publica, nao altera ranking v0 e nao implementa fuzzy, ontologia ou recomendador
hibrido.

## Decisao De Arquitetura

Foi escolhida a Rota B: recriar `frontend/` como aplicacao Vite + React +
TypeScript.

Motivos:

- a interface tem muitas secoes reutilizaveis;
- o playground da API precisa de estado de loading, erro, sucesso e JSON bruto;
- os graficos da Fase 5 ficam mais claros com componentes Recharts;
- dados estaticos em TypeScript reduzem duplicacao e facilitam manutencao;
- o widget real permanece separado em `widget/kouzina-reco.js`.

## Stack

- Vite;
- React;
- TypeScript;
- Recharts;
- lucide-react;
- CSS autoral em `frontend/src/styles.css`.

## O Que A Interface Mostra

- estado atual do projeto;
- o que existe e o que ainda nao existe;
- linha do tempo das fases;
- fluxo do produto no site ate eventos anonimos;
- arquitetura com widget, API, ranking v0 e PostgreSQL;
- playground de `GET /health`, `GET /recommendations` e `POST /events`;
- cards visuais de recomendacao;
- ranking v0 e guardrails editoriais;
- eventos anonimos e LGPD;
- modelo de dados e migrations Alembic;
- avaliacao offline com metricas reais da Fase 5.1;
- regressao do ranking v0 pos-refatoracao;
- politica de paths seguros;
- comandos locais;
- glossario.

## Dados Usados Nos Graficos

Fontes versionadas usadas como base visual:

- `reports/evaluation/dataset_profile.json`;
- `reports/baselines/v0_baseline_snapshot.json`;
- `reports/baselines/v0_baseline_post_refactor.json`;
- `docs/RESULTS_PHASE_5_BASELINE.md`;
- `docs/PHASE_5_3_3_RANKING_V0_REGRESSION.md`;
- `docs/PHASE_5_3_4_SCRIPT_OUTPUT_PATHS.md`.

Os numeros representam artefatos offline ou regressao tecnica. Eles nao
representam CTR real, conversao real, funil real ou validacao final com cliente.

## Como Rodar

```powershell
cd frontend
npm install
npm run dev
```

Abrir:

```text
http://localhost:5173
```

O playground usa por padrao `/api-local`, proxy do Vite para:

```text
http://localhost:8000
```

Para testar com backend real:

```powershell
docker compose up -d
cd backend
uvicorn app.main:app --reload
```

## Build

```powershell
cd frontend
npm run build
```

`frontend/dist/` e `frontend/node_modules/` devem permanecer ignorados pelo Git.

## Limites Declarados Na Interface

- fuzzy nao esta implementado;
- ontologia nao esta implementada;
- recomendador hibrido nao esta implementado;
- nao ha deploy;
- nao ha painel administrativo;
- nao ha integracao Tray;
- nao ha dados reais de funil;
- nao ha CTR real;
- nao ha conversao real;
- nao ha validacao com clientes reais nesta etapa.

## Arquivos Principais

```text
frontend/
  package.json
  vite.config.ts
  tsconfig.json
  src/
    App.tsx
    main.tsx
    styles.css
    components/
    data/
    services/
    types/
```

## Observacao Sobre O Widget

`widget/kouzina-reco.js` continua sendo o widget real embutivel no site. O
frontend criado nesta fase e apenas uma camada visual para explicacao e
demonstracao local do projeto.
