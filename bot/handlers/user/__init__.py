from aiogram import Dispatcher

from products import get_product
from filters.admin import IsAdminFilter


def register_handlers(dp: Dispatcher):
    dp.message.register(get_product, IsAdminFilter())
    # dp.message.register(stop, Command(commands='stop'))
    # dp.callback_query.register(hide_message, Text(text='hide_message'))
