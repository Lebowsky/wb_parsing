from aiogram import Dispatcher

from . import admin, user


def register_handlers(dp: Dispatcher):
    user.register_handlers(dp)
    admin.register_handlers(dp)
