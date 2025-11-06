# Phase 2: Core Pattern Engine

**Duration:** Weeks 3–4 (Sprints 2)
**Team:** 2 backend engineers + QA
**Capacity:** ~90-100 story points
**Status:** Planned

---

## Phase Overview

Phase 2 focuses on implementing the core pattern compilation logic for geometric shapes. This is the most critical technical component of Knit-Wit, as all downstream features (visualization, export, parsing) depend on accurate, performant pattern generation.

The pattern engine will generate mathematically precise crochet patterns for three foundational shapes:
- **Sphere** (complete rounds, spiral construction)
- **Cylinder** (hemispherical caps + constant-stitch body)
- **Cone/Tapered** (linear taper with even distribution)

All patterns will follow established crochet conventions, ensure proper gauge calculations, and meet strict performance requirements (< 200ms generation time).

### Phase Context

**Preceding Phase:**
- Phase 1 (Weeks 1-2): Architecture & Setup complete, algorithm spike validated, monorepo operational

**Following Phase:**
- Phase 3 (Weeks 5-7): Visualization Foundation begins, requiring working pattern DSL outputs

**Critical Path:**
This phase is on the critical path. Delays will cascade to all subsequent phases, as visualization and export features cannot proceed without working pattern generation.

---

## Goals & Deliverables

### Primary Goals

1. **Sphere Pattern Generation:** Complete implementation of sphere compiler with even increase/decrease distribution
2. **Cylinder Pattern Generation:** Cylinder compiler supporting optional end caps (hemispherical)
3. **Cone/Tapered Generation:** Cone compiler with Bresenham-based linear taper (no stacked deltas)
4. **Comprehensive Testing:** Unit test coverage > 80% for all pattern engine code
5. **Performance Validation:** All shape generation < 200ms on typical inputs

### Key Deliverables

- [ ] `knit_wit_engine/shapes/sphere.py` - Sphere compiler implementation
- [ ] `knit_wit_engine/shapes/cylinder.py` - Cylinder compiler implementation
- [ ] `knit_wit_engine/shapes/cone.py` - Cone/tapered compiler implementation
- [ ] `knit_wit_engine/algorithms/gauge.py` - Gauge conversion utilities
- [ ] `knit_wit_engine/algorithms/distribution.py` - Even distribution algorithm
- [ ] `knit_wit_engine/algorithms/translator.py` - US ↔ UK terminology translator
- [ ] Comprehensive test suite (pytest) with 80%+ coverage
- [ ] Performance benchmarks documentation
- [ ] API integration for pattern generation endpoint

### Success Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Test Coverage | > 80% | pytest-cov |
| Generation Time (10cm sphere) | < 200ms | pytest-benchmark |
| Generation Time (8cm cylinder) | < 150ms | pytest-benchmark |
| Generation Time (12cm cone taper) | < 200ms | pytest-benchmark |
| Equator Stitch Accuracy | ±1 stitch | Unit test assertions |
| Distribution Evenness | Max gap ≤ min gap + 1 | Algorithm validation |

---

## Epic Breakdown

### EPIC A: Pattern Engine (Python)

**Owner:** Backend Lead
**Duration:** Weeks 3–4
**Total Effort:** ~80 story points
**Priority:** P0 (Critical Path)

**Epic Overview:**

Implement the core pattern compilation logic for geometric shapes (sphere, cylinder, cone). This epic encompasses the mathematical algorithms, gauge conversions, stitch distribution logic, and terminology translation needed to produce accurate, human-readable crochet patterns.

**Epic Goals:**
- Sphere, cylinder, and cone patterns generate in < 200ms
- Outputs are mathematically accurate and follow crochet conventions
- Unit tests cover edge cases and performance
- Code is maintainable and well-documented

**Stories:**

| ID | Title | Effort | Priority | Dependencies | Assignee |
|----|-------|--------|----------|--------------|----------|
| A1 | Gauge mapping & yardage estimator | 5 pt | P0 | None | Backend Eng 1 |
| A2 | Sphere compiler (sc, spiral) | 13 pt | P0 | A1, A5 | Backend Lead |
| A3 | Cylinder compiler (with caps) | 10 pt | P0 | A1, A2, A5 | Backend Eng 2 |
| A4 | Cone/tapered compiler (Bresenham) | 13 pt | P0 | A1, A5 | Backend Lead |
| A5 | Even distribution algorithm | 8 pt | P0 | None | Backend Eng 1 |
| A6 | US ↔ UK translator | 3 pt | P1 | None | Backend Eng 2 |
| A7 | Unit tests & benchmarks | 20 pt | P0 | A2, A3, A4 | QA Lead + Backend |

**Total Story Points:** 72 points

**Acceptance Criteria:**

- **AC-G-1:** Generating a 10 cm sphere (14/16 gauge, US sc, spiral) produces expected equator stitch count (±1 stitch)
- **AC-G-2:** Tapered limb 6→2 cm over 8 rounds has monotonic taper with no stacked deltas (verified visually)
- **AC-G-3:** All unit tests pass; coverage > 80%
- **AC-G-4:** Performance < 200ms for typical inputs (10cm sphere, 8cm cylinder, 12cm cone)
- **AC-G-5:** Generated patterns compile to valid PatternDSL structure
- **AC-G-6:** US ↔ UK terminology translation works for all MVP stitches (sc, inc, dec, ch, slst, MR)

### EPIC: Testing & Validation

**Owner:** QA Lead
**Duration:** Weeks 3–4 (parallel to EPIC A)
**Total Effort:** ~26 story points

**Stories:**

| Story ID | Title | Description | Effort | Status |
|----------|-------|-------------|--------|--------|
| TEST-1 | Unit tests: Sphere | pytest tests for sphere.py with multiple gauges/sizes | 8 pt | Backlog |
| TEST-2 | Unit tests: Cylinder | pytest tests for cylinder.py, verify cap dimensions | 6 pt | Backlog |
| TEST-3 | Unit tests: Cone | pytest tests for cone.py, verify linear taper | 6 pt | Backlog |
| TEST-4 | Unit tests: Algorithms | pytest for distribution, translator, gauge functions | 6 pt | Backlog |
| TEST-5 | Performance benchmarks | Benchmark < 200ms target for each shape type | 3 pt | Backlog |

**Total Story Points:** 29 points

---

## Sprint Plan

### Sprint 2: Core Pattern Engine (Weeks 3–4)

**Sprint Goal:** All three shape compilers working; 80%+ test coverage; performance targets met

**Sprint Duration:** 2 weeks (10 working days)

**Team Capacity:**
- Backend Lead: 40 pts
- Backend Engineer 1: 35 pts
- Backend Engineer 2: 35 pts
- QA Lead: 29 pts (parallel testing)
- **Total Capacity:** ~110 pts (includes buffer)

**Planned Stories:**

#### Week 3 (Days 1-5)

**Day 1-2: Foundation & Algorithms**
- [ ] A1: Gauge mapping & yardage (5 pt) - Backend Eng 1
- [ ] A5: Even distribution algorithm (8 pt) - Backend Eng 1
- [ ] A6: US ↔ UK translator (3 pt) - Backend Eng 2

**Day 3-5: Sphere Implementation**
- [ ] A2: Sphere compiler (13 pt) - Backend Lead
- [ ] TEST-1: Unit tests: Sphere (8 pt) - QA Lead (starts Day 4)

**Checkpoint:** Friday Week 3
- Gauge utilities working
- Sphere generation produces valid patterns
- Basic unit tests passing

#### Week 4 (Days 6-10)

**Day 6-8: Cylinder & Cone**
- [ ] A3: Cylinder compiler (10 pt) - Backend Eng 2
- [ ] A4: Cone/tapered compiler (13 pt) - Backend Lead
- [ ] TEST-2: Unit tests: Cylinder (6 pt) - QA Lead (parallel)
- [ ] TEST-3: Unit tests: Cone (6 pt) - QA Lead (parallel)

**Day 9-10: Integration & Performance**
- [ ] TEST-4: Unit tests: Algorithms (6 pt) - QA Lead
- [ ] TEST-5: Performance benchmarks (3 pt) - Backend Eng 1
- [ ] Code review & documentation polish - All

**Checkpoint:** Friday Week 4 (End of Sprint 2)
- All three shapes generating patterns
- Unit tests passing with > 80% coverage
- Performance benchmarks documented and meeting targets

**Sprint Burndown Target:**

| Day | Remaining Points | Notes |
|-----|------------------|-------|
| Day 1 | 75 pts | Foundation stories started |
| Day 3 | 62 pts | Sphere implementation underway |
| Day 5 | 42 pts | Sphere complete, tests passing |
| Day 7 | 23 pts | Cylinder & cone progressing |
| Day 9 | 9 pts | Final tests and benchmarks |
| Day 10 | 0 pts | Sprint complete |

**Daily Standup Focus:**
- Blockers on algorithm implementation
- Test coverage progress
- Performance benchmark results
- Integration points between stories

**Sprint Demo Objectives:**

**What to Demonstrate:**
1. Generate sphere pattern (10cm, 14/16 gauge) via API call
2. Generate cylinder pattern (6cm diameter, 8cm height) with caps
3. Generate cone pattern (6cm → 2cm taper over 8cm)
4. Show unit test report (coverage > 80%)
5. Display performance benchmarks (all < 200ms)
6. Demonstrate US ↔ UK terminology translation

**Demo Script:**
```bash
# 1. Run unit tests
pytest tests/unit/test_sphere.py -v --cov=knit_wit_engine

# 2. Generate sphere via Python
python -c "
from knit_wit_engine.shapes.sphere import SphereCompiler
from knit_wit_engine.models import GenerateRequest, Gauge

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
print(f'Generated {len(dsl.rounds)} rounds')
print(f'Max stitches (equator): {max(r.stitches for r in dsl.rounds)}')
"

# 3. Run performance benchmarks
pytest tests/performance/test_benchmarks.py --benchmark-only

# 4. Show cylinder generation
python demo_cylinder.py

# 5. Show cone generation with visualization of taper
python demo_cone.py
```

**Demo Audience:** Product Owner, Frontend Team, Stakeholders

---

## Technical Implementation

### Architecture Overview

```
knit_wit_engine/
├── shapes/
│   ├── __init__.py
│   ├── base.py              # ShapeCompiler abstract base class
│   ├── sphere.py            # SphereCompiler
│   ├── cylinder.py          # CylinderCompiler
│   └── cone.py              # ConeCompiler
├── algorithms/
│   ├── __init__.py
│   ├── gauge.py             # Gauge conversions, yardage estimation
│   ├── distribution.py      # Even distribution (Bresenham-like)
│   └── translator.py        # US ↔ UK terminology
├── models/
│   ├── __init__.py
│   ├── dsl.py               # PatternDSL, Round, Operation classes
│   └── request.py           # GenerateRequest, Gauge, RenderOptions
└── tests/
    ├── unit/
    │   ├── test_sphere.py
    │   ├── test_cylinder.py
    │   ├── test_cone.py
    │   ├── test_gauge.py
    │   ├── test_distribution.py
    │   └── test_translator.py
    └── performance/
        └── test_benchmarks.py
```

### Data Models

#### PatternDSL Structure

```python
@dataclass
class Operation:
    """Single stitch operation in a round."""
    type: str  # 'sc', 'inc', 'dec', 'ch', 'slst', 'MR'
    count: int = 1
    description: Optional[str] = None

@dataclass
class Round:
    """Single round in a pattern."""
    number: int
    stitches: int  # Final stitch count after this round
    operations: List[Operation]
    notes: Optional[str] = None

@dataclass
class PatternDSL:
    """Complete pattern representation."""
    shape: str  # 'sphere', 'cylinder', 'cone'
    metadata: Dict[str, Any]  # gauge, diameter, etc.
    rounds: List[Round]
    materials: Dict[str, Any]  # yarn weight, hook size, yardage
    instructions: Optional[str] = None
```

#### Example PatternDSL Output (Sphere, 10cm)

```python
PatternDSL(
    shape='sphere',
    metadata={
        'diameter': 10,
        'gauge': {'sts_per_10cm': 14, 'rows_per_10cm': 16},
        'stitch': 'sc',
        'round_mode': 'spiral',
        'terms': 'US'
    },
    rounds=[
        Round(number=1, stitches=6, operations=[
            Operation(type='MR', count=6, description='Magic ring, 6 sc')
        ]),
        Round(number=2, stitches=12, operations=[
            Operation(type='inc', count=6, description='2 sc in each st around (12)')
        ]),
        Round(number=3, stitches=18, operations=[
            Operation(type='sc', count=1),
            Operation(type='inc', count=1),
            Operation(type='repeat', count=6, description='[sc, inc] x6 (18)')
        ]),
        # ... more rounds ...
    ],
    materials={
        'yarn_weight': 'Worsted',
        'hook_size': '4.0mm',
        'yardage_estimate': 45.2  # meters
    }
)
```

### Algorithm Details

#### 1. Sphere Algorithm

**Mathematical Foundation:**

For a sphere with diameter `D` and gauge `G` (stitches/10cm):

1. **Radius:** `r = D / 2`
2. **Equator Stitches:** `S_eq = π × D × (G / 10)`
3. **Total Rounds:** `R_total = 2 × (G_rows / 10) × r`
4. **Increase Phase:** Rounds 1 to R_eq (equator)
5. **Decrease Phase:** Rounds R_eq+1 to R_total (closing)

**Increase Distribution:**

```python
# Start with magic ring (6 sc)
initial_stitches = 6

# Calculate rounds to equator
equator_rounds = round((gauge.rows_per_10cm / 10) * radius)

# Distribute increases evenly
for round_num in range(1, equator_rounds + 1):
    # Target stitch count for this round
    progress = round_num / equator_rounds
    target_stitches = initial_stitches + int((S_eq - initial_stitches) * progress)

    # Increases needed this round
    increases_needed = target_stitches - current_stitches

    # Use even_distribution to space increases
    increase_positions = even_distribution(current_stitches, increases_needed)

    # Build operation list for this round
    operations = build_operations(current_stitches, increase_positions)
```

**Pseudocode:**

```
FUNCTION generate_sphere(diameter, gauge):
    radius = diameter / 2
    S_eq = π × diameter × (gauge.sts_per_10cm / 10)
    R_eq = round(gauge.rows_per_10cm × radius / 10)

    rounds = []
    current_stitches = 6

    # Round 1: Magic ring
    rounds.append(Round(1, 6, [MR(6)]))

    # Increase phase
    FOR r = 2 TO R_eq:
        target = calculate_target_stitches(r, R_eq, 6, S_eq)
        increases = target - current_stitches
        positions = even_distribution(current_stitches, increases)
        ops = build_ops_with_increases(current_stitches, positions)
        rounds.append(Round(r, target, ops))
        current_stitches = target

    # Equator (1-2 steady rounds)
    rounds.append(Round(R_eq + 1, S_eq, [SC(S_eq)]))

    # Decrease phase (mirror of increases)
    FOR r = R_eq + 2 TO R_total:
        # Similar logic, but decreases instead of increases

    RETURN PatternDSL(shape='sphere', rounds=rounds, ...)
```

#### 2. Cylinder Algorithm

**Mathematical Foundation:**

Cylinder = Hemispherical cap + Constant-stitch body + Optional closing cap

1. **Cap Height:** `h_cap = radius / 2` (hemisphere approximation)
2. **Cap Rounds:** `R_cap = round((gauge.rows_per_10cm / 10) × h_cap)`
3. **Body Rounds:** `R_body = round((gauge.rows_per_10cm / 10) × height)`
4. **Circumference Stitches:** `S_circ = π × diameter × (gauge.sts_per_10cm / 10)`

**Implementation Strategy:**

```python
def generate_cylinder(diameter, height, gauge, include_caps=True):
    radius = diameter / 2
    S_circ = round(π * diameter * (gauge.sts_per_10cm / 10))

    rounds = []

    if include_caps:
        # Generate opening cap (same as sphere increase phase to radius/2)
        cap_rounds = generate_hemisphere(radius, gauge, increasing=True)
        rounds.extend(cap_rounds)
    else:
        # Start with chain circle
        rounds.append(Round(1, S_circ, [CH(S_circ), SLST()]))

    # Body rounds (constant stitch count)
    R_body = round((gauge.rows_per_10cm / 10) * height)
    current_round = len(rounds) + 1
    for r in range(R_body):
        rounds.append(Round(current_round + r, S_circ, [SC(S_circ)]))

    if include_caps:
        # Generate closing cap (same as sphere decrease phase)
        closing_rounds = generate_hemisphere(radius, gauge, increasing=False)
        rounds.extend(closing_rounds)

    return PatternDSL(shape='cylinder', rounds=rounds, ...)
```

#### 3. Cone/Tapered Algorithm (Bresenham Distribution)

**Problem:** Taper from diameter D1 to D2 over height H without stacking increases/decreases in same column.

**Bresenham Analogy:**

Bresenham's line algorithm distributes pixels evenly along a line. We adapt this to distribute stitch changes (±1) evenly across rounds.

**Algorithm:**

```python
def generate_cone(diameter_start, diameter_end, height, gauge):
    S_start = round(π * diameter_start * (gauge.sts_per_10cm / 10))
    S_end = round(π * diameter_end * (gauge.sts_per_10cm / 10))
    R_total = round((gauge.rows_per_10cm / 10) * height)

    delta_total = abs(S_start - S_end)  # Total stitch changes needed
    increasing = S_end > S_start

    rounds = []
    current_stitches = S_start
    error = 0  # Bresenham error accumulator

    for r in range(1, R_total + 1):
        # Bresenham decision: should we place a change this round?
        error += delta_total

        if error >= R_total:
            # Place a change
            changes_this_round = error // R_total
            error = error % R_total

            if increasing:
                positions = even_distribution(current_stitches, changes_this_round)
                ops = build_ops_with_increases(current_stitches, positions)
                current_stitches += changes_this_round
            else:
                positions = even_distribution(current_stitches, changes_this_round)
                ops = build_ops_with_decreases(current_stitches, positions)
                current_stitches -= changes_this_round
        else:
            # No changes this round, all sc
            ops = [SC(current_stitches)]

        rounds.append(Round(r, current_stitches, ops))

    return PatternDSL(shape='cone', rounds=rounds, ...)
```

**Example:**

Taper from 36 stitches to 24 stitches over 12 rounds:
- Delta = 12 decreases
- Bresenham places 1 decrease per round, evenly distributed
- Result: monotonic taper, no stacked decreases

#### 4. Even Distribution Algorithm

**Purpose:** Given N stitches and K changes (increases or decreases), return indices where changes should occur.

**Implementation:**

```python
def even_distribution(total_stitches: int, num_changes: int) -> List[int]:
    """
    Return indices (1-indexed) where changes should occur.

    Example:
        even_distribution(36, 6) -> [6, 12, 18, 24, 30, 36]
        (Changes every 6 stitches)
    """
    if num_changes <= 0:
        return []
    if num_changes >= total_stitches:
        # Every stitch is a change
        return list(range(1, total_stitches + 1))

    indices = []
    gap = total_stitches / num_changes

    for i in range(num_changes):
        position = round((i + 1) * gap)
        indices.append(position)

    return indices
```

**Properties:**
- Spacing is as even as possible
- Max gap - min gap ≤ 1 (optimal distribution)
- Works for any N and K where K ≤ N

**Test Cases:**

```python
def test_even_distribution():
    # Perfect division
    assert even_distribution(36, 6) == [6, 12, 18, 24, 30, 36]

    # Imperfect division (12 changes in 36 stitches = every 3)
    result = even_distribution(36, 12)
    assert len(result) == 12
    assert all(result[i+1] - result[i] in [2, 3, 4] for i in range(11))

    # Edge cases
    assert even_distribution(10, 0) == []
    assert even_distribution(10, 1) == [10]
    assert even_distribution(10, 10) == list(range(1, 11))
```

#### 5. Gauge Conversion Utilities

**Gauge Definitions:**

- **Gauge:** Stitches per 10cm × Rows per 10cm
- **Common Gauges:**
  - Baby weight: 24-28 sts / 32-36 rows per 10cm
  - DK weight: 18-22 sts / 24-28 rows per 10cm
  - Worsted: 14-18 sts / 18-22 rows per 10cm
  - Bulky: 10-14 sts / 14-18 rows per 10cm

**Functions:**

```python
def stitches_per_cm(gauge: Gauge) -> float:
    """Return stitches per cm."""
    return gauge.sts_per_10cm / 10.0

def rows_per_cm(gauge: Gauge) -> float:
    """Return rows per cm."""
    return gauge.rows_per_10cm / 10.0

def estimate_yardage(stitch_count: int, yarn_weight: str) -> float:
    """
    Estimate yarn yardage in meters.

    Formula:
        yardage = stitch_count × avg_stitch_length × 1.1 (10% waste)
    """
    # Stitch length lookup (cm per stitch)
    stitch_length_map = {
        'Baby': 0.4,
        'DK': 0.5,
        'Worsted': 0.6,
        'Bulky': 0.8,
    }

    stitch_length_cm = stitch_length_map.get(yarn_weight, 0.6)
    total_length_cm = stitch_count * stitch_length_cm * 1.1  # 10% waste
    return total_length_cm / 100  # Convert to meters
```

#### 6. US ↔ UK Terminology Translator

**Terminology Mapping:**

| US Term | UK Term | MVP Support |
|---------|---------|-------------|
| sc (single crochet) | dc (double crochet) | ✅ Yes |
| hdc (half double crochet) | htr (half treble) | ❌ v1.1 |
| dc (double crochet) | tr (treble) | ❌ v1.1 |
| inc (increase) | inc2 (2 in 1) | ✅ Yes |
| dec (decrease) | dec2 (2 together) | ✅ Yes |
| ch (chain) | ch (chain) | ✅ Yes (same) |
| slst (slip stitch) | ss (slip stitch) | ✅ Yes |
| MR (magic ring) | MR (magic ring) | ✅ Yes (same) |

**Implementation:**

```python
# Translation dictionaries
US_TO_UK = {
    'sc': 'dc',
    'inc': 'inc2',
    'dec': 'dec2',
    'ch': 'ch',
    'slst': 'ss',
    'MR': 'MR',
}

UK_TO_US = {v: k for k, v in US_TO_UK.items()}

def translate_term(term: str, from_lang: str, to_lang: str) -> str:
    """
    Translate a crochet term between US and UK conventions.

    Args:
        term: The term to translate (e.g., 'sc', 'dc')
        from_lang: Source language ('US' or 'UK')
        to_lang: Target language ('US' or 'UK')

    Returns:
        Translated term

    Raises:
        ValueError: If term is unknown or languages invalid
    """
    if from_lang == to_lang:
        return term

    if from_lang == 'US' and to_lang == 'UK':
        if term not in US_TO_UK:
            raise ValueError(f"Unknown US term: {term}")
        return US_TO_UK[term]
    elif from_lang == 'UK' and to_lang == 'US':
        if term not in UK_TO_US:
            raise ValueError(f"Unknown UK term: {term}")
        return UK_TO_US[term]
    else:
        raise ValueError(f"Invalid languages: {from_lang} -> {to_lang}")

def translate_pattern(dsl: PatternDSL, to_lang: str) -> PatternDSL:
    """
    Translate all terms in a PatternDSL to target language.
    """
    from_lang = dsl.metadata.get('terms', 'US')

    if from_lang == to_lang:
        return dsl

    # Create new DSL with translated operations
    translated_rounds = []
    for round in dsl.rounds:
        translated_ops = [
            Operation(
                type=translate_term(op.type, from_lang, to_lang),
                count=op.count,
                description=op.description  # TODO: Translate descriptions
            )
            for op in round.operations
        ]
        translated_rounds.append(Round(
            number=round.number,
            stitches=round.stitches,
            operations=translated_ops,
            notes=round.notes
        ))

    return PatternDSL(
        shape=dsl.shape,
        metadata={**dsl.metadata, 'terms': to_lang},
        rounds=translated_rounds,
        materials=dsl.materials,
        instructions=dsl.instructions
    )
```

### Testing Strategy

#### Unit Testing Approach

**Test Pyramid:**
- 80% unit tests (fast, focused)
- 15% integration tests (API endpoints)
- 5% E2E tests (full pipeline)

**Key Test Categories:**

1. **Algorithm Tests** (test_gauge.py, test_distribution.py, test_translator.py)
   - Test pure functions in isolation
   - Edge cases, boundary conditions
   - Property-based testing (hypothesis) for distribution algorithm

2. **Shape Compiler Tests** (test_sphere.py, test_cylinder.py, test_cone.py)
   - Test pattern generation with known inputs/outputs
   - Verify mathematical accuracy (stitch counts, round counts)
   - Verify distribution properties (no stacking, even spacing)
   - Test multiple gauges and sizes

3. **Performance Tests** (test_benchmarks.py)
   - Benchmark each shape compiler
   - Verify < 200ms target
   - Regression testing (detect performance degradation)

**Example Test: Sphere Accuracy**

```python
def test_sphere_10cm_sc_spiral_gauge_14_16():
    """
    Test sphere generation for standard 10cm diameter.

    Expected:
    - Equator stitches: π × 10 × (14 / 10) ≈ 44 stitches
    - Total rounds: 2 × (16 / 10) × 5 = 16 rounds
    """
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

    # Verify structure
    assert dsl.shape == 'sphere'
    assert len(dsl.rounds) >= 10  # At least 10 rounds

    # Verify equator stitch count
    max_stitches = max(r.stitches for r in dsl.rounds)
    expected_equator = round(π * 10 * (14 / 10))
    assert abs(max_stitches - expected_equator) <= 1  # ±1 stitch tolerance

    # Verify first round (magic ring)
    assert dsl.rounds[0].stitches == 6
    assert any(op.type == 'MR' for op in dsl.rounds[0].operations)

    # Verify monotonic increase phase
    increase_phase = dsl.rounds[:dsl.rounds.index(max(dsl.rounds, key=lambda r: r.stitches))]
    assert all(
        increase_phase[i+1].stitches >= increase_phase[i].stitches
        for i in range(len(increase_phase) - 1)
    ), "Increase phase should be monotonically increasing"

    # Verify even distribution (no obvious columns)
    # This is complex to test programmatically; manual visualization recommended
```

**Example Test: Distribution Algorithm**

```python
@pytest.mark.parametrize("total,changes,expected_spacing", [
    (36, 6, 6),    # Perfect division: every 6th stitch
    (40, 8, 5),    # Perfect division: every 5th stitch
    (37, 6, None), # Imperfect: spacing varies between 6 and 7
])
def test_even_distribution_spacing(total, changes, expected_spacing):
    """Test that distribution is as even as possible."""
    indices = even_distribution(total, changes)

    # Verify count
    assert len(indices) == changes

    # Verify range
    assert all(1 <= idx <= total for idx in indices)

    # Verify spacing
    gaps = [indices[i+1] - indices[i] for i in range(len(indices) - 1)]

    if expected_spacing:
        # Perfect division case
        assert all(gap == expected_spacing for gap in gaps)
    else:
        # Imperfect division: max gap - min gap <= 1
        assert max(gaps) - min(gaps) <= 1
```

**Example Test: Performance Benchmark**

```python
import pytest

def test_sphere_generation_benchmark(benchmark):
    """Benchmark sphere generation time."""
    compiler = SphereCompiler()
    request = GenerateRequest(
        shape='sphere',
        diameter=10,
        gauge=Gauge(sts_per_10cm=14, rows_per_10cm=16),
        stitch='sc',
        round_mode='spiral',
        terms='US'
    )

    # Run benchmark
    result = benchmark(compiler.generate, request)

    # Verify performance target
    assert benchmark.stats.mean < 0.2, f"Generation took {benchmark.stats.mean:.3f}s, target: < 0.2s"

    # Verify result is valid
    assert result.shape == 'sphere'
    assert len(result.rounds) > 0
```

#### Test Coverage Requirements

**Target Coverage: 80%+**

```bash
# Run tests with coverage report
pytest tests/unit/ --cov=knit_wit_engine --cov-report=html --cov-report=term

# Expected output:
# Name                                    Stmts   Miss  Cover
# ---------------------------------------------------------
# knit_wit_engine/shapes/sphere.py          150     20    87%
# knit_wit_engine/shapes/cylinder.py        120     18    85%
# knit_wit_engine/shapes/cone.py            140     22    84%
# knit_wit_engine/algorithms/gauge.py        45      5    89%
# knit_wit_engine/algorithms/distribution.py 35      3    91%
# knit_wit_engine/algorithms/translator.py   25      2    92%
# ---------------------------------------------------------
# TOTAL                                     515     70    86%
```

**Coverage Exemptions:**
- Error handling for impossible cases (covered by integration tests)
- Defensive programming assertions (would require mocking internals)
- Deprecated code paths (clearly marked)

### Performance Optimization

#### Target Metrics

| Shape | Input Size | Target Time | Max Acceptable |
|-------|------------|-------------|----------------|
| Sphere | 10cm diameter | < 150ms | 200ms |
| Cylinder | 6cm × 8cm | < 100ms | 150ms |
| Cone | 12cm taper | < 150ms | 200ms |

#### Optimization Strategies

1. **Algorithmic Efficiency**
   - Use integer arithmetic where possible (avoid float operations)
   - Pre-calculate constants (π, gauge conversions)
   - Avoid redundant calculations in loops

2. **Data Structure Choices**
   - Use lists for sequential access (rounds)
   - Use dicts for lookups (translation tables)
   - Avoid deep copying unless necessary

3. **Caching**
   - Cache gauge calculations per request
   - Memoize distribution patterns for common inputs
   - Consider LRU cache for repeated gauge/size combinations

4. **Profiling**
   - Use `cProfile` to identify hot spots
   - Focus optimization on 80/20 rule (optimize bottlenecks first)
   - Benchmark after each optimization

**Profiling Example:**

```bash
# Profile sphere generation
python -m cProfile -o profile.stats demo_sphere.py

# Analyze with snakeviz
snakeviz profile.stats
```

**Expected Hot Spots:**
- `even_distribution()` - called multiple times per round
- Stitch count calculations - happening in tight loops
- Operation list building - appending to lists

**Optimization Example:**

```python
# Before: Recalculating π in every call
def calculate_circumference(diameter, gauge):
    return 3.14159 * diameter * (gauge.sts_per_10cm / 10)

# After: Use cached constant
from math import pi
def calculate_circumference(diameter, gauge):
    return pi * diameter * (gauge.sts_per_10cm / 10)

# Further optimization: Pre-calculate gauge factor
class SphereCompiler:
    def generate(self, request):
        gauge_factor = request.gauge.sts_per_10cm / 10
        circumference = pi * request.diameter * gauge_factor
        # Use gauge_factor throughout
```

### API Integration

#### Pattern Generation Endpoint

**Endpoint:** `POST /api/v1/patterns/generate`

**Request Schema:**

```json
{
  "shape": "sphere",
  "diameter": 10,
  "height": null,
  "diameter_end": null,
  "gauge": {
    "sts_per_10cm": 14,
    "rows_per_10cm": 16
  },
  "stitch": "sc",
  "round_mode": "spiral",
  "terms": "US",
  "yarn_weight": "Worsted",
  "metadata": {
    "title": "My Sphere",
    "notes": "Optional user notes"
  }
}
```

**Response Schema:**

```json
{
  "pattern_id": "uuid-here",
  "dsl": {
    "shape": "sphere",
    "metadata": { ... },
    "rounds": [
      {
        "number": 1,
        "stitches": 6,
        "operations": [
          {"type": "MR", "count": 6, "description": "Magic ring, 6 sc"}
        ],
        "notes": null
      },
      ...
    ],
    "materials": {
      "yarn_weight": "Worsted",
      "hook_size": "4.0mm",
      "yardage_estimate": 45.2
    },
    "instructions": "Work in continuous spiral. Do not join rounds unless specified."
  },
  "assets": {
    "text": "/api/v1/patterns/uuid-here/text",
    "visualization": "/api/v1/patterns/uuid-here/visualize"
  },
  "performance": {
    "generation_time_ms": 145
  }
}
```

**Error Response:**

```json
{
  "error": {
    "code": "INVALID_GAUGE",
    "message": "Gauge must have positive stitches and rows per 10cm",
    "details": {
      "field": "gauge.sts_per_10cm",
      "value": -5,
      "constraint": "must be > 0"
    }
  },
  "request_id": "req-uuid"
}
```

**FastAPI Implementation:**

```python
# api/routes/patterns.py
from fastapi import APIRouter, HTTPException
from knit_wit_engine.shapes import SphereCompiler, CylinderCompiler, ConeCompiler
from knit_wit_engine.models import GenerateRequest, PatternDSL
from api.models import GenerateRequestAPI, GenerateResponseAPI
import time

router = APIRouter(prefix="/api/v1/patterns")

@router.post("/generate", response_model=GenerateResponseAPI)
async def generate_pattern(request: GenerateRequestAPI):
    """
    Generate a crochet pattern for a geometric shape.
    """
    start_time = time.time()

    try:
        # Select compiler based on shape
        if request.shape == 'sphere':
            compiler = SphereCompiler()
        elif request.shape == 'cylinder':
            compiler = CylinderCompiler()
        elif request.shape == 'cone':
            compiler = ConeCompiler()
        else:
            raise HTTPException(status_code=400, detail=f"Unknown shape: {request.shape}")

        # Generate pattern
        dsl = compiler.generate(request.to_engine_request())

        # Calculate generation time
        generation_time_ms = (time.time() - start_time) * 1000

        # Build response
        pattern_id = str(uuid.uuid4())
        return GenerateResponseAPI(
            pattern_id=pattern_id,
            dsl=dsl,
            assets={
                'text': f'/api/v1/patterns/{pattern_id}/text',
                'visualization': f'/api/v1/patterns/{pattern_id}/visualize'
            },
            performance={
                'generation_time_ms': round(generation_time_ms, 2)
            }
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Log error for debugging
        logger.exception(f"Pattern generation failed: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

---

## Success Criteria

### Phase Exit Criteria

All criteria must be met before proceeding to Phase 3:

- [ ] **Sphere compiler complete:** Generates valid patterns for diameters 5-30cm, gauges 10-28 sts/10cm
- [ ] **Cylinder compiler complete:** Generates valid patterns with/without caps, heights 5-50cm
- [ ] **Cone compiler complete:** Generates smooth tapers with no stacked deltas (visual verification)
- [ ] **Unit test coverage:** > 80% line coverage for `knit_wit_engine/` package
- [ ] **Performance benchmarks:** All shapes < 200ms on standard hardware (MacBook Pro M1 equivalent)
- [ ] **API integration:** POST `/api/v1/patterns/generate` endpoint functional, returns valid PatternDSL
- [ ] **Code review:** All code reviewed and approved by backend lead
- [ ] **Documentation:** All functions have docstrings; architecture documented

### Acceptance Testing

**Manual Acceptance Tests:**

| Test ID | Test Case | Expected Result | Status |
|---------|-----------|----------------|--------|
| AC-G-1 | Generate 10cm sphere, 14/16 gauge, US sc | Equator: 44±1 stitches | ⬜ |
| AC-G-2 | Generate cone 6cm→2cm over 8cm | Monotonic taper, no stacked deltas | ⬜ |
| AC-G-3 | Generate cylinder 6cm diameter × 8cm height with caps | Caps are hemispherical, body constant | ⬜ |
| AC-G-4 | Translate sphere pattern US → UK | All terms translated correctly | ⬜ |
| AC-G-5 | Run full test suite | All tests pass, coverage > 80% | ⬜ |
| AC-G-6 | Run performance benchmarks | Sphere, cylinder, cone all < 200ms | ⬜ |

**Automated Acceptance Tests:**

```bash
# Run full acceptance test suite
pytest tests/acceptance/ -v

# Expected tests:
# ✓ test_generate_sphere_10cm_standard_gauge
# ✓ test_generate_cylinder_with_caps
# ✓ test_generate_cone_smooth_taper
# ✓ test_translate_us_to_uk
# ✓ test_performance_benchmarks_pass
```

### Definition of Done

**Story-Level DoD:**

- [ ] Code written and follows style guide (PEP 8 for Python)
- [ ] Unit tests written and passing (coverage > 80% for story)
- [ ] Code reviewed and approved by at least one other developer
- [ ] Docstrings present for all public functions/classes
- [ ] No high-priority linter warnings (Pylint, Flake8)
- [ ] Performance benchmarks pass (if applicable)
- [ ] Story demo-able in isolation

**Sprint-Level DoD:**

- [ ] All story-level DoD criteria met for all stories
- [ ] Integration tests pass
- [ ] No critical or high-priority bugs remaining
- [ ] Sprint demo completed and approved by Product Owner
- [ ] Documentation updated (README, architecture docs)
- [ ] Code merged to `main` branch
- [ ] CI/CD pipeline green

**Phase-Level DoD:**

- [ ] All sprint-level DoD criteria met
- [ ] Phase exit criteria met (see above)
- [ ] Acceptance tests pass
- [ ] Performance targets met
- [ ] Stakeholder sign-off obtained
- [ ] Retrospective completed, action items documented
- [ ] Handoff to next phase (Phase 3) complete

---

## Dependencies & Blockers

### Dependencies

#### Upstream Dependencies (Must Complete Before Phase 2 Starts)

1. **Phase 1: Architecture & Setup (Complete)**
   - Monorepo structure finalized
   - Python package structure (`knit_wit_engine/`) in place
   - FastAPI backend scaffolded
   - CI/CD pipeline operational (pytest, coverage, linting)
   - Algorithm spike completed and validated

2. **Algorithm Validation (Complete)**
   - Sphere math verified with hand-calculated examples
   - Bresenham distribution algorithm validated
   - Gauge conversion formulas confirmed

3. **Data Models Defined (Complete)**
   - `PatternDSL` data structure finalized
   - `GenerateRequest` schema defined
   - `Operation`, `Round` models agreed upon

#### Downstream Dependencies (What Depends on Phase 2)

1. **Phase 3: Visualization Foundation**
   - Requires working `PatternDSL` outputs from Phase 2
   - Requires `Visualizer.dsl_to_frames()` backend support (EPIC B)
   - Requires functional pattern generation API

2. **Phase 4: Export & Parsing**
   - Requires stable PatternDSL format
   - Requires pattern generation working for all shapes

3. **All Subsequent Phases**
   - Pattern engine is foundational for entire MVP

### Potential Blockers

| Blocker | Probability | Impact | Mitigation | Owner |
|---------|-------------|--------|-----------|-------|
| Algorithm bugs causing invalid patterns | High | Critical | Pair program on complex sections; extensive unit tests; daily code review | Backend Lead |
| Performance regression (> 200ms) | Medium | High | Profile early and often; optimize hot paths; use cProfile | Backend Eng 1 |
| Gauge assumptions prove incorrect | Medium | Medium | Validate with knitting community; allow param tweaking; build feedback loop | Product Owner |
| Test coverage difficult to achieve | Medium | Medium | Write tests alongside code (TDD); use pytest-cov; set coverage as CI gate | QA Lead |
| Team member unavailability | Low | High | Cross-train team; document design decisions; use pairing for critical code | Scrum Master |
| Integration issues with FastAPI | Low | Medium | Test API integration early (Day 6); use TestClient for integration tests | Backend Eng 2 |

### External Dependencies

1. **Python Libraries:**
   - `numpy` (mathematical operations) - Version: 1.24+
   - `pydantic` (data validation) - Version: 2.0+
   - `pytest` (testing) - Version: 7.4+
   - `pytest-cov` (coverage) - Version: 4.1+
   - `pytest-benchmark` (performance testing) - Version: 4.0+

2. **Infrastructure:**
   - GitHub Actions runners (CI/CD)
   - Python 3.11+ runtime
   - Development environments set up

3. **Stakeholder Input:**
   - Feedback on generated patterns (from Product Owner / domain expert)
   - Confirmation of gauge calculations accuracy

---

## Risks & Mitigation

### Technical Risks

| Risk | Description | Probability | Impact | Mitigation Strategy | Contingency Plan |
|------|-------------|-------------|--------|---------------------|------------------|
| **Algorithm Complexity** | Sphere/cone algorithms prove more complex than estimated | High | Critical | - Pair programming on critical sections<br>- Daily code reviews<br>- Spike results documented<br>- Break into smaller sub-tasks | - Simplify algorithms for MVP (e.g., fewer steady rounds)<br>- Extend sprint by 2-3 days<br>- Escalate to architect for design review |
| **Performance Issues** | Generation time exceeds 200ms target | Medium | High | - Profile early (Day 3)<br>- Optimize hot paths proactively<br>- Use pytest-benchmark in CI<br>- Test on target hardware | - Accept 250ms as acceptable for MVP<br>- Optimize in Phase 5 (polish)<br>- Use caching for common patterns |
| **Test Coverage Gap** | Difficult to achieve 80% coverage | Medium | Medium | - TDD approach (write tests first)<br>- Coverage reports in CI<br>- Block PRs if coverage drops | - Accept 75% coverage with justification<br>- Focus on critical paths (compilers, distribution)<br>- Manual testing for edge cases |
| **Edge Cases** | Unusual gauge/size combinations break algorithms | Medium | Medium | - Extensive parameterized testing<br>- Test with extreme values (tiny/huge gauges)<br>- Community feedback loop | - Validate inputs and reject extreme cases<br>- Display warnings for unusual inputs<br>- Document known limitations |
| **Integration Issues** | FastAPI integration more complex than expected | Low | Medium | - Test API early (Day 6)<br>- Use TestClient for integration tests<br>- Mock pattern engine in API tests | - Defer API integration to Phase 3<br>- Focus on pure Python implementation first |

### Process Risks

| Risk | Description | Probability | Impact | Mitigation Strategy | Contingency Plan |
|------|-------------|-------------|--------|---------------------|------------------|
| **Scope Creep** | Adding features not in sprint plan | Medium | High | - Strict adherence to sprint backlog<br>- Product Owner approval required for changes<br>- Track "nice-to-have" in separate backlog | - Defer new features to Phase 4 or v1.1<br>- Time-box explorations to 1 hour |
| **Team Availability** | Backend engineer unavailable mid-sprint | Low | High | - Cross-train team members<br>- Pair programming for knowledge sharing<br>- Document design decisions | - Reassign stories to other team members<br>- Reduce sprint scope<br>- Extend sprint by 1-2 days |
| **Blocked on Reviews** | Code reviews delay merges | Medium | Medium | - Daily code review sessions<br>- Max 24-hour review turnaround<br>- Use draft PRs for early feedback | - Relax review requirements for minor changes<br>- Async reviews via comments<br>- Pair review sessions |
| **Unclear Requirements** | Ambiguity in pattern conventions | Low | Medium | - Clarify with Product Owner immediately<br>- Document assumptions<br>- Validate with knitting community | - Make reasonable assumptions and document<br>- Build flexibility into design<br>- Iterate based on feedback |

### Quality Risks

| Risk | Description | Probability | Impact | Mitigation Strategy | Contingency Plan |
|------|-------------|-------------|--------|---------------------|------------------|
| **Generated Patterns Invalid** | Patterns don't follow crochet conventions | Medium | Critical | - Validate outputs with domain expert<br>- Manual inspection of generated patterns<br>- Compare to known good patterns | - Fix in Phase 5 (QA)<br>- Add validation layer<br>- Provide pattern preview before export |
| **Regression Bugs** | Changes break existing functionality | Medium | High | - Comprehensive unit tests<br>- CI runs full test suite on every PR<br>- Manual regression testing checklist | - Hotfix critical regressions immediately<br>- Add regression test for bug<br>- More aggressive code freeze |
| **Performance Regression** | Optimizations introduce bugs | Low | Medium | - Benchmark before/after optimizations<br>- Code review for performance changes<br>- Profile guided optimization | - Revert optimization if bugs introduced<br>- Accept slower performance for MVP |

### Risk Response Plan

**High-Priority Risks (Algorithm Complexity, Performance Issues):**

1. **Daily Risk Check:** Standup includes "Are we on track for performance targets?"
2. **Early Warning Triggers:**
   - Benchmark fails in CI → Immediate investigation
   - Unit test failure → Block merges until resolved
   - Complexity estimate > 2x actual time → Escalate to Scrum Master
3. **Escalation Path:**
   - Day 1-3: Team resolves internally
   - Day 4-5: Scrum Master intervention (reprioritize, reduce scope)
   - Day 6+: Stakeholder decision (extend sprint, reduce scope, accept technical debt)

**Medium-Priority Risks (Test Coverage, Edge Cases):**

1. **Weekly Risk Review:** Friday retrospective includes risk assessment
2. **Monitoring:** Coverage reports, edge case test results
3. **Response:** Adjust testing strategy, add parameterized tests

**Low-Priority Risks (Integration Issues, Unclear Requirements):**

1. **As-Needed Response:** Address when encountered
2. **No Proactive Mitigation:** Focus energy on high-priority risks

---

## Phase Exit Criteria

Before proceeding to **Phase 3: Visualization Foundation**, all of the following must be satisfied:

### Functional Criteria

- [ ] **Sphere Compiler Operational**
  - Generates patterns for diameters 5-30cm
  - Supports gauges 10-28 sts/10cm, 12-36 rows/10cm
  - Equator stitch count accurate (±1 stitch)
  - Increases evenly distributed (no visible columns)

- [ ] **Cylinder Compiler Operational**
  - Generates patterns with and without caps
  - Heights 5-50cm supported
  - Caps are hemispherical (follow sphere logic)
  - Body maintains constant stitch count

- [ ] **Cone Compiler Operational**
  - Generates smooth tapers (diameter_start ≠ diameter_end)
  - No stacked deltas (verified visually or programmatically)
  - Monotonic taper (stitch count changes consistently)

- [ ] **US ↔ UK Translation Working**
  - Translates all MVP terms (sc, inc, dec, ch, slst, MR)
  - Round-trip translation preserves meaning

### Quality Criteria

- [ ] **Test Coverage > 80%**
  - Unit tests for all shape compilers
  - Unit tests for all algorithm utilities
  - Integration tests for API endpoint
  - Performance benchmarks documented

- [ ] **All Tests Passing**
  - `pytest tests/` exits with 0 failures
  - CI pipeline green
  - No flaky tests (all tests deterministic)

- [ ] **Performance Targets Met**
  - Sphere generation < 200ms (average over 10 runs)
  - Cylinder generation < 150ms
  - Cone generation < 200ms
  - Benchmarks documented and tracked

### Documentation Criteria

- [ ] **Code Documentation Complete**
  - All public functions have docstrings (PEP 257)
  - Complex algorithms explained with comments
  - README updated with usage examples

- [ ] **Architecture Documentation Updated**
  - Pattern engine design documented
  - Algorithm explanations included
  - Data models documented (PatternDSL, etc.)

- [ ] **API Documentation Updated**
  - OpenAPI schema generated
  - Example requests/responses provided
  - Error codes documented

### Process Criteria

- [ ] **Sprint Demo Completed**
  - Demo to Product Owner successful
  - Stakeholder feedback collected
  - Action items documented

- [ ] **Code Review Approved**
  - All PRs reviewed by at least one other developer
  - No unresolved review comments
  - Code follows style guide (PEP 8)

- [ ] **Retrospective Completed**
  - Team retrospective held
  - Learnings documented
  - Action items assigned

- [ ] **Handoff to Phase 3**
  - Frontend team briefed on PatternDSL structure
  - Example DSL outputs provided for testing
  - API endpoint available on dev environment

### Sign-Off

**Required Approvals:**

- [ ] **Backend Lead:** Code quality, architecture, performance
- [ ] **QA Lead:** Test coverage, quality assurance
- [ ] **Product Owner:** Functional requirements met
- [ ] **Scrum Master:** Process followed, risks addressed

**Sign-Off Date:** __________ (End of Week 4)

---

## Next Phase Preview

### Phase 3: Visualization Foundation (Weeks 5-7, Sprints 3-4)

**Objective:** Build the visualization layer that renders PatternDSL outputs as interactive, step-by-step visual guides.

**Key Features:**
- RN/Expo app shell with navigation
- DSL → render primitives conversion (backend support)
- SVG renderer displaying rounds as circular diagrams
- Interactive scrubber + step controls (Next/Previous buttons, slider)
- Stitch highlighting (color-code inc/dec)
- Basic tooltips on stitch tap
- Accessibility labels and WCAG AA color contrast

**Dependencies on Phase 2:**
- Requires working PatternDSL outputs
- Requires pattern generation API (`POST /api/v1/patterns/generate`)
- Requires stable data models

**Key Epic: EPIC B - Visualization**

**Stories Preview:**

| ID | Title | Effort | Description |
|----|-------|--------|-------------|
| B1 | Visualizer.dsl_to_frames() (backend) | 13 pt | Convert PatternDSL to render primitives (nodes, edges, highlights) |
| B2 | SVG renderer component (frontend) | 13 pt | React Native SVG rendering of frames |
| B3 | Round scrubber + step controls | 8 pt | Slider, Next/Back buttons, jump-to-round |
| B4 | Stitch highlighting (inc/dec) | 8 pt | Color-code increases (green), decreases (red) |
| B5 | Legend overlay | 5 pt | Display stitch type colors and meanings |
| B6 | Basic tooltips | 5 pt | On-tap stitch info: "inc = 2 sc in same st" |
| B7 | VisualizationScreen integration | 8 pt | Main screen layout, frame display, controls |
| B8 | Accessibility: labels & contrast | 13 pt | WCAG AA compliance, screen reader support |

**Handoff Items from Phase 2 to Phase 3:**

1. **Example PatternDSL Outputs**
   - Provide 3-5 example DSL files (sphere, cylinder, cone)
   - Include JSON serialization for frontend consumption
   - Document DSL schema and structure

2. **API Endpoint Documentation**
   - OpenAPI spec for `/api/v1/patterns/generate`
   - Example curl commands
   - Postman collection

3. **Algorithm Insights**
   - Visualization requirements (node placement, edge connections)
   - Stitch type information (which operations are inc/dec)
   - Round-to-round dependencies

4. **Performance Baseline**
   - Pattern generation performance benchmarks
   - Expected DSL sizes (number of rounds, stitches per round)
   - Performance considerations for frontend rendering

**Risks Carried Forward:**

- **Pattern Accuracy:** Any bugs in Phase 2 compilers will surface in visualization; plan for quick hotfixes
- **Performance:** Large patterns (100+ rounds) may challenge frontend rendering; monitor performance in Phase 3
- **Data Model Stability:** Avoid breaking changes to PatternDSL in Phase 3; use versioning if needed

**Preparation for Phase 3:**

- [ ] Backend team provides DSL examples and API documentation
- [ ] Frontend team reviews PatternDSL structure
- [ ] Design mockups finalized for visualization screens
- [ ] React Native SVG library tested and confirmed working

---

## Appendix

### A. Story Details (Full Specifications)

See **Epic Breakdown** section above for detailed story specifications.

### B. Algorithm Pseudocode

See **Technical Implementation > Algorithm Details** section above for comprehensive algorithm pseudocode.

### C. Data Model Schemas

See **Technical Implementation > Data Models** section above for PatternDSL, Round, Operation schemas.

### D. Test Examples

See **Technical Implementation > Testing Strategy** section above for comprehensive test examples.

### E. Performance Benchmarking Guide

**Running Benchmarks:**

```bash
# Run all performance benchmarks
pytest tests/performance/ --benchmark-only

# Run with detailed stats
pytest tests/performance/ --benchmark-only --benchmark-verbose

# Save benchmark results for comparison
pytest tests/performance/ --benchmark-only --benchmark-save=phase2

# Compare against previous benchmark
pytest tests/performance/ --benchmark-only --benchmark-compare=phase2
```

**Analyzing Results:**

```bash
# View benchmark report
cat .benchmarks/Darwin-CPython-3.11-64bit/0001_phase2.json

# Visualize with pytest-benchmark's histogram
pytest-benchmark compare --histogram
```

### F. Code Review Checklist

**Reviewer Checklist:**

- [ ] Code follows PEP 8 style guide
- [ ] All functions have docstrings
- [ ] Complex logic is commented
- [ ] Unit tests cover new code (> 80% coverage)
- [ ] Performance benchmarks pass (if applicable)
- [ ] No hardcoded values (use constants or config)
- [ ] Error handling is appropriate
- [ ] Naming is clear and consistent
- [ ] No obvious bugs or logic errors
- [ ] Code is DRY (Don't Repeat Yourself)
- [ ] Changes are scoped to the story (no scope creep)

**Approval Criteria:**

- At least one approval from another backend developer
- All CI checks pass (tests, linting, coverage)
- No unresolved comments
- Code merged via squash or rebase (no merge commits)

### G. Sprint Retrospective Template

**What Went Well:**
- [Team fills in during retrospective]

**What Didn't Go Well:**
- [Team fills in during retrospective]

**Action Items:**
- [Action item 1] - Owner: [Name] - Due: [Date]
- [Action item 2] - Owner: [Name] - Due: [Date]

**Metrics:**
- Velocity: [Story points completed] / [Story points planned]
- Test Coverage: [Actual %]
- Performance: [Actual times vs targets]
- Bugs Found: [Count]

### H. Useful Commands

```bash
# Setup development environment
cd packages/knit-wit-engine
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

# Run tests
pytest tests/unit/ -v
pytest tests/unit/ --cov=knit_wit_engine --cov-report=html

# Run linters
flake8 knit_wit_engine/
pylint knit_wit_engine/
black knit_wit_engine/ --check
mypy knit_wit_engine/

# Format code
black knit_wit_engine/
isort knit_wit_engine/

# Run benchmarks
pytest tests/performance/ --benchmark-only

# Start backend API (for integration testing)
cd apps/backend
uvicorn main:app --reload

# Generate OpenAPI docs
cd apps/backend
python -c "from main import app; import json; print(json.dumps(app.openapi(), indent=2))" > openapi.json
```

### I. Resources & References

**Documentation:**
- [Crochet Gauge Guide](https://www.craftyarncouncil.com/standards/crochet-gauge)
- [Bresenham's Line Algorithm](https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

**Internal Documents:**
- PRD: `knit-wit/project_plans/mvp/prd.md`
- Architecture Decision Records: `knit-wit/project_plans/mvp/adrs/`
- Implementation Plan: `knit-wit/project_plans/mvp/implementation-plan.md`

**Team Contacts:**
- Backend Lead: [Name] - [Email]
- Backend Engineer 1: [Name] - [Email]
- Backend Engineer 2: [Name] - [Email]
- QA Lead: [Name] - [Email]
- Product Owner: [Name] - [Email]

---

**Document Version:** 1.0
**Last Updated:** 2025-11-05
**Owner:** Backend Lead
**Status:** Planned

**Change Log:**

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-05 | 1.0 | Initial Phase 2 plan created | Documentation Writer |

---

*End of Phase 2 Plan*
