from typing import Set

from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery


class IsUserPermitted(Filter):
    def __init__(self, user_ids: Set[int] | int):
        if isinstance(user_ids, int):
            self.user_ids = [user_ids]
        else:
            self.user_ids = set(user_ids)

    async def __call__(self, query: Message | CallbackQuery):
        return query.from_user.id in self.user_ids
