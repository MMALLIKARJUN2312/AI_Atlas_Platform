# AI Atlas

**AI Atlas** is an intelligence platform for AI vendors in Germany's Food & Beverage industry. It combines a searchable, evidence-backed company directory, an AI assistant grounded in a curated knowledge base, automated per-company news, and an admin workflow for discovering and vetting new vendors — all in one product.

---

## Table of Contents

- [Product Overview](#product-overview)
- [Features](#features)
- [Architecture](#architecture)
- [Setup Guide](#setup-guide)
- [User Walkthrough](#user-walkthrough)
- [Deployment](#deployment)
  - [Backend on Render](#backend-on-render)
  - [Frontend on Vercel](#frontend-on-vercel)
- [Testing](#testing)
- [Repository Layout](#repository-layout)

---

## Product Overview

### Purpose

Food & Beverage manufacturers, investors, and industry analysts need a fast way to answer questions like *"which vendors solve cold-chain traceability, and who's already using them in Germany?"* — without digging through vendor websites, press releases, and spreadsheets one at a time.

AI Atlas indexes a structured dataset of AI vendors, the industry problems they solve, and market sectors, then layers an AI assistant on top that answers questions **only from that grounded data** (with citations), rather than guessing from general LLM knowledge.

### Problem Solved

- **Fragmented vendor research** — vendor capabilities, customers, funding, and maturity live in scattered sources. AI Atlas centralizes them into structured, filterable profiles.
- **Stale information** — a directory alone goes stale. AI Atlas automatically fetches and indexes fresh company news so answers stay current.
- **Untrustworthy AI answers** — generic chatbots hallucinate company facts. AI Atlas's assistant is grounded strictly in the indexed dataset and refuses to answer when it doesn't have the facts.
- **Manual vendor discovery** — finding new vendors for an emerging sector/country combination is manual and error-prone. AI Atlas's admin discovery workflow automates the research step while keeping a human in the loop before anything is published.

### Target Users

- **Analysts / researchers** — browse the directory, ask natural-language questions, and follow citations back to source records or news articles.
- **Admins / data curators** — discover new vendor candidates for a sector and country, review the evidence behind each one, and approve or reject before they go live.

---

## Features

### Company Directory
- Search and filter vendors by sector, company type, maturity, and AI category.
- Company profile pages with three tabs: **Overview** (AI use case, deployment evidence, customers), **Problems Solved** (mapped industry problems with ROI benchmarks), and **Newsletter** (live news).

### Ask AI
- A grounded, citation-backed assistant available from a dedicated page and linked from the top navigation on every screen.
- Retrieves relevant chunks from a pgvector-backed knowledge base (companies, problems, sectors, and news), then generates an answer strictly from that retrieved context.
- Explicitly says *"I don't have enough information to answer that question"* rather than inventing facts when nothing relevant is retrieved.
- Every answer links back to the company profile or news source it came from.

### Newsletter (Automated Company News)
- Every company profile has a live Newsletter tab. Articles are fetched from Google News RSS — never entered by hand.
- Relevance filtering rejects name-collision false positives (e.g. a company whose name is also a common word).
- Deduplicated by URL, both within a single refresh and across the stored history.
- Refreshable on demand from the UI, and indexed into the knowledge base immediately so Ask AI can cite recent developments.

### Admin: AI-Powered Company Discovery
- An admin enters a sector and country (including combinations not yet in the dataset).
- The system searches the live web via an LLM with Google Search grounding, extracts candidate companies strictly from the returned search results, and requires every candidate to have at least one piece of evidence traceable to a real search result before it's ever shown for review.
- Each candidate displays a confidence score and clickable evidence links.
- **Human-in-the-loop**: nothing is written to the database until an admin explicitly approves a candidate. Approved companies are deduplicated against existing entries, written to the database, and indexed into the knowledge base immediately — no rebuild or redeploy required.

### Admin: Data Management
- Manually add a new company or edit an existing one through a validated form.
- Changes are immediately visible in the public directory and answerable by Ask AI.

### Authentication
- Simple email/password login for the admin area, backed by hashed passwords and short-lived JWT bearer tokens.
- A bootstrap admin account is created automatically on first API startup from `ADMIN_EMAIL`/`ADMIN_PASSWORD`, so a clean deployment has working credentials with no manual seeding step.

---

## Architecture

```
Next.js 16 (apps/web)  ──HTTP──►  FastAPI (apps/api)  ──►  PostgreSQL 18 + pgvector
                                        │
                                        ├──► Gemini (LLM generation + Google Search grounding)
                                        ├──► Gemini (text embeddings)
                                        └──► Google News RSS (company news)
```

### Frontend (`apps/web`)
- **Next.js 16** (App Router) + **React 19** + **TypeScript** (strict).
- **TanStack Query** for all server state (companies, problems, sectors, news, Ask AI, admin) — no separate global store; local UI state uses plain React state.
- **Tailwind CSS v4** with a token-based design system (`styles/tokens/*`: color, spacing, radius, shadow, typography) shared across every component.
- Hand-built, shadcn-style UI primitives in `components/ui` (Button, Card, Input, Badge, EmptyState, LoadingSkeleton, …) — consistent spacing, focus states, and primary/secondary/danger variants.
- **React Hook Form + Zod** for the admin company form.
- Route structure: `/` (dashboard), `/companies`, `/companies/[id]`, `/ask-ai`, `/admin`, `/admin/companies`, `/admin/login`.
- Responsive: a collapsible desktop sidebar and a slide-in mobile drawer share the same navigation source of truth.

### Backend (`apps/api`)
- **FastAPI** (async) with a repository/service layering: `api/routes` → `services` → `repositories` → SQLAlchemy models.
- **SQLAlchemy 2.0** (async, via `psycopg`) + **Alembic** migrations.
- **Pydantic v2** for request/response schemas.
- Auth: bcrypt password hashing + PyJWT bearer tokens, enforced via a FastAPI dependency on every `/admin/*` route. Public routes (directory, Ask AI, news) require no auth.

### Database
- **PostgreSQL 18** with the **pgvector** extension.
- Core tables: `companies`, `problems`, `problem_company_mappings`, `sectors`, `news` (FK → companies), `company_candidates` (discovery review queue), `users` (admin accounts), `embeddings` (chunked, embedded knowledge base with an HNSW index for cosine similarity).

### AI / RAG Workflow

**Ingestion** (`python -m app.ingestion.load_dataset`):
```
4 source CSVs → validated import → companies/problems/sectors/mappings tables
                                  → document builders → chunking → Gemini embeddings → pgvector
```
Bulk inserts are idempotent (`ON CONFLICT DO NOTHING`), so re-running the ingestion script is always safe.

**Ask AI request**:
```
question → pgvector semantic retrieval → similarity gate (min score 0.60)
   ├─ below threshold → "I don't have enough information..." (no LLM call)
   └─ above threshold → context-only prompt → Gemini → answer + citations from retrieved chunk metadata
```

**News refresh** (on-demand or scheduled):
```
company → Google News RSS search → name-collision relevance filter → URL dedup
        → stored in `news` table → chunked + embedded into pgvector → citable by Ask AI
```

**Admin discovery**:
```
sector + country → Gemini + Google Search grounding (live web search)
                  → context-only extraction of candidates from the grounded search results
                  → verification gate: every candidate must trace back to a real search result
                  → stored as pending `company_candidates` for human review
                  → on approval: written to `companies`, deduplicated, indexed into pgvector immediately
```

### External Integrations
- **Google Gemini** — LLM generation, Google Search grounding for discovery, and text embeddings (single provider, behind an internal interface so a second provider could be added without touching call sites).
- **Google News RSS** — company news source (no API key required).

---

## Setup Guide

### Requirements
- Node.js 20+ and pnpm 11+
- Python 3.12+
- Docker Desktop (for local PostgreSQL + Redis)
- A Gemini API key ([Google AI Studio](https://aistudio.google.com/)) with Google Search grounding enabled on your plan/tier

### Installation

```bash
git clone <repository-url>
cd AI_Atlas_Platform
cp .env.example .env
pnpm install

docker compose up -d postgres redis
```

### Backend

```bash
cd apps/api
python -m venv .venv

# macOS/Linux
source .venv/bin/activate
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
alembic upgrade head
python -m app.ingestion.load_dataset

uvicorn app.main:app --reload
```

> **Windows note:** use `python -m app.main` instead of the `uvicorn` CLI above. `psycopg`'s async driver requires a `SelectorEventLoop`, which can only be applied *before* uvicorn creates its own event loop — the CLI form creates it too early on Windows. `python -m app.main` handles this correctly and still supports the `PORT` environment variable.

API docs: `http://localhost:8000/docs` · Health check: `http://localhost:8000/api/v1/health`

### Frontend

In a second terminal:

```bash
cd apps/web
cp .env.local.example .env.local
pnpm dev
```

App: `http://localhost:3000`

### Database Setup Summary

| Step | Command | Notes |
| --- | --- | --- |
| Start Postgres + Redis | `docker compose up -d postgres redis` | Postgres image is `pgvector/pgvector:pg18`, pre-enabled for the `vector` extension. Host port `5434` maps to container `5432` (see `docker-compose.yaml`). |
| Run migrations | `alembic upgrade head` (from `apps/api`) | Creates all tables, the `vector` extension, and the HNSW index. |
| Load & index the dataset | `python -m app.ingestion.load_dataset` (from `apps/api`) | Imports the 4 CSVs and embeds every row. Idempotent — safe to re-run. |

### Environment Variables

Copy `.env.example` to `.env` (root) and `apps/web/.env.local.example` to `apps/web/.env.local`, then set:

| Variable | Where | Purpose |
| --- | --- | --- |
| `DATABASE_URL` | root `.env` | Async PostgreSQL connection URL (pgvector-enabled). |
| `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` | root `.env` | Local Docker Postgres bootstrap credentials. |
| `LLM_PROVIDER`, `LLM_MODEL`, `LLM_API_KEY` | root `.env` | Gemini provider, model, and API key for Ask AI generation + admin discovery. |
| `EMBEDDING_PROVIDER`, `EMBEDDING_MODEL` | root `.env` | Gemini embedding model used during ingestion and retrieval. |
| `GNEWS_API_KEY` | root `.env` | Reserved for an optional secondary news provider (currently unused — Google News RSS needs no key). |
| `NEWS_SCHEDULER_ENABLED`, `NEWS_REFRESH_INTERVAL_MINUTES` | root `.env` | Enables periodic in-process news refresh. |
| `JWT_SECRET`, `JWT_ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES` | root `.env` | Signs and validates admin session tokens. **Set a real, random `JWT_SECRET` before deploying publicly.** |
| `ADMIN_EMAIL`, `ADMIN_PASSWORD` | root `.env` | Bootstrap admin account, created automatically on first API startup if it doesn't exist. |
| `ALLOWED_ORIGINS` | root `.env` | Comma-separated browser origins allowed to call the API. `*` for local dev; set to your deployed frontend URL(s) in production. |
| `NEXT_PUBLIC_API_URL` | `apps/web/.env.local` | Frontend API base URL, e.g. `http://localhost:8000/api/v1` locally or `https://your-api.onrender.com/api/v1` in production. |

---

## User Walkthrough

1. **Land on the Dashboard** (`/`) — see directory-wide stats (companies, sectors, AI categories, maturity levels), a list of recently added companies, and quick links into Ask AI, the directory, and the admin workspace.
2. **Browse the directory** (`/companies`) — search by name, filter by sector, company type, maturity, or AI category. Filter options stay stable as you narrow results.
3. **Open a company profile** (`/companies/[id]`) — read the Overview (AI use case, deployment evidence, customers, funding), switch to **Problems Solved** to see mapped industry problems and ROI benchmarks, and switch to **Newsletter** to read live news or trigger a manual refresh.
4. **Ask AI** (`/ask-ai`) — ask a natural-language question (e.g. *"What problems does Krones solve and is there recent news about them?"*). The answer cites the company records and/or news articles it drew from; clicking a citation opens that company's profile.
5. **Sign in to the admin workspace** (`/admin/login`) — log in with the bootstrap admin credentials (or any admin account created later).
6. **Discover new vendors** (`/admin`) — enter a sector and country, review the AI-proposed candidates with their evidence links and confidence scores, and approve or reject each one.
7. **Confirm it's live** — the approved company appears in `/companies` immediately, and Ask AI can answer questions about it right away — no rebuild or redeploy.
8. **Manage data directly** (`/admin/companies`) — add a company manually, or edit an existing record; changes are live immediately.

---

## Deployment

### Backend on Render

The repository ships with a root `Dockerfile` and `render.yaml` blueprint targeting a single Docker web service.

**Docker configuration** — `Dockerfile` builds from `python:3.12-slim`, installs `apps/api/requirements.txt`, and starts with:
```
alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
```
Migrations run automatically on every deploy before the server starts.

**Steps:**
1. Provision a managed PostgreSQL instance with the `vector` extension available (Render's managed Postgres, or any pgvector-capable provider), and set `DATABASE_URL` accordingly.
2. In the Render dashboard, create a new **Blueprint** from this repository (it will pick up `render.yaml`), or create a Docker web service manually pointing at the root `Dockerfile`.
3. Fill in every environment variable marked `sync: false` in `render.yaml`:
   - `DATABASE_URL` — your managed Postgres connection string
   - `REDIS_URL` — optional; not currently consumed by application code
   - `LLM_API_KEY` — your Gemini API key
   - `GNEWS_API_KEY` — optional, reserved for future use
   - `JWT_SECRET` — a long random string (**do not** leave the code default)
   - `ADMIN_EMAIL` / `ADMIN_PASSWORD` — your real admin login
   - `ALLOWED_ORIGINS` — your deployed Vercel frontend URL, e.g. `https://ai-atlas.vercel.app`
4. Deploy. Render builds the Docker image, runs `alembic upgrade head`, and starts the API.
5. Run the dataset ingestion once against the production database (e.g. via a Render one-off job or a local run with `DATABASE_URL` pointed at production):
   ```bash
   python -m app.ingestion.load_dataset
   ```
6. **Health check**: Render polls `healthCheckPath: /api/v1/health` (configured in `render.yaml`) — confirm it returns `{"status": "healthy", ...}`.
7. **Verify publicly**: `curl https://<your-service>.onrender.com/api/v1/health` and `https://<your-service>.onrender.com/docs`.

> The checked-in `docker-compose.yaml` only runs Postgres and Redis for local development — it is not a production deployment target.

### Frontend on Vercel

1. Import the repository into Vercel.
2. Set **Root Directory** to `apps/web` in the project's General settings (this is a pnpm workspace; Vercel auto-detects the workspace root and runs `pnpm install` from there).
3. Framework preset: **Next.js** (auto-detected). Build command and output directory can be left at Vercel's Next.js defaults.
4. Set the environment variable:
   - `NEXT_PUBLIC_API_URL` = `https://<your-render-service>.onrender.com/api/v1`
5. Deploy. Vercel builds and serves the app on your `*.vercel.app` domain (or a custom domain).
6. Go back to Render and set `ALLOWED_ORIGINS` to this exact Vercel URL, then redeploy the API so CORS allows it.

### Verifying the Full Production Flow

1. Open the deployed frontend URL.
2. Browse `/companies` and confirm real data loads (proves frontend → backend connectivity).
3. Open `/ask-ai` and ask a question; confirm a grounded answer with citations returns.
4. Go to `/admin/login` and sign in with the production admin credentials.
5. Run a discovery search, approve a candidate, and confirm it appears in `/companies` without redeploying anything.

---

## Testing

**Backend:**
```bash
cd apps/api
pytest
```
Unit tests cover the RAG pipeline (retrievers, builders, indexing), Ask AI service, admin discovery/approval logic (including the hallucination-prevention gate), and the auth dependency.

**Frontend:**
```bash
cd apps/web
pnpm lint          # ESLint
npx tsc --noEmit   # Type check
pnpm build         # Production build
```

---

## Repository Layout

```text
apps/web/            Next.js UI — app router pages, feature components, hooks, services, design tokens
apps/api/             FastAPI app — routes, services, repositories, RAG/AI modules, ingestion, tests
apps/api/data/        Source CSV datasets (companies, problems, mappings, sectors)
apps/api/alembic/     Database migrations
packages/              Shared TypeScript scaffolding (not currently consumed by apps/web)
docs/                  Architecture and deployment notes
infrastructure/        Local Postgres bootstrap SQL
render.yaml            Render Blueprint for the backend
Dockerfile              Backend production image
docker-compose.yaml    Local Postgres + Redis for development
```

See [docs/architecture.md](docs/architecture.md) for further design notes and trade-offs.
