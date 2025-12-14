import asyncio
import os

from dotenv import load_dotenv

from logger.logger import get_logger
from webhook.webhook import get_bot, get_dispatcher, app

load_dotenv()

USE_WEBHOOK = os.getenv("USE_WEBHOOK", "false").lower() == "true"
logger = get_logger(__name__)


async def run_polling():
    """Run bot in polling mode (for local development)."""
    logger.warning("Bot is starting in POLLING mode")
    bot = get_bot()
    dp = get_dispatcher()

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
            polling_timeout=30,
            handle_signals=True,
        )
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        logger.warning("Bot is stopping")
        await bot.session.close()


def main():
    """Main entry point - runs polling or webhook based on USE_WEBHOOK env var."""
    if USE_WEBHOOK:
        import uvicorn
        logger.warning("Bot is starting in WEBHOOK mode")
        port = int(os.getenv("PORT", 8080))
        uvicorn.run(app, host="0.0.0.0", port=port)
    else:
        asyncio.run(run_polling())


if __name__ == "__main__":
    main()
