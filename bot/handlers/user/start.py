from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from dialogs.dialogs_states import MainSG


async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MainSG.main, mode=StartMode.RESET_STACK)
