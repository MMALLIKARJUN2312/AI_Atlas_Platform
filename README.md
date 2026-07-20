# AI Atlas

AI Atlas is an intelligence platform for German Food & Beverage AI companies. It combines a searchable company directory, automated company news, grounded RAG answers with citations, and an evidence-led admin review workflow.

## Features

- **Company directory** — search, filters, profiles, maturity and problem coverage.
- **Newsletter** — fetches, relevance-scores, stores, refreshes, and indexes company news.
- **Ask AI** — embeds the platform knowledge base into pgvector, retrieves relevant chunks, then returns grounded answers with source citations.
- **Admin discovery** — review evidence-backed candidates, approve or reject them, and index approved companies immediately.

## Architecture

`Next.js + React Query` calls FastAPI REST endpoints. FastAPI uses a service/repository pattern over PostgreSQL, with pgvector storing embeddings. The AI flow is:

`CSV/database records → document builders → chunking → Gemini embeddings → pgvector → retrieval → LLM generation → citations`

News follows: `Company → fetch → relevance validation → URL deduplication → storage → embedding → Ask AI retrieval`.

The repository is organised as:

```text
apps/web/       Next.js UI, components, hooks, services, design tokens
apps/api/       FastAPI APIs, services, repositories, RAG and AI modules
apps/api/data/  CSV source datasets
docs/           architecture and deployment notes
infrastructure/ database bootstrap assets
```

## Prerequisites

- Node.js 20+ and pnpm 11+
- Python 3.12+
- Docker Desktop / Docker Compose
- A Gemini API key for embeddings and Ask AI

## Local development

```bash
git clone <repository-url>
cd AI_Atlas_Platform
cp .env.example .env
pnpm install

docker compose up -d postgres redis

cd apps/api
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
alembic upgrade head
python -m app.ingestion.load_dataset
uvicorn app.main:app --reload
# On Windows, use `python -m app.main` instead of the uvicorn CLI above —
# psycopg's async driver requires a SelectorEventLoop, which can only be
# applied before uvicorn creates its own event loop.
```

In another terminal:

```bash
cd apps/web
cp .env.local.example .env.local
pnpm dev
```

The web app runs on `http://localhost:3000`; API documentation is at `http://localhost:8000/docs`.

## Environment variables

Copy `.env.example` and set:

| Variable | Purpose |
| --- | --- |
| `DATABASE_URL` | Async PostgreSQL connection URL; use pgvector-enabled PostgreSQL. |
| `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` | Docker database bootstrap credentials. |
| `LLM_PROVIDER`, `LLM_MODEL`, `LLM_API_KEY` | Ask AI generation provider and credentials. |
| `EMBEDDING_PROVIDER`, `EMBEDDING_MODEL` | Embedding provider/model used during ingestion and retrieval. |
| `GNEWS_API_KEY` | Optional company-news provider key. |
| `NEWS_SCHEDULER_ENABLED`, `NEWS_REFRESH_INTERVAL_MINUTES` | Enables periodic news refreshes in the API process. |
| `JWT_SECRET`, `JWT_ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES` | Signs and validates admin session tokens. Set a real `JWT_SECRET` before deploying anywhere public. |
| `ADMIN_EMAIL`, `ADMIN_PASSWORD` | Bootstrap admin account, auto-created on first API startup if it doesn't already exist. Used to log in and obtain a token for `/api/v1/admin/*`. |
| `NEXT_PUBLIC_API_URL` | Frontend API base URL, normally `http://localhost:8000/api/v1`. |

## Dataset ingestion and indexing

`python -m app.ingestion.load_dataset` imports `companies_germany.csv`, `problems_germany.csv`, `problem_company_mapping.csv`, and `sectors_reference.csv`, then creates/replaces their embeddings. Re-run it after changing source datasets or document metadata.

## Important APIs

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/v1/companies` | Directory search and filters |
| GET | `/api/v1/companies/{id}` | Company profile |
| GET | `/api/v1/companies/{id}/news` | Stored company news |
| POST | `/api/v1/companies/{id}/news/refresh` | Refresh company news |
| POST | `/api/v1/ai/ask` | Grounded Ask AI response and sources |
| POST | `/api/v1/auth/login` | Admin login; returns a bearer token |
| POST | `/api/v1/admin/discover` | Evidence-backed admin candidate discovery (requires admin bearer token) |

All `/api/v1/admin/*` routes require an `Authorization: Bearer <token>` header from a successful `/api/v1/auth/login`. Log in with `ADMIN_EMAIL`/`ADMIN_PASSWORD` (the bootstrap admin account created automatically on API startup).

## Demo walkthrough

1. Open **Companies**, filter a sector, and open a profile.
2. Review the Overview, Problems Solved, and Newsletter tabs.
3. Open **Ask AI**, ask a company or news question, and inspect citations.
4. Open **Admin**, run discovery with a sector and country, review evidence, and approve a candidate.
5. Confirm the approved company appears in the directory and can be retrieved by Ask AI.

## Deployment

Deploy the web app to Vercel and the API to Railway, Render, or AWS. Use managed PostgreSQL with the `vector` extension and managed Redis. Run migrations and dataset ingestion once per environment before serving traffic. Configure all production environment variables in the relevant provider.

For Render, deploy the root `Dockerfile` as a Docker web service. Add the secret variables marked `sync: false` in `render.yaml`, run the initial dataset ingestion as a one-off job, and set the Vercel `NEXT_PUBLIC_API_URL` to the deployed Render API URL plus `/api/v1`. The checked-in Compose file currently runs only PostgreSQL and Redis; worker and scheduler containers still need dedicated production entrypoints.

See [docs/architecture.md](docs/architecture.md) for system design, trade-offs, and scaling notes.
