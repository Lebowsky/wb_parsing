import logging
from typing import Any

from aiogram.types import ContentType, CallbackQuery
from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Row, Button
from aiogram_dialog.widgets.media import StaticMedia, DynamicMedia
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.widgets.text import Const, Format

from dialogs.dialogs_states import ProductViewSG, MainSG, ProductSG
from exceptions import ProductNotFoundError
from handlers.user.product_commands import add_product, failure_input
from models.product import Product
from services import http_services

logger = logging.getLogger(__name__)


async def _get_data(**kwargs):
    manager: DialogManager = kwargs['dialog_manager']
    product_info: Product = manager.dialog_data.get('product_info')

    image = MediaAttachment(
        ContentType.PHOTO,
        url=product_info.image_url)

    result = {'photo': image}
    result.update(product_info)

    return result


async def _btn_back(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.start(MainSG.main)


async def _btn_add(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.start(ProductSG.add)


async def on_dialog_start(start_data: Any, manager: DialogManager):
    if not start_data:
        return
    user_id = manager.event.from_user.id
    product_id = start_data.get('product_id')
    try:
        product_info = await http_services.get_product_info(user_id, product_id)
        manager.dialog_data['product_info'] = product_info
    except ProductNotFoundError:
        await manager.start(ProductViewSG.error)


product_view_window = Window(
    DynamicMedia('photo'),
    Const('Товар успешно добавлен:'),
    Format('{name}'),
    Format('Прошлая цена: {current_price}'),
    Format('Текущая цена: {previous_price}'),
    Format('{url}'),
    Row(
        Button(Const('Назад'), id='back', on_click=_btn_back),
        Button(Const('Добавить еще'), id='add_more', on_click=_btn_add)
    ),
    state=ProductViewSG.view,
    getter=_get_data,
)

product_not_found_window = Window(
    Const('Товар не найден, попробуйте еще'),
    TextInput('product_link', on_success=add_product, on_error=failure_input),
    state=ProductViewSG.error
)

dialog = Dialog(product_view_window, product_not_found_window, on_start=on_dialog_start)
