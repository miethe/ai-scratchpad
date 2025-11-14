"""
Correlation ID middleware for request tracing.

Adds a unique correlation ID to each request for tracking across
logs and error tracking systems (Sentry).
"""

import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging_config import set_correlation_id, clear_correlation_id


class CorrelationIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add correlation IDs to requests.

    This middleware:
    1. Generates a unique correlation ID for each request
    2. Sets it in the logging context
    3. Adds it to the response headers
    4. Automatically cleans up after request completes

    The correlation ID is available to:
    - Structured logs (via logging_config)
    - Sentry events (via sentry_config)
    - Response headers (for client-side tracing)
    """

    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        """
        Process request with correlation ID.

        Args:
            request: Incoming HTTP request
            call_next: Next middleware/route handler

        Returns:
            HTTP response with correlation ID header
        """
        # Check if client provided a correlation ID
        correlation_id = request.headers.get("X-Correlation-ID")

        # Generate new ID if not provided
        if not correlation_id:
            correlation_id = f"req_{uuid.uuid4().hex[:16]}"

        # Set correlation ID in logging context
        set_correlation_id(correlation_id)

        try:
            # Process request
            response = await call_next(request)

            # Add correlation ID to response headers
            response.headers["X-Correlation-ID"] = correlation_id

            return response
        finally:
            # Clean up correlation ID from context
            clear_correlation_id()
