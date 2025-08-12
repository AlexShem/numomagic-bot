# middlewares/paywall.py
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from typing import Callable, Awaitable, Any
from logger.logger import get_logger

ALLOWED = {"/start", "/help", "/subscribe", "/pricing"}  # free routes

logger = get_logger(__name__)


class ChannelMembershipGate(BaseMiddleware):
    def __init__(self, channel_id: int):
        self.channel_id = channel_id

    async def __call__(self,
                       handler: Callable[[TelegramObject, dict], Awaitable[Any]],
                       event: TelegramObject,
                       data: dict) -> Any:
        user_id, text = None, None

        if isinstance(event, Message):
            user_id = event.from_user.id if event.from_user else None
            text = (event.text or "").split()[0].lower() if event.text else None
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id if event.from_user else None

        # Let non-user events or whitelisted commands pass
        if not user_id or (text in ALLOWED):
            return await handler(event, data)

        # Membership check
        try:
            logger.warning(f"Checking membership for user {user_id} in channel {self.channel_id}")
            member = await data["bot"].get_chat_member(self.channel_id, user_id)
            logger.warning(f"User {user_id} is in channel {self.channel_id}")
            status = getattr(member, "status", "").lower()
            logger.warning(f"User {user_id} status in channel {self.channel_id}: {status}")
            if status in {"member", "administrator", "creator"}:
                return await handler(event, data)
        except Exception as e:
            # e.g., bot lacks rights or chat not found; treat as not a member
            logger.error(f"Failed to check membership for user {user_id} in channel {self.channel_id}")
            logger.error(f"Error checking membership: {e}")
            pass

        # Not a member -> push to /subscribe
        if isinstance(event, Message):
            await event.answer("🔒 Access requires subscription. Use /subscribe to join via Stars.")
        elif isinstance(event, CallbackQuery):
            await event.message.answer("🔒 Access requires subscription. Use /subscribe to join via Stars.")
        return None
