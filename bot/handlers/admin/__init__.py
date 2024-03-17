from aiogram import Dispatcher
from aiogram.filters import Command

from filters.admin import IsAdminFilter
from .config import config


def register_handlers(dp: Dispatcher):
    # dp.message.register(config, Command(commands='config'), IsAdminFilter())
    dp.message.register(config, IsAdminFilter())
