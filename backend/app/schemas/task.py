from pydantic import BaseModel, field_validator
from app.db.base import Priority, TaskKind
from datetime import datetime
from uuid import UUID

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    priority: Priority
    estimated_duration: int
    deadline: datetime | None = None
    category_id: int | None = None
    project_id: int | None = None
    kind: TaskKind
    is_flexible: bool = True


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: Priority | None = None
    estimated_duration: int | None = None
    deadline: datetime | None = None
    category_id: int | None = None
    project_id: int | None = None
    kind: TaskKind | None = None
    is_flexible: bool | None = None

    @field_validator("category_id", "project_id", mode="before")
    @classmethod
    def normalize_fk_zero(cls, value):
        if value == 0:
            return None
        return value