from pydantic import BaseModel
from datetime import time


class SettingsUpdate(BaseModel):
    timezone: str| None = None
    planning_start: time | None = None
    planning_end: time | None = None
    profile_description: str | None = None
    weekly_schedule_json: dict | None = None
    notification_enabled: bool | None = None

class SettingsDelete(BaseModel):
    planning_start: time | None = None
    planning_end: time | None = None
    profile_description: str | None = None
    weekly_schedule_json: dict | None = None
    notification_enabled: bool | None = None