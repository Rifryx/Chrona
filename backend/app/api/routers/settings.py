from fastapi import APIRouter
from app.schemas.settings import SettingsDelete, SettingsUpdate
from app.services.settings_service import SettingsService, get_settings_service
from fastapi import Depends
from app.db.base import Task
from uuid import UUID


router = APIRouter()

@router.get("/user/{us_id}/settings", tags=["settings"])
async def get_sett_mh(us_id: int, service: SettingsService = Depends(get_settings_service)):
    result = await SettingsService.get_settings(us_id)
    return result

@router.patch("/user/{us_id}/settings", tags=["settings"])
async def update_sett_mh(us_id: int, task: SettingsUpdate, service: SettingsService = Depends(get_settings_service)):
    return await SettingsService.update_settings(us_id=us_id, sett_data=task)

@router.delete("/user/{us_id}/settings", tags=["settings"])
async def delete_sett_mh(us_id: int, task: SettingsUpdate, service: SettingsService = Depends(get_settings_service)):
    return await SettingsService.delete_sett(us_id=us_id, del_sett_data=task)
