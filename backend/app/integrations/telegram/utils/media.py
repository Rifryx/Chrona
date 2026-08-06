import os
from aiogram.types import FSInputFile, InputMediaPhoto, InputMediaVideo


media_dict = {
    "start": "app/integrations/telegram/media/start.png"
}

def get_photo(key: str)->FSInputFile:
    file_path = media_dict.get(key)
    if not file_path or not os.path.exists(file_path):
        raise FileNotFoundError("file not found")
    return FSInputFile(path=file_path)
