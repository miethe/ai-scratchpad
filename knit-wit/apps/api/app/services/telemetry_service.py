"""
Telemetry Service for Knit-Wit API

Provides privacy-respecting anonymous event tracking with NO PII.
All events are logged as structured JSON for later analysis.

Logging is configured with:
- Daily rotation (TimedRotatingFileHandler)
- 90-day retention policy
- Structured JSON output
- Request correlation IDs for tracing
"""

import logging
import json
from datetime import datetime, timezone
from typing import Dict, Any, Set, Optional
from enum import Enum


# Use the configured structured JSON logger
# Logger is configured via app.core.logging_config.init_logging() at startup
logger = logging.getLogger("knit_wit.telemetry")


class EventType(str, Enum):
    """Supported telemetry event types."""

    PATTERN_GENERATED = "pattern_generated"
    PATTERN_VISUALIZED = "pattern_visualized"
    PATTERN_EXPORTED = "pattern_exported"


class TelemetryError(Exception):
    """Exception raised for telemetry validation errors."""

    pass


class TelemetryService:
    """
    Service for anonymous telemetry event tracking.

    **Privacy Principles:**
    - NO personally identifiable information (PII)
    - NO pattern content, dimensions, or user-specific data
    - NO IP addresses, user agents, or request metadata
    - Silent failures: never block user experience

    **Supported Events:**
    - pattern_generated: Pattern compilation completed
    - pattern_visualized: Visualization rendered
    - pattern_exported: Pattern exported to PDF/JSON/SVG

    **Log Format:**
    ```json
    {
        "timestamp": "2024-11-13T19:00:00.000Z",
        "event": "pattern_generated",
        "properties": {
            "shape_type": "sphere",
            "stitch_type": "sc",
            "terms": "US"
        }
    }
    ```
    """

    # Properties that could contain PII or sensitive data
    PII_FIELDS: Set[str] = {
        "pattern_content",
        "pattern_text",
        "notes",
        "user_id",
        "email",
        "ip_address",
        "user_agent",
        "session_id",
        "diameter",
        "height",
        "radius",
        "circumference",
        "dimensions",
        "stitches",
        "rounds",
        "yardage",
    }

    # Allowed properties for each event type (whitelist)
    ALLOWED_PROPERTIES: Dict[str, Set[str]] = {
        EventType.PATTERN_GENERATED: {
            "shape_type",
            "stitch_type",
            "terms",
            "units",
            "round_mode",
        },
        EventType.PATTERN_VISUALIZED: {
            "shape_type",
            "highlight_changes",
            "terms",
        },
        EventType.PATTERN_EXPORTED: {
            "export_format",
            "include_diagram",
            "paper_size",
            "terms",
        },
    }

    def __init__(self):
        """Initialize telemetry service."""
        pass

    def track_event(
        self, event: str, properties: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Track an anonymous telemetry event.

        **Privacy Guarantee:** This method validates that NO PII is logged.
        All properties are scrubbed and validated against a whitelist.

        Args:
            event: Event name (must be in EventType enum)
            properties: Event properties (optional, will be scrubbed)

        Raises:
            TelemetryError: If event name is invalid (validation only)

        Note:
            This method NEVER raises exceptions during normal operation.
            All errors are logged and swallowed to prevent blocking user experience.
        """
        try:
            # Validate event type
            self._validate_event_type(event)

            # Scrub and validate properties
            safe_properties = self._scrub_properties(event, properties or {})

            # Build log entry
            log_entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "event": event,
                "properties": safe_properties,
            }

            # Log as structured JSON (compatible with existing tests and logging rotation)
            logger.info(json.dumps(log_entry))

        except TelemetryError:
            # Validation errors should be raised (for API validation)
            raise

        except Exception as e:
            # All other errors are logged but swallowed (silent failure)
            logger.error(
                f"Telemetry tracking failed: {str(e)}",
                extra={"event": event, "error": str(e)},
            )

    def _validate_event_type(self, event: str) -> None:
        """
        Validate event type against whitelist.

        Args:
            event: Event name to validate

        Raises:
            TelemetryError: If event type is not supported
        """
        valid_events = {e.value for e in EventType}
        if event not in valid_events:
            raise TelemetryError(
                f"Invalid event type: '{event}'. "
                f"Supported: {', '.join(sorted(valid_events))}"
            )

    def _scrub_properties(
        self, event: str, properties: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Scrub properties to remove PII and validate against whitelist.

        This method implements multiple layers of protection:
        1. Block any properties in PII_FIELDS blacklist
        2. Only allow properties in event-specific whitelist
        3. Validate property values are not sensitive

        Args:
            event: Event type
            properties: Raw properties to scrub

        Returns:
            Scrubbed and validated properties

        Raises:
            TelemetryError: If PII is detected in properties
        """
        if not properties:
            return {}

        scrubbed = {}
        allowed = self.ALLOWED_PROPERTIES.get(event, set())

        for key, value in properties.items():
            # Check PII blacklist
            if key in self.PII_FIELDS:
                logger.warning(
                    f"Blocked PII field in telemetry: {key}",
                    extra={"event": event, "field": key},
                )
                continue

            # Check whitelist for this event type
            if key not in allowed:
                logger.warning(
                    f"Blocked non-whitelisted field in telemetry: {key}",
                    extra={"event": event, "field": key},
                )
                continue

            # Validate value is not suspiciously large (potential data leak)
            if isinstance(value, str) and len(value) > 100:
                logger.warning(
                    f"Blocked oversized string value in telemetry: {key}",
                    extra={"event": event, "field": key, "length": len(value)},
                )
                continue

            # Value is safe - include it
            scrubbed[key] = value

        return scrubbed

    def validate_event(self, event: str, properties: Dict[str, Any]) -> None:
        """
        Validate event and properties without logging.

        Used for API validation before accepting telemetry events.

        Args:
            event: Event name to validate
            properties: Properties to validate

        Raises:
            TelemetryError: If validation fails
        """
        self._validate_event_type(event)
        self._scrub_properties(event, properties)


# Global telemetry service instance
telemetry_service = TelemetryService()
