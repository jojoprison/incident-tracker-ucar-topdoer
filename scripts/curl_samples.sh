#!/usr/bin/env bash
set -euo pipefail

base_url=${BASE_URL:-http://localhost:8000}

pp() {
  if command -v jq >/dev/null 2>&1; then jq .; else cat; fi
}

create_admin() {
  echo "Creating Django superuser admin/admin ..."
  docker compose exec -T backend env \
    DJANGO_SUPERUSER_USERNAME=admin \
    DJANGO_SUPERUSER_PASSWORD=admin \
    DJANGO_SUPERUSER_EMAIL=admin@example.com \
    uv run python src/manage.py createsuperuser --noinput || true
}

create() {
  curl -sS -X POST "$base_url/api/v1/incidents/" \
    -H "Content-Type: application/json" \
    -d '{"text":"Не могу снять бронь с автомобиля","source":"partner","status":"new"}' | pp
}

list_filtered_new() {
  curl -sS "$base_url/api/v1/incidents/?status=new" | pp
}

list_all() {
  curl -sS "$base_url/api/v1/incidents/" | pp
}

update_status() {
  local id=${1:-1}
  curl -sS -X PATCH "$base_url/api/v1/incidents/$id/status/" \
    -H "Content-Type: application/json" \
    -d '{"status":"resolved"}' | pp
}

case "${1:-}" in
  admin|create-admin) create_admin;;
  create) create;;
  list-new) list_filtered_new;;
  list-all) list_all;;
  update) update_status "${2:-1}";;
  *) echo "Usage: $0 {admin|create|list-new|list-all|update [id]}"; exit 2;;
 esac
