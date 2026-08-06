from aiogram import Router, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from app.core.config import settings
from app.db.base import User
from app.services.user_serv import UserService
from app.integrations.telegram.keyboards.tz_kb import tz_keyboard, tz_of_key
from app.integrations.telegram.utils.media import get_photo

router = Router()

@router.message(CommandStart())
async def start_chat(msg: Message, user: User, is_new_user: bool):
    if is_new_user:
        await msg.answer_photo(photo=get_photo("start"),
            caption=f"Привет, {user.first_name}! Рада тебя видеть тут, вібери часовой пояс и давай знакомиться",
            reply_markup=tz_keyboard())
    else:
        await msg.answer_photo(photo=get_photo("start"),
            caption=f"Привет, {user.first_name}! твой айди  {user.id}")


@router.callback_query(F.data.startswith("tz:"))
async def pick_tz_start(call: CallbackQuery):
    # Выбор пояса на СТАРТ-экране: сохраняем и показываем главное меню.
    key = call.data.split(":", 1)[1]
    iana = tz_of_key(key)
    if iana is None:
        await call.answer("Неизвестный пояс, попробуй ещё раз", show_alert=True)
        return
    await UserService.set_tz(call.from_user.id, iana)
    await call.message.edit_media(media=InputMediaPhoto(
        media=get_photo("success"),
        caption="Часовой пояс сохранён. Теперь ты можешь пользоваться ботом."),
        reply_markup=None
    )
    await call.answer()
    return
    