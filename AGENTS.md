# AGENTS.md

## Projeto: Kouzina Reco MVP

Este repositório implementa o MVP comercial mínimo de um sistema de recomendação para o site Kouzina Club, com evolução acadêmica futura para um sistema de recomendação híbrido baseado em ontologia fuzzy.

O objetivo imediato é criar um produto funcional, simples e mensurável:

1. uma API de recomendação;
2. um widget JavaScript instalável no site;
3. registro de eventos anônimos;
4. recomendações mockadas na primeira fase;
5. evolução posterior para catálogo, ranking por regras, fuzzy e ontologia;
6. documentação suficiente para apoiar o TCC e a futura monetização.

Este arquivo orienta agentes de código como Codex, Claude Code, Copilot, Cursor, Devin-like agents e outros assistentes automatizados que forem trabalhar neste projeto.

---

## 0. Estado atual e hierarquia de documentos

Este repositório está em fase inicial. Quando o usuário pedir para "começar", "implementar o MVP", "criar a primeira versão" ou "iniciar o projeto", o agente deve primeiro identificar a fase solicitada e não assumir que todo o plano acadêmico deve ser implementado de uma vez.

### Hierarquia de leitura

Use esta ordem de prioridade:

1. solicitação atual do usuário;
2. `AGENTS.md`;
3. `CLAUDE.md`, quando estiver usando Claude Code;
4. `docs/COMECAR.md`;
5. `SKILL.md`;
6. `docs/deep-research-report.md` apenas como contexto acadêmico e visão futura;
7. demais arquivos em `docs/` como referências complementares.

### Papel de cada documento

- `AGENTS.md`: regras gerais, limites de escopo, contratos e padrões para qualquer agente.
- `CLAUDE.md`: regras operacionais específicas para Claude Code.
- `docs/COMECAR.md`: guia operacional principal para começar a implementação.
- `SKILL.md`: playbook complementar do projeto.
- `docs/deep-research-report.md`: base acadêmica e visão completa de TCC, não backlog imediato.
- `README.md`: instruções de execução para humanos.

### Regra sobre o relatório de pesquisa

`docs/deep-research-report.md` não autoriza implementar crawler, scraping, ontologia, fuzzy, baselines, painel, estudo com usuários, MLflow, DVC, CEP, deploy ou infraestrutura acadêmica sem pedido explícito.

Use esse relatório apenas para entender o objetivo científico e a direção de longo prazo.

---

## 1. Missão do MVP

Construir um widget JavaScript plugável no site da Kouzina que:

- identifica o contexto da página de produto;
- chama uma API própria;
- exibe recomendações de produtos compatíveis;
- registra eventos de impressão e clique;
- permite medir CTR e engajamento;
- prepara a base para recomendação semântico-fuzzy.

A primeira versão deve funcionar mesmo sem ontologia completa, sem app Tray homologado, sem domínio próprio e sem integração real com o catálogo da Tray.

---

## 2. Fase atual padrão: Fase 1 técnica local

Se o usuário pedir para iniciar o projeto do zero ou começar o MVP, implementar somente a **Fase 1 técnica local**.

### A Fase 1 técnica local inclui

- backend FastAPI mínimo;
- `GET /health`;
- `POST /events` mockado;
- `GET /recommendations` mockado;
- `widget/kouzina-reco.js`;
- `widget/demo.html`;
- `docker-compose.yml` com PostgreSQL;
- `.env.example`;
- `.gitignore`, se necessário;
- `backend/requirements.txt`;
- `backend/Dockerfile`;
- `data/products_seed.csv` com 3 produtos mockados;
- README atualizado;
- documentação mínima complementar.

### A Fase 1 técnica local não inclui

- banco persistente conectado;
- SQLAlchemy models completos;
- seed real de 30 a 50 produtos;
- ranking v0 real;
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
- MLflow, DVC ou pipeline acadêmico completo.

### Critério de sucesso da Fase 1 técnica local

A Fase 1 está pronta quando:

1. a API roda localmente;
2. `/health` responde;
3. `/events` recebe e valida payload;
4. `/recommendations` retorna recomendações mockadas;
5. `widget/demo.html` carrega o widget;
6. o widget renderiza recomendações;
7. o widget envia `page_view`;
8. o widget envia `recommendation_impression`;
9. o widget envia `recommendation_click`;
10. nenhum dado pessoal é coletado.

---

## 3. Escopo do MVP completo

O MVP completo é maior que a Fase 1 técnica local.

### MVP completo deve conter futuramente

- Backend em Python com FastAPI.
- Banco PostgreSQL.
- Endpoint `GET /health`.
- Endpoint `POST /events`.
- Endpoint `GET /recommendations`.
- Widget em JavaScript puro.
- Página local `widget/demo.html`.
- Cadastro inicial manual de 30 a 50 produtos em CSV.
- Ranking inicial por regras.
- Motivos textuais para cada recomendação.
- Registro dos eventos:
  - `page_view`;
  - `product_view`;
  - `recommendation_impression`;
  - `recommendation_click`.
- Cálculo básico de CTR.
- Base para fuzzy v1.

### MVP completo não deve conter inicialmente

- Login de usuários.
- Painel administrativo complexo.
- App Tray homologado.
- Deep learning.
- LLM no motor de recomendação.
- Neo4j obrigatório.
- FuzzyDL obrigatório.
- Ontologia OWL grande.
- Sistema multi-loja.
- Checkout tracking avançado.
- Captura de dados pessoais identificáveis.

---

## 4. Regras de ouro para agentes

1. **Não superdimensionar o projeto.** Priorizar o MVP mensurável antes de fuzzy, ontologia formal e painéis avançados.
2. **Não avançar de fase sem autorização explícita.** Se o usuário pedir Fase 1, entregar apenas Fase 1.
3. **Não colocar segredo no JavaScript.** O widget pode conter `publicKey`, `storeId` e URL pública da API; nunca tokens privados.
4. **Não coletar dados pessoais no MVP.** Usar apenas `anonymous_id`, `session_id`, `event_type`, `page_url`, `product_id`, `widget_id`, `recommended_product_id` e `metadata` não sensível.
5. **Não consultar a API da Tray diretamente pelo widget.** O backend deve sincronizar/cachear catálogo em fase futura.
6. **Não quebrar o site da Kouzina.** O widget deve falhar silenciosamente em caso de erro.
7. **Não bloquear renderização da página.** O script deve carregar de forma assíncrona e leve.
8. **Não alterar código de produção sem confirmação humana.** Criar primeiro demo local, depois teste controlado.
9. **Sempre manter documentação atualizada.** Cada mudança relevante deve refletir em `README.md` ou `docs/`.
10. **Toda recomendação deve ter uma razão textual.** Isso apoia explicabilidade e TCC.
11. **Toda feature deve gerar algum dado mensurável.** O foco comercial é medir impressões, cliques e engajamento.
12. **Preservar documentos existentes.** Não apagar `docs/`, `AGENTS.md`, `CLAUDE.md`, `SKILL.md` ou relatórios sem pedido explícito.

---

## 5. Stack padrão

### Backend

- Python 3.11+
- FastAPI
- Uvicorn
- Pydantic
- Pydantic Settings
- SQLAlchemy ou SQLModel em fase posterior
- PostgreSQL
- pandas para importação inicial em fase posterior
- pytest para testes em fase posterior

### Widget

- JavaScript puro
- Sem React na versão inicial
- Sem Vue, Angular ou Next.js dentro do widget
- CSS isolado inline, escopado ou com prefixo próprio
- Carregamento assíncrono

### Infra local

- Docker Compose
- PostgreSQL em container
- `.env` para configurações locais
- `.env.example` versionado
- GitHub para versionamento

### Evolução posterior

- Redis para cache
- Alembic para migrations
- Sentry para erros
- PostHog/Plausible ou dashboard próprio
- Owlready2/RDFLib para ontologia
- scikit-fuzzy ou implementação própria para fuzzy
- app Tray homologado em fase futura

---

## 6. Estrutura esperada do repositório

### Estrutura mínima da Fase 1 técnica local

```text
kouzina-reco/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── schemas.py
│   │   ├── recommender.py
│   │   └── settings.py
│   │
│   ├── requirements.txt
│   └── Dockerfile
│
├── widget/
│   ├── kouzina-reco.js
│   └── demo.html
│
├── data/
│   └── products_seed.csv
│
├── docs/
│   ├── MVP.md
│   ├── API.md
│   ├── EVENTS.md
│   ├── DATA_MODEL.md
│   └── TCC_NOTES.md
│
├── docker-compose.yml
├── .env.example
├── .gitignore
├── AGENTS.md
├── CLAUDE.md
├── SKILL.md
└── README.md
```

### Estrutura futura do MVP completo

```text
kouzina-reco/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── recommender.py
│   │   ├── seed.py
│   │   └── settings.py
│   │
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
│
├── widget/
│   ├── kouzina-reco.js
│   └── demo.html
│
├── data/
│   ├── products_seed.csv
│   └── product_taxonomy.csv
│
├── docs/
│   ├── MVP.md
│   ├── API.md
│   ├── EVENTS.md
│   ├── DATA_MODEL.md
│   ├── RECOMMENDER.md
│   ├── FUZZY_MODEL.md
│   └── TCC_NOTES.md
│
├── docker-compose.yml
├── .env.example
├── .gitignore
├── AGENTS.md
├── CLAUDE.md
├── SKILL.md
└── README.md
```

Não criar pastas grandes ou complexas antes da necessidade real.

---

## 7. Variáveis de ambiente

Usar `.env.example` como fonte de referência:

```env
APP_NAME=Kouzina Reco API
ENVIRONMENT=local
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/kouzina_reco
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5500,http://localhost:8000,https://www.kouzinaclub.com.br,https://kouzinaclub.com.br
PUBLIC_WIDGET_KEY=kouzina_public_dev_key
```

Nunca versionar `.env`.

O `http://localhost:5500` deve ser permitido porque o `widget/demo.html` deve ser servido por um servidor local simples, por exemplo:

```bash
cd widget
python -m http.server 5500
```

Depois abrir:

```text
http://localhost:5500/demo.html
```

Evitar testar o widget por `file://`, pois isso pode gerar origem `null` e problemas de CORS.

---

## 8. Contratos mínimos da API

### `GET /health`

Retorna status do serviço.

Resposta esperada na Fase 1:

```json
{
  "status": "ok",
  "service": "kouzina-reco-api",
  "version": "0.1.0"
}
```

Resposta futura aceitável:

```json
{
  "status": "ok",
  "service": "kouzina-reco-api",
  "version": "0.1.0",
  "timestamp": "2026-04-29T00:00:00Z"
}
```

### `POST /events`

Recebe evento do widget.

Na Fase 1, apenas valida o payload e retorna confirmação. Não precisa salvar no banco.

Request:

```json
{
  "event_type": "recommendation_click",
  "anonymous_id": "anon_123",
  "session_id": "sess_456",
  "page_url": "https://www.kouzinaclub.com.br/produto-x",
  "product_id": "12345",
  "widget_id": "product-page",
  "recommended_product_id": "67890",
  "metadata": {}
}
```

Resposta:

```json
{
  "received": true,
  "event_type": "recommendation_click",
  "timestamp": "2026-04-29T00:00:00Z"
}
```

### `GET /recommendations`

Parâmetros:

```text
product_id, opcional
widget_id, opcional
anonymous_id, opcional em fase futura
```

Exemplo:

```text
GET /recommendations?product_id=12345&widget_id=product-page
```

Resposta:

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

## 9. Modelo de dados mínimo futuro

Na Fase 1 técnica local, não é obrigatório implementar as tabelas. Apenas preparar PostgreSQL via Docker Compose e documentar o modelo.

### `stores`

Representa uma loja.

Campos principais:

- `id`
- `slug`
- `name`
- `domain`
- `public_key`
- `created_at`

### `products`

Representa produto sincronizado ou cadastrado manualmente.

Campos principais:

- `id`
- `store_id`
- `external_id`
- `name`
- `url`
- `image_url`
- `category`
- `subcategory`
- `brand`
- `price`
- `promotional_price`
- `available`
- `availability_text`
- `stock`
- `voltage`
- `width_cm`
- `installation_type`
- `product_type`
- `environment`
- `premium_level`
- `description`
- `active`

### `manual_product_relations`

Relações manuais entre produtos.

Tipos aceitos inicialmente:

- `complements`
- `substitutes`
- `same_line`
- `same_environment`
- `upsell`
- `cross_sell`

### `recommendation_events`

Eventos capturados pelo widget.

Campos principais:

- `event_type`
- `anonymous_id`
- `session_id`
- `page_url`
- `product_external_id`
- `widget_id`
- `recommended_product_external_id`
- `metadata`
- `created_at`

---

## 10. Eventos permitidos

Usar estes nomes exatamente na versão inicial:

```text
page_view
product_view
recommendation_impression
recommendation_click
```

Eventos futuros:

```text
category_view
search
add_to_cart
whatsapp_click
checkout_start
purchase
```

Não adicionar novos eventos sem atualizar `docs/EVENTS.md`.

---

## 11. Widget JavaScript

### Requisitos

- Deve funcionar com JavaScript puro.
- Deve ler `window.KouzinaReco`.
- Deve procurar containers com `[data-kouzina-reco]`.
- Deve criar `anonymous_id` no `localStorage`.
- Deve criar `session_id` no `sessionStorage`.
- Deve enviar `page_view`.
- Deve chamar `/recommendations`.
- Deve renderizar cards.
- Deve registrar `recommendation_impression`.
- Deve registrar `recommendation_click`.
- Deve enviar `recommended_product_id` como campo opcional de evento.
- Deve falhar com `console.warn`, nunca com erro fatal.
- Deve evitar estilos globais que afetem a loja.

### Configuração esperada

```html
<script>
  window.KouzinaReco = {
    apiBaseUrl: "https://api.exemplo.com",
    publicKey: "kouzina_public_key"
  };
</script>
<script async src="https://cdn.exemplo.com/kouzina-reco.js"></script>
```

### Container esperado

```html
<div data-kouzina-reco="product-page"></div>
```

Se não houver container, o agente pode implementar criação automática, mas somente depois da versão manual estar validada em `demo.html`.

---

## 12. Recomendador v0 por regras

Implementar apenas depois da Fase 1 técnica local.

### Relações complementares iniciais

```python
COMPLEMENTARY_TYPES = {
    "Coifa": ["Cooktop", "Forno", "Dominó"],
    "Cooktop": ["Coifa", "Forno", "Dominó"],
    "Adega": ["Cervejeira", "Frigobar", "Churrasqueira"],
    "Churrasqueira": ["Adega", "Cervejeira", "Coifa", "Cooktop"],
    "Forno": ["Cooktop", "Coifa"],
}
```

### Critérios de pontuação

- `+30` se o tipo do candidato complementa o tipo do produto atual.
- `+20` se o candidato está disponível.
- `+15` se tem mesma voltagem.
- `+15` se tem faixa de preço próxima.
- `+10` se tem mesma marca.
- `+10` se pertence ao mesmo ambiente.
- `+10` se tem nível premium semelhante.
- `-100` se for o mesmo produto.
- `-30` se estiver indisponível.

Cada recomendação deve retornar pelo menos uma razão textual.

---

## 13. Fuzzy v1

Só implementar depois que o ranking v0 estiver funcionando e validado.

### Variáveis fuzzy iniciais

- `compatibilidade_tecnica`
- `afinidade_ambiente`
- `proximidade_preco`
- `similaridade_premium`
- `disponibilidade`

### Fórmula inicial aceitável

```python
final_score = (
    0.35 * compatibilidade_tecnica +
    0.25 * afinidade_ambiente +
    0.20 * proximidade_preco +
    0.10 * similaridade_premium +
    0.10 * disponibilidade
)
```

Documentar tudo em `docs/FUZZY_MODEL.md`.

---

## 14. Ontologia mínima

A ontologia formal pode começar como documentação e tabelas no banco. OWL/Protégé entram depois.

### Classes iniciais

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

AtributoTecnico
  Voltagem
  Largura
  TipoInstalacao
  Marca
  FaixaPreco
  Disponibilidade
```

### Relações iniciais

```text
complementa
substitui
compativelCom
pertenceAoAmbiente
temVoltagem
temMarca
temFaixaPreco
temTipoInstalacao
```

Não começar com ontologia grande. Priorizar poucas classes úteis ao widget.

---

## 15. Comandos úteis

### Rodar banco

```bash
docker compose up -d
```

### Rodar API local

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

No Windows, ativar ambiente com:

```bash
.venv\Scripts\activate
```

### Servir widget demo

```bash
cd widget
python -m http.server 5500
```

Abrir:

```text
http://localhost:5500/demo.html
```

### Testar API

```bash
curl http://localhost:8000/health
```

### Rodar testes

```bash
cd backend
pytest
```

Se ainda não houver testes, não criar uma suíte grande na Fase 1. Criar testes mínimos apenas se a tarefa pedir revisão ou validação.

---

## 16. Processo de desenvolvimento para agentes

Antes de editar:

1. Ler `AGENTS.md`.
2. Ler `CLAUDE.md`, se estiver usando Claude Code.
3. Ler `README.md`, se existir.
4. Ler `docs/COMECAR.md`.
5. Consultar `docs/deep-research-report.md` apenas como contexto.
6. Inspecionar estrutura de pastas.
7. Rodar `git status`.
8. Identificar fase atual do MVP.
9. Evitar reescrever tudo.
10. Fazer mudança pequena e testável.

Ao implementar:

1. Criar ou alterar arquivos mínimos.
2. Manter nomes de endpoints estáveis.
3. Atualizar documentação essencial.
4. Criar testes quando houver lógica real.
5. Rodar testes disponíveis quando possível.
6. Reportar o que foi alterado.

Ao finalizar:

1. Informar arquivos modificados.
2. Informar comandos executados.
3. Informar testes realizados.
4. Informar próximos passos concretos.
5. Informar limitações ou pendências.

---

## 17. Critérios de conclusão

### Fase 1 técnica local concluída

- `GET /health` responde.
- `POST /events` recebe eventos mockados.
- `GET /recommendations` retorna produtos mockados.
- `widget/demo.html` renderiza recomendações.
- O widget registra impressão.
- O widget registra clique.
- `docker-compose.yml` existe com PostgreSQL.
- `data/products_seed.csv` existe com 3 produtos mockados.
- Documentação básica está atualizada.

### MVP completo concluído

- `POST /events` salva eventos.
- `GET /recommendations` retorna produtos reais.
- Existem 30 a 50 produtos no catálogo.
- O ranking v0 usa regras semânticas.
- Cada recomendação tem razão textual.
- CTR pode ser calculado.
- A documentação explica API, eventos, dados e recomendador.

---

## 18. LGPD e privacidade

No MVP, coletar somente dados anônimos.

Permitido:

- `anonymous_id`
- `session_id`
- `event_type`
- `page_url`
- `product_id`
- `widget_id`
- `recommended_product_id`
- `timestamp`
- metadados técnicos não sensíveis

Não permitido:

- nome;
- CPF;
- e-mail;
- telefone;
- endereço;
- dados de pagamento;
- dados sensíveis;
- conteúdo de formulários;
- mensagens de WhatsApp.

Todo evento deve ter finalidade ligada à recomendação, mensuração ou melhoria do widget.

---

## 19. Segurança

- Nunca versionar `.env`.
- Nunca expor token privado no widget.
- Validar `publicKey` no backend em fase posterior.
- Configurar CORS de forma restrita.
- Sanitizar dados recebidos no backend.
- Evitar armazenar dados pessoais.
- Criar logs sem dados sensíveis.
- Preparar rate limiting em fase posterior.

---

## 20. Estilo de código

### Python

- Usar type hints.
- Preferir funções pequenas.
- Separar schemas, modelos, banco e recomendador.
- Evitar lógica de recomendação dentro de `main.py`.
- Usar nomes claros em inglês para código.
- Usar comentários apenas quando explicarem regra de negócio.

### JavaScript

- Usar IIFE ou módulo simples.
- Evitar dependências externas.
- Evitar poluir escopo global além de `window.KouzinaReco`.
- Não quebrar a página se a API falhar.
- Usar `localStorage` apenas para `anonymous_id`.
- Usar `sessionStorage` para `session_id`.
- Usar `data-*` attributes para eventos e containers.

### Documentação

- Português do Brasil.
- Explicar decisões técnicas.
- Registrar limitações.
- Manter exemplos de payloads.

---

## 21. Prioridade de tarefas

A ordem correta é:

1. API mínima.
2. Widget local.
3. Eventos mockados.
4. Docker/PostgreSQL preparado.
5. Catálogo manual pequeno.
6. Eventos salvos.
7. Catálogo manual de 30 a 50 produtos.
8. Ranking v0.
9. Recomendação real no demo.
10. Deploy HTTPS.
11. Teste controlado no site.
12. Fuzzy v1.
13. Ontologia formal.
14. Baselines acadêmicos.
15. Painel.
16. App Tray.
17. Monetização multi-loja.

Nunca inverter essa ordem sem motivo técnico forte e sem explicar a razão.

---

## 22. Entregáveis esperados por fase

### Fase 1 técnica local

- `GET /health`
- `POST /events` mockado
- `GET /recommendations` mockado
- `widget/kouzina-reco.js`
- `widget/demo.html`
- `docker-compose.yml`
- `.env.example`
- `data/products_seed.csv` com 3 produtos mockados
- README atualizado

### Fase 2: persistência e catálogo inicial

- PostgreSQL conectado
- tabelas
- seed de produtos
- eventos salvos

### Fase 3: recomendador v0

- ranking por regras
- produtos reais do CSV
- motivos textuais
- CTR calculável

### Fase 4: teste controlado

- API publicada em HTTPS
- widget publicado em URL pública
- instalação controlada no site
- relatório inicial de uso

### Fase 5: fuzzy e TCC

- fuzzy v1
- documentação fuzzy
- comparação com baseline simples
- preparação acadêmica

---

## 23. Instrução final para agentes

Ao receber uma tarefa neste repositório, trabalhar sempre para aproximar o projeto do MVP funcional e mensurável.

Evitar decisões que aumentem complexidade sem gerar valor imediato para:

1. widget funcionando;
2. recomendação exibida;
3. evento registrado;
4. métrica calculada;
5. base acadêmica documentada.
