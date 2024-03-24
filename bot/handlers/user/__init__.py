from aiogram import Dispatcher
from aiogram.filters import Command

from .products_list import get_product
from filters.admin import IsAdminFilter

from .main import dialog as main_dialog
from .product_commands import dialog as product_commands_dialog
from .start import start


def register_handlers(dp: Dispatcher):
    dp.message.register(start, IsAdminFilter(), Command('start'))
    # dp.message.register(get_product, IsAdminFilter(), IsProductIdFilter())

    dp.include_router(main_dialog)
    dp.include_router(product_commands_dialog)

