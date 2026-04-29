Montei os três arquivos para você colocar na raiz do projeto:

* [AGENTS.md](sandbox:/mnt/data/kouzina_reco_agent_docs/AGENTS.md)
* [CLAUDE.md](sandbox:/mnt/data/kouzina_reco_agent_docs/CLAUDE.md)
* [SKILL.md](sandbox:/mnt/data/kouzina_reco_agent_docs/SKILL.md)

## Como usar no projeto

Quando criar o repositório, coloque os arquivos assim:

```text
kouzina-reco/
├── AGENTS.md
├── CLAUDE.md
├── SKILL.md
├── README.md
├── backend/
├── widget/
├── data/
└── docs/
```

## Função de cada arquivo

### `AGENTS.md`

Use como instrução principal para  **Codex, Cursor, Copilot, agentes OpenAI e outros agentes de código** .

Ele define:

```text
escopo do MVP
arquitetura
stack
contratos da API
modelo de dados
regras do widget
recomendador v0
fuzzy v1
LGPD
segurança
ordem correta de implementação
critérios de pronto
```

Esse é o arquivo mais importante para evitar que o agente “invente moda” e tente começar por deep learning, ontologia enorme, painel complexo ou app Tray antes da hora.

### `CLAUDE.md`

Use especificamente com  **Claude Code** .

Ele é mais direto para fluxo de trabalho com Claude:

```text
como inspecionar o projeto
como planejar mudanças
como responder ao finalizar tarefas
o que não alterar
como validar
quais arquivos criar primeiro
como manter o MVP pequeno
```

### `SKILL.md`

Esse é opcional, mas recomendo manter.

Ele funciona como um  **playbook reutilizável do projeto** . Também serve como base caso você queira transformar esse fluxo em uma Skill formal depois.

Observação importante: este `SKILL.md` já tem frontmatter e instruções no formato de Skill, mas ainda não é um pacote completo de Skill do ChatGPT. Para virar uma Skill instalável, depois seria necessário criar a estrutura completa com `agents/openai.yaml`, referências e empacotamento. Para o seu repositório, ele já é útil como guia operacional.

## Primeiro prompt para usar com Codex ou Claude

Depois de colocar os arquivos na raiz do repositório, peça ao agente:

```text
Leia AGENTS.md, CLAUDE.md e SKILL.md.

Implemente somente a Fase 1 do projeto kouzina-reco:

1. Criar a estrutura inicial de pastas.
2. Criar backend FastAPI mínimo.
3. Criar GET /health.
4. Criar POST /events mockado.
5. Criar GET /recommendations mockado.
6. Criar widget/kouzina-reco.js.
7. Criar widget/demo.html.
8. Criar requirements.txt.
9. Criar docker-compose.yml com PostgreSQL.
10. Criar README.md com instruções de execução.

Não implemente fuzzy ainda.
Não implemente ontologia ainda.
Não implemente painel.
Não use dados pessoais.
Não integre Tray ainda.
```

## Ordem recomendada agora

Seu próximo passo é criar o repositório com esta estrutura inicial:

```text
kouzina-reco/
├── AGENTS.md
├── CLAUDE.md
├── SKILL.md
├── README.md
├── backend/
│   └── app/
├── widget/
├── data/
└── docs/
```

Depois disso, peça para o Codex ou Claude executar apenas a primeira entrega:  **API mínima + widget demo local** . Isso vai tirar o projeto do zero sem inflar o escopo.
