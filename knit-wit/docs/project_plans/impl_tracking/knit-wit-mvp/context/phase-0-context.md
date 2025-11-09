# Phase 0 Context: Project Setup & Architecture

**Last Updated:** 2025-11-09
**Phase Status:** In Progress (0% complete, 0/57 pts)
**Current Branch:** `claude/execute-phase-0-2-implementation-011CUxtD6fkCRPr7TDboHA1v`
**Active Story:** SETUP-1 (Initialize Monorepo)

---

## Current State

### What's Happening Now
- **Task:** Setting up initial monorepo structure with pnpm workspaces
- **Goal:** Create foundation for Phase 0 development (all setup stories depend on this)
- **Blocker:** None (first story in phase)

### What Exists
- Repository created with initial planning documents
- Phase plans in `project_plans/mvp/phases/`
- PRD in `project_plans/mvp/prd.md`
- Git branch for Phase 0 implementation

### What Doesn't Exist Yet
- Monorepo workspace configuration
- Project scaffolds (backend, frontend, pattern-engine)
- CI/CD pipeline
- Docker development environment
- Architecture validation (algorithms, DSL, API contracts)

---

## Key Decisions Made

### Tech Stack (Finalized)
- **Monorepo:** pnpm workspaces (chosen for performance, disk efficiency)
- **Frontend:** React Native 0.73+ / Expo SDK 51+, TypeScript
- **Backend:** FastAPI 0.104+, Python 3.11+, uvicorn
- **Pattern Engine:** Standalone Python library (no FastAPI deps)
- **State Management:** Zustand (pending implementation in ARCH-4)
- **CI/CD:** GitHub Actions
- **Containerization:** Docker + Docker Compose

### Architecture Pattern (Validated)
**Layered Backend:**
```
Routes (HTTP) → Services (orchestration) → Pattern Engine (pure logic)
```

**Key Principles:**
- Stateless backend (no database in MVP)
- API-first design (backend exposes REST, frontend consumes)
- Mobile-first UI (touch-optimized, small screens)
- Accessibility by default (WCAG AA from start)

### Repository Structure (Planned)
```
knit-wit/
├── apps/
│   ├── mobile/          # React Native/Expo (SETUP-5)
│   └── api/             # FastAPI backend (SETUP-3)
├── packages/
│   └── pattern-engine/  # Python library (SETUP-4)
├── docs/                # Technical documentation
├── .github/workflows/   # CI/CD (SETUP-2)
├── docker-compose.yml   # Local dev env (SETUP-6)
├── package.json         # Root workspace config
└── pnpm-workspace.yaml  # Workspace definitions
```

### Pattern DSL v0.1 (In Progress - ARCH-2)
**Format:** JSON with Pydantic validation

**Core Structure:**
```json
{
  "meta": { "version": "0.1", "units": "cm", "terms": "US", "gauge": {...} },
  "object": { "type": "sphere", "params": {"diameter": 10} },
  "rounds": [
    { "r": 1, "ops": [{"op": "MR", "count": 1}, {"op": "sc", "count": 6}], "stitches": 6 }
  ],
  "materials": { "yarn_weight": "Worsted", "hook_size_mm": 4.0, "yardage_estimate": 25 },
  "notes": ["Work in spiral; use stitch marker"]
}
```

**Op Vocabulary (MVP):** MR, sc, inc, dec, slst, ch, seq

---

## Technical Patterns & Standards

### Code Quality
- **Linting:** ESLint (frontend), black + isort + ruff (backend)
- **Type Checking:** TypeScript (frontend), mypy (backend)
- **Testing:** Jest + RNTL (frontend), pytest (backend)
- **Coverage Targets:**
  - Pattern engine: 80%+ (critical)
  - Backend services: 60%+
  - API endpoints: 80%+

### Git Workflow (Pending SETUP-1 completion)
- **Branching:** Feature branches from main
- **Commits:** Conventional format (`type(scope): message`)
- **PRs:** Require CI passing + 1 approval
- **Protection:** Main branch protected, requires up-to-date

### Performance Targets
- Pattern generation: < 200ms server-side
- API response (p95): < 500ms
- Frontend rendering: 60 FPS
- CI pipeline: < 5 minutes

---

## Algorithm Context (ARCH-1)

### Gauge Mapping
```python
# Physical dimensions → stitch count
stitches = dimension_cm * (sts_per_10cm / 10)
yardage = total_stitches * stitch_multiplier * yarn_factor
```

### Even Distribution (Bresenham-like)
```python
# Distribute N increases across M stitches evenly
# Example: 6 inc in 18 sts → [0, 3, 6, 9, 12, 15]
step = total_stitches / delta_changes
positions = [int(i * step) for i in range(delta_changes)]
```

### Sphere Compilation (To Validate)
1. Calculate radius from diameter + gauge
2. Determine equator stitch count (circumference / stitch width)
3. Calculate increase rounds (radius / row height)
4. Distribute increases evenly (Bresenham)
5. Mirror for decrease phase (symmetry validation required)

**Validation:** Must test against 3+ known crochet sphere patterns

---

## API Endpoints (ARCH-3)

### POST /api/v1/patterns/generate
**Request:**
```json
{
  "shape": "sphere",
  "diameter": 10,
  "units": "cm",
  "gauge": {"sts_per_10cm": 14, "rows_per_10cm": 16},
  "stitch": "sc",
  "terms": "US"
}
```

**Response (201):**
```json
{
  "dsl": {...},
  "assets": {"diagram_svg": "data:image/svg+xml;base64,..."},
  "exports": {"pdf_available": true}
}
```

### POST /api/v1/patterns/visualize
**Purpose:** Generate SVG frames for round-by-round visualization

### POST /api/v1/export/pdf
**Purpose:** Generate downloadable PDF with pattern + optional diagram

---

## Dependencies & Blockers

### Critical Path (Sequential)
1. **SETUP-1** (In Progress) → Unlocks all other SETUP stories
2. **SETUP-2, 3, 4, 5** (Parallel) → Project scaffolds + CI/CD
3. **SETUP-6** (Depends on 3 & 5) → Docker Compose full-stack
4. **ARCH-1, 2, 3, 4, 5** (Parallel, depends on respective SETUP stories)

### External Dependencies (SETUP Phase)
- GitHub organization access
- Docker Desktop installed (team members)
- Node.js 18+ installed (team members)
- Python 3.11+ installed (team members)
- pnpm installed globally

---

## Known Gotchas

### Backend
- ❌ Don't mix FastAPI code into pattern engine (keep pure Python)
- ✅ Always validate gauge reasonableness (prevent 1000+ stitch patterns)
- ✅ Use async/await for all FastAPI routes
- ✅ Cache pattern compilation (deterministic output)

### Frontend
- ❌ Don't render all rounds at once (lazy render current round)
- ✅ Use React.memo for expensive SVG components
- ✅ Implement loading states for API calls
- ✅ Test accessibility on actual devices, not just simulators

### Algorithms
- ✅ Test edge cases (very small/large dimensions, unusual gauges)
- ✅ Ensure increase/decrease distribution is visually even
- ✅ Validate symmetry for spheres (increase mirrors decrease)

---

## Quick Reference

### Run Commands (Post-Setup)
```bash
# Root level
pnpm install                  # Install all deps
pnpm test                     # Run all tests
pnpm lint                     # Lint all packages

# Frontend (SETUP-5)
pnpm --filter mobile dev      # Start Expo dev server
pnpm --filter mobile test     # Run Jest tests

# Backend (SETUP-3)
pnpm --filter api dev         # Start FastAPI (uvicorn with reload)
pnpm --filter api test        # Run pytest

# Pattern Engine (SETUP-4)
pnpm --filter pattern-engine test
pip install -e packages/pattern-engine/  # Dev mode

# Full Stack (SETUP-6)
docker-compose up             # Run everything
```

### Key Files to Create (Phase 0)
- `/package.json` - Root workspace config with scripts
- `/pnpm-workspace.yaml` - Workspace package definitions
- `/.github/workflows/ci.yml` - CI/CD pipeline
- `/apps/api/app/main.py` - FastAPI app entry point
- `/apps/mobile/App.tsx` - React Native root component
- `/packages/pattern-engine/knit_wit_engine/compiler.py` - Pattern engine entry
- `/docker-compose.yml` - Local development environment

---

## Next Steps (Story-by-Story)

### SETUP-1 (Active)
1. Create monorepo structure (`apps/`, `packages/`)
2. Configure pnpm workspaces (`package.json`, `pnpm-workspace.yaml`)
3. Add root scripts (install, build, test, lint)
4. Configure `.gitignore` (Node, Python, OS files)
5. Write README with quick-start
6. Enable branch protection on main
7. Verify `pnpm install` succeeds

### SETUP-2 (Next)
1. Create `.github/workflows/ci.yml`
2. Configure jobs: lint, type-check, test, build
3. Set up caching: pnpm, pip, Docker
4. Add branch protection rules (CI required)
5. Test with dummy PR
6. Optimize for < 5 min runtime

### SETUP-3, 4, 5 (Parallel After SETUP-1)
- **SETUP-3:** FastAPI scaffold with health check
- **SETUP-4:** Pattern engine Python package
- **SETUP-5:** Expo app with TypeScript

### Architecture Stories (After Respective SETUP Stories)
- **ARCH-1:** Algorithm validation (sphere/cylinder formulas)
- **ARCH-2:** DSL schema finalization (Pydantic models)
- **ARCH-3:** API contract documentation (OpenAPI)
- **ARCH-4:** Frontend state architecture (Zustand)
- **ARCH-5:** Accessibility baseline (WCAG AA)

---

## Learning & Observations

### To Document During Phase 0
- **Monorepo setup challenges:** Any workspace config gotchas
- **CI/CD optimization:** Caching strategies that work well
- **Docker performance:** Volume mount performance on different platforms
- **Algorithm validation:** Real-world pattern comparison findings
- **Accessibility wins:** Quick wins for WCAG AA compliance

**Log Location:** `.claude/worknotes/observations/observation-log-11-25.md` (when patterns emerge)

---

## Team Context

**Team Size:** 4-6 developers
**Roles:**
- DevOps Lead: SETUP-1, 2, 6
- Backend Lead: SETUP-3, 4 + ARCH-2, 3
- Algorithm Lead: ARCH-1
- Frontend Lead: SETUP-5 + ARCH-4, 5

**Velocity Target:** 40-50 story points per 2-week sprint
**Buffer:** 10% for learning curve and unexpected setup issues

---

## Success Signals

### Phase 0 Complete When:
- [ ] All 11 stories completed (57 pts)
- [ ] CI/CD green on main
- [ ] All team members can run full stack locally
- [ ] Algorithm validated against known patterns
- [ ] API contracts agreed upon by frontend/backend
- [ ] Accessibility baseline established

### Ready for Phase 1 When:
- [ ] All Phase 0 exit criteria met
- [ ] No blockers for pattern engine implementation
- [ ] Team confident in architecture decisions
- [ ] Development velocity established
