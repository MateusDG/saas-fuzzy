import type { CommandGroup } from "../types/project";

export const commandGroups: CommandGroup[] = [
  {
    title: "Backend local",
    description: "Sobe banco e API para o playground conversar com o sistema real.",
    commands: [
      "docker compose up -d",
      "cd backend",
      "uvicorn app.main:app --reload",
    ],
  },
  {
    title: "Catalogo e migrations",
    description: "Prepara schema e dados locais quando necessario.",
    commands: [
      "cd backend",
      "alembic upgrade head",
      "python -m app.seed",
      "python -m app.seed --file ../data/products_kouzina_official.csv --replace-products",
    ],
  },
  {
    title: "Widget real",
    description: "Serve o demo do widget sem passar pelo frontend visual.",
    commands: ["cd widget", "python -m http.server 5500"],
  },
  {
    title: "Frontend visual",
    description: "Executa esta apresentacao interativa da Fase 5.5.",
    commands: ["cd frontend", "npm install", "npm run dev", "npm run build"],
  },
  {
    title: "Avaliacao e regressao",
    description: "Reproduz artefatos usados nos graficos e na narrativa academica.",
    commands: [
      "cd backend",
      "python -m app.run_offline_evaluation --top-k 10",
      "python -m app.freeze_v0_baseline --limit-products 30 --top-k 4",
      "pytest",
    ],
  },
];
