"""
Unit tests for TelemetryService

Tests privacy-respecting telemetry with NO PII logging.
"""

import pytest
import logging
import json
from unittest.mock import patch, MagicMock

from app.services.telemetry_service import (
    TelemetryService,
    TelemetryError,
    EventType,
)


@pytest.fixture
def telemetry_service():
    """Create telemetry service instance."""
    return TelemetryService()


@pytest.fixture
def mock_logger():
    """Create mock logger to capture log output."""
    with patch("app.services.telemetry_service.logger") as mock:
        yield mock


class TestEventValidation:
    """Test event type validation."""

    def test_validate_supported_events(self, telemetry_service):
        """Test validation passes for all supported events."""
        supported_events = [
            "pattern_generated",
            "pattern_visualized",
            "pattern_exported",
        ]

        for event in supported_events:
            # Should not raise
            telemetry_service._validate_event_type(event)

    def test_validate_invalid_event(self, telemetry_service):
        """Test validation fails for unsupported events."""
        with pytest.raises(TelemetryError, match="Invalid event type"):
            telemetry_service._validate_event_type("invalid_event")

    def test_validate_event_suggests_alternatives(self, telemetry_service):
        """Test error message suggests valid event types."""
        with pytest.raises(TelemetryError) as exc_info:
            telemetry_service._validate_event_type("user_login")

        error_msg = str(exc_info.value)
        assert "Supported:" in error_msg
        assert "pattern_generated" in error_msg


class TestPIIProtection:
    """Test PII protection and scrubbing."""

    def test_block_pii_fields(self, telemetry_service, mock_logger):
        """Test that PII fields are blocked from logging."""
        pii_fields = [
            "user_id",
            "email",
            "ip_address",
            "pattern_content",
            "diameter",
            "stitches",
            "yardage",
        ]

        for field in pii_fields:
            properties = {field: "sensitive_value", "shape_type": "sphere"}

            scrubbed = telemetry_service._scrub_properties(
                EventType.PATTERN_GENERATED, properties
            )

            # PII field should be removed
            assert field not in scrubbed
            # Safe field should remain
            assert "shape_type" in scrubbed

            # Warning should be logged
            assert mock_logger.warning.called

    def test_allow_whitelisted_fields(self, telemetry_service):
        """Test that whitelisted fields are allowed."""
        properties = {
            "shape_type": "sphere",
            "stitch_type": "sc",
            "terms": "US",
            "units": "cm",
        }

        scrubbed = telemetry_service._scrub_properties(
            EventType.PATTERN_GENERATED, properties
        )

        # All whitelisted fields should be present
        assert scrubbed == properties

    def test_block_non_whitelisted_fields(self, telemetry_service):
        """Test that non-whitelisted fields are blocked."""
        properties = {
            "shape_type": "sphere",
            "custom_field": "value",  # Not whitelisted
        }

        scrubbed = telemetry_service._scrub_properties(
            EventType.PATTERN_GENERATED, properties
        )

        # Only whitelisted field should remain
        assert "shape_type" in scrubbed
        assert "custom_field" not in scrubbed

    def test_block_oversized_strings(self, telemetry_service):
        """Test that suspiciously large strings are blocked."""
        properties = {
            "shape_type": "x" * 200,  # Too large
            "terms": "US",  # Normal
        }

        scrubbed = telemetry_service._scrub_properties(
            EventType.PATTERN_GENERATED, properties
        )

        # Oversized field should be removed
        assert "shape_type" not in scrubbed
        # Normal field should remain
        assert "terms" in scrubbed

    def test_empty_properties(self, telemetry_service):
        """Test scrubbing empty properties."""
        scrubbed = telemetry_service._scrub_properties(
            EventType.PATTERN_GENERATED, {}
        )
        assert scrubbed == {}

        scrubbed = telemetry_service._scrub_properties(
            EventType.PATTERN_GENERATED, None
        )
        assert scrubbed == {}


class TestEventTracking:
    """Test event tracking functionality."""

    def test_track_valid_event(self, telemetry_service, mock_logger):
        """Test tracking a valid event logs correctly."""
        telemetry_service.track_event(
            event="pattern_generated",
            properties={"shape_type": "sphere", "terms": "US"},
        )

        # Should log info
        assert mock_logger.info.called
        log_call = mock_logger.info.call_args[0][0]

        # Should be valid JSON
        log_data = json.loads(log_call)

        # Check log structure
        assert "timestamp" in log_data
        assert log_data["event"] == "pattern_generated"
        assert "properties" in log_data
        assert log_data["properties"]["shape_type"] == "sphere"
        assert log_data["properties"]["terms"] == "US"

    def test_track_event_timestamp_format(self, telemetry_service, mock_logger):
        """Test that timestamp is in ISO 8601 format with timezone."""
        telemetry_service.track_event("pattern_generated", {})

        log_call = mock_logger.info.call_args[0][0]
        log_data = json.loads(log_call)

        # Should have ISO 8601 timestamp with timezone
        timestamp = log_data["timestamp"]
        assert "T" in timestamp
        assert "Z" in timestamp or "+" in timestamp

    def test_track_event_scrubs_pii(self, telemetry_service, mock_logger):
        """Test that PII is scrubbed from tracked events."""
        telemetry_service.track_event(
            event="pattern_generated",
            properties={
                "shape_type": "sphere",
                "user_id": "secret123",  # PII - should be removed
                "diameter": 10,  # PII - should be removed
            },
        )

        log_call = mock_logger.info.call_args[0][0]
        log_data = json.loads(log_call)

        # Should contain safe field
        assert log_data["properties"]["shape_type"] == "sphere"

        # Should NOT contain PII
        assert "user_id" not in log_data["properties"]
        assert "diameter" not in log_data["properties"]

    def test_track_event_without_properties(self, telemetry_service, mock_logger):
        """Test tracking event without properties."""
        telemetry_service.track_event("pattern_generated")

        log_call = mock_logger.info.call_args[0][0]
        log_data = json.loads(log_call)

        assert log_data["event"] == "pattern_generated"
        assert log_data["properties"] == {}

    def test_track_invalid_event_raises(self, telemetry_service):
        """Test tracking invalid event raises TelemetryError."""
        with pytest.raises(TelemetryError):
            telemetry_service.track_event("invalid_event")


class TestSilentFailures:
    """Test that telemetry failures never block user experience."""

    def test_logging_error_caught(self, telemetry_service, mock_logger):
        """Test that logging errors are caught and logged."""
        # Make logger.info raise an exception
        mock_logger.info.side_effect = Exception("Logging failed")

        # Should not raise - silent failure
        telemetry_service.track_event("pattern_generated", {"shape_type": "sphere"})

        # Error should be logged
        assert mock_logger.error.called

    def test_json_serialization_error_caught(self, telemetry_service):
        """Test that JSON serialization errors are caught."""
        # Properties with non-serializable value
        properties = {"callback": lambda x: x}

        # Should not raise - silent failure
        telemetry_service.track_event("pattern_generated", properties)


class TestEventSpecificWhitelists:
    """Test event-specific property whitelists."""

    def test_pattern_generated_whitelist(self, telemetry_service):
        """Test pattern_generated event whitelist."""
        properties = {
            "shape_type": "sphere",
            "stitch_type": "sc",
            "terms": "US",
            "units": "cm",
            "round_mode": "spiral",
        }

        scrubbed = telemetry_service._scrub_properties(
            EventType.PATTERN_GENERATED, properties
        )

        # All should be allowed
        assert scrubbed == properties

    def test_pattern_visualized_whitelist(self, telemetry_service):
        """Test pattern_visualized event whitelist."""
        properties = {
            "shape_type": "cylinder",
            "highlight_changes": True,
            "terms": "UK",
        }

        scrubbed = telemetry_service._scrub_properties(
            EventType.PATTERN_VISUALIZED, properties
        )

        assert scrubbed == properties

    def test_pattern_exported_whitelist(self, telemetry_service):
        """Test pattern_exported event whitelist."""
        properties = {
            "export_format": "pdf",
            "include_diagram": True,
            "paper_size": "A4",
            "terms": "US",
        }

        scrubbed = telemetry_service._scrub_properties(
            EventType.PATTERN_EXPORTED, properties
        )

        assert scrubbed == properties

    def test_cross_event_property_blocking(self, telemetry_service):
        """Test that properties are blocked across wrong event types."""
        # export_format is valid for EXPORTED but not GENERATED
        properties = {"export_format": "pdf"}

        scrubbed = telemetry_service._scrub_properties(
            EventType.PATTERN_GENERATED, properties
        )

        # Should be blocked (wrong event type)
        assert "export_format" not in scrubbed


class TestValidateEventMethod:
    """Test validate_event method for API validation."""

    def test_validate_event_success(self, telemetry_service):
        """Test validate_event passes for valid input."""
        # Should not raise
        telemetry_service.validate_event(
            "pattern_generated",
            {"shape_type": "sphere", "terms": "US"},
        )

    def test_validate_event_invalid_type(self, telemetry_service):
        """Test validate_event raises for invalid event type."""
        with pytest.raises(TelemetryError):
            telemetry_service.validate_event("invalid_event", {})

    def test_validate_event_does_not_log(self, telemetry_service, mock_logger):
        """Test validate_event does not log events."""
        telemetry_service.validate_event(
            "pattern_generated",
            {"shape_type": "sphere"},
        )

        # Should NOT log
        assert not mock_logger.info.called


class TestRealWorldScenarios:
    """Test realistic usage scenarios."""

    def test_pattern_generation_event(self, telemetry_service, mock_logger):
        """Test logging a pattern generation event."""
        telemetry_service.track_event(
            event="pattern_generated",
            properties={
                "shape_type": "sphere",
                "stitch_type": "sc",
                "terms": "US",
                "units": "cm",
                "round_mode": "spiral",
            },
        )

        log_call = mock_logger.info.call_args[0][0]
        log_data = json.loads(log_call)

        assert log_data["event"] == "pattern_generated"
        assert log_data["properties"]["shape_type"] == "sphere"

    def test_pattern_export_event(self, telemetry_service, mock_logger):
        """Test logging a pattern export event."""
        telemetry_service.track_event(
            event="pattern_exported",
            properties={
                "export_format": "pdf",
                "include_diagram": True,
                "paper_size": "A4",
            },
        )

        log_call = mock_logger.info.call_args[0][0]
        log_data = json.loads(log_call)

        assert log_data["event"] == "pattern_exported"
        assert log_data["properties"]["export_format"] == "pdf"

    def test_mixed_safe_and_unsafe_properties(self, telemetry_service, mock_logger):
        """Test that safe properties are logged while unsafe are removed."""
        telemetry_service.track_event(
            event="pattern_generated",
            properties={
                "shape_type": "cylinder",  # Safe
                "terms": "UK",  # Safe
                "diameter": 15,  # PII - should be removed
                "user_email": "user@example.com",  # PII - should be removed
            },
        )

        log_call = mock_logger.info.call_args[0][0]
        log_data = json.loads(log_call)

        # Safe properties should be present
        assert log_data["properties"]["shape_type"] == "cylinder"
        assert log_data["properties"]["terms"] == "UK"

        # PII should be absent
        assert "diameter" not in log_data["properties"]
        assert "user_email" not in log_data["properties"]


class TestNoPIIGuarantee:
    """Critical tests to verify NO PII can leak through."""

    @pytest.mark.parametrize(
        "pii_field,pii_value",
        [
            ("user_id", "user123"),
            ("email", "test@example.com"),
            ("ip_address", "192.168.1.1"),
            ("pattern_content", "R1: MR 6 sc (6)"),
            ("pattern_text", "Some pattern"),
            ("diameter", 10),
            ("height", 15),
            ("stitches", 36),
            ("rounds", 12),
            ("yardage", 50),
        ],
    )
    def test_no_pii_fields_logged(
        self, telemetry_service, mock_logger, pii_field, pii_value
    ):
        """Test that NO PII fields are ever logged."""
        properties = {pii_field: pii_value, "shape_type": "sphere"}

        telemetry_service.track_event("pattern_generated", properties)

        log_call = mock_logger.info.call_args[0][0]
        log_data = json.loads(log_call)

        # PII field must NOT be in logged data
        assert pii_field not in log_data["properties"]
        assert str(pii_value) not in str(log_data["properties"])

    def test_no_pattern_dimensions_logged(self, telemetry_service, mock_logger):
        """Test that pattern dimensions are NEVER logged."""
        telemetry_service.track_event(
            event="pattern_generated",
            properties={
                "shape_type": "sphere",
                "diameter": 10,  # Should be blocked
                "height": 15,  # Should be blocked
                "radius": 5,  # Should be blocked
            },
        )

        log_call = mock_logger.info.call_args[0][0]
        log_data = json.loads(log_call)

        # NO dimensions should be present
        assert "diameter" not in log_data["properties"]
        assert "height" not in log_data["properties"]
        assert "radius" not in log_data["properties"]

    def test_no_user_identifiers_logged(self, telemetry_service, mock_logger):
        """Test that NO user identifiers are logged."""
        telemetry_service.track_event(
            event="pattern_generated",
            properties={
                "shape_type": "cylinder",
                "user_id": "user123",
                "session_id": "session456",
                "email": "test@example.com",
            },
        )

        log_call = mock_logger.info.call_args[0][0]
        log_data = json.loads(log_call)

        # NO user identifiers
        assert "user_id" not in log_data["properties"]
        assert "session_id" not in log_data["properties"]
        assert "email" not in log_data["properties"]
