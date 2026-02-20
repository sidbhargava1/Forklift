# AGENTS.md

## Purpose
This repository is a reusable baseline for product work built with Codex.
Keep infrastructure stable, then layer product-specific features on top.

## Stack Baseline
- Backend: FastAPI + SQLAlchemy + Alembic on Python 3.12.
- Frontend: React 18 + TypeScript + Vite on Node 20.
- Infra: Docker Compose with Postgres 16 and Redis 7.
- Auth: Auth0 integration is optional and controlled by env vars.
- LLM: Shared OpenAI client with optional Redis caching.

## Source of Truth
- Runtime/config values come from `.env` (`.env.example` as template).
- Backend settings are centralized in `backend/app/core/config.py`.
- Frontend env parsing is centralized in `frontend/src/config/env.ts`.
- Prompts used by backend services live in `prompts/*.txt`.

## How To Extend This Boilerplate
- Add product endpoints in `backend/app/api/v1/endpoints/`.
- Add domain logic in `backend/app/services/`.
- Add/modify DB models in `backend/app/models/`.
- Add migrations in `backend/alembic/versions/`.
- Add frontend features under `frontend/src/` (components/hooks/api).
- Keep infra-level code generic and reusable; keep product logic in app-layer modules.

## Backend Guardrails
- Do not read env vars directly in route handlers or services; use `get_settings()`.
- Keep endpoint handlers thin: validate input, call service layer, return response.
- Prefer explicit response payloads and clear HTTP error handling.
- Reuse `llm_client` for OpenAI calls instead of creating ad hoc clients.
- If schema/data behavior changes, include an Alembic migration.

## Frontend Guardrails
- Keep API calls in `frontend/src/api/`; avoid scattering `fetch` calls in components.
- Keep auth access through existing auth context/hooks.
- Build reusable, composable components; avoid one-off page-only logic when possible.
- Maintain strict TypeScript hygiene (no unnecessary `any`).
- Preserve mobile responsiveness and accessibility (keyboard/focus/labels).

## Design Direction
- Avoid generic UI defaults; give each product surface a distinct visual direction.
- Use purposeful typography, spacing rhythm, and clear color hierarchy.
- Prefer CSS variables/tokens for theme consistency.
- Use motion intentionally (state changes, loading, reveals), not decoration everywhere.
- Ensure layouts work well on both desktop and mobile.

## Commands (Preferred)
- Start stack: `make up`
- Stop stack: `make down`
- Logs: `make logs`
- Lint: `make lint`
- Format: `make fmt`
- Backend tests: `make test`
- Pre-commit install/run: `make precommit-install`, `make precommit-run`

## Quality Bar (Definition of Done)
For substantive changes, Codex should aim to:
- implement the feature end-to-end (not partial scaffolding only),
- keep changes scoped and consistent with current architecture,
- run relevant checks (`make lint`, tests when backend behavior changes),
- update docs when behavior, setup, or commands change,
- avoid leaving dead code or TODO placeholders without clear follow-up context.

## Non-Goals For This Boilerplate
- Do not overfit repo-wide defaults to one product domain.
- Do not replace core infra choices (FastAPI/React/Postgres/Redis) unless explicitly requested.
- Do not add large dependencies when existing stack utilities already cover the need.
