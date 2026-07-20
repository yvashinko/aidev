# AGENTS.md — Task Service

## Stack
- Python 3.11+
- FastAPI + Pydantic
- SQLAlchemy 2.0 + SQLite
- pytest + httpx
- ruff

## Conventions
- snake_case for functions/variables, PascalCase for classes.
- Routers handle HTTP only; business logic in service.py.
- Repository returns domain models, not ORM entities.
- Errors return RFC 7807 ProblemDetails.

## Security baseline
- No hardcoded secrets.
- Validate all inputs via Pydantic.
- SQL via ORM only.

## Commands
- `make test`
- `make lint`
- `make run`

## Definition of Done
- [ ] Tests pass
- [ ] Lint passes
- [ ] README updated if behavior changed
