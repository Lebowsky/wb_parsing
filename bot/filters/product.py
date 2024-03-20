from typing import Union
import re

from aiogram.filters import Filter
from aiogram import types

from config import settings


class IsProductIdFilter(Filter):
    async def __call__(self, message: Union[types.Message, types.CallbackQuery]) -> bool:
        return _is_product_id(message.text)


def _is_product_id(message: str) -> bool:
    if message.isdigit():
        return True

    url = re.findall(r'http.*\d{1,10}', message)

    try:
        return bool(int(next(iter(url)).split('/')[-1]))
    except (IndexError, ValueError, StopIteration):
        return False
