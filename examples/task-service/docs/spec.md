# Specification: Task Service

## 1. Stack & versions
- Python 3.11+
- FastAPI 0.110+, Pydantic 2.x
- SQLAlchemy 2.0 + SQLite
- pytest 8+, httpx

## 2. Domain
- Task: id, title, description, status (todo/done), created_at.
- No users/roles.

## 3. API contracts
- REST over HTTP/JSON.
- Endpoints:
  - POST /tasks — create
  - GET /tasks — list
  - GET /tasks/{id} — get
- ProblemDetails on errors.

## 4. NFR
- p95 latency < 100 ms locally.
- Single-process, SQLite.

## 5. Architecture style
- Layered: router → service → repository → SQLite.
- In-memory SQLite for tests.

## 6. Security baseline
- Input validation.
- No secrets.

## 7. Definition of Done
- [ ] Endpoint works and manually tested.
- [ ] Unit + integration tests added.
- [ ] Lint passes.
- [ ] README updated.
