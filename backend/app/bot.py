import asyncio
from aiogram import Bot, Dispatcher
from app.core.config import settings

from app.integrations.telegram.handlers.start import router
from aiogram.client.default import DefaultBotProperties
from app.middlewares.registration import RegistrationMiddleware

async def start():
    bot = Bot(token=settings.BOT_API, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()

    dp.update.middleware(RegistrationMiddleware())
    dp.include_router(router)


    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start())