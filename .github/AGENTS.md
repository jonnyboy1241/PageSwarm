# AGENTS

This file defines how coding agents should operate in this monorepo.

## Scope
- Applies to the whole repository.
- Component-specific constraints should be added in local `AGENTS.md` files inside component folders when needed.

## Monorepo Rules
- Treat each component folder as an independent deployable unit.
- Assume each component has its own `Dockerfile` and is orchestrated by root `docker-compose.yml`.
- Avoid coupling components through direct file imports across service boundaries unless explicitly requested.

## Change Discipline
- Prefer small, targeted edits.
- Do not refactor unrelated services during feature work.
- Keep service and compose names stable unless the user asks for renames.

## Docker and Compose Expectations
- If adding a component, update root `docker-compose.yml` with:
  - `build.context` pointing to the component folder
  - required environment variables
  - required volumes/networks
- Keep container startup deterministic and reproducible.
- Prefer explicit health checks for long-running services.

## API and Worker Patterns
- API layer should remain thin: validate input, enqueue work, report status.
- Workers should be idempotent and safe to retry.
- Preserve message schema compatibility unless explicitly versioning it.

## Testing and Validation
- For code changes, run or add the narrowest useful tests.
- For compose changes, validate syntax and service build paths.
- If validation cannot be run, state what was not validated.

## Documentation Rules
- Update `README.md` whenever:
  - setup steps change
  - new services are added
  - ports, env vars, or run commands change

## Escalation
- Ask before making broad cross-service architectural changes.
- Ask before introducing new infrastructure dependencies not already in use.
