SHELL := /bin/bash

.PHONY: help up up-b down logs shell bash migrate makemigrations test admin curl-create curl-list curl-update curl-smoke format lint pre-commit-install

help:
	@echo "Targets:"
	@echo "  up            - run docker compose (db+backend)"
	@echo "  up-b          - build and run"
	@echo "  down          - stop"
	@echo "  curl-*        - sample API calls"


	@echo "  migrate       - run migrations"
	@echo "  makemigrations- make migrations"
	@echo "  admin         - create Django superuser admin/admin"

	@echo "  logs          - tail logs"
	@echo "  shell         - Django shell (manage.py shell) inside backend"
	@echo "  bash          - open interactive shell inside backend"

	@echo "  test          - run pytest in container"
	@echo "  format        - black + ruff format"
	@echo "  lint          - ruff check"
	@echo "  pre-commit-install - install hooks"

up:
	docker compose up -d

up-b:
	docker compose up -d --build

down:
	docker compose down -v

logs:
	docker compose logs -f --tail=200

shell:
	docker compose exec backend uv run python src/manage.py shell

bash:
	docker compose exec backend /bin/bash || docker compose exec backend sh

migrate:
	docker compose exec backend uv run python src/manage.py migrate

makemigrations:
	docker compose exec backend uv run python src/manage.py makemigrations

test:
	docker compose exec backend uv run pytest

admin:
	bash scripts/curl_samples.sh admin

curl-create:
	bash scripts/curl_samples.sh create

curl-list-new:
	bash scripts/curl_samples.sh list-new

curl-update:
	bash scripts/curl_samples.sh update 1

curl-list-all:
	bash scripts/curl_samples.sh list-all

curl-smoke: curl-create curl-list-new curl-update

format:
	uv run black src
	uv run ruff format src

lint:
	uv run ruff check src

pre-commit-install:
	uv run pre-commit install
