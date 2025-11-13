"""
Logging configuration for Knit-Wit API.

Provides production-grade structured JSON logging with:
- Automatic log rotation (daily)
- 90-day retention policy
- Request correlation IDs for tracing
- Environment-based log levels
- Both file and console output
"""

import json
import logging
import sys
from datetime import datetime, timezone
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import Any, Dict, Optional
from contextvars import ContextVar

# Context variable for correlation IDs (request tracing)
correlation_id: ContextVar[Optional[str]] = ContextVar("correlation_id", default=None)


class JSONFormatter(logging.Formatter):
    """
    Formats log records as structured JSON.

    Output format:
    {
        "timestamp": "2024-11-13T19:00:00.000Z",
        "level": "INFO",
        "logger": "knit_wit.telemetry",
        "message": "Event tracked",
        "correlation_id": "req_abc123",
        "event": "pattern_generated",
        "properties": {...}
    }
    """

    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record as JSON string.

        Args:
            record: Log record to format

        Returns:
            JSON-formatted log string
        """
        # Build base log entry
        log_entry: Dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(
                record.created, tz=timezone.utc
            ).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add correlation ID if present
        corr_id = correlation_id.get()
        if corr_id:
            log_entry["correlation_id"] = corr_id

        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        # Add extra fields from LogRecord
        # Pydantic and FastAPI often use 'extra' dict for additional context
        if hasattr(record, "extra") and isinstance(record.extra, dict):
            log_entry.update(record.extra)

        # Standard extra fields from logging.LogRecord.__dict__
        # Filter out built-in fields to avoid duplicates
        builtin_fields = {
            "name",
            "msg",
            "args",
            "created",
            "msecs",
            "levelname",
            "levelno",
            "pathname",
            "filename",
            "module",
            "exc_info",
            "exc_text",
            "stack_info",
            "lineno",
            "funcName",
            "process",
            "processName",
            "thread",
            "threadName",
            "taskName",
            "relativeCreated",
            "extra",
        }

        for key, value in record.__dict__.items():
            if key not in builtin_fields and not key.startswith("_"):
                log_entry[key] = value

        return json.dumps(log_entry, default=str, ensure_ascii=False)


class LoggingConfig:
    """
    Centralized logging configuration for the application.

    Manages:
    - JSON formatting for structured logs
    - Daily log rotation with 90-day retention
    - File and console handlers
    - Environment-based log levels
    """

    def __init__(
        self,
        log_level: str = "INFO",
        log_dir: str = "logs/telemetry",
        retention_days: int = 90,
        enable_console: bool = True,
    ):
        """
        Initialize logging configuration.

        Args:
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_dir: Directory for log files
            retention_days: Number of days to retain logs
            enable_console: Whether to enable console logging
        """
        self.log_level = getattr(logging, log_level.upper())
        self.log_dir = Path(log_dir)
        self.retention_days = retention_days
        self.enable_console = enable_console

        # Ensure log directory exists
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def configure(self) -> None:
        """
        Configure application logging with rotation and JSON formatting.

        Sets up:
        - Root logger with specified level
        - TimedRotatingFileHandler (daily rotation, 90-day retention)
        - Console handler (optional)
        - JSON formatter for structured output
        """
        # Get root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(self.log_level)

        # Remove existing handlers to avoid duplicates
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        # Create JSON formatter
        json_formatter = JSONFormatter()

        # File handler with rotation
        file_handler = TimedRotatingFileHandler(
            filename=self.log_dir / "telemetry.log",
            when="D",  # Daily rotation
            interval=1,  # Every 1 day
            backupCount=self.retention_days,  # Keep 90 days
            encoding="utf-8",
            utc=True,  # Use UTC for timestamps
        )
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(json_formatter)
        file_handler.suffix = "%Y-%m-%d"  # File pattern: telemetry.log.2024-11-13
        root_logger.addHandler(file_handler)

        # Console handler (development/debugging)
        if self.enable_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(self.log_level)
            console_handler.setFormatter(json_formatter)
            root_logger.addHandler(console_handler)

        # Configure knit_wit loggers
        self._configure_app_loggers()

    def _configure_app_loggers(self) -> None:
        """Configure application-specific loggers with appropriate levels."""
        # Telemetry logger (main use case)
        telemetry_logger = logging.getLogger("knit_wit.telemetry")
        telemetry_logger.setLevel(self.log_level)

        # API logger
        api_logger = logging.getLogger("knit_wit.api")
        api_logger.setLevel(self.log_level)

        # Service logger
        service_logger = logging.getLogger("knit_wit.service")
        service_logger.setLevel(self.log_level)

        # Reduce noise from third-party libraries
        logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
        logging.getLogger("uvicorn.error").setLevel(logging.INFO)

    def get_logger(self, name: str) -> logging.Logger:
        """
        Get a configured logger by name.

        Args:
            name: Logger name (e.g., "knit_wit.telemetry")

        Returns:
            Configured logger instance
        """
        return logging.getLogger(name)


def set_correlation_id(corr_id: str) -> None:
    """
    Set correlation ID for the current request context.

    Used for request tracing across logs.

    Args:
        corr_id: Correlation ID (e.g., "req_abc123")
    """
    correlation_id.set(corr_id)


def get_correlation_id() -> Optional[str]:
    """
    Get correlation ID for the current request context.

    Returns:
        Correlation ID if set, None otherwise
    """
    return correlation_id.get()


def clear_correlation_id() -> None:
    """Clear correlation ID for the current request context."""
    correlation_id.set(None)


# Global logging config instance (initialized in main.py)
_logging_config: Optional[LoggingConfig] = None


def init_logging(
    log_level: str = "INFO",
    log_dir: str = "logs/telemetry",
    retention_days: int = 90,
    enable_console: bool = True,
) -> LoggingConfig:
    """
    Initialize global logging configuration.

    Should be called once at application startup.

    Args:
        log_level: Logging level
        log_dir: Directory for log files
        retention_days: Number of days to retain logs
        enable_console: Whether to enable console logging

    Returns:
        Configured LoggingConfig instance
    """
    global _logging_config

    _logging_config = LoggingConfig(
        log_level=log_level,
        log_dir=log_dir,
        retention_days=retention_days,
        enable_console=enable_console,
    )
    _logging_config.configure()

    return _logging_config


def get_logging_config() -> Optional[LoggingConfig]:
    """
    Get the global logging configuration.

    Returns:
        LoggingConfig instance if initialized, None otherwise
    """
    return _logging_config
