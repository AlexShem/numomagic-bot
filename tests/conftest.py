import os

# Set default env vars for testing BEFORE any other imports
# This ensures the webhook module gets the test values on first import
os.environ.setdefault("BOT_TOKEN", "test_token")
os.environ.setdefault("PRO_CHANNEL_ID", "0")
os.environ.setdefault("LOG_PATH", "/tmp/test_logs/action.csv")
os.environ.setdefault("WEBHOOK_SECRET", "test_webhook_secret")

import pytest
from dotenv import load_dotenv
from middlewares.paywall import ChannelMembershipGate

load_dotenv()


PRO_CHANNEL_ID = int(os.getenv("PRO_CHANNEL_ID", default="0"))


@pytest.fixture
def middleware():
    """Create a middleware instance for testing."""
    return ChannelMembershipGate(channel_id=PRO_CHANNEL_ID)  # Example channel ID
