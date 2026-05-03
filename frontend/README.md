# Kouzina Reco — Mapa Visual do MVP

Frontend local, estático e didático para entender o estado atual do MVP Kouzina Reco.

Ele não é painel administrativo, não tem login, não faz deploy, não integra Tray e não coleta dados pessoais.

## Como rodar

Em um terminal:

```powershell
cd frontend
python -m http.server 5600
```

Abra:

```text
http://localhost:5600
```

## API esperada

O testador visual assume a API em:

```text
http://localhost:8000
```

Para rodar a API:

```powershell
docker compose up -d
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Se o navegador bloquear por CORS, confirme que `ALLOWED_ORIGINS` inclui:

```text
http://localhost:5600
```

## O que esta área mostra

- Visão geral do MVP.
- Linha do tempo das fases 1, 2, 3 e 4.2 a 4.6.
- Arquitetura widget, API, PostgreSQL, ranking v0 e fallback.
- Fluxo do widget.
- Endpoints `/health`, `/recommendations` e `/events`.
- Testador visual da API.
- Ranking v0 explicado por barras.
- Modelo de dados atual.
- Privacidade e LGPD.
- Catálogo, importação e relatório de revisão qualitativa.

## Limites

Esta área usa apenas HTML, CSS e JavaScript puro. Ela não modifica o widget principal e não adiciona dependências.
