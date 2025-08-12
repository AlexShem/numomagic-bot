import asyncio
import os

from logger.logger import get_logger
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from dialogs.dialogs import (
    main_dialog,
    four_digits_dialog,
    five_digits_dialog,
    six_digits_dialog,
    join_channel_dialog,
    payment_dialog, subscribe_dialog,
)
from handlers.handlers import start, on_subscribe_command
from middlewares.paywall import ChannelMembershipGate

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
PRO_CHANNEL_ID = int(os.getenv("PRO_CHANNEL_ID", 0))
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
    dialog_router.include_router(payment_dialog)
    dialog_router.include_router(subscribe_dialog)
    dp = Dispatcher(storage=MemoryStorage())
    dp.message.middleware(ChannelMembershipGate(channel_id=PRO_CHANNEL_ID))
    dp.callback_query.middleware(ChannelMembershipGate(channel_id=PRO_CHANNEL_ID))
    dp.message.register(start, CommandStart())
    dp.message.register(on_subscribe_command, Command("subscribe"))
    dp.include_router(dialog_router)
    setup_dialogs(dp)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        logger.warning("Bot is stopping")
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
