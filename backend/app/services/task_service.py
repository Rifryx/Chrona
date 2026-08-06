from datetime import datetime, timezone
from typing import Any
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from app.schemas.task import TaskCreate, TaskUpdate
from app.db.base import Task, Project
from app.db.session import session_factory


def get_task_service():
    return TaskService()


class TaskService:
    @staticmethod
    async def create_task(us_id: int, task: TaskCreate) -> Task:
        async with session_factory() as session:
            if task.project_id is not None and task.project_id != 0:
                project = await TaskService.get_project(us_id, task.project_id)
                if project is None:
                    raise ValueError("Project not found for the given user.")

            deadline = TaskService._normalize_datetime(task.deadline)
            new_task = Task(
                user_id=us_id,
                title=task.title,
                description=task.description,
                priority=task.priority,
                estimated_duration=task.estimated_duration,
                deadline=deadline,
                category_id=task.category_id,
                project_id=task.project_id,
                kind=task.kind,
                is_flexible=task.is_flexible,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            session.add(new_task)
            try:
                await session.commit()
                await session.refresh(new_task)
                return new_task
            except IntegrityError:
                await session.rollback()
                raise ValueError("Task creation failed due to integrity error.")

    @staticmethod
    def _normalize_datetime(value: datetime | None) -> datetime | None:
        if value is None:
            return None
        if value.tzinfo is not None:
            return value.astimezone(timezone.utc).replace(tzinfo=None)
        return value

    @staticmethod
    async def get_task(us_id: int, task_id: int) -> Task | None:
        async with session_factory() as session:
            result = await session.execute(select(Task).where(Task.user_id == us_id, Task.id == task_id, Task.deleted_at.is_(None)))
            return result.scalar_one_or_none()

    @staticmethod
    async def update_task(us_id: int, task_id: int, task_data: TaskUpdate) -> Task:
        update_data: dict[str, Any] = {
            key: value
            for key, value in task_data.model_dump().items()
            if key in task_data.model_fields_set
        }
        if "deadline" in update_data:
            update_data["deadline"] = TaskService._normalize_datetime(update_data["deadline"])

        if not update_data:
            existing = await TaskService.get_task(us_id, task_id)
            if existing is None:
                raise ValueError("Task not found.")
            return existing

        update_data["updated_at"] = datetime.utcnow()
        async with session_factory() as session:
            result = await session.execute(select(Task).where(Task.user_id == us_id, Task.id == task_id, Task.deleted_at.is_(None)))
            existing = result.scalar_one_or_none()
            if existing is None:
                raise ValueError("Task not found.")

            await session.execute(
                update(Task)
                .where(Task.user_id == us_id, Task.id == task_id)
                .values(**update_data)
            )
            try:
                await session.commit()
            except IntegrityError:
                await session.rollback()
                raise ValueError("Task update failed due to integrity error.")

            await session.refresh(existing)
            return existing

    @staticmethod
    async def soft_delete_task(us_id: int, task_id: int) -> Task:
        async with session_factory() as session:
            res = await session.execute(select(Task).where(Task.id == task_id, Task.user_id == us_id))
            exis = res.scalar_one_or_none()
            if exis is None:
                raise ValueError("Task not found")
            await session.execute(
                update(Task)
                .where(Task.user_id == us_id, Task.id == task_id)
                .values(deleted_at=datetime.utcnow())
            )
            try:
                await session.commit()
            except IntegrityError:
                await session.rollback()
                raise ValueError("Task soft delete failed due to integrity error.")
            await session.refresh(exis)
            return exis

    @staticmethod
    async def harsh_delete_task(us_id: int, task_id: int) -> dict[str, int | bool]:
        async with session_factory() as session:
            res = await session.execute(select(Task).where(Task.id == task_id, Task.user_id == us_id, Task.deleted_at.is_not(None)))
            exs = res.scalar_one_or_none()
            if exs is None:
                raise ValueError("Soft deleted task not found")
            await session.delete(exs)
            try:
                await session.commit()
            except IntegrityError:
                await session.rollback()
                raise ValueError("Task deletion failed due to integrity error.")
            return {"task_id": task_id, "deleted": True}

    @staticmethod
    async def get_project(user_id: int, project_id: int) -> Project | None:
        async with session_factory() as session:
            result = await session.execute(select(Project).where(Project.user_id == user_id, Project.id == project_id))
            return result.scalar_one_or_none()

