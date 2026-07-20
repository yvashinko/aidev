from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from task_service.models import Task, TaskCreate
from task_service.repository import TaskRepository, get_db
from task_service.service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_service(db: Session = Depends(get_db)) -> TaskService:
    return TaskService(TaskRepository(db))


@router.post("", response_model=Task, status_code=201)
def create_task(data: TaskCreate, service: TaskService = Depends(get_service)):
    return service.create(data)


@router.get("", response_model=list[Task])
def list_tasks(service: TaskService = Depends(get_service)):
    return service.list()


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int, service: TaskService = Depends(get_service)):
    return service.get(task_id)
