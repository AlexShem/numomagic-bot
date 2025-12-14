import time
from middlewares.paywall import ChannelMembershipGate


class TestChannelMembershipCache:
    def test_cache_empty_initially(self, middleware: ChannelMembershipGate):
        """Test that cache is empty on initialization."""
        assert not middleware._cache

    def test_set_and_get_cached_membership(self, middleware: ChannelMembershipGate):
        """Test setting and retrieving cached membership."""
        user_id = 123
        middleware._set_cached_membership(user_id=user_id, is_member=True)

        assert middleware._is_cached(user_id)
        assert middleware._get_cached_membership(user_id) is True

    def test_cache_stores_false_membership(self, middleware: ChannelMembershipGate):
        """Test caching non-member status."""
        user_id = 456
        middleware._set_cached_membership(user_id=user_id, is_member=False)

        assert middleware._is_cached(user_id)
        assert middleware._get_cached_membership(user_id) is False

    def test_cache_with_zero_expiry_uses_default(self, middleware: ChannelMembershipGate):
        """Test that zero or negative expiry uses default expiry time (one day)."""
        user_id = 111
        middleware._set_cached_membership(user_id=user_id, is_member=True, expiry_seconds=0)

        # Should still be cached immediately after setting
        assert middleware._is_cached(user_id)

    def test_cache_not_expired(self, middleware: ChannelMembershipGate):
        """Test that cache is valid before expiry."""
        user_id = 789
        middleware._set_cached_membership(user_id=user_id, is_member=True)

        # Should still be cached immediately after setting
        assert middleware._is_cached(user_id)

    def test_cache_expiry(self, middleware: ChannelMembershipGate):
        """Test that cache expires after specified time."""
        user_id = 999

        # Set cache with a short expiry time for testing
        expiry_seconds = 0.1  # 1 second for quick expiry
        middleware._set_cached_membership(user_id=user_id, is_member=True, expiry_seconds=expiry_seconds)

        # Initially, it should be cached
        assert middleware._is_cached(user_id)

        # Wait for expiry
        time.sleep(expiry_seconds + 0.1)

        # Now it should be expired
        assert not middleware._is_cached(user_id)

    def test_multiple_users_cached(self, middleware: ChannelMembershipGate):
        """Test caching multiple users independently."""
        middleware._set_cached_membership(user_id=1, is_member=True)
        middleware._set_cached_membership(user_id=2, is_member=False)
        middleware._set_cached_membership(user_id=3, is_member=True)

        assert middleware._is_cached(1)
        assert middleware._get_cached_membership(1) is True
        assert middleware._is_cached(2)
        assert middleware._get_cached_membership(2) is False
        assert middleware._is_cached(3)
        assert middleware._get_cached_membership(3) is True
