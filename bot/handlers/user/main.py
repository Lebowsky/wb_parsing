from aiogram.types import CallbackQuery

from aiogram_dialog import Window, Dialog, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format

from dialogs.dialogs_data import get_products_ids
from dialogs.dialogs_states import MainSG, ProductSG, ProductsListSG


async def all_products(callback: CallbackQuery, button: Button, manager: DialogManager):
    products_ids, _, __ = await get_products_ids(manager.event.from_user.id)
    await manager.start(ProductsListSG.all, mode=StartMode.RESET_STACK, data=list(products_ids))


async def down_in_price(callback: CallbackQuery, button: Button, manager: DialogManager):
    pass


async def up_in_price(callback: CallbackQuery, button: Button, manager: DialogManager):
    pass


async def add_product(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.start(ProductSG.add, mode=StartMode.RESET_STACK)


async def _on_start_dialog(callback: CallbackQuery, manager: DialogManager):
    manager.dialog_data['products_stats'] = dict(zip(
        ('all_products', 'down_in_price', 'up_in_price'),
        (f' ({len(items)}) ' if items else '' for items in (await get_products_ids(manager.event.from_user.id)))
    ))


async def _get_products_stats(**kwargs):
    return kwargs.get('dialog_manager').dialog_data['products_stats']


main_window = Window(
    Const('Выберите пункт меню:'),
    Button(Format('Мои товары {all_products} 🛒'), id='all_products', on_click=all_products),
    Button(Format('Подешевело {down_in_price} ↘️'), id='down_in_price', on_click=down_in_price),
    Button(Format('Подорожало {up_in_price} ↗️'), id='up_in_price', on_click=up_in_price),
    Button(Const('Добавить ➕'), id='add_product', on_click=add_product),
    getter=_get_products_stats,
    state=MainSG.main,
)

dialog = Dialog(main_window, on_start=_on_start_dialog)
