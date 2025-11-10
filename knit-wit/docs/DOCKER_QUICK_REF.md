# Docker Quick Reference

One-page cheat sheet for Knit-Wit Docker development.

## Quick Start

```bash
# First time setup
cp .env.example .env
chmod +x docker-dev.sh

# Start development environment
./docker-dev.sh start-d

# Stop environment
./docker-dev.sh stop
```

## Common Commands

| Task | Command |
|------|---------|
| Start services (foreground) | `./docker-dev.sh start` |
| Start services (background) | `./docker-dev.sh start-d` |
| Stop services | `./docker-dev.sh stop` |
| View logs | `./docker-dev.sh logs` |
| Restart backend | `./docker-dev.sh rb` |
| Check status | `./docker-dev.sh status` |
| Connect to database | `./docker-dev.sh db` |
| Run tests | `./docker-dev.sh test` |
| Reset everything | `./docker-dev.sh reset` |

## Access Points

| Service | URL | Credentials |
|---------|-----|-------------|
| Backend API | http://localhost:8000 | - |
| API Docs | http://localhost:8000/docs | - |
| Health Check | http://localhost:8000/health | - |
| PostgreSQL | localhost:5432 | knitwit / knitwit_dev_pass |
| pgAdmin | http://localhost:5050 | admin@knitwit.local / admin |

## Development Workflow

```bash
# 1. Start environment
./docker-dev.sh start-d

# 2. Watch logs
./docker-dev.sh logs backend

# 3. Edit code in apps/api/app/
# (server auto-restarts on changes)

# 4. Test changes
curl http://localhost:8000/health

# 5. Run tests
./docker-dev.sh test

# 6. Stop when done
./docker-dev.sh stop
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 8000 in use | Change `BACKEND_PORT` in `.env` |
| Port 5432 in use | Change `POSTGRES_PORT` in `.env` |
| Container won't start | `./docker-dev.sh stop && ./docker-dev.sh rebuild` |
| Hot reload not working | `./docker-dev.sh rb` |
| Database connection error | Wait 10s for DB to initialize |
| Permission denied | Check Docker Desktop file sharing settings |

## Environment Variables (.env)

```bash
# Backend
BACKEND_PORT=8000
BACKEND_ENV=development
LOG_LEVEL=INFO

# Database
POSTGRES_USER=knitwit
POSTGRES_PASSWORD=knitwit_dev_pass
POSTGRES_DB=knitwit_dev
POSTGRES_PORT=5432

# CORS
CORS_ORIGINS=http://localhost:19006,http://localhost:8081
```

## Docker Compose (Manual)

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Restart service
docker-compose restart backend

# Rebuild
docker-compose up --build

# Stop
docker-compose down

# Reset (destroys data!)
docker-compose down -v

# Start with pgAdmin
docker-compose --profile tools up
```

## Database

```bash
# Connect via psql
./docker-dev.sh db
# or: docker-compose exec db psql -U knitwit -d knitwit_dev

# Common psql commands
\dt              # List tables
\d+ table_name   # Describe table
\l               # List databases
\q               # Quit

# Backup database
docker-compose exec db pg_dump -U knitwit knitwit_dev > backup.sql

# Restore database
cat backup.sql | docker-compose exec -T db psql -U knitwit -d knitwit_dev
```

## Health Checks

```bash
# Check service health
./docker-dev.sh health

# Or manually
docker inspect knitwit-backend --format='{{.State.Health.Status}}'
docker inspect knitwit-db --format='{{.State.Health.Status}}'

# Test API health
curl http://localhost:8000/health
```

## Logs

```bash
# All services
./docker-dev.sh logs

# Specific service
./docker-dev.sh logs backend
./docker-dev.sh logs db

# Last 50 lines
docker-compose logs --tail=50 backend

# Follow from specific time
docker-compose logs --since 30m -f backend
```

## Testing

```bash
# Run all tests
./docker-dev.sh test

# Run specific test file
docker-compose exec backend pytest tests/test_health.py

# With coverage
docker-compose exec backend pytest --cov=app --cov-report=term

# Watch mode
docker-compose exec backend pytest --watch
```

## Linting & Formatting

```bash
# Format code
docker-compose exec backend black app tests
docker-compose exec backend isort app tests

# Check linting
docker-compose exec backend ruff app tests

# Type checking
docker-compose exec backend mypy app

# All at once
./docker-dev.sh lint
```

## Shell Access

```bash
# Backend container
./docker-dev.sh shell
# or: docker-compose exec backend sh

# Database container
./docker-dev.sh shell db
# or: docker-compose exec db sh

# Run Python REPL
docker-compose exec backend python
```

## Cleanup

```bash
# Remove stopped containers
docker-compose down

# Remove volumes (data loss!)
docker-compose down -v

# Clean Docker system
./docker-dev.sh clean

# Nuclear option (all Docker data)
docker system prune -a --volumes
```

## Port Mapping

| Container Port | Host Port | Service |
|----------------|-----------|---------|
| 8000 | 8000 (configurable) | Backend API |
| 5432 | 5432 (configurable) | PostgreSQL |
| 80 | 5050 (configurable) | pgAdmin |

## Volume Mounts

| Host Path | Container Path | Purpose |
|-----------|----------------|---------|
| `./apps/api/app` | `/app/app` | Source code (hot-reload) |
| `./apps/api/tests` | `/app/tests` | Test files |
| `postgres-data` | `/var/lib/postgresql/data` | Database storage |

## Service Dependencies

```
backend depends_on db (health check)
pgadmin depends_on db
```

## Profiles

| Profile | Services | Command |
|---------|----------|---------|
| default | backend, db | `docker-compose up` |
| tools | backend, db, pgadmin | `docker-compose --profile tools up` |

## Useful One-Liners

```bash
# Check if services are healthy
docker-compose ps | grep healthy

# Follow backend logs for errors
docker-compose logs -f backend | grep ERROR

# Check database connections
docker-compose exec db psql -U knitwit -d knitwit_dev -c "SELECT count(*) FROM pg_stat_activity;"

# Tail last 20 API requests
docker-compose logs --tail=20 backend | grep "GET\|POST"

# Watch resource usage
docker stats knitwit-backend knitwit-db

# Force rebuild backend
docker-compose build --no-cache backend

# Export database schema
docker-compose exec db pg_dump -U knitwit -d knitwit_dev --schema-only > schema.sql
```

## Help

```bash
# Helper script help
./docker-dev.sh help

# Docker Compose help
docker-compose --help

# Service-specific help
docker-compose help up
docker-compose help logs
```

## Further Reading

- Full Documentation: `docs/DOCKER.md`
- Main README: `README.md`
- API Documentation: http://localhost:8000/docs
