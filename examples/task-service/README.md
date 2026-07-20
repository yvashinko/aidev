# Task Service

Учебный backend MVP для курса «ИИ в разработке».
Управляет задачами через REST API.

## Quick start

```bash
cd examples/task-service
python -m venv .venv
source .venv/bin/activate
make install
make run
```

## Smoke test

```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title":"learn AI"}'
```

## Test

```bash
make test
```

## Known limitations

- SQLite по умолчанию.
- Нет аутентификации.
- Нет пагинации.
