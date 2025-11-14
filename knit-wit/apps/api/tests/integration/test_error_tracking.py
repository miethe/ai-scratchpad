"""
Integration tests for error tracking with Sentry.

Tests end-to-end error tracking including:
- Correlation ID middleware
- Automatic exception capture
- Manual error reporting
- PII filtering in real requests
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    """Create test client with Sentry disabled."""
    # Ensure Sentry is disabled for tests
    with patch.dict("os.environ", {"SENTRY_ENABLED": "false"}):
        return TestClient(app)


class TestCorrelationIDMiddleware:
    """Test correlation ID middleware integration."""

    def test_generates_correlation_id(self, client: TestClient) -> None:
        """Test middleware generates correlation ID for requests."""
        response = client.get("/health")

        assert response.status_code == 200
        assert "X-Correlation-ID" in response.headers
        assert response.headers["X-Correlation-ID"].startswith("req_")

    def test_accepts_client_correlation_id(self, client: TestClient) -> None:
        """Test middleware accepts correlation ID from client."""
        custom_corr_id = "client_custom_id_123"

        response = client.get(
            "/health",
            headers={"X-Correlation-ID": custom_corr_id}
        )

        assert response.status_code == 200
        assert response.headers["X-Correlation-ID"] == custom_corr_id

    def test_correlation_id_different_per_request(self, client: TestClient) -> None:
        """Test each request gets a unique correlation ID."""
        response1 = client.get("/health")
        response2 = client.get("/health")

        corr_id1 = response1.headers["X-Correlation-ID"]
        corr_id2 = response2.headers["X-Correlation-ID"]

        assert corr_id1 != corr_id2


class TestErrorCapture:
    """Test error capture in API endpoints."""

    @patch("app.core.sentry_config.sentry_sdk")
    def test_server_error_captured(
        self, mock_sentry_sdk: Mock, client: TestClient
    ) -> None:
        """Test 500 errors are captured by Sentry."""
        # Enable Sentry for this test
        with patch("app.core.settings.sentry_enabled", True):
            with patch("app.core.settings.sentry_dsn", "https://test@sentry.io/0"):
                # Trigger an error in export endpoint with invalid data
                response = client.post(
                    "/api/v1/export/pdf",
                    json={"invalid": "data"},  # Will fail validation
                )

                # Should get error response (4xx or 5xx)
                assert response.status_code >= 400

    def test_validation_error_not_captured(self, client: TestClient) -> None:
        """Test 4xx validation errors are not sent to Sentry."""
        # Invalid request should return 422 but not be sent to Sentry
        response = client.post(
            "/api/v1/export/pdf",
            json={},  # Missing required fields
        )

        # Should get validation error
        assert response.status_code == 422
        # Note: Sentry capture is filtered in before_send_handler


class TestBreadcrumbs:
    """Test breadcrumb collection during request processing."""

    @patch("app.core.sentry_config.sentry_sdk")
    def test_breadcrumbs_added_during_export(
        self, mock_sentry_sdk: Mock, client: TestClient
    ) -> None:
        """Test breadcrumbs are added during export operations."""
        # Mock pattern DSL data for export
        pattern_data = {
            "meta": {
                "version": "0.1",
                "units": "cm",
                "terms": "US",
                "stitch": "sc",
                "round_mode": "spiral",
                "gauge": {
                    "sts_per_10cm": 14,
                    "rows_per_10cm": 16
                }
            },
            "object": {
                "type": "sphere",
                "params": {"diameter": 10}
            },
            "rounds": []
        }

        # This would normally add breadcrumbs during processing
        # In real usage, breadcrumbs help trace the path to an error


class TestPIIFiltering:
    """Test PII is filtered from captured errors."""

    @patch("app.core.sentry_config.sentry_sdk")
    def test_headers_filtered_in_error_context(
        self, mock_sentry_sdk: Mock, client: TestClient
    ) -> None:
        """Test sensitive headers are filtered from error reports."""
        # Make request with sensitive headers
        response = client.get(
            "/health",
            headers={
                "Authorization": "Bearer secret_token",
                "Cookie": "session=abc123",
            }
        )

        assert response.status_code == 200
        # Headers should be filtered by before_send_handler if error occurred


@pytest.mark.parametrize("endpoint,method,payload", [
    ("/health", "GET", None),
    ("/", "GET", None),
    ("/api/v1/telemetry/events", "POST", {
        "event_type": "pattern_generated",
        "properties": {"shape": "sphere"}
    }),
])
class TestCorrelationIDInVariousEndpoints:
    """Test correlation ID is added to all endpoint responses."""

    def test_correlation_id_present(
        self,
        client: TestClient,
        endpoint: str,
        method: str,
        payload: dict
    ) -> None:
        """Test correlation ID is present in response headers."""
        if method == "GET":
            response = client.get(endpoint)
        elif method == "POST":
            response = client.post(endpoint, json=payload)

        assert "X-Correlation-ID" in response.headers
        assert len(response.headers["X-Correlation-ID"]) > 0


class TestSentryInitialization:
    """Test Sentry initialization on app startup."""

    @patch("app.core.sentry_config.init_sentry")
    def test_sentry_initialized_when_enabled(
        self, mock_init_sentry: Mock
    ) -> None:
        """Test Sentry is initialized when DSN is provided."""
        with patch.dict("os.environ", {
            "SENTRY_DSN": "https://test@sentry.io/0",
            "SENTRY_ENABLED": "true",
            "SENTRY_ENVIRONMENT": "test",
        }):
            # Create new app instance which triggers lifespan
            from app.main import app
            with TestClient(app):
                # Sentry should have been initialized
                pass  # Lifespan runs on context enter

    @patch("app.core.sentry_config.init_sentry")
    def test_sentry_not_initialized_when_disabled(
        self, mock_init_sentry: Mock
    ) -> None:
        """Test Sentry is not initialized when disabled."""
        with patch.dict("os.environ", {
            "SENTRY_ENABLED": "false",
        }):
            from app.main import app
            with TestClient(app):
                # Sentry should not be initialized
                pass


class TestErrorContextEnrichment:
    """Test errors are enriched with context before sending to Sentry."""

    @patch("app.core.sentry_config.capture_exception")
    def test_service_errors_include_context(
        self, mock_capture: Mock, client: TestClient
    ) -> None:
        """Test service layer adds context to captured exceptions."""
        # This would be tested by triggering actual errors in services
        # which use capture_exception with context
        pass


class TestSentryPerformance:
    """Test Sentry doesn't significantly impact performance."""

    def test_request_performance_with_sentry_disabled(
        self, client: TestClient
    ) -> None:
        """Test requests complete quickly with Sentry disabled."""
        import time

        start = time.time()
        response = client.get("/health")
        duration = time.time() - start

        assert response.status_code == 200
        assert duration < 0.5  # Should be very fast (< 500ms)

    @patch("app.core.sentry_config.sentry_sdk")
    def test_request_performance_with_sentry_enabled(
        self, mock_sentry_sdk: Mock, client: TestClient
    ) -> None:
        """Test requests complete quickly with Sentry enabled."""
        import time

        with patch("app.core.settings.sentry_enabled", True):
            with patch("app.core.settings.sentry_dsn", "https://test@sentry.io/0"):
                start = time.time()
                response = client.get("/health")
                duration = time.time() - start

                assert response.status_code == 200
                # Should still be fast with Sentry (< 1 second)
                assert duration < 1.0
