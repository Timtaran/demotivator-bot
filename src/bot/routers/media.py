import os

from aiogram import Router, F
from aiogram.types import Message, Animation, PhotoSize, Video, FSInputFile

from utils import DemotivatorCreator

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

demotivator = DemotivatorCreator()
media_router = Router()


@media_router.message(F.photo)
async def photo_handler(message: Message):
    await process_media(message, message.photo[-1])


@media_router.message(F.video)
async def video_handler(message: Message):
    await process_media(message, message.video)


@media_router.message(F.animation)
async def handler(message: Message):
    await process_media(message, message.animation)


async def process_media(message: Message, media: Animation | Video | PhotoSize):
    if media.file_size > MAX_FILE_SIZE:
        await message.answer("Размер файла слишком большой")
        return

    msg = await message.answer("Обработка...")
    res = await demotivator.create_demotivator(message.bot, media, message.caption)

    await message.answer_animation(FSInputFile(res))

    await msg.delete()
    os.unlink(res)
