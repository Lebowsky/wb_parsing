import logging
from typing import Any

from aiogram.types import ContentType
from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.media import StaticMedia, DynamicMedia
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.widgets.text import Const

from dialogs.dialogs_states import ProductViewSG
from exceptions import ProductNotFoundError
from models.product import Product
from services import http_services

logger = logging.getLogger(__name__)


async def _get_data(**kwargs):
    manager: DialogManager = kwargs['dialog_manager']
    product_info: Product = manager.dialog_data.get('product_info')

    image = MediaAttachment(
        ContentType.PHOTO,
        url=product_info.image_url)
    return {'photo': image}


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



    # item_info = await http_services.get_product_info(message.from_user.id, item_id)

    # manager.dialog_data['user'] = {
    #     'test_result': True,
    # }


product_view_window = Window(
    DynamicMedia('photo'),
    state=ProductViewSG.view,
    getter=_get_data,
)

product_not_found_window = Window(
    Const('Товар не найден'),
    state=ProductViewSG.error
)

dialog = Dialog(product_view_window, product_not_found_window, on_start=on_dialog_start)
