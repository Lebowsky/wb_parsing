import re
import logging

from aiogram.types import Message

from aiogram_dialog import Window, Dialog, DialogManager, StartMode
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.text import Const

from dialogs.dialogs_states import ProductSG, ProductViewSG
from exceptions import WrongProductQuery

logger = logging.getLogger(__name__)


async def add_product(message: Message, __: ManagedTextInput, manager: DialogManager, data: str):
    try:
        product_id = _get_id_from_message(data)
        await manager.start(ProductViewSG.view, mode=StartMode.RESET_STACK, data={'product_id': product_id})
    except WrongProductQuery:
        await message.answer(f'Некорректный ввод {data}')


async def failure_input(message: Message, __: ManagedTextInput, manager: DialogManager, error):
    await message.answer('Некорректный ввод')
    await manager.start(ProductSG.add, mode=StartMode.RESET_STACK)


add_product_window = Window(
    Const('Отправь ссылку на товар или его ID:'),
    TextInput('product_link', on_success=add_product, on_error=failure_input),
    state=ProductSG.add
)

dialog = Dialog(add_product_window)


def _get_id_from_message(message_text: str):
    if message_text.isdigit():
        return True

    url = re.findall(r'http.*\d{1,10}', message_text)

    try:
        return int(next(iter(url)).split('/')[-1])
    except (IndexError, ValueError, StopIteration, TypeError):
        logging.error(f'can`t parse{url}')
        raise WrongProductQuery
