import asyncio
import json
import logging.config
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from dialogs.dialogs import main_dialog, four_digits_dialog, five_digits_dialog, six_digits_dialog
from handlers.handlers import start

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dialog_router = Router()
    dialog_router.include_router(main_dialog)
    dialog_router.include_router(four_digits_dialog)
    dialog_router.include_router(five_digits_dialog)
    dialog_router.include_router(six_digits_dialog)
    dp = Dispatcher(storage=MemoryStorage())
    dp.message.register(start, CommandStart())
    dp.include_router(dialog_router)
    setup_dialogs(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())



if __name__ == "__main__":
    logger_config_path = os.path.join(os.path.dirname(__file__), 'logger', 'config.json')
    with open(logger_config_path, 'r') as f:
        logger_config = json.load(f)
        logging.config.dictConfig(logger_config)
    logger = logging.getLogger(__name__)
    logger.warning("Bot v1.3.0 started")
    asyncio.run(main())
