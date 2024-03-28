from aiogram.types import CallbackQuery

from aiogram_dialog import Window, Dialog, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from dialogs.dialogs_states import MainSG, ProductSG


async def all_products(callback: CallbackQuery, button: Button, manager: DialogManager):
    pass
    # dialog_data = manager.dialog_data
    # event = manager.event
    # middleware_data = manager.middleware_data
    # start_data = manager.start_data


async def down_in_price(callback: CallbackQuery, button: Button, manager: DialogManager):
    pass


async def up_in_price(callback: CallbackQuery, button: Button, manager: DialogManager):
    pass


async def add_product(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.start(ProductSG.add, mode=StartMode.RESET_STACK)


main_window = Window(
    Const('Выберите пункт меню:'),
    Button(Const('Мои товары 🛒'), id='all_products', on_click=all_products),
    Button(Const('Подешевело ↘️'), id='down_in_price', on_click=down_in_price),
    Button(Const('Подорожало ↗️'), id='up_in_price', on_click=up_in_price),
    Button(Const('Добавить ➕'), id='add_product', on_click=add_product),
    state=MainSG.main,
)

dialog = Dialog(main_window)
