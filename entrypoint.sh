#!/usr/bin/env sh
set -e

uv sync --frozen || uv sync

uv run python src/manage.py makemigrations incidents --noinput || true
uv run python src/manage.py migrate --noinput
uv run python src/manage.py runserver 0.0.0.0:8000
