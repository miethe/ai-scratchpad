# Knit-Wit API

FastAPI backend for the Knit-Wit crochet pattern generator.

**Status**: MVP v1.0 (Production Ready)
**Language**: Python 3.11+
**Framework**: FastAPI 0.104+
**API Version**: v0.1.0

## Quick Links

- **[Full API Documentation](../../docs/api/README.md)** - Complete API reference with examples
- **[Technical Architecture](../../project_plans/mvp/supporting-docs/technical-architecture.md)** - System design
- **[Testing Strategy](../../project_plans/mvp/supporting-docs/testing-strategy.md)** - Test approach
- **[DSL Specification](../../docs/dsl-specification.md)** - Pattern data format
- **[Main README](../../README.md)** - Project overview and setup

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

## Architecture

### Layered Architecture Pattern

**Routes → Services → Pattern Engine**

```
HTTP Request
    ↓
Routes Layer (app/api/v1/endpoints/)
    - Handle HTTP request/response
    - Pydantic validation
    - OpenAPI schema generation
    ↓
Services Layer (app/services/)
    - Business logic orchestration
    - Error handling and logging
    - Call pattern engine
    ↓
Pattern Engine (packages/pattern-engine/)
    - Pure Python, no framework dependencies
    - Deterministic algorithms
    - Fully testable in isolation
    ↓
HTTP Response
```

### Key Principles

- **Separation of concerns**: Routes handle HTTP, services orchestrate, engine computes
- **Stateless**: No database in MVP (planned for v1.1)
- **API-first**: Backend provides clean REST API; frontend is one client
- **Error handling**: Multi-layer validation and consistent error responses
- **Logging**: Structured logs with correlation IDs for tracing

## Development Standards

### Code Style

- **Black**: Auto-formatting (run `black app tests`)
- **isort**: Import sorting (run `isort app tests`)
- **Ruff**: Linting (run `ruff check app tests`)
- **mypy**: Type checking (run `mypy app`)

Run all checks:
```bash
black app tests && isort app tests && ruff check app tests && mypy app
```

### Testing

- **Unit tests**: Test pure functions in isolation
- **Integration tests**: Test API contracts and data flow
- **Coverage goal**: 60%+ overall, 80%+ for critical paths

```bash
# Run tests with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_main.py

# Run in watch mode (with pytest-watch)
ptw
```

### Type Safety

- All function parameters must have type hints
- All function return values must have type hints
- Use specific types, not `Any` (use `Union` for multiple types)
- Pydantic models for all request/response validation

**Example:**
```python
async def generate_pattern(
    request: PatternGenerationRequest,
    db: Session = Depends(get_db)
) -> PatternGenerationResponse:
    """Generate a crochet pattern based on parameters."""
    service = PatternService(db)
    return await service.generate(request)
```

## API Endpoint Development

### Adding a New Endpoint

1. **Create Pydantic models** in `app/models/`
   ```python
   from pydantic import BaseModel, Field

   class MyRequest(BaseModel):
       shape: str = Field(..., description="Shape type")
       diameter: float = Field(..., gt=0, description="Diameter in cm")
   ```

2. **Create service logic** in `app/services/`
   ```python
   class MyService:
       async def process(self, request: MyRequest) -> MyResponse:
           # Business logic here
           return response
   ```

3. **Create route handler** in `app/api/v1/endpoints/`
   ```python
   @router.post("/my-endpoint", response_model=MyResponse)
   async def my_endpoint(
       request: MyRequest,
       service: MyService = Depends()
   ) -> MyResponse:
       return await service.process(request)
   ```

4. **Test the endpoint** in `tests/`
   ```bash
   pytest tests/test_my_endpoint.py
   ```

5. **Document the endpoint** in `docs/api/api-contract.md`

### Error Handling

Always return consistent error responses:

```python
from app.core.errors import ValidationError

try:
    result = service.process(request)
except ValueError as e:
    raise ValidationError(
        field="parameter_name",
        message=str(e)
    )
```

Error format:
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid gauge parameters",
    "details": {
      "field": "gauge.stitches_per_cm",
      "constraint": "must be between 6 and 25"
    }
  }
}
```

## Pattern Engine Integration

### Using the Pattern Engine

```python
from knit_wit_engine import compile_sphere, PatternRequest

request = PatternRequest(
    shape_type="sphere",
    diameter_cm=10.0,
    gauge={"sts_per_10cm": 14, "rows_per_10cm": 16}
)

pattern_dsl = compile_sphere(request)
```

### Understanding DSL v0.1

The Pattern DSL is JSON-based and includes:

- **Meta**: Gauge, units, stitch type, terminology
- **Object**: Shape type and parameters
- **Rounds**: List of rounds with operations per round
- **Materials**: Yarn and hook information
- **Notes**: Pattern-specific guidance

See `docs/dsl-specification.md` for complete format.

## Performance Optimization

### API Response Times

- Generation: <200ms (p95)
- Visualization: <100ms per frame
- Exports: <2s (PDF), <500ms (SVG/PNG)

### Optimization Techniques

1. **Caching**: Results are deterministic (same input = same output)
   - Future: Redis caching for distributed deployments

2. **Async processing**: Use async/await for all I/O
   ```python
   async def fetch_data():
       # Non-blocking operations
       result = await external_api.call()
       return result
   ```

3. **Connection pooling**: Database connections reused
   - Future: When database is added in v1.1

4. **Resource limits**: Prevent unreasonable requests
   - Max stitch count: ~2000 per round
   - Generation timeout: 30 seconds

## Monitoring & Debugging

### Logging

Structured logs with correlation ID:

```python
import logging

logger = logging.getLogger(__name__)

logger.info(
    "Pattern generated",
    extra={
        "correlation_id": correlation_id,
        "shape": "sphere",
        "duration_ms": 150
    }
)
```

Check logs:
```bash
# With Docker
docker-compose logs -f backend

# Locally
tail -f logs/app.log
```

### Error Tracking with Sentry

Sentry automatically captures exceptions. For manual reporting:

```python
from app.core import capture_exception, capture_message

try:
    risky_operation()
except Exception as e:
    capture_exception(
        e,
        context={"user_input": data},
        tags={"component": "generation"}
    )
```

### Health Checks

Check API health:
```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

## Deployment

### Production Build

```bash
docker build -t knit-wit-api:latest \
  --target production \
  .
```

### Environment Variables

See `.env.example` for all configurable options.

Critical variables for production:
- `BACKEND_ENV=production`
- `DEBUG=false`
- `SENTRY_DSN=<your-sentry-dsn>`
- `SENTRY_ENABLED=true`

## Contributing

1. **Follow code standards**: Black, isort, ruff, mypy
2. **Write tests**: Unit + integration tests required
3. **Update documentation**: Update API docs if endpoint changes
4. **Commit conventionally**: Use conventional commit format
5. **Request review**: Code review required before merge

## Troubleshooting

### "Module not found" errors

```bash
# Reinstall dependencies
uv pip install -e ".[dev]"

# Or with pip directly
pip install -e ".[dev]"
```

### Type checking failures

```bash
# Check all type issues
mypy app --show-error-codes

# Fix specific module
mypy app/services/pattern_service.py
```

### Tests failing

```bash
# Run with verbose output
pytest -vv tests/

# Run single test file
pytest tests/test_main.py

# Run with coverage
pytest --cov=app tests/
```

### Server won't start

```bash
# Check syntax
python -m py_compile app/main.py

# Run with traceback
python -m uvicorn app.main:app --reload
```

## License

Part of the Knit-Wit project. See repository root for details.
