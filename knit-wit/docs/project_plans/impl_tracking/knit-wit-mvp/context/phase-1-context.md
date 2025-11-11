# Phase 1 Context: Core Pattern Engine

**Last Updated:** 2025-11-11
**Phase Status:** In Progress (0% complete, 0/81 pts)
**Current Branch:** TBD (create feature branch)
**Active Stories:** None (initialization complete)

---

## Current State

### What's Happening Now
- **Phase:** Phase 1 (Core Pattern Engine) - Weeks 3-4
- **Goal:** Implement sphere, cylinder, and cone pattern compilers with 80%+ test coverage
- **Blocker:** None (ready to start)

### What Exists (from Phase 0)
- Monorepo structure with pnpm workspaces
- Pattern engine package initialized: `packages/pattern-engine/`
- CI/CD pipeline (GitHub Actions)
- DSL v0.1 schema (Pydantic models)
- Algorithm spike validated (gauge, distribution math)

### What Doesn't Exist Yet
- Shape compilers (sphere, cylinder, cone)
- Algorithm implementations (gauge, distribution, translator)
- Comprehensive test suite (unit, performance)
- Pattern generation working end-to-end

---

## Phase Scope Summary

### Primary Deliverables
1. **Three Shape Compilers:** Sphere, Cylinder, Cone (all with spiral sc)
2. **Core Algorithms:** Gauge mapping, yardage estimation, even distribution, US/UK translator
3. **Test Suite:** 80%+ coverage, performance benchmarks < 200ms
4. **Acceptance Validation:** AC-G-1 (sphere equator), AC-G-2 (cone taper)

### Non-Goals (Deferred)
- Visualization rendering (Phase 2)
- API endpoints (Phase 2)
- HDC/DC stitches (v1.1)
- Joined rounds (v1.1)

---

## Key Architectural Decisions

### Pattern Engine Architecture
```
knit_wit_engine/
├── algorithms/           # Pure Python utility functions
│   ├── gauge.py         # Gauge conversion, yardage estimation
│   ├── distribution.py  # Bresenham-like even distribution
│   └── translator.py    # US ↔ UK term translation
├── shapes/              # Shape-specific compilers
│   ├── base.py         # ShapeCompiler abstract base class
│   ├── sphere.py       # SphereCompiler
│   ├── cylinder.py     # CylinderCompiler
│   └── cone.py         # ConeCompiler
├── models/              # Pydantic data models
│   ├── dsl.py          # PatternDSL, Round, Operation
│   └── requests.py     # GenerateRequest, Gauge
└── tests/
    ├── unit/           # 80%+ coverage target
    └── performance/    # < 200ms benchmarks
```

### Critical Design Patterns
- **Separation of Concerns:** Algorithms (pure functions) → Compilers (shape logic) → Models (data)
- **Pydantic Validation:** All inputs validated via Pydantic v2 models
- **Zero Framework Deps:** Pattern engine is pure Python (no FastAPI)
- **Performance First:** All operations < 200ms; algorithms < 1ms

### Core Algorithms

**Gauge Mapping:**
```python
# Convert gauge to stitch length
stitch_length = yarn_weight_factor × (10 / gauge.sts_per_10cm)

# Estimate yardage with 10% waste
yardage = (total_stitches × stitch_length / 100) × 1.1
```

**Even Distribution (Bresenham):**
```python
# Distribute N changes across M stitches evenly
gap = total_stitches / num_changes
positions = [int(round(i * gap)) for i in range(num_changes)]
```

**Sphere Compilation:**
1. Calculate radius from diameter and gauge
2. Determine equator stitch count: `S_eq = circumference × (sts_per_10cm / 10)`
3. Calculate rounds: `r_inc = radius × (rows_per_10cm / 10)`
4. Distribute increases evenly (Bresenham)
5. Mirror for decrease phase

**Cone Compilation:**
1. Calculate stitch counts at start and end
2. Determine total rounds from height
3. Calculate stitch delta per round
4. Use Bresenham to distribute changes without stacking

---

## Development Commands

### Pattern Engine Development
```bash
# Install in development mode
pip install -e packages/pattern-engine/

# Run unit tests
pytest packages/pattern-engine/tests/unit/ -v

# Run with coverage
pytest packages/pattern-engine/tests/ --cov=knit_wit_engine --cov-report=html

# Run performance benchmarks
pytest packages/pattern-engine/tests/performance/ -v

# Lint and format
black packages/pattern-engine/
isort packages/pattern-engine/
ruff check packages/pattern-engine/
```

### Monorepo Commands
```bash
# Run all pattern-engine tests
pnpm --filter pattern-engine test

# Run all linting
pnpm --filter pattern-engine lint

# Full CI check (runs in GitHub Actions)
pnpm test  # All workspaces
```

---

## Key Files Reference

### To Create (Phase 1)
```
packages/pattern-engine/knit_wit_engine/
├── algorithms/
│   ├── gauge.py              # A1: Gauge mapping & yardage
│   ├── distribution.py       # A5: Even distribution algorithm
│   └── translator.py         # A6: US/UK translator
├── shapes/
│   ├── sphere.py            # A2: Sphere compiler
│   ├── cylinder.py          # A3: Cylinder compiler
│   └── cone.py              # A4: Cone/tapered compiler
└── tests/
    ├── unit/
    │   ├── test_sphere.py   # TEST-1
    │   ├── test_cylinder.py # TEST-2
    │   ├── test_cone.py     # TEST-3
    │   └── test_algorithms.py # TEST-4
    └── performance/
        └── test_benchmarks.py # TEST-5
```

### Existing (from Phase 0)
```
packages/pattern-engine/knit_wit_engine/
├── __init__.py
├── models/
│   ├── dsl.py              # PatternDSL, Round, Operation
│   └── requests.py         # GenerateRequest, Gauge
└── shapes/
    └── base.py             # ShapeCompiler abstract base class
```

---

## Story Dependencies

### Immediate Start (No Dependencies)
- **A1:** Gauge mapping & yardage estimator
- **A5:** Even distribution algorithm
- **A6:** US ↔ UK translator

### Sprint 2 (Week 3)
- **A2:** Sphere compiler (depends on A1, A5)
- **TEST-1:** Sphere unit tests (depends on A2)

### Sprint 3 (Week 4)
- **A3:** Cylinder compiler (depends on A1, A2, A5)
- **A4:** Cone compiler (depends on A1, A5)
- **TEST-2:** Cylinder tests (depends on A3)
- **TEST-3:** Cone tests (depends on A4)
- **TEST-4:** Algorithm tests (depends on A1, A5, A6)
- **TEST-5:** Performance benchmarks (depends on A2, A3, A4)

---

## Acceptance Criteria Reference

### AC-G-1: Sphere Equator Validation
**Test:** 10 cm diameter sphere with 14 sts/10cm, 16 rows/10cm gauge
**Expected:** Equator round has 44 stitches (±1)
**Calculation:** `circumference = π × 10 cm = 31.4 cm`, `stitches = 31.4 × 1.4 = 43.96 ≈ 44`

### AC-G-2: Cone Taper Validation
**Test:** Tapered limb 6 cm → 2 cm diameter over 8 cm height
**Expected:** Monotonic decrease, no stacked deltas in same column
**Verification:** Visual inspection of generated pattern (no consecutive decreases at same position)

---

## Integration Points

### Phase 0 Dependencies (Complete)
- ✅ Monorepo initialized (SETUP-1)
- ✅ Pattern engine package scaffold (SETUP-4)
- ✅ DSL v0.1 schema finalized (ARCH-2)
- ✅ Algorithm spike validated (ARCH-1)
- ✅ CI/CD pipeline operational (SETUP-2)

### Phase 2 Handoff (Future)
- Pattern engine library complete → Backend API routes can call compilers
- DSL output validated → Visualization can render patterns
- Performance benchmarks met → Mobile app can generate patterns client-side

---

## Common Patterns

### Pydantic Model Usage
```python
from knit_wit_engine.models.requests import GenerateRequest
from knit_wit_engine.models.dsl import PatternDSL

def generate(request: GenerateRequest) -> PatternDSL:
    # Pydantic validates inputs automatically
    # Return type is also validated
    pass
```

### Compiler Pattern
```python
from knit_wit_engine.shapes.base import ShapeCompiler

class SphereCompiler(ShapeCompiler):
    def generate(self, request: GenerateRequest) -> PatternDSL:
        # 1. Extract parameters
        # 2. Calculate geometry
        # 3. Generate rounds
        # 4. Return PatternDSL
        pass
```

### Test Structure
```python
import pytest
from knit_wit_engine.shapes.sphere import SphereCompiler

def test_sphere_10cm_standard_gauge():
    """AC-G-1: 10cm sphere with 14/16 gauge has 44 stitches at equator"""
    compiler = SphereCompiler()
    request = GenerateRequest(
        shape="sphere",
        diameter=10,
        gauge=Gauge(sts_per_10cm=14, rows_per_10cm=16)
    )
    pattern = compiler.generate(request)

    # Find equator round (max stitch count)
    max_stitches = max(r.stitches for r in pattern.rounds)
    assert 43 <= max_stitches <= 45  # ±1 tolerance
```

---

## Risk Mitigation

### Performance Risk
**Risk:** Pattern generation exceeds 200ms target
**Mitigation:** Profile early (pytest-benchmark), optimize hot paths, consider caching

### Algorithm Risk
**Risk:** Bresenham distribution creates visible stacking
**Mitigation:** Visual inspection in tests, hand-calculate small examples, iterate on offset strategy

### Test Coverage Risk
**Risk:** Coverage falls below 80% threshold
**Mitigation:** TDD approach, write tests alongside implementation, use coverage tool in CI/CD

---

## Next Actions

1. Create feature branch: `feature/phase-1-pattern-engine`
2. Start foundation stories: A1 (Gauge), A5 (Distribution), A6 (Translator)
3. Implement A2 (Sphere) once A1 and A5 complete
4. Follow dependency graph for remaining stories
5. Continuous testing: run pytest after each function implementation
6. Code review at 50% completion (end of Sprint 2)
