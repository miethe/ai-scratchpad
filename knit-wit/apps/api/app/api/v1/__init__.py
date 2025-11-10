"""API v1 router configuration."""

from fastapi import APIRouter

from app.core import settings

# Create main v1 router
api_router = APIRouter()

# Import and include endpoint routers here
# Example: from app.api.v1.endpoints import health
# api_router.include_router(health.router, tags=["health"])

__all__ = ["api_router"]
