# DevOps & Infrastructure

## Overview

This document defines the DevOps practices, infrastructure setup, and operational procedures for the Knit-Wit MVP. It covers environment configuration, CI/CD pipelines, containerization, deployment strategies, monitoring, security, and disaster recovery.

### Infrastructure Philosophy

- **Simplicity First**: Use managed services and simple deployment solutions appropriate for MVP scale
- **Automation**: Automate builds, tests, and deployments to reduce manual errors
- **Observability**: Structured logging, error tracking, and performance monitoring from day one
- **Security by Default**: Secrets management, dependency scanning, HTTPS/TLS enforcement
- **Cost-Effective**: Balance infrastructure costs with reliability needs for MVP scale

### Environment Strategy

The Knit-Wit MVP uses three environments:

1. **Local Development**: Docker Compose for backend; native mobile development
2. **Staging**: Cloud-hosted environment for integration testing and QA
3. **Production**: Cloud-hosted production environment with monitoring and backups

### Related Documents

- [Implementation Plan](../implementation-plan.md) - Full MVP implementation details
- [Phase 0: Foundation](../phases/phase-0.md) - Initial infrastructure setup
- [Testing Strategy](../implementation-plan.md#testing-strategy) - QA and testing approach

---

## Environment Setup

### Local Development Environment

Local development uses Docker Compose for the backend API and native tooling for React Native mobile development.

**docker-compose.yml**

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build:
      context: apps/api
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - ENV=development
      - LOG_LEVEL=DEBUG
      - CORS_ORIGINS=http://localhost:19006,http://localhost:19000
    volumes:
      - ./apps/api:/app
      - /app/__pycache__  # Exclude cache
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  postgres:
    # Optional: PostgreSQL for future versions
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=knitwit
      - POSTGRES_USER=dev
      - POSTGRES_PASSWORD=dev
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U dev"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

**Starting Local Environment**

```bash
# Start backend
docker-compose up

# In another terminal, start mobile app
cd apps/mobile
pnpm expo start
# Press 'i' for iOS simulator, 'a' for Android emulator
```

**Environment Variables (.env.example)**

```bash
# Backend API (.env.example in apps/api/)
ENV=development
LOG_LEVEL=DEBUG
CORS_ORIGINS=http://localhost:19006,http://localhost:19000
API_HOST=0.0.0.0
API_PORT=8000

# Future: Database
DATABASE_URL=postgresql://dev:dev@postgres:5432/knitwit

# Future: Authentication
JWT_SECRET=your-secret-key-here

# Monitoring (optional in dev)
SENTRY_DSN=
```

```bash
# Mobile App (.env.example in apps/mobile/)
EXPO_PUBLIC_API_URL=http://localhost:8000
EXPO_PUBLIC_ENV=development
EXPO_PUBLIC_SENTRY_DSN=
```

### Staging Environment

Staging replicates production configuration with test data and verbose logging.

**Platform Options:**
- Render.com (Recommended for MVP)
- Railway.app
- Fly.io
- Heroku

**Configuration:**
- Uses same Dockerfile as production
- Environment: `ENV=staging`
- Verbose logging: `LOG_LEVEL=INFO`
- Automated deployment on merge to `main` branch
- Test data loaded on deployment
- Protected by basic HTTP auth or IP whitelist

**Environment Variables (Staging)**

```bash
ENV=staging
LOG_LEVEL=INFO
CORS_ORIGINS=https://staging.knitwit.app
DATABASE_URL=postgresql://user:pass@staging-db.provider.com:5432/knitwit
SENTRY_DSN=https://xxx@sentry.io/xxx
SENTRY_ENVIRONMENT=staging
```

### Production Environment

Production environment with minimal logging, full monitoring, and backups.

**Configuration:**
- Environment: `ENV=production`
- Minimal logging: `LOG_LEVEL=WARNING`
- Full monitoring and alerting enabled
- Automated daily backups
- Manual deployment approval required

**Environment Variables (Production)**

```bash
ENV=production
LOG_LEVEL=WARNING
CORS_ORIGINS=https://app.knitwit.com
DATABASE_URL=postgresql://user:pass@prod-db.provider.com:5432/knitwit
SENTRY_DSN=https://xxx@sentry.io/xxx
SENTRY_ENVIRONMENT=production
SENTRY_TRACES_SAMPLE_RATE=0.1
```

### Secrets Management

**Development:**
- `.env` files (never committed)
- `.env.example` templates committed to repo

**Staging/Production:**
- Environment variables via cloud provider dashboard
- Secrets stored in:
  - GitHub Secrets (for CI/CD)
  - Cloud provider secret management (Render, Railway, etc.)
  - Future: AWS Secrets Manager, Vault, or similar

**Secret Rotation:**
- API keys rotated quarterly
- Database credentials rotated on security events
- JWT secrets rotated after security incidents

---

## CI/CD Pipeline

### GitHub Actions Workflows

The CI/CD pipeline uses GitHub Actions with separate workflows for testing and deployment.

#### Test Workflow

**`.github/workflows/test.yml`**

```yaml
name: Test

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main, develop]

jobs:
  lint-and-test-backend:
    name: Backend Lint & Test
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'
          cache-dependency-path: 'apps/api/requirements.txt'

      - name: Install dependencies
        run: |
          cd apps/api
          pip install -r requirements.txt

      - name: Lint with Black
        run: |
          cd apps/api
          black --check .

      - name: Lint with isort
        run: |
          cd apps/api
          isort --check-only .

      - name: Type check with mypy
        run: |
          cd apps/api
          mypy app/

      - name: Run tests
        run: |
          cd apps/api
          pytest --cov=app --cov-report=xml --cov-report=term

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./apps/api/coverage.xml
          flags: backend
          name: backend-coverage

  lint-and-test-frontend:
    name: Frontend Lint & Test
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node 18
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'pnpm'
          cache-dependency-path: 'apps/mobile/pnpm-lock.yaml'

      - name: Install pnpm
        run: npm install -g pnpm

      - name: Install dependencies
        run: |
          cd apps/mobile
          pnpm install --frozen-lockfile

      - name: Lint
        run: |
          cd apps/mobile
          pnpm lint

      - name: Type check
        run: |
          cd apps/mobile
          pnpm typecheck

      - name: Run tests
        run: |
          cd apps/mobile
          pnpm test --coverage

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./apps/mobile/coverage/coverage-final.json
          flags: frontend
          name: frontend-coverage

  security-scan:
    name: Security Scanning
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'

      - name: Check for secrets with Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

#### Build & Deploy Workflow

**`.github/workflows/deploy.yml`**

```yaml
name: Build & Deploy

on:
  push:
    branches: [main]
  workflow_dispatch:  # Manual trigger

jobs:
  build-backend:
    name: Build Backend Docker Image
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Login to GitHub Container Registry
        uses: docker/login-action@v2
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: ./apps/api
          file: ./apps/api/Dockerfile
          push: true
          tags: |
            ghcr.io/${{ github.repository }}/api:latest
            ghcr.io/${{ github.repository }}/api:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: build-backend
    environment: staging

    steps:
      - uses: actions/checkout@v3

      - name: Deploy to Render/Railway
        run: |
          # Trigger deployment via webhook or CLI
          curl -X POST "${{ secrets.STAGING_DEPLOY_WEBHOOK }}"

      - name: Wait for deployment
        run: sleep 60

      - name: Run smoke tests
        run: |
          ./scripts/smoke-tests.sh https://staging.knitwit.app

  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: deploy-staging
    environment: production  # Requires manual approval

    steps:
      - uses: actions/checkout@v3

      - name: Deploy to Production
        run: |
          curl -X POST "${{ secrets.PRODUCTION_DEPLOY_WEBHOOK }}"

      - name: Wait for deployment
        run: sleep 60

      - name: Run smoke tests
        run: |
          ./scripts/smoke-tests.sh https://app.knitwit.com

      - name: Notify team
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: 'Production deployment completed'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### Quality Gates

CI/CD pipeline enforces the following quality gates:

| Gate | Requirement | Blocks Merge |
|------|-------------|--------------|
| Linting | Black, isort, ESLint pass | Yes |
| Type checking | mypy, TypeScript pass | Yes |
| Unit tests | 100% pass, coverage ≥ 80% | Yes |
| Security scan | No high/critical vulnerabilities | Yes |
| Secrets scan | No leaked secrets | Yes |
| Build | Docker image builds successfully | Yes |
| Smoke tests | Core endpoints respond 200 | Staging only |

### Pipeline Performance Targets

- **PR build time**: < 5 minutes
- **Cache hit rate**: > 80%
- **Deployment to staging**: < 10 minutes
- **Deployment to production**: < 15 minutes (including approval)

---

## Containerization

### Backend Docker Setup

**apps/api/Dockerfile** (Multi-stage build)

```dockerfile
# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**apps/api/.dockerignore**

```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
.pytest_cache/
.coverage
htmlcov/
.mypy_cache/
.DS_Store
*.log
.env
.env.local
tests/
docs/
README.md
```

### Frontend Build (Future)

For future web deployment or Expo build server:

```dockerfile
# apps/mobile/Dockerfile (if needed for web build)
FROM node:18-alpine

WORKDIR /app

# Install pnpm
RUN npm install -g pnpm

# Copy package files
COPY package.json pnpm-lock.yaml ./

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy app source
COPY . .

# Build for web
RUN pnpm build:web

# Serve static files
FROM nginx:alpine
COPY --from=0 /app/web-build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Docker Compose for Production-like Testing

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  api:
    build:
      context: apps/api
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - ENV=production
      - LOG_LEVEL=INFO
      - DATABASE_URL=postgresql://user:pass@postgres:5432/knitwit
    depends_on:
      postgres:
        condition: service_healthy
    restart: unless-stopped

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=knitwit
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=securepassword
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - api
    restart: unless-stopped

volumes:
  postgres_data:
```

---

## Deployment Strategy

### Backend Deployment

**Platform Recommendation (MVP):**
- **Primary**: Render.com (easy, free tier, auto-deploy from GitHub)
- **Alternative**: Railway.app, Fly.io

**Deployment Process:**

1. **Build**: GitHub Actions builds Docker image on push to `main`
2. **Registry**: Image pushed to GitHub Container Registry (ghcr.io)
3. **Staging Deploy**: Automatic deployment to staging environment
4. **Smoke Tests**: Automated smoke tests verify staging deployment
5. **Production Approval**: Manual approval required in GitHub Actions
6. **Production Deploy**: Deploy to production after approval
7. **Verification**: Smoke tests verify production deployment

**Rollback Strategy:**

```bash
# Rollback to previous version
# Option 1: Render/Railway dashboard - select previous deployment
# Option 2: Re-deploy previous Git commit
git revert HEAD
git push origin main

# Option 3: Re-deploy previous Docker image
docker pull ghcr.io/org/api:previous-sha
# Update deployment to use previous-sha
```

**Zero-Downtime Deployment:**
- Health checks ensure new containers are ready before routing traffic
- Rolling deployment: new version deployed alongside old, then switched
- Database migrations run before deployment (backward compatible)

### Frontend Deployment (Mobile)

**Android Deployment:**

1. **Build**: EAS Build or local build
   ```bash
   cd apps/mobile
   eas build --platform android --profile production
   ```
2. **Output**: `.apk` (debug) or `.aab` (release)
3. **Distribution**:
   - Internal testing: Firebase App Distribution or TestFlight alternative
   - Production: Google Play Store

**iOS Deployment:**

1. **Build**: EAS Build (requires Apple Developer account)
   ```bash
   eas build --platform ios --profile production
   ```
2. **Output**: `.ipa` file
3. **Distribution**:
   - Internal testing: TestFlight
   - Production: Apple App Store

**Release Process:**

1. Version bump in `app.json`: `"version": "1.0.1"`
2. Build for both platforms
3. Upload to TestFlight/Firebase App Distribution
4. QA testing on real devices
5. Submit to App Store/Play Store
6. Manual approval by product owner
7. Release to production (can be staged rollout)

### Database Deployment (Future)

**MVP Phase**: No external database required (stateless API)

**Future Phases**:
- **Platform**: Managed PostgreSQL (Render, RDS, etc.)
- **Migrations**: Alembic (Python) for schema migrations
- **Deployment Process**:
  1. Run migrations before deploying new API version
  2. Migrations are backward compatible
  3. API can run with old or new schema during rollout
- **Backup**: Automated daily backups (see Backup & Recovery section)

---

## Monitoring & Observability

### Logging Strategy

**Structured Logging (Backend)**

```python
# app/core/config.py
import structlog

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()
```

**Usage:**

```python
# app/services/pattern_generator.py
logger.info(
    "pattern_generated",
    shape=request.shape,
    diameter=request.diameter,
    gauge_spi=gauge.spi,
    total_rounds=len(pattern.rounds),
    generation_time_ms=elapsed_ms
)
```

**Log Levels by Environment:**

| Environment | Level | Purpose |
|-------------|-------|---------|
| Development | DEBUG | All details for debugging |
| Staging | INFO | Key events + warnings |
| Production | WARNING | Warnings and errors only |

### Error Tracking (Sentry)

**Backend Integration:**

```python
# app/main.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="https://xxx@sentry.io/xxx",
    environment="production",
    traces_sample_rate=0.1,  # 10% of transactions for performance monitoring
    integrations=[
        FastApiIntegration(),
    ],
)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    sentry_sdk.capture_exception(exc)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "request_id": request.state.request_id}
    )
```

**Frontend Integration:**

```typescript
// apps/mobile/src/utils/monitoring.ts
import * as Sentry from '@sentry/react-native';

Sentry.init({
  dsn: process.env.EXPO_PUBLIC_SENTRY_DSN,
  environment: process.env.EXPO_PUBLIC_ENV,
  tracesSampleRate: 0.1,
});
```

### Performance Monitoring (APM)

**Backend Metrics:**

```python
# app/middleware/metrics.py
from prometheus_client import Counter, Histogram
import time

REQUEST_COUNT = Counter('api_requests_total', 'Total API requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('api_request_duration_seconds', 'API request duration', ['method', 'endpoint'])

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()

    REQUEST_DURATION.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)

    return response
```

**Pattern Generation Metrics:**

```python
PATTERN_GENERATION_TIME = Histogram(
    'pattern_generation_seconds',
    'Time to generate pattern',
    ['shape']
)

# In pattern_generator.py
with PATTERN_GENERATION_TIME.labels(shape=request.shape).time():
    pattern = compiler.compile(request)
```

### Monitoring Dashboards

**Key Metrics to Track:**

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| API response time (p95) | < 200ms | > 500ms |
| Error rate | < 0.1% | > 1% |
| Uptime | > 99.5% | < 99% |
| Pattern generation time (p95) | < 200ms | > 500ms |
| Mobile app crash rate | < 0.5% | > 2% |

**Dashboard Layout:**

```
┌─────────────────────────────────────────┐
│ API Health                              │
│ - Uptime: 99.9%                         │
│ - Response time (p95): 145ms            │
│ - Error rate: 0.05%                     │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Pattern Generation                      │
│ - Sphere: 120ms avg, 180ms p95          │
│ - Cylinder: 150ms avg, 220ms p95        │
│ - Flat Circle: 100ms avg, 150ms p95     │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ User Engagement                         │
│ - Patterns generated today: 234          │
│ - Exports (PDF): 89                      │
│ - Exports (Text): 145                    │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Mobile App                              │
│ - Active users (DAU): 156                │
│ - Crash rate: 0.3%                       │
│ - Session duration: 8.5min avg           │
└─────────────────────────────────────────┘
```

### Alerting

**Alert Channels:**
- **Critical**: PagerDuty or on-call phone
- **High**: Slack channel #alerts
- **Medium**: Email to team

**Alert Rules:**

```yaml
# alerts.yml
alerts:
  - name: HighErrorRate
    condition: error_rate > 1%
    duration: 5m
    severity: critical
    channel: pagerduty

  - name: SlowAPIResponse
    condition: api_p95_latency > 500ms
    duration: 10m
    severity: high
    channel: slack

  - name: DiskSpaceHigh
    condition: disk_usage > 80%
    duration: 15m
    severity: medium
    channel: email

  - name: HighCrashRate
    condition: mobile_crash_rate > 2%
    duration: 30m
    severity: high
    channel: slack
```

---

## Infrastructure as Code

### Configuration Management

**Environment Configuration:**

```python
# apps/api/app/core/config.py
from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    env: Literal["development", "staging", "production"] = "development"
    log_level: str = "INFO"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # CORS
    cors_origins: list[str] = ["http://localhost:19006"]

    # Database (future)
    database_url: str | None = None

    # Monitoring
    sentry_dsn: str | None = None
    sentry_environment: str | None = None
    sentry_traces_sample_rate: float = 0.1

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
```

### Environment Provisioning

**Render Blueprint (render.yaml):**

```yaml
# render.yaml
services:
  - type: web
    name: knitwit-api
    env: docker
    dockerfilePath: ./apps/api/Dockerfile
    region: oregon
    plan: starter  # Free tier for MVP
    envVars:
      - key: ENV
        value: production
      - key: LOG_LEVEL
        value: WARNING
      - key: DATABASE_URL
        fromDatabase:
          name: knitwit-db
          property: connectionString
      - key: SENTRY_DSN
        sync: false  # Set manually in dashboard
    healthCheckPath: /health
    autoDeploy: false  # Manual approval for production

databases:
  - name: knitwit-db
    databaseName: knitwit
    plan: starter
    region: oregon
```

**Railway Configuration (railway.json):**

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "apps/api/Dockerfile"
  },
  "deploy": {
    "numReplicas": 1,
    "restartPolicyType": "ON_FAILURE",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100
  }
}
```

---

## Security

### Dependency Scanning

**Automated Scanning:**

```yaml
# .github/workflows/security-scan.yml
name: Security Scan

on:
  schedule:
    - cron: '0 2 * * 1'  # Weekly on Monday at 2am
  pull_request:
  workflow_dispatch:

jobs:
  dependency-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run Snyk for Python
        uses: snyk/actions/python@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          command: test
          args: --file=apps/api/requirements.txt --severity-threshold=high

      - name: Run Snyk for Node
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          command: test
          args: --file=apps/mobile/package.json --severity-threshold=high
```

**Manual Scanning:**

```bash
# Python dependencies
pip-audit -r apps/api/requirements.txt

# Node dependencies
cd apps/mobile
pnpm audit --audit-level=high
```

### Secrets Scanning

**Pre-commit Hook:**

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.16.1
    hooks:
      - id: gitleaks
```

**CI/CD Integration:**
- Gitleaks action in test workflow (see CI/CD section)
- Fails build if secrets detected

### HTTPS/TLS Configuration

**Nginx Reverse Proxy (if self-hosted):**

```nginx
# nginx.conf
server {
    listen 80;
    server_name app.knitwit.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name app.knitwit.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    location / {
        proxy_pass http://api:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Managed Platform:**
- Render, Railway, Fly.io provide automatic HTTPS/TLS
- Free Let's Encrypt certificates
- Automatic renewal

### API Security

**CORS Configuration:**

```python
# app/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,  # Specific origins only
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Limited methods
    allow_headers=["*"],
)
```

**Rate Limiting (Future):**

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/v1/generate")
@limiter.limit("10/minute")
async def generate_pattern(request: Request, data: GenerateRequest):
    # ...
```

**Input Validation:**
- Pydantic models enforce strict validation
- Maximum input sizes enforced
- Type checking on all inputs

---

## Backup & Recovery

### Data Backup Strategy

**MVP Phase (Stateless API):**
- No persistent user data
- No backup required for MVP

**Future Phase (With Database):**

**Backup Schedule:**
- **Daily**: Automated full backup at 2am UTC
- **Weekly**: Full backup retained for 4 weeks
- **Monthly**: Full backup retained for 12 months

**Backup Locations:**
- **Primary**: Managed database service backups (Render, RDS)
- **Secondary**: AWS S3 or equivalent (encrypted at rest)

**Backup Verification:**
- Weekly automated restore test to staging environment
- Monthly manual restore test with data validation

### Disaster Recovery Plan

**Recovery Time Objective (RTO):** 4 hours
- Time from incident to service restored

**Recovery Point Objective (RPO):** 24 hours
- Maximum acceptable data loss (1 day of data)

**Disaster Scenarios:**

| Scenario | Recovery Procedure | RTO | RPO |
|----------|-------------------|-----|-----|
| **API service down** | 1. Check platform status<br>2. Rollback to previous version<br>3. Scale up resources | 30 min | 0 |
| **Database corruption** | 1. Stop writes<br>2. Restore from latest backup<br>3. Verify data integrity | 2 hours | 24 hours |
| **Data center outage** | 1. Failover to backup region<br>2. Update DNS<br>3. Verify services | 4 hours | 24 hours |
| **Complete infrastructure loss** | 1. Provision new infrastructure<br>2. Deploy from Git<br>3. Restore database from S3 | 4 hours | 24 hours |

**Recovery Runbook:**

```markdown
# Disaster Recovery Runbook

## 1. Assess Situation
- [ ] Identify affected services
- [ ] Determine scope of outage
- [ ] Notify team via Slack #incidents

## 2. API Service Recovery
- [ ] Check platform status dashboard
- [ ] Review recent deployments (rollback if needed)
- [ ] Check logs in Sentry for errors
- [ ] Scale resources if needed
- [ ] Verify health endpoint responds

## 3. Database Recovery (if applicable)
- [ ] Identify database issue (corruption, connectivity, etc.)
- [ ] Stop write operations
- [ ] Restore from most recent backup
- [ ] Verify data integrity with test queries
- [ ] Resume write operations

## 4. Verification
- [ ] Run smoke tests
- [ ] Check monitoring dashboards
- [ ] Test critical user flows
- [ ] Monitor error rates for 30 minutes

## 5. Post-Incident
- [ ] Update status page
- [ ] Notify users if needed
- [ ] Schedule post-mortem within 48 hours
- [ ] Document lessons learned
```

### Backup Testing

**Monthly Backup Test:**

```bash
#!/bin/bash
# scripts/test-backup-restore.sh

# 1. Download latest backup
aws s3 cp s3://knitwit-backups/latest.sql.gz /tmp/

# 2. Restore to staging database
gunzip /tmp/latest.sql.gz
psql $STAGING_DATABASE_URL < /tmp/latest.sql

# 3. Run data validation queries
psql $STAGING_DATABASE_URL -c "SELECT COUNT(*) FROM users;"
psql $STAGING_DATABASE_URL -c "SELECT COUNT(*) FROM patterns;"

# 4. Verify API can connect
curl https://staging.knitwit.app/health

echo "Backup restore test completed successfully"
```

---

## DevOps Toolchain

### Tools & Services

| Category | Tool | Purpose | Cost |
|----------|------|---------|------|
| **Source Control** | GitHub | Code repository, CI/CD | Free (public) |
| **CI/CD** | GitHub Actions | Automated testing, deployment | Free tier |
| **Container Registry** | GitHub Container Registry | Docker image storage | Free (public) |
| **Hosting (API)** | Render.com | Backend deployment | Free tier |
| **Hosting (Mobile)** | Expo EAS | Mobile app builds | Free tier |
| **Database** | Render PostgreSQL | Managed database (future) | $7/month |
| **Error Tracking** | Sentry | Error monitoring | Free tier |
| **Monitoring** | Render metrics | Basic metrics | Included |
| **Security Scanning** | Snyk | Dependency vulnerabilities | Free tier |
| **Secrets Scanning** | Gitleaks | Prevent secret leaks | Free |
| **Code Coverage** | Codecov | Track test coverage | Free (open source) |

### Setup Instructions

**1. GitHub Repository**

```bash
# Initialize repository
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/org/knit-wit.git
git push -u origin main

# Enable branch protection
# Settings > Branches > Add rule
# - Require PR reviews
# - Require status checks to pass
# - Require linear history
```

**2. Render.com Setup**

1. Create account at render.com
2. Connect GitHub repository
3. Create Web Service:
   - Environment: Docker
   - Dockerfile path: `apps/api/Dockerfile`
   - Region: Oregon (or closest)
   - Plan: Free tier
4. Add environment variables (see Environment Setup section)
5. Deploy

**3. Sentry Setup**

```bash
# Create Sentry account and project
# Copy DSN

# Add to .env
SENTRY_DSN=https://xxx@sentry.io/xxx

# Add to GitHub Secrets
gh secret set SENTRY_DSN --body "https://xxx@sentry.io/xxx"
```

**4. Codecov Setup**

```bash
# Sign up at codecov.io with GitHub
# Add repository
# Copy token

# Add to GitHub Secrets
gh secret set CODECOV_TOKEN --body "your-token"
```

**5. Expo EAS Setup**

```bash
# Install EAS CLI
npm install -g eas-cli

# Login to Expo
eas login

# Configure project
cd apps/mobile
eas build:configure

# Update eas.json with build profiles
```

### Access & Credentials

**Credential Management:**

| Service | Access Method | Stored In |
|---------|--------------|-----------|
| GitHub | Personal Access Token | Password manager |
| Render | Dashboard login (OAuth) | N/A |
| Sentry | Dashboard login (OAuth) | N/A |
| Expo | `eas login` | Expo CLI |
| Database | Connection string | Render dashboard |

**Team Access:**
- GitHub: Add team members to repository with appropriate roles
- Render: Invite team members to project
- Sentry: Invite team members to organization
- Expo: Add members to organization

**Credential Rotation:**
- Personal access tokens: Rotate every 90 days
- API keys: Rotate quarterly
- Database passwords: Rotate on security events

---

## Appendix

### Smoke Tests Script

**scripts/smoke-tests.sh**

```bash
#!/bin/bash
# Smoke tests for API deployment verification

API_URL="${1:-http://localhost:8000}"

echo "Running smoke tests against $API_URL..."

# Test 1: Health endpoint
echo "Test 1: Health check"
response=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL/health")
if [ "$response" -eq 200 ]; then
    echo "✓ Health check passed"
else
    echo "✗ Health check failed (HTTP $response)"
    exit 1
fi

# Test 2: Generate sphere pattern
echo "Test 2: Generate sphere pattern"
response=$(curl -s -X POST "$API_URL/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{"shape":"sphere","diameter":4,"gauge":{"spi":5,"rpi":6}}')

if echo "$response" | jq -e '.pattern.rounds' > /dev/null 2>&1; then
    echo "✓ Sphere generation passed"
else
    echo "✗ Sphere generation failed"
    echo "$response"
    exit 1
fi

# Test 3: Export to text
echo "Test 3: Export pattern to text"
response=$(curl -s -X POST "$API_URL/api/v1/export/text" \
  -H "Content-Type: application/json" \
  -d "$response")

if [ -n "$response" ]; then
    echo "✓ Text export passed"
else
    echo "✗ Text export failed"
    exit 1
fi

echo ""
echo "All smoke tests passed! ✓"
```

### Environment Variables Checklist

**Backend (.env):**
```bash
ENV=development|staging|production
LOG_LEVEL=DEBUG|INFO|WARNING
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=comma,separated,origins
DATABASE_URL=postgresql://...  # Future
SENTRY_DSN=https://...
SENTRY_ENVIRONMENT=development|staging|production
```

**Frontend (.env):**
```bash
EXPO_PUBLIC_API_URL=http://localhost:8000
EXPO_PUBLIC_ENV=development|staging|production
EXPO_PUBLIC_SENTRY_DSN=https://...
```

### Useful Commands Reference

```bash
# Local development
docker-compose up              # Start backend
docker-compose down            # Stop backend
docker-compose logs -f api     # View backend logs
cd apps/mobile && pnpm expo start  # Start mobile app

# Testing
cd apps/api && pytest          # Run backend tests
cd apps/mobile && pnpm test    # Run frontend tests

# Building
docker build -t knitwit-api apps/api/  # Build backend image
cd apps/mobile && eas build --platform android  # Build mobile app

# Deployment
git push origin main           # Trigger CI/CD
eas submit -p android          # Submit to Play Store
eas submit -p ios              # Submit to App Store
```

---

**Document Version**: 1.0
**Last Updated**: 2025-11-05
**Maintained By**: DevOps Team
