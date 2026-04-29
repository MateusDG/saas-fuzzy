---
name: kouzina-reco-mvp
description: use this skill when the user asks to plan, build, debug, document, review, or evolve the kouzina reco mvp, a javascript widget and fastapi recommendation api for the kouzina club e-commerce, including phase-based mvp implementation, recommendation rules, fuzzy scoring, ontology planning, lgpd-safe analytics, commercial scope, and tcc-oriented documentation.
---

# Kouzina Reco MVP Skill

## Objetivo

Ajudar a criar, revisar e evoluir o projeto `kouzina-reco` ou `saas-fuzzy`: um MVP comercial mínimo de recomendação de produtos para a Kouzina Club, com API própria, widget JavaScript, coleta de eventos, recomendação por regras e evolução futura para ontologia fuzzy.

Use este skill como guia operacional quando a tarefa envolver:

- backend FastAPI;
- widget JavaScript;
- coleta de eventos;
- modelagem de catálogo;
- recomendador por regras;
- fuzzy v1;
- ontologia de produtos;
- documentação do MVP;
- documentação do TCC;
- monetização futura como API/widget para e-commerce.

---

## Princípio central

Priorizar sempre o MVP funcional antes da sofisticação acadêmica.

A ordem correta é:

```text
api mínima -> widget local -> evento recebido -> recomendação exibida -> clique medido -> eventos salvos -> ranking v0 -> fuzzy v1 -> ontologia formal -> baseline acadêmico -> monetização
```

Não começar por OWL completo, deep learning, LLM, painel complexo, crawler, integração Tray ou app Tray homologado.

---

## Hierarquia de execução

Quando este skill for usado dentro do projeto `kouzina-reco` ou `saas-fuzzy`, considerar:

1. `AGENTS.md` como regras gerais para agentes;
2. `CLAUDE.md` como regras específicas para Claude Code;
3. `docs/COMECAR.md` como guia operacional principal;
4. `SKILL.md` como playbook complementar;
5. `docs/deep-research-report.md` apenas como contexto acadêmico e visão futura.

Não repetir toda a documentação no prompt se os arquivos já estiverem no repositório.

Antes de implementar, identificar a fase solicitada pelo usuário.

---

## Regra anti-escopo

Se o usuário pedir para iniciar, começar ou criar o MVP pela primeira vez, executar somente a próxima fase pendente.

A fase inicial padrão é a **Fase 1 técnica local**.

Não implementar fuzzy, ontologia, integração Tray, crawler, painel, login, deploy ou multi-loja antes de existir:

1. API mínima funcionando;
2. widget demo funcionando;
3. eventos mockados funcionando;
4. recomendações mockadas funcionando;
5. documentação básica atualizada.

`docs/deep-research-report.md` é contexto acadêmico e não backlog imediato. Não usar o relatório de pesquisa como autorização para implementar escopo avançado.

---

## Fase inicial obrigatória

Se o usuário pedir para iniciar, começar ou criar o MVP pela primeira vez, implementar somente a Fase 1 técnica local.

### Fase 1 técnica local inclui

1. API mínima;
2. `GET /health`;
3. `POST /events` mockado;
4. `GET /recommendations` mockado;
5. widget JavaScript local;
6. `widget/demo.html`;
7. Docker Compose com PostgreSQL preparado;
8. `.env.example`;
9. `backend/requirements.txt`;
10. `backend/Dockerfile`;
11. CSV mockado com 3 produtos;
12. documentação básica.

### Fase 1 técnica local não inclui

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
- MLflow;
- DVC;
- estudo com usuários.

---

## Escopo do MVP

### Fazer primeiro na Fase 1 técnica local

1. Criar API mínima:
   - `GET /health`;
   - `POST /events` mockado;
   - `GET /recommendations` mockado.

2. Criar widget:
   - `widget/kouzina-reco.js`;
   - `widget/demo.html`.

3. Preparar infraestrutura local:
   - `docker-compose.yml`;
   - `.env.example`;
   - `backend/requirements.txt`;
   - `backend/Dockerfile`.

4. Criar dados mockados:
   - `data/products_seed.csv` com 3 produtos coerentes com o nicho.

5. Atualizar documentação:
   - `README.md`;
   - `docs/MVP.md`;
   - `docs/API.md`;
   - `docs/EVENTS.md`;
   - `docs/DATA_MODEL.md`;
   - `docs/TCC_NOTES.md`, se aplicável.

### Fazer depois

1. Criar banco persistente:
   - `stores`;
   - `products`;
   - `manual_product_relations`;
   - `recommendation_events`.

2. Criar catálogo manual:
   - 30 a 50 produtos;
   - CSV inicial;
   - categorias, marcas, preço, voltagem, ambiente e tipo de produto.

3. Criar recomendador por regras:
   - complementaridade;
   - disponibilidade;
   - preço;
   - marca;
   - voltagem;
   - ambiente;
   - nível premium.

4. Coletar métricas:
   - impressões;
   - cliques;
   - CTR.

5. Evoluir:
   - fuzzy v1;
   - ontologia mínima;
   - baseline acadêmico;
   - deploy;
   - teste controlado no site.

### Evitar no início

- Login.
- Painel grande.
- Multi-loja.
- App Tray.
- LLM no motor.
- Deep learning.
- Ontologia grande.
- Captura de dados pessoais.
- Checkout tracking avançado.

---

## Arquitetura recomendada

### Fase 1 técnica local

```text
widget/demo.html
        |
        | script javascript local
        v
widget/kouzina-reco.js
        |
        | GET /recommendations
        | POST /events
        v
API FastAPI mockada
```

### MVP completo

```text
Site Kouzina / Tray
        |
        | script javascript
        v
Widget de recomendação
        |
        | GET /recommendations
        | POST /events
        v
API FastAPI
        |
        | ranking + eventos
        v
PostgreSQL
```

Evolução futura:

```text
PostgreSQL -> ranking v0 -> fuzzy score -> ontologia -> dashboard -> app Tray -> multi-loja
```

---

## Stack padrão

- Python 3.11+
- FastAPI
- PostgreSQL
- SQLAlchemy ou SQLModel em fase posterior
- Docker Compose
- JavaScript puro
- pandas para seed em fase posterior
- pytest para testes
- Owlready2/RDFLib somente na fase de ontologia
- scikit-fuzzy ou implementação própria somente após ranking v0

---

## Estrutura de arquivos

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
```

### Fases futuras

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

---

## Regras para gerar código

### Backend

- Manter `main.py` enxuto.
- Separar schemas, settings e recomendador.
- Na Fase 1, não criar banco persistente se a tarefa não pedir.
- Usar type hints.
- Usar Pydantic para entrada/saída.
- Validar campos de eventos.
- Não armazenar dados pessoais.
- Retornar mensagens de erro claras.
- Criar testes para lógica real quando ela existir.

### Widget

- Usar JavaScript puro.
- Não usar React, Vue ou Next.js dentro do widget inicial.
- Não poluir CSS global.
- Não quebrar a página se a API falhar.
- Usar `console.warn` para erros não fatais.
- Criar `anonymous_id` no `localStorage`.
- Criar `session_id` no `sessionStorage`.
- Chamar `/events`.
- Chamar `/recommendations`.
- Renderizar cards simples.
- Registrar impressões e cliques.
- Enviar `recommended_product_id` no evento de clique.

### Banco

- Na Fase 1, preparar PostgreSQL com Docker Compose, sem obrigar persistência.
- Em fase posterior, começar com schema simples.
- Não otimizar antes de ter dados.
- Usar índices apenas quando necessário.
- Registrar `created_at`.
- Manter `external_id` para o id do produto na loja.

---

## Contratos de API

### Health

```text
GET /health
```

Resposta mínima:

```json
{
  "status": "ok",
  "service": "kouzina-reco-api",
  "version": "0.1.0"
}
```

### Eventos

```text
POST /events
```

Payload:

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

### Recomendações

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

## Eventos permitidos

Na versão inicial, usar exatamente:

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

Atualizar `docs/EVENTS.md` sempre que um evento for criado ou alterado.

---

## Recomendador por regras

Implementar antes do fuzzy formal, mas somente após a Fase 1 técnica local.

### Relações iniciais

```python
COMPLEMENTARY_TYPES = {
    "Coifa": ["Cooktop", "Forno", "Dominó"],
    "Cooktop": ["Coifa", "Forno", "Dominó"],
    "Adega": ["Cervejeira", "Frigobar", "Churrasqueira"],
    "Churrasqueira": ["Adega", "Cervejeira", "Coifa", "Cooktop"],
    "Forno": ["Cooktop", "Coifa"],
}
```

### Score inicial

- `+30`: candidato complementa produto atual.
- `+20`: candidato disponível.
- `+15`: mesma voltagem.
- `+15`: preço próximo.
- `+10`: mesma marca.
- `+10`: mesmo ambiente.
- `+10`: nível premium semelhante.
- `-100`: é o mesmo produto.
- `-30`: indisponível.

Cada recomendação precisa ter pelo menos uma razão textual.

---

## Fuzzy v1

Implementar após o recomendador por regras estar funcionando.

### Variáveis

- `compatibilidade_tecnica`
- `afinidade_ambiente`
- `proximidade_preco`
- `similaridade_premium`
- `disponibilidade`

### Score sugerido

```python
final_score = (
    0.35 * compatibilidade_tecnica +
    0.25 * afinidade_ambiente +
    0.20 * proximidade_preco +
    0.10 * similaridade_premium +
    0.10 * disponibilidade
)
```

### Regras conceituais

```text
SE compatibilidade_tecnica é alta
E afinidade_ambiente é alta
E proximidade_preco é média ou alta
ENTÃO recomendação é alta
```

```text
SE produto atual é Coifa
E candidato é Cooktop
E ambiente é Cozinha Gourmet
ENTÃO recomendação é alta
```

```text
SE candidato está indisponível
ENTÃO reduzir recomendação
```

Documentar funções de pertinência em `docs/FUZZY_MODEL.md`.

---

## Ontologia mínima

Começar como taxonomia documentada, depois formalizar em OWL.

### Classes

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

### Relações

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

---

## LGPD e privacidade

Coletar somente dados anônimos no MVP.

Permitido:

- `anonymous_id`;
- `session_id`;
- `event_type`;
- `page_url`;
- `product_id`;
- `widget_id`;
- `recommended_product_id`;
- `timestamp`;
- metadados técnicos não sensíveis.

Proibido:

- nome;
- CPF;
- e-mail;
- telefone;
- endereço;
- dados de pagamento;
- dados sensíveis;
- conteúdo de formulários;
- mensagens de WhatsApp.

---

## Teste local do widget

Não depender de `file://`.

Usar:

```bash
cd widget
python -m http.server 5500
```

Abrir:

```text
http://localhost:5500/demo.html
```

Garantir CORS para:

```text
http://localhost:5500
```

---

## Critérios de pronto

### Fase 1 técnica local pronta

1. a API roda;
2. `/health` responde;
3. `/events` recebe evento mockado;
4. `/recommendations` retorna recomendações mockadas;
5. o widget funciona no `demo.html`;
6. eventos são recebidos;
7. cliques são registrados;
8. documentação foi atualizada;
9. não há segredo exposto;
10. não há coleta de dados pessoais;
11. há próximo passo claro.

### MVP completo pronto

1. eventos são salvos;
2. recomendações reais são exibidas;
3. ranking v0 funciona;
4. CTR é calculável;
5. fuzzy v1 está documentado;
6. há base para TCC.

---

## Resposta esperada ao usuário

Quando concluir uma tarefa, responder com:

```text
Resumo:
- ...

Arquivos criados/alterados:
- ...

Como rodar:
- ...

Como validar:
- ...

Próximo passo recomendado:
- ...
```

Se algo não foi feito ou não pôde ser testado, informar claramente.

---

## Ordem de execução sugerida

1. Criar/validar estrutura do repositório.
2. Criar API mínima.
3. Criar widget local.
4. Receber eventos mockados.
5. Preparar Docker/PostgreSQL.
6. Criar CSV mockado.
7. Salvar eventos.
8. Criar schema do banco.
9. Criar CSV real de produtos.
10. Importar produtos.
11. Implementar ranking v0.
12. Publicar API.
13. Testar no site de forma controlada.
14. Implementar fuzzy v1.
15. Criar documentação acadêmica.
16. Criar baseline.
17. Criar dashboard simples.
18. Planejar monetização multi-loja.

---

## Diretriz final

Sempre preferir a solução mais simples que permita medir valor real.

O projeto deve evoluir por evidência: primeiro cliques e eventos, depois ranking, fuzzy, ontologia e otimizações.
