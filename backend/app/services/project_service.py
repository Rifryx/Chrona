from datetime import datetime
from typing import Any
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.db.base import Project
from app.db.session import session_factory


def get_project_service():
    return ProjectService()


class ProjectService:
    @staticmethod
    async def create_project(us_id: int, project: ProjectCreate) -> Project:
        async with session_factory() as session:
            new_project = Project(
                user_id=us_id,
                title=project.title,
                description=project.description,
                status=project.status,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            session.add(new_project)
            try:
                await session.commit()
                await session.refresh(new_project)
                return new_project
            except IntegrityError:
                await session.rollback()
                raise ValueError("Project creation failed due to integrity error.")

    @staticmethod
    async def get_project(us_id: int, project_id: int) -> Project | None:
        async with session_factory() as session:
            result = await session.execute(
                select(Project).where(Project.user_id == us_id, Project.id == project_id)
            )
            return result.scalar_one_or_none()

    @staticmethod
    async def get_projects(us_id: int) -> list[Project]:
        async with session_factory() as session:
            result = await session.execute(select(Project).where(Project.user_id == us_id))
            return result.scalars().all()

    @staticmethod
    async def update_project(us_id: int, project_id: int, project_data: ProjectUpdate) -> Project:
        update_data: dict[str, Any] = {
            key: value
            for key, value in project_data.model_dump().items()
            if key in project_data.model_fields_set
        }
        if not update_data:
            existing = await ProjectService.get_project(us_id, project_id)
            if existing is None:
                raise ValueError("Project not found.")
            return existing

        update_data["updated_at"] = datetime.utcnow()
        async with session_factory() as session:
            result = await session.execute(
                select(Project).where(Project.user_id == us_id, Project.id == project_id)
            )
            existing = result.scalar_one_or_none()
            if existing is None:
                raise ValueError("Project not found.")

            await session.execute(
                update(Project)
                .where(Project.user_id == us_id, Project.id == project_id)
                .values(**update_data)
            )
            try:
                await session.commit()
            except IntegrityError:
                await session.rollback()
                raise ValueError("Project update failed due to integrity error.")
            await session.refresh(existing)
            return existing

    @staticmethod
    async def soft_delete_project(us_id: int, project_id: int) -> Project:
        async with session_factory() as session:
            result = await session.execute(
                select(Project).where(Project.user_id == us_id, Project.id == project_id)
            )
            existing = result.scalar_one_or_none()
            if existing is None:
                raise ValueError("Project not found.")
            await session.execute(
                update(Project)
                .where(Project.user_id == us_id, Project.id == project_id)
                .values(deleted_at=datetime.utcnow())
            )
            try:
                await session.commit()
            except IntegrityError:
                await session.rollback()
                raise ValueError("Project soft delete failed due to integrity error.")
            await session.refresh(existing)
            return existing

    @staticmethod
    async def harsh_delete_project(us_id: int, project_id: int) -> dict[str, int | bool]:
        async with session_factory() as session:
            result = await session.execute(
                select(Project).where(Project.user_id == us_id, Project.id == project_id, Project.deleted_at.is_not(None))
            )
            existing = result.scalar_one_or_none()
            if existing is None:
                raise ValueError("Soft deleted project not found.")
            await session.delete(existing)
            try:
                await session.commit()
            except IntegrityError:
                await session.rollback()
                raise ValueError("Project deletion failed due to integrity error.")
            return {"project_id": project_id, "deleted": True}
