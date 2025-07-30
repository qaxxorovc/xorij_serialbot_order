from data.config import get_admins_ids_from_env
from aiogram.dispatcher.filters import Filter
from aiogram import types


class IsAdmin(Filter):
    async def check(self, message: types.Message) -> bool:
        ADMINS = await get_admins_ids_from_env()
        return message.from_user.id in ADMINS
