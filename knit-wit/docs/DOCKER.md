# Docker Development Environment

Complete guide to using Docker for Knit-Wit development.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Services](#services)
- [Configuration](#configuration)
- [Development Workflow](#development-workflow)
- [Database Management](#database-management)
- [Troubleshooting](#troubleshooting)
- [Production Deployment](#production-deployment)

## Overview

The Knit-Wit Docker Compose environment provides a complete development stack with:

- FastAPI backend with hot-reload
- PostgreSQL 15 database with persistent storage
- pgAdmin for database management (optional)
- Health checks and service dependencies
- Volume mounts for live code editing

## Prerequisites

- Docker Desktop 20.10+ or Docker Engine 20.10+
- Docker Compose 2.0+ (or `docker compose` plugin)
- At least 4GB RAM allocated to Docker
- Ports 8000 and 5432 available

### Installation

**macOS/Windows:**
- Download [Docker Desktop](https://www.docker.com/products/docker-desktop)

**Linux:**
```bash
# Install Docker Engine
curl -fsSL https://get.docker.com | sh

# Install Docker Compose plugin
sudo apt-get update
sudo apt-get install docker-compose-plugin

# Add user to docker group (logout/login required)
sudo usermod -aG docker $USER
```

## Quick Start

### Using the Helper Script (Recommended)

```bash
# Make script executable (first time only)
chmod +x docker-dev.sh

# Start development environment
./docker-dev.sh start-d

# View logs
./docker-dev.sh logs

# Stop environment
./docker-dev.sh stop
```

### Using Docker Compose Directly

```bash
# Create .env file
cp .env.example .env

# Start services
docker-compose up

# Start in background
docker-compose up -d

# Stop services
docker-compose down
```

## Architecture

### Service Diagram

```
┌─────────────────────────────────────┐
│         Docker Network              │
│         (knitwit-network)           │
│                                     │
│  ┌──────────────────────────────┐  │
│  │  Backend (knitwit-backend)   │  │
│  │  - FastAPI + uvicorn         │  │
│  │  - Port: 8000                │  │
│  │  - Hot-reload enabled        │  │
│  │  - Health check: /health     │  │
│  └──────────────┬───────────────┘  │
│                 │                   │
│                 │ connects to       │
│                 ▼                   │
│  ┌──────────────────────────────┐  │
│  │  Database (knitwit-db)       │  │
│  │  - PostgreSQL 15 Alpine      │  │
│  │  - Port: 5432                │  │
│  │  - Persistent volume         │  │
│  │  - Health check: pg_isready  │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │  pgAdmin (optional)          │  │
│  │  - Database UI               │  │
│  │  - Port: 5050                │  │
│  │  - Profile: tools            │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
```

### Volume Mounts

**Backend Service:**
```yaml
./apps/api/app → /app/app (read-only)
./apps/api/tests → /app/tests (read-only)
./apps/api/pyproject.toml → /app/pyproject.toml (read-only)
```

**Database Service:**
```yaml
postgres-data → /var/lib/postgresql/data (persistent)
./apps/api/scripts/init-db.sql → /docker-entrypoint-initdb.d/init.sql
```

## Services

### Backend (knitwit-backend)

**Purpose:** FastAPI application server with hot-reload for development.

**Key Features:**
- Built from `apps/api/Dockerfile` (development stage)
- Source code mounted as read-only volumes
- Environment variables from `.env`
- Health check every 30s on `/health` endpoint
- Depends on database being healthy

**Access:**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

### Database (knitwit-db)

**Purpose:** PostgreSQL database for pattern storage and user data (future).

**Key Features:**
- PostgreSQL 15 Alpine (lightweight)
- Persistent storage via Docker volume
- Health check via `pg_isready`
- Initialization script support

**Access:**
- Connection: `postgresql://knitwit:knitwit_dev_pass@localhost:5432/knitwit_dev`
- CLI: `docker-compose exec db psql -U knitwit -d knitwit_dev`

### pgAdmin (knitwit-pgadmin)

**Purpose:** Web-based database management UI (optional).

**Key Features:**
- Only starts with `--profile tools`
- Lightweight configuration
- Pre-configured for local development

**Access:**
- URL: http://localhost:5050
- Email: admin@knitwit.local
- Password: admin

## Configuration

### Environment Variables

Create `.env` from `.env.example`:

```bash
cp .env.example .env
```

**Backend Configuration:**
```bash
BACKEND_PORT=8000          # API server port
BACKEND_HOST=0.0.0.0       # Bind to all interfaces
BACKEND_ENV=development    # Environment mode
LOG_LEVEL=INFO             # Logging level
```

**Database Configuration:**
```bash
POSTGRES_USER=knitwit              # Database username
POSTGRES_PASSWORD=knitwit_dev_pass # Database password (change in production!)
POSTGRES_DB=knitwit_dev            # Database name
POSTGRES_PORT=5432                 # Database port
```

**CORS Configuration:**
```bash
CORS_ORIGINS=http://localhost:19006,http://localhost:8081
```

**pgAdmin Configuration:**
```bash
PGADMIN_EMAIL=admin@knitwit.local  # pgAdmin login email
PGADMIN_PASSWORD=admin             # pgAdmin login password
PGADMIN_PORT=5050                  # pgAdmin web UI port
```

### Port Customization

If default ports conflict with existing services:

```bash
# In .env file
BACKEND_PORT=8001
POSTGRES_PORT=5433
PGADMIN_PORT=5051
```

### Docker Compose Profiles

**Default profile** (no flag):
- Starts backend and database

**Tools profile** (`--profile tools`):
- Starts all default services plus pgAdmin

```bash
docker-compose --profile tools up
```

## Development Workflow

### Starting Development

```bash
# Option 1: Using helper script
./docker-dev.sh start-d

# Option 2: Using docker-compose
docker-compose up -d
```

### Making Code Changes

1. Edit files in `apps/api/app/`
2. Save changes
3. Watch server restart in logs:
   ```bash
   docker-compose logs -f backend
   ```
4. Test changes at http://localhost:8000

### Dependency Changes

If you modify `pyproject.toml`:

```bash
# Rebuild backend container
docker-compose up --build backend

# Or using helper script
./docker-dev.sh rebuild
```

### Running Tests

```bash
# Option 1: Inside container
docker-compose exec backend pytest

# Option 2: Using helper script
./docker-dev.sh test

# With coverage report
docker-compose exec backend pytest --cov=app --cov-report=html
```

### Running Linters

```bash
# Format code
docker-compose exec backend black app tests
docker-compose exec backend isort app tests

# Check linting
docker-compose exec backend ruff app tests

# Type checking
docker-compose exec backend mypy app

# Or use helper script for all linters
./docker-dev.sh lint
```

### Viewing Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f db

# Last 100 lines
docker-compose logs --tail=100 backend

# Using helper script
./docker-dev.sh logs backend
```

### Restarting Services

```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart backend

# Using helper script
./docker-dev.sh restart-backend
```

## Database Management

### Connecting via psql

```bash
# Interactive terminal
docker-compose exec db psql -U knitwit -d knitwit_dev

# Run single command
docker-compose exec db psql -U knitwit -d knitwit_dev -c "SELECT version();"

# Using helper script
./docker-dev.sh db
```

### Common psql Commands

```sql
\dt              -- List tables
\d+ table_name   -- Describe table
\l               -- List databases
\du              -- List users
\q               -- Quit
```

### Using pgAdmin

```bash
# Start with pgAdmin
docker-compose --profile tools up -d

# Or using helper script
./docker-dev.sh pgadmin
```

**Access pgAdmin:**
1. Open http://localhost:5050
2. Login: `admin@knitwit.local` / `admin`
3. Add server:
   - **Name:** Knit-Wit Dev
   - **Host:** `db` (service name)
   - **Port:** 5432
   - **Username:** knitwit
   - **Password:** knitwit_dev_pass
   - **Database:** knitwit_dev

### Backup and Restore

**Backup:**
```bash
# Dump database
docker-compose exec db pg_dump -U knitwit knitwit_dev > backup.sql

# Dump with compression
docker-compose exec db pg_dump -U knitwit knitwit_dev | gzip > backup.sql.gz
```

**Restore:**
```bash
# Restore from dump
cat backup.sql | docker-compose exec -T db psql -U knitwit -d knitwit_dev

# Restore from compressed dump
gunzip -c backup.sql.gz | docker-compose exec -T db psql -U knitwit -d knitwit_dev
```

### Reset Database

```bash
# Stop and remove volumes (DESTRUCTIVE!)
docker-compose down -v

# Start fresh
docker-compose up -d

# Or using helper script
./docker-dev.sh reset
```

## Troubleshooting

### Port Already in Use

**Problem:** `Error starting userland proxy: listen tcp4 0.0.0.0:8000: bind: address already in use`

**Solution:**
```bash
# Find process using the port
lsof -i :8000
lsof -i :5432

# Kill the process (replace PID)
kill -9 <PID>

# Or change port in .env
BACKEND_PORT=8001
POSTGRES_PORT=5433
```

### Container Won't Start

**Problem:** Service exits immediately or won't start.

**Solution:**
```bash
# Check logs
docker-compose logs backend
docker-compose logs db

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

### Database Connection Errors

**Problem:** Backend can't connect to database.

**Solution:**
```bash
# Check database is healthy
docker-compose ps

# Wait for database initialization (first run takes ~10-15 seconds)
docker-compose logs db | grep "database system is ready"

# Verify backend is connecting to correct host
docker-compose exec backend env | grep DATABASE_URL
# Should be: postgresql://knitwit:...@db:5432/...
#                                    ^^^ important!
```

### Hot Reload Not Working

**Problem:** Code changes don't trigger server restart.

**Solution:**
```bash
# Verify volume mounts
docker-compose config | grep -A 5 volumes

# Check if uvicorn reload is enabled
docker-compose logs backend | grep reload

# On Windows/Mac: Ensure file sharing is enabled in Docker Desktop
# Settings → Resources → File Sharing → Add project directory

# Force restart
docker-compose restart backend
```

### Permission Denied Errors

**Problem:** `Permission denied` when accessing files in container.

**Solution:**
```bash
# Check file ownership
ls -la apps/api/app

# Fix ownership (Linux only)
sudo chown -R $USER:$USER apps/api

# On Windows/Mac: Ensure Docker Desktop has proper permissions
```

### Health Check Failing

**Problem:** Service stuck in "starting" or "unhealthy" state.

**Solution:**
```bash
# Check health check status
docker inspect knitwit-backend --format='{{json .State.Health}}' | jq

# Test health endpoint manually
curl http://localhost:8000/health

# Check logs for errors
docker-compose logs backend

# Adjust health check timing if needed (in docker-compose.yml)
# - Increase start_period for slow machines
# - Increase interval for resource-constrained environments
```

### Out of Disk Space

**Problem:** `no space left on device`

**Solution:**
```bash
# Check Docker disk usage
docker system df

# Clean up unused resources
docker system prune -a --volumes

# Using helper script
./docker-dev.sh clean
```

### Slow Performance

**Problem:** Containers running slowly.

**Solution:**
```bash
# Increase Docker Desktop resources
# Settings → Resources → Advanced
# - CPUs: 2+ cores
# - Memory: 4GB+ RAM

# Check resource usage
docker stats

# Reduce logging verbosity
LOG_LEVEL=WARNING  # in .env

# Use production build for performance testing
docker build --target production ./apps/api
```

## Production Deployment

### Building Production Image

```bash
# Build production image
docker build \
  -t knitwit-api:1.0.0 \
  --target production \
  ./apps/api

# Test production image locally
docker run -d \
  -p 8000:8000 \
  -e BACKEND_ENV=production \
  -e DATABASE_URL=postgresql://... \
  knitwit-api:1.0.0
```

### Production Best Practices

1. **Environment Variables:**
   - Never use default passwords in production
   - Use secrets management (AWS Secrets Manager, HashiCorp Vault)
   - Set `BACKEND_ENV=production`

2. **Database:**
   - Use managed database service (AWS RDS, Google Cloud SQL)
   - Enable automated backups
   - Set up read replicas for scaling

3. **Security:**
   - Run containers as non-root user (already configured)
   - Use HTTPS/TLS for all connections
   - Enable network policies
   - Scan images for vulnerabilities: `docker scan knitwit-api:1.0.0`

4. **Monitoring:**
   - Enable health checks
   - Set up log aggregation (ELK, CloudWatch)
   - Configure alerts for service failures
   - Monitor resource usage

5. **Scaling:**
   - Use orchestration platform (Kubernetes, ECS, Cloud Run)
   - Enable horizontal pod autoscaling
   - Implement circuit breakers
   - Use load balancers

See `docs/deployment/` for platform-specific deployment guides.

## Advanced Topics

### Multi-Stage Build Optimization

The Dockerfile uses multi-stage builds for optimization:

```dockerfile
# base → builder → production (minimal)
# base → development (with dev tools)
```

Benefits:
- Smaller production images (no dev dependencies)
- Faster builds (layer caching)
- Security (fewer installed packages in production)

### Custom Networks

Services communicate via `knitwit-network` bridge network:

```bash
# Inspect network
docker network inspect knitwit_knitwit-network

# Connect another container
docker run --network knitwit_knitwit-network ...
```

### Volume Management

```bash
# List volumes
docker volume ls | grep knitwit

# Inspect volume
docker volume inspect knitwit_postgres-data

# Backup volume
docker run --rm \
  -v knitwit_postgres-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/postgres-backup.tar.gz /data

# Restore volume
docker run --rm \
  -v knitwit_postgres-data:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/postgres-backup.tar.gz -C /
```

## Helper Script Reference

The `docker-dev.sh` script provides convenient shortcuts:

```bash
./docker-dev.sh start          # Start services (foreground)
./docker-dev.sh start-d        # Start services (background)
./docker-dev.sh stop           # Stop services
./docker-dev.sh restart        # Restart all services
./docker-dev.sh rb             # Restart backend only
./docker-dev.sh logs [service] # View logs
./docker-dev.sh build          # Rebuild images
./docker-dev.sh rebuild        # Rebuild and start
./docker-dev.sh reset          # Reset environment (destructive!)
./docker-dev.sh clean          # Clean Docker system
./docker-dev.sh status         # Show service status
./docker-dev.sh health         # Check health status
./docker-dev.sh db             # Connect to database
./docker-dev.sh pgadmin        # Start with pgAdmin
./docker-dev.sh shell [db]     # Open shell in container
./docker-dev.sh test           # Run tests
./docker-dev.sh lint           # Run linters
./docker-dev.sh help           # Show help
```

## Further Reading

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Docker Deployment](https://fastapi.tiangolo.com/deployment/docker/)
- [PostgreSQL Docker Official Image](https://hub.docker.com/_/postgres)
- [Best practices for writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

## Support

For issues or questions:
- Check logs: `./docker-dev.sh logs`
- Review this documentation
- Check the [troubleshooting section](#troubleshooting)
- Consult the main project documentation
- Contact the development team
