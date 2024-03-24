import re
import logging

from aiogram.types import Message

from aiogram_dialog import Window, Dialog, DialogManager, StartMode
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.text import Const

from dialogs.dialogs_states import ProductSG, MainSG

logger = logging.getLogger(__name__)


async def add_product(message: Message, __: ManagedTextInput, manager: DialogManager, data: str):
    if _is_product_id(data):
        logger.debug('success')
        await manager.start(MainSG.main, mode=StartMode.RESET_STACK)
    else:
        await message.answer(f'Некорректный ввод {data}')
        logger.info(data)


async def failure_input(message: Message, __: ManagedTextInput, manager: DialogManager, error):
    await message.answer('Некорректный ввод')
    await manager.start(ProductSG.add, mode=StartMode.RESET_STACK)


add_product_window = Window(
    Const('Отправь ссылку на товар или его ID:'),
    TextInput('product_link', on_success=add_product, on_error=failure_input),
    state=ProductSG.add
)

dialog = Dialog(add_product_window)


def _is_product_id(message: str) -> bool:
    if message.isdigit():
        return True

    url = re.findall(r'http.*\d{1,10}', message)

    try:
        return bool(int(next(iter(url)).split('/')[-1]))
    except (IndexError, ValueError, StopIteration):
        return False