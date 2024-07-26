import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs
from dotenv import load_dotenv

from dialogs.dialogs import main_dialog
from handlers import router, start
from menu import main_menu_commands
import db

# exporting BOT_TOKEN from env file
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


async def main():
    db.connection.connect()
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher(storage=MemoryStorage())
    dp.message.register(start, CommandStart())
    dp.include_router(main_dialog)
    setup_dialogs(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    db.connection.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
