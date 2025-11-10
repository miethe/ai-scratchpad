# Knit-Wit MVP

A mobile-first web application for generating parametric crochet patterns with interactive visualization.

## Project Overview

Knit-Wit generates clean, parametric crochet patterns for geometric shapes (sphere, cylinder, cone) and provides step-by-step interactive visualization with beginner-friendly guidance.

**Target Launch:** MVP completion before end of Q1 2025

## Tech Stack

- **Frontend:** React Native/Expo (mobile-first web app)
- **Backend:** FastAPI (Python 3.11+)
- **Pattern Engine:** Python library with parametric algorithms
- **Infrastructure:** pnpm workspaces, GitHub Actions, Docker

## Quick Start

### Prerequisites

- Node.js 18+
- pnpm 8+
- Python 3.11+
- Docker Desktop

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd knit-wit

# Install all dependencies
pnpm install

# Set up backend Python environment
cd apps/api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cd ../..
```

### Development

#### Option 1: Docker Compose (Recommended)

The easiest way to run the development environment:

```bash
# First time setup
cp .env.example .env
chmod +x docker-dev.sh

# Start all services using the helper script
./docker-dev.sh start-d

# View logs
./docker-dev.sh logs backend

# Stop all services
./docker-dev.sh stop

# See all available commands
./docker-dev.sh help
```

Alternatively, use Docker Compose directly:

```bash
# Start all services (backend + database)
docker-compose up

# Start in detached mode
docker-compose up -d

# Stop services
docker-compose down
```

Services will be available at:
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- PostgreSQL: localhost:5432
- pgAdmin (optional): http://localhost:5050 (use `docker-compose --profile tools up`)

**Hot-reload is enabled** - code changes in `apps/api/app/` will automatically restart the server.

#### Option 2: Local Development

Run services without Docker:

```bash
# Run all services
pnpm dev

# Run mobile app only
pnpm dev:mobile

# Run API only
pnpm dev:api
```

### Testing

```bash
# Run all tests
pnpm test

# Run mobile tests
pnpm test:mobile

# Run API tests
pnpm test:api

# Run pattern engine tests
pnpm test:engine
```

### Build

```bash
# Build all apps
pnpm build

# Type checking
pnpm typecheck

# Linting
pnpm lint

# Formatting
pnpm format
```

## Docker Development Environment

### Architecture

The Docker Compose setup includes:

- **backend**: FastAPI application with hot-reload enabled
- **db**: PostgreSQL 15 database with persistent storage
- **pgadmin**: Database management UI (optional, use `--profile tools`)

### Configuration

Environment variables are managed through `.env` file:

```bash
# Create your local .env from the example
cp .env.example .env

# Edit values as needed (defaults are suitable for development)
nano .env
```

Key variables for Docker:
- `BACKEND_PORT`: Backend API port (default: 8000)
- `POSTGRES_USER`: Database username (default: knitwit)
- `POSTGRES_PASSWORD`: Database password (default: knitwit_dev_pass)
- `POSTGRES_DB`: Database name (default: knitwit_dev)
- `POSTGRES_PORT`: Database port (default: 5432)

### Common Commands

```bash
# Start all services
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f
docker-compose logs -f backend
docker-compose logs -f db

# Restart a service
docker-compose restart backend

# Rebuild after dependency changes
docker-compose up --build

# Stop all services
docker-compose down

# Stop and remove all data (reset database)
docker-compose down -v

# Start with pgAdmin for database management
docker-compose --profile tools up
```

### Hot Reload

Hot-reload is enabled for the backend service:

1. Edit files in `apps/api/app/`
2. Save your changes
3. The server automatically restarts (watch logs: `docker-compose logs -f backend`)

If dependencies change (`pyproject.toml`), rebuild the container:
```bash
docker-compose up --build backend
```

### Health Checks

All services include health checks:

```bash
# Check service status
docker-compose ps

# Inspect health status
docker inspect knitwit-backend --format='{{.State.Health.Status}}'
docker inspect knitwit-db --format='{{.State.Health.Status}}'
```

Services will show as `healthy` when ready.

### Accessing Services

- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **PostgreSQL**: `postgresql://knitwit:knitwit_dev_pass@localhost:5432/knitwit_dev`
- **pgAdmin**: http://localhost:5050 (if started with `--profile tools`)

### Database Management

#### Using psql

```bash
# Connect to database via Docker
docker-compose exec db psql -U knitwit -d knitwit_dev

# Run SQL commands
\dt  # List tables
\q   # Quit
```

#### Using pgAdmin

```bash
# Start pgAdmin
docker-compose --profile tools up -d

# Access at http://localhost:5050
# Email: admin@knitwit.local
# Password: admin

# Add server connection:
# Host: db
# Port: 5432
# Username: knitwit
# Password: knitwit_dev_pass
```

### Troubleshooting

#### Port Already in Use

If ports 8000 or 5432 are already in use:

```bash
# Option 1: Stop conflicting services
# Check what's using the port
lsof -i :8000
lsof -i :5432

# Option 2: Change ports in .env
BACKEND_PORT=8001
POSTGRES_PORT=5433
```

#### Container Won't Start

```bash
# Check logs
docker-compose logs backend
docker-compose logs db

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

#### Database Connection Errors

```bash
# Wait for database to be healthy
docker-compose ps

# Database takes ~10 seconds to initialize on first run
# Check health status
docker-compose logs db | grep "database system is ready"
```

#### Hot Reload Not Working

```bash
# Ensure volumes are mounted correctly
docker-compose config

# Check if file changes are detected (watch logs)
docker-compose logs -f backend

# On Windows/Mac, ensure Docker Desktop has proper file sharing permissions
```

### Production Builds

For production deployments, use the production stage:

```bash
# Build production image
docker build -t knitwit-api:latest \
  --target production \
  ./apps/api

# Run production container
docker run -d \
  -p 8000:8000 \
  -e BACKEND_ENV=production \
  knitwit-api:latest
```

See `docs/deployment/` for detailed deployment guides.

## Repository Structure

```
knit-wit/
├── apps/
│   ├── mobile/          # React Native/Expo frontend
│   └── api/             # FastAPI backend
├── packages/
│   └── pattern-engine/  # Shared Python library for pattern generation
├── docs/                # Technical documentation
├── .github/             # CI/CD workflows
├── project_plans/       # Planning artifacts
├── docker-compose.yml   # Local dev environment
├── package.json         # Root workspace config
└── pnpm-workspace.yaml  # Workspace definitions
```

## Documentation

- [Product Requirements](./project_plans/mvp/prd.md)
- [Implementation Plan](./project_plans/mvp/implementation-plan-overview.md)
- [Phase 0 Plan](./project_plans/mvp/phases/phase-0.md)
- [Technical Architecture](./project_plans/mvp/supporting-docs/technical-architecture.md)
- [Testing Strategy](./project_plans/mvp/supporting-docs/testing-strategy.md)
- [DevOps & Infrastructure](./project_plans/mvp/supporting-docs/devops-infrastructure.md)

## Development Workflow

See [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed contribution guidelines.

## License

MIT License - see [LICENSE](./LICENSE) for details.

## Contact

For questions or clarifications, contact the Development Team.
