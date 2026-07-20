install:
	pip install -e ".[dev]"

run:
	uvicorn task_service.main:app --reload --port 8000

test:
	pytest -q

lint:
	ruff check src tests
	ruff format --check src tests
