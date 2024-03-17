from typing import Union

from aiogram.filters import Filter
from aiogram import types

from config import settings


class IsAdminFilter(Filter):
    async def __call__(self, message: Union[types.Message, types.CallbackQuery]) -> bool:
        return message.from_user.id in settings.admins_id
