from fastapi import HTTPException, status

from task_service.models import Task, TaskCreate
from task_service.repository import TaskRepository


class TaskService:
    def __init__(self, repo: TaskRepository):
        self._repo = repo

    def create(self, data: TaskCreate) -> Task:
        return self._repo.create(data)

    def list(self, limit: int = 100) -> list[Task]:
        return self._repo.list(limit)

    def get(self, task_id: int) -> Task:
        task = self._repo.get(task_id)
        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )
        return task
