from aiogram import Dispatcher
from aiogram.filters import Command

from filters.admin import IsAdminFilter



def register_handlers(dp: Dispatcher):
    pass
    # dp.message.register(config, Command(commands='config'), IsAdminFilter())
    # dp.message.register(get_product, IsAdminFilter())
    # dp.message.register(get_product)
