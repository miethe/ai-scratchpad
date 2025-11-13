"""
Integration tests for Telemetry API endpoint

Tests POST /api/v1/telemetry/events with privacy validation.
"""

import pytest
import json
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def mock_logger():
    """Mock logger to capture telemetry output."""
    with patch("app.services.telemetry_service.logger") as mock:
        yield mock


class TestTelemetryEndpoint:
    """Test telemetry API endpoint."""

    def test_track_pattern_generated_event(self, client, mock_logger):
        """Test tracking a pattern_generated event."""
        response = client.post(
            "/api/v1/telemetry/events",
            json={
                "event": "pattern_generated",
                "properties": {
                    "shape_type": "sphere",
                    "stitch_type": "sc",
                    "terms": "US",
                },
            },
        )

        # Should return 204 No Content
        assert response.status_code == 204
        assert response.content == b""

        # Should have logged the event
        assert mock_logger.info.called
        log_call = mock_logger.info.call_args[0][0]
        log_data = json.loads(log_call)

        assert log_data["event"] == "pattern_generated"
        assert log_data["properties"]["shape_type"] == "sphere"

    def test_track_pattern_visualized_event(self, client, mock_logger):
        """Test tracking a pattern_visualized event."""
        response = client.post(
            "/api/v1/telemetry/events",
            json={
                "event": "pattern_visualized",
                "properties": {
                    "shape_type": "cylinder",
                    "highlight_changes": True,
                    "terms": "UK",
                },
            },
        )

        assert response.status_code == 204

        log_call = mock_logger.info.call_args[0][0]
        log_data = json.loads(log_call)

        assert log_data["event"] == "pattern_visualized"
        assert log_data["properties"]["shape_type"] == "cylinder"

    def test_track_pattern_exported_event(self, client, mock_logger):
        """Test tracking a pattern_exported event."""
        response = client.post(
            "/api/v1/telemetry/events",
            json={
                "event": "pattern_exported",
                "properties": {
                    "export_format": "pdf",
                    "include_diagram": True,
                    "paper_size": "A4",
                },
            },
        )

        assert response.status_code == 204

        log_call = mock_logger.info.call_args[0][0]
        log_data = json.loads(log_call)

        assert log_data["event"] == "pattern_exported"
        assert log_data["properties"]["export_format"] == "pdf"

    def test_track_event_without_properties(self, client, mock_logger):
        """Test tracking event without properties."""
        response = client.post(
            "/api/v1/telemetry/events",
            json={"event": "pattern_generated"},
        )

        assert response.status_code == 204

        log_call = mock_logger.info.call_args[0][0]
        log_data = json.loads(log_call)

        assert log_data["properties"] == {}


class TestInvalidEvents:
    """Test error handling for invalid events."""

    def test_invalid_event_type(self, client):
        """Test invalid event type returns 400."""
        response = client.post(
            "/api/v1/telemetry/events",
            json={
                "event": "invalid_event",
                "properties": {},
            },
        )

        assert response.status_code == 400
        detail = response.json()["detail"]
        assert "Invalid event type" in detail
        assert "invalid_event" in detail

    def test_invalid_event_suggests_alternatives(self, client):
        """Test error message suggests valid events."""
        response = client.post(
            "/api/v1/telemetry/events",
            json={"event": "user_clicked"},
        )

        assert response.status_code == 400
        detail = response.json()["detail"]
        assert "Supported:" in detail
        assert "pattern_generated" in detail

    def test_missing_event_field(self, client):
        """Test missing event field returns 422."""
        response = client.post(
            "/api/v1/telemetry/events",
            json={"properties": {}},
        )

        assert response.status_code == 422

    def test_invalid_json(self, client):
        """Test invalid JSON returns 422."""
        response = client.post(
            "/api/v1/telemetry/events",
            data="not json",
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 422


class TestPIIScrubbing:
    """Test that PII is scrubbed at API level."""

    def test_scrub_pii_fields(self, client, mock_logger):
        """Test that PII fields are removed before logging."""
        response = client.post(
            "/api/v1/telemetry/events",
            json={
                "event": "pattern_generated",
                "properties": {
                    "shape_type": "sphere",
                    "user_id": "user123",  # Should be removed
                    "diameter": 10,  # Should be removed
                },
            },
        )

        # Should succeed (silent scrubbing)
        assert response.status_code == 204

        # Check logged data
        log_call = mock_logger.info.call_args[0][0]
        log_data = json.loads(log_call)

        # Safe field should be present
        assert log_data["properties"]["shape_type"] == "sphere"

        # PII should be absent
        assert "user_id" not in log_data["properties"]
        assert "diameter" not in log_data["properties"]

    def test_scrub_pattern_content(self, client, mock_logger):
        """Test that pattern content is never logged."""
        response = client.post(
            "/api/v1/telemetry/events",
            json={
                "event": "pattern_generated",
                "properties": {
                    "shape_type": "cylinder",
                    "pattern_content": "R1: MR 6 sc (6)",  # Should be removed
                    "pattern_text": "Some pattern",  # Should be removed
                },
            },
        )

        assert response.status_code == 204

        log_call = mock_logger.info.call_args[0][0]
        log_data = json.loads(log_call)

        # NO pattern content should be logged
        assert "pattern_content" not in log_data["properties"]
        assert "pattern_text" not in log_data["properties"]

    def test_scrub_user_identifiers(self, client, mock_logger):
        """Test that user identifiers are never logged."""
        response = client.post(
            "/api/v1/telemetry/events",
            json={
                "event": "pattern_visualized",
                "properties": {
                    "shape_type": "sphere",
                    "user_id": "user123",
                    "email": "test@example.com",
                    "session_id": "session456",
                },
            },
        )

        assert response.status_code == 204

        log_call = mock_logger.info.call_args[0][0]
        log_data = json.loads(log_call)

        # NO user identifiers
        assert "user_id" not in log_data["properties"]
        assert "email" not in log_data["properties"]
        assert "session_id" not in log_data["properties"]


class TestSilentFailures:
    """Test that telemetry never blocks user experience."""

    def test_logging_failure_returns_204(self, client, mock_logger):
        """Test that logging failures still return 204."""
        # Make logger.info raise an exception
        mock_logger.info.side_effect = Exception("Logging failed")

        response = client.post(
            "/api/v1/telemetry/events",
            json={
                "event": "pattern_generated",
                "properties": {"shape_type": "sphere"},
            },
        )

        # Should still return 204 (silent failure)
        assert response.status_code == 204

    def test_internal_error_returns_204(self, client):
        """Test that internal errors return 204 (silent failure)."""
        with patch(
            "app.services.telemetry_service.telemetry_service.track_event"
        ) as mock_track:
            # Make track_event raise unexpected exception
            mock_track.side_effect = RuntimeError("Unexpected error")

            response = client.post(
                "/api/v1/telemetry/events",
                json={
                    "event": "pattern_generated",
                    "properties": {"shape_type": "sphere"},
                },
            )

            # Should return 204 (silent failure)
            assert response.status_code == 204


class TestWhitelistEnforcement:
    """Test that only whitelisted properties are logged."""

    def test_pattern_generated_whitelist(self, client, mock_logger):
        """Test pattern_generated only logs whitelisted properties."""
        response = client.post(
            "/api/v1/telemetry/events",
            json={
                "event": "pattern_generated",
                "properties": {
                    "shape_type": "sphere",  # Whitelisted
                    "stitch_type": "sc",  # Whitelisted
                    "terms": "US",  # Whitelisted
                    "custom_field": "value",  # NOT whitelisted
                },
            },
        )

        assert response.status_code == 204

        log_call = mock_logger.info.call_args[0][0]
        log_data = json.loads(log_call)

        # Whitelisted fields should be present
        assert log_data["properties"]["shape_type"] == "sphere"
        assert log_data["properties"]["stitch_type"] == "sc"
        assert log_data["properties"]["terms"] == "US"

        # Non-whitelisted field should be absent
        assert "custom_field" not in log_data["properties"]

    def test_pattern_exported_whitelist(self, client, mock_logger):
        """Test pattern_exported only logs whitelisted properties."""
        response = client.post(
            "/api/v1/telemetry/events",
            json={
                "event": "pattern_exported",
                "properties": {
                    "export_format": "pdf",  # Whitelisted
                    "paper_size": "A4",  # Whitelisted
                    "shape_type": "sphere",  # NOT whitelisted for this event
                },
            },
        )

        assert response.status_code == 204

        log_call = mock_logger.info.call_args[0][0]
        log_data = json.loads(log_call)

        # Whitelisted for this event
        assert log_data["properties"]["export_format"] == "pdf"
        assert log_data["properties"]["paper_size"] == "A4"

        # Not whitelisted for pattern_exported
        assert "shape_type" not in log_data["properties"]


class TestAPIDocumentation:
    """Test API documentation."""

    def test_endpoint_in_openapi_spec(self, client):
        """Test that telemetry endpoint appears in OpenAPI spec."""
        response = client.get("/openapi.json")
        assert response.status_code == 200

        openapi = response.json()
        paths = openapi["paths"]

        # Check endpoint exists
        assert "/api/v1/telemetry/events" in paths

        # Check it's a POST endpoint
        endpoint = paths["/api/v1/telemetry/events"]
        assert "post" in endpoint

    def test_endpoint_documentation(self, client):
        """Test that endpoint has proper documentation."""
        response = client.get("/openapi.json")
        openapi = response.json()

        endpoint = openapi["paths"]["/api/v1/telemetry/events"]["post"]

        # Check documentation
        assert "summary" in endpoint
        assert "description" in endpoint
        assert "Privacy" in endpoint["description"]

        # Check responses
        assert "204" in endpoint["responses"]
        assert "400" in endpoint["responses"]


class TestRealWorldScenarios:
    """Test realistic usage scenarios."""

    def test_complete_pattern_workflow(self, client, mock_logger):
        """Test tracking complete pattern generation workflow."""
        # 1. Pattern generated
        response = client.post(
            "/api/v1/telemetry/events",
            json={
                "event": "pattern_generated",
                "properties": {
                    "shape_type": "sphere",
                    "stitch_type": "sc",
                    "terms": "US",
                },
            },
        )
        assert response.status_code == 204

        # 2. Pattern visualized
        response = client.post(
            "/api/v1/telemetry/events",
            json={
                "event": "pattern_visualized",
                "properties": {
                    "shape_type": "sphere",
                    "highlight_changes": True,
                },
            },
        )
        assert response.status_code == 204

        # 3. Pattern exported
        response = client.post(
            "/api/v1/telemetry/events",
            json={
                "event": "pattern_exported",
                "properties": {
                    "export_format": "pdf",
                    "include_diagram": True,
                },
            },
        )
        assert response.status_code == 204

        # All three events should be logged
        assert mock_logger.info.call_count == 3

    def test_mixed_valid_and_invalid_properties(self, client, mock_logger):
        """Test that valid properties are logged while invalid are dropped."""
        response = client.post(
            "/api/v1/telemetry/events",
            json={
                "event": "pattern_generated",
                "properties": {
                    "shape_type": "cylinder",  # Valid
                    "terms": "UK",  # Valid
                    "user_id": "secret",  # Invalid - PII
                    "diameter": 15,  # Invalid - PII
                    "random_field": "value",  # Invalid - not whitelisted
                },
            },
        )

        assert response.status_code == 204

        log_call = mock_logger.info.call_args[0][0]
        log_data = json.loads(log_call)

        # Valid properties should be present
        assert log_data["properties"]["shape_type"] == "cylinder"
        assert log_data["properties"]["terms"] == "UK"

        # Invalid properties should be absent
        assert "user_id" not in log_data["properties"]
        assert "diameter" not in log_data["properties"]
        assert "random_field" not in log_data["properties"]


class TestNoPIIGuarantee:
    """Critical tests to verify NO PII can ever be logged via API."""

    @pytest.mark.parametrize(
        "pii_field,pii_value",
        [
            ("user_id", "user123"),
            ("email", "test@example.com"),
            ("ip_address", "192.168.1.1"),
            ("pattern_content", "R1: MR 6 sc (6)"),
            ("diameter", 10),
            ("stitches", 36),
            ("yardage", 50),
        ],
    )
    def test_no_pii_ever_logged(self, client, mock_logger, pii_field, pii_value):
        """Test that NO PII can be logged through API."""
        response = client.post(
            "/api/v1/telemetry/events",
            json={
                "event": "pattern_generated",
                "properties": {
                    "shape_type": "sphere",
                    pii_field: pii_value,
                },
            },
        )

        # Should succeed (silently scrub)
        assert response.status_code == 204

        # Check logged data
        log_call = mock_logger.info.call_args[0][0]
        log_data = json.loads(log_call)

        # PII must NOT be in logged data
        assert pii_field not in log_data["properties"]
        assert str(pii_value) not in str(log_data["properties"])

    def test_no_pattern_details_logged(self, client, mock_logger):
        """Test that pattern details are NEVER logged."""
        response = client.post(
            "/api/v1/telemetry/events",
            json={
                "event": "pattern_generated",
                "properties": {
                    "shape_type": "sphere",
                    "diameter": 10,
                    "height": 15,
                    "rounds": 12,
                    "stitches": 36,
                    "yardage": 50,
                },
            },
        )

        assert response.status_code == 204

        log_call = mock_logger.info.call_args[0][0]
        log_data = json.loads(log_call)

        # NO pattern details
        assert "diameter" not in log_data["properties"]
        assert "height" not in log_data["properties"]
        assert "rounds" not in log_data["properties"]
        assert "stitches" not in log_data["properties"]
        assert "yardage" not in log_data["properties"]

    def test_only_safe_metadata_logged(self, client, mock_logger):
        """Test that only safe metadata (types, not values) is logged."""
        response = client.post(
            "/api/v1/telemetry/events",
            json={
                "event": "pattern_generated",
                "properties": {
                    # Safe: types and categories
                    "shape_type": "cylinder",
                    "stitch_type": "sc",
                    "terms": "US",
                    "units": "cm",
                    # Unsafe: actual values
                    "diameter": 20,
                    "height": 30,
                },
            },
        )

        assert response.status_code == 204

        log_call = mock_logger.info.call_args[0][0]
        log_data = json.loads(log_call)

        # Only safe metadata should be present
        props = log_data["properties"]
        assert "shape_type" in props
        assert "stitch_type" in props
        assert "terms" in props

        # NO actual values
        assert "diameter" not in props
        assert "height" not in props
