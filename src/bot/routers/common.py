from aiogram import Router
from aiogram.types import Message

common_router = Router()


@common_router.message()
async def default_answer(message: Message):
    await message.answer(
        "Привет! Это бот для создания GIF-демотиваторов из GIF, видео и картинок\n\n"
        "Чтобы сделать демотиватор, отправьте GIF, видео или картинку с подписью"
    )
