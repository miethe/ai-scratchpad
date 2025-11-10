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
```

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
