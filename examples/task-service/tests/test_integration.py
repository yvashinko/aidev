from fastapi.testclient import TestClient

from task_service.main import app
from task_service.repository import Base, engine

client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def teardown_function():
    Base.metadata.drop_all(engine)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200


def test_create_and_get_task():
    r = client.post("/tasks", json={"title": "learn AI"})
    assert r.status_code == 201
    body = r.json()
    assert body["title"] == "learn AI"
    assert body["status"] == "todo"

    r2 = client.get(f"/tasks/{body['id']}")
    assert r2.status_code == 200
    assert r2.json()["id"] == body["id"]


def test_get_task_not_found():
    r = client.get("/tasks/999")
    assert r.status_code == 404


def test_create_task_validation():
    r = client.post("/tasks", json={"title": ""})
    assert r.status_code == 422
