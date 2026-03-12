---
description: 'Python coding conventions and guidelines'
applyTo: '**/*.py'
---

# Python Coding Conventions

- Python 3.12+, FastAPI for HTTP services, boto3 for AWS (S3/SQS via LocalStack), PyPDF for PDF processing.
- Use `uv` for dependency and environment management with `pyproject.toml` and committed `uv.lock`.

## Project Structure

```text
fastapi-project/
    app/
        __init__.py
        main.py                # Entry point; wires routers together
        api/                   # API versioning root
            __init__.py
            v1/                # Version 1 endpoints
                __init__.py
                api.py         # Includes all routers for v1
                endpoints/     # Feature-specific route handlers
                    __init__.py
                    users.py
                    items.py
        core/                  # App-wide config (JWT, settings)
        crud/                  # Reusable database operations
        db/                    # Session management and engine setup
        models/                # SQLAlchemy/Database models
        schemas/               # Pydantic models for validation
        services/              # Complex business logic
    tests/                     # Unit and integration tests
    .env                       # Environment variables
    pyproject.toml             # Project metadata and dependencies
    uv.lock                    # Locked dependency graph
    alembic/                   # Database migrations
```

## FastAPI

- Keep route handlers thin: validate input, call a service layer, return schema models.
- Mount versioned routers from `app/api/v1/api.py` in `app/main.py`.
- Keep feature endpoints in `app/api/v1/endpoints/` and group by domain (`users`, `items`, etc.).
- Use Pydantic models in `app/schemas/`, database models in `app/models/`, and reusable operations in `app/crud/`.
- Keep environment-driven settings and security helpers under `app/core/`.

## Code Style

- PEP 8, 4-space indent, 88 char line limit, full type hints on public functions.
- Structured logging with contextual fields (`job_id`, `page_number`, `request_id`).
- Worker logic must be idempotent — duplicate page processing must not corrupt results.
- Keep session/engine wiring in `app/db/`; database migrations belong in top-level `alembic/`.
- Use `pytest` for unit and integration coverage across API, CRUD, and service layers.

## Example Entrypoint

```python
from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(title="PageSwarm API")

    @app.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
```
