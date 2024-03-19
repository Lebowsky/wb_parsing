import logging
import re
from aiogram import types

from exceptions import WrongProductQuery, ProductNotFoundError, ApiRequestError
from models.product import Product
from services import http_services


async def get_product(message: types.Message):
    try:
        item_id = _parse_message(message.text)
        item_info = await http_services.get_product_info(item_id)
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
