import asyncio
import os

from logger.logger import get_logger
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from dialogs.dialogs import main_dialog, four_digits_dialog, five_digits_dialog, six_digits_dialog, join_channel_dialog
from handlers.handlers import start

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
logger = get_logger(__name__)


async def main():
    logger.warning("Bot is starting")
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dialog_router = Router()
    dialog_router.include_router(main_dialog)
    dialog_router.include_router(four_digits_dialog)
    dialog_router.include_router(five_digits_dialog)
    dialog_router.include_router(six_digits_dialog)
    dialog_router.include_router(join_channel_dialog)
    dp = Dispatcher(storage=MemoryStorage())
    dp.message.register(start, CommandStart())
    dp.include_router(dialog_router)
    setup_dialogs(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
