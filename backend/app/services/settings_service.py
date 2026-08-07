from datetime import datetime
from typing import Any
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.settings import SettingsDelete, SettingsUpdate
from app.db.base import UserSettings
from app.db.session import session_factory

def get_settings_service():
    return SettingsService()

class SettingsService():

    @staticmethod
    async def get_settings(us_id: int) -> UserSettings | None:
        async with session_factory() as session:
            res = await session.execute(select(UserSettings).where(UserSettings.user_id==us_id))
            return res.scalar_one_or_none()
    
    @staticmethod
    async def create_sett(us_id: int, tz: str) -> UserSettings | None:
        async with session_factory() as session:
            new_sett = UserSettings(
                user_id=us_id,
                timezone=tz,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(new_sett)
            try:
                await session.flush()
                await session.commit()
                await session.refresh(new_sett)
                return new_sett
            except IntegrityError:
                await session.rollback()
                raise ValueError("settings not create due to integrity error")

    @staticmethod
    async def get_tz(us_id: int) -> str | None:
        async with session_factory() as session:
            result = await session.execute(select(UserSettings.timezone).where(UserSettings.user_id == us_id))
            return result.scalar_one_or_none()

    @staticmethod
    async def update_settings(us_id: int, sett_data: SettingsUpdate) -> UserSettings:
        update_data = {
            key: value for key, value in sett_data.model_dump().items()
            if key in sett_data.model_fields_set
        }
        if not update_data:
            exis = await SettingsService.get_settings(us_id=us_id)
            if exis is None:
                raise ValueError("User settings not found")
            return exis
        update_data["updated_at"] = datetime.utcnow()
        async with session_factory() as session:
            result =  await session.execute(select(UserSettings).where(UserSettings.user_id==us_id))
            exis = result.scalar_one_or_none()
            if exis is None:
                raise ValueError("User settings not found")

            await session.execute(update(UserSettings).where(
                UserSettings.user_id==us_id)
                .values(**update_data)
            )
            try:
                await session.commit()
            except IntegrityError:
                await session.rollback()
                raise ValueError("User settings failed due to Inegrity error")
            await session.refresh(exis)
            return exis
    @staticmethod
    async def delete_sett(us_id: int, del_sett_data: SettingsDelete) -> UserSettings:
        deleted_data = {
            key: None
            for key in del_sett_data.model_dump(exclude_unset=True).keys()
        }
        if not deleted_data:
            exis = await SettingsService.get_settings(us_id=us_id)
            if exis is None:
                raise ValueError("sett not found")
            return exis
        deleted_data["updated_at"] = datetime.utcnow()
        async with session_factory() as session:
            await session.execute(
                update(UserSettings)
                .where(UserSettings.user_id == us_id)
                .values(**deleted_data)
            )
            await session.commit()

