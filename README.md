# FastAPI REST Skeleton

A production-oriented **FastAPI + Pydantic v2** REST API starter with a clean
**layered architecture** (routers -> services -> repositories -> models),
SQLAlchemy 2.0 ORM, JWT authentication, Docker, and pytest.

> Clone it, `pip install -r requirements.txt`, run `uvicorn app.main:app --reload`,
> and you have a running, tested, layered API.

## Features

- FastAPI + Pydantic v2 (type-safe request/response models)
- Layered architecture: `api` -> `services` -> `repositories` -> `models`
- SQLAlchemy 2.0 ORM core (SQLite by default, swap to Postgres via `DATABASE_URL`)
- JWT bearer auth (`/api/v1/auth/login`, `/auth/me`) with BCrypt password hashing
- Centralized configuration via `pydantic-settings` (`.env`)
- Global exception handler (`AppError` -> consistent JSON errors)
- Docker + docker-compose, Makefile, Ruff / pytest configuration
- Sample domain: `User` and `Item` with full CRUD

## Architecture

```
HTTP Request
    |
    v
app/api/v1/*.py      (routers: parse request, call service, shape response)
    |
    v
app/services/*.py    (business logic, validation, orchestration)
    |
    v
app/repositories/*.py (data access, SQLAlchemy sessions)
    |
    v
app/models/*.py      (ORM models / DB tables)
```

Cross-cutting:
- `app/config.py`        -> typed settings from env / `.env`
- `app/database.py`      -> engine, session factory, `get_db` dependency
- `app/dependencies.py`  -> DI wiring (repos, current user)
- `app/core/security.py` -> password hashing + JWT
- `app/core/exceptions.py` -> `AppError` + handler

## Project Structure

```
fastapi-rest-skeleton/
|-- app/
|   |-- api/v1/        routers (auth, users, items) + router aggregator
|   |-- core/          security, exceptions
|   |-- models/        SQLAlchemy ORM models
|   |-- repositories/  data-access layer (+ generic BaseRepository)
|   |-- schemas/       Pydantic request/response models
|   |-- services/      business logic
|   |-- config.py      pydantic-settings
|   |-- database.py    engine + sessions
|   |-- dependencies.py DI
|   |-- main.py        FastAPI app / lifespan / exception handlers
|-- tests/             pytest (+ TestClient) end-to-end + unit tests
|-- Dockerfile         python:3.12-slim image
|-- docker-compose.yml one-command dev stack
|-- Makefile           commontasks
|-- pyproject.toml     ruff / pytest config
|-- requirements.txt   runtime deps
|-- requirements-dev.txt dev deps
|-- .env.example       config template
```

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env             # then edit SECRET_KEY
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit http://localhost:8000/docs for the interactive Swagger UI.

Create a demo user programmatically (optional):

```bash
python -m app.seed
```

## API Quick Reference

| Method | Path                   | Auth | Description              |
|--------|------------------------|------|--------------------------|
| GET    | `/health`              | No   | Liveness probe           |
| POST   | `/api/v1/users`        | No   | Register a user          |
| GET    | `/api/v1/users`        | No   | List users               |
| GET    | `/api/v1/users/{id}`   | No   | Get a user               |
| PATCH  | `/api/v1/users/{id}`   | No   | Update a user            |
| DELETE | `/api/v1/users/{id}`   | No   | Delete a user            |
| POST   | `/api/v1/auth/login`   | No   | OAuth2 password -> JWT   |
| GET    | `/api/v1/auth/me`      | Yes  | Current user             |
| POST   | `/api/v1/items`        | Yes  | Create an item           |
| GET    | `/api/v1/items`        | Yes  | List my items            |
| GET    | `/api/v1/items/{id}`   | Yes  | Get an item              |
| PATCH  | `/api/v1/items/{id}`   | Yes  | Update an item           |
| DELETE | `/api/v1/items/{id}`   | Yes  | Delete an item           |

Example login (returns a Bearer token):

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -d "username=demo@example.com&password=demo1234"
```

Then use the token:

```bash
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

## Testing

```bash
pytest                 # runs unit + end-to-end tests against an in-memory DB
ruff check app tests   # lint
ruff format app tests  # format
```

## Configuration

All configuration lives in environment variables (see `.env.example`):

| Variable                     | Default            | Notes                          |
|------------------------------|--------------------|--------------------------------|
| `APP_NAME`                   | FastAPI REST Skeleton | API title                   |
| `DEBUG`                      | false              |                                |
| `HOST` / `PORT`              | 0.0.0.0 / 8000    |                                |
| `SECRET_KEY`                 | change-me          | **CHANGE in production**       |
| `ALGORITHM`                  | HS256              |                                |
| `ACCESS_TOKEN_EXPIRE_MINUTES`| 30                 |                                |
| `DATABASE_URL`               | sqlite:///./app.db | e.g. postgresql+psycopg://...  |

## Next Steps

- Swap SQLite for Postgres: set `DATABASE_URL` and add `psycopg[binary]`.
- Add Alembic migrations (replace `init_db()` create_all for production).
- Enforce per-user ownership on items (routers currently rely on `current_user`
  being passed to the service; add `item.owner_id == current_user.id` checks).
- Add role/permission authorization, rate limiting, and structured logging.
