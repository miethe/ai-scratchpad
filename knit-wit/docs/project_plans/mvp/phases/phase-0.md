# Phase 0: Project Setup & Architecture

**Phase:** 0 (Foundation)
**Duration:** Weeks 1-2 (Sprint 1)
**Capacity:** 40-50 story points
**Team:** Full team (4-6 people)
**Status:** Active Development

**Parent Document:** [Implementation Plan Overview](../implementation-plan-overview.md)

---

## Table of Contents

1. [Phase Overview](#phase-overview)
2. [Goals & Deliverables](#goals--deliverables)
3. [Epic Breakdown](#epic-breakdown)
4. [Sprint 1 Plan](#sprint-1-plan)
5. [Technical Setup Tasks](#technical-setup-tasks)
6. [Success Criteria](#success-criteria)
7. [Dependencies & Blockers](#dependencies--blockers)
8. [Risks](#risks)
9. [Phase Exit Criteria](#phase-exit-criteria)
10. [Next Phase Preview](#next-phase-preview)

---

## Phase Overview

### Purpose

Phase 0 establishes the foundational infrastructure, development environment, and architectural patterns for the Knit-Wit MVP. This phase ensures the team can begin feature development with confidence, clear patterns, and automated quality gates in place.

### Timeline

- **Start Date:** Week 1, Day 1
- **End Date:** Week 2, Day 5
- **Duration:** 2 weeks (Sprint 1)

### Phase Context

**Precedes:** Phase 1 (Core Pattern Engine)
**Follows:** Project kickoff and team formation
**Critical Path:** Yes — all subsequent work depends on this phase

### Capacity Planning

- **Total Capacity:** 40-50 story points
- **Team Size:** 4-6 people
- **Velocity Target:** 40-50 points per 2-week sprint
- **Buffer:** 10% for learning curve and unexpected setup issues

---

## Goals & Deliverables

### Primary Goals

1. **Infrastructure Foundation**
   - Monorepo initialized with proper workspace configuration
   - CI/CD pipeline operational and green on every PR
   - Development environments reproducible via Docker

2. **Development Environment**
   - Local development setup documented and tested
   - All team members can run backend and frontend locally
   - Code quality tools (linters, formatters, tests) integrated

3. **Architecture Prototypes**
   - Algorithm spike completed with math validation
   - API contracts defined and documented
   - Frontend state management approach selected and validated

4. **Team Readiness**
   - Development guidelines documented
   - Branching and PR workflow established
   - Team onboarded to tech stack and tools

### Deliverables with Acceptance Criteria

#### D1: Monorepo Setup
**Acceptance Criteria:**
- [ ] GitHub repository created with main branch protected
- [ ] pnpm workspaces configured for packages/apps
- [ ] Root package.json with scripts for build, test, lint
- [ ] All packages installable via single `pnpm install` command
- [ ] README.md with quick-start instructions

#### D2: CI/CD Pipeline
**Acceptance Criteria:**
- [ ] GitHub Actions workflow runs on every PR
- [ ] Pipeline includes: lint, type-check, test, build steps
- [ ] Branch protection rules require CI passing
- [ ] Build artifacts cached for faster runs
- [ ] Pipeline completes in < 5 minutes for typical changes

#### D3: Backend Scaffold
**Acceptance Criteria:**
- [ ] FastAPI application runs locally via Docker Compose
- [ ] Health check endpoint responds at `/health`
- [ ] API documentation auto-generated via Swagger/OpenAPI
- [ ] Hot-reload working for development
- [ ] Python 3.11+ environment with virtual env

#### D4: Pattern Engine Library
**Acceptance Criteria:**
- [ ] Python package structure with setup.py/pyproject.toml
- [ ] Importable from both backend and test suites
- [ ] Initial module structure documented
- [ ] Basic CI tests pass (even if just imports)

#### D5: Frontend Scaffold
**Acceptance Criteria:**
- [ ] Expo app runs on iOS simulator
- [ ] Expo app runs on Android emulator
- [ ] TypeScript compilation passes
- [ ] Basic navigation (stack + tabs) functional
- [ ] Hot-reload working

#### D6: Docker Development Environment
**Acceptance Criteria:**
- [ ] Docker Compose file defines backend service
- [ ] Optional PostgreSQL service for future use
- [ ] Volume mounts for hot-reload
- [ ] Environment variables configurable via .env file
- [ ] One-command startup: `docker-compose up`

#### D7: Algorithm Spike
**Acceptance Criteria:**
- [ ] Sphere equator calculation validated against manual calculations
- [ ] Cylinder cap generation approach documented
- [ ] Round distribution algorithm prototyped
- [ ] Gauge mapping formula verified with sample data
- [ ] Results documented in `docs/algorithm-spike.md`

#### D8: API Contract Definition
**Acceptance Criteria:**
- [ ] All endpoints documented with request/response schemas
- [ ] Pydantic models created for request validation
- [ ] TypeScript types generated from schemas (or manually defined)
- [ ] Error response formats standardized
- [ ] API versioning strategy decided

#### D9: Development Guidelines
**Acceptance Criteria:**
- [ ] CONTRIBUTING.md created with PR workflow
- [ ] Code style guide documented
- [ ] Commit message conventions defined
- [ ] Testing requirements specified
- [ ] Accessibility checklist included

---

## Epic Breakdown

### EPIC D: App Shell & Setup

**Epic Owner:** Frontend Lead
**Duration:** Sprint 1 (Weeks 1-2)
**Total Effort:** 31 story points
**Priority:** P0 (Critical Path)

**Overview:**
Establish the application infrastructure and initial architecture prototypes. This epic covers repository setup, CI/CD pipeline, project scaffolding, and architectural decision documentation.

**Goals:**
- Team can clone repository and run all projects locally
- CI/CD pipeline prevents broken code from merging
- Architecture decisions documented and validated
- Development workflow smooth and automated

#### Stories

---

##### Story SETUP-1: Initialize Monorepo

**Story ID:** SETUP-1
**Title:** Initialize monorepo with pnpm workspaces
**Epic:** EPIC D — App Shell & Setup
**Effort:** 5 story points
**Priority:** P0 (Critical Path)
**Complexity:** Low
**Owner:** DevOps Lead / Backend Lead

**Description:**
Create the GitHub repository and configure it as a monorepo using pnpm workspaces. Set up the workspace structure for multiple packages (backend, frontend, pattern-engine library).

**User Story:**
As a developer, I want a single repository with all project code so that I can work across frontend and backend with consistent tooling.

**Technical Requirements:**
- GitHub repository created with main branch
- pnpm workspaces configured in root package.json
- Workspace structure: `apps/`, `packages/` directories
- Root-level scripts for common tasks (install, build, test, lint)
- `.gitignore` configured for Node, Python, OS files
- Initial README with quick-start instructions

**Acceptance Criteria:**
- [ ] Repository created at `github.com/[org]/knit-wit`
- [ ] pnpm workspace configuration in root `package.json`
- [ ] Directory structure:
  ```
  knit-wit/
  ├── apps/
  │   ├── backend/
  │   └── frontend/
  ├── packages/
  │   └── pattern-engine/
  ├── docs/
  ├── .github/workflows/
  ├── package.json
  ├── pnpm-workspace.yaml
  └── README.md
  ```
- [ ] `pnpm install` runs successfully from root
- [ ] README includes setup instructions
- [ ] Branch protection enabled on main branch

**Technical Implementation Notes:**
- Use pnpm workspaces for better performance and disk usage
- Configure workspace protocol for internal dependencies
- Set up Turborepo or Nx if complex build orchestration needed
- Consider monorepo tools: Lerna (optional), pnpm built-in features

**Dependencies:**
- None (first story)

**Definition of Done:**
- [ ] Code committed to main branch
- [ ] README includes clear setup steps
- [ ] All team members can clone and install successfully
- [ ] No security vulnerabilities in dependencies

---

##### Story SETUP-2: GitHub Actions CI/CD Pipeline

**Story ID:** SETUP-2
**Title:** Create CI/CD pipeline with GitHub Actions
**Epic:** EPIC D — App Shell & Setup
**Effort:** 8 story points
**Priority:** P0 (Critical Path)
**Complexity:** Medium
**Owner:** DevOps Lead

**Description:**
Set up automated testing, linting, type-checking, and build workflows using GitHub Actions. Configure branch protection to require passing CI before merge.

**User Story:**
As a developer, I want automated quality checks on every PR so that broken code cannot be merged to main.

**Technical Requirements:**
- GitHub Actions workflow for PR validation
- Separate jobs: lint, type-check, test, build
- Caching for node_modules and pip packages
- Workflow runs on: push to main, all PRs
- Branch protection rules require passing CI
- Build time optimization (parallel jobs, caching)

**Acceptance Criteria:**
- [ ] Workflow file created: `.github/workflows/ci.yml`
- [ ] Pipeline includes jobs:
  - `lint`: Run ESLint (frontend), Ruff/Black (backend)
  - `type-check`: TypeScript tsc, mypy
  - `test`: Jest (frontend), pytest (backend)
  - `build`: Build all apps and packages
- [ ] Caching configured for:
  - pnpm store
  - Python pip cache
  - Docker layers (if building containers)
- [ ] Branch protection on main requires:
  - CI passing
  - At least 1 approval
  - Up-to-date with main
- [ ] Pipeline completes in < 5 minutes for typical PR
- [ ] Failed checks prevent merge

**Technical Implementation Notes:**
```yaml
# .github/workflows/ci.yml (skeleton)
name: CI

on:
  pull_request:
  push:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v3
        with:
          node-version: 18
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm lint

  # ... other jobs
```

**Dependencies:**
- SETUP-1 (monorepo structure)

**Definition of Done:**
- [ ] CI workflow runs on test PR
- [ ] All jobs pass with green checkmarks
- [ ] Failed build blocks merge
- [ ] Team can see clear error messages on failures
- [ ] Documentation in CONTRIBUTING.md explains CI requirements

---

##### Story SETUP-3: Backend Project Initialization

**Story ID:** SETUP-3
**Title:** Initialize FastAPI backend project
**Epic:** EPIC D — App Shell & Setup
**Effort:** 5 story points
**Priority:** P0 (Critical Path)
**Complexity:** Low
**Owner:** Backend Lead

**Description:**
Create the FastAPI application skeleton with proper project structure, Docker setup, and basic health check endpoint.

**User Story:**
As a backend developer, I want a FastAPI project structure so that I can start building API endpoints.

**Technical Requirements:**
- FastAPI app with uvicorn server
- Project structure following best practices
- Dockerfile for containerization
- Health check endpoint at `/health`
- Auto-generated API documentation
- CORS middleware configured
- Environment variable management

**Acceptance Criteria:**
- [ ] Directory structure:
  ```
  apps/backend/
  ├── app/
  │   ├── __init__.py
  │   ├── main.py
  │   ├── api/
  │   │   ├── __init__.py
  │   │   └── routes/
  │   ├── core/
  │   │   ├── config.py
  │   │   └── __init__.py
  │   └── models/
  ├── tests/
  ├── Dockerfile
  ├── requirements.txt
  ├── pyproject.toml
  └── README.md
  ```
- [ ] FastAPI app runs locally: `uvicorn app.main:app --reload`
- [ ] Health check endpoint returns 200 OK
- [ ] Swagger docs available at `/docs`
- [ ] ReDoc available at `/redoc`
- [ ] CORS configured for frontend origins
- [ ] Environment variables loaded from `.env` file

**Technical Implementation Notes:**
```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Knit-Wit API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for frontend origin
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

**Dependencies:**
- SETUP-1 (monorepo structure)

**Definition of Done:**
- [ ] App starts without errors
- [ ] Health check accessible at http://localhost:8000/health
- [ ] API docs load successfully
- [ ] Hot-reload works when code changes
- [ ] README documents how to run locally

---

##### Story SETUP-4: Pattern Engine Library Initialization

**Story ID:** SETUP-4
**Title:** Initialize pattern-engine Python package
**Epic:** EPIC D — App Shell & Setup
**Effort:** 3 story points
**Priority:** P0 (Critical Path)
**Complexity:** Low
**Owner:** Backend Lead

**Description:**
Create the Python package structure for the pattern engine library. This library will contain all pattern generation algorithms and will be importable by the backend and tests.

**User Story:**
As a backend developer, I want a separate pattern engine package so that I can develop and test algorithms independently from the API layer.

**Technical Requirements:**
- Python package structure with setup.py or pyproject.toml
- Proper module organization
- Installable in development mode
- Initial module stubs created
- Basic CI test for import

**Acceptance Criteria:**
- [ ] Directory structure:
  ```
  packages/pattern-engine/
  ├── knit_wit_engine/
  │   ├── __init__.py
  │   ├── algorithms/
  │   │   ├── __init__.py
  │   │   ├── sphere.py
  │   │   ├── cylinder.py
  │   │   └── cone.py
  │   ├── models/
  │   │   ├── __init__.py
  │   │   └── dsl.py
  │   └── utils/
  │       ├── __init__.py
  │       └── gauge.py
  ├── tests/
  │   └── __init__.py
  ├── pyproject.toml
  └── README.md
  ```
- [ ] Package installable: `pip install -e packages/pattern-engine`
- [ ] Import works: `from knit_wit_engine import __version__`
- [ ] Basic pytest test passes
- [ ] CI can import and test the package

**Technical Implementation Notes:**
```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "knit-wit-engine"
version = "0.1.0"
description = "Parametric crochet pattern generation engine"
requires-python = ">=3.11"
dependencies = [
    "pydantic>=2.0",
    "numpy>=1.24",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "mypy>=1.0",
]
```

**Dependencies:**
- SETUP-1 (monorepo structure)

**Definition of Done:**
- [ ] Package installs successfully
- [ ] Import test passes in CI
- [ ] README explains package purpose
- [ ] Version number accessible
- [ ] No import errors

---

##### Story SETUP-5: React Native/Expo App Initialization

**Story ID:** SETUP-5
**Title:** Initialize RN/Expo app with TypeScript
**Epic:** EPIC D — App Shell & Setup
**Effort:** 5 story points
**Priority:** P0 (Critical Path)
**Complexity:** Medium
**Owner:** Frontend Lead

**Description:**
Create the React Native app using Expo with TypeScript configuration and basic navigation setup.

**User Story:**
As a frontend developer, I want a React Native app with Expo so that I can start building mobile UI screens.

**Technical Requirements:**
- Expo SDK (latest stable version)
- TypeScript configuration
- React Navigation setup (stack + tabs)
- ESLint and Prettier configured
- Basic screen structure created
- Development server runs on simulator/emulator

**Acceptance Criteria:**
- [ ] Expo app created with TypeScript template
- [ ] App runs on iOS simulator without errors
- [ ] App runs on Android emulator without errors
- [ ] React Navigation configured with:
  - Bottom tab navigator
  - Stack navigator for modal screens
- [ ] Basic screens created:
  - `HomeScreen.tsx`
  - `GenerateScreen.tsx` (placeholder)
  - `SettingsScreen.tsx` (placeholder)
- [ ] TypeScript compilation passes
- [ ] ESLint + Prettier configured and passing
- [ ] Hot-reload working

**Technical Implementation Notes:**
```typescript
// App.tsx
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

const Tab = createBottomTabNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Tab.Navigator>
        <Tab.Screen name="Home" component={HomeScreen} />
        <Tab.Screen name="Generate" component={GenerateScreen} />
        <Tab.Screen name="Settings" component={SettingsScreen} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
```

**Dependencies:**
- SETUP-1 (monorepo structure)

**Definition of Done:**
- [ ] Expo start command works: `pnpm dev`
- [ ] App loads on iOS simulator
- [ ] App loads on Android emulator
- [ ] Navigation between tabs works
- [ ] TypeScript errors: 0
- [ ] ESLint errors: 0
- [ ] README documents how to run on simulators

---

##### Story SETUP-6: Docker Compose Development Environment

**Story ID:** SETUP-6
**Title:** Create Docker Compose for local development
**Epic:** EPIC D — App Shell & Setup
**Effort:** 5 story points
**Priority:** P0 (Critical Path)
**Complexity:** Medium
**Owner:** DevOps Lead / Backend Lead

**Description:**
Create a Docker Compose configuration that allows developers to run the backend (and optional PostgreSQL) with a single command.

**User Story:**
As a developer, I want to run the entire backend stack with one command so that I can focus on coding instead of environment setup.

**Technical Requirements:**
- Docker Compose file defines all services
- Backend service with hot-reload
- PostgreSQL service (optional, for future use)
- Volume mounts for code changes
- Environment variable configuration
- Health checks for all services

**Acceptance Criteria:**
- [ ] `docker-compose.yml` created with services:
  - `backend`: FastAPI application
  - `db`: PostgreSQL (optional, not required for MVP initially)
- [ ] Backend service:
  - Builds from `apps/backend/Dockerfile`
  - Mounts source code for hot-reload
  - Exposes port 8000
  - Environment variables from `.env`
- [ ] PostgreSQL service:
  - Uses official postgres:15 image
  - Persistent volume for data
  - Exposes port 5432
- [ ] Single command starts all: `docker-compose up`
- [ ] Health checks work for all services
- [ ] Code changes trigger hot-reload

**Technical Implementation Notes:**
```yaml
# docker-compose.yml
version: '3.9'

services:
  backend:
    build:
      context: ./apps/backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    volumes:
      - ./apps/backend/app:/app/app
      - ./packages/pattern-engine:/app/pattern-engine
    environment:
      - DATABASE_URL=${DATABASE_URL:-postgresql://postgres:postgres@db:5432/knitwit}
    depends_on:
      - db
    command: uvicorn app.main:app --host 0.0.0.0 --reload

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=knitwit
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

**Dependencies:**
- SETUP-3 (backend scaffold)

**Definition of Done:**
- [ ] `docker-compose up` starts all services
- [ ] Backend accessible at http://localhost:8000
- [ ] Database accessible at localhost:5432
- [ ] Hot-reload verified by changing code
- [ ] `docker-compose down` cleans up properly
- [ ] README documents Docker setup

---

##### Story ARCH-1: Algorithm Spike (Sphere/Cylinder)

**Story ID:** ARCH-1
**Title:** Research and prototype gauge mapping and pattern algorithms
**Epic:** EPIC D — App Shell & Setup
**Effort:** 8 story points
**Priority:** P0 (Critical Path)
**Complexity:** High
**Owner:** Backend Lead

**Description:**
Conduct an architectural spike to research, prototype, and validate the core mathematical algorithms for sphere and cylinder pattern generation. Document findings and implementation approach.

**User Story:**
As a backend engineer, I want validated pattern algorithms so that I can confidently implement the pattern engine.

**Technical Requirements:**
- Research crochet sphere geometry and mathematics
- Prototype gauge mapping functions
- Calculate equator round counts
- Design round distribution algorithm
- Validate against manual pattern calculations
- Document findings and formulas

**Acceptance Criteria:**
- [ ] Spike document created: `docs/algorithm-spike.md`
- [ ] Sphere equator calculation formula documented
- [ ] Cylinder cap generation approach defined
- [ ] Gauge mapping formula validated with sample data:
  - 10 sts/10cm, DK yarn → stitch length = X cm
  - 15 sts/10cm, Worsted yarn → stitch length = Y cm
- [ ] Round distribution algorithm prototyped (Python or pseudocode)
- [ ] Sample calculations verified against known patterns:
  - 10cm diameter sphere at 12 sts/10cm = ~N stitches at equator
- [ ] Edge cases identified and documented
- [ ] Performance considerations noted

**Technical Implementation Notes:**

Key formulas to validate:
```python
# Gauge to stitch dimensions
def gauge_to_stitch_length(sts_per_10cm: float, yarn_weight_factor: float) -> float:
    """
    Calculate stitch length in cm.
    yarn_weight_factor: 0.5 (Baby), 0.6 (DK), 0.7 (Worsted), 0.9 (Bulky)
    """
    return yarn_weight_factor * (10.0 / sts_per_10cm)

# Sphere equator circumference → stitch count
def sphere_equator_stitches(radius_cm: float, gauge: Gauge) -> int:
    """
    Circumference = 2 * π * radius
    Stitches = circumference / stitch_width
    """
    circumference = 2 * 3.14159 * radius_cm
    stitch_width = gauge.sts_per_10cm / 10.0
    return round(circumference * stitch_width)
```

**Dependencies:**
- None (can proceed independently)

**Definition of Done:**
- [ ] Document reviewed by Backend Lead and one other engineer
- [ ] Formulas validated against at least 3 known patterns
- [ ] Sample code runs and produces expected outputs
- [ ] Edge cases documented with mitigation strategies
- [ ] Performance targets noted (< 200ms per generation)
- [ ] Document committed to repo

---

##### Story ARCH-2: DSL Schema Finalization

**Story ID:** ARCH-2
**Title:** Finalize JSON DSL schema and Pydantic models
**Epic:** EPIC D — App Shell & Setup
**Effort:** 5 story points
**Priority:** P0 (Critical Path)
**Complexity:** Medium
**Owner:** Backend Lead

**Description:**
Define the Domain-Specific Language (DSL) JSON schema that represents crochet patterns. Create Pydantic models for validation and type safety.

**User Story:**
As a developer, I want a well-defined DSL schema so that frontend and backend can communicate with a consistent pattern representation.

**Technical Requirements:**
- JSON schema for pattern DSL
- Pydantic models for Python validation
- TypeScript types for frontend consumption
- Schema documentation with examples
- Validation rules for all fields

**Acceptance Criteria:**
- [ ] JSON schema file created: `docs/dsl-schema.json`
- [ ] Pydantic models created in `packages/pattern-engine/knit_wit_engine/models/dsl.py`
- [ ] TypeScript types created in `apps/frontend/src/types/dsl.ts`
- [ ] Schema includes:
  - Pattern metadata (name, gauge, yarn)
  - Round definitions
  - Instruction sequences
  - Stitch types and counts
- [ ] Sample valid DSL JSON documents created (sphere, cylinder, cone)
- [ ] Validation tests pass for valid/invalid inputs
- [ ] Documentation includes field descriptions and examples

**Technical Implementation Notes:**
```python
# dsl.py
from pydantic import BaseModel, Field
from typing import List, Literal

class Gauge(BaseModel):
    sts_per_10cm: float = Field(gt=0, description="Stitches per 10cm")
    rows_per_10cm: float = Field(gt=0, description="Rows per 10cm")

class Instruction(BaseModel):
    type: Literal["sc", "inc", "dec", "ch"]
    count: int = Field(ge=1)

class Round(BaseModel):
    number: int = Field(ge=1)
    instructions: List[Instruction]
    stitch_count: int = Field(ge=1)

class Pattern(BaseModel):
    name: str
    shape: Literal["sphere", "cylinder", "cone"]
    gauge: Gauge
    yarn_weight: str
    rounds: List[Round]
    total_stitches: int
    estimated_yardage_m: float
```

**Dependencies:**
- ARCH-1 (algorithm spike provides context)

**Definition of Done:**
- [ ] Schema validates sample patterns
- [ ] Pydantic models pass type checking
- [ ] TypeScript types match Pydantic models
- [ ] Documentation explains all fields
- [ ] Tests verify validation rules
- [ ] Code reviewed and merged

---

##### Story ARCH-3: API Contract Definition

**Story ID:** ARCH-3
**Title:** Document all API endpoints with request/response models
**Epic:** EPIC D — App Shell & Setup
**Effort:** 5 story points
**Priority:** P0 (Critical Path)
**Complexity:** Medium
**Owner:** Backend Lead + Frontend Lead

**Description:**
Define the REST API contract for all endpoints that will be implemented during the MVP. Document request/response formats, error codes, and validation rules.

**User Story:**
As a frontend developer, I want a clear API contract so that I can build UI screens while the backend is being implemented.

**Technical Requirements:**
- Document all endpoints with HTTP methods
- Define request/response schemas
- Standardize error response format
- Include authentication placeholders
- Version API (v1)

**Acceptance Criteria:**
- [ ] API contract document created: `docs/api-contract.md`
- [ ] Endpoints documented:
  - `POST /api/v1/patterns/generate` — Generate pattern
  - `GET /api/v1/patterns/{id}` — Retrieve pattern
  - `POST /api/v1/patterns/{id}/export` — Export pattern (PDF/SVG)
  - `GET /health` — Health check
- [ ] For each endpoint:
  - HTTP method and path
  - Request schema (JSON)
  - Response schema (200 OK)
  - Error responses (4xx, 5xx)
  - Example requests/responses
- [ ] Error response format standardized:
  ```json
  {
    "error": {
      "code": "VALIDATION_ERROR",
      "message": "Invalid gauge value",
      "details": { "field": "gauge.sts_per_10cm" }
    }
  }
  ```
- [ ] API versioning strategy documented (URL path: `/api/v1/`)
- [ ] Authentication approach defined (deferred for MVP, but placeholder added)

**Technical Implementation Notes:**
Example endpoint definition:
```markdown
### POST /api/v1/patterns/generate

Generate a crochet pattern based on input parameters.

**Request:**
```json
{
  "shape": "sphere",
  "diameter_cm": 10,
  "gauge": {
    "sts_per_10cm": 12,
    "rows_per_10cm": 14
  },
  "yarn_weight": "DK",
  "stitch_type": "sc"
}
```

**Response (201 Created):**
```json
{
  "id": "uuid",
  "pattern": { /* DSL object */ },
  "created_at": "2024-11-05T12:00:00Z"
}
```

**Dependencies:**
- ARCH-2 (DSL schema)

**Definition of Done:**
- [ ] Document reviewed by both backend and frontend leads
- [ ] All MVP endpoints documented
- [ ] Example requests/responses provided
- [ ] Error codes documented
- [ ] Frontend team agrees contract is sufficient

---

##### Story ARCH-4: Frontend State Architecture

**Story ID:** ARCH-4
**Title:** Choose state management approach and design store structure
**Epic:** EPIC D — App Shell & Setup
**Effort:** 3 story points
**Priority:** P0
**Complexity:** Low
**Owner:** Frontend Lead

**Description:**
Decide on the state management approach for the React Native app and design the global store structure.

**User Story:**
As a frontend developer, I want a clear state management pattern so that I can manage app state consistently.

**Technical Requirements:**
- Evaluate state management options (Zustand, Redux Toolkit, React Context)
- Design global store structure
- Document state management patterns
- Create sample store implementation

**Acceptance Criteria:**
- [ ] State management library chosen (recommendation: Zustand)
- [ ] Store structure designed for:
  - User settings (units, terminology, Kid Mode)
  - Current pattern data
  - Visualization state (current round, zoom level)
  - Export preferences
- [ ] Basic store implementation created
- [ ] Documentation explains:
  - How to add new state
  - How to update state
  - How to access state in components
- [ ] Sample usage in placeholder screens

**Technical Implementation Notes:**
```typescript
// stores/settingsStore.ts
import create from 'zustand';

interface SettingsStore {
  units: 'metric' | 'imperial';
  terminology: 'US' | 'UK';
  kidMode: boolean;
  textSize: 'small' | 'medium' | 'large';

  setUnits: (units: 'metric' | 'imperial') => void;
  setTerminology: (terminology: 'US' | 'UK') => void;
  toggleKidMode: () => void;
  setTextSize: (size: 'small' | 'medium' | 'large') => void;
}

export const useSettingsStore = create<SettingsStore>((set) => ({
  units: 'metric',
  terminology: 'US',
  kidMode: false,
  textSize: 'medium',

  setUnits: (units) => set({ units }),
  setTerminology: (terminology) => set({ terminology }),
  toggleKidMode: () => set((state) => ({ kidMode: !state.kidMode })),
  setTextSize: (textSize) => set({ textSize }),
}));
```

**Dependencies:**
- SETUP-5 (frontend scaffold)

**Definition of Done:**
- [ ] Store created and importable
- [ ] Sample usage in at least one screen
- [ ] Documentation written
- [ ] Code reviewed
- [ ] Team trained on pattern

---

##### Story ARCH-5: Accessibility Baseline

**Story ID:** ARCH-5
**Title:** Establish WCAG AA baseline and accessibility checklist
**Epic:** EPIC D — App Shell & Setup
**Effort:** 5 story points
**Priority:** P0
**Complexity:** Medium
**Owner:** Frontend Lead + QA Lead

**Description:**
Define the accessibility baseline for the app, including WCAG AA requirements, color palette verification, and initial accessibility checklist.

**User Story:**
As a user with accessibility needs, I want the app to meet WCAG AA standards so that I can use it effectively.

**Technical Requirements:**
- WCAG AA compliance checklist
- Color palette with verified contrast ratios
- Font size and scaling requirements
- Keyboard navigation requirements
- Screen reader support baseline

**Acceptance Criteria:**
- [ ] Accessibility checklist created: `docs/accessibility-checklist.md`
- [ ] Color palette defined with contrast ratios:
  - All text: 4.5:1 minimum (normal), 3:1 (large text)
  - Interactive elements: 3:1 minimum
- [ ] Font choices documented with scalability requirements
- [ ] Keyboard navigation requirements listed:
  - Tab order logical
  - All interactive elements focusable
  - Focus indicators visible
- [ ] Screen reader requirements:
  - All images have alt text
  - Form inputs have labels
  - Interactive elements have accessible names
- [ ] Testing tools identified:
  - React Native Accessibility Inspector
  - axe DevTools
  - Manual screen reader testing (VoiceOver/TalkBack)

**Technical Implementation Notes:**
```typescript
// Example accessible component
<TouchableOpacity
  accessible={true}
  accessibilityLabel="Generate sphere pattern"
  accessibilityHint="Opens form to create a new sphere pattern"
  accessibilityRole="button"
  onPress={handleGeneratePress}
>
  <Text>Generate</Text>
</TouchableOpacity>
```

**Dependencies:**
- SETUP-5 (frontend scaffold)

**Definition of Done:**
- [ ] Checklist reviewed by team
- [ ] Color palette verified with contrast checker
- [ ] Font scaling tested on devices
- [ ] Document committed to repo
- [ ] Team trained on accessibility requirements

---

## Sprint 1 Plan

### Sprint Goal

**"Foundation complete; team ready to build pattern engine"**

By the end of Sprint 1, the team should have:
- Fully functional development environment
- CI/CD pipeline preventing broken code merges
- Architecture validated and documented
- All team members productive and unblocked

### Stories Included

| Story ID | Title | Points | Owner | Status |
|----------|-------|--------|-------|--------|
| SETUP-1 | Initialize monorepo | 5 | DevOps/Backend Lead | Active |
| SETUP-2 | GitHub Actions CI/CD | 8 | DevOps Lead | Active |
| SETUP-3 | Backend project init | 5 | Backend Lead | Active |
| SETUP-4 | Pattern-engine lib init | 3 | Backend Lead | Active |
| SETUP-5 | RN/Expo app init | 5 | Frontend Lead | Active |
| SETUP-6 | Docker Compose local | 5 | DevOps/Backend Lead | Active |
| ARCH-1 | Algorithm spike | 8 | Backend Lead | Active |
| ARCH-2 | DSL schema finalization | 5 | Backend Lead | Active |
| ARCH-3 | API contract definition | 5 | Backend + Frontend Lead | Active |
| ARCH-4 | Frontend state architecture | 3 | Frontend Lead | Active |
| ARCH-5 | Accessibility baseline | 5 | Frontend + QA Lead | Active |

**Total:** 57 story points (adjusted for team capacity: aim for 40-50 completed)

### Daily Standup Focus Areas

**Week 1:**
- **Monday-Tuesday:** Repository setup, CI/CD configuration
- **Wednesday-Thursday:** Project scaffolding (backend, frontend, pattern-engine)
- **Friday:** Algorithm spike kickoff, architecture discussions

**Week 2:**
- **Monday-Tuesday:** Complete architecture spike, finalize schemas
- **Wednesday-Thursday:** Documentation, API contracts, state management
- **Friday:** Sprint review prep, accessibility baseline review

### Sprint Review Demo Plan

**Date:** End of Week 2, Friday afternoon
**Duration:** 1.5 hours
**Attendees:** Full team + stakeholders

**Demo Outline:**

1. **Monorepo & CI/CD (10 min)**
   - Show repository structure
   - Trigger a PR and watch CI run
   - Demonstrate branch protection

2. **Backend Running (10 min)**
   - Start backend with Docker Compose: `docker-compose up`
   - Hit health endpoint: `curl http://localhost:8000/health`
   - Show Swagger docs at `/docs`

3. **Frontend Running (10 min)**
   - Start Expo app: `pnpm dev`
   - Show running on iOS simulator
   - Navigate between screens (Home, Generate, Settings)

4. **Architecture Artifacts (15 min)**
   - Walk through algorithm spike document
   - Show DSL schema with sample pattern JSON
   - Review API contract definitions

5. **Development Workflow (10 min)**
   - Make a code change
   - Push to PR
   - Watch CI run and pass
   - Merge to main

6. **Q&A (15 min)**

**Success Metric:** All demos work without errors

### Sprint Retrospective Topics

**Date:** End of Week 2, Friday (after demo)
**Duration:** 1 hour
**Attendees:** Full team

**Retrospective Questions:**

1. **What went well?**
   - Setup processes that were smooth
   - Tools that worked great
   - Team collaboration highlights

2. **What could be improved?**
   - Setup blockers or pain points
   - Documentation gaps
   - Tooling issues

3. **Action items for Sprint 2:**
   - Process improvements
   - Documentation needs
   - Tool upgrades or changes

4. **Velocity calibration:**
   - Did we estimate accurately?
   - Adjust story point estimates for future sprints?

**Output:** Action items documented in `docs/retrospectives/sprint-01.md`

---

## Technical Setup Tasks

### Repository Scaffolding Checklist

- [ ] Create GitHub repository: `knit-wit`
- [ ] Initialize with README, .gitignore, LICENSE
- [ ] Configure branch protection on main:
  - Require PR before merge
  - Require status checks to pass
  - Require 1 approval minimum
  - Require up-to-date branches
- [ ] Add team members with appropriate permissions
- [ ] Create initial project board with columns:
  - Backlog
  - Sprint 1
  - In Progress
  - In Review
  - Done
- [ ] Create issue templates:
  - Bug report
  - Feature request
  - Story template

### Development Environment Setup Steps

#### Prerequisites (team member local setup)

- [ ] Install Node.js 18+
- [ ] Install pnpm: `npm install -g pnpm`
- [ ] Install Python 3.11+
- [ ] Install Docker Desktop
- [ ] Install Expo CLI: `npm install -g expo-cli`
- [ ] Install iOS Simulator (macOS) or Android Studio
- [ ] Clone repository: `git clone git@github.com:[org]/knit-wit.git`

#### Setup commands

```bash
# Install all dependencies
pnpm install

# Verify backend setup
cd apps/backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload

# Verify frontend setup
cd apps/frontend
pnpm dev
# Press 'i' for iOS, 'a' for Android

# Verify Docker setup
docker-compose up
# Backend should be running at http://localhost:8000
```

### CI/CD Pipeline Initial Configuration

**GitHub Actions Workflow:**

- [ ] Workflow file: `.github/workflows/ci.yml`
- [ ] Jobs configured:
  - Lint (ESLint, Ruff/Black)
  - Type-check (TypeScript, mypy)
  - Test (Jest, pytest)
  - Build (pnpm build, docker build)
- [ ] Caching configured:
  - pnpm store cache
  - pip cache
  - Docker layer cache
- [ ] Notifications configured (Slack or email on failure)
- [ ] Branch protection requires passing CI

**Performance Targets:**

- Typical PR build: < 5 minutes
- Cache hit rate: > 80%
- Parallel jobs reduce total time

### Documentation Structure Setup

**Create documentation structure:**

```
docs/
├── README.md                  # Documentation index
├── development/
│   ├── setup.md              # Setup guide
│   ├── contributing.md       # Contribution guidelines
│   └── coding-standards.md   # Code style guide
├── architecture/
│   ├── overview.md           # High-level architecture
│   ├── algorithm-spike.md    # Algorithm research
│   └── dsl-schema.json       # DSL JSON schema
├── api/
│   └── api-contract.md       # API endpoint documentation
├── accessibility/
│   └── accessibility-checklist.md
└── retrospectives/
    └── sprint-01.md          # Sprint retrospectives
```

**Required Documents (Phase 0):**

- [ ] `CONTRIBUTING.md` — PR workflow, commit conventions
- [ ] `docs/development/setup.md` — Local setup instructions
- [ ] `docs/architecture/algorithm-spike.md` — Spike results
- [ ] `docs/api/api-contract.md` — API endpoint specs
- [ ] `docs/accessibility/accessibility-checklist.md` — WCAG requirements

---

## Success Criteria

### Specific, Measurable Criteria for Phase Completion

1. **Infrastructure**
   - [ ] CI/CD pipeline: 100% of PRs run automated checks
   - [ ] Build success rate: > 90% (failures only due to actual bugs)
   - [ ] Pipeline speed: < 5 minutes average

2. **Development Environment**
   - [ ] Setup time: New developer productive in < 2 hours
   - [ ] Backend startup: `docker-compose up` succeeds on first try
   - [ ] Frontend startup: App loads on simulator within 2 minutes
   - [ ] Hot-reload: Code changes reflect in < 5 seconds

3. **Architecture Validation**
   - [ ] Algorithm spike: Formulas validated against 3+ known patterns
   - [ ] DSL schema: Validates sample patterns for all 3 shapes
   - [ ] API contract: Frontend and backend teams agree on endpoints

4. **Team Readiness**
   - [ ] All team members completed setup successfully
   - [ ] 100% of team can create PRs and pass CI
   - [ ] Team velocity established: 40-50 points per sprint
   - [ ] Zero blockers for starting Phase 1 work

### Quality Gates

**Quality Gate 1: Build Health**
- All CI checks pass
- Zero TypeScript errors
- Zero ESLint errors
- All tests pass (even if minimal)

**Quality Gate 2: Documentation**
- All setup steps documented
- API contract complete
- Architecture decisions documented
- Contributing guidelines clear

**Quality Gate 3: Team Consensus**
- Architecture reviewed and approved
- Tech stack decisions signed off
- Development workflow agreed upon
- Sprint 2 plan created and committed

---

## Dependencies & Blockers

### External Dependencies Needed

**Access & Accounts:**
- [ ] GitHub organization access for all team members
- [ ] Docker Hub account (if pushing images)
- [ ] Expo account (for build services, optional in Phase 0)
- [ ] Cloud provider account (AWS/GCP/Azure) — staging environment

**Software & Tools:**
- [ ] Node.js 18+ (team installs locally)
- [ ] Python 3.11+ (team installs locally)
- [ ] Docker Desktop (team installs locally)
- [ ] Git (team installs locally)

**Hardware:**
- [ ] macOS machines for iOS development (frontend team)
- [ ] Android emulator or physical devices for testing
- [ ] Sufficient RAM for running Docker + simulators (16GB minimum recommended)

### Potential Blockers and Mitigation

| Blocker | Likelihood | Impact | Mitigation Strategy |
|---------|-----------|--------|---------------------|
| **RN/Expo versioning issues** | Medium | High | Pin Expo SDK version early; test on real devices by week 2 |
| **Monorepo tooling complexity** | Medium | Medium | Use pnpm with simple config; avoid over-engineering |
| **Team members lack Docker experience** | Low | Medium | Provide Docker tutorial session; document common commands |
| **macOS vs Windows differences** | Medium | Low | Test setup on both platforms; document platform-specific steps |
| **CI/CD cache misses** | Low | Low | Monitor cache hit rates; adjust caching strategy if needed |
| **Algorithm spike takes longer than expected** | Medium | Medium | Allocate extra time; can spill into early Phase 1 if needed |

**Escalation Path:**
- Blockers identified in daily standup
- Critical blockers escalated to Engineering Lead same day
- Team lead unblocks within 24 hours or re-prioritizes work

---

## Risks

### Phase-Specific Risks

**Risk 1: Setup Complexity Delays Development**

- **Description:** Monorepo + Docker + RN/Expo setup more complex than expected
- **Probability:** Medium
- **Impact:** Medium (delays feature work by 3-5 days)
- **Mitigation:**
  - Start setup tasks Day 1
  - Pair program on tricky setup steps
  - Document setup issues as they arise
- **Contingency:**
  - If setup takes > 1 week, simplify architecture (remove Docker requirement for local dev)

**Risk 2: Algorithm Spike Invalidates Approach**

- **Description:** Math doesn't work as expected; need to rethink algorithms
- **Probability:** Low
- **Impact:** High (requires architecture redesign)
- **Mitigation:**
  - Validate math with crochet expert early
  - Test against multiple known patterns
  - Have backup algorithms researched
- **Contingency:**
  - Extend Phase 0 by 1 week if major rework needed
  - Defer complex shapes (cone) to Phase 2

**Risk 3: Team Unfamiliarity with Tech Stack**

- **Description:** Team members need time to learn FastAPI, React Native, or Expo
- **Probability:** Medium
- **Impact:** Medium (slower velocity in early sprints)
- **Mitigation:**
  - Provide learning resources and tutorials
  - Pair experienced engineers with newcomers
  - Schedule architecture sync meetings for knowledge transfer
- **Contingency:**
  - Adjust Sprint 2 velocity down if needed
  - Bring in contractor for short-term boost if critical

**Risk 4: CI/CD Pipeline Unreliable**

- **Description:** Flaky tests, intermittent failures, long build times
- **Probability:** Low
- **Impact:** High (blocks merges, frustrates team)
- **Mitigation:**
  - Use GitHub Actions with proven setups
  - Monitor build times and optimize early
  - Isolate flaky tests immediately
- **Contingency:**
  - Temporarily disable flaky tests and file bugs
  - Increase cache usage or parallelize jobs

### Mitigation Strategies

**For All Risks:**

1. **Early Detection:**
   - Daily standup: Ask "Are you blocked?"
   - Monitor CI/CD metrics daily
   - Sprint burndown chart reviewed mid-sprint

2. **Quick Response:**
   - Blockers escalated within 24 hours
   - Team lead unblocks or adjusts plan
   - Retrospective captures lessons learned

3. **Learning Culture:**
   - Document solutions to setup issues
   - Share knowledge in team meetings
   - Update onboarding docs as we learn

### Contingency Plans

**If Phase 0 runs over 2 weeks:**

- **Week 3 Extension Plan:**
  - Complete critical setup tasks (CI/CD, monorepo)
  - Defer nice-to-have tasks (Docker optimization)
  - Start Phase 1 work in parallel for unblocked engineers
  - Adjust Sprint 2 scope to compensate

**If key team member unavailable:**

- **Backup Plan:**
  - Cross-train engineers on critical paths
  - Document decisions in writing, not just verbal
  - Have secondary owner for each epic

---

## Phase Exit Criteria

### Checklist for Moving to Phase 1

**Infrastructure:**
- [ ] Monorepo compiles and CI/CD pipeline is green
- [ ] Docker Compose brings up backend successfully
- [ ] React Native app runs on iOS and Android simulators
- [ ] All linters, type-checkers, and tests pass

**Architecture:**
- [ ] Algorithm spike completed and validated
- [ ] DSL schema defined and documented
- [ ] API contract reviewed and approved by frontend/backend teams
- [ ] State management architecture implemented

**Documentation:**
- [ ] `CONTRIBUTING.md` written and reviewed
- [ ] Setup guide tested by at least one new team member
- [ ] Architecture decisions documented (ADRs or spike docs)
- [ ] API endpoints documented with examples

**Team Readiness:**
- [ ] All team members completed local setup
- [ ] Team trained on development workflow (PRs, code review, merging)
- [ ] Sprint 2 planning complete with stories assigned
- [ ] Zero critical blockers for Phase 1 work

**Quality Gates:**
- [ ] Zero build errors in CI
- [ ] Zero critical bugs in issue tracker
- [ ] Code review coverage: 100% of merged code reviewed
- [ ] Sprint 1 retrospective completed with action items documented

### Demo Requirements

**Sprint 1 Demo Checklist:**
- [ ] Live demo of CI/CD pipeline (create PR, watch it run)
- [ ] Live demo of backend starting via Docker Compose
- [ ] Live demo of frontend running on iOS simulator
- [ ] Walkthrough of algorithm spike results
- [ ] Walkthrough of DSL schema with sample pattern
- [ ] Walkthrough of API contract documentation

**Demo Success Criteria:**
- All demos work without manual intervention
- Stakeholders can see clear progress
- Team confident in foundation for Phase 1

### Documentation Requirements

**Required Documents for Phase Exit:**

1. **`CONTRIBUTING.md`**
   - PR workflow
   - Code review process
   - Commit message conventions
   - Testing requirements

2. **`docs/development/setup.md`**
   - Prerequisites
   - Step-by-step setup instructions
   - Troubleshooting common issues
   - Verification steps

3. **`docs/architecture/algorithm-spike.md`**
   - Research findings
   - Mathematical formulas
   - Sample calculations
   - Implementation recommendations

4. **`docs/api/api-contract.md`**
   - All MVP endpoints documented
   - Request/response schemas
   - Error codes and formats
   - Example requests

5. **`docs/accessibility/accessibility-checklist.md`**
   - WCAG AA requirements
   - Color palette with contrast ratios
   - Font and text scaling requirements
   - Testing procedures

6. **`docs/retrospectives/sprint-01.md`**
   - What went well
   - What to improve
   - Action items for Sprint 2

---

## Next Phase Preview

### Link to Phase 1

**Phase 1: Core Pattern Engine (Weeks 3-4)**

After completing Phase 0 setup and architecture, Phase 1 focuses on building the core pattern generation engine.

**Key Phase 1 Deliverables:**
- Sphere pattern compiler fully functional
- Cylinder pattern compiler (with caps)
- Cone/tapered pattern compiler
- Unit test coverage > 80%
- Performance benchmarks: < 200ms per generation

**Phase 1 Epics:**
- EPIC A: Pattern Engine Implementation (shapes)
- EPIC TEST: Testing & Validation

**Phase 1 Stories (preview):**
- ENG-1: Gauge mapping & yardage estimator (5 pt)
- ENG-2: Sphere compiler (13 pt)
- ENG-3: Cylinder compiler (10 pt)
- ENG-4: Cone/tapered compiler (13 pt)
- TEST-1 to TEST-5: Comprehensive test coverage

**Transition Activities:**
- Sprint 1 retrospective action items implemented
- Sprint 2 planning session (Phase 1 kickoff)
- Architecture decisions from Phase 0 reviewed
- Pattern engine library ready for implementation

### Handoff Requirements

**From Phase 0 to Phase 1:**

1. **Codebase Ready:**
   - Pattern engine package structure created
   - Backend can import pattern engine library
   - Test framework configured and working

2. **Architecture Validated:**
   - Algorithm spike results reviewed
   - Math formulas confirmed correct
   - DSL schema locked and versioned

3. **Team Unblocked:**
   - Backend engineers trained on algorithm approach
   - Test infrastructure ready for TDD
   - CI/CD will catch regressions

4. **Documentation Current:**
   - API contract defines endpoints for pattern generation
   - DSL schema documents expected output format
   - Contributing guide explains testing standards

**Handoff Meeting Agenda:**
- Review Sprint 1 accomplishments
- Demo all working infrastructure
- Review algorithm spike findings
- Assign Phase 1 stories to engineers
- Confirm Sprint 2 commitment

---

**Document Version:** 1.0
**Last Updated:** November 5, 2024
**Next Review:** End of Sprint 1 (Week 2)

---

**For questions or clarification, contact:**
- Backend Lead (algorithm questions, pattern engine)
- Frontend Lead (app architecture, state management)
- DevOps Lead (CI/CD, Docker, infrastructure)
- Scrum Master (process, sprint planning)

---

**END OF PHASE 0 PLAN**
