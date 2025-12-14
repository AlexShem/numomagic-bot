import os

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

# Cached dispatcher (stateless, can be reused)
_dp: Dispatcher | None = None


def create_bot() -> Bot:
    """Create a new bot instance for this request."""
    return Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )


def get_dispatcher() -> Dispatcher:
    """Get or create dispatcher instance with all routers configured.

    Dispatcher is stateless and can be cached/reused across requests.
    """
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


app = FastAPI()


@app.post("/webhook")
async def webhook_handler(request: Request) -> Response:
    """Handle incoming Telegram updates via webhook (serverless-compatible).

    Each request creates its own bot instance, processes the update,
    and cleans up. This allows the function to work in serverless environments.
    """
    # Verify secret token if configured
    if WEBHOOK_SECRET:
        secret_header = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
        if secret_header != WEBHOOK_SECRET:
            logger.warning("Invalid webhook secret token received")
            return Response(status_code=403)

    # Create bot instance for this request
    bot = create_bot()
    dp = get_dispatcher()

    try:
        # Parse and process the update
        update_data = await request.json()
        update = Update.model_validate(update_data, context={"bot": bot})

        await dp.feed_update(bot=bot, update=update)

        return Response(status_code=200)
    except Exception as e:
        logger.error(f"Error processing update: {e}")
        return Response(status_code=200)  # Return 200 to prevent Telegram retries
    finally:
        # Clean up bot session
        await bot.session.close()


@app.get("/health")
async def health_check():
    """Health check endpoint for Railway monitoring."""
    return {"status": "healthy", "bot": "running"}


@app.post("/setup-webhook")
async def setup_webhook():
    """One-time webhook setup endpoint.

    Call this once after deployment to register the webhook with Telegram.
    Example: curl -X POST https://your-domain.railway.app/setup-webhook
    """
    if not WEBHOOK_URL:
        return {"error": "WEBHOOK_URL environment variable not set"}

    bot = create_bot()
    dp = get_dispatcher()

    try:
        webhook_url = f"{WEBHOOK_URL}/webhook"
        logger.warning(f"Setting webhook to: {webhook_url}")

        await bot.delete_webhook(drop_pending_updates=True)
        await bot.set_webhook(
            url=webhook_url,
            secret_token=WEBHOOK_SECRET if WEBHOOK_SECRET else None,
            allowed_updates=dp.resolve_used_update_types(),
        )

        logger.warning("Webhook set successfully")
        return {"status": "success", "webhook_url": webhook_url}
    except Exception as e:
        logger.error(f"Failed to set webhook: {e}")
        return {"error": str(e)}
    finally:
        await bot.session.close()


@app.get("/webhook-info")
async def webhook_info():
    """Get current webhook information from Telegram."""
    bot = create_bot()

    try:
        info = await bot.get_webhook_info()
        return {
            "url": info.url,
            "has_custom_certificate": info.has_custom_certificate,
            "pending_update_count": info.pending_update_count,
            "last_error_date": info.last_error_date,
            "last_error_message": info.last_error_message,
            "max_connections": info.max_connections,
        }
    finally:
        await bot.session.close()


