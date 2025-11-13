"""
Core configuration module for Knit-Wit API.

This module handles all application settings using Pydantic Settings,
loading configuration from environment variables with sensible defaults.
"""

from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    All settings can be overridden via .env file or environment variables.
    Pydantic will automatically handle type conversion and validation.
    """

    # Application metadata
    app_name: str = Field(default="Knit-Wit API", description="Application name")
    app_version: str = Field(default="0.1.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")

    # Server configuration
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")

    # CORS configuration
    cors_origins: List[str] = Field(
        default=[
            "http://localhost:3000",  # Frontend dev server
            "http://localhost:19006",  # Expo dev server
            "http://localhost:8081",   # Expo alternative port
        ],
        description="Allowed CORS origins"
    )
    cors_credentials: bool = Field(default=True, description="Allow credentials in CORS")
    cors_methods: List[str] = Field(default=["*"], description="Allowed HTTP methods")
    cors_headers: List[str] = Field(default=["*"], description="Allowed HTTP headers")

    # API configuration
    api_v1_prefix: str = Field(default="/api/v1", description="API v1 route prefix")

    # Logging configuration
    log_level: str = Field(default="INFO", description="Logging level")
    log_dir: str = Field(
        default="logs/telemetry",
        description="Directory for log files"
    )
    log_retention_days: int = Field(
        default=90,
        description="Number of days to retain log files"
    )
    log_enable_console: bool = Field(
        default=True,
        description="Enable console logging (in addition to file logging)"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: str | List[str]) -> List[str]:
        """Parse CORS origins from comma-separated string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level is one of the standard levels."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(f"Log level must be one of: {', '.join(valid_levels)}")
        return v_upper


# Global settings instance
settings = Settings()
