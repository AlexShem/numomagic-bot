import os
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Update
from aiogram_dialog import setup_dialogs
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response

from dialogs.dialogs import (
    main_dialog,
    four_digits_dialog,
    five_digits_dialog,
    six_digits_dialog,
    join_channel_dialog,
    payment_dialog,
    subscribe_dialog,
)
from handlers.handlers import start, on_subscribe_command
from aiogram.filters import CommandStart, Command
from logger.logger import get_logger
from middlewares.paywall import ChannelMembershipGate

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
PRO_CHANNEL_ID = int(os.getenv("PRO_CHANNEL_ID", 0))
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")

logger = get_logger(__name__)

# Global bot and dispatcher instances
_bot: Bot | None = None
_dp: Dispatcher | None = None


def get_bot() -> Bot:
    """Get or create bot instance."""
    global _bot
    if _bot is None:
        _bot = Bot(
            token=BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
    return _bot


def get_dispatcher() -> Dispatcher:
    """Get or create dispatcher instance with all routers configured."""
    global _dp
    if _dp is None:
        dialog_router = Router()
        dialog_router.include_router(main_dialog)
        dialog_router.include_router(four_digits_dialog)
        dialog_router.include_router(five_digits_dialog)
        dialog_router.include_router(six_digits_dialog)
        dialog_router.include_router(join_channel_dialog)
        dialog_router.include_router(payment_dialog)
        dialog_router.include_router(subscribe_dialog)

        _dp = Dispatcher(storage=MemoryStorage())
        _dp.message.middleware(ChannelMembershipGate(channel_id=PRO_CHANNEL_ID))
        _dp.callback_query.middleware(ChannelMembershipGate(channel_id=PRO_CHANNEL_ID))
        _dp.message.register(start, CommandStart())
        _dp.message.register(on_subscribe_command, Command("subscribe"))
        _dp.include_router(dialog_router)
        setup_dialogs(_dp)
    return _dp


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager to set/delete webhook on startup/shutdown."""
    bot = get_bot()
    dp = get_dispatcher()

    # Set webhook on startup
    webhook_url = f"{WEBHOOK_URL}/webhook"
    logger.warning(f"Setting webhook to: {webhook_url}")

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(
        url=webhook_url,
        secret_token=WEBHOOK_SECRET if WEBHOOK_SECRET else None,
        allowed_updates=dp.resolve_used_update_types(),
    )
    logger.warning("Webhook set successfully")

    yield

    # Delete webhook on shutdown
    logger.warning("Deleting webhook...")
    is_webhook_deleted = await bot.delete_webhook()
    if is_webhook_deleted:
        logger.warning("Webhook deleted successfully")
    else:
        logger.warning("Failed to delete webhook")
    await bot.session.close()
    logger.warning("Bot stopped")


app = FastAPI(lifespan=lifespan)


@app.post("/webhook")
async def webhook_handler(request: Request) -> Response:
    """Handle incoming Telegram updates via webhook."""
    # Verify secret token if configured
    if WEBHOOK_SECRET:
        secret_header = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
        if secret_header != WEBHOOK_SECRET:
            logger.warning("Invalid webhook secret token received")
            return Response(status_code=403)

    bot = get_bot()
    dp = get_dispatcher()

    # Parse and process the update
    update_data = await request.json()
    update = Update.model_validate(update_data, context={"bot": bot})

    await dp.feed_update(bot=bot, update=update)

    return Response(status_code=200)


@app.get("/health")
async def health_check():
    """Health check endpoint for Railway monitoring."""
    return {"status": "healthy", "bot": "running"}

