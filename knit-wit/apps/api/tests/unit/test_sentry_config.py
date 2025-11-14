"""
Unit tests for Sentry error tracking configuration.

Tests Sentry initialization, PII filtering, exception capture,
and breadcrumb handling.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any, Optional

from app.core.sentry_config import (
    init_sentry,
    before_send_handler,
    before_breadcrumb_handler,
    capture_exception,
    capture_message,
    add_breadcrumb,
    set_user_context,
    clear_user_context,
    _scrub_pii_from_request,
    _scrub_pii_from_dict,
)


class TestSentryInit:
    """Test Sentry initialization."""

    @patch("app.core.sentry_config.sentry_sdk")
    def test_init_sentry_with_valid_dsn(self, mock_sentry_sdk: Mock) -> None:
        """Test Sentry initializes with valid DSN."""
        dsn = "https://examplePublicKey@o0.ingest.sentry.io/0"
        environment = "production"
        sample_rate = 0.5

        init_sentry(
            dsn=dsn,
            environment=environment,
            traces_sample_rate=sample_rate,
            release="test@1.0.0",
        )

        # Verify sentry_sdk.init was called
        mock_sentry_sdk.init.assert_called_once()
        call_kwargs = mock_sentry_sdk.init.call_args.kwargs

        assert call_kwargs["dsn"] == dsn
        assert call_kwargs["environment"] == environment
        assert call_kwargs["traces_sample_rate"] == sample_rate
        assert call_kwargs["release"] == "test@1.0.0"
        assert call_kwargs["send_default_pii"] is False
        assert call_kwargs["attach_stacktrace"] is True

    @patch("app.core.sentry_config.sentry_sdk")
    @patch("app.core.sentry_config.logger")
    def test_init_sentry_without_dsn(
        self, mock_logger: Mock, mock_sentry_sdk: Mock
    ) -> None:
        """Test Sentry skips initialization when DSN is empty."""
        init_sentry(dsn="", environment="development")

        # Should log warning and not call init
        mock_logger.warning.assert_called_once()
        mock_sentry_sdk.init.assert_not_called()

    @patch("app.core.sentry_config.sentry_sdk")
    def test_init_sentry_development_debug_mode(self, mock_sentry_sdk: Mock) -> None:
        """Test Sentry enables debug mode in development."""
        init_sentry(
            dsn="https://test@sentry.io/0",
            environment="development",
        )

        call_kwargs = mock_sentry_sdk.init.call_args.kwargs
        assert call_kwargs["debug"] is True

    @patch("app.core.sentry_config.sentry_sdk")
    def test_init_sentry_production_no_debug(self, mock_sentry_sdk: Mock) -> None:
        """Test Sentry disables debug mode in production."""
        init_sentry(
            dsn="https://test@sentry.io/0",
            environment="production",
        )

        call_kwargs = mock_sentry_sdk.init.call_args.kwargs
        assert call_kwargs["debug"] is False


class TestBeforeSendHandler:
    """Test before_send event handler."""

    @patch("app.core.sentry_config.get_correlation_id")
    def test_adds_correlation_id_to_event(self, mock_get_corr_id: Mock) -> None:
        """Test correlation ID is added to event tags."""
        mock_get_corr_id.return_value = "req_abc123"

        event: Dict[str, Any] = {"event_id": "test123"}
        hint: Dict[str, Any] = {}

        result = before_send_handler(event, hint)

        assert result is not None
        assert "tags" in result
        assert result["tags"]["correlation_id"] == "req_abc123"

    def test_filters_client_errors(self) -> None:
        """Test 4xx client errors are filtered out."""
        # Mock HTTPException with 404 status
        mock_exc_type = type("HTTPException", (), {"__name__": "HTTPException"})
        mock_exc_instance = Mock()
        mock_exc_instance.status_code = 404

        event: Dict[str, Any] = {
            "event_id": "test123",
            "request": {"url": "/api/v1/patterns/123"},
        }
        hint: Dict[str, Any] = {
            "exc_info": (mock_exc_type, mock_exc_instance, None)
        }

        result = before_send_handler(event, hint)

        # Should return None to skip sending this event
        assert result is None

    def test_allows_server_errors(self) -> None:
        """Test 5xx server errors are allowed through."""
        mock_exc_type = type("HTTPException", (), {"__name__": "HTTPException"})
        mock_exc_instance = Mock()
        mock_exc_instance.status_code = 500

        event: Dict[str, Any] = {
            "event_id": "test123",
            "request": {"url": "/api/v1/patterns/generate"},
        }
        hint: Dict[str, Any] = {
            "exc_info": (mock_exc_type, mock_exc_instance, None)
        }

        result = before_send_handler(event, hint)

        # Should not filter out server errors
        assert result is not None

    def test_scrubs_pii_from_request(self) -> None:
        """Test PII is scrubbed from request data."""
        event: Dict[str, Any] = {
            "event_id": "test123",
            "request": {
                "url": "/api/v1/patterns/generate",
                "headers": {
                    "Authorization": "Bearer secret_token",
                    "Cookie": "session=abc123",
                    "Content-Type": "application/json",
                },
                "cookies": {"session": "abc123"},
            },
        }
        hint: Dict[str, Any] = {}

        result = before_send_handler(event, hint)

        assert result is not None
        assert result["request"]["headers"]["Authorization"] == "[Filtered]"
        assert result["request"]["headers"]["Cookie"] == "[Filtered]"
        assert result["request"]["headers"]["Content-Type"] == "application/json"
        assert result["request"]["cookies"] == "[Filtered]"

    def test_scrubs_pii_from_extra_data(self) -> None:
        """Test PII is scrubbed from extra context."""
        event: Dict[str, Any] = {
            "event_id": "test123",
            "extra": {
                "user_input": {"diameter": 10, "password": "secret123"},
                "api_key": "sk_test_abc123",
            },
        }
        hint: Dict[str, Any] = {}

        result = before_send_handler(event, hint)

        assert result is not None
        assert result["extra"]["user_input"]["diameter"] == 10
        assert result["extra"]["user_input"]["password"] == "[Filtered]"
        assert result["extra"]["api_key"] == "[Filtered]"


class TestBeforeBreadcrumbHandler:
    """Test before_breadcrumb handler."""

    def test_filters_health_check_breadcrumbs(self) -> None:
        """Test health check requests are filtered from breadcrumbs."""
        crumb: Dict[str, Any] = {
            "type": "http",
            "category": "httplib",
            "data": {"url": "http://localhost:8000/health", "method": "GET"},
        }
        hint: Dict[str, Any] = {}

        result = before_breadcrumb_handler(crumb, hint)

        # Should filter out health checks
        assert result is None

    def test_allows_non_health_breadcrumbs(self) -> None:
        """Test non-health-check breadcrumbs are allowed."""
        crumb: Dict[str, Any] = {
            "type": "http",
            "category": "httplib",
            "data": {"url": "http://localhost:8000/api/v1/patterns", "method": "POST"},
        }
        hint: Dict[str, Any] = {}

        result = before_breadcrumb_handler(crumb, hint)

        assert result is not None
        assert result["data"]["url"] == "http://localhost:8000/api/v1/patterns"

    def test_scrubs_pii_from_breadcrumb_data(self) -> None:
        """Test PII is scrubbed from breadcrumb data."""
        crumb: Dict[str, Any] = {
            "type": "http",
            "category": "httplib",
            "data": {
                "url": "http://localhost:8000/api/v1/patterns",
                "password": "secret123",
                "diameter": 10,
            },
        }
        hint: Dict[str, Any] = {}

        result = before_breadcrumb_handler(crumb, hint)

        assert result is not None
        assert result["data"]["password"] == "[Filtered]"
        assert result["data"]["diameter"] == 10


class TestPIIScrubbing:
    """Test PII scrubbing functions."""

    def test_scrub_pii_from_request_headers(self) -> None:
        """Test sensitive headers are scrubbed."""
        request_data: Dict[str, Any] = {
            "url": "/api/v1/patterns",
            "headers": {
                "authorization": "Bearer token123",
                "cookie": "session=abc",
                "x-api-key": "sk_live_xyz",
                "content-type": "application/json",
            },
        }

        result = _scrub_pii_from_request(request_data)

        assert result["headers"]["authorization"] == "[Filtered]"
        assert result["headers"]["cookie"] == "[Filtered]"
        assert result["headers"]["x-api-key"] == "[Filtered]"
        assert result["headers"]["content-type"] == "application/json"

    def test_scrub_pii_from_request_cookies(self) -> None:
        """Test cookies are scrubbed."""
        request_data: Dict[str, Any] = {
            "url": "/api/v1/patterns",
            "cookies": {"session": "abc123", "user_id": "user_xyz"},
        }

        result = _scrub_pii_from_request(request_data)

        assert result["cookies"] == "[Filtered]"

    def test_scrub_pii_from_dict_sensitive_keys(self) -> None:
        """Test sensitive keys are scrubbed from dictionary."""
        data: Dict[str, Any] = {
            "diameter": 10,
            "password": "secret123",
            "api_key": "sk_test_abc",
            "secret": "hidden",
            "token": "auth_token",
            "user_email": "test@example.com",  # Not sensitive by default
        }

        result = _scrub_pii_from_dict(data)

        assert result["diameter"] == 10
        assert result["password"] == "[Filtered]"
        assert result["api_key"] == "[Filtered]"
        assert result["secret"] == "[Filtered]"
        assert result["token"] == "[Filtered]"
        assert result["user_email"] == "test@example.com"

    def test_scrub_pii_from_nested_dict(self) -> None:
        """Test PII scrubbing works recursively on nested dicts."""
        data: Dict[str, Any] = {
            "shape": "sphere",
            "user_data": {
                "preferences": {"color": "blue"},
                "auth": {"password": "secret", "username": "user123"},
            },
        }

        result = _scrub_pii_from_dict(data)

        assert result["shape"] == "sphere"
        assert result["user_data"]["preferences"]["color"] == "blue"
        assert result["user_data"]["auth"]["password"] == "[Filtered]"
        assert result["user_data"]["auth"]["username"] == "user123"

    def test_scrub_pii_from_list_of_dicts(self) -> None:
        """Test PII scrubbing works on lists containing dicts."""
        data: Dict[str, Any] = {
            "patterns": [
                {"id": "pat_1", "api_key": "sk_1"},
                {"id": "pat_2", "api_key": "sk_2"},
            ]
        }

        result = _scrub_pii_from_dict(data)

        assert result["patterns"][0]["id"] == "pat_1"
        assert result["patterns"][0]["api_key"] == "[Filtered]"
        assert result["patterns"][1]["id"] == "pat_2"
        assert result["patterns"][1]["api_key"] == "[Filtered]"

    def test_scrub_pii_case_insensitive(self) -> None:
        """Test PII scrubbing is case-insensitive."""
        data: Dict[str, Any] = {
            "Password": "secret",
            "API_KEY": "key123",
            "Token": "token123",
        }

        result = _scrub_pii_from_dict(data)

        assert result["Password"] == "[Filtered]"
        assert result["API_KEY"] == "[Filtered]"
        assert result["Token"] == "[Filtered]"


class TestCaptureException:
    """Test manual exception capture."""

    @patch("app.core.sentry_config.sentry_sdk")
    @patch("app.core.sentry_config.get_correlation_id")
    def test_capture_exception_with_context(
        self, mock_get_corr_id: Mock, mock_sentry_sdk: Mock
    ) -> None:
        """Test exception capture with additional context."""
        mock_get_corr_id.return_value = "req_xyz789"
        mock_scope = MagicMock()
        mock_sentry_sdk.push_scope.return_value.__enter__.return_value = mock_scope
        mock_sentry_sdk.capture_exception.return_value = "event_abc123"

        error = ValueError("Invalid input")
        context = {"shape": "sphere", "diameter": -10}
        tags = {"component": "pattern_generator"}

        event_id = capture_exception(
            error,
            context=context,
            level="error",
            tags=tags,
        )

        # Verify scope configuration
        mock_scope.set_tag.assert_any_call("correlation_id", "req_xyz789")
        mock_scope.set_tag.assert_any_call("component", "pattern_generator")
        mock_scope.set_extra.assert_any_call("shape", "sphere")
        mock_scope.set_extra.assert_any_call("diameter", -10)

        # Verify exception was captured
        mock_sentry_sdk.capture_exception.assert_called_once_with(error)
        assert event_id == "event_abc123"

    @patch("app.core.sentry_config.sentry_sdk")
    def test_capture_exception_scrubs_pii_from_context(
        self, mock_sentry_sdk: Mock
    ) -> None:
        """Test PII is scrubbed from exception context."""
        mock_scope = MagicMock()
        mock_sentry_sdk.push_scope.return_value.__enter__.return_value = mock_scope

        error = ValueError("Auth failed")
        context = {"username": "user123", "password": "secret123"}

        capture_exception(error, context=context)

        # Verify password was filtered
        calls = mock_scope.set_extra.call_args_list
        extra_dict = {call[0][0]: call[0][1] for call in calls}

        assert extra_dict["username"] == "user123"
        assert extra_dict["password"] == "[Filtered]"


class TestCaptureMessage:
    """Test manual message capture."""

    @patch("app.core.sentry_config.sentry_sdk")
    @patch("app.core.sentry_config.get_correlation_id")
    def test_capture_message_with_context(
        self, mock_get_corr_id: Mock, mock_sentry_sdk: Mock
    ) -> None:
        """Test message capture with context and tags."""
        mock_get_corr_id.return_value = "req_message123"
        mock_scope = MagicMock()
        mock_sentry_sdk.push_scope.return_value.__enter__.return_value = mock_scope
        mock_sentry_sdk.capture_message.return_value = "msg_event_123"

        message = "Pattern generation took longer than expected"
        context = {"duration_ms": 5000, "shape": "cylinder"}
        tags = {"performance": "slow"}

        event_id = capture_message(
            message,
            level="warning",
            context=context,
            tags=tags,
        )

        # Verify scope configuration
        mock_scope.set_tag.assert_any_call("correlation_id", "req_message123")
        mock_scope.set_tag.assert_any_call("performance", "slow")
        mock_scope.set_extra.assert_any_call("duration_ms", 5000)
        mock_scope.set_extra.assert_any_call("shape", "cylinder")

        # Verify message was captured
        mock_sentry_sdk.capture_message.assert_called_once_with(
            message, level="warning"
        )
        assert event_id == "msg_event_123"


class TestAddBreadcrumb:
    """Test breadcrumb addition."""

    @patch("app.core.sentry_config.sentry_sdk")
    def test_add_breadcrumb_with_data(self, mock_sentry_sdk: Mock) -> None:
        """Test breadcrumb is added with data."""
        message = "Pattern compilation started"
        category = "pattern_engine"
        data = {"shape": "sphere", "diameter": 10}

        add_breadcrumb(
            message=message,
            category=category,
            level="info",
            data=data,
        )

        mock_sentry_sdk.add_breadcrumb.assert_called_once_with(
            category=category,
            message=message,
            level="info",
            data=data,
        )

    @patch("app.core.sentry_config.sentry_sdk")
    def test_add_breadcrumb_scrubs_pii(self, mock_sentry_sdk: Mock) -> None:
        """Test breadcrumb scrubs PII from data."""
        data = {"username": "user123", "password": "secret"}

        add_breadcrumb(
            message="Auth attempt",
            category="auth",
            data=data,
        )

        call_kwargs = mock_sentry_sdk.add_breadcrumb.call_args.kwargs
        assert call_kwargs["data"]["username"] == "user123"
        assert call_kwargs["data"]["password"] == "[Filtered]"


class TestUserContext:
    """Test user context management."""

    @patch("app.core.sentry_config.sentry_sdk")
    def test_set_user_context(self, mock_sentry_sdk: Mock) -> None:
        """Test user context is set."""
        set_user_context(user_id="user_abc123", subscription="premium")

        mock_sentry_sdk.set_user.assert_called_once_with({
            "id": "user_abc123",
            "subscription": "premium",
        })

    @patch("app.core.sentry_config.sentry_sdk")
    def test_clear_user_context(self, mock_sentry_sdk: Mock) -> None:
        """Test user context is cleared."""
        clear_user_context()

        mock_sentry_sdk.set_user.assert_called_once_with(None)
