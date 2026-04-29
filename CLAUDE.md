# CLAUDE.md

## Contexto do projeto

Você está trabalhando no projeto `kouzina-reco` ou `saas-fuzzy`, um MVP comercial mínimo para recomendar produtos no site Kouzina Club usando uma API própria e um widget JavaScript plugável.

O projeto também servirá como base de TCC sobre sistema de recomendação híbrido baseado em ontologia fuzzy aplicado a e-commerce premium de cozinha e área gourmet.

O foco é construir primeiro um MVP funcional e mensurável, depois evoluir para:

1. persistência real de eventos;
2. catálogo manual;
3. recomendador por regras;
4. métricas de clique;
5. fuzzy v1;
6. ontologia;
7. baselines acadêmicos;
8. monetização.

---

## Documentos do projeto e prioridade de leitura

Antes de alterar qualquer arquivo, leia nesta ordem:

1. `AGENTS.md`;
2. `CLAUDE.md`;
3. `README.md`, se existir;
4. `docs/COMECAR.md`.

Leia `SKILL.md` como playbook complementar.

Leia `docs/deep-research-report.md` apenas como contexto acadêmico e visão futura do TCC.

Não use `docs/deep-research-report.md` para expandir o escopo da implementação atual. Ele contém o plano completo de pesquisa, mas a implementação deve seguir a fase solicitada pelo usuário.

### Hierarquia de prioridade

Se houver conflito entre documentos:

1. a solicitação atual do usuário tem prioridade;
2. `AGENTS.md` define limites gerais;
3. `CLAUDE.md` define como trabalhar no Claude Code;
4. `docs/COMECAR.md` define o passo a passo operacional;
5. `SKILL.md` complementa o fluxo;
6. `docs/deep-research-report.md` é apenas referência acadêmica.

---

## Regra de fase

Nunca avance de fase sem autorização explícita.

Se ainda não existirem `backend/`, `widget/`, `data/`, `.env.example` e `docker-compose.yml`, considerar que o projeto está antes da Fase 1 técnica local.

Quando o usuário pedir para "começar", "iniciar", "implementar o MVP" ou "criar a primeira versão", implementar somente a **Fase 1 técnica local**.

### Fase 1 técnica local

A primeira implementação deve entregar somente:

- API FastAPI mínima;
- `GET /health`;
- `POST /events` mockado;
- `GET /recommendations` mockado;
- widget JavaScript local;
- `widget/demo.html`;
- Docker Compose com PostgreSQL preparado;
- `.env.example`;
- `backend/requirements.txt`;
- `backend/Dockerfile`;
- `data/products_seed.csv` com 3 produtos mockados;
- documentação básica.

### Não implementar na Fase 1 técnica local

- banco persistente conectado;
- SQLAlchemy models completos;
- ranking real;
- fuzzy;
- ontologia;
- integração Tray;
- crawler;
- scraping;
- painel;
- login;
- deploy;
- multi-loja;
- testes A/B;
- MLflow ou DVC;
- estudo com usuários.

---

## Objetivo principal

Construir de forma incremental:

1. backend FastAPI;
2. widget JavaScript;
3. eventos mockados;
4. recomendações mockadas;
5. banco PostgreSQL preparado;
6. persistência real em fase posterior;
7. recomendador por regras em fase posterior;
8. fuzzy v1 em fase posterior;
9. documentação técnica e acadêmica.

O projeto deve ser útil comercialmente e defensável academicamente, mas a primeira entrega deve ser pequena e executável.

---

## Como trabalhar neste repositório

Antes de qualquer alteração:

1. leia `AGENTS.md`;
2. leia este arquivo;
3. leia `README.md`, se existir;
4. leia `docs/COMECAR.md`;
5. consulte `docs/deep-research-report.md` apenas como contexto;
6. inspecione a árvore de arquivos;
7. rode `git status`;
8. identifique a fase atual do projeto;
9. faça um plano curto;
10. implemente em passos pequenos.

Comandos úteis para inspeção:

```bash
find . -maxdepth 3 -type f | sort
git status
```

Não reescreva o projeto inteiro sem necessidade. Prefira patches pequenos, testáveis e documentados.

---

## Prioridade absoluta

A prioridade é fazer o ciclo mínimo funcionar:

```text
demo.html -> widget JS -> API -> recomendação mockada -> evento recebido
```

Antes de implementar fuzzy, ontologia, painel, app Tray ou integração avançada, garanta que:

- a API responde;
- o widget renderiza;
- o evento chega;
- a recomendação aparece;
- o clique é registrado.

---

## Escopo atual

### Incluído na primeira fase

- Python + FastAPI.
- Docker Compose.
- PostgreSQL preparado.
- JavaScript puro para widget.
- Recomendações mockadas.
- Eventos anônimos mockados.
- CSV com 3 produtos mockados.
- Documentação básica do MVP.

### Incluído em fases posteriores

- PostgreSQL conectado via SQLAlchemy/SQLModel.
- Tabelas.
- CSV manual de 30 a 50 produtos.
- Importação de produtos.
- Recomendação por regras.
- Eventos salvos.
- CTR calculável.
- Fuzzy v1.
- Ontologia mínima.
- Baselines acadêmicos.

### Excluído por enquanto

- Login.
- Painel completo.
- Multi-tenant.
- App Tray homologado.
- LLM no motor.
- Deep learning.
- Ontologia OWL grande.
- Dados pessoais.
- Checkout tracking completo.
- Crawler/scraping.
- Deploy em produção.

---

## Regras de segurança

Nunca:

- versionar `.env`;
- expor credenciais no widget;
- colocar token privado no frontend;
- coletar CPF, e-mail, telefone ou endereço;
- capturar mensagens de WhatsApp;
- consultar API da Tray diretamente pelo navegador do visitante;
- instalar código no site real sem etapa de teste controlada;
- quebrar a renderização da página caso a API falhe.

O widget deve falhar silenciosamente, com no máximo `console.warn`.

---

## LGPD

Coletar apenas dados anônimos no MVP:

```text
anonymous_id
session_id
event_type
page_url
product_id
widget_id
recommended_product_id
timestamp
metadata não sensível
```

Não coletar:

```text
nome
CPF
e-mail
telefone
endereço
dados de pagamento
dados sensíveis
conteúdo de formulários
```

Sempre documentar novos eventos em `docs/EVENTS.md`.

---

## Estrutura alvo

### Fase 1 técnica local

```text
backend/
  app/
    __init__.py
    main.py
    schemas.py
    recommender.py
    settings.py
  requirements.txt
  Dockerfile

widget/
  kouzina-reco.js
  demo.html

data/
  products_seed.csv

docs/
  MVP.md
  API.md
  EVENTS.md
  DATA_MODEL.md
  TCC_NOTES.md

docker-compose.yml
.env.example
.gitignore
README.md
```

### Fases posteriores

```text
backend/
  app/
    database.py
    models.py
    seed.py
  tests/

data/
  product_taxonomy.csv

docs/
  RECOMMENDER.md
  FUZZY_MODEL.md
```

Ao criar arquivos, mantenha esta estrutura simples.

---

## Contratos de API

Não quebrar esses contratos sem atualizar documentação e testes.

### `GET /health`

Deve retornar status do serviço.

Resposta esperada:

```json
{
  "status": "ok",
  "service": "kouzina-reco-api",
  "version": "0.1.0"
}
```

Pode incluir `timestamp`, se documentado.

### `POST /events`

Na Fase 1, deve receber evento do widget, validar payload e retornar confirmação. Não precisa salvar no banco ainda.

Campos esperados:

```json
{
  "event_type": "page_view",
  "anonymous_id": "anon_123",
  "session_id": "sess_456",
  "page_url": "https://www.kouzinaclub.com.br/produto-x",
  "product_id": "12345",
  "widget_id": "product-page",
  "recommended_product_id": "67890",
  "metadata": {}
}
```

Resposta esperada:

```json
{
  "received": true,
  "event_type": "page_view",
  "timestamp": "2026-04-29T00:00:00Z"
}
```

### `GET /recommendations`

Na Fase 1, deve retornar recomendações mockadas.

Parâmetros:

```text
product_id, opcional
widget_id, opcional
anonymous_id, opcional em fase futura
```

Resposta esperada:

```json
{
  "widget_title": "Complete seu projeto",
  "product_id": "12345",
  "recommendations": [
    {
      "product_id": "mock-001",
      "name": "Cooktop premium compatível",
      "url": "https://www.kouzinaclub.com.br/",
      "image_url": null,
      "price": 9990.0,
      "reason": "Produto complementar para composição de cozinha gourmet.",
      "score": 0.92
    }
  ]
}
```

---

## Widget JavaScript

O widget deve:

- usar JavaScript puro;
- ler `window.KouzinaReco`;
- procurar containers `[data-kouzina-reco]`;
- criar `anonymous_id` no `localStorage`;
- criar `session_id` no `sessionStorage`;
- detectar `product_id` quando possível;
- enviar `page_view`;
- buscar recomendações;
- renderizar cards;
- enviar `recommendation_impression`;
- enviar `recommendation_click`;
- enviar `recommended_product_id` como campo opcional no evento de clique;
- não depender de frameworks;
- não afetar CSS global do site;
- falhar com `console.warn`, sem quebrar a página.

Configuração esperada:

```html
<script>
  window.KouzinaReco = {
    apiBaseUrl: "http://localhost:8000",
    publicKey: "kouzina_public_dev_key"
  };
</script>
<script src="./kouzina-reco.js"></script>
```

Container esperado:

```html
<div data-kouzina-reco="product-page"></div>
```

### Teste local do widget

Não depender de `file://`.

Servir o widget assim:

```bash
cd widget
python -m http.server 5500
```

Abrir:

```text
http://localhost:5500/demo.html
```

O backend deve liberar CORS para:

```text
http://localhost:5500
```

---

## Recomendador v0

Não implementar na Fase 1 técnica local, a menos que o usuário peça explicitamente.

Quando chegar a fase do recomendador real, começar simples.

Critérios:

- complementaridade de tipo;
- disponibilidade;
- mesma voltagem;
- faixa de preço próxima;
- mesma marca;
- mesmo ambiente;
- nível premium semelhante;
- exclusão do próprio produto.

Relações iniciais:

```python
COMPLEMENTARY_TYPES = {
    "Coifa": ["Cooktop", "Forno", "Dominó"],
    "Cooktop": ["Coifa", "Forno", "Dominó"],
    "Adega": ["Cervejeira", "Frigobar", "Churrasqueira"],
    "Churrasqueira": ["Adega", "Cervejeira", "Coifa", "Cooktop"],
    "Forno": ["Cooktop", "Coifa"],
}
```

Cada recomendação deve ter `reason`.

---

## Fuzzy v1

Só implementar depois do ranking por regras estar funcionando.

Variáveis iniciais:

```text
compatibilidade_tecnica
afinidade_ambiente
proximidade_preco
similaridade_premium
disponibilidade
```

Score inicial:

```python
final_score = (
    0.35 * compatibilidade_tecnica +
    0.25 * afinidade_ambiente +
    0.20 * proximidade_preco +
    0.10 * similaridade_premium +
    0.10 * disponibilidade
)
```

Documentar funções de pertinência em `docs/FUZZY_MODEL.md`.

---

## Ontologia

Não começar por OWL completo.

Primeiro representar o domínio de modo simples:

```text
Produto
  Coifa
  Cooktop
  Adega
  Churrasqueira
  Forno
  Cervejeira
  Frigobar
  Dominó

Ambiente
  CozinhaPlanejada
  CozinhaGourmet
  EspacoGourmet
  VarandaGourmet
  AreaChurrasco
```

Relações:

```text
complementa
substitui
compativelCom
pertenceAoAmbiente
temVoltagem
temMarca
temFaixaPreco
```

A formalização OWL/Protégé entra depois que o MVP já estiver recomendando produtos.

---

## Comandos de desenvolvimento

### Banco

```bash
docker compose up -d
```

### API

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Windows:

```bash
.venv\Scripts\activate
```

### Widget demo

```bash
cd widget
python -m http.server 5500
```

Abrir:

```text
http://localhost:5500/demo.html
```

### Testes

```bash
cd backend
pytest
```

Se `pytest` ainda não existir, não criar suíte grande sem necessidade. Em fase de revisão, criar testes mínimos para:

- health;
- events;
- recommendations.

---

## Critérios de qualidade

Antes de considerar uma tarefa concluída:

- rodar testes disponíveis;
- testar endpoint alterado manualmente quando possível;
- verificar se o widget ainda carrega;
- verificar se a API não expõe segredos;
- atualizar documentação;
- explicar limitações.

Se não conseguiu executar algum teste, diga claramente.

---

## Estilo de resposta ao finalizar uma tarefa

Ao terminar, responda com:

```text
Resumo:
- ...

Arquivos alterados:
- ...

Testes/comandos executados:
- ...

Como validar:
- ...

Pendências:
- ...
```

---

## Coisas a evitar

Evite:

- criar arquitetura enterprise cedo demais;
- adicionar dependências sem necessidade;
- criar painel antes de ter eventos;
- implementar fuzzy antes de ranking simples;
- formalizar ontologia antes do catálogo mínimo;
- conectar Tray antes de ter CSV/manual/mock funcionando;
- mudar contratos de API sem documentação;
- usar dados pessoais;
- bloquear renderização do site;
- reescrever documentação grande sem necessidade;
- avançar para fases futuras por conta própria.

---

## Ordem recomendada de implementação

### Fase 1 técnica local

1. `GET /health`.
2. `POST /events` mockado.
3. `GET /recommendations` mockado.
4. `widget/demo.html`.
5. `widget/kouzina-reco.js`.
6. `docker-compose.yml`.
7. `.env.example`.
8. `backend/requirements.txt`.
9. `backend/Dockerfile`.
10. `data/products_seed.csv` com 3 produtos mockados.
11. README atualizado.

### Fase 2: persistência e catálogo inicial

1. PostgreSQL conectado.
2. tabelas.
3. eventos salvos.
4. CSV de produtos.
5. importação de produtos.

### Fase 3: recomendador v0

1. ranking por regras.
2. recomendações reais.
3. motivos textuais.
4. CTR calculável.

### Fases futuras

1. deploy HTTPS.
2. teste controlado no site.
3. fuzzy v1.
4. ontologia.
5. baseline acadêmico.
6. painel.
7. integração Tray futura.

---

## Definição de pronto

### Fase 1 técnica local pronta

- o widget aparece em `demo.html`;
- a API retorna recomendações mockadas;
- o clique em recomendação dispara evento;
- `/health` responde;
- `/events` valida payload;
- `/recommendations` retorna JSON no contrato esperado;
- não há dados pessoais;
- documentação mínima explica como rodar.

### MVP completo pronto

- a API retorna recomendações reais;
- eventos são salvos;
- o catálogo tem 30 a 50 produtos;
- há motivo textual para cada recomendação;
- é possível calcular CTR;
- a documentação explica API, eventos, dados e recomendador;
- a solução pode ser instalada de forma controlada no site da Kouzina.

---

## Diretriz final

Sempre priorize a próxima entrega que torne o produto mais real, mensurável e simples de validar.

O projeto só deve ficar mais sofisticado depois que o ciclo abaixo estiver funcionando:

```text
visitante vê produto -> widget aparece -> recomendação é exibida -> visitante clica -> evento é recebido/salvo -> métrica é calculada
```
