# Incident Tracker for UCar<>TopDoer (Django + DRF + PostgreSQL)

## Стек

- **Python** 3.12.x
- **Django** 5.2.x
- **Django REST Framework** 3.16.x
- **PostgreSQL** 16
- **Docker Compose**
- **uv** (менеджер окружения и зависимостей)

## Важно

- Сервис запускается ИСКЛЮЧИТЕЛЬНО под Docker Compose. Локальный запуск без контейнеров не поддерживается.

## Быстрый старт

1. Скопируйте переменные окружения:
   ```bash
   cp .env.example .env
   ```
   Опционально: задайте таймзону в `.env` (например):
   ```bash
   echo 'TIME_ZONE=Europe/Moscow' >> .env
   ```
2. Соберите и запустите контейнеры:
   ```bash
   make up-b
   ```
3. Создайте суперпользователя для админки:
   ```bash
   make admin
   ```
   Логин/пароль: `admin/admin`.
4. Админка: http://localhost:8000/admin (логин/пароль: admin/admin)
5. Смоук API (создать → показать new → обновить статус):
   ```bash
   make curl-smoke
   ```
6. Проверки качества кода:
   ```bash
   make test
   make format
   make lint
   ```
    - make test — pytest в контейнере
    - make format — black + ruff format
    - make lint — ruff check
7. Pre-commit хуки (единый стиль в команде):
   ```bash
   make pre-commit
   ```

## Полезные команды Makefile

- **up** — запустить без сборки
- **up-b** — собрать и запустить
- **down** — остановить и УДАЛИТЬ volumes (БД очищается!). После `down` при новом запуске нужно заново делать
  `make admin`.
- **logs** — логи сервисов
- **shell** — Django shell внутри контейнера (`manage.py shell`)
- **makemigrations**, **migrate** — управление миграциями
- **curl-create**, **curl-list-new**, **curl-list-all**, **curl-update** — ручные вызовы API
    - ВНИМАНИЕ: `curl-update` обновляет запись с id=1

## API и документация

- v1:
    - `POST /api/v1/incidents/`
    - `GET  /api/v1/incidents/?status=new`
    - `PATCH /api/v1/incidents/{id}/status/`
- Документация:
    - [Swagger UI](http://localhost:8000/api/docs/)
    - [Redoc](http://localhost:8000/api/redoc/)
    - [OpenAPI JSON](http://localhost:8000/api/schema)

## Архитектура

- Плоский layout под `src/`:
    - `src/manage.py`
    - `src/incidents/` — доменная логика: модели, сериализаторы, вьюхи, сервисы, селекторы, админка, миграции
- Docker Compose:
    - сервис `backend` (Django server)
    - база `db` (PostgreSQL 16)
    - готовность БД контролируется healthcheck в compose; ожидание в `entrypoint.sh` удалено
- Настройки:
    - таймзона через ENV `TIME_ZONE` (по умолчанию `Europe/Moscow`)
    - для удобства тестов API открыт (`AllowAny`) — не для продакшена

## Примечания

- При старте `entrypoint.sh` выполняется `makemigrations incidents` (идемпотентно) и `migrate`.
- Используйте `pre-commit`, чтобы автоматически проверять стиль (black/ruff) перед коммитами.
