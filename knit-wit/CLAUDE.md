# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Knit-Wit** is a mobile-first web application that generates parametric crochet patterns for geometric shapes and provides interactive step-by-step visualization. The MVP targets hobbyist crocheters of all skill levels with a focus on accessibility and educational features.

**Current Status**: Active Development (MVP Phase)
**Timeline**: 16 weeks across 6 phases
**Team Size**: 4-6 developers

## Core Capabilities

- Parametric pattern generation (sphere, cylinder, cone/tapered shapes)
- Interactive SVG visualization with round-by-round guidance
- Multi-format exports (PDF, SVG, JSON Pattern DSL)
- WCAG AA accessibility compliance
- Kid Mode with simplified UI and beginner-friendly copy
- US/UK terminology translation

## Architecture Overview

### High-Level Structure

```
┌─────────────────────────────────┐
│  React Native / Expo Frontend   │
│  - Screens (Home, Generate,     │
│    Visualize, Export, Settings) │
│  - SVG visualization engine     │
│  - Zustand state management     │
└──────────────┬──────────────────┘
               │ REST API (JSON)
               ▼
┌─────────────────────────────────┐
│     FastAPI Backend             │
│  - Routes: /patterns, /export   │
│  - Services: business logic     │
│  - Pydantic validation          │
└──────────────┬──────────────────┘
               │ Python import
               ▼
┌─────────────────────────────────┐
│   Pattern Engine (Python lib)   │
│  - Compiler (sphere, cylinder,  │
│    cone generators)             │
│  - Algorithms (gauge, yardage)  │
│  - DSL v0.1 (JSON format)       │
└─────────────────────────────────┘
```

### Repository Structure

```
knit-wit/
├── apps/
│   ├── mobile/              # React Native/Expo frontend
│   │   ├── src/
│   │   │   ├── screens/     # Feature-based screen components
│   │   │   ├── components/  # Reusable UI components
│   │   │   ├── services/    # API client, auth, storage
│   │   │   ├── context/     # Zustand stores
│   │   │   ├── hooks/       # Custom React hooks
│   │   │   └── theme/       # Colors, fonts, accessibility
│   │   └── __tests__/       # Jest + React Native Testing Library
│   │
│   └── api/                 # FastAPI backend
│       ├── app/
│       │   ├── api/routes/  # HTTP layer (request/response)
│       │   ├── services/    # Business logic orchestration
│       │   ├── models/      # Pydantic request/response models
│       │   ├── core/        # Config, security, constants
│       │   └── main.py      # FastAPI app initialization
│       └── tests/
│           ├── unit/        # Pure function tests
│           └── integration/ # API contract tests
│
├── packages/
│   └── pattern-engine/      # Standalone Python library
│       ├── knit_wit_engine/
│       │   ├── compiler.py  # Main entry point, factory
│       │   ├── dsl.py       # Pattern DSL v0.1 models
│       │   ├── shapes/      # Sphere, cylinder, cone generators
│       │   ├── algorithms/  # Gauge, distribution, yardage
│       │   ├── rendering/   # DSL → render primitives
│       │   └── parsing/     # Text → DSL converter
│       └── tests/           # 80%+ unit test coverage
│
├── project_plans/           # Planning artifacts
│   ├── initialization/      # Initial PRD
│   └── mvp/                 # Implementation plans, phases
│       ├── prd.md
│       ├── implementation-plan-overview.md
│       ├── phases/          # Phase-specific breakdowns
│       └── supporting-docs/ # Technical architecture, testing
│
└── docs/                    # Technical documentation
    ├── api/                 # API reference
    ├── architecture/        # System design docs
    └── deployment/          # DevOps guides
```

## Technology Stack

### Frontend (React Native / Expo)
- **Framework**: React Native 0.73+, Expo SDK 51+
- **State**: Zustand (global state)
- **Navigation**: React Navigation 6+
- **Rendering**: react-native-svg (diagrams)
- **HTTP**: axios
- **Testing**: Jest + React Native Testing Library

### Backend (FastAPI)
- **Framework**: FastAPI 0.104+
- **Runtime**: Python 3.11+
- **Server**: uvicorn (ASGI)
- **Validation**: Pydantic v2
- **Testing**: pytest, pytest-asyncio

### Pattern Engine (Python)
- **Language**: Python 3.11+
- **Data Models**: Pydantic (DSL)
- **Algorithms**: Custom parametric generation
- **Math**: Standard library (numpy optional)

### Infrastructure
- **Monorepo**: pnpm workspaces
- **CI/CD**: GitHub Actions
- **Containers**: Docker + Docker Compose
- **Deployment**: Netlify/Vercel (frontend), Railway/Render (backend)

## Development Commands

### Frontend Development
```bash
# Install dependencies
pnpm install

# Run Expo dev server
pnpm --filter mobile dev

# Run tests
pnpm --filter mobile test

# Lint and format
pnpm --filter mobile lint
pnpm --filter mobile format
```

### Backend Development
```bash
# Run FastAPI dev server (with hot reload)
pnpm --filter api dev
# or directly: uvicorn app.main:app --reload

# Run tests
pnpm --filter api test
# or directly: pytest

# Lint and format
pnpm --filter api lint  # black, isort
```

### Pattern Engine Development
```bash
# Run unit tests (80%+ coverage required)
pnpm --filter pattern-engine test
# or directly: pytest packages/pattern-engine/tests/

# Install in development mode
pip install -e packages/pattern-engine/
```

### Full Stack
```bash
# Run entire stack locally
docker-compose up

# Run all tests across monorepo
pnpm test

# Lint all packages
pnpm lint
```

## Architecture Principles

### Layered Backend Architecture

**Routes → Services → Pattern Engine**

```python
# Routes Layer (app/api/routes/)
# - HTTP request/response handling
# - OpenAPI schema generation
# - Dependency injection

# Services Layer (app/services/)
# - Business logic orchestration
# - Error handling and logging
# - Calls pattern engine

# Pattern Engine (packages/pattern-engine/)
# - Pure Python logic
# - No FastAPI dependencies
# - Fully testable in isolation
```

### Critical Rules

- ✓ **Separation of concerns**: Routes handle HTTP, services orchestrate, pattern engine computes
- ✓ **Stateless backend**: No database in MVP; patterns generated on-demand
- ✓ **API-first design**: Backend exposes clean REST API; frontend is one potential client
- ✓ **Mobile-first**: All UI optimized for touch and small screens
- ✓ **Accessibility by default**: WCAG AA compliance from start, not bolted on

### Pattern DSL v0.1 (JSON)

The core data interchange format between backend and frontend:

```json
{
  "meta": {
    "version": "0.1",
    "units": "cm",
    "terms": "US",
    "stitch": "sc",
    "round_mode": "spiral",
    "gauge": {
      "sts_per_10cm": 14,
      "rows_per_10cm": 16
    }
  },
  "object": {
    "type": "sphere",
    "params": { "diameter": 10 }
  },
  "rounds": [
    {
      "r": 1,
      "ops": [
        {"op": "MR", "count": 1},
        {"op": "sc", "count": 6}
      ],
      "stitches": 6
    }
  ],
  "materials": {
    "yarn_weight": "Worsted",
    "hook_size_mm": 4.0,
    "yardage_estimate": 25
  },
  "notes": ["Work in a spiral; use a stitch marker."]
}
```

**Op vocabulary (MVP)**: `MR` (magic ring), `sc`, `inc`, `dec`, `slst`, `ch`, `seq` (sequences)

## Key Algorithms

### Gauge Mapping
```python
# Convert physical dimensions to stitch count
stitches = dimension_cm * (sts_per_10cm / 10)

# Estimate yardage
yardage = total_stitches * stitch_multiplier * yarn_factor
```

### Even Distribution (Bresenham-like)
```python
# Distribute N increases across M stitches evenly
# Example: 6 increases in 18 stitches → [0, 3, 6, 9, 12, 15]
def bresenham_spacing(total_stitches: int, delta_changes: int):
    step = total_stitches / delta_changes
    return [int(i * step) for i in range(delta_changes)]
```

### Sphere Compilation
1. Calculate radius from diameter and gauge
2. Determine equator stitch count (circumference / stitch width)
3. Calculate increase rounds (radius / row height)
4. Distribute increases evenly (Bresenham)
5. Mirror for decrease phase

## API Endpoints

### Pattern Generation
```
POST /api/v1/patterns/generate
Content-Type: application/json

{
  "shape": "sphere",
  "diameter": 10,
  "units": "cm",
  "gauge": {"sts_per_10cm": 14, "rows_per_10cm": 16},
  "stitch": "sc",
  "terms": "US"
}

→ 201 Created
{
  "dsl": { ... },
  "assets": {"diagram_svg": "data:image/svg+xml;base64,..."},
  "exports": {"pdf_available": true}
}
```

### Visualization
```
POST /api/v1/patterns/visualize
{
  "dsl": { ... },
  "options": {"highlight_changes": true}
}

→ 200 OK
{
  "frames": [
    {
      "round": 1,
      "nodes": [...],
      "edges": [...],
      "highlights": [...]
    }
  ]
}
```

### Export
```
POST /api/v1/export/pdf
{
  "dsl": { ... },
  "options": {"include_diagram": true, "paper_size": "A4"}
}

→ 200 OK
{
  "url": "https://storage.example.com/patterns/abc123.pdf",
  "expires_at": "2024-11-30T12:00:00Z"
}
```

## Testing Strategy

### Test Pyramid
- **70% Unit tests** - Fast, comprehensive coverage of algorithms
- **20% Integration tests** - API contracts, data flow validation
- **10% E2E tests** - Critical user paths (generate → visualize → export)

### Coverage Goals
| Layer | Target | Priority |
|-------|--------|----------|
| Pattern engine | 80%+ | Critical |
| Backend services | 60%+ | High |
| Frontend components | 60%+ | Medium |
| API endpoints | 80%+ | High |

### Testing Tools
- **Backend**: pytest, pytest-asyncio, httpx (test client)
- **Frontend**: Jest, React Native Testing Library
- **E2E**: Playwright (future)
- **Accessibility**: axe-core, manual WCAG AA audits

## Performance Targets

- Pattern generation: < 200ms server-side
- Visualization frame generation: < 100ms
- API response time (p95): < 500ms
- Frontend rendering: 60 FPS

## Accessibility Requirements

### WCAG AA Compliance
- ✓ Color contrast ratios (4.5:1 for text, 3:1 for UI components)
- ✓ Screen reader labels on all interactive elements
- ✓ Keyboard navigation support (mobile: external keyboard)
- ✓ Focus indicators visible
- ✓ Touch targets ≥ 44×44 points

### Kid Mode Features
- Larger tap targets (56×56 points minimum)
- Simplified copy and beginner terminology
- Animated "what is an increase?" micro-tutorials
- Safe, friendly color palette

## Development Workflow

### Standard Feature Flow
1. **Explore**: Use `codebase-explorer` to find existing patterns
2. **Plan**: Break down into stories, estimate complexity
3. **Implement**:
   - Backend: Schema → Algorithm → Service → Route → Tests
   - Frontend: Component → Hook → Screen → Tests
4. **Test**: Unit + integration + manual verification
5. **Review**: Code review focusing on architecture patterns
6. **Document**: Update relevant docs (technical, API reference)

### Before Implementing
- Find similar implementations first (avoid reinventing)
- Understand existing conventions and patterns
- Plan affected layers/files
- Write tests alongside implementation

### Adding New Shapes
1. Create shape compiler in `packages/pattern-engine/knit_wit_engine/shapes/`
2. Inherit from `BaseShapeCompiler`
3. Implement `generate(request) → PatternDSL` method
4. Register in factory (`compiler.py`)
5. Add shape type to Pydantic enum
6. Write comprehensive unit tests (80%+ coverage)

### Adding New Stitch Types
1. Add to `StitchOp` enum in `dsl.py`
2. Update US/UK translator (`algorithms/translator.py`)
3. Add rendering style (`rendering/styles.py`)
4. Update yardage calculations (`algorithms/yardage.py`)

## Project Planning Reference

Detailed planning documents in `project_plans/mvp/`:

- **[PRD](project_plans/mvp/prd.md)** - Product requirements, use cases, acceptance criteria
- **[Implementation Plan](project_plans/mvp/implementation-plan-overview.md)** - Epic/story breakdown, timeline
- **[Technical Architecture](project_plans/mvp/supporting-docs/technical-architecture.md)** - Deep dive on system design
- **[Testing Strategy](project_plans/mvp/supporting-docs/testing-strategy.md)** - Comprehensive test approach
- **[DevOps](project_plans/mvp/supporting-docs/devops-infrastructure.md)** - CI/CD, deployment, monitoring

### Current Phase
Check `project_plans/mvp/phases/` for active phase documents with sprint goals and story assignments.

## Known Constraints

### MVP Scope Limitations
- ✗ No HDC/DC stitches (deferred to v1.1)
- ✗ No joined rounds (spiral only in MVP)
- ✗ No colorwork or stripes
- ✗ No user accounts or pattern persistence
- ✗ No community features or social sharing

### Technical Debt to Address Post-MVP
- Add database for pattern storage
- Implement user authentication (OAuth 2.0)
- Support joined rounds and multiple stitch types
- Add Redis caching for distributed deployments
- Implement background job queue for slow exports

## Error Handling

### Standard Error Response
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid gauge parameters",
    "details": {
      "field": "gauge.sts_per_10cm",
      "constraint": "must be between 6 and 25"
    }
  },
  "request_id": "req_abc123xyz"
}
```

### Error Codes
- `VALIDATION_ERROR` (400) - Invalid input data
- `NOT_FOUND` (404) - Resource not found
- `INTERNAL_ERROR` (500) - Unexpected server error
- `UNSUPPORTED_SHAPE` (400) - Shape type not implemented

## Security Considerations

### MVP Approach
- **No authentication** - Patterns are ephemeral, no user data
- **Input validation** - Multi-layer (Pydantic + business logic)
- **No sensitive data** - GDPR-compliant by design
- **Sanitization** - Strip HTML from user notes

### Future Enhancements (Post-MVP)
- OAuth 2.0 / OpenID Connect for user accounts
- JWT tokens for API access
- Rate limiting (Redis-backed)
- User pattern libraries with RLS

## Common Gotchas

### Backend
- ✗ Don't mix framework code into pattern engine (keep it pure Python)
- ✓ Always validate gauge reasonableness (prevent 1000+ stitch patterns)
- ✓ Use async/await for all FastAPI routes
- ✓ Cache pattern compilation results (deterministic output)

### Frontend
- ✗ Don't render all rounds at once (lazy render current round only)
- ✓ Use React.memo for expensive SVG components
- ✓ Implement proper loading states for API calls
- ✓ Test accessibility on actual devices, not just simulators

### Algorithms
- ✓ Test edge cases (very small/large dimensions, unusual gauges)
- ✓ Ensure increase/decrease distribution is visually even
- ✓ Validate symmetry for spheres (increase pattern mirrors decrease)

## Documentation vs AI Artifacts

| Type | Audience | Location | Use |
|------|----------|----------|-----|
| **Documentation** | Humans | `docs/`, READMEs | API reference, guides, architecture |
| **AI Artifacts** | AI agents | `.claude/`, `ai/` | Skills, agents, symbols |

When documenting:
- API docs → `docs/api/`
- Architecture decisions → `docs/architecture/`
- Deployment guides → `docs/deployment/`
- Planning artifacts → `project_plans/`

## Professional Standards

This project follows parent repository standards:
- **No emojis** unless explicitly requested
- **Concise, objective communication** - technical accuracy over enthusiasm
- **Tool-appropriate** - use Read/Write/Edit, not bash workarounds
- **Git discipline** - conventional commits, no secrets, proper attribution

## Next Steps for New Contributors

1. Read this CLAUDE.md for project context
2. Review [PRD](project_plans/initialization/initial-prd.md) for product vision
3. Set up development environment (see phase documents)
4. Check active phase in `project_plans/mvp/phases/` for current sprint
5. Pick a story aligned with your expertise
6. Follow standard feature flow (explore → plan → implement → test → review)

For questions, refer to planning documents or ask the development team.
