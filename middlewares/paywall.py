# middlewares/paywall.py
import time
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from typing import Callable, Awaitable, Any, Dict, Tuple
from logger.logger import get_logger

logger = get_logger(__name__)

# Cache expiry time: 1 day in seconds
CACHE_EXPIRY_SECONDS = 86400


class ChannelMembershipGate(BaseMiddleware):
    def __init__(self, channel_id: int):
        self.channel_id = channel_id
        # Cache structure: {user_id: (is_member: bool, expiry_timestamp: float)}
        self._cache: Dict[int, Tuple[bool, float]] = {}

    def _is_cached(self, user_id: int) -> bool:
        """Check if user_id is in cache and not expired."""
        if user_id not in self._cache:
            return False
        _, expiry_time = self._cache[user_id]
        return time.time() < expiry_time

    def _get_cached_membership(self, user_id: int) -> bool:
        """Get cached membership status. Assumes cache is valid (call _is_cached first)."""
        is_member, _ = self._cache[user_id]
        return is_member

    def _set_cached_membership(self, user_id: int, is_member: bool):
        """Cache membership status with expiry timestamp."""
        expiry_time = time.time() + CACHE_EXPIRY_SECONDS
        self._cache[user_id] = (is_member, expiry_time)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict], Awaitable[Any]],
        event: TelegramObject,
        data: dict,
    ) -> Any:
        user_id = None

        if isinstance(event, Message):
            user_id = event.from_user.id if event.from_user else None
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id if event.from_user else None

        # Let non-user events pass
        if not user_id:
            return await handler(event, data)

        # Check cache first
        is_member = None
        if self._is_cached(user_id):
            is_member = self._get_cached_membership(user_id)
            logger.debug(f"Using cached membership for user {user_id}: {is_member}")
        else:
            # Cache miss or expired - check via Telegram API
            try:
                logger.warning(
                    f"Checking membership for user {user_id} in channel {self.channel_id}"
                )
                member = await data["bot"].get_chat_member(self.channel_id, user_id)
                status = getattr(member, "status", "").lower()
                is_member = status in {"member", "administrator", "creator"}
                logger.warning(
                    f"User {user_id} membership status: {is_member} (status: {status})"
                )
                # Cache the result
                self._set_cached_membership(user_id, is_member)
            except Exception as e:
                # e.g., bot lacks rights or chat not found; treat as not a member
                logger.error(
                    f"Failed to check membership for user {user_id} in channel {self.channel_id}"
                )
                logger.error(f"Error checking membership: {e}")
                is_member = False
                # Cache the negative result to avoid repeated API calls
                self._set_cached_membership(user_id, False)

        # Only allow events to pass through if user is a confirmed member
        if is_member:
            return await handler(event, data)

        # Not a member - bot appears completely silent (no response)
        return None
