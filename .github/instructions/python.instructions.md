---
description: 'Python coding conventions and guidelines'
applyTo: '**/*.py'
---

# Python Coding Conventions

- Python 3.12+, FastAPI for HTTP services, boto3 for AWS (S3/SQS via LocalStack), PyPDF for PDF processing.
- Use `uv` for dependencies: `pyproject.toml` + committed `uv.lock`. Use `uv add --dev` for test/tooling deps.

## Project Structure

```text
<component-name>/
    Dockerfile
    pyproject.toml / uv.lock
    src/
        <component_name>/
            main.py          # FastAPI app factory (create_app)
            api/routes.py
            core/config.py   # env-based settings
            core/logging.py
            services/
            clients/
            models/
    tests/
```

## FastAPI

- Use `create_app()` factory pattern. Keep handlers thin — validate, call service, return model.
- Use Pydantic models for schemas, `Depends` for shared resources, clear HTTP status codes.

## Code Style

- PEP 8, 4-space indent, 88 char line limit, full type hints on public functions.
- Structured logging with contextual fields (`job_id`, `page_number`, `request_id`).
- Worker logic must be idempotent — duplicate page processing must not corrupt results.
- Use `pytest`; cover critical paths, API contracts, and edge cases.

## Example Entrypoint

```python
from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(title="PageSwarm Component")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
```
