# CI/CD Pipeline Setup

## Overview

The Knit-Wit project uses GitHub Actions for continuous integration and continuous deployment. The pipeline is optimized for speed (< 5 minutes target) and uses smart change detection to skip unnecessary jobs.

## Pipeline Architecture

### File Location
- **Workflow**: `.github/workflows/ci.yml`

### Trigger Events
- Pull requests to any branch
- Pushes to `main` branch

### Jobs Overview

1. **changes** - Detects which parts of the codebase changed (frontend/backend/python)
2. **frontend-lint** - ESLint/Prettier for React Native code
3. **frontend-typecheck** - TypeScript type checking
4. **frontend-test** - Jest unit/integration tests
5. **backend-lint** - Black, isort, ruff for Python code
6. **backend-typecheck** - mypy type checking
7. **backend-test** - pytest with coverage
8. **build-frontend** - Expo build verification
9. **build-backend** - Python package build
10. **ci-status** - Final status aggregation (required for branch protection)

## Performance Optimizations

### Change Detection
Uses `dorny/paths-filter@v3` to detect file changes and skip unnecessary jobs:
- Frontend changes: Runs only frontend jobs
- Backend changes: Runs only backend jobs
- No changes: Skips most jobs

### Parallel Execution
Jobs run in parallel where possible:
- Frontend jobs (lint, typecheck, test) run concurrently
- Backend jobs run as matrix (apps/api, packages/pattern-engine) in parallel
- No sequential dependencies except build jobs

### Caching Strategy

**pnpm cache**:
- Managed by `actions/setup-node@v4` with `cache: 'pnpm'`
- Caches: `~/.pnpm-store`

**Python cache**:
- Managed by `astral-sh/setup-uv@v3` with `enable-cache: true`
- Caches: uv package cache for fast installs

**Concurrency**:
- Cancels in-progress runs for the same PR/branch on new pushes
- Prevents wasted CI time on outdated commits

## Technology Stack

### Actions Used
- `actions/checkout@v4` - Checkout repository
- `actions/setup-node@v4` - Setup Node.js with pnpm caching
- `actions/setup-python@v5` - Setup Python
- `pnpm/action-setup@v3` - Install pnpm
- `astral-sh/setup-uv@v3` - Install uv (fast Python package manager)
- `dorny/paths-filter@v3` - Detect file changes
- `codecov/codecov-action@v4` - Upload coverage reports (optional)

### Environment
- **Node.js**: 18
- **Python**: 3.11
- **pnpm**: 8.15.0
- **OS**: ubuntu-latest

## Branch Protection Configuration

### Required Status Checks

To enable branch protection on the `main` branch:

1. Navigate to: **Settings** → **Branches** → **Branch protection rules**
2. Click **Add rule**
3. Configure:
   - **Branch name pattern**: `main`
   - **Require status checks to pass before merging**: ✓
   - **Require branches to be up to date before merging**: ✓
   - **Status checks that are required**:
     - `CI Status` (the final aggregator job)
   - **Require linear history**: ✓ (optional, but recommended)
   - **Do not allow bypassing the above settings**: ✓

### Why Only Require `CI Status`?

The `ci-status` job depends on all other jobs and fails if any upstream job fails. This provides:
- Single required check (simpler configuration)
- Automatic failure propagation
- Clear pass/fail indicator

## Running Locally

### Frontend Checks
```bash
# Install dependencies
pnpm install

# Run all frontend checks
pnpm lint
pnpm typecheck
pnpm test:mobile
```

### Backend Checks
```bash
# API checks
cd apps/api
pip install -e ".[dev]"
black --check .
isort --check-only .
mypy .
pytest --cov

# Pattern engine checks
cd packages/pattern-engine
pip install -e ".[dev]"
black --check .
isort --check-only .
mypy .
pytest --cov
```

## Troubleshooting

### Job Skipped Due to No Changes
- **Expected**: Change detection optimization
- **Override**: Manually trigger workflow via GitHub UI

### Frontend Build Fails
- Check `pnpm-lock.yaml` is committed
- Verify `package.json` scripts exist
- Ensure Node.js version matches CI (18)

### Backend Tests Fail
- Verify `pyproject.toml` exists in target directory
- Check Python version matches CI (3.11)
- Ensure test dependencies installed (`pip install -e ".[dev]"`)

### Timeout (> 5 minutes)
- Check if caching is working (look for cache hit logs)
- Consider splitting large test suites
- Review parallelization opportunities

## Extending the Pipeline

### Adding New Jobs

1. Add job definition in `.github/workflows/ci.yml`
2. Set appropriate `needs:` dependencies
3. Use `if:` conditions for change detection
4. Update `ci-status` job's `needs:` array

Example:
```yaml
new-job:
  name: New Job
  runs-on: ubuntu-latest
  needs: changes
  if: needs.changes.outputs.frontend == 'true'
  steps:
    - uses: actions/checkout@v4
    # ... job steps
```

### Adding New Change Detection Paths

Edit the `changes` job filter:
```yaml
filters: |
  frontend:
    - 'apps/new-frontend-app/**'
  backend:
    - 'packages/new-python-package/**'
```

## Performance Metrics

**Target**: < 5 minutes total pipeline time

**Typical Timing**:
- Change detection: ~10s
- Frontend lint/typecheck/test: ~2min (parallel)
- Backend lint/typecheck/test: ~2min (parallel, matrix)
- Build jobs: ~1min (parallel)
- Total: ~3-4 minutes

## Security Considerations

### Secrets Management
- No secrets required for MVP CI
- Future: Add `CODECOV_TOKEN` for coverage uploads
- Use GitHub encrypted secrets, never commit secrets

### Dependency Security
- `pnpm install --frozen-lockfile` prevents supply chain attacks
- Consider adding `dependabot.yml` for automated updates
- Review PRs from bots carefully

## Future Enhancements

### Post-MVP Additions
- [ ] End-to-end tests (Playwright/Detox)
- [ ] Performance benchmarking
- [ ] Docker image builds
- [ ] Deployment to staging/production
- [ ] Security scanning (Snyk, Dependabot)
- [ ] License compliance checks

### CD (Continuous Deployment)
When ready for deployment:
- Add deployment jobs conditional on `push` to `main`
- Use environments (staging, production) with approvals
- Implement blue/green or canary deployments
- Add smoke tests post-deployment

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [pnpm CI Configuration](https://pnpm.io/continuous-integration)
- [uv Package Manager](https://github.com/astral-sh/uv)
- [Branch Protection Rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
