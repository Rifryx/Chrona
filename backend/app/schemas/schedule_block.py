from pydantic import BaseModel, field_validator
from app.db.base import Priority, TaskKind
from datetime import datetime, time
from uuid import UUID

class ScheduleBlockCreate(BaseModel):
    task_id: int | None
    start_time: time
    end_time: time
    order_index: int

class ScheduleBlockUpdate(BaseModel):
    task_id: int | None
    start_time: time | None
    end_time: time | None
    order_index: int | None