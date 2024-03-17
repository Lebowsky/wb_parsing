import asyncio
import sys
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage, SimpleEventIsolation
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import BotCommandScopeAllGroupChats, BotCommand, BotCommandScopeAllPrivateChats, BotCommandScopeChat

# from aiogram_dialog import DialogRegistry
from config import settings


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=settings.token)
    dp = Dispatcher(storage=MemoryStorage(), events_isolation=SimpleEventIsolation())
    # registry = DialogRegistry()

    print('Бот запущен')
    await dp.start_polling(bot)


if __name__ == '__main__':
    if sys.platform == "win32" and sys.version_info.minor >= 8:
        asyncio.set_event_loop_policy(
            asyncio.WindowsSelectorEventLoopPolicy()
        )
    asyncio.run(main())
