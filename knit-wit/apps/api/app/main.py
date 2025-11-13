"""
Main FastAPI application entry point for Knit-Wit API.

This module initializes the FastAPI application with all necessary
middleware, routers, and lifecycle handlers.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1 import api_router
from app.core import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan handler for startup and shutdown events.

    This handles resource initialization on startup and cleanup on shutdown.
    """
    # Startup logic
    print(f"Starting {settings.app_name} v{settings.app_version}")
    print(f"Debug mode: {settings.debug}")
    print(f"CORS origins: {settings.cors_origins}")

    yield

    # Shutdown logic
    print(f"Shutting down {settings.app_name}")


# Initialize FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="FastAPI backend for parametric crochet pattern generation",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    debug=settings.debug,
    lifespan=lifespan,
    openapi_tags=[
        {"name": "health", "description": "Health check endpoints"},
        {"name": "root", "description": "Root API information"},
        {"name": "visualization", "description": "Pattern visualization endpoints"},
        {"name": "parser", "description": "Pattern text parsing endpoints"},
    ],
)


# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_credentials,
    allow_methods=settings.cors_methods,
    allow_headers=settings.cors_headers,
)


# Health check endpoint (root level, not versioned)
@app.get("/health", tags=["health"])
async def health_check() -> JSONResponse:
    """
    Health check endpoint.

    Returns the current health status of the API and version information.
    This endpoint is not versioned and should always be available.

    Returns:
        JSONResponse: Health status and version
    """
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "version": settings.app_version,
            "app_name": settings.app_name,
        },
    )


# Root endpoint
@app.get("/", tags=["root"])
async def root() -> JSONResponse:
    """
    Root endpoint providing API information.

    Returns:
        JSONResponse: API welcome message and documentation links
    """
    return JSONResponse(
        status_code=200,
        content={
            "message": f"Welcome to {settings.app_name}",
            "version": settings.app_version,
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health",
        },
    )


# Include API v1 router
app.include_router(api_router, prefix=settings.api_v1_prefix)


if __name__ == "__main__":
    """
    Entry point for running the application directly.

    For development, prefer using: uvicorn app.main:app --reload
    """
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
