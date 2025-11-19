"""API v1 router configuration."""

from fastapi import APIRouter

from app.core import settings
from app.api.v1.endpoints import visualization, parser, export, telemetry, patterns

# Create main v1 router
api_router = APIRouter()

# Include endpoint routers
api_router.include_router(patterns.router)
api_router.include_router(visualization.router)
api_router.include_router(parser.router)
api_router.include_router(export.router)
api_router.include_router(telemetry.router)

__all__ = ["api_router"]
