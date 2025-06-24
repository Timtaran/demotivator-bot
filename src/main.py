import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot import all_routers, CheckUserPermissionMiddleware
from settings import settings

dp = Dispatcher()


async def main() -> None:
    bot = Bot(
        token=settings.bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp.include_routers(*all_routers)

    if settings.is_private:
        dp.message.outer_middleware(CheckUserPermissionMiddleware())
        dp.callback_query.outer_middleware(CheckUserPermissionMiddleware())

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG if settings.debug_mode else logging.INFO,
        format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    )
    asyncio.run(main())
