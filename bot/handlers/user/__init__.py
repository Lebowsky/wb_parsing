from aiogram import Dispatcher

from filters.product import IsProductIdFilter
from .products import get_product
from filters.admin import IsAdminFilter


def register_handlers(dp: Dispatcher):
    dp.message.register(get_product, IsAdminFilter(), IsProductIdFilter())
    # dp.message.register(stop, Command(commands='stop'))
    # dp.callback_query.register(hide_message, Text(text='hide_message'))
