from typing import Callable, Dict, Any, Set, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from bot.filters import IsUserPermitted
from settings import settings


class CheckUserPermissionMiddleware(BaseMiddleware):
    def __init__(self, user_ids: Set[int] | int | None = None):
        if user_ids is None:
            user_ids = settings.admin_ids
        self.filter = IsUserPermitted(user_ids)

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        if await self.filter(event):
            await handler(event, data)
