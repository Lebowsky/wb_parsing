from aiogram import Dispatcher
from aiogram.filters import Command

from filters.admin import IsAdminFilter

from .start import start

from . import (
    main,
    product_commands,
    product_view,
    products_list
)


def register_handlers(dp: Dispatcher):
    dp.message.register(start, IsAdminFilter(), Command('start'))

    dp.include_router(main.dialog)
    dp.include_router(product_commands.dialog)
    dp.include_router(product_view.dialog)
    dp.include_router(products_list.dialog)
