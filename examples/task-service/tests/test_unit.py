import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from task_service.models import TaskCreate
from task_service.repository import Base, TaskRepository
from task_service.service import TaskService


@pytest.fixture
def db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def service(db):
    return TaskService(TaskRepository(db))


def test_create_task(service):
    data = TaskCreate(title="learn AI")
    task = service.create(data)
    assert task.id == 1
    assert task.status == "todo"


def test_get_task_not_found(service):
    with pytest.raises(Exception) as exc:
        service.get(999)
    assert exc.value.status_code == 404


def test_create_task_title_too_long():
    with pytest.raises(ValueError):
        TaskCreate(title="x" * 201)
