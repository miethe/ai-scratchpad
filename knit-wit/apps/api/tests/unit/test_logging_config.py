"""
Unit tests for logging configuration module.

Tests:
- JSON formatting
- Log rotation configuration
- 90-day retention policy
- Correlation ID tracking
- Log levels
"""

import json
import logging
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from app.core.logging_config import (
    JSONFormatter,
    LoggingConfig,
    init_logging,
    set_correlation_id,
    get_correlation_id,
    clear_correlation_id,
)


class TestJSONFormatter:
    """Test JSON log formatting."""

    def test_basic_formatting(self):
        """Test basic JSON log entry formatting."""
        formatter = JSONFormatter()
        record = logging.LogRecord(
            name="test.logger",
            level=logging.INFO,
            pathname="test.py",
            lineno=42,
            msg="Test message",
            args=(),
            exc_info=None,
        )

        result = formatter.format(record)
        log_entry = json.loads(result)

        assert log_entry["level"] == "INFO"
        assert log_entry["logger"] == "test.logger"
        assert log_entry["message"] == "Test message"
        assert "timestamp" in log_entry
        # Verify timestamp is valid ISO8601
        datetime.fromisoformat(log_entry["timestamp"])

    def test_correlation_id_included(self):
        """Test correlation ID is included when set."""
        formatter = JSONFormatter()
        set_correlation_id("req_test123")

        record = logging.LogRecord(
            name="test.logger",
            level=logging.INFO,
            pathname="test.py",
            lineno=42,
            msg="Test message",
            args=(),
            exc_info=None,
        )

        result = formatter.format(record)
        log_entry = json.loads(result)

        assert log_entry["correlation_id"] == "req_test123"

        # Cleanup
        clear_correlation_id()

    def test_extra_fields_included(self):
        """Test extra fields are included in log output."""
        formatter = JSONFormatter()
        record = logging.LogRecord(
            name="test.logger",
            level=logging.INFO,
            pathname="test.py",
            lineno=42,
            msg="Test message",
            args=(),
            exc_info=None,
        )
        # Add extra fields
        record.event = "pattern_generated"
        record.properties = {"shape_type": "sphere"}

        result = formatter.format(record)
        log_entry = json.loads(result)

        assert log_entry["event"] == "pattern_generated"
        assert log_entry["properties"] == {"shape_type": "sphere"}

    def test_exception_formatting(self):
        """Test exception information is formatted correctly."""
        formatter = JSONFormatter()

        try:
            raise ValueError("Test error")
        except ValueError:
            import sys
            record = logging.LogRecord(
                name="test.logger",
                level=logging.ERROR,
                pathname="test.py",
                lineno=42,
                msg="Error occurred",
                args=(),
                exc_info=sys.exc_info(),
            )

            result = formatter.format(record)
            log_entry = json.loads(result)

            assert log_entry["level"] == "ERROR"
            assert "exception" in log_entry
            assert "ValueError: Test error" in log_entry["exception"]

    def test_timestamp_is_utc(self):
        """Test timestamp is in UTC timezone."""
        formatter = JSONFormatter()
        record = logging.LogRecord(
            name="test.logger",
            level=logging.INFO,
            pathname="test.py",
            lineno=42,
            msg="Test message",
            args=(),
            exc_info=None,
        )

        result = formatter.format(record)
        log_entry = json.loads(result)

        # Parse timestamp and verify it's UTC
        timestamp = datetime.fromisoformat(log_entry["timestamp"])
        assert timestamp.tzinfo == timezone.utc


class TestCorrelationID:
    """Test correlation ID context management."""

    def test_set_and_get_correlation_id(self):
        """Test setting and getting correlation ID."""
        set_correlation_id("req_abc123")
        assert get_correlation_id() == "req_abc123"
        clear_correlation_id()

    def test_clear_correlation_id(self):
        """Test clearing correlation ID."""
        set_correlation_id("req_test456")
        clear_correlation_id()
        assert get_correlation_id() is None

    def test_default_correlation_id_is_none(self):
        """Test default correlation ID is None."""
        clear_correlation_id()
        assert get_correlation_id() is None


class TestLoggingConfig:
    """Test logging configuration."""

    @pytest.fixture
    def temp_log_dir(self):
        """Create temporary log directory for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    def test_init_creates_log_directory(self, temp_log_dir):
        """Test LoggingConfig creates log directory if it doesn't exist."""
        log_dir = Path(temp_log_dir) / "new_logs"
        assert not log_dir.exists()

        config = LoggingConfig(log_dir=str(log_dir))
        assert log_dir.exists()

    def test_configure_sets_log_level(self, temp_log_dir):
        """Test configure() sets the correct log level."""
        config = LoggingConfig(log_level="DEBUG", log_dir=temp_log_dir)
        config.configure()

        root_logger = logging.getLogger()
        assert root_logger.level == logging.DEBUG

    def test_configure_adds_file_handler(self, temp_log_dir):
        """Test configure() adds TimedRotatingFileHandler."""
        config = LoggingConfig(log_dir=temp_log_dir)
        config.configure()

        root_logger = logging.getLogger()
        file_handlers = [
            h for h in root_logger.handlers
            if isinstance(h, logging.handlers.TimedRotatingFileHandler)
        ]

        assert len(file_handlers) > 0
        handler = file_handlers[0]
        assert handler.when == "D"  # Daily rotation
        # Note: interval is in seconds for 'D' mode, so 1 day = 86400 seconds
        assert handler.interval == 86400
        assert handler.backupCount == 90  # 90-day retention

    def test_configure_adds_console_handler(self, temp_log_dir):
        """Test configure() adds console handler when enabled."""
        config = LoggingConfig(log_dir=temp_log_dir, enable_console=True)
        config.configure()

        root_logger = logging.getLogger()
        console_handlers = [
            h for h in root_logger.handlers
            if isinstance(h, logging.StreamHandler) and not isinstance(h, logging.handlers.TimedRotatingFileHandler)
        ]

        assert len(console_handlers) > 0

    def test_configure_no_console_handler(self, temp_log_dir):
        """Test configure() doesn't add console handler when disabled."""
        config = LoggingConfig(log_dir=temp_log_dir, enable_console=False)
        config.configure()

        root_logger = logging.getLogger()
        # Remove all handlers first, then configure
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        config.configure()

        console_handlers = [
            h for h in root_logger.handlers
            if isinstance(h, logging.StreamHandler) and not isinstance(h, logging.handlers.TimedRotatingFileHandler)
        ]

        assert len(console_handlers) == 0

    def test_retention_days_configuration(self, temp_log_dir):
        """Test custom retention days configuration."""
        config = LoggingConfig(log_dir=temp_log_dir, retention_days=30)
        config.configure()

        root_logger = logging.getLogger()
        file_handlers = [
            h for h in root_logger.handlers
            if isinstance(h, logging.handlers.TimedRotatingFileHandler)
        ]

        assert file_handlers[0].backupCount == 30

    def test_get_logger(self, temp_log_dir):
        """Test get_logger() returns configured logger."""
        config = LoggingConfig(log_dir=temp_log_dir)
        config.configure()

        logger = config.get_logger("test.logger")
        assert logger.name == "test.logger"
        assert isinstance(logger, logging.Logger)

    def test_json_formatter_attached(self, temp_log_dir):
        """Test handlers use JSONFormatter."""
        config = LoggingConfig(log_dir=temp_log_dir)
        config.configure()

        root_logger = logging.getLogger()
        for handler in root_logger.handlers:
            assert isinstance(handler.formatter, JSONFormatter)


class TestInitLogging:
    """Test global logging initialization."""

    @pytest.fixture
    def temp_log_dir(self):
        """Create temporary log directory for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    def test_init_logging_returns_config(self, temp_log_dir):
        """Test init_logging() returns LoggingConfig instance."""
        config = init_logging(log_dir=temp_log_dir)
        assert isinstance(config, LoggingConfig)

    def test_init_logging_with_custom_parameters(self, temp_log_dir):
        """Test init_logging() accepts custom parameters."""
        config = init_logging(
            log_level="DEBUG",
            log_dir=temp_log_dir,
            retention_days=30,
            enable_console=False,
        )

        assert config.log_level == logging.DEBUG
        assert str(config.log_dir) == temp_log_dir
        assert config.retention_days == 30
        assert config.enable_console is False


class TestLogRotation:
    """Test log rotation behavior."""

    @pytest.fixture
    def temp_log_dir(self):
        """Create temporary log directory for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    def test_log_file_created(self, temp_log_dir):
        """Test that log file is created after configuration."""
        config = LoggingConfig(log_dir=temp_log_dir)
        config.configure()

        # Write a log message
        logger = logging.getLogger("test")
        logger.info("Test message")

        # Check log file exists
        log_file = Path(temp_log_dir) / "telemetry.log"
        assert log_file.exists()

    def test_log_content_is_json(self, temp_log_dir):
        """Test that log file contains valid JSON."""
        config = LoggingConfig(log_dir=temp_log_dir)
        config.configure()

        # Write a log message
        logger = logging.getLogger("test")
        logger.info("Test message", extra={"event": "test_event"})

        # Read and verify JSON
        log_file = Path(temp_log_dir) / "telemetry.log"
        with open(log_file) as f:
            line = f.readline()
            log_entry = json.loads(line)

            assert log_entry["message"] == "Test message"
            assert log_entry["event"] == "test_event"
            assert log_entry["level"] == "INFO"

    @patch("logging.handlers.TimedRotatingFileHandler.shouldRollover")
    def test_rotation_trigger(self, mock_should_rollover, temp_log_dir):
        """Test that rotation is triggered appropriately."""
        config = LoggingConfig(log_dir=temp_log_dir)
        config.configure()

        # Mock rotation trigger
        mock_should_rollover.return_value = True

        logger = logging.getLogger("test")
        logger.info("Test message before rotation")

        # Verify shouldRollover was called
        assert mock_should_rollover.called


class TestTelemetryIntegration:
    """Test integration with TelemetryService."""

    @pytest.fixture
    def temp_log_dir(self):
        """Create temporary log directory for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    def test_telemetry_logs_to_file(self, temp_log_dir):
        """Test TelemetryService logs are written to rotating file."""
        from app.services.telemetry_service import TelemetryService

        # Initialize logging
        config = LoggingConfig(log_dir=temp_log_dir)
        config.configure()

        # Track an event
        service = TelemetryService()
        service.track_event(
            "pattern_generated",
            {"shape_type": "sphere", "stitch_type": "sc", "terms": "US"},
        )

        # Verify log file contains the event
        log_file = Path(temp_log_dir) / "telemetry.log"
        assert log_file.exists()

        with open(log_file) as f:
            line = f.readline()
            log_wrapper = json.loads(line)

            # TelemetryService logs JSON as a string in the message field
            # Parse the inner JSON to verify event data
            inner_log = json.loads(log_wrapper["message"])

            assert inner_log["event"] == "pattern_generated"
            assert inner_log["properties"]["shape_type"] == "sphere"
            assert log_wrapper["level"] == "INFO"

    def test_telemetry_warning_logs(self, temp_log_dir):
        """Test TelemetryService warning logs for PII blocking."""
        from app.services.telemetry_service import TelemetryService

        # Initialize logging
        config = LoggingConfig(log_dir=temp_log_dir)
        config.configure()

        # Try to track event with PII (should be blocked)
        service = TelemetryService()
        service.track_event(
            "pattern_generated",
            {
                "shape_type": "sphere",
                "user_id": "secret123",  # PII - should be blocked
            },
        )

        # Verify warning log
        log_file = Path(temp_log_dir) / "telemetry.log"
        with open(log_file) as f:
            lines = f.readlines()

            # Should have at least 2 lines: 1 warning (PII blocked), 1 info (event tracked)
            assert len(lines) >= 2

            # Check for warning about PII
            warning_found = False
            for line in lines:
                entry = json.loads(line)
                if entry["level"] == "WARNING" and "PII" in entry["message"]:
                    warning_found = True
                    # Warning logs have extra fields from TelemetryService
                    assert entry["field"] == "user_id"
                    assert entry["event"] == "pattern_generated"

            assert warning_found
