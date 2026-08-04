from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from app.services.user_serv import UserService

class RegistrationMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data: dict):
        tg_user = data.get("event_from_user")
        if tg_user is None:
            return await handler(event, data)
        user, is_new = await UserService.get_or_create(tg_id=tg_user.id,
                                                       username=tg_user.username,
                                                       first_name=tg_user.first_name)
        data["user"] = user
        data["is_new_user"] = is_new
        return await handler(event, data)