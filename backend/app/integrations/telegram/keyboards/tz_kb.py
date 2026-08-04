from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


TIMEZONES: dict[str, tuple[str, str]] = {
    "kyiv":     ("🇺🇦 Киев",       "Europe/Kyiv"),
    "moscow":   ("🇷🇺 Москва",     "Europe/Moscow"),
    "minsk":    ("🇧🇾 Минск",      "Europe/Minsk"),
    "warsaw":   ("🇵🇱 Варшава",    "Europe/Warsaw"),
    "berlin":   ("🇩🇪 Берлин",     "Europe/Berlin"),
    "london":   ("🇬🇧 Лондон",     "Europe/London"),
    "istanbul": ("🇹🇷 Стамбул",    "Europe/Istanbul"),
    "almaty":   ("🇰🇿 Алматы",     "Asia/Almaty"),
    "tbilisi":  ("🇬🇪 Тбилиси",    "Asia/Tbilisi"),
    "dubai":    ("🇦🇪 Дубай",      "Asia/Dubai"),
}

# Обратный индекс: IANA-имя → подпись. Нужен, чтобы показать юзеру его
# текущий пояс человекочитаемо (по значению из БД).
_IANA_TO_LABEL = {iana: label for label, iana in TIMEZONES.values()}


def tz_of_key(key: str) -> str | None:
    """'kyiv' → 'Europe/Kyiv'. None, если ключа нет (защита от левого callback)."""
    row = TIMEZONES.get(key)
    return row[1] if row else None


def label_of_tz(iana: str | None) -> str:
    """'Europe/Kyiv' → '🇺🇦 Киев'. Неизвестный/None → 'не выбран'."""
    if not iana:
        return "не выбран"
    return _IANA_TO_LABEL.get(iana, iana)


def tz_keyboard(prefix: str = "tz") -> InlineKeyboardMarkup:
    
    kb = InlineKeyboardBuilder()
    for key, (label, _iana) in TIMEZONES.items():
        kb.button(text=label, callback_data=f"{prefix}:{key}")
    kb.adjust(2)
    return kb.as_markup()
