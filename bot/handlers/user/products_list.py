import logging
import re

from aiogram import types
from aiogram.enums import ContentType
from aiogram.types import CallbackQuery
from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.kbd import Row, Button
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.text import Const, Format

from dialogs.dialogs_data import get_card_data
from dialogs.dialogs_states import ProductsListSG, MainSG, ProductSG
from exceptions import WrongProductQuery, ProductNotFoundError, ApiRequestError
from models.product import Product
from services import http_services

logger = logging.getLogger(__name__)


async def _get_card_data(**kwargs):
    manager: DialogManager = kwargs['dialog_manager']
    product_id = manager.dialog_data.get('current_card_id')

    card_data = (await get_card_data(product_id)).model_dump()
    card_data['photo'] = MediaAttachment(ContentType.PHOTO, url=card_data['image_url'])
    return card_data


async def on_dialog_start(start_data: list, manager: DialogManager):
    manager.dialog_data['current_index'] = 0
    manager.dialog_data['cards_data'] = start_data
    manager.dialog_data['current_card_id'] = start_data[manager.dialog_data['current_index']]
    logger.debug(manager.dialog_data['current_index'])


async def _btn_prev(callback: CallbackQuery, button: Button, manager: DialogManager):
    cards_data = manager.dialog_data['cards_data']
    current_index = manager.dialog_data['current_index']

    manager.dialog_data['current_index'] = len(cards_data) - 1 if (current_index - 1 < 0) else current_index - 1
    manager.dialog_data['current_card_id'] = manager.dialog_data['cards_data'][manager.dialog_data['current_index']]

    logger.debug(manager.dialog_data['current_index'])


async def _btn_next(callback: CallbackQuery, button: Button, manager: DialogManager):
    cards_data = manager.dialog_data['cards_data']
    current_index = manager.dialog_data['current_index']
    manager.dialog_data['current_index'] = current_index + 1 if (current_index + 1 < len(cards_data)) else 0
    manager.dialog_data['current_card_id'] = manager.dialog_data['cards_data'][manager.dialog_data['current_index']]

    logger.debug(manager.dialog_data['current_index'])


async def _btn_back(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.start(MainSG.main)


async def _btn_add(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.start(ProductSG.add)


window = Window(
    DynamicMedia('photo'),
    Format('{name}'),
    Format('Старая цена: {current_price}'),
    Format('Новая цена: {previous_price}'),
    Format('{url}'),
    Row(
        Button(Const('◀️'), id='btn_prev', on_click=_btn_prev),
        Button(Const('▶️'), id='btn_next', on_click=_btn_next)
    ),
    Row(
        Button(Const('Назад'), id='btn_back', on_click=_btn_back),
        Button(Const('Добавить'), id='btn_add', on_click=_btn_add)
    ),
    getter=_get_card_data,
    state=ProductsListSG.all
)

dialog = Dialog(window, on_start=on_dialog_start)


async def get_product(message: types.Message):
    try:
        item_id = _parse_message(message.text)
        item_info = await http_services.get_product_info(message.from_user.id, item_id)
    except WrongProductQuery:
        error_text = 'Неверный запрос'
    except ProductNotFoundError:
        error_text = f'По идентификатору {item_id} товар не найден'
    except ApiRequestError:
        error_text = 'Нет связи с сервером БД'
    else:
        await message.answer_photo(**_format_product_photo(item_info), parse_mode='html')
        return

    await message.answer(error_text)


def _parse_message(message: str) -> int:
    if message.isdigit():
        return int(message)

    url = re.findall(r'http.*\d{1,10}', message)

    try:
        item_id = int(next(iter(url)).split('/')[-1])
    except (IndexError, ValueError, StopIteration):
        logging.error(f'can`t parse{url}')
        raise WrongProductQuery

    return item_id


def _format_product_photo(product_info: Product):
    return {
        'photo': product_info.image_url,
        'caption': f'<b>{product_info.name}</b>\n'
                   f'Старая цена: {product_info.previous_price} руб.\n'
                   f'Новая цена: {product_info.current_price} руб.\n'
                   f'{product_info.url}'
    }
