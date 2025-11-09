# Multi-stage Dockerfile for Knit-Wit API
# Uses uv for fast, reliable dependency installation

# Stage 1: Base image with Python and uv
FROM python:3.11-slim AS base

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1

# Set working directory
WORKDIR /app

# Stage 2: Dependencies installation
FROM base AS builder

# Copy dependency files
COPY pyproject.toml README.md ./

# Install dependencies to system Python (UV_SYSTEM_PYTHON=1)
RUN uv pip install --no-cache .

# Stage 3: Production image
FROM base AS production

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY ./app /app/app

# Create non-root user for security
RUN useradd -m -u 1000 apiuser && \
    chown -R apiuser:apiuser /app

# Switch to non-root user
USER apiuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Stage 4: Development image (with hot-reload)
FROM base AS development

# Copy dependency files
COPY pyproject.toml README.md ./

# Install dependencies including dev dependencies
RUN uv pip install --no-cache -e ".[dev]"

# Copy application code
COPY ./app /app/app
COPY ./tests /app/tests

# Expose port
EXPOSE 8000

# Run with hot-reload
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
