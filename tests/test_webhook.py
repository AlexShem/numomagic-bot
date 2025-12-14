"""Tests for webhook handler functionality."""

import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

# Set required env vars before importing webhook module
os.environ.setdefault("BOT_TOKEN", "test_token")
os.environ.setdefault("PRO_CHANNEL_ID", "0")


class TestWebhookHandler:
    """Tests for the /webhook endpoint."""

    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app."""
        # Import here to ensure env vars are set
        from webhook.webhook import app
        return TestClient(app)

    @pytest.fixture
    def valid_update(self):
        """Create a valid Telegram update payload."""
        return {
            "update_id": 123456789,
            "message": {
                "message_id": 1,
                "date": 1234567890,
                "chat": {"id": 12345, "type": "private"},
                "from": {"id": 12345, "is_bot": False, "first_name": "Test"},
                "text": "/start",
            },
        }

    def test_webhook_without_secret_succeeds(self, client, valid_update):
        """Test that webhook accepts requests when no secret is configured."""
        with patch("webhook.webhook.WEBHOOK_SECRET", ""):
            with patch("webhook.webhook.get_dispatcher") as mock_dp:
                with patch("webhook.webhook.create_bot") as mock_bot:
                    # Setup mocks
                    mock_bot_instance = AsyncMock()
                    mock_bot.return_value = mock_bot_instance
                    mock_dp_instance = MagicMock()
                    mock_dp_instance.feed_update = AsyncMock()
                    mock_dp.return_value = mock_dp_instance

                    response = client.post("/webhook", json=valid_update)

                    assert response.status_code == 200

    def test_webhook_with_valid_secret_succeeds(self, client, valid_update):
        """Test that webhook accepts requests with valid secret token."""
        with patch("webhook.webhook.WEBHOOK_SECRET", "test_secret"):
            with patch("webhook.webhook.get_dispatcher") as mock_dp:
                with patch("webhook.webhook.create_bot") as mock_bot:
                    # Setup mocks
                    mock_bot_instance = AsyncMock()
                    mock_bot.return_value = mock_bot_instance
                    mock_dp_instance = MagicMock()
                    mock_dp_instance.feed_update = AsyncMock()
                    mock_dp.return_value = mock_dp_instance

                    response = client.post(
                        "/webhook",
                        json=valid_update,
                        headers={"X-Telegram-Bot-Api-Secret-Token": "test_secret"},
                    )

                    assert response.status_code == 200

    def test_webhook_with_invalid_secret_returns_403(self, client, valid_update):
        """Test that webhook rejects requests with invalid secret token."""
        with patch("webhook.webhook.WEBHOOK_SECRET", "test_secret"):
            response = client.post(
                "/webhook",
                json=valid_update,
                headers={"X-Telegram-Bot-Api-Secret-Token": "wrong_secret"},
            )

            assert response.status_code == 403

    def test_webhook_missing_secret_when_required_returns_403(self, client, valid_update):
        """Test that webhook rejects requests without secret when one is configured."""
        with patch("webhook.webhook.WEBHOOK_SECRET", "test_secret"):
            response = client.post("/webhook", json=valid_update)

            assert response.status_code == 403

    def test_webhook_handles_processing_error_gracefully(self, client, valid_update):
        """Test that webhook returns 200 even on processing errors to prevent Telegram retries."""
        with patch("webhook.webhook.WEBHOOK_SECRET", ""):
            with patch("webhook.webhook.get_dispatcher") as mock_dp:
                with patch("webhook.webhook.create_bot") as mock_bot:
                    # Setup mocks to raise an exception
                    mock_bot_instance = AsyncMock()
                    mock_bot.return_value = mock_bot_instance
                    mock_dp_instance = MagicMock()
                    mock_dp_instance.feed_update = AsyncMock(
                        side_effect=Exception("Test error")
                    )
                    mock_dp.return_value = mock_dp_instance

                    response = client.post("/webhook", json=valid_update)

                    # Should return 200 to prevent Telegram from retrying
                    assert response.status_code == 200


class TestHealthCheck:
    """Tests for the /health endpoint."""

    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app."""
        from webhook.webhook import app
        return TestClient(app)

    def test_health_check_returns_healthy(self, client):
        """Test that health check returns healthy status."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "dispatcher_cached" in data


class TestSetupWebhook:
    """Tests for the /setup-webhook endpoint."""

    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app."""
        from webhook.webhook import app
        return TestClient(app)

    def test_setup_webhook_without_auth_returns_401(self, client):
        """Test that setup-webhook requires authentication."""
        with patch("webhook.webhook.WEBHOOK_SECRET", "test_secret"):
            response = client.post("/setup-webhook")

            assert response.status_code == 401

    def test_setup_webhook_with_wrong_auth_returns_401(self, client):
        """Test that setup-webhook rejects wrong credentials."""
        with patch("webhook.webhook.WEBHOOK_SECRET", "test_secret"):
            response = client.post(
                "/setup-webhook",
                headers={"Authorization": "Bearer wrong_secret"},
            )

            assert response.status_code == 401

    def test_setup_webhook_with_valid_auth_succeeds(self, client):
        """Test that setup-webhook works with valid authentication."""
        with patch("webhook.webhook.WEBHOOK_SECRET", "test_secret"):
            with patch("webhook.webhook.WEBHOOK_URL", "https://example.com"):
                with patch("webhook.webhook.create_bot") as mock_bot:
                    with patch("webhook.webhook.get_dispatcher") as mock_dp:
                        # Setup mocks
                        mock_bot_instance = AsyncMock()
                        mock_bot_instance.delete_webhook = AsyncMock()
                        mock_bot_instance.set_webhook = AsyncMock()
                        mock_bot.return_value = mock_bot_instance
                        mock_dp_instance = MagicMock()
                        mock_dp_instance.resolve_used_update_types = MagicMock(
                            return_value=[]
                        )
                        mock_dp.return_value = mock_dp_instance

                        response = client.post(
                            "/setup-webhook",
                            headers={"Authorization": "Bearer test_secret"},
                        )

                        assert response.status_code == 200
                        data = response.json()
                        assert data["status"] == "success"


class TestWebhookInfo:
    """Tests for the /webhook-info endpoint."""

    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app."""
        from webhook.webhook import app
        return TestClient(app)

    def test_webhook_info_without_auth_returns_401(self, client):
        """Test that webhook-info requires authentication."""
        with patch("webhook.webhook.WEBHOOK_SECRET", "test_secret"):
            response = client.get("/webhook-info")

            assert response.status_code == 401

    def test_webhook_info_with_valid_auth_succeeds(self, client):
        """Test that webhook-info works with valid authentication."""
        with patch("webhook.webhook.WEBHOOK_SECRET", "test_secret"):
            with patch("webhook.webhook.create_bot") as mock_bot:
                # Setup mock webhook info
                mock_info = MagicMock()
                mock_info.url = "https://example.com/webhook"
                mock_info.has_custom_certificate = False
                mock_info.pending_update_count = 0
                mock_info.last_error_date = None
                mock_info.last_error_message = None
                mock_info.max_connections = 40

                mock_bot_instance = AsyncMock()
                mock_bot_instance.get_webhook_info = AsyncMock(return_value=mock_info)
                mock_bot.return_value = mock_bot_instance

                response = client.get(
                    "/webhook-info",
                    headers={"Authorization": "Bearer test_secret"},
                )

                assert response.status_code == 200
                data = response.json()
                assert data["url"] == "https://example.com/webhook"

