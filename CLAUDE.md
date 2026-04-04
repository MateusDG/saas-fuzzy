# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the MVP for a **fuzzy ontology-based recommendation system for premium appliance e-commerce**, developed as a TCC (undergraduate thesis) at UFOP (Universidade Federal de Ouro Preto), under Prof. Dr. Mateus Ferreira Satler.

The project follows a **hybrid approach**:
- **Phase 1 (Academic Validation):** Train and validate the fuzzy engine using the public Amazon Appliances dataset (~600K reviews).
- **Phase 2 (Real Application):** Deploy the validated engine on Kouzina Club (kouzinaclub.com.br), a real premium appliance e-commerce site.

## Data Files

- `Appliances.json/Appliances.json` — Amazon Appliances reviews (~602K lines, JSONL). Each line is a JSON object with fields: `overall` (1-5 rating), `reviewerID`, `asin`, `reviewText`, `unixReviewTime`, etc.
- `meta_Appliances.json/meta_Appliances.json` — Amazon Appliances product metadata (~30K lines, JSONL). Fields: `asin`, `title`, `brand`, `category`, `price`, `feature`, `description`, `also_buy`, `also_view`, etc. Note: `tech1` contains raw HTML from Amazon product pages.
- `documentacao_mvp (1).docx` — Full MVP documentation in Portuguese (architecture, data model, API contracts, evaluation metrics, tech stack, timeline).

## Architecture (Target)

Three-layer modular architecture: data collection → fuzzy processing → recommendation delivery.

Key components to be built:
- **Event Collector:** CSV ingestion (Phase 1) / JS tracker (Phase 2)
- **Fuzzy Engine:** Converts events into membership degrees, builds user profiles (Python + scikit-fuzzy / Simpful)
- **Ontology:** OWL representation of appliance domain (Owlready2 / Protégé + FuzzyOWL2)
- **Recommendation Generator:** Crosses fuzzy profiles with ontology to rank products (FastAPI)
- **Storage:** PostgreSQL + Redis (profile cache)
- **Dashboard:** Streamlit (MVP)

## Target Tech Stack

- Python 3.11+, scikit-fuzzy, Owlready2, FastAPI, Pandas/NumPy
- PostgreSQL 16+, Redis 7+
- Docker for containerization
- Streamlit for dashboard

## Key Domain Concepts

- **Fuzzy user profiles:** Vector of membership degrees (0-1) over ontology categories. Updated via `μ'(u,c) = max(μ(u,c), w_event × relevance(product,c))`.
- **Rating-to-fuzzy mapping (Phase 1):** 1★→0.0, 2★→0.25, 3★→0.5, 4★→0.75, 5★→1.0.
- **Event weights (Phase 2):** page_view=0.1, product_view=0.3, click_detail=0.4, add_to_cart=0.7, purchase=1.0.
- **Temporal decay:** `μ_effective = μ × e^(-λ × Δt)` with λ=0.01/day initial.
- **Ontology hierarchy:** Eletrodoméstico → Cocção, Refrigeração, Lavanderia, Área Gourmet, Climatização (with subcategories).

## Evaluation Metrics

- Offline (Phase 1): Precision@K, Recall@K, NDCG@K, MAP, Coverage. Temporal 80/20 split.
- Baselines: Random, Most Popular, Item-based Collaborative Filtering, Content-Based (TF-IDF).
- Online (Phase 2): CTR, Conversion rate, A/B testing.

## API Endpoints (Target)

- `POST /api/v1/events` — Register user event
- `GET /api/v1/recommendations/{user_id}` — Get recommendations
- `GET /api/v1/profile/{user_id}` — Get fuzzy profile
- `GET /api/v1/metrics` — Evaluation metrics
- `POST /api/v1/evaluate` — Run baseline comparison

## Academic Foundation

Based on Prof. Satler's prior work:
- "Fuzzy ontologies-based user profiles applied to enhance e-learning activities" (Soft Computing, 2012)
- "Fuzzy Ontology-Based Approach for Automatic Construction of User Profiles" (RSCTC, 2014)

The contribution is transposing fuzzy ontology profile construction from e-learning to premium appliance e-commerce.
