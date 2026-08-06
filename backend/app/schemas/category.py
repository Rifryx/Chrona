from pydantic import BaseModel, field_validator
from app.db.base import Priority, TaskKind
from datetime import datetime
from uuid import UUID

class CategoryCreate(BaseModel):
    name: str
    icon: str
    color: str

class CategoryUpdate(BaseModel):
    name: str | None = None
    icon: str | None = None
    color: str | None = None
