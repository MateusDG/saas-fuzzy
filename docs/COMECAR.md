A melhor forma de começar é construir  **uma versão mínima comercial que funcione antes da ontologia fuzzy completa** .

Seu primeiro objetivo não é ainda “fazer o TCC inteiro”. Seu primeiro objetivo é:

> **Ter um script JavaScript instalado no site da Kouzina, chamando uma API sua, exibindo recomendações simples e registrando impressões e cliques.**

Depois disso, você evolui para a ontologia, fuzzy, métricas acadêmicas e monetização.

Abaixo está a documentação passo a passo para começar do zero.

---

# Documentação inicial do MVP comercial mínimo

## 1. Nome do projeto

Use um nome simples internamente:

```text
kouzina-reco
```

Nome comercial futuro:

```text
Smart Gourmet Recommendations
```

Nome acadêmico:

```text
Sistema de recomendação híbrido baseado em ontologia fuzzy para e-commerce premium de cozinha e área gourmet
```

---

# 2. O que será o MVP

## 2.1. Definição do MVP

O MVP será composto por:

```text
1. Um backend com API de recomendação
2. Um banco de dados com produtos e eventos
3. Um widget JavaScript instalável no site
4. Um algoritmo inicial de recomendação por regras
5. Registro de métricas comerciais
6. Estrutura preparada para evoluir para ontologia fuzzy
```

A Kouzina é um bom piloto porque o catálogo possui categorias e filtros ricos, como adegas, cervejeiras, churrasqueiras, coifas, cooktops, fornos, frigobar, marcas, voltagem, preço e disponibilidade. Isso favorece recomendação por compatibilidade, não apenas por popularidade. ([Kouzina Club](https://www.kouzinaclub.com.br/espaco-gourmet?utm_source=chatgpt.com "Espaço Gourmet | Kouzina Club"))

## 2.2. O que o MVP fará na primeira versão

Na página de produto da Kouzina, o widget exibirá:

```text
"Complete seu projeto"
3 ou 4 produtos recomendados
motivo simples da recomendação
botão "Ver produto"
```

Exemplo:

```text
Produto atual:
Coifa de Ilha 90cm 220V

Recomendações:
- Cooktop 5 queimadores 220V
- Forno de embutir premium
- Dominó compatível
- Produto da mesma linha/marca
```

## 2.3. O que o MVP não fará ainda

Na primeira versão, não faça:

```text
login de usuários
painel administrativo complexo
app Tray homologado
deep learning
LLM
Neo4j
sistema multi-loja
checkout tracking avançado
ontologia enorme
fuzzy formal completo
```

Essas coisas entram depois.

---

# 3. Arquitetura inicial

A arquitetura mínima será:

```text
Site Kouzina / Tray
        |
        | script JS instalado via GTM ou tema
        v
Widget de recomendação
        |
        | GET /recommendations
        | POST /events
        v
API FastAPI
        |
        | consulta produtos
        | calcula ranking
        | salva eventos
        v
PostgreSQL
```

A Tray permite instalar códigos externos via Google Tag Manager sem editar diretamente o HTML do tema, o que é ideal para começar com baixo risco. A própria documentação da Tray informa que o GTM permite incluir códigos na loja sem alterar diretamente o HTML do tema. ([Basede Conhecimento](https://basedeconhecimento.tray.com.br/hc/pt-br/articles/6762108858139-Como-Integrar-com-o-Google-Tag-Manager?utm_source=chatgpt.com "Como integrar o Google Tag Manager – Tray Tecnologia em Ecommerce LTDA"))

---

# 4. Stack recomendada para começar

## 4.1. Stack do MVP

Use esta stack:

```text
Linguagem backend: Python
Framework backend: FastAPI
Banco de dados: PostgreSQL
ORM ou acesso SQL: SQLAlchemy ou SQLModel
Frontend do widget: JavaScript puro
Containerização: Docker Compose
Versionamento: Git + GitHub
Deploy inicial: serviço com URL provisória
Instalação no site: Google Tag Manager
```

FastAPI é uma boa escolha porque gera documentação interativa automaticamente em `/docs` e documentação alternativa em `/redoc`, além de ser baseado em OpenAPI. Isso facilita testar e documentar sua API desde o início. ([FastAPI](https://fastapi.tiangolo.com/tutorial/first-steps/ "First Steps - FastAPI"))

Docker Compose será útil porque permite rodar API e banco em conjunto por um arquivo YAML, simplificando ambiente local, testes e futura implantação. ([Docker Documentation](https://docs.docker.com/compose/ "Docker Compose | Docker Docs"))

## 4.2. Por que JavaScript puro no widget

O widget precisa ser leve e fácil de instalar em qualquer loja. Por isso, não comece com React ou Next.js dentro do site da Kouzina.

Use JavaScript puro. Depois, se quiser mais organização, transforme o widget em Web Component. Web Components permitem criar elementos reutilizáveis e encapsulados, reduzindo risco de conflito com o CSS/JS do site onde o script é instalado. ([MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/Web_Components?utm_source=chatgpt.com "Web Components - Web APIs | MDN"))

---

# 5. Estrutura de pastas do projeto

Crie esta estrutura:

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
│   └── TCC_NOTES.md
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

# 6. Primeira decisão importante: sem domínio próprio

Como você ainda não tem domínio, comece assim:

```text
Desenvolvimento local:
http://localhost:8000

Teste do widget:
arquivo demo.html local

Teste no site real:
URL provisória da API gerada pelo provedor de deploy

Futuro:
https://api.seudominio.com
https://cdn.seudominio.com/kouzina-reco.js
```

No começo, você não precisa comprar domínio. Você precisa provar que:

```text
1. a API responde;
2. o widget aparece;
3. o clique é registrado;
4. a recomendação faz sentido.
```

---

# 7. Fase 0 — Preparação do ambiente

## 7.1. Instale as ferramentas

Instale:

```text
Python 3.11 ou superior
Git
Docker Desktop
VS Code
Postman ou Insomnia
DBeaver ou Beekeeper Studio
Conta no GitHub
Conta em um provedor de deploy
```

## 7.2. Crie o repositório

No terminal:

```bash
mkdir kouzina-reco
cd kouzina-reco
git init
```

Crie também o `.gitignore`:

```gitignore
.env
__pycache__/
*.pyc
.venv/
node_modules/
.DS_Store
*.log
```

---

# 8. Fase 1 — Backend mínimo

## 8.1. Crie o `requirements.txt`

Arquivo:

```text
backend/requirements.txt
```

Conteúdo:

```txt
fastapi
uvicorn[standard]
pydantic
pydantic-settings
sqlalchemy
psycopg2-binary
python-dotenv
pandas
```

## 8.2. Crie o `.env.example`

Arquivo:

```text
.env.example
```

Conteúdo:

```env
APP_NAME=Kouzina Reco API
ENVIRONMENT=local
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/kouzina_reco
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000,https://www.kouzinaclub.com.br
PUBLIC_WIDGET_KEY=kouzina_public_dev_key
```

Depois crie o `.env` real:

```bash
cp .env.example .env
```

---

# 9. Fase 2 — Docker Compose

Crie:

```text
docker-compose.yml
```

Conteúdo:

```yaml
services:
  db:
    image: postgres:16
    container_name: kouzina_reco_db
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: kouzina_reco
    ports:
      - "5432:5432"
    volumes:
      - kouzina_reco_db_data:/var/lib/postgresql/data

volumes:
  kouzina_reco_db_data:
```

Suba o banco:

```bash
docker compose up -d
```

Verifique:

```bash
docker ps
```

---

# 10. Fase 3 — API mínima

## 10.1. Crie `backend/app/main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


app = FastAPI(
    title="Kouzina Reco API",
    version="0.1.0",
    description="API mínima para recomendações de produtos no site Kouzina."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://localhost:3000",
        "https://www.kouzinaclub.com.br",
        "https://kouzinaclub.com.br"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class EventIn(BaseModel):
    event_type: str
    anonymous_id: str
    session_id: Optional[str] = None
    page_url: Optional[str] = None
    product_id: Optional[str] = None
    widget_id: Optional[str] = None
    metadata: Optional[dict] = None


class RecommendationItem(BaseModel):
    product_id: str
    name: str
    url: str
    image_url: Optional[str] = None
    price: Optional[float] = None
    reason: str
    score: float


class RecommendationResponse(BaseModel):
    widget_title: str
    product_id: Optional[str]
    recommendations: List[RecommendationItem]


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "kouzina-reco-api",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/events")
def create_event(event: EventIn):
    # MVP inicial: apenas confirma recebimento.
    # Na próxima fase, salvar no PostgreSQL.
    return {
        "received": True,
        "event_type": event.event_type,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/recommendations", response_model=RecommendationResponse)
def get_recommendations(product_id: Optional[str] = None, widget_id: str = "product-page"):
    # MVP inicial: mock.
    return {
        "widget_title": "Complete seu projeto",
        "product_id": product_id,
        "recommendations": [
            {
                "product_id": "mock-001",
                "name": "Cooktop premium compatível",
                "url": "https://www.kouzinaclub.com.br/",
                "image_url": None,
                "price": 9990.00,
                "reason": "Produto complementar para composição de cozinha gourmet.",
                "score": 0.92
            },
            {
                "product_id": "mock-002",
                "name": "Forno de embutir recomendado",
                "url": "https://www.kouzinaclub.com.br/",
                "image_url": None,
                "price": 8490.00,
                "reason": "Combina com projetos de cozinha planejada.",
                "score": 0.85
            }
        ]
    }
```

## 10.2. Rode a API

Dentro da pasta do projeto:

```bash
cd backend
python -m venv .venv
```

Ative o ambiente:

Windows:

```bash
.venv\Scripts\activate
```

Mac/Linux:

```bash
source .venv/bin/activate
```

Instale dependências:

```bash
pip install -r requirements.txt
```

Rode:

```bash
uvicorn app.main:app --reload
```

Teste no navegador:

```text
http://localhost:8000/health
http://localhost:8000/docs
```

Resultado esperado em `/health`:

```json
{
  "status": "ok",
  "service": "kouzina-reco-api",
  "timestamp": "..."
}
```

---

# 11. Fase 4 — Widget JavaScript mínimo

Crie:

```text
widget/kouzina-reco.js
```

Conteúdo:

```javascript
(function () {
  const CONFIG = {
    apiBaseUrl: window.KouzinaReco?.apiBaseUrl || "http://localhost:8000",
    publicKey: window.KouzinaReco?.publicKey || "kouzina_public_dev_key",
    widgetSelector: "[data-kouzina-reco]",
  };

  function getOrCreateId(key) {
    let value = localStorage.getItem(key);
    if (!value) {
      value = crypto.randomUUID();
      localStorage.setItem(key, value);
    }
    return value;
  }

  const anonymousId = getOrCreateId("kouzina_reco_anonymous_id");
  const sessionId = getOrCreateId("kouzina_reco_session_id");

  function detectProductId() {
    const metaProduct = document.querySelector("meta[property='product:retailer_item_id']");
    if (metaProduct?.content) return metaProduct.content;

    const bodyText = document.body.innerText || "";
    const match = bodyText.match(/Código[:\s]+([0-9]+)/i);
    if (match) return match[1];

    return null;
  }

  async function sendEvent(eventType, extra = {}) {
    try {
      await fetch(`${CONFIG.apiBaseUrl}/events`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Kouzina-Public-Key": CONFIG.publicKey
        },
        body: JSON.stringify({
          event_type: eventType,
          anonymous_id: anonymousId,
          session_id: sessionId,
          page_url: window.location.href,
          product_id: extra.product_id || detectProductId(),
          widget_id: extra.widget_id || null,
          metadata: extra
        })
      });
    } catch (error) {
      console.warn("[KouzinaReco] event error", error);
    }
  }

  async function fetchRecommendations(productId, widgetId) {
    const url = new URL(`${CONFIG.apiBaseUrl}/recommendations`);
    if (productId) url.searchParams.set("product_id", productId);
    url.searchParams.set("widget_id", widgetId);

    const response = await fetch(url.toString(), {
      headers: {
        "X-Kouzina-Public-Key": CONFIG.publicKey
      }
    });

    return response.json();
  }

  function renderWidget(container, data) {
    container.innerHTML = `
      <div style="border:1px solid #ddd;padding:16px;margin:24px 0;font-family:Arial,sans-serif;">
        <h3 style="margin:0 0 8px;">${data.widget_title}</h3>
        <p style="margin:0 0 16px;color:#555;">Produtos selecionados para complementar sua escolha.</p>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;">
          ${data.recommendations.map(item => `
            <a
              href="${item.url}"
              data-kouzina-reco-click="${item.product_id}"
              style="display:block;text-decoration:none;color:#222;border:1px solid #eee;padding:12px;border-radius:8px;"
            >
              ${item.image_url ? `<img src="${item.image_url}" alt="${item.name}" style="max-width:100%;height:auto;">` : ""}
              <strong style="display:block;margin-bottom:8px;">${item.name}</strong>
              ${item.price ? `<span style="display:block;margin-bottom:8px;">R$ ${item.price.toLocaleString("pt-BR")}</span>` : ""}
              <small style="color:#666;">${item.reason}</small>
            </a>
          `).join("")}
        </div>
      </div>
    `;

    container.querySelectorAll("[data-kouzina-reco-click]").forEach(link => {
      link.addEventListener("click", () => {
        sendEvent("recommendation_click", {
          widget_id: container.dataset.kouzinaReco,
          recommended_product_id: link.dataset.kouzinaRecoClick
        });
      });
    });
  }

  async function init() {
    const productId = detectProductId();

    sendEvent("page_view", { product_id: productId });

    const containers = document.querySelectorAll(CONFIG.widgetSelector);

    containers.forEach(async (container) => {
      const widgetId = container.dataset.kouzinaReco || "product-page";

      try {
        const data = await fetchRecommendations(productId, widgetId);
        renderWidget(container, data);

        sendEvent("recommendation_impression", {
          widget_id: widgetId,
          product_id: productId,
          count: data.recommendations.length
        });
      } catch (error) {
        console.warn("[KouzinaReco] recommendation error", error);
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
```

---

# 12. Fase 5 — Página de teste local

Crie:

```text
widget/demo.html
```

Conteúdo:

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Teste Kouzina Reco</title>
</head>
<body>
  <h1>Coifa de Ilha 90cm 220V</h1>
  <p>Código: 12345</p>

  <div data-kouzina-reco="product-page"></div>

  <script>
    window.KouzinaReco = {
      apiBaseUrl: "http://localhost:8000",
      publicKey: "kouzina_public_dev_key"
    };
  </script>
  <script src="./kouzina-reco.js"></script>
</body>
</html>
```

Abra o arquivo no navegador.

Resultado esperado:

```text
Widget aparece
Produtos mockados aparecem
API recebe page_view
API recebe recommendation_impression
Clique gera recommendation_click
```

---

# 13. Fase 6 — Banco de dados real

Agora crie as tabelas.

## 13.1. Modelo inicial de dados

Você precisa de quatro tabelas no começo:

```text
stores
products
recommendation_events
manual_product_relations
```

## 13.2. SQL inicial

Crie o arquivo:

```text
docs/schema_v0.sql
```

Conteúdo:

```sql
CREATE TABLE stores (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    domain VARCHAR(255),
    public_key VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    store_id INTEGER REFERENCES stores(id),
    external_id VARCHAR(100) NOT NULL,
    name TEXT NOT NULL,
    url TEXT,
    image_url TEXT,
    category VARCHAR(255),
    subcategory VARCHAR(255),
    brand VARCHAR(255),
    price NUMERIC(12,2),
    promotional_price NUMERIC(12,2),
    available BOOLEAN DEFAULT TRUE,
    availability_text VARCHAR(255),
    stock INTEGER,
    voltage VARCHAR(50),
    width_cm NUMERIC(8,2),
    installation_type VARCHAR(100),
    product_type VARCHAR(100),
    environment VARCHAR(100),
    premium_level VARCHAR(100),
    description TEXT,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(store_id, external_id)
);

CREATE TABLE manual_product_relations (
    id SERIAL PRIMARY KEY,
    store_id INTEGER REFERENCES stores(id),
    source_product_id INTEGER REFERENCES products(id),
    target_product_id INTEGER REFERENCES products(id),
    relation_type VARCHAR(100) NOT NULL,
    weight NUMERIC(5,2) DEFAULT 1.0,
    reason TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE recommendation_events (
    id SERIAL PRIMARY KEY,
    store_id INTEGER REFERENCES stores(id),
    event_type VARCHAR(100) NOT NULL,
    anonymous_id VARCHAR(255),
    session_id VARCHAR(255),
    page_url TEXT,
    product_external_id VARCHAR(100),
    widget_id VARCHAR(100),
    recommended_product_external_id VARCHAR(100),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## 13.3. Eventos mínimos

Você vai registrar estes eventos:

```text
page_view
product_view
recommendation_impression
recommendation_click
```

Depois:

```text
add_to_cart
whatsapp_click
purchase
search
category_view
```

---

# 14. Fase 7 — Catálogo manual inicial

No começo,  **não dependa da API da Tray** .

Monte um CSV manual com 30 a 50 produtos.

Arquivo:

```text
data/products_seed.csv
```

Colunas:

```csv
external_id,name,url,image_url,category,subcategory,brand,price,available,availability_text,voltage,width_cm,installation_type,product_type,environment,premium_level
```

Exemplo:

```csv
12345,Coifa de Ilha 90cm 220V,https://www.kouzinaclub.com.br/produto-x,,Cozinha,Coifas,Elettromec,10290,true,Disponível em 30 dias úteis,220v,90,Ilha,Coifa,Cozinha Gourmet,Premium
23456,Cooktop 5 Queimadores 220V,https://www.kouzinaclub.com.br/produto-y,,Cozinha,Cooktops,Elettromec,8990,true,Disponível em 15 dias úteis,220v,90,Embutir,Cooktop,Cozinha Gourmet,Premium
```

A API de produtos da Tray pode ser usada depois para automatizar o catálogo, pois a documentação informa endpoints para consultar e listar produtos em JSON, com campos como id, nome, preço, marca, categoria, disponibilidade, imagens, URL, variações, estoque e quantidade vendida. ([Central do Parceiro Tray](https://partners.tray.com.br/themes/construindo-seu-template/apis-disponiveis/produtos "Produtos | Documentação de Temas | Central do Parceiro"))

---

# 15. Fase 8 — Algoritmo v0

Antes da ontologia fuzzy formal, implemente um ranking simples.

## 15.1. Critérios do ranking v0

Para cada produto candidato:

```text
+30 se for complementar ao tipo do produto atual
+20 se estiver disponível
+15 se tiver mesma voltagem
+15 se estiver em faixa de preço próxima
+10 se for da mesma marca
+10 se for do mesmo ambiente
+10 se for nível premium semelhante
-100 se for o mesmo produto
-30 se estiver indisponível
```

## 15.2. Relações complementares iniciais

Crie uma matriz simples:

```python
COMPLEMENTARY_TYPES = {
    "Coifa": ["Cooktop", "Forno", "Dominó"],
    "Cooktop": ["Coifa", "Forno", "Dominó"],
    "Adega": ["Cervejeira", "Frigobar", "Churrasqueira"],
    "Churrasqueira": ["Adega", "Cervejeira", "Coifa", "Cooktop"],
    "Forno": ["Cooktop", "Coifa"],
}
```

## 15.3. Função conceitual

```python
def recommend(product, candidates):
    ranked = []

    for candidate in candidates:
        score = 0
        reasons = []

        if candidate.id == product.id:
            continue

        if candidate.product_type in COMPLEMENTARY_TYPES.get(product.product_type, []):
            score += 30
            reasons.append("Produto complementar ao item visualizado")

        if candidate.available:
            score += 20
            reasons.append("Produto disponível")

        if product.voltage and candidate.voltage == product.voltage:
            score += 15
            reasons.append("Mesma voltagem")

        if product.brand and candidate.brand == product.brand:
            score += 10
            reasons.append("Mesma marca")

        if product.environment and candidate.environment == product.environment:
            score += 10
            reasons.append("Indicado para o mesmo ambiente")

        if product.premium_level and candidate.premium_level == product.premium_level:
            score += 10
            reasons.append("Faixa premium semelhante")

        ranked.append((candidate, score, reasons))

    ranked.sort(key=lambda item: item[1], reverse=True)
    return ranked[:4]
```

---

# 16. Fase 9 — Versão fuzzy v1

Depois que o ranking v0 estiver funcionando, você cria a primeira camada fuzzy.

## 16.1. Variáveis fuzzy iniciais

Use poucas variáveis:

```text
compatibilidade_tecnica
afinidade_ambiente
proximidade_preco
similaridade_premium
disponibilidade
```

## 16.2. Exemplo de pertinência

Para preço:

```text
preço próximo = 1.0 se diferença <= 15%
preço próximo = 0.7 se diferença <= 30%
preço próximo = 0.4 se diferença <= 50%
preço próximo = 0.1 acima disso
```

Para disponibilidade:

```text
disponível imediato ou poucos dias = alto
30 dias = médio
60+ dias = baixo
sob consulta = baixo/médio
esgotado = zero ou penalidade
```

## 16.3. Regra fuzzy simples

```text
SE compatibilidade_tecnica é alta
E afinidade_ambiente é alta
E proximidade_preco é média ou alta
ENTÃO recomendação é alta
```

No código, inicialmente você pode calcular sem biblioteca:

```python
final_score = (
    0.35 * compatibilidade_tecnica +
    0.25 * afinidade_ambiente +
    0.20 * proximidade_preco +
    0.10 * similaridade_premium +
    0.10 * disponibilidade
)
```

Isso já é defensável como primeira modelagem fuzzy operacional.

---

# 17. Fase 10 — Ontologia mínima

A ontologia não precisa ser grande no início.

## 17.1. Classes

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

## 17.2. Relações

```text
complementa
substitui
compatívelCom
pertenceAoAmbiente
temVoltagem
temMarca
temFaixaPreco
temTipoInstalacao
```

## 17.3. Exemplo conceitual

```text
CoifaDeIlha complementa Cooktop
Cooktop pertenceAoAmbiente CozinhaGourmet
Adega pertenceAoAmbiente EspacoGourmet
Churrasqueira complementa Cervejeira
```

No MVP, você pode representar isso no banco primeiro. Depois, formaliza em OWL/Protégé para o TCC.

---

# 18. Fase 11 — Instalação inicial no site

## 18.1. Antes de instalar

Tenha pronto:

```text
API publicada em URL HTTPS
widget JS publicado em URL pública HTTPS
endpoint /health funcionando
endpoint /recommendations funcionando
endpoint /events funcionando
CORS liberado apenas para Kouzina
script testado em demo.html
```

## 18.2. Código de instalação

Quando a API estiver publicada:

```html
<script>
  window.KouzinaReco = {
    apiBaseUrl: "https://sua-api-provisoria.com",
    publicKey: "kouzina_public_key",
  };
</script>

<script async src="https://sua-url-widget.com/kouzina-reco.js"></script>
```

## 18.3. Onde renderizar

O widget precisa de um container:

```html
<div data-kouzina-reco="product-page"></div>
```

Se você não conseguir inserir esse `div` no tema da Tray inicialmente, o próprio script pode criar o container automaticamente depois de algum elemento da página, como bloco de descrição, preço ou produtos relacionados.

---

# 19. Fase 12 — Cuidados com segurança

## 19.1. Nunca coloque segredo no JavaScript

No widget pode existir:

```text
publicKey
storeId
apiBaseUrl
```

Não pode existir:

```text
senha
token secreto
chave privada
credencial da Tray
token de banco
```

## 19.2. CORS

Libere apenas:

```text
https://www.kouzinaclub.com.br
https://kouzinaclub.com.br
localhost durante desenvolvimento
```

## 19.3. Rate limit

Adicione depois:

```text
limite por IP
limite por publicKey
bloqueio de origem desconhecida
logs de erro
```

Como a API da Tray possui limites de requisição, o catálogo deve ser sincronizado para o seu banco, e não consultado diretamente pelo widget a cada visita. A documentação da Tray informa limite de 180 requisições por minuto e 10 mil requisições diárias por loja, com 50 mil para loja corporativa. ([Central do Parceiro Tray](https://partners.tray.com.br/loja-de-aplicativos/comece-por-aqui/como-usar-a-api "Como usar a API | Loja de Aplicativos | Central do Parceiro"))

---

# 20. Fase 13 — LGPD desde o começo

No MVP, colete somente dados anônimos:

```text
anonymous_id
session_id
event_type
page_url
product_id
timestamp
widget_id
recommended_product_id
```

Não colete:

```text
nome
CPF
e-mail
telefone
endereço
dados de pagamento
dados sensíveis
```

A ANPD mantém guia orientativo sobre cookies e proteção de dados pessoais, e a página oficial destaca o tema de cookies, proteção de dados e boas práticas. Para seu MVP, adote minimização de dados, finalidade clara e transparência desde o início. ([Serviços e Informações do Brasil](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia_orientativo_cookies_e_protecao_de_dados_pessoais?utm_source=chatgpt.com "Guia orientativo Cookies e proteção de dados pessoais — Agência Nacional de Proteção de Dados"))

Documente no `docs/EVENTS.md`:

```text
Quais eventos são coletados
Qual finalidade
Quais dados são anônimos
Como remover dados
Como desativar tracking
```

---

# 21. Métricas do MVP

## 21.1. Métricas técnicas

```text
API uptime
tempo médio de resposta
erros do widget
erros de CORS
eventos recebidos por dia
```

## 21.2. Métricas comerciais

```text
impressões do widget
cliques nas recomendações
CTR do widget
produtos mais recomendados
produtos mais clicados
sessões com clique em recomendação
```

Fórmula inicial:

```text
CTR = recommendation_click / recommendation_impression
```

## 21.3. Métricas acadêmicas futuras

```text
Precision@K
Coverage
Diversity
Novelty
CTR comparado por baseline
avaliação qualitativa das explicações
```

---

# 22. Baselines para comparar

Na fase acadêmica, compare:

```text
Baseline A: produtos aleatórios da mesma categoria
Baseline B: produtos mais caros/destaque
Baseline C: produtos da mesma marca
Modelo proposto: regras semânticas + fuzzy + ontologia
```

No MVP comercial, você pode fazer A/B simples:

```text
50% dos visitantes recebem recomendação por categoria
50% recebem recomendação semântico-fuzzy
```

No começo, faça manualmente ou por regra simples.

---

# 23. Cronograma prático de 30 dias

## Semana 1 — Fundação técnica

Entregáveis:

```text
repositório criado
FastAPI rodando localmente
PostgreSQL rodando
endpoint /health
endpoint /events
endpoint /recommendations mockado
widget JS local
demo.html funcionando
```

Critério de conclusão:

```text
abrir demo.html e ver recomendações mockadas
clicar em uma recomendação e ver evento chegando na API
```

## Semana 2 — Catálogo e recomendação v0

Entregáveis:

```text
CSV com 30 a 50 produtos
importação para PostgreSQL
ranking por regras
recomendações reais, não mockadas
motivos textuais da recomendação
```

Critério de conclusão:

```text
informar product_id e receber 3 ou 4 produtos compatíveis
```

## Semana 3 — Publicação e teste real controlado

Entregáveis:

```text
API publicada em HTTPS
widget publicado em HTTPS
CORS configurado
script instalado via GTM ou ambiente de teste
eventos reais chegando
```

Critério de conclusão:

```text
abrir uma página real da Kouzina e ver o widget funcionando
```

## Semana 4 — Fuzzy v1 e relatório

Entregáveis:

```text
variáveis fuzzy iniciais
score fuzzy
comparação com recomendação por categoria
primeiro painel ou relatório CSV
documentação do MVP
```

Critério de conclusão:

```text
ter dados para mostrar: impressões, cliques, CTR e exemplos de recomendações
```

---

# 24. Documentos que você deve criar desde o início

## `README.md`

Conteúdo:

```text
O que é o projeto
Como rodar localmente
Como instalar dependências
Como subir banco
Como testar API
Como testar widget
```

## `docs/MVP.md`

Conteúdo:

```text
Objetivo do MVP
Escopo
Fora de escopo
Fluxo do usuário
Fluxo técnico
Critérios de sucesso
```

## `docs/API.md`

Conteúdo:

```text
GET /health
POST /events
GET /recommendations
formatos de request
formatos de response
códigos de erro
```

## `docs/EVENTS.md`

Conteúdo:

```text
page_view
product_view
recommendation_impression
recommendation_click
campos coletados
finalidade
LGPD
```

## `docs/DATA_MODEL.md`

Conteúdo:

```text
tabelas
campos
relacionamentos
exemplos
```

## `docs/TCC_NOTES.md`

Conteúdo:

```text
decisões técnicas
justificativas
limitações
ideias para metodologia
baselines
métricas
```

---

# 25. Checklist de início absoluto

Faça nesta ordem:

```text
[ ] Criar pasta kouzina-reco
[ ] Criar repositório Git
[ ] Criar estrutura de pastas
[ ] Criar backend FastAPI
[ ] Criar endpoint /health
[ ] Criar endpoint /events
[ ] Criar endpoint /recommendations mockado
[ ] Criar widget/kouzina-reco.js
[ ] Criar widget/demo.html
[ ] Testar localmente
[ ] Criar docker-compose com PostgreSQL
[ ] Criar schema inicial
[ ] Criar products_seed.csv
[ ] Cadastrar 30 a 50 produtos manualmente
[ ] Implementar ranking v0
[ ] Publicar API em HTTPS
[ ] Publicar JS em HTTPS
[ ] Instalar script em teste controlado
[ ] Medir impressões e cliques
[ ] Implementar fuzzy v1
[ ] Documentar resultados
```

---

# 26. Critério de sucesso do MVP

O MVP estará pronto quando você conseguir demonstrar isto:

```text
1. A API está online.
2. O widget carrega em uma página.
3. O widget identifica o contexto do produto.
4. A API retorna recomendações reais.
5. O visitante vê os produtos recomendados.
6. Cliques são registrados.
7. Você consegue calcular CTR.
8. O ranking tem justificativa semântica.
9. Há base para evoluir para fuzzy.
10. Há documentação suficiente para o TCC.
```

---

# 27. A ordem exata para você começar hoje

Comece por estas 10 ações:

```text
1. Criar a pasta kouzina-reco
2. Criar o repositório GitHub
3. Criar backend/app/main.py
4. Rodar FastAPI localmente
5. Testar /health
6. Criar widget/kouzina-reco.js
7. Criar widget/demo.html
8. Fazer o widget chamar /events
9. Fazer o widget chamar /recommendations
10. Confirmar que clique em recomendação gera evento
```

Somente depois disso vá para banco, catálogo, fuzzy e ontologia.

---

# 28. Versão final esperada do primeiro MVP

Ao final do MVP mínimo, você terá:

```text
kouzina-reco/
├── API online
├── widget JavaScript instalável
├── banco com produtos
├── banco com eventos
├── recomendador por regras
├── score fuzzy inicial
├── documentação técnica
├── dados reais de uso
└── base acadêmica para o TCC
```

Essa é a fundação correta: pequena, comercial, mensurável e evolutiva.

O próximo passo concreto é criar o repositório e implementar  **somente** :

```text
GET /health
POST /events
GET /recommendations
widget/demo.html
widget/kouzina-reco.js
```

Com isso funcionando, o projeto deixa de ser ideia e vira produto em execução.
