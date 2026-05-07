# Kouzina Reco Frontend Visual

Frontend didatico da Fase 5.5. Ele apresenta o funcionamento atual do Kouzina Reco para avaliadores, professores, stakeholders, clientes futuros e equipe tecnica.

Esta interface nao e painel administrativo, nao altera ranking, nao altera widget, nao altera API publica e nao implementa fuzzy, ontologia ou recomendador hibrido.

## Stack

- Vite
- React
- TypeScript
- Recharts
- lucide-react
- CSS autoral em `src/styles.css`

## Como rodar

```powershell
cd frontend
npm install
npm run dev
```

Abra:

```text
http://localhost:5173
```

## API local

O playground usa por padrao o proxy `/api-local`, configurado no Vite para encaminhar chamadas para:

```text
http://localhost:8000
```

Para testar a API real diretamente, rode o backend:

```powershell
docker compose up -d
cd backend
uvicorn app.main:app --reload
```

Depois use o playground visual para chamar:

- `GET /health`
- `GET /recommendations`
- `POST /events`

## Build

```powershell
npm run build
```

O build gera `frontend/dist/`, que deve continuar ignorado pelo Git.

## Limites

- Nao usa dados reais de clientes.
- Nao mostra CTR real, conversao real ou funil real.
- Graficos de avaliacao usam os artefatos versionados da Fase 5.
- Recomendacoes exibidas no playground so sao reais quando a API local esta rodando.
