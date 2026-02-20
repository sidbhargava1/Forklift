# Codex Full-Stack Boilerplate (FastAPI + React + Postgres + Redis + Auth0 + OpenAI)

A reusable, Docker-first starter repo for building apps with Codex on top of a stable baseline.

This template intentionally provides infrastructure and integrations, not product-specific business endpoints.

## Included

- `backend`: FastAPI + SQLAlchemy + Alembic + Auth0 token verification + reusable OpenAI client + Redis caching
- `frontend`: React + Vite + TypeScript + Auth0 SPA wiring + starter health/auth checks
- `db`: PostgreSQL 16 via Docker Compose
- `redis`: Redis 7 via Docker Compose
- `prompts/`: prompt files that backend services can load by name
- Linting and formatting: Ruff (Python), ESLint + Prettier (frontend)
- Git hooks: pre-commit setup for backend/frontend quality checks
- CI workflow (`.github/workflows/ci.yml`) running pre-commit on push/PR

## Project structure

```text
.
├── backend/
│   ├── alembic/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   └── services/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── requirements-dev.txt
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── auth/
│   │   ├── config/
│   │   └── hooks/
│   └── Dockerfile
├── prompts/
├── docker-compose.yml
├── .env.example
└── .pre-commit-config.yaml
```

## Quick start

1. Create env file:

```bash
cp .env.example .env
```

2. Start the stack:

```bash
docker compose up --build
```

3. Open:

- Frontend: http://localhost:5173
- Backend OpenAPI: http://localhost:8000/docs
- Backend health: http://localhost:8000/api/v1/health

## Environment variables

All config is centralized in `.env` (copy from `.env.example`). Key groups:

- Database: `DATABASE_URL`, `POSTGRES_*`
- Redis cache: `REDIS_URL`, `LLM_CACHE_ENABLED`, `OPENAI_CACHE_TTL_SECONDS`
- OpenAI connector: `OPENAI_API_KEY`, `OPENAI_MODEL`
- Auth0 backend: `AUTH_ENABLED`, `AUTH0_DOMAIN`, `AUTH0_AUDIENCE`, `AUTH0_ISSUER`
- Auth0 frontend: `VITE_ENABLE_AUTH`, `VITE_AUTH0_*`

## OpenAI + Redis connector usage (backend)

No default endpoint is exposed for LLM calls. Build your own use-case services/endpoints and call the shared client:

```python
from app.services.llm_client import llm_client

result = await llm_client.generate(
    prompt_name="system",
    input_text="Summarize this text...",
)
# result => {"output_text": "...", "model": "...", "cached": False}
```

Prompts are loaded from `prompts/<prompt_name>.txt`.

## Auth0 usage

- Frontend can run with Auth disabled (`VITE_ENABLE_AUTH=false`) for local development.
- Backend can run with Auth disabled (`AUTH_ENABLED=false`) and returns a mock dev identity at `/api/v1/auth/me`.
- When enabled, backend validates JWTs against Auth0 JWKS.
- Use `AUTH0_DOMAIN` without protocol (example: `your-tenant.us.auth0.com`).

## Database and migrations

- Backend startup script waits for DB and runs migrations automatically in dev:
  - `python -m app.db.wait_for_db`
  - `alembic upgrade head`
- Alembic versions live in `backend/alembic/versions`.

## Linting, formatting, and hooks

### Run lint/format manually

```bash
make lint
make fmt
```

### Pre-commit hooks

Install pre-commit on your machine, then:

```bash
pre-commit install
pre-commit run --all-files
```

Configured hooks include:

- YAML/whitespace/basic git hygiene checks
- Ruff (`backend/`)
- ESLint + Prettier checks (`frontend/src`)

## Common dev commands

```bash
make up              # start all services
make down            # stop services
make logs            # follow logs
make backend-shell   # shell into backend container
make frontend-shell  # shell into frontend container
make db-shell        # psql shell
```

## Notes for extending

- Add domain modules under `backend/app/services` and corresponding routers under `backend/app/api/v1/endpoints`.
- Keep prompt templates in `prompts/` and version them with code.
- Add your own tests under `backend/tests` and `frontend` test setup as needed.
