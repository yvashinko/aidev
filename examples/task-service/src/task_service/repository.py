from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from task_service.config import settings
from task_service.models import Task, TaskCreate, TaskStatus

Base = declarative_base()


class TaskORM(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, default="")
    status = Column(String, default=TaskStatus.todo.value)
    created_at = Column(DateTime, default=datetime.utcnow)


engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class TaskRepository:
    def __init__(self, db: Session):
        self._db = db

    def create(self, task: TaskCreate) -> Task:
        orm = TaskORM(title=task.title, description=task.description)
        self._db.add(orm)
        self._db.commit()
        self._db.refresh(orm)
        return Task.model_validate(orm)

    def list(self, limit: int = 100) -> list[Task]:
        rows = (
            self._db.query(TaskORM)
            .order_by(TaskORM.created_at.desc())
            .limit(limit)
            .all()
        )
        return [Task.model_validate(r) for r in rows]

    def get(self, task_id: int) -> Task | None:
        row = self._db.query(TaskORM).filter(TaskORM.id == task_id).first()
        if row is None:
            return None
        return Task.model_validate(row)
