"""
Sentry error tracking configuration for Knit-Wit API.

Provides production-grade error tracking with:
- Automatic exception capture with stack traces
- Request context and breadcrumbs
- PII filtering for data privacy
- Integration with structured logging
- Environment-specific configuration
"""

import logging
from typing import Any, Dict, Optional

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.asyncio import AsyncioIntegration

from app.core.logging_config import get_correlation_id

logger = logging.getLogger("knit_wit.sentry")


def init_sentry(
    dsn: str,
    environment: str = "development",
    traces_sample_rate: float = 0.1,
    release: Optional[str] = None,
    enable_logging_integration: bool = True,
) -> None:
    """
    Initialize Sentry error tracking.

    Configures Sentry SDK with:
    - FastAPI integration for request context
    - Logging integration for breadcrumbs
    - PII scrubbing for data privacy
    - Custom before_send hook for filtering

    Args:
        dsn: Sentry DSN (Data Source Name) from project settings
        environment: Environment name (development, staging, production)
        traces_sample_rate: Percentage of transactions to trace (0.0-1.0)
        release: Application version/release identifier
        enable_logging_integration: Enable automatic logging breadcrumbs

    Example:
        >>> init_sentry(
        ...     dsn="https://examplePublicKey@o0.ingest.sentry.io/0",
        ...     environment="production",
        ...     traces_sample_rate=0.2,
        ...     release="knit-wit-api@0.1.0"
        ... )
    """
    if not dsn:
        logger.warning("Sentry DSN not provided - error tracking disabled")
        return

    # Configure integrations
    integrations = [
        # FastAPI integration - captures request data, headers, user info
        FastApiIntegration(
            transaction_style="endpoint",  # Group by endpoint, not by URL params
            failed_request_status_codes={500, 501, 502, 503, 504},  # Only track server errors
        ),
        # Asyncio integration - capture asyncio exceptions
        AsyncioIntegration(),
    ]

    # Add logging integration if enabled
    if enable_logging_integration:
        integrations.append(
            LoggingIntegration(
                level=logging.INFO,  # Capture INFO and above as breadcrumbs
                event_level=logging.ERROR,  # Send ERROR and above as events
            )
        )

    # Initialize Sentry SDK
    sentry_sdk.init(
        dsn=dsn,
        environment=environment,
        release=release,
        traces_sample_rate=traces_sample_rate,
        integrations=integrations,
        # Before send hook for custom filtering and PII scrubbing
        before_send=before_send_handler,
        # Before breadcrumb hook for filtering
        before_breadcrumb=before_breadcrumb_handler,
        # Enable performance monitoring
        enable_tracing=True,
        # Send default PII (disabled for privacy)
        send_default_pii=False,
        # Attach stack traces to messages
        attach_stacktrace=True,
        # Maximum breadcrumbs to keep
        max_breadcrumbs=50,
        # Debug mode (only in development)
        debug=environment == "development",
    )

    logger.info(f"Sentry initialized: environment={environment}, sample_rate={traces_sample_rate}")


def before_send_handler(event: Dict[str, Any], hint: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Filter and modify events before sending to Sentry.

    This hook allows us to:
    - Add custom context (correlation IDs, user context)
    - Filter sensitive data (PII)
    - Skip certain errors
    - Modify event data

    Args:
        event: Sentry event dictionary
        hint: Additional context (exception info, log record, etc.)

    Returns:
        Modified event dict, or None to skip sending this event

    Example event structure:
        {
            "event_id": "abc123",
            "timestamp": "2024-11-13T19:00:00",
            "level": "error",
            "message": "Error message",
            "exception": {"values": [...]},
            "request": {"url": "...", "headers": {...}},
            "tags": {...},
            "extra": {...}
        }
    """
    # Add correlation ID if available
    correlation_id = get_correlation_id()
    if correlation_id:
        if "tags" not in event:
            event["tags"] = {}
        event["tags"]["correlation_id"] = correlation_id

    # Filter out client errors (4xx) - we only care about server errors
    if "request" in event:
        # Check if this is a client error based on exception type
        exc_info = hint.get("exc_info")
        if exc_info:
            exc_type = exc_info[0]
            # Skip HTTPException with 4xx status codes
            if hasattr(exc_type, "__name__") and "HTTPException" in exc_type.__name__:
                exc_instance = hint.get("exc_info", [None, None, None])[1]
                if hasattr(exc_instance, "status_code") and 400 <= exc_instance.status_code < 500:
                    # Don't send client errors to Sentry
                    return None

    # Scrub PII from request data
    if "request" in event:
        event["request"] = _scrub_pii_from_request(event["request"])

    # Scrub PII from extra data
    if "extra" in event:
        event["extra"] = _scrub_pii_from_dict(event["extra"])

    return event


def before_breadcrumb_handler(crumb: Dict[str, Any], hint: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Filter and modify breadcrumbs before adding to event context.

    Breadcrumbs are the trail of events leading up to an error. This hook
    allows us to filter sensitive data and reduce noise.

    Args:
        crumb: Breadcrumb dictionary
        hint: Additional context

    Returns:
        Modified breadcrumb dict, or None to skip this breadcrumb

    Example breadcrumb structure:
        {
            "type": "http",
            "category": "httplib",
            "data": {"url": "...", "method": "GET"},
            "level": "info",
            "timestamp": 1234567890
        }
    """
    # Filter out noisy breadcrumbs
    if crumb.get("category") == "httplib" and crumb.get("type") == "http":
        # Skip health check requests
        url = crumb.get("data", {}).get("url", "")
        if "/health" in url:
            return None

    # Scrub PII from breadcrumb data
    if "data" in crumb:
        crumb["data"] = _scrub_pii_from_dict(crumb["data"])

    return crumb


def _scrub_pii_from_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Remove PII from request data.

    Scrubs:
    - Authorization headers
    - Cookies
    - Query parameters (if needed)
    - Form data (if needed)

    Args:
        request_data: Request data dictionary

    Returns:
        Scrubbed request data
    """
    scrubbed = request_data.copy()

    # Scrub headers
    if "headers" in scrubbed:
        headers = scrubbed["headers"]
        sensitive_headers = ["authorization", "cookie", "x-api-key", "x-auth-token"]
        for header in sensitive_headers:
            if header in headers:
                headers[header] = "[Filtered]"
            # Case-insensitive check
            for key in list(headers.keys()):
                if key.lower() in sensitive_headers:
                    headers[key] = "[Filtered]"

    # Scrub cookies
    if "cookies" in scrubbed:
        scrubbed["cookies"] = "[Filtered]"

    # Scrub query parameters (if they contain sensitive data)
    # For Knit-Wit, we don't have sensitive query params, but this is here for future use
    if "query_string" in scrubbed:
        # Could parse and filter specific params here if needed
        pass

    return scrubbed


def _scrub_pii_from_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively scrub PII from dictionary.

    Filters out common PII field names like:
    - email, password, token, secret, api_key, etc.

    Args:
        data: Dictionary to scrub

    Returns:
        Scrubbed dictionary
    """
    if not isinstance(data, dict):
        return data

    scrubbed = {}
    sensitive_keys = {
        "password", "passwd", "secret", "token", "api_key", "apikey",
        "access_token", "refresh_token", "authorization",
        "cookie", "session", "private_key", "credit_card", "ssn"
    }

    for key, value in data.items():
        # Check if key is sensitive (case-insensitive)
        # But only filter if the value is not a nested dict (to allow nested processing)
        if key.lower() in sensitive_keys and not isinstance(value, dict):
            scrubbed[key] = "[Filtered]"
        elif isinstance(value, dict):
            # Recursively scrub nested dicts
            scrubbed[key] = _scrub_pii_from_dict(value)
        elif isinstance(value, list):
            # Scrub list items if they're dicts
            scrubbed[key] = [
                _scrub_pii_from_dict(item) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            scrubbed[key] = value

    return scrubbed


def capture_exception(
    error: Exception,
    context: Optional[Dict[str, Any]] = None,
    level: str = "error",
    tags: Optional[Dict[str, str]] = None,
) -> Optional[str]:
    """
    Manually capture an exception with additional context.

    Use this in exception handlers when you want to add extra context
    beyond what automatic capture provides.

    Args:
        error: Exception instance to capture
        context: Additional context dictionary (added to event.extra)
        level: Severity level (debug, info, warning, error, fatal)
        tags: Tags to attach to event (for filtering/grouping)

    Returns:
        Event ID if sent, None if Sentry is disabled

    Example:
        >>> try:
        ...     risky_operation()
        ... except ValueError as e:
        ...     capture_exception(
        ...         e,
        ...         context={"user_input": data, "step": "validation"},
        ...         tags={"component": "pattern_generator"}
        ...     )
        ...     raise
    """
    with sentry_sdk.push_scope() as scope:
        # Set level
        scope.level = level

        # Add correlation ID from logging context
        correlation_id = get_correlation_id()
        if correlation_id:
            scope.set_tag("correlation_id", correlation_id)

        # Add custom tags
        if tags:
            for key, value in tags.items():
                scope.set_tag(key, value)

        # Add context as extra data
        if context:
            # Scrub PII from context
            scrubbed_context = _scrub_pii_from_dict(context)
            for key, value in scrubbed_context.items():
                scope.set_extra(key, value)

        # Capture exception
        event_id = sentry_sdk.capture_exception(error)

    return event_id


def capture_message(
    message: str,
    level: str = "info",
    context: Optional[Dict[str, Any]] = None,
    tags: Optional[Dict[str, str]] = None,
) -> Optional[str]:
    """
    Capture a message (not an exception) to Sentry.

    Use this for important events that aren't errors but should be tracked,
    like critical state changes or unusual conditions.

    Args:
        message: Message to send
        level: Severity level (debug, info, warning, error, fatal)
        context: Additional context dictionary
        tags: Tags to attach to event

    Returns:
        Event ID if sent, None if Sentry is disabled

    Example:
        >>> capture_message(
        ...     "Pattern generation took longer than expected",
        ...     level="warning",
        ...     context={"duration_ms": 5000, "shape": "sphere"},
        ...     tags={"performance": "slow"}
        ... )
    """
    with sentry_sdk.push_scope() as scope:
        # Set level
        scope.level = level

        # Add correlation ID
        correlation_id = get_correlation_id()
        if correlation_id:
            scope.set_tag("correlation_id", correlation_id)

        # Add custom tags
        if tags:
            for key, value in tags.items():
                scope.set_tag(key, value)

        # Add context
        if context:
            scrubbed_context = _scrub_pii_from_dict(context)
            for key, value in scrubbed_context.items():
                scope.set_extra(key, value)

        # Capture message
        event_id = sentry_sdk.capture_message(message, level=level)

    return event_id


def add_breadcrumb(
    message: str,
    category: str = "custom",
    level: str = "info",
    data: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Add a breadcrumb to the current scope.

    Breadcrumbs provide context about what happened before an error.
    They appear in Sentry event details chronologically.

    Args:
        message: Breadcrumb message
        category: Category for grouping (e.g., "http", "db", "auth")
        level: Severity level
        data: Additional structured data

    Example:
        >>> add_breadcrumb(
        ...     message="Pattern compilation started",
        ...     category="pattern_engine",
        ...     data={"shape": "sphere", "diameter": 10}
        ... )
    """
    sentry_sdk.add_breadcrumb(
        category=category,
        message=message,
        level=level,
        data=_scrub_pii_from_dict(data) if data else None,
    )


def set_user_context(user_id: Optional[str] = None, **kwargs: Any) -> None:
    """
    Set user context for error tracking.

    This associates errors with specific users (if applicable).
    For MVP, Knit-Wit has no user accounts, so this is for future use.

    Args:
        user_id: User identifier (hashed/anonymized)
        **kwargs: Additional user fields (email, username, etc.)

    Example:
        >>> set_user_context(user_id="user_abc123", subscription="free")
    """
    user_data = {}
    if user_id:
        user_data["id"] = user_id
    user_data.update(kwargs)

    sentry_sdk.set_user(user_data)


def clear_user_context() -> None:
    """Clear user context from current scope."""
    sentry_sdk.set_user(None)
