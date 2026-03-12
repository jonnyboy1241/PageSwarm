# Copilot Workspace Instructions

This repository is a Docker Compose monorepo for PageSwarm.

## Repository Intent
- The root `docker-compose.yml` orchestrates all runnable components.
- Each component lives in its own subfolder and has its own `Dockerfile`.
- Components should be independently buildable and runnable, then composed together through the root compose file.

## Preferred Component Layout
- Use a consistent layout like `<component-name>/` at the repository root.
- Each component folder should include:
  - `Dockerfile`
  - Source code
  - Component-local dependency/lock files
  - Tests (where applicable)

## Compose Conventions
- Keep service names stable and descriptive; avoid renaming unless necessary.
- In `docker-compose.yml`, prefer `build.context` paths that point to component folders.
- Prefer explicit `depends_on`, environment variables, and named volumes when required.
- Do not pin random host ports unless needed for local development.

## Coding Expectations
- Keep changes minimal and scoped to the requested feature.
- Preserve backward compatibility for service names, queue names, and storage paths unless explicitly requested.
- Add or update tests when behavior changes.
- Update `README.md` when architecture, setup, or run commands change.

## Python Service Defaults
- Target Python 3.12+.
- Prefer FastAPI for API services and boto3 for AWS interactions.
- Keep worker logic idempotent; duplicate message processing must not corrupt results.
- Use structured logging for API and worker flows.

## Infrastructure and LocalStack
- LocalStack is used for local AWS emulation (S3, SQS).
- Favor environment-based configuration over hardcoded endpoints.
- Do not commit secrets; use `.env` files and compose environment wiring.

## What Copilot Should Do by Default
- When adding a new component, also wire it into `docker-compose.yml`.
- When changing service contracts, update all affected components.
- When adding new infra dependencies, document them in `README.md`.
- If a requested change is ambiguous across components, ask a clarifying question before broad edits.
