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

```bash
# Run all services
pnpm dev

# Run mobile app only
pnpm dev:mobile

# Run API only
pnpm dev:api

# Run with Docker Compose
docker-compose up
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
