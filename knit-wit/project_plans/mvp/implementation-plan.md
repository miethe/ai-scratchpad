# Knit-Wit MVP — Implementation Plan

**Document Version:** 1.0
**Last Updated:** November 2024
**Status:** Active Development
**Owner:** Development Team
**Visibility:** Internal - Development Guidance

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Development Approach](#development-approach)
3. [Technical Architecture](#technical-architecture)
4. [Phase Breakdown](#phase-breakdown)
5. [Epic Breakdown](#epic-breakdown)
6. [Story Breakdown](#story-breakdown)
7. [Sprint Plan](#sprint-plan)
8. [Testing Strategy](#testing-strategy)
9. [DevOps & Infrastructure](#devops--infrastructure)
10. [Dependencies & Blockers](#dependencies--blockers)
11. [Risk Management](#risk-management)
12. [Definition of Ready/Done](#definition-of-readydone)
13. [Team Roles & Responsibilities](#team-roles--responsibilities)
14. [Timeline & Milestones](#timeline--milestones)
15. [Success Metrics & Tracking](#success-metrics--tracking)

---

## Executive Summary

### Project Overview

Knit-Wit MVP is a mobile-first web application that generates parametric crochet patterns and provides interactive visualization. Development spans approximately **16 weeks** across **6 major phases**, organized using **2-week sprints** and Agile methodology.

**Scope:**
- Pattern generation for sphere, cylinder, and cone/tapered shapes
- Interactive visualization with step-by-step guides
- Multi-format exports (PDF, SVG, JSON)
- Accessibility compliance (WCAG AA)
- Kid Mode with simplified UI

**Non-Scope (MVP):**
- Community features or social sharing
- HDC/DC stitches (defer to v1.1)
- Joined rounds (defer to v1.1)
- E-commerce integrations
- Advanced colorwork or stripes

### Timeline and Milestones

| Milestone | Target Date | Phase | Duration |
|-----------|------------|-------|----------|
| Project Kickoff | Week 1 | Prep | 1 week |
| Architecture & Setup Complete | Week 2 | Phase 1 | 2 weeks |
| Core Pattern Engine Ready | Week 4 | Phase 2 | 2 weeks |
| Basic Visualization Alpha | Week 7 | Phase 3 | 3 weeks |
| Full Feature Implementation | Week 11 | Phase 4 | 4 weeks |
| QA & Polish | Week 15 | Phase 5 | 2 weeks |
| Launch Readiness | Week 16 | Phase 6 | 1 week |

**Total Development Time:** 16 weeks (4 months)

### Team Structure Recommendations

**Recommended Team Size:** 4-6 people

| Role | Count | Responsibilities |
|------|-------|------------------|
| **Backend Lead** | 1 | Pattern engine architecture, FastAPI setup, algorithm implementation |
| **Backend Engineer(s)** | 1-2 | Pattern compilation, API endpoints, export functionality |
| **Frontend Lead** | 1 | RN/Expo setup, navigation, accessibility |
| **Frontend Engineer(s)** | 1-2 | Visualization, UI components, Kid Mode |
| **QA/Testing** | 1 | Test strategy, automation, accessibility audits |
| **DevOps** | 0-1 (shared) | CI/CD, deployment, monitoring |

**Meeting Cadence:**
- **Daily Standup:** 15 min (async or 9 AM daily)
- **Sprint Planning:** 2 hours (every 2 weeks, Monday)
- **Sprint Review & Demo:** 1.5 hours (every 2 weeks, Friday)
- **Sprint Retrospective:** 1 hour (every 2 weeks, Friday)
- **Architecture Sync:** 1 hour (weekly, as needed)

### Key Deliverables

| Deliverable | Format | Owner | Timeline |
|------------|--------|-------|----------|
| **Codebase Setup** | Git monorepo, CI/CD | DevOps Lead | Week 1-2 |
| **Pattern Compiler Library** | Python package | Backend Lead | Week 4 |
| **FastAPI Backend** | Deployed service | Backend Team | Week 5 |
| **RN/Expo Frontend** | Mobile app | Frontend Team | Week 7 |
| **Visualization Engine** | Interactive SVG renderer | Frontend Lead | Week 8 |
| **Export Module** | PDF/SVG/JSON | Backend Engineer | Week 10 |
| **Accessibility Audit Report** | Audit document | QA Lead | Week 14 |
| **Launch Package** | Release notes, docs, deployment guide | All | Week 16 |

---

## Development Approach

### Agile Methodology

**Framework:** Scrum with 2-week sprints

**Rationale:**
- Rapid feedback loops enable pattern engine validation early
- Bi-weekly demos surface visualization UX issues quickly
- Accessibility can be tested iteratively

**Sprint Capacity Assumptions:**
- Average team velocity: **40-50 story points per sprint** (6-person team)
- Sustainable pace: 6-7 hours of coding per day per engineer
- Meetings/admin: ~5 hours per week per person

### Development Phases Breakdown

```
PHASE 1: Project Setup & Architecture (Weeks 1–2)
  - Monorepo initialization
  - CI/CD pipeline
  - Spike on pattern algorithms

PHASE 2: Core Pattern Engine (Weeks 3–4)
  - Sphere compiler
  - Cylinder + caps
  - Cone/tapered shapes

PHASE 3: Visualization Foundation (Weeks 5–7)
  - RN/Expo app shell
  - DSL → render primitives
  - Basic SVG renderer

PHASE 4: Full Feature Implementation (Weeks 8–11)
  - Advanced visualization (tooltips, controls)
  - Parsing & export
  - Kid Mode & accessibility
  - Settings & telemetry

PHASE 5: QA & Polish (Weeks 12–15)
  - Cross-device testing
  - Accessibility audit
  - Performance optimization
  - Bug fixes

PHASE 6: Launch Preparation (Week 16)
  - Final smoke tests
  - Documentation
  - Deployment & monitoring setup
```

### Testing Strategy Overview

**Testing Pyramid:**

```
        /\
       /  \        E2E Tests (Selenium/Detox)
      /----\       10 % of tests, 4 weeks before launch
     /      \
    /________\      Integration Tests
   /          \     (pytest, Jest)
  /            \    20 % of tests, throughout
 /              \
/________________\ Unit Tests
                   (pytest, Jest)
                   70 % of tests, during development
```

**Test Coverage Goals:**
- Unit tests: 80%+ coverage for pattern engine & core logic
- Integration tests: 60%+ coverage for API endpoints
- E2E tests: Critical user flows only (generate → visualize → export)

### CI/CD Approach

**Pipeline Stages:**

1. **Lint & Format** (2 min)
   - ESLint, Prettier for JS/TS
   - Black, isort for Python
   - Auto-fix on PR

2. **Unit Tests** (5 min)
   - Jest for RN/Expo
   - pytest for Python

3. **Build** (10 min)
   - RN/Expo bundle
   - FastAPI + pattern-compiler package

4. **Integration Tests** (10 min)
   - API contract tests
   - Basic E2E smoke test

5. **Artifacts** (2 min)
   - Push Docker image (backend)
   - Generate APK/IPA previews (optional, weekly)

6. **Staging Deployment** (5 min, main branch only)
   - Deploy to staging environment
   - Run smoke tests

7. **Manual Approval → Production** (on-demand)

**Tools:**
- **CI/CD:** GitHub Actions
- **Artifact Storage:** GitHub Packages or DockerHub
- **Deployment:** Vercel (frontend), Railway or Render (backend), or on-premises

---

## Technical Architecture

### Repository Structure (Monorepo)

```
knit-wit/
├── apps/
│   ├── mobile/                    # React Native / Expo app
│   │   ├── src/
│   │   │   ├── screens/           # Home, Generate, Visualization, Settings
│   │   │   ├── components/        # Reusable UI components
│   │   │   ├── services/          # API client, auth, storage
│   │   │   ├── context/           # Global state (React Context or Zustand)
│   │   │   ├── hooks/             # Custom hooks
│   │   │   ├── utils/             # Helpers
│   │   │   ├── theme/             # Colors, fonts, accessibility
│   │   │   └── App.tsx            # Entry point
│   │   ├── __tests__/             # Jest tests
│   │   ├── .eslintrc.js
│   │   ├── jest.config.js
│   │   ├── app.json               # Expo config
│   │   ├── package.json
│   │   └── tsconfig.json
│   │
│   └── api/                       # FastAPI backend
│       ├── app/
│       │   ├── api/
│       │   │   ├── routes/        # Routers: /patterns, /export, /health
│       │   │   ├── models/        # Pydantic models (request/response)
│       │   │   ├── schemas/       # API schemas
│       │   │   └── deps.py        # Dependencies (auth, validation)
│       │   ├── core/
│       │   │   ├── config.py      # Settings (env vars)
│       │   │   ├── security.py    # Auth, CORS
│       │   │   └── constants.py   # Shared constants
│       │   ├── services/          # Business logic (calls pattern_engine)
│       │   ├── middleware/        # Logging, error handling
│       │   ├── main.py            # FastAPI app initialization
│       │   └── __init__.py
│       ├── tests/
│       │   ├── conftest.py        # pytest fixtures
│       │   ├── unit/              # Unit tests
│       │   ├── integration/       # API tests
│       │   └── fixtures/          # Test data
│       ├── Dockerfile             # Multi-stage build
│       ├── requirements.txt
│       ├── pyproject.toml         # Poetry or setuptools config
│       ├── .env.example
│       └── main.py                # Entry point
│
├── packages/
│   └── pattern-engine/            # Shared Python library
│       ├── knit_wit_engine/
│       │   ├── __init__.py
│       │   ├── compiler.py        # Main compiler entry point
│       │   ├── dsl.py             # DSL models (Pydantic)
│       │   ├── shapes/
│       │   │   ├── __init__.py
│       │   │   ├── sphere.py      # Sphere generation logic
│       │   │   ├── cylinder.py    # Cylinder + caps
│       │   │   ├── cone.py        # Cone/tapered shapes
│       │   │   └── base.py        # Abstract base class
│       │   ├── algorithms/
│       │   │   ├── __init__.py
│       │   │   ├── gauge.py       # Gauge mapping
│       │   │   ├── distribution.py # Increase/decrease spacing (Bresenham)
│       │   │   ├── yardage.py     # Yarn estimation
│       │   │   └── translator.py  # US ↔ UK translation
│       │   ├── rendering/
│       │   │   ├── __init__.py
│       │   │   ├── primitives.py  # Node, edge, highlight data classes
│       │   │   ├── visualizer.py  # DSL → render primitives
│       │   │   └── styles.py      # Color palettes, defaults
│       │   ├── parsing/
│       │   │   ├── __init__.py
│       │   │   ├── text_parser.py # Text → DSL converter
│       │   │   └── grammar.py     # BNF-like grammar definition
│       │   └── utils/
│       │       ├── __init__.py
│       │       └── math.py        # Geometric helpers
│       ├── tests/
│       │   ├── conftest.py
│       │   ├── unit/
│       │   │   ├── test_sphere.py
│       │   │   ├── test_cylinder.py
│       │   │   ├── test_cone.py
│       │   │   ├── test_distribution.py
│       │   │   ├── test_translator.py
│       │   │   └── test_parser.py
│       │   ├── integration/
│       │   │   └── test_full_pipeline.py
│       │   └── fixtures/
│       │       └── sample_patterns.json
│       ├── setup.py
│       ├── pyproject.toml
│       ├── requirements.txt
│       └── README.md
│
├── docs/
│   ├── api/                       # API documentation
│   │   └── endpoints.md
│   ├── architecture/
│   │   ├── pattern-dsl.md         # DSL specification
│   │   ├── algorithm-design.md    # Detailed algorithms
│   │   └── data-flow.md           # System data flow
│   ├── frontend/
│   │   ├── component-library.md
│   │   └── accessibility.md
│   ├── deployment/
│   │   ├── setup.md
│   │   ├── ci-cd.md
│   │   └── monitoring.md
│   └── CONTRIBUTING.md
│
├── .github/
│   ├── workflows/
│   │   ├── test.yml               # Run tests on PR
│   │   ├── lint.yml               # Lint & format checks
│   │   ├── build.yml              # Build artifacts
│   │   └── deploy.yml             # Deploy to staging/prod
│   └── ISSUE_TEMPLATE/
│       ├── bug.md
│       ├── feature.md
│       └── epic.md
│
├── .gitignore
├── docker-compose.yml             # Local dev environment
├── .env.example
├── pnpm-workspace.yaml            # or lerna.json for monorepo management
├── package.json                   # Root package.json (scripts, dependencies)
├── README.md
├── LICENSE
└── project_plans/
    ├── initialization/
    │   └── initial-prd.md
    ├── mvp/
    │   ├── prd.md
    │   └── implementation-plan.md (this file)
    └── roadmap/
        └── v1.1-roadmap.md (future)
```

### Frontend Architecture (React Native/Expo)

**Technology Stack:**
- **Framework:** React Native 0.73+ with Expo SDK 51+
- **State Management:** Zustand or React Context (keep it lightweight)
- **Navigation:** React Navigation 6+
- **UI Components:** Custom (no heavy libs to start; react-native-paper optional later)
- **Rendering:** react-native-svg for diagrams, optional skia-react for performance
- **HTTP Client:** axios or fetch
- **Testing:** Jest + React Native Testing Library

**Architecture Pattern:** Feature-based folders

```
screens/
├── HomeScreen.tsx              # Landing + main menu
├── GenerateScreen/
│   ├── GenerateScreen.tsx      # Wizard: Shape → Params → Gauge → Review
│   ├── ShapeSelector.tsx
│   ├── ParamsForm.tsx
│   ├── GaugeConfirm.tsx
│   └── PreviewCard.tsx
├── VisualizationScreen/
│   ├── VisualizationScreen.tsx # Main visualization controller
│   ├── PatternFrame.tsx        # Single round view
│   ├── RoundScrubber.tsx       # Navigation slider
│   ├── StitchTooltip.tsx
│   ├── LegendOverlay.tsx       # Color key
│   ├── ExplainDrawer.tsx       # Round explanation
│   └── VisualizationRenderer.tsx
├── ExportScreen/
│   ├── ExportScreen.tsx        # Choose format + download
│   ├── PDFPreview.tsx
│   └── ShareCard.tsx
└── SettingsScreen/
    ├── SettingsScreen.tsx      # Preferences
    ├── AccessibilitySettings.tsx
    ├── UnitsToggle.tsx
    └── KidModeToggle.tsx
```

**State Management (Zustand example):**
```typescript
// stores/patternStore.ts
interface PatternStore {
  pattern: Pattern | null
  setPattern: (pattern: Pattern) => void
  generatePattern: (params: GenerateRequest) => Promise<void>
  // ... other actions
}

// stores/uiStore.ts
interface UIStore {
  currentRound: number
  selectedStitch: Stitch | null
  kidMode: boolean
  handedness: 'right' | 'left'
  terms: 'US' | 'UK'
  // ... setters
}
```

### Backend Architecture (FastAPI)

**Technology Stack:**
- **Framework:** FastAPI 0.104+
- **ASGI Server:** uvicorn
- **Data Validation:** Pydantic v2
- **Database:** Not in MVP (patterns are stateless)
- **Async:** asyncio (built-in to FastAPI)
- **Logging:** structlog or standard logging
- **Error Handling:** Custom exception classes

**API Structure:**

```
/api/v1/
├── /patterns/
│   ├── POST /generate           # Generate pattern from params
│   ├── POST /visualize          # DSL → render primitives
│   └── POST /parse-text         # Text → DSL converter
├── /export/
│   ├── POST /pdf                # Pattern → PDF
│   └── POST /svg                # Pattern → SVG/PNG
└── /health/
    └── GET /                    # Health check + version
```

**Request/Response Models (Pydantic):**

```python
# app/api/models/pattern.py

class GaugeInput(BaseModel):
    sts_per_10cm: float
    rows_per_10cm: float

class GenerateRequest(BaseModel):
    shape: Literal['sphere', 'cylinder', 'cone']
    diameter: float = Field(..., gt=0, le=50)
    height: Optional[float] = Field(default=None, gt=0, le=100)
    units: Literal['cm', 'in'] = 'cm'
    gauge: GaugeInput
    stitch: Literal['sc'] = 'sc'  # MVP only
    round_mode: Literal['spiral'] = 'spiral'  # MVP only
    terms: Literal['US', 'UK'] = 'US'

class PatternDSL(BaseModel):
    meta: PatternMeta
    object: ShapeObject
    rounds: List[Round]
    materials: MaterialSpec
    notes: List[str]

class GenerateResponse(BaseModel):
    dsl: PatternDSL
    assets: Dict[str, str]  # diagram_svg, preview_png
    exports: Dict[str, bool]  # pdf_available
```

**Dependency Injection (FastAPI deps):**

```python
# app/api/deps.py

async def get_pattern_compiler() -> PatternCompiler:
    return PatternCompiler()

async def validate_generate_request(req: GenerateRequest) -> GenerateRequest:
    # Validate gauge, dimensions, etc.
    return req
```

**Middleware Stack:**

```python
# app/main.py

app.add_middleware(CORSMiddleware, allow_origins=[...])
app.add_middleware(LoggingMiddleware)
app.add_middleware(ErrorHandlerMiddleware)

@app.on_event('startup')
async def startup():
    # Initialize pattern compiler, caches, etc.
    pass
```

### Pattern Engine Library (Python)

**Purpose:** Core business logic, reusable by FastAPI and potentially other frontends.

**Key Classes:**

```python
# knit_wit_engine/dsl.py

@dataclass
class StitchOp:
    op: str  # 'MR', 'sc', 'inc', 'dec', 'ch', 'slst'
    count: Optional[int] = None
    repeat: Optional[int] = None

@dataclass
class Round:
    r: int
    ops: List[StitchOp]
    stitches: int  # post-round stitch count

class PatternDSL:
    meta: PatternMeta
    object: ShapeObject
    rounds: List[Round]
    materials: MaterialSpec
    notes: List[str]

# knit_wit_engine/compiler.py

class PatternCompiler:
    def compile(self, request: GenerateRequest) -> PatternDSL:
        shape = self._get_shape_compiler(request.shape)
        return shape.generate(request)

    def _get_shape_compiler(self, shape_type: str) -> ShapeCompiler:
        # Factory pattern: return SphereCompiler, CylinderCompiler, etc.

# knit_wit_engine/shapes/sphere.py

class SphereCompiler(ShapeCompiler):
    def generate(self, request: GenerateRequest) -> PatternDSL:
        rounds = []
        # Calculate radius, equator stitches, increase rounds, etc.
        # Use even_distribution() for spacing
        return PatternDSL(meta=..., rounds=rounds, ...)

# knit_wit_engine/algorithms/distribution.py

def bresenham_spacing(total_stitches: int, delta_changes: int) -> List[int]:
    """Return indices where ±1 changes occur, evenly distributed."""
    # Use Bresenham line algorithm to avoid stacking changes
```

**Rendering Path:**

```python
# knit_wit_engine/rendering/visualizer.py

class Visualizer:
    def dsl_to_frames(self, dsl: PatternDSL, options: RenderOptions) -> List[RenderFrame]:
        frames = []
        for round_data in dsl.rounds:
            nodes, edges, highlights = self._compile_round(round_data, options)
            frame = RenderFrame(
                round=round_data.r,
                nodes=nodes,
                edges=edges,
                highlights=highlights
            )
            frames.append(frame)
        return frames

    def _compile_round(self, round_data: Round, options: RenderOptions) -> Tuple[...]:
        # Place nodes in circular pattern
        # Draw edges between consecutive stitches
        # Highlight inc/dec operations
        pass
```

---

## Phase Breakdown

### Phase 1: Project Setup & Architecture (Weeks 1–2)

**Duration:** 2 weeks
**Capacity:** ~90-100 story points
**Team:** Full team (4-6 people)

#### Goals & Deliverables

- Monorepo initialized and CI/CD pipeline running
- Development environments set up (local + staging)
- Pattern engine library scaffold and algorithm spike complete
- Team onboarded, development practices documented

#### Epics & Stories

**Epic: Setup & Infrastructure**

| Story ID | Title | Description | Effort | Status |
|----------|-------|-------------|--------|--------|
| SETUP-1 | Initialize monorepo | Create GitHub repo, configure pnpm/lerna workspaces, set root package.json | 5 pt | Active |
| SETUP-2 | GitHub Actions CI/CD | Create test, lint, build, and deploy workflows; add branch protection rules | 8 pt | Active |
| SETUP-3 | Backend project init | FastAPI skeleton, project structure, Docker setup | 5 pt | Active |
| SETUP-4 | Pattern-engine lib init | Python package structure, setup.py, initial __init__.py | 3 pt | Active |
| SETUP-5 | RN/Expo app init | Expo init, TypeScript config, basic navigation setup | 5 pt | Active |
| SETUP-6 | Docker Compose local | dev environment for backend + optional PostgreSQL | 5 pt | Active |

**Epic: Architecture & Design Spike**

| Story ID | Title | Description | Effort | Status |
|----------|-------|-------------|--------|--------|
| ARCH-1 | Algorithm spike (sphere/cylinder) | Research, prototype gauge mapping, equator calc, round distribution | 8 pt | Active |
| ARCH-2 | DSL schema finalization | Finalize JSON schema, create Pydantic models | 5 pt | Active |
| ARCH-3 | API contract definition | Document all endpoints, request/response models | 5 pt | Active |
| ARCH-4 | Frontend state architecture | Choose Zustand/Context, design store structure | 3 pt | Active |
| ARCH-5 | Accessibility baseline | WCAG AA checklist, color palette definitions, font choices | 5 pt | Active |

#### Dependencies

- GitHub repository access
- Docker + Docker Compose installed locally
- Python 3.11+, Node 18+

#### Success Criteria

- [ ] Monorepo compiles and CI/CD pipeline is green
- [ ] FastAPI app runs locally with Docker Compose
- [ ] RN/Expo app runs on iOS simulator
- [ ] Pattern engine library is importable from both backend and tests
- [ ] Team has signed-off on architecture decisions
- [ ] Development guidelines documented in CONTRIBUTING.md

#### Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| Monorepo tooling complexity | Medium | Medium | Use pnpm + simple setup; avoid Lerna until necessary |
| FastAPI learning curve | Low | Low | Use template examples; pair on initial endpoints |
| RN/Expo versioning issues | Medium | High | Pin Expo SDK version early; test on real devices week 2 |

---

### Phase 2: Core Pattern Engine (Weeks 3–4)

**Duration:** 2 weeks
**Capacity:** ~90-100 story points
**Team:** 2 backend engineers + QA

#### Goals & Deliverables

- Sphere pattern generation fully working
- Cylinder + caps generation working
- Cone/tapered shape generation working
- Unit tests covering all shapes (80%+ coverage)
- Performance targets met (< 200ms per generation)

#### Epics & Stories

**Epic: Pattern Engine — Shapes**

| Story ID | Title | Description | Effort | Status |
|----------|-------|-------------|--------|--------|
| ENG-1 | Gauge mapping & yardage | Implement gauge conversion, yarn weight lookup, yardage calc | 5 pt | Backlog |
| ENG-2 | Sphere compiler (sc, spiral) | Implement sphere.py: radius, equator rounds, inc/dec phases | 13 pt | Backlog |
| ENG-3 | Cylinder compiler (sc) | Implement cylinder.py: cap gen (hemisphere), body rounds | 10 pt | Backlog |
| ENG-4 | Cone/tapered compiler | Implement cone.py: linear taper, Bresenham distribution | 13 pt | Backlog |
| ENG-5 | Even distribution algorithm | Implement Bresenham-like spacing to avoid stacked inc/dec | 8 pt | Backlog |
| ENG-6 | US ↔ UK translator | Implement translator.py: sc↔dc, inc↔inc2, etc. mappings | 3 pt | Backlog |

**Epic: Testing & Validation**

| Story ID | Title | Description | Effort | Status |
|----------|-------|-------------|--------|--------|
| TEST-1 | Unit tests: Sphere | pytest tests for sphere.py with multiple gauges/sizes | 8 pt | Backlog |
| TEST-2 | Unit tests: Cylinder | pytest tests for cylinder.py, verify cap dimensions | 6 pt | Backlog |
| TEST-3 | Unit tests: Cone | pytest tests for cone.py, verify linear taper | 6 pt | Backlog |
| TEST-4 | Unit tests: Algorithms | pytest for distribution, translator, gauge functions | 6 pt | Backlog |
| TEST-5 | Performance bench | Benchmark < 200ms target for each shape type | 3 pt | Backlog |

#### Dependencies

- Phase 1 complete (architecture finalized)
- Algorithm spike outputs (math verified)

#### Success Criteria

- [ ] All three shapes (sphere, cylinder, cone) generate valid patterns
- [ ] Unit test coverage > 80% for pattern-engine package
- [ ] Generation time < 200ms for typical inputs (10cm sphere)
- [ ] Acceptance criteria AC-G-1 and AC-G-2 from PRD pass
- [ ] Code review approved by backend lead

#### Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| Algorithm bugs causing invalid patterns | High | High | Pair program on complex sections; extensive unit tests |
| Performance regression | Medium | Medium | Profile early and often; cache intermediate results |
| Gauge assumptions prove incorrect | Medium | Medium | Have feedback loop with PRD author; allow param tweaking |

---

### Phase 3: Visualization Foundation (Weeks 5–7)

**Duration:** 3 weeks
**Capacity:** ~135-150 story points
**Team:** 2 frontend engineers + 1 backend (export prep)

#### Goals & Deliverables

- RN/Expo app shell complete with navigation
- DSL → render primitives working (Visualizer class)
- Basic SVG renderer displaying rounds
- Interactive scrubber + step controls working
- Basic accessibility labels added

#### Epics & Stories

**Epic: App Shell & Navigation**

| Story ID | Title | Description | Effort | Status |
|----------|-------|-------------|--------|--------|
| APP-1 | Navigation stack setup | Configure React Navigation with tabs + stack | 5 pt | Backlog |
| APP-2 | HomeScreen build | Landing, menu, brief intro, start CTA | 5 pt | Backlog |
| APP-3 | SettingsScreen build | Preferences for units, terms, handedness, text size | 8 pt | Backlog |
| APP-4 | Global theme + style system | Define colors, fonts, spacing; accessibility overrides | 5 pt | Backlog |
| APP-5 | HTTP client setup | axios integration, error handling, auth stubs | 3 pt | Backlog |

**Epic: Visualization Engine**

| Story ID | Title | Description | Effort | Status |
|----------|-------|-------------|--------|--------|
| VIZ-1 | Visualizer.dsl_to_frames() | Implement render primitives conversion in pattern-engine | 13 pt | Backlog |
| VIZ-2 | SVG renderer component | React Native SVG component to render nodes, edges, highlights | 13 pt | Backlog |
| VIZ-3 | Round scrubber + stepping | Implement slider, Next/Back buttons, jump-to-round | 8 pt | Backlog |
| VIZ-4 | Stitch highlighting | Color-code inc/dec; highlight current stitch on tap | 8 pt | Backlog |
| VIZ-5 | Legend overlay | Display stitch type colors and meanings | 5 pt | Backlog |
| VIZ-6 | Basic tooltips | On-tap stitch info: "inc = 2 sc in same st" | 5 pt | Backlog |

**Epic: Pattern Display Integration**

| Story ID | Title | Description | Effort | Status |
|----------|-------|-------------|--------|--------|
| DISP-1 | VisualizationScreen layout | Main container, frame display, controls | 8 pt | Backlog |
| DISP-2 | PatternFrame component | Display single round, manage stitch nodes | 8 pt | Backlog |
| DISP-3 | Pattern text display | Show human-readable pattern alongside diagram | 5 pt | Backlog |

#### Dependencies

- Phase 2 complete (pattern engine + Visualizer class)
- Design mockups approved

#### Success Criteria

- [ ] App starts and navigates between screens
- [ ] Clicking "Visualize" on a sample pattern renders first round
- [ ] Scrubber advances round by round without errors
- [ ] SVG renders legible on iPhone 12 and mid-range Android
- [ ] All interactive controls are keyboard accessible
- [ ] Color contrast ratios meet WCAG AA

#### Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| SVG rendering performance issues on old devices | Medium | High | Profile early; consider canvas fallback if needed |
| React Navigation complexity | Low | Medium | Use simple examples; avoid nested stacks until v1.1 |
| Parity issues between Android/iOS | Medium | Medium | Test on both platforms during development |

---

### Phase 4: Full Feature Implementation (Weeks 8–11)

**Duration:** 4 weeks
**Capacity:** ~180-200 story points
**Team:** Full team

#### Goals & Deliverables

- Generation screen (form → API call → preview) working end-to-end
- Export (PDF, SVG, JSON) fully functional
- Text parser for common pattern syntax
- Kid Mode UI variant complete
- Settings screen functional
- Telemetry stubs in place

#### Epics & Stories

**Epic: Pattern Generation Flow**

| Story ID | Title | Description | Effort | Status |
|----------|-------|-------------|--------|--------|
| GEN-1 | Shape selector screen | Radio buttons or cards: sphere, cylinder, cone | 5 pt | Backlog |
| GEN-2 | Params form (shape-specific) | Dynamic fields based on shape; validation | 8 pt | Backlog |
| GEN-3 | Gauge input & confirmation | Form + visual gauge guide; confirm before proceed | 8 pt | Backlog |
| GEN-4 | Generate API integration | Call POST /patterns/generate; show spinner | 5 pt | Backlog |
| GEN-5 | Pattern preview & review | Show generated pattern, diagram, yarn estimate | 8 pt | Backlog |
| GEN-6 | Error handling & retry | Display user-friendly errors; retry button | 5 pt | Backlog |

**Epic: Export & Sharing**

| Story ID | Title | Description | Effort | Status |
|----------|-------|-------------|--------|--------|
| EXP-1 | PDF export endpoint (backend) | FastAPI POST /export/pdf; render pattern + cover page | 13 pt | Backlog |
| EXP-2 | SVG/PNG export endpoint (backend) | FastAPI POST /export/svg; return diagram | 8 pt | Backlog |
| EXP-3 | Export screen UI | Download buttons, format selector, success toast | 8 pt | Backlog |
| EXP-4 | PDF preview (mobile) | Show preview before download (optional, can defer) | 5 pt | Backlog |
| EXP-5 | Share to clipboard | Copy pattern text or JSON to clipboard | 3 pt | Backlog |

**Epic: Pattern Parsing**

| Story ID | Title | Description | Effort | Status |
|----------|-------|-------------|--------|--------|
| PARSE-1 | Text parser implementation (backend) | knit_wit_engine/parsing/text_parser.py; limited grammar | 13 pt | Backlog |
| PARSE-2 | Parser test suite | Unit tests covering common syntax variants | 8 pt | Backlog |
| PARSE-3 | Parse screen UI (mobile) | Text input, real-time feedback, paste helper | 8 pt | Backlog |
| PARSE-4 | Error messages for parse | Show which line/token failed; suggestions | 5 pt | Backlog |

**Epic: Kid Mode & Accessibility**

| Story ID | Title | Description | Effort | Status |
|----------|-------|-------------|--------|--------|
| KID-1 | Kid Mode toggle in settings | Boolean flag; theme override | 3 pt | Backlog |
| KID-2 | Kid Mode copy rewrite | "Add two in one stitch" for "inc"; simplified tooltips | 8 pt | Backlog |
| KID-3 | Larger tap targets (Kid Mode) | Buttons, sliders resized; spacing increased | 5 pt | Backlog |
| KID-4 | Animated stitch explanations | 2-3 second loop showing "what is an increase" | 13 pt | Backlog |
| KID-5 | Accessibility settings screen | Text size, high-contrast toggle, dyslexia font option | 8 pt | Backlog |
| KID-6 | Screen reader labels (full) | aria-labels on all controls; announcements on navigation | 8 pt | Backlog |

**Epic: Telemetry & Monitoring**

| Story ID | Title | Description | Effort | Status |
|----------|-------------|-------------|--------|--------|
| TEL-1 | Telemetry service setup (mobile) | Stub for event tracking; localStorage for opt-in flag | 5 pt | Backlog |
| TEL-2 | Event emission: generation | Track shape, gauge, export format on generation success | 3 pt | Backlog |
| TEL-3 | Event emission: visualization | Track round steps, pause/resume engagement | 3 pt | Backlog |
| TEL-4 | Backend logging & monitoring | Structured logging for API requests; error tracking | 5 pt | Backlog |

#### Dependencies

- Phase 3 complete (visualization working)
- Design finalized for all screens

#### Success Criteria

- [ ] End-to-end: generate sphere → visualize → export to PDF works
- [ ] Text parser handles common bracket/repeat syntax
- [ ] Kid Mode toggles successfully; UX is kid-friendly
- [ ] All interactive elements have accessibility labels
- [ ] Export files are valid (PDF printable, JSON parseable)
- [ ] Telemetry opt-in works; events are logged

#### Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| Scope creep on Kid Mode animations | Medium | Medium | Time-box to 5 hours; MVP can use simple fades |
| PDF generation library issues | Medium | High | Test early; have fallback (print-to-PDF) |
| Performance regression with full feature set | Medium | High | Profile after each phase; optimize hot paths |
| Accessibility audit failures late | Medium | High | Integrate audits into weekly testing; fix incrementally |

---

### Phase 5: QA & Polish (Weeks 12–15)

**Duration:** 4 weeks
**Capacity:** ~180-200 story points
**Team:** QA lead + 1 engineer for fixes, full team for reviews

#### Goals & Deliverables

- Cross-device testing complete (iOS 14+, Android 10+, tablets)
- Accessibility audit report with zero critical issues
- Performance profiling + optimization
- Bug list triaged and resolved
- Documentation updated

#### Epics & Stories

**Epic: Testing & Quality Assurance**

| Story ID | Title | Description | Effort | Status |
|----------|-------|-------------|--------|--------|
| QA-1 | iOS smoke tests (multiple devices) | iPhone 12, 14, SE; iOS 14, 16, 17 | 8 pt | Backlog |
| QA-2 | Android smoke tests | Pixel 5a, Samsung A10, OnePlus; Android 10-14 | 8 pt | Backlog |
| QA-3 | Tablet layout testing | iPad Air, Samsung Galaxy Tab; landscape/portrait | 5 pt | Backlog |
| QA-4 | Browser testing (web fallback) | Chrome, Safari, Firefox on macOS/Windows | 5 pt | Backlog |
| QA-5 | E2E automation (Detox or Playwright) | Critical flows: generate → visualize → export | 13 pt | Backlog |
| QA-6 | Regression test suite | Verify no breakage in previous features | 8 pt | Backlog |

**Epic: Accessibility & Compliance**

| Story ID | Title | Description | Effort | Status |
|----------|-------|-------------|--------|--------|
| A11Y-1 | WCAG AA audit (automated) | axe DevTools, Lighthouse audits | 5 pt | Backlog |
| A11Y-2 | Manual accessibility review | Keyboard nav, screen reader testing on iOS/Android | 8 pt | Backlog |
| A11Y-3 | Color contrast verification | Verify all text meets 4.5:1 (normal) or 3:1 (large) | 5 pt | Backlog |
| A11Y-4 | Accessibility audit report | Document findings, fixes, sign-off | 5 pt | Backlog |
| A11Y-5 | Dyslexia-friendly font testing | Verify legibility of dyslexia font option | 3 pt | Backlog |

**Epic: Performance Optimization**

| Story ID | Title | Description | Effort | Status |
|----------|-------|-------------|--------|--------|
| PERF-1 | Backend profiling | Measure generation time, API response times; identify hot spots | 5 pt | Backlog |
| PERF-2 | Frontend profiling | React Native performance monitor; measure frame rates | 5 pt | Backlog |
| PERF-3 | SVG optimization | Reduce diagram complexity for large patterns (100+ rounds) | 8 pt | Backlog |
| PERF-4 | Caching strategy | Cache compiler instances, DSL templates; reduce recomputation | 5 pt | Backlog |
| PERF-5 | Bundle size optimization | Tree-shake; minify; measure APK/IPA size | 5 pt | Backlog |

**Epic: Bug Fixes & Polish**

| Story ID | Title | Description | Effort | Status |
|----------|-------|-------------|--------|--------|
| BUG-1 | Triage open issues | Review all bugs reported; label priority | 3 pt | Backlog |
| BUG-2 | Critical bugs | Fix high-priority bugs (crashes, data loss, major UX issues) | 21 pt | Backlog |
| BUG-3 | Minor polish | Visual tweaks, animation refinements, copy improvements | 8 pt | Backlog |
| BUG-4 | Regression testing | Verify fixes don't break other features | 8 pt | Backlog |

**Epic: Documentation**

| Story ID | Title | Description | Effort | Status |
|----------|-------|-------------|--------|--------|
| DOC-1 | API documentation (OpenAPI/Swagger) | Auto-generate from FastAPI; publish to Swagger UI | 5 pt | Backlog |
| DOC-2 | User guide & FAQ | How-to docs for generating patterns, troubleshooting | 8 pt | Backlog |
| DOC-3 | Developer docs (README updates) | Setup, running locally, contributing guide | 5 pt | Backlog |
| DOC-4 | Release notes | Changelog, known issues, upgrade instructions | 3 pt | Backlog |

#### Dependencies

- Phase 4 complete (all features implemented)
- Test infrastructure in place

#### Success Criteria

- [ ] Zero critical bugs; all high-priority bugs fixed
- [ ] Automated E2E tests pass on iOS and Android
- [ ] WCAG AA audit: 0 critical, < 5 warnings
- [ ] Performance benchmarks meet targets (< 200ms generation, > 50 fps visualization)
- [ ] Bundle size within limits (APK < 50MB, IPA < 100MB)
- [ ] Documentation complete and reviewed

#### Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| Device fragmentation issues | Medium | Medium | Test on 4-5 representative devices; use CI for some tests |
| Accessibility audit failures | Medium | High | Fix iteratively; involve accessibility consultant if needed |
| Last-minute performance regressions | Medium | High | Profile early; avoid major refactors in this phase |
| Documentation not keeping pace | Low | Low | Assign owner; track as stories |

---

### Phase 6: Launch Preparation (Week 16)

**Duration:** 1 week
**Capacity:** ~50 story points
**Team:** Full team

#### Goals & Deliverables

- Final smoke tests and sign-off
- Deployment scripts ready
- Monitoring and alerting configured
- Go/no-go decision
- Soft launch or public release

#### Epics & Stories

**Epic: Launch Readiness**

| Story ID | Title | Description | Effort | Status |
|----------|-------|-------------|--------|--------|
| LAUNCH-1 | Final smoke tests (staging) | Run all critical flows on staging env | 5 pt | Backlog |
| LAUNCH-2 | Database migration scripts (if needed) | Verify no data loss, rollback plan | 3 pt | Backlog |
| LAUNCH-3 | Deployment runbook | Step-by-step deployment instructions | 5 pt | Backlog |
| LAUNCH-4 | Rollback plan | Document rollback procedures | 3 pt | Backlog |
| LAUNCH-5 | Monitoring setup | Dashboards, alerts, log aggregation | 8 pt | Backlog |
| LAUNCH-6 | Incident response plan | On-call schedule, escalation procedure | 3 pt | Backlog |
| LAUNCH-7 | Analytics setup | Verify telemetry pipeline, dashboards | 5 pt | Backlog |
| LAUNCH-8 | Release notes & announcement | Write blog post, social media, in-app messaging | 8 pt | Backlog |
| LAUNCH-9 | Go/no-go review | Final leadership decision | 2 pt | Backlog |

#### Dependencies

- Phase 5 complete (QA signed off)

#### Success Criteria

- [ ] Deployment to production succeeds
- [ ] Monitoring shows no errors or anomalies
- [ ] Go/no-go decision made and approved
- [ ] Release announcement published
- [ ] On-call rotation established

---

## Epic Breakdown

### EPIC A: Pattern Engine (Python)

**Owner:** Backend Lead
**Duration:** Weeks 3–4 (Phase 2)
**Total Effort:** ~80 story points

**Overview:**
Implement the core pattern compilation logic for geometric shapes (sphere, cylinder, cone). This is the most critical component; all downstream features depend on it.

**Goals:**
- Sphere, cylinder, and cone patterns generate in < 200ms
- Outputs are mathematically accurate and follow crochet conventions
- Unit tests cover edge cases and performance

**Stories:**

| ID | Title | Effort | Priority | Dependencies |
|----|-------|--------|----------|--------------|
| A1 | Gauge mapping & yardage estimator | 5 pt | P0 | None |
| A2 | Sphere compiler (sc, spiral) | 13 pt | P0 | A1 |
| A3 | Cylinder compiler (with caps) | 10 pt | P0 | A1 |
| A4 | Cone/tapered compiler (Bresenham) | 13 pt | P0 | A1 |
| A5 | Even distribution algorithm | 8 pt | P0 | None |
| A6 | US ↔ UK translator | 3 pt | P1 | None |
| A7 | Unit tests & benchmarks | 20 pt | P0 | A2, A3, A4 |

**Acceptance Criteria:**
- AC-G-1: Generating a 10 cm sphere (14/16 gauge, US sc, spiral) produces expected equator stitch count
- AC-G-2: Tapered limb 6→2 cm over 8 rounds has monotonic taper with no stacked deltas
- All unit tests pass; coverage > 80%
- Performance < 200ms for typical inputs

---

### EPIC B: Visualization (Frontend & Backend Support)

**Owner:** Frontend Lead + Backend Engineer (render primitives)
**Duration:** Weeks 5–8 (Phases 3–4)
**Total Effort:** ~90 story points

**Overview:**
Render patterns as interactive, visual step-by-step guides. Includes DSL→primitives conversion (backend) and RN SVG rendering (frontend).

**Goals:**
- Visualize any round with stitch nodes, edges, highlights
- Users can step forward/back, jump to any round
- Touch-friendly controls; keyboard accessible
- Smooth performance on mid-range devices

**Stories:**

| ID | Title | Effort | Priority | Dependencies |
|----|-------|--------|----------|--------------|
| B1 | Visualizer.dsl_to_frames() (backend) | 13 pt | P0 | A2, A3, A4 |
| B2 | SVG renderer component (frontend) | 13 pt | P0 | B1 |
| B3 | Round scrubber + step controls | 8 pt | P0 | B2 |
| B4 | Stitch highlighting (inc/dec) | 8 pt | P0 | B2 |
| B5 | Legend overlay | 5 pt | P1 | B2 |
| B6 | Basic tooltips | 5 pt | P1 | B4 |
| B7 | VisualizationScreen integration | 8 pt | P0 | B3, B4 |
| B8 | Accessibility: labels & contrast | 13 pt | P0 | B7 |
| B9 | Performance optimization | 8 pt | P1 | B2, B7 |

**Acceptance Criteria:**
- AC-V-1: Pasting pattern renders correctly; highlights appear on inc/dec
- AC-V-2: US↔UK toggle updates labels without geometry change
- AC-A11y-1: All controls have accessible labels; colors have text equivalents
- Smooth stepping on iPhone 12, mid-range Android
- Frame render time < 50ms per round

---

### EPIC C: Parsing & I/O

**Owner:** Backend Engineer + Frontend
**Duration:** Weeks 8–10 (Phase 4)
**Total Effort:** ~60 story points

**Overview:**
Enable users to paste their own patterns (limited syntax support) and export results in multiple formats (PDF, SVG, JSON).

**Goals:**
- Parse common bracket/repeat syntax (limited grammar)
- Export to PDF (printable), SVG, JSON
- User-friendly parse error messages
- PDF includes cover, materials, pattern, diagrams

**Stories:**

| ID | Title | Effort | Priority | Dependencies |
|----|-------|--------|----------|--------------|
| C1 | Text parser (backend) | 13 pt | P0 | A6 |
| C2 | Parser test suite | 8 pt | P0 | C1 |
| C3 | PDF export (backend) | 13 pt | P0 | B1 |
| C4 | SVG/PNG export (backend) | 8 pt | P1 | B1 |
| C5 | Export screen (frontend) | 8 pt | P0 | C3, C4 |
| C6 | Parse input screen (frontend) | 8 pt | P1 | C1 |

**Acceptance Criteria:**
- Parser handles `R4: [2 sc, inc] x6 (24)` syntax
- PDF exports are printable (A4/Letter)
- JSON export round-trips (export + re-parse = same pattern)
- Error messages guide users to fixes

---

### EPIC D: App Shell & Settings

**Owner:** Frontend Lead
**Duration:** Weeks 5–9 (Phases 3–4)
**Total Effort:** ~50 story points

**Overview:**
Navigation, screens, global state, settings. The infrastructure holding features together.

**Goals:**
- Smooth navigation between screens
- Settings persist across sessions
- Global theme/accessibility settings apply consistently

**Stories:**

| ID | Title | Effort | Priority | Dependencies |
|----|-------|--------|----------|--------------|
| D1 | Navigation stack setup | 5 pt | P0 | None |
| D2 | HomeScreen | 5 pt | P0 | D1 |
| D3 | SettingsScreen | 8 pt | P0 | D1 |
| D4 | Global theme system | 5 pt | P0 | None |
| D5 | Zustand store setup (global state) | 5 pt | P0 | None |
| D6 | HTTP client + error handling | 3 pt | P0 | None |
| D7 | Local storage for preferences | 3 pt | P0 | D5 |
| D8 | Accessibility options (text size, contrast) | 8 pt | P0 | D3, D4 |

**Acceptance Criteria:**
- App starts without errors
- Navigation flows smoothly
- Settings persist on re-launch
- Global font size setting applies to all screens
- High-contrast mode toggles correctly

---

### EPIC E: Kid Mode & Accessibility

**Owner:** Frontend Lead + Accessibility Specialist
**Duration:** Weeks 9–11 (Phase 4)
**Total Effort:** ~55 story points

**Overview:**
Make the app approachable for children and ensure WCAG AA compliance. Simplified UI variant, animated explanations, large buttons.

**Goals:**
- Kid Mode toggle in settings activates child-friendly UI
- All interactive elements accessible via keyboard + screen reader
- Color contrast meets WCAG AA
- Explanatory micro-animations help learners

**Stories:**

| ID | Title | Effort | Priority | Dependencies |
|----|-------|--------|----------|--------------|
| E1 | Kid Mode toggle & theme | 3 pt | P0 | D4 |
| E2 | Copy rewrite (beginner-friendly) | 8 pt | P0 | E1 |
| E3 | Larger tap targets (Kid Mode) | 5 pt | P0 | E1 |
| E4 | Stitch explanation animations | 13 pt | P1 | B2 |
| E5 | Accessibility settings screen | 8 pt | P0 | D3 |
| E6 | Screen reader labels (full coverage) | 13 pt | P0 | E1, E5 |
| E7 | Color palette verification (WCAG AA) | 5 pt | P0 | None |

**Acceptance Criteria:**
- Kid Mode activates; UI is noticeably simplified
- Keyboard navigation works on all screens
- Screen reader announces all interactive elements
- Color contrast ratios: 4.5:1 (normal), 3:1 (large text)
- Animations are smooth and under 3 seconds

---

### EPIC F: Telemetry & Monitoring

**Owner:** Backend Engineer + Frontend
**Duration:** Weeks 9–10 (Phase 4)
**Total Effort:** ~20 story points

**Overview:**
Track user engagement (opt-in) and system health. Enable data-driven improvements.

**Goals:**
- Telemetry pipeline operational
- Key events tracked (generation, visualization, export)
- Backend logging and monitoring in place

**Stories:**

| ID | Title | Effort | Priority | Dependencies |
|----|-------|--------|----------|--------------|
| F1 | Telemetry service (frontend) | 5 pt | P1 | None |
| F2 | Event emission: generation + visualization | 3 pt | P1 | F1 |
| F3 | Event emission: export + parse | 3 pt | P1 | F1 |
| F4 | Backend logging & structured logs | 5 pt | P0 | None |
| F5 | Error tracking (Sentry or similar) | 4 pt | P1 | None |

**Acceptance Criteria:**
- Opt-in toggle works; respected on app restart
- Generation events logged with shape, gauge, success/failure
- Errors are captured and traceable
- Dashboards show top events

---

## Story Breakdown

### EPIC A: Pattern Engine — Detailed Stories

#### Story A1: Gauge Mapping & Yardage Estimator

**Story ID:** A1
**Epic:** EPIC A — Pattern Engine
**Effort:** 5 story points
**Priority:** P0 (Critical Path)
**Complexity:** Low

**Title:** Gauge Mapping & Yardage Estimator

**Description:**
Implement utility functions for gauge conversions and yarn yardage estimation. These are foundational for all shape generators.

**Requirements:**
- Convert user gauge (sts/10cm, rows/10cm) into stitches per stitch and rows per stitch
- Estimate yardage based on stitch count × average stitch length + 10% waste factor
- Support common yarn weights (Baby, DK, Worsted, Bulky) with typical stitch lengths

**Acceptance Criteria:**
- [ ] `gauge_to_stitch_length(gauge: Gauge, stitch_type: str) -> float` returns stitch length in cm
- [ ] `estimate_yardage(stitch_count: int, stitch_length: float) -> float` returns meters ± 10%
- [ ] Unit tests verify conversions against known values
- [ ] Handles edge cases (very fine gauge, very coarse gauge)
- [ ] Performance: < 1ms per call

**Technical Notes:**
- Implement in `knit_wit_engine/algorithms/gauge.py`
- Use data from standard crochet gauge references
- Stitch length formula: `yarn_weight_factor × (1 / gauge.sts_per_10cm)`
- Consider building a small YAML lookup table for yarn weights

**Implementation Hints:**
```python
# knit_wit_engine/algorithms/gauge.py

YARN_WEIGHT_FACTORS = {
    'Baby': 0.5,
    'DK': 0.6,
    'Worsted': 0.7,
    'Bulky': 0.9,
    # ... etc
}

def estimate_yardage(stitch_count: int, yarn_weight: str) -> float:
    """Return yarn yardage in meters."""
    factor = YARN_WEIGHT_FACTORS[yarn_weight]
    # stitch_length ≈ factor (cm)
    # total = stitch_count × stitch_length (cm) + 10% waste
    pass
```

**Dependencies:** None (foundation story)

**Definition of Ready:**
- [ ] Yarn weight reference data sourced
- [ ] Formula validated with known patterns
- [ ] Test cases prepared

**Definition of Done:**
- [ ] Code written, tests passing
- [ ] Code reviewed and approved
- [ ] Documentation in docstring

---

#### Story A2: Sphere Compiler (SC, Spiral)

**Story ID:** A2
**Epic:** EPIC A — Pattern Engine
**Effort:** 13 story points
**Priority:** P0 (Critical Path)
**Complexity:** High

**Title:** Sphere Compiler (Single Crochet, Spiral Rounds)

**Description:**
Implement the sphere shape compiler. Given a diameter and gauge, generate a complete spiral-round sc sphere pattern with even increase and decrease spacing.

**Requirements:**
- Accept: diameter (cm), gauge (sts/10cm, rows/10cm), units (cm/in)
- Calculate: radius, equator stitch count, number of increase rounds, number of steady rounds, number of decrease rounds
- Output: PatternDSL with rounds array, each with stitch operations and final stitch count
- Ensure even distribution of increases/decreases around the circumference (no visible columns)

**Acceptance Criteria:**
- [ ] `SphereCompiler.generate(request: GenerateRequest) -> PatternDSL` returns valid DSL
- [ ] Generated pattern matches PRD example (10 cm, 14/16 gauge, 6 sc→6 inc per round)
- [ ] Equator stitch count equals computed S_eq (within ±1)
- [ ] Increases evenly spaced (no stacking visible in diagram)
- [ ] Unit test: `test_sphere_10cm_sc_spiral()` passes
- [ ] Performance: < 150ms for typical inputs

**Technical Notes:**
- File: `knit_wit_engine/shapes/sphere.py`
- Class: `SphereCompiler(ShapeCompiler)`
- Algorithm:
  1. radius = diameter / 2
  2. equator_rounds = round(gauge.rows_per_10cm × (diameter / 2) / 10)
  3. initial_count = 6 (magic ring 6 sc)
  4. equator_stitch_count = round(π × diameter × gauge.sts_per_10cm / 10)
  5. increase_rounds = ceil((equator_stitch_count - 6) / avg_increase_per_round)
  6. steady_rounds = 1–2 (optional, around equator)
  7. Mirror increases as decreases for closing
  8. Use `even_distribution()` for spacing

**Implementation Hints:**
```python
class SphereCompiler(ShapeCompiler):
    def generate(self, request: GenerateRequest) -> PatternDSL:
        radius = request.diameter / 2
        equator_stitches = self._calc_equator_stitches(request.diameter, request.gauge)
        rounds = []

        # Increase phase
        rounds.append(Round(r=1, ops=[MR(6), SC(6)], stitches=6))
        for r in range(2, increase_rounds + 1):
            inc_count = (equator_stitches - previous_count) // num_remaining_rounds
            ops = self._even_distribute_incs(previous_count, inc_count)
            rounds.append(Round(r=r, ops=ops, stitches=new_count))

        # Steady rounds (optional)
        # Decrease phase (mirror)

        return PatternDSL(...)
```

**Dependencies:**
- A1 (Gauge mapping)
- even_distribution algorithm (A5)

**Definition of Ready:**
- [ ] Algorithm validated with hand-calculated example
- [ ] Sphere algorithm documented in architecture doc
- [ ] Test fixtures prepared (multiple gauges)

**Definition of Done:**
- [ ] Code written, all unit tests pass
- [ ] Performance benchmark meets target
- [ ] Code review approved
- [ ] Docstring + inline comments clear

---

#### Story A3: Cylinder Compiler (with Caps)

**Story ID:** A3
**Epic:** EPIC A — Pattern Engine
**Effort:** 10 story points
**Priority:** P0 (Critical Path)
**Complexity:** Medium-High

**Title:** Cylinder Compiler (with Optional End Caps)

**Description:**
Implement the cylinder shape compiler. Cylinders are half-sphere cap → constant-stitch body → optional half-sphere cap.

**Requirements:**
- Accept: diameter, height, gauge, optional caps (boolean)
- Calculate: cap rounds (hemisphere), body rounds (constant stitch)
- Output: PatternDSL with cap + body + optional closing cap

**Acceptance Criteria:**
- [ ] `CylinderCompiler.generate(request)` returns valid DSL
- [ ] Body maintains constant stitch count for height calculation
- [ ] Cap (if present) uses same logic as sphere hemisphere
- [ ] Unit test: `test_cylinder_6cm_height_8cm_with_caps()` passes
- [ ] Performance: < 150ms

**Technical Notes:**
- File: `knit_wit_engine/shapes/cylinder.py`
- Class: `CylinderCompiler(ShapeCompiler)`
- Algorithm:
  1. cap_count = round(gauge.rows_per_10cm × (diameter / 4) / 10)  [hemisphere height]
  2. body_count = round(gauge.rows_per_10cm × height / 10)
  3. stitch_count = round(π × diameter × gauge.sts_per_10cm / 10)
  4. First cap: 6 sc → increase to stitch_count over cap_count rounds
  5. Body: stitch_count sc per round for body_count rounds
  6. Second cap (if enabled): decrease back to 6 sc, close

**Dependencies:**
- A1, A2, A5

**Definition of Done:**
- [ ] Code written, unit tests pass
- [ ] Handles both capped and uncapped variations
- [ ] Code review approved

---

#### Story A4: Cone/Tapered Compiler (Bresenham)

**Story ID:** A4
**Epic:** EPIC A — Pattern Engine
**Effort:** 13 story points
**Priority:** P0 (Critical Path)
**Complexity:** High

**Title:** Cone/Tapered Limb Compiler (with Bresenham Distribution)

**Description:**
Implement the cone/tapered shape compiler. Given start diameter, end diameter, and height, generate a pattern that tapers linearly without stacking increase/decrease deltas.

**Requirements:**
- Accept: diameter_start, diameter_end, height, gauge
- Calculate: number of rounds, stitch counts at each round, increase/decrease distribution
- Use Bresenham-like algorithm to avoid stacking deltas in same column
- Output: PatternDSL with smooth linear taper

**Acceptance Criteria:**
- [ ] `ConeCompiler.generate(request)` returns valid DSL
- [ ] Stitch count tapers monotonically from start to end
- [ ] No two consecutive ±1 deltas in same stitch position (column)
- [ ] Unit test: `test_cone_6cm_to_2cm_over_8cm()` passes with AC-G-2 criteria
- [ ] Performance: < 150ms

**Technical Notes:**
- File: `knit_wit_engine/shapes/cone.py`
- Class: `ConeCompiler(ShapeCompiler)`
- Algorithm:
  1. stitch_count_start = round(π × diameter_start × gauge.sts_per_10cm / 10)
  2. stitch_count_end = round(π × diameter_end × gauge.sts_per_10cm / 10)
  3. delta_total = stitch_count_start - stitch_count_end  [number of ±1 changes]
  4. rounds_count = round(gauge.rows_per_10cm × height / 10)
  5. Use Bresenham to place each delta evenly across rounds (avoid stacking)

**Bresenham Detail:**
```
For each round r in 1..rounds_count:
  target_change = round(delta_total × r / rounds_count)
  actual_change = sum of deltas placed so far
  if target_change > actual_change:
    place a dec (or inc if tapering out)
  # This spreads deltas evenly without clustering
```

**Dependencies:**
- A1, A5 (distribution algorithm)

**Definition of Done:**
- [ ] Code written, unit tests pass
- [ ] Bresenham algorithm verified against hand-calculated taper
- [ ] No stacked deltas in visualization test
- [ ] Code review approved

---

#### Story A5: Even Distribution Algorithm

**Story ID:** A5
**Epic:** EPIC A — Pattern Engine
**Effort:** 8 story points
**Priority:** P0 (Critical Path)
**Complexity:** Medium

**Title:** Even Distribution Algorithm (Increase/Decrease Spacing)

**Description:**
Implement the core algorithm for distributing increases/decreases evenly around a circumference, avoiding visible columns and stacking.

**Requirements:**
- Accept: total_stitches, num_changes (increases or decreases)
- Return: list of indices where changes occur, evenly spaced
- Avoid consecutive same-position changes in adjacent rounds
- Handle both increases and decreases

**Acceptance Criteria:**
- [ ] `even_distribution(total: int, changes: int) -> List[int]` returns valid indices
- [ ] Spacing is as even as possible (max gap = min gap + 1)
- [ ] Unit test: `test_even_distribution_6_changes_36_stitches()` places incs every 6 stitches
- [ ] Unit test: `test_even_distribution_edge_cases()` handles 1 change, large changes, etc.
- [ ] Performance: < 1ms per call

**Technical Notes:**
- File: `knit_wit_engine/algorithms/distribution.py`
- Use Bresenham or similar line-drawing algorithm
- Example: 6 increases in 36 stitches → indices [6, 12, 18, 24, 30, 36]
- For multi-round tapers, jitter the offset per round to avoid column stacking

**Implementation Hints:**
```python
def even_distribution(total_stitches: int, num_changes: int) -> List[int]:
    """Return indices where changes occur."""
    if num_changes <= 0:
        return []
    if num_changes >= total_stitches:
        return list(range(1, total_stitches + 1))

    indices = []
    gap = total_stitches / num_changes
    offset = 0
    for i in range(num_changes):
        indices.append(int(round(offset + gap)))
        offset += gap
    return indices
```

**Dependencies:** None

**Definition of Done:**
- [ ] Code written, all unit tests pass
- [ ] Docstring with examples
- [ ] Code review approved

---

#### Story A6: US ↔ UK Translator

**Story ID:** A6
**Epic:** EPIC A — Pattern Engine
**Effort:** 3 story points
**Priority:** P1
**Complexity:** Low

**Title:** US ↔ UK Terminology Translator

**Description:**
Implement term translation between US and UK crochet conventions.

**Requirements:**
- Translate stitch names: sc↔dc, hdc↔tr, inc↔inc2, dec↔dec2
- Support both directions (US→UK, UK→US)
- Handle MVP stitches (sc, inc, dec, ch, slst, MR); defer hdc/dc to v1.1

**Acceptance Criteria:**
- [ ] `translate_term(term: str, from_lang: str, to_lang: str) -> str` works
- [ ] Unit test covers all MVP terms
- [ ] Unknown terms raise clear error

**Technical Notes:**
- File: `knit_wit_engine/algorithms/translator.py`
- Simple dict lookup; no complex logic needed for MVP

**Dependencies:** None

**Definition of Done:**
- [ ] Code written, unit tests pass
- [ ] Docstring clear

---

### EPIC B: Visualization — Detailed Stories

#### Story B1: Visualizer.dsl_to_frames() (Backend)

**Story ID:** B1
**Epic:** EPIC B — Visualization
**Effort:** 13 story points
**Priority:** P0 (Critical Path)
**Complexity:** High

**Title:** Visualizer: DSL to Render Primitives Conversion

**Description:**
Implement the Visualizer class that converts a PatternDSL into render frames (list of round data with node/edge/highlight primitives).

**Requirements:**
- Accept: PatternDSL, RenderOptions (handedness, terms, contrast)
- Output: List[RenderFrame] where each frame contains nodes, edges, highlights for a single round
- Node placement in circular pattern (standard crochet visualization)
- Highlight color-coding: inc (green), dec (red), normal (gray)
- Support different terms (US/UK) in output

**Acceptance Criteria:**
- [ ] `Visualizer.dsl_to_frames(dsl, options)` returns valid frames
- [ ] Each round has correct stitch count and operation counts
- [ ] Nodes placed in roughly circular pattern, readable on mobile
- [ ] Unit test: `test_visualizer_sphere_10_rounds()` produces 10 frames
- [ ] Performance: < 50ms for 100 rounds

**Technical Notes:**
- File: `knit_wit_engine/rendering/visualizer.py`
- Classes: `Visualizer`, `RenderFrame`, `Node`, `Edge`, `Highlight` (in `primitives.py`)
- Node placement: for round with N stitches, place nodes on circle at angles 0°, 360°/N, 2×360°/N, ...
- Edge: line between consecutive stitches (with wrap-around)
- Highlight: annotation on specific stitch indices (color + label)

**Implementation Hints:**
```python
class Node:
    id: int
    type: str  # 'sc', 'inc', 'dec', 'ch', 'slst'
    x: float   # normalized 0-1, relative to bounding box
    y: float
    label: Optional[str] = None

class Edge:
    from_id: int
    to_id: int
    style: str = 'normal'

class Highlight:
    type: str  # 'inc', 'dec', 'normal'
    indices: List[int]
    color: str

class RenderFrame:
    round: int
    stitches: int
    nodes: List[Node]
    edges: List[Edge]
    highlights: List[Highlight]
```

**Dependencies:**
- A1–A4 (pattern engine generates DSL)

**Definition of Done:**
- [ ] Code written, unit tests pass
- [ ] Handles US/UK terms correctly
- [ ] Code review approved

---

#### Story B2: SVG Renderer Component (Frontend)

**Story ID:** B2
**Epic:** EPIC B — Visualization
**Effort:** 13 story points
**Priority:** P0 (Critical Path)
**Complexity:** High

**Title:** SVG Renderer Component (React Native + react-native-svg)

**Description:**
Implement the React Native component that renders RenderFrame data as interactive SVG diagrams.

**Requirements:**
- Accept: RenderFrame, options (scale, colors)
- Render: SVG with nodes, edges, highlight colors
- Interactive: tap on stitch to select; show tooltip
- Touch-friendly: nodes large enough to tap on phones
- Support right-handed and left-handed layouts

**Acceptance Criteria:**
- [ ] `<PatternFrameRenderer frame={frame} />` renders without errors
- [ ] Nodes are visible and tappable on iPhone 12, mid-range Android
- [ ] Edges connect correctly; circular pattern is recognizable
- [ ] Highlight colors match legend (green inc, red dec)
- [ ] Unit test: Jest snapshot test for sample frame
- [ ] Performance: render < 50ms on mid-range device

**Technical Notes:**
- File: `apps/mobile/src/components/PatternFrameRenderer.tsx`
- Use `react-native-svg` for SVG rendering
- Node size: 12–20pt radius depending on total stitch count
- Edge width: 1–2pt
- Test on both iOS and Android simulators
- Consider Skia or canvas fallback if performance issues

**Implementation Hints:**
```typescript
import Svg, { Circle, Line, Text } from 'react-native-svg';

export const PatternFrameRenderer: React.FC<Props> = ({ frame, scale = 1.0 }) => {
  const size = 300; // SVG canvas size (device-scaled)
  const centerX = size / 2;
  const centerY = size / 2;
  const radius = size / 2 - 20; // Leave margin

  return (
    <Svg width={size} height={size}>
      {/* Render edges first */}
      {frame.edges.map((edge) => (
        <Line key={`edge-${edge.from_id}-${edge.to_id}`} {...} />
      ))}
      {/* Render nodes on top */}
      {frame.nodes.map((node) => (
        <Circle key={`node-${node.id}`} {...} onPress={() => handleStitchTap(node)} />
      ))}
    </Svg>
  );
};
```

**Dependencies:**
- B1 (render primitives)

**Definition of Done:**
- [ ] Component renders without errors
- [ ] Tested on iOS simulator and Android emulator
- [ ] Performance meets target
- [ ] Code review approved

---

#### Story B3: Round Scrubber + Step Controls

**Story ID:** B3
**Epic:** EPIC B — Visualization
**Effort:** 8 story points
**Priority:** P0 (Critical Path)
**Complexity:** Medium

**Title:** Round Scrubber & Navigation Controls

**Description:**
Implement UI controls for navigating between rounds: horizontal slider scrubber, Next/Back buttons, jump-to-round input.

**Requirements:**
- Horizontal slider (scrubber) spanning 0 to max_rounds
- Previous/Next buttons (large, touch-friendly)
- Text input: "Jump to round X"
- Display current round number and total rounds
- Smooth animation when changing rounds

**Acceptance Criteria:**
- [ ] Scrubber is responsive and updates current round in real-time
- [ ] Previous/Next buttons are at least 44x44pt
- [ ] Jump input validates; shows error if out of range
- [ ] Scrubber position updates correctly when jumping rounds
- [ ] Unit test: Jest for button presses and scrubber state
- [ ] Accessibility: buttons have labels; slider is keyboard accessible

**Technical Notes:**
- File: `apps/mobile/src/components/RoundScrubber.tsx`
- Use `react-native` Slider (built-in or react-native-slider)
- Debounce scrubber input to avoid excessive re-renders
- Store current round in Zustand store

**Implementation Hints:**
```typescript
export const RoundScrubber: React.FC<Props> = ({ currentRound, maxRound, onRoundChange }) => {
  return (
    <View>
      <Slider
        style={{ width: '100%' }}
        minimumValue={0}
        maximumValue={maxRound}
        value={currentRound}
        onValueChange={onRoundChange}
        step={1}
      />
      <Text>Round {currentRound} of {maxRound}</Text>
      <Button title="< Previous" onPress={() => onRoundChange(currentRound - 1)} />
      <Button title="Next >" onPress={() => onRoundChange(currentRound + 1)} />
    </View>
  );
};
```

**Dependencies:**
- B2, D5 (global state)

**Definition of Done:**
- [ ] Code written, Jest tests pass
- [ ] Tested on iOS and Android
- [ ] Accessibility checks pass
- [ ] Code review approved

---

### (Remaining stories B4–B9, C1–C6, D1–D8, E1–E7, F1–F5 follow similar format)

For brevity, I'll summarize the remaining stories in a compressed format:

---

## Sprint Plan

### Sprint 1: Setup & Architecture (Week 1–2)

**Sprint Goal:** Foundation complete; team ready to build pattern engine

**Stories:**
- SETUP-1 (5pt) → SETUP-6 (5pt)
- ARCH-1 (8pt) → ARCH-5 (5pt)

**Total:** 60 pts (adjusted for team capacity)

**Standout Tasks:**
- Monorepo + GitHub Actions working
- Spike results documented
- Team comfortable with architecture

**Demo Objectives:**
- CI/CD pipeline running on every PR
- RN/Expo app compiles and runs on simulator
- Backend FastAPI app starts

---

### Sprint 2: Core Pattern Engine (Week 3–4)

**Sprint Goal:** All three shape compilers working; 80%+ test coverage

**Stories:**
- A1 (5pt), A2 (13pt), A3 (10pt), A4 (13pt), A5 (8pt)
- TEST-1 (8pt), TEST-2 (6pt), TEST-3 (6pt), TEST-4 (6pt)

**Total:** 75 pts

**Demo Objectives:**
- Generate sphere, cylinder, cone patterns
- Unit tests passing
- Performance benchmarks documented

---

### Sprint 3: Visualization Alpha (Week 5–6)

**Sprint Goal:** Pattern visualization working end-to-end for one pattern

**Stories:**
- APP-1 (5pt), APP-2 (5pt), D4 (5pt), D5 (5pt)
- B1 (13pt), B2 (13pt), B3 (8pt)

**Total:** 59 pts

**Demo Objectives:**
- User can see a generated sphere pattern visualized
- Can step through rounds
- App doesn't crash

---

### Sprint 4: Full Visualization & Start Export (Week 7–8)

**Sprint Goal:** Visualization feature-complete; export endpoints ready

**Stories:**
- B4 (8pt), B5 (5pt), B6 (5pt), B7 (8pt)
- C1 (13pt), C3 (13pt)
- APP-3 (8pt), APP-4 (5pt), APP-5 (3pt)

**Total:** 68 pts

**Demo Objectives:**
- Tooltips, highlights, legend working
- PDF export endpoint functional
- Settings screen functional

---

### Sprint 5: Generation Form & Kid Mode (Week 9–10)

**Sprint Goal:** End-to-end generate → visualize flow; Kid Mode UI

**Stories:**
- GEN-1 (5pt) → GEN-6 (5pt)
- EXP-3 (8pt), C5 (8pt)
- E1 (3pt), E2 (8pt), E3 (5pt)
- TEL-1 (5pt)

**Total:** 75 pts

**Demo Objectives:**
- User can generate a sphere pattern via form
- Export to PDF works
- Kid Mode toggles and changes UI

---

### Sprint 6: Accessibility & Polish (Week 11–12)

**Sprint Goal:** Accessibility-ready; known issues triaged

**Stories:**
- E5 (8pt), E6 (13pt), E7 (5pt)
- D6 (3pt), D7 (3pt), D8 (8pt)
- QA-1 (8pt), QA-2 (8pt)
- BUG-1 (3pt), BUG-2 (21pt)

**Total:** ~82 pts (some overlap with QA/bug triage)

**Demo Objectives:**
- WCAG AA checklist reviewed
- Cross-device tests run (iOS, Android)
- High-priority bugs fixed

---

## Testing Strategy

### Unit Testing

**Backend (Python — pytest)**

```python
# tests/unit/test_sphere.py
def test_sphere_10cm_sc_spiral_gauge_14_16():
    compiler = SphereCompiler()
    request = GenerateRequest(
        shape='sphere',
        diameter=10,
        gauge=Gauge(sts_per_10cm=14, rows_per_10cm=16),
        stitch='sc',
        round_mode='spiral',
        terms='US'
    )
    dsl = compiler.generate(request)

    # Verify equator stitches
    expected_equator = compute_expected_equator(10, 14)
    assert find_max_stitches(dsl.rounds) == expected_equator

    # Verify increases are even
    increase_positions = extract_increase_positions(dsl)
    assert are_evenly_spaced(increase_positions, tolerance=1)

def test_even_distribution_6_changes_36_stitches():
    indices = even_distribution(36, 6)
    assert indices == [6, 12, 18, 24, 30, 36]
    assert all(indices[i+1] - indices[i] == 6 for i in range(len(indices)-1))
```

**Frontend (JavaScript/TypeScript — Jest)**

```typescript
// __tests__/components/RoundScrubber.test.tsx
import { render, fireEvent } from '@testing-library/react-native';
import { RoundScrubber } from '../components/RoundScrubber';

describe('RoundScrubber', () => {
  it('should call onRoundChange when Next is pressed', () => {
    const onRoundChange = jest.fn();
    const { getByText } = render(
      <RoundScrubber currentRound={5} maxRound={20} onRoundChange={onRoundChange} />
    );

    fireEvent.press(getByText('Next >'));
    expect(onRoundChange).toHaveBeenCalledWith(6);
  });
});
```

**Coverage Goals:**
- Pattern engine: 80%+ line coverage
- API routes: 75%+ coverage
- UI components: 60%+ coverage (integration tests cover rest)

### Integration Testing

**API Integration Tests (pytest + FastAPI TestClient)**

```python
# tests/integration/test_generate_endpoint.py
def test_post_patterns_generate_sphere(client):
    response = client.post('/api/v1/patterns/generate', json={
        'shape': 'sphere',
        'diameter': 10,
        'gauge': {'sts_per_10cm': 14, 'rows_per_10cm': 16},
        # ...
    })
    assert response.status_code == 200
    data = response.json()
    assert 'dsl' in data
    assert 'assets' in data
    assert len(data['dsl']['rounds']) > 0
```

**Full Pipeline Tests (pytest)**

```python
# tests/integration/test_full_pipeline.py
def test_generate_visualize_export_pipeline():
    # 1. Generate pattern
    dsl = compiler.generate(sphere_request)

    # 2. Visualize
    frames = visualizer.dsl_to_frames(dsl, render_options)

    # 3. Export to PDF
    pdf_bytes = exporter.to_pdf(dsl)

    assert pdf_bytes is not None
    assert len(pdf_bytes) > 1000  # Sanity check size
```

### E2E Testing

**Critical User Flows (Detox for RN, or Selenium/Playwright for web)**

**Flow 1: Generate → Visualize**
```typescript
describe('Generate and Visualize Flow', () => {
  it('should generate a sphere and visualize it', async () => {
    // Tap "Generate"
    await element(by.text('Generate')).tap();

    // Select "Sphere"
    await element(by.text('Sphere')).tap();

    // Enter diameter
    await element(by.id('diameterInput')).typeText('10');

    // Enter gauge
    await element(by.id('gaugeInput')).typeText('14/16');

    // Tap "Generate"
    await element(by.text('Generate')).tap();

    // Wait for visualization
    await waitFor(element(by.id('patternFrame'))).toBeVisible();

    // Verify first round is shown
    await expect(element(by.text('Round 1'))).toBeVisible();
  });
});
```

**Flow 2: Export to PDF**
```typescript
describe('Export Flow', () => {
  it('should export to PDF', async () => {
    // ... generate pattern ...

    // Tap "Export"
    await element(by.text('Export')).tap();

    // Select "PDF"
    await element(by.text('PDF')).tap();

    // Tap "Download"
    await element(by.text('Download')).tap();

    // Verify success toast
    await expect(element(by.text('Downloaded'))).toBeVisible();
  });
});
```

### Accessibility Testing

**Automated (axe-core, Lighthouse)**
- Run in CI on every PR
- Flag critical issues, warn on warnings

**Manual Testing (weekly)**
- Keyboard navigation: Tab, Shift+Tab through all controls
- Screen reader (VoiceOver on iOS, TalkBack on Android): Verify all elements announced
- Color contrast: Use Colour Contrast Analyzer
- Zoom: Verify layout works at 200% zoom

**Accessibility Checklist:**
- [ ] All buttons have `aria-label` or visible text
- [ ] Color not the only indicator of meaning (text labels present)
- [ ] Contrast ratios: 4.5:1 normal text, 3:1 large text
- [ ] Focus visible (underline or border)
- [ ] All images have alt text (diagrams have descriptions)
- [ ] No motion that flashes > 3 times per second
- [ ] Forms have associated labels

### Performance Testing

**Backend Benchmarks**

```python
# tests/performance/test_benchmarks.py
def test_sphere_generation_benchmark(benchmark):
    request = GenerateRequest(shape='sphere', diameter=10, ...)
    compiler = PatternCompiler()

    result = benchmark(compiler.compile, request)
    assert benchmark.stats.mean < 0.2  # < 200ms
```

**Frontend Performance**

- Measure frame rendering time: use React DevTools Profiler
- Target: 60 fps (16.67 ms per frame)
- Test on real devices: iPhone 12, Pixel 5a

**Load Testing**

- Simulate 100+ concurrent requests to API
- Verify < 500ms response time under load
- Use `locust` or `k6` for load tests

---

## DevOps & Infrastructure

### Environment Setup

**Development Environment (Local)**

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
    volumes:
      - ./apps/api:/app
    command: uvicorn app.main:app --host 0.0.0.0 --reload

  mobile:
    # RN/Expo runs on local machine, not in Docker
    # Commands: `cd apps/mobile && pnpm expo start`

  postgres:  # Optional, for future versions
    image: postgres:15
    environment:
      - POSTGRES_DB=knitwit
      - POSTGRES_USER=dev
      - POSTGRES_PASSWORD=dev
    ports:
      - "5432:5432"
```

**Staging Environment (Optional)**

```yaml
# Deployed to cloud provider (Render, Railway, etc.)
# Uses same Dockerfile as production
# Environment: staging (test data, verbose logging)
```

**Production Environment**

```yaml
# Deployed to cloud provider or on-premises
# Environment: production (minimal logging, monitoring enabled)
```

### CI/CD Pipeline

**GitHub Actions Workflows**

```yaml
# .github/workflows/test.yml
name: Test

on: [pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: |
          pip install -r apps/api/requirements.txt
          cd apps/mobile && pnpm install

      - name: Lint
        run: |
          cd apps/api && black --check . && isort --check .
          cd apps/mobile && pnpm lint

      - name: Test Backend
        run: cd apps/api && pytest --cov

      - name: Test Frontend
        run: cd apps/mobile && pnpm test

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

```yaml
# .github/workflows/build-and-deploy.yml
name: Build & Deploy

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Build backend Docker image
        run: docker build -t knitwit-api:latest apps/api

      - name: Push to Docker registry
        run: docker push ${{ secrets.DOCKER_REGISTRY }}/knitwit-api:latest

      - name: Deploy to staging
        run: |
          ssh deploy@staging-server "cd /app && docker-compose pull && docker-compose up -d"

      - name: Run smoke tests
        run: |
          ./scripts/smoke-tests.sh https://staging.knitwit.app

      - name: Manual approval for production
        # Requires manual approval before continuing
```

### Deployment Strategy

**Backend (FastAPI)**

1. **Build:** Docker image with uvicorn
2. **Registry:** Push to DockerHub or GitHub Packages
3. **Deployment:**
   - **Staging:** Automatic on PR merge
   - **Production:** Manual trigger after smoke tests + approval

**Frontend (React Native/Expo)**

1. **Build:** EAS Build (Expo) or local build
2. **Distribution:**
   - **Android:** Generate APK/AAB for Google Play Store
   - **iOS:** Generate IPA for TestFlight or App Store
3. **Release:** Manual approval by product owner

**Database (Future)**

- Use managed PostgreSQL (Heroku, RDS, etc.)
- Migrations run automatically before deploy
- Backups automated daily

### Monitoring & Logging

**Backend Logging**

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
```

**Monitoring Dashboards**

- **API latency:** Histogram of response times
- **Generation time:** Breakdown by shape type
- **Error rate:** % of requests with 5xx errors
- **User engagement:** # of patterns generated, exported

**Alerting**

- Error rate > 1%: page on-call
- API latency p95 > 500ms: notify team
- Disk space > 80%: alert DevOps

**Error Tracking (Sentry)**

```python
# app/main.py
import sentry_sdk

sentry_sdk.init(
    dsn="https://xxx@sentry.io/xxx",
    environment="production",
    traces_sample_rate=0.1,
)
```

---

## Dependencies & Blockers

### External Dependencies

| Dependency | Version | Purpose | Risk | Mitigation |
|-----------|---------|---------|------|-----------|
| React Native | 0.73+ | Mobile framework | Low | Extensive testing; pin version |
| Expo SDK | 51+ | RN tooling | Low | Use official docs; ESC community |
| FastAPI | 0.104+ | Backend framework | Very Low | Mature, stable project |
| Pydantic | v2 | Data validation | Low | v2 is current standard |
| pytest | 7+ | Testing framework | Very Low | Widely used; mature |
| react-native-svg | Latest | SVG rendering | Medium | Test on devices; have canvas fallback |

### Critical Path Items

```
Phase 1 ─→ Phase 2 (Pattern Engine) ─→ Phase 3 (Visualization)
                                        ↓
                        Phase 4 (Full Features)
                        ↓
        Phase 5 (QA & Polish) ─→ Phase 6 (Launch)
```

**Critical Dependencies:**
1. Pattern engine working correctly (blocks visualization)
2. Visualization rendering (blocks export + UI)
3. Export functionality (blocks feature completeness)
4. Accessibility compliance (blocks launch)

### Potential Blockers

| Blocker | Likelihood | Impact | Workaround |
|---------|-----------|--------|-----------|
| RN/Expo build issues on macOS/Windows | Medium | High | Use Docker build; have CI as backup |
| SVG performance on old Android devices | Medium | Medium | Implement canvas/Skia fallback |
| PDF generation library quirks | Low | High | Test early; have print-to-PDF backup |
| Gauge algorithm assumptions incorrect | Low | High | Build flexibility into algorithm; user feedback loop |
| Team member departure | Low | High | Document architecture well; pair programming |

---

## Risk Management

### Technical Risks

| Risk | Probability | Impact | Mitigation | Owner |
|------|-------------|--------|-----------|-------|
| **SVG rendering too slow on mid-range Android** | Medium | High | Profile early (week 5); implement Skia or canvas fallback | Frontend Lead |
| **Pattern algorithm produces invalid geometries** | Medium | High | Extensive unit tests; hand-verify examples; user feedback | Backend Lead |
| **PDF generation library incompatibility** | Low | High | Test all dependencies in week 1; vet before commit | Backend Engineer |
| **Memory leak in RN visualization (100+ rounds)** | Low | Medium | Profile heap; implement round caching; limit displayed rounds | Frontend Engineer |
| **Expo build pipeline breaks with version update** | Low | High | Pin Expo SDK version; test upgrades in CI before main | DevOps |

### Schedule Risks

| Risk | Probability | Impact | Mitigation | Owner |
|------|-------------|--------|-----------|-------|
| **Scope creep on Kid Mode features** | High | Medium | Define Kid Mode MVP early; time-box to 5 days | Product Owner |
| **Accessibility audit finds major issues late** | Medium | High | Integrate audits from week 5; fix incrementally | QA Lead |
| **Design changes late in project** | Medium | Medium | Finalize designs by end of Phase 2; limit iterations | Product Owner |
| **Team velocity lower than estimated** | Medium | Medium | Adjust sprint scope; deprioritize Phase 4 polish | Scrum Master |

### Resource Risks

| Risk | Probability | Impact | Mitigation | Owner |
|------|-------------|--------|-----------|-------|
| **Key person becomes unavailable** | Low | High | Document architecture; cross-train team; pair program | Engineering Lead |
| **Insufficient backend capacity (1 engineer)** | Medium | Medium | Hire contractor or defer features to v1.1 | Project Lead |
| **External API/service goes down (PDF library, etc.)** | Low | Medium | Use multiple vendors; have fallback; offline mode | DevOps |

### Mitigation Strategy

**Risk Monitoring:**
- Review risks weekly in standups
- Escalate to leadership if probability/impact increases
- Update risk register each sprint

**Escalation Process:**
1. If risk becomes imminent (probability > 70%), discuss in standup
2. Assign owner to develop mitigation plan (1–2 hours)
3. Implement mitigation or escalate to project lead
4. Update timeline/scope if needed

---

## Definition of Ready/Done

### Story Readiness Criteria (Definition of Ready)

Before a story enters the sprint, it must meet ALL of these:

- [ ] **Clear Description:** 1–2 sentence summary of what needs to be done
- [ ] **Acceptance Criteria:** 3–5 testable criteria (AC-1, AC-2, etc.)
- [ ] **Effort Estimated:** Story points assigned (5, 8, 13, 21)
- [ ] **Dependencies Listed:** What other stories must be done first
- [ ] **Technical Notes:** Implementation hints, file paths, code structure
- [ ] **Definition of Done Specified:** What "done" looks like
- [ ] **No Blockers:** External dependencies resolved; no unknowns
- [ ] **Design Approved:** UI mockups (if applicable) reviewed by design

**Checklist for Story Review:**
```
Ready stories = Backlog Refinement Session (Thursday of previous sprint)
- PO presents upcoming stories
- Team asks questions, identifies gaps
- Tech Lead assigns effort
- Team says "ready" or "needs work"
```

### Story Completion Criteria (Definition of Done)

A story is **DONE** only when ALL of these are true:

- [ ] **Code Written:** Implemented per acceptance criteria
- [ ] **Tests Passing:** All unit + integration tests pass (100% green CI)
- [ ] **Code Reviewed:** 2nd engineer approved changes
- [ ] **Test Coverage:** Unit tests cover > 80% of new code paths
- [ ] **Documentation:** Docstrings, comments, external docs updated
- [ ] **Performance:** Benchmarks met (if applicable)
- [ ] **Accessibility:** Compliance checks pass (if applicable)
- [ ] **No Regressions:** Existing tests still pass
- [ ] **Merged to Main:** Code merged after review
- [ ] **Demo-Ready:** Feature works end-to-end; no obvious UX issues

**Checklist for Story Closure:**
```
Each engineer, before marking story "Done":
1. Run full test suite locally: `pnpm test && pytest`
2. Verify acceptance criteria manually
3. Create pull request, link to story
4. Request review (min 2 approvals for backend)
5. Merge after approval
6. Verify merged code deploys to staging
7. Mark story "Done" in project board
```

### Sprint Completion Criteria

A sprint is **COMPLETE** only when:

- [ ] **All Committed Stories Done:** 100% of planned stories in "Done" column
  - (or explicit carry-over to next sprint with reason)
- [ ] **Demo Successful:** All stories demoed; team + PO sign-off
- [ ] **No Critical Bugs:** Zero critical bugs introduced; high-priority bugs triaged
- [ ] **Sprint Metrics Recorded:** Velocity, burndown, blockers documented
- [ ] **Retro Completed:** Team discusses what went well, what didn't, action items
- [ ] **Next Sprint Planned:** Stories prepped for upcoming sprint

**Sprint Close Checklist (Friday afternoon):**
```
1. Run full CI suite (test, lint, build)
2. Deploy to staging if applicable
3. Triage any bugs discovered in demo
4. Document velocity (pts completed / planned)
5. Retro meeting (1 hour): discuss blockers, improvements
6. Plan next sprint (1.5 hours): estimate stories, assign owners
```

---

## Team Roles & Responsibilities

### Recommended Team Structure (4–6 people)

#### Backend Lead (1 FTE)

**Responsibilities:**
- Pattern engine architecture & implementation
- FastAPI setup & core API design
- Algorithm validation & performance profiling
- Technical code review (backend)
- Mentorship for backend engineer(s)

**Skills Required:**
- 5+ years Python development
- Algorithms & mathematics (geometry, distribution)
- FastAPI or Django experience
- Git, Docker, CI/CD familiarity

**Deliverables:**
- Pattern compiler library (EPIC A)
- Visualizer render primitives (EPIC B, part)
- Export endpoints (EPIC C)
- API documentation

#### Backend Engineer (1–2 FTE)

**Responsibilities:**
- FastAPI endpoint implementation
- Export functionality (PDF, SVG, JSON)
- Text parser implementation
- Unit test & integration test coverage
- Telemetry & logging setup

**Skills Required:**
- 3+ years Python development
- FastAPI/REST API experience
- Comfortable with algorithms
- Testing best practices (pytest)

**Deliverables:**
- Export endpoints & services (EPIC C)
- Text parser (EPIC C)
- Backend tests & monitoring

#### Frontend Lead (1 FTE)

**Responsibilities:**
- React Native & Expo architecture
- Component library & design system
- Navigation & global state setup
- Accessibility strategy & implementation
- Technical code review (frontend)
- RN-specific performance optimization

**Skills Required:**
- 5+ years React development
- 2+ years React Native
- Mobile UX best practices
- Accessibility (WCAG AA)
- Git, testing (Jest), CI/CD

**Deliverables:**
- App shell & navigation (EPIC D)
- Visualization components (EPIC B, part)
- Generation flow (EPIC part)
- Accessibility implementation (EPIC E)

#### Frontend Engineer (1–2 FTE)

**Responsibilities:**
- Screen implementation (Generate, Export, Settings)
- SVG renderer component
- UI polish & responsive design
- Mobile testing (iOS & Android devices)
- Unit tests (Jest)

**Skills Required:**
- 3+ years React development
- React Native basics
- Mobile UI/UX sensibility
- Testing (Jest)

**Deliverables:**
- Visualization component (EPIC B)
- Generation screen (EPIC part)
- Export & Settings screens (EPIC part)
- UI tests & cross-device verification

#### QA/Testing Lead (1 FTE, can be part-time)

**Responsibilities:**
- Test strategy & test plans
- Automation (E2E, API contract tests)
- Accessibility audits (manual + automated)
- Performance testing & profiling
- Bug triage & regression testing
- Devices & simulator setup

**Skills Required:**
- 3+ years QA/testing
- Accessibility (WCAG AA knowledge)
- Detox or Playwright (mobile E2E)
- Performance profiling tools
- Accessibility audit tools (axe, Lighthouse)

**Deliverables:**
- Test plans & automation (EPIC part)
- Accessibility audit report (EPIC E)
- Performance benchmarks (EPIC part)
- Cross-device test results

#### DevOps (0–1 FTE, shared or contractor)

**Responsibilities:**
- CI/CD pipeline setup & maintenance
- Docker & deployment automation
- Environment management (dev, staging, prod)
- Monitoring & alerting setup
- Secrets management

**Skills Required:**
- Docker & Kubernetes (or simpler deployment)
- GitHub Actions or similar CI/CD
- Cloud platforms (AWS, GCP, Heroku, etc.)
- Logging & monitoring tools

**Deliverables:**
- CI/CD pipeline (EPIC part)
- Deployment scripts & runbooks
- Monitoring dashboard & alerts

### Meeting Cadence & Time Commitment

| Meeting | Frequency | Duration | Attendees | Owner |
|---------|-----------|----------|-----------|-------|
| Daily Standup | Daily (async OK) | 15 min | Full team | Scrum Master |
| Sprint Planning | Every 2 weeks, Monday | 2 hours | Full team | Scrum Master + PO |
| Backlog Refinement | Every Thursday | 1 hour | PO + Tech Lead + willing engineers | PO |
| Sprint Demo | Every 2 weeks, Friday | 1.5 hours | Full team + stakeholders | Scrum Master |
| Sprint Retro | Every 2 weeks, Friday | 1 hour | Full team | Scrum Master |
| Architecture Sync | Weekly (as needed) | 1 hour | Tech Leads + interested engineers | Tech Lead |
| 1:1 Check-ins | Every 2 weeks | 30 min per person | Manager + engineer | Engineering Lead |

### Collaboration Model

**Communication Channels:**
- **Slack:** Daily updates, quick questions
- **GitHub:** Code review, issue tracking
- **Linear/Jira:** Story tracking, sprint board
- **Meetings:** Decisions, demos, planning

**Code Review Process:**
1. Engineer opens PR, links to story
2. Request review from 2nd engineer
3. Address feedback
4. Backend: min 2 approvals; Frontend: 1 approval OK
5. Merge to main branch
6. CI/CD deploys to staging

**Pair Programming:**
- Use for complex algorithms (A2, A4, B1)
- "Mob" on critical bugs
- Knowledge transfer on architecture spikes

---

## Timeline & Milestones

### High-Level Gantt Chart

```
Week  Phase         Activity                        Deliverables
────────────────────────────────────────────────────────────────
1-2   Phase 1       ┌─────┐ Setup & Architecture   Monorepo, CI/CD
                    │Setup│                         Design spike
3-4   Phase 2       │     └──────────────┐          Pattern engine
                    │       Phase 2      │          (all shapes)
5-7   Phase 3       │                    └──────┐   Visualization
                    │          Phase 3          │   alpha
8-11  Phase 4       │                           │   Full features
                    │            Phase 4        └─  Export, Kid Mode
12-15 Phase 5       │                             │  QA & polish
                    │              Phase 5        │  Accessibility
16    Phase 6       │                             │  Launch prep
                    │                Launch Prep ─┘  Production ready
```

### Major Milestones

| # | Milestone | Target Date | Phase | Success Criteria |
|---|-----------|-----------|-------|------------------|
| M1 | **Kickoff** | Week 1 | Phase 1 | Team assembled; project board set up |
| M2 | **Architecture Finalized** | End of Week 2 | Phase 1 | Design approved; algorithm spike complete; CI/CD green |
| M3 | **Pattern Engine MVP** | End of Week 4 | Phase 2 | All 3 shapes working; 80%+ test coverage; < 200ms |
| M4 | **Visualization Alpha** | End of Week 7 | Phase 3 | User can visualize a pattern; step through rounds |
| M5 | **Full Feature Implementation** | End of Week 11 | Phase 4 | Generate → Visualize → Export end-to-end works |
| M6 | **QA Sign-Off** | End of Week 15 | Phase 5 | Zero critical bugs; WCAG AA pass; performance targets met |
| M7 | **Production Launch** | Week 16 | Phase 6 | App deployed; monitoring live; go/no-go decision made |

### Release Plan

**MVP Release (Week 16)**
- Initial release to early access users or public
- Announcement & launch event
- On-call support ready

**Post-Launch Support (Weeks 17+)**
- Monitor errors & user feedback
- Patch critical bugs (48-hour turnaround)
- Collect feedback for v1.1 roadmap

**v1.1 Planning (Week 18+)**
- Retrospective on MVP
- Prioritize v1.1 features (HDC/DC, joined rounds, stripes, etc.)
- Start planning 8-week v1.1 development

---

## Success Metrics & Tracking

### KPIs for Development

| KPI | Target | How Measured | Frequency |
|-----|--------|--------------|-----------|
| **Sprint Velocity** | 40–50 pts/sprint | Completed story points / planned | Bi-weekly |
| **Test Coverage** | 80%+ (backend), 60%+ (frontend) | Coverage report from CI | Every commit |
| **Code Review Time** | < 24 hours | PR merge time from creation | Weekly |
| **Bug Escape Rate** | < 5% (phase 4+) | Bugs found in testing / total bugs | Weekly |
| **Performance: Generation** | < 200ms | Benchmark test results | Every commit |
| **Performance: Visualization** | < 50ms per round | Profile on mid-range device | Weekly |
| **Accessibility: WCAG AA** | 0 critical, < 5 warnings | Automated + manual audit | Monthly |

### Tracking Methodology

**Sprint Metrics Board:**
- Velocity chart (last 6 sprints)
- Burndown chart (planned vs actual)
- Bug/issue count by priority
- Blockers & risks log

**Accessibility Metrics:**
- Color contrast violations: 0
- Missing alt text: 0
- Keyboard navigation: 100% of controls
- Screen reader labels: 100% of interactive elements

**Performance Dashboard:**
- Generation time histogram (by shape)
- Visualization frame render time
- API latency p50/p95/p99
- Memory usage on test device

### Quality Gates

**Code Merge Gate (CI/CD):**
- [ ] All tests pass
- [ ] Linting passes
- [ ] Coverage >= threshold
- [ ] No critical SonarQube violations

**Phase Gate (End of Phase):**
- [ ] All phase stories in "Done"
- [ ] Demo successful
- [ ] No critical bugs (P0)
- [ ] Accessibility baseline met
- [ ] Performance targets met

**Launch Gate (End of Phase 6):**
- [ ] Zero critical bugs
- [ ] WCAG AA: 0 critical issues
- [ ] Performance benchmarks met
- [ ] Monitoring live & alerting configured
- [ ] On-call rotation established
- [ ] Release notes published
- [ ] Leadership sign-off

### Reporting

**Weekly Status Report** (every Friday)
- Velocity & burndown chart
- Top blockers & risks
- Upcoming milestones
- Any scope changes

**Bi-Weekly Demo** (every Friday)
- Live demo of completed features
- Q&A with stakeholders
- Feedback collected

**Sprint Retrospective** (every 2 weeks)
- What went well? What didn't?
- Action items for next sprint
- Process improvements

**Monthly Stakeholder Update** (end of month)
- Overall progress (% complete)
- Budget/burn rate (if applicable)
- Key achievements & learnings
- Roadmap preview

---

## Appendix: Quick Reference

### File Paths & Ownership

| Path | Owner | Purpose |
|------|-------|---------|
| `/apps/api/` | Backend Lead | FastAPI backend |
| `/apps/mobile/` | Frontend Lead | React Native app |
| `/packages/pattern-engine/` | Backend Lead | Pattern compiler library |
| `/docs/` | All | Documentation |
| `.github/workflows/` | DevOps | CI/CD pipeline |

### Key Technologies

**Frontend:**
- React Native 0.73+
- Expo SDK 51+
- TypeScript
- react-native-svg
- Zustand (state) or Context API
- Jest (testing)

**Backend:**
- Python 3.11+
- FastAPI
- Pydantic v2
- pytest
- Docker

**Infrastructure:**
- GitHub Actions (CI/CD)
- Docker & Docker Compose (dev)
- Cloud deployment (Render, Railway, or AWS)
- Sentry (error tracking)

### Git Workflow

```bash
# Create feature branch
git checkout -b feat/A2-sphere-compiler

# Commit with story ID
git commit -m "feat(A2): implement sphere compiler

- Calculate equator stitches based on gauge
- Distribute increases evenly
- Generate pattern DSL

Closes #123"

# Push & open PR
git push origin feat/A2-sphere-compiler

# After review, merge to main
git merge --squash feat/A2-sphere-compiler
```

### Command Reference

```bash
# Run tests
pnpm test                 # Frontend tests
pytest --cov             # Backend tests + coverage

# Run app locally
cd apps/mobile && pnpm expo start
cd apps/api && uvicorn app.main:app --reload

# Run linting
pnpm lint                # Frontend
black . && isort .       # Backend

# Build Docker image
docker build -t knitwit-api:latest apps/api

# Deploy (example)
git push main            # Triggers GitHub Actions
# → CI/CD runs tests → builds → deploys to staging
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | November 2024 | Initial implementation plan for MVP |

---

## Document Approval

**Prepared by:** Development Team
**Reviewed by:** [Tech Lead, Product Owner]
**Approved by:** [Project Lead]
**Next Review:** [Date + 2 weeks or after Phase 1]

---

**END OF IMPLEMENTATION PLAN**

This document is a living reference. Update it:
- After each sprint retrospective
- When risks materialize
- When scope changes
- Quarterly during major planning sessions

For questions or updates, contact the Backend Lead or Scrum Master.
