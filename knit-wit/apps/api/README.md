# Knit-Wit API

FastAPI backend for the Knit-Wit crochet pattern generator.

## Setup

This project uses [uv](https://github.com/astral-sh/uv) for fast, reliable Python dependency management.

### Prerequisites

- Python 3.11+
- uv package manager

### Installation

1. Create and activate virtual environment:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
uv pip install -e ".[dev]"
```

### Development

Start the development server with hot-reload:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### API Documentation

Once the server is running, access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

### Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

## Project Structure

```
apps/api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── endpoints/   # API endpoint modules
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py        # Configuration and settings
│   └── models/
│       └── __init__.py      # Pydantic models
├── tests/
│   └── __init__.py
├── Dockerfile               # Production container image
├── pyproject.toml           # Project metadata and dependencies
└── README.md
```

## Architecture

The API follows a layered architecture pattern:
- **Routers**: Handle HTTP requests and responses (in `api/v1/endpoints/`)
- **Services**: Business logic layer (to be implemented)
- **Repositories**: Data access layer (to be implemented)

## Environment Variables

Copy `.env.example` to `.env` and configure:

```env
# Application
APP_NAME=Knit-Wit API
APP_VERSION=0.1.0
DEBUG=true

# Server
HOST=0.0.0.0
PORT=8000

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:19006

# Logging
LOG_LEVEL=INFO
LOG_DIR=logs/telemetry
LOG_RETENTION_DAYS=90
LOG_ENABLE_CONSOLE=true

# Error Tracking (Sentry)
SENTRY_DSN=                          # Your Sentry DSN from sentry.io
SENTRY_ENVIRONMENT=development       # development, staging, or production
SENTRY_TRACES_SAMPLE_RATE=0.1       # 0.0 to 1.0 (10% of transactions)
SENTRY_ENABLED=true                  # Set to false to disable Sentry
```

## Error Tracking with Sentry

The API uses [Sentry](https://sentry.io) for production error tracking and monitoring.

### Setup Sentry

1. **Create a Sentry Account**
   - Go to [sentry.io](https://sentry.io) and create a free account
   - Create a new project for "Python" / "FastAPI"

2. **Get Your DSN**
   - Navigate to Project Settings → Client Keys (DSN)
   - Copy your DSN (looks like: `https://examplePublicKey@o0.ingest.sentry.io/0`)

3. **Configure Environment**
   ```bash
   # In your .env file
   SENTRY_DSN=https://your-dsn@sentry.io/project-id
   SENTRY_ENVIRONMENT=development
   SENTRY_ENABLED=true
   ```

4. **Test Error Tracking**
   - Start the API server
   - Trigger an error (e.g., invalid API request)
   - Check Sentry dashboard for captured error

### Features

- **Automatic Exception Capture**: All unhandled exceptions are automatically sent to Sentry
- **Stack Traces**: Full stack traces with local variables
- **Request Context**: Captures request URL, headers, and parameters
- **Correlation IDs**: Each request gets a unique ID for tracing through logs and errors
- **Breadcrumbs**: Trail of events leading up to an error
- **PII Filtering**: Automatically filters sensitive data (passwords, tokens, API keys)
- **Performance Monitoring**: Tracks slow API endpoints (configurable sample rate)

### Manual Error Reporting

Use Sentry helpers in your code for manual error tracking:

```python
from app.core import capture_exception, capture_message, add_breadcrumb

# Capture exception with context
try:
    risky_operation()
except ValueError as e:
    capture_exception(
        e,
        context={"user_input": data, "step": "validation"},
        tags={"component": "pattern_generator"}
    )
    raise

# Log important events
capture_message(
    "Pattern generation took longer than expected",
    level="warning",
    context={"duration_ms": 5000, "shape": "sphere"}
)

# Add breadcrumbs for context
add_breadcrumb(
    message="Starting PDF generation",
    category="export",
    data={"shape": "sphere", "paper_size": "A4"}
)
```

### Correlation IDs

Every request automatically gets a unique correlation ID that appears in:
- Response headers: `X-Correlation-ID`
- Structured logs: `correlation_id` field
- Sentry events: Tagged with correlation ID

You can provide your own correlation ID:
```bash
curl -H "X-Correlation-ID: my-custom-id" http://localhost:8000/api/v1/patterns
```

### Disabling Sentry

For local development or testing, disable Sentry:
```bash
# In .env
SENTRY_ENABLED=false

# Or remove/leave empty SENTRY_DSN
SENTRY_DSN=
```

Tests automatically disable Sentry via `tests/conftest.py`.

## Testing

Run tests with coverage:
```bash
pytest
```

Run specific test file:
```bash
pytest tests/test_main.py
```

## Code Quality

Format code:
```bash
black app tests
isort app tests
```

Lint code:
```bash
ruff check app tests
mypy app
```

## Docker

Build and run with Docker:
```bash
docker build -t knit-wit-api .
docker run -p 8000:8000 knit-wit-api
```

## License

Part of the Knit-Wit project.
