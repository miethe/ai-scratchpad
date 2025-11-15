"""
Pytest configuration and shared fixtures for Knit-Wit API tests.

This module provides:
- Test environment configuration
- Shared fixtures
- Sentry disabling for tests
"""

import os
import pytest
from typing import Generator


@pytest.fixture(scope="session", autouse=True)
def disable_sentry_for_tests() -> Generator[None, None, None]:
    """
    Disable Sentry error tracking during tests.

    This fixture runs automatically for all tests and ensures
    Sentry is disabled to prevent test errors from being reported
    to production Sentry projects.

    Scope: session (runs once for entire test session)
    Autouse: True (automatically applied to all tests)
    """
    # Save original environment variables
    original_sentry_enabled = os.environ.get("SENTRY_ENABLED")
    original_sentry_dsn = os.environ.get("SENTRY_DSN")

    # Disable Sentry for tests
    os.environ["SENTRY_ENABLED"] = "false"
    os.environ["SENTRY_DSN"] = ""

    yield

    # Restore original environment variables
    if original_sentry_enabled is not None:
        os.environ["SENTRY_ENABLED"] = original_sentry_enabled
    else:
        os.environ.pop("SENTRY_ENABLED", None)

    if original_sentry_dsn is not None:
        os.environ["SENTRY_DSN"] = original_sentry_dsn
    else:
        os.environ.pop("SENTRY_DSN", None)


@pytest.fixture(scope="function")
def mock_sentry_enabled() -> Generator[None, None, None]:
    """
    Temporarily enable Sentry for specific tests.

    Use this fixture when you want to test Sentry integration
    without actually sending events to Sentry.

    Example:
        >>> def test_sentry_capture(mock_sentry_enabled):
        ...     # Sentry is enabled but mocked for this test
        ...     pass
    """
    original_enabled = os.environ.get("SENTRY_ENABLED")

    os.environ["SENTRY_ENABLED"] = "true"
    os.environ["SENTRY_DSN"] = "https://test@sentry.io/0"

    yield

    if original_enabled is not None:
        os.environ["SENTRY_ENABLED"] = original_enabled
    else:
        os.environ.pop("SENTRY_ENABLED", None)
