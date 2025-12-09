import os

import pytest
from dotenv import load_dotenv
from middlewares.paywall import ChannelMembershipGate

load_dotenv()

PRO_CHANNEL_ID = int(os.getenv("PRO_CHANNEL_ID"), 0)


@pytest.fixture
def middleware():
    """Create a middleware instance for testing."""
    return ChannelMembershipGate(channel_id=PRO_CHANNEL_ID)  # Example channel ID
