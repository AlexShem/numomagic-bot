import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from handlers import router
from menu import main_menu_commands
import db

# exporting BOT_TOKEN from env file
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Creating Dispatcher and router
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)


async def set_menu(bot: Bot):
    await bot.set_my_commands(main_menu_commands)


async def main():
    db.connection.connect()
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await set_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    db.connection.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
