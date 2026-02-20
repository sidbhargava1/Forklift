.PHONY: up down logs ps backend-shell frontend-shell db-shell lint fmt test precommit-install precommit-run

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f --tail=200

ps:
	docker compose ps

backend-shell:
	docker compose exec backend /bin/sh

frontend-shell:
	docker compose exec frontend /bin/sh

db-shell:
	docker compose exec db psql -U $$POSTGRES_USER -d $$POSTGRES_DB

lint:
	docker compose exec backend ruff check .
	docker compose exec frontend npm run lint

fmt:
	docker compose exec backend ruff format .
	docker compose exec frontend npm run format

test:
	docker compose exec backend pytest -q

precommit-install:
	pre-commit install

precommit-run:
	pre-commit run --all-files
