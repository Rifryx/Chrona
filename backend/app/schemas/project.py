from pydantic import BaseModel
from app.db.base import ProjectStatus


class ProjectCreate(BaseModel):
    title: str
    description: str | None = None
    status: ProjectStatus = ProjectStatus.ACTIVE


class ProjectUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: ProjectStatus | None = None
