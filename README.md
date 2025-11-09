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

## Примеры запросов (cURL)

- **Создать инцидент**
  ```bash
  curl -X POST http://localhost:8000/api/v1/incidents/ \
    -H "Content-Type: application/json" \
    -d '{"text":"Не могу снять бронь с автомобиля","source":"partner","status":"new"}'
  ```

- **Список всех**
  ```bash
  curl http://localhost:8000/api/v1/incidents/
  ```

- **Список по статусу (new)**
  ```bash
  curl "http://localhost:8000/api/v1/incidents/?status=new"
  ```

- **Обновить статус на resolved (id=1)**
  ```bash
  curl -X PATCH http://localhost:8000/api/v1/incidents/1/status/ \
    -H "Content-Type: application/json" \
    -d '{"status":"resolved"}'
  ```

## FAQ / Troubleshooting

- **Сервис не поднимается / healthcheck падает**
    - Проверьте логи: `make logs` (и отдельно `docker compose logs db`).
    - Убедитесь, что порты 8000/5432 свободны на хосте.
    - Проверьте, что есть `.env` и корректные переменные подключения к БД (в контейнере `POSTGRES_HOST=db`).

- **После `make down` всё «пропало»**
    - Команда выполняет `docker compose down -v` и УДАЛЯЕТ volume c БД. Это ожидаемо.
    - Подними заново `make up-b` и снова создай админа: `make admin`.

- **`/` отдаёт 404**
    - Это нормально. Используйте `/api/v1/`, или открой
      доку: [Swagger UI](http://localhost:8000/api/docs/) / [Redoc](http://localhost:8000/api/redoc/).

- **`make test` не находит тесты (0 tests)**
    - Тесты лежат в `tests/`, внутри контейнера они монтируются (`docker-compose.yml`).
    - Имена файлов должны быть вида `test_*.py` (см. `tests/test_incidents.py`).
    - Конфигурация `pytest.ini` смонтирована и применится автоматически. Запуск: `make test`.

- **Ошибка таймзоны: `Incorrect timezone setting: Moscow/Europe`**
    - Укажите корректный IANA-идентификатор: `TIME_ZONE=Europe/Moscow` в `.env`.

- **Не могу войти в админку**
    - Создайте суперпользователя: `make admin` (логин/пароль `admin/admin`). Команда идемпотентна.

- **`curl-update` не меняет запись**
    - Команда обновляет id=1. Посмотрите реальные id: `make curl-list-all`.
    - После `make down` БД пустая — создайте данные заново.

- **pre-commit не ставится/не работает**
    - Установите dev-зависимости: `uv sync` (в контейнере это уже выполняется при сборке).
    - Поставьте хуки: `make pre-commit`.

- **CORS/безопасность**
    - Проект в dev-режиме: API открыт (`AllowAny`) для простоты тестирования. В проде требуются аутентификация и жёсткие
      настройки безопасности.
