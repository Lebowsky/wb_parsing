import logging
import re
from aiogram import types

from exceptions import WrongProductQuery, ProductNotFoundError
from wb_services import get_card_details, ProductModel


async def get_product(message: types.Message):
    try:
        item_id = _parse_message(message.text)
    except WrongProductQuery:
        await message.answer('Неверный запрос')
        return

    if item_id:
        logging.info(f'item_id: %s' % item_id)
        try:
            item_info = get_card_details(item_id)
            await message.answer_photo(**format_product_photo(item_info), parse_mode='html')
        except ProductNotFoundError:
            await message.answer(f'Товар с идентификатором {item_id} не найден', parse_mode='html')


def _parse_message(message: str) -> int:
    if message.isdigit():
        return int(message)

    url = re.findall(r'http.*\d{1,10}', message)

    if url:
        try:
            item_id = int(url[0].split('/')[-1])
        except (IndexError, ValueError):
            logging.error(f'can`t parse{url}')
            raise WrongProductQuery

        return int(item_id)
    else:
        raise WrongProductQuery


def format_product_photo(product_info: ProductModel):
    return {
        'photo': product_info.image_url,
        'caption': f'<b>{product_info.name}</b>\n'
                   f'Цена: {product_info.price} руб.\n'
                   f'{product_info.url}'
    }


def format_product_info(product: ProductModel) -> str:
    return (
        f'<b>{product.name}</b>\n'
        f'Цена: {product.price} руб.\n'
        f'Ссылка: {product.url}\n'
        f'{product.image_url}'
    )
