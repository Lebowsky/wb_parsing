import asyncio
import sys
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage, SimpleEventIsolation
from aiogram.exceptions import TelegramBadRequest

from aiogram_dialog import setup_dialogs
from config import settings
from handlers import register_handlers

logger = logging.getLogger(__name__)


async def on_startup_notify(bot: Bot):
    for admin in settings.admins_id:
        try:
            text = 'Бот запущен'
            await bot.send_message(chat_id=admin, text=text)
        except TelegramBadRequest:
            logger.info(f'chat {admin} not found')
        except Exception as err:
            logger.exception(err)


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=settings.token)
    dp = Dispatcher(storage=MemoryStorage(), events_isolation=SimpleEventIsolation())

    register_handlers(dp)
    setup_dialogs(dp)

    await on_startup_notify(bot)

    print('Бот запущен')
    await dp.start_polling(bot)


if __name__ == '__main__':
    if sys.platform == "win32" and sys.version_info.minor >= 8:
        asyncio.set_event_loop_policy(
            asyncio.WindowsSelectorEventLoopPolicy()
        )
    asyncio.run(main())
