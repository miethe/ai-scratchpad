# Phase 1: Core Pattern Engine

**Knit-Wit MVP Implementation Plan**

---

## Phase Overview

**Phase Number:** 1
**Phase Name:** Core Pattern Engine
**Duration:** 2 weeks (Weeks 3-4 of project timeline)
**Sprints:** Sprint 2, partial Sprint 3
**Target Dates:** Week 3 (Start) → End of Week 4
**Capacity:** ~90-100 story points
**Team:** 2 backend engineers + QA engineer

### Phase Purpose

This is the most critical phase of the Knit-Wit MVP development. Phase 1 implements the core pattern compilation logic for geometric shapes (sphere, cylinder, cone). All downstream features—visualization, export, and user interface—depend on the successful completion of this phase.

The pattern engine must generate mathematically accurate patterns that follow crochet conventions, complete with even distribution of increases/decreases to avoid visible columns or stacking. Performance is critical: patterns must compile in under 200ms.

### Phase Context

- **Previous Phase:** Phase 0 (Project Setup & Architecture, Weeks 1-2) established the monorepo, CI/CD pipeline, development environments, and architectural foundations. The algorithm spike completed in Phase 0 validated the mathematical approaches for gauge mapping and round distribution.
- **Next Phase:** Phase 2 (Visualization Foundation, Weeks 5-7) will build the rendering engine and mobile UI to display generated patterns interactively.

---

## Goals & Deliverables

### Primary Goals

1. **Sphere Pattern Generation:** Fully functional sphere compiler generating spiral single crochet (sc) patterns with even increase/decrease distribution
2. **Cylinder Pattern Generation:** Cylinder compiler with optional hemisphere caps working for various heights and diameters
3. **Cone/Tapered Pattern Generation:** Cone compiler using Bresenham distribution for smooth linear tapers without stacking deltas
4. **High Test Coverage:** Unit tests covering all shapes with 80%+ code coverage
5. **Performance Targets Met:** Pattern generation completes in < 200ms for typical inputs

### Key Deliverables

| Deliverable | Description | Success Metric |
|------------|-------------|----------------|
| **Pattern Engine Library** | Python package with all three shape compilers | All compilers pass acceptance tests |
| **Gauge Utilities** | Gauge conversion and yardage estimation functions | Unit tests pass; calculations within ±5% |
| **Distribution Algorithms** | Even distribution and Bresenham spacing implementations | No stacked deltas visible in test outputs |
| **US/UK Translator** | Terminology translator for MVP stitch types | All MVP terms translate correctly |
| **Test Suite** | Comprehensive pytest suite with 80%+ coverage | All tests green; benchmarks documented |
| **Performance Benchmarks** | Documentation of generation times for typical inputs | < 200ms target met for all shapes |

### Non-Goals (Deferred to Later Phases)

- Visualization rendering (Phase 2)
- API endpoints (Phase 2)
- Mobile app integration (Phase 2+)
- Export functionality (Phase 3)
- Joined rounds or HDC/DC stitches (v1.1)
- Advanced colorwork (v1.1)

---

## Epic Breakdown

### EPIC A: Pattern Engine (Python)

**Epic Owner:** Backend Lead
**Epic Duration:** Weeks 3-4 (Full Phase 1)
**Total Effort:** ~80 story points
**Priority:** P0 (Critical Path)

#### Epic Overview

Implement the core pattern compilation logic for geometric shapes (sphere, cylinder, cone). This epic encompasses all the fundamental algorithms that convert physical dimensions and gauge specifications into step-by-step crochet instructions.

#### Epic Goals

- Sphere, cylinder, and cone patterns generate in < 200ms
- Outputs are mathematically accurate and follow crochet conventions
- Unit tests cover edge cases and performance
- Code is maintainable and well-documented

#### Epic Stories Summary

| Story ID | Title | Effort | Priority | Dependencies |
|----------|-------|--------|----------|--------------|
| A1 | Gauge mapping & yardage estimator | 5 pt | P0 | None |
| A2 | Sphere compiler (sc, spiral) | 13 pt | P0 | A1, A5 |
| A3 | Cylinder compiler (with caps) | 10 pt | P0 | A1, A2, A5 |
| A4 | Cone/tapered compiler (Bresenham) | 13 pt | P0 | A1, A5 |
| A5 | Even distribution algorithm | 8 pt | P0 | None |
| A6 | US ↔ UK translator | 3 pt | P1 | None |
| TEST-1 | Unit tests: Sphere | 8 pt | P0 | A2 |
| TEST-2 | Unit tests: Cylinder | 6 pt | P0 | A3 |
| TEST-3 | Unit tests: Cone | 6 pt | P0 | A4 |
| TEST-4 | Unit tests: Algorithms | 6 pt | P0 | A1, A5, A6 |
| TEST-5 | Performance benchmarks | 3 pt | P0 | A2, A3, A4 |

**Total:** 81 story points

#### Epic Acceptance Criteria

- **AC-G-1:** Generating a 10 cm sphere (14/16 gauge, US sc, spiral) produces expected equator stitch count (±1 stitch tolerance)
- **AC-G-2:** Tapered limb from 6 cm → 2 cm over 8 cm height has monotonic taper with no stacked deltas
- **AC-G-3:** All unit tests pass with coverage > 80%
- **AC-G-4:** Performance < 200ms for typical inputs (10 cm sphere, 8 cm cylinder, 8 cm cone)
- **AC-G-5:** Code review approved by backend lead
- **AC-G-6:** Documentation includes docstrings and inline comments for complex algorithms

---

## Sprint Plans

### Sprint 2: Core Shape Compilers (Week 3)

**Sprint Goal:** Implement all three shape compilers and foundational algorithms; begin testing

**Sprint Duration:** 1 week (5 working days)
**Sprint Capacity:** ~45-50 story points
**Team:** 2 backend engineers, 1 QA engineer

#### Sprint 2 Stories

**Backend Engineering Track:**

| Story ID | Title | Assignee | Effort | Status |
|----------|-------|----------|--------|--------|
| A1 | Gauge mapping & yardage estimator | Backend Engineer 1 | 5 pt | Sprint 2 |
| A5 | Even distribution algorithm | Backend Engineer 1 | 8 pt | Sprint 2 |
| A2 | Sphere compiler (sc, spiral) | Backend Engineer 1 | 13 pt | Sprint 2 |
| A3 | Cylinder compiler (with caps) | Backend Engineer 2 | 10 pt | Sprint 2 |
| A6 | US ↔ UK translator | Backend Engineer 2 | 3 pt | Sprint 2 |

**Testing Track:**

| Story ID | Title | Assignee | Effort | Status |
|----------|-------|----------|--------|--------|
| TEST-1 | Unit tests: Sphere | QA Engineer + BE1 | 8 pt | Sprint 2 (starts mid-sprint) |

**Total Sprint 2 Allocation:** 47 story points

#### Sprint 2 Daily Standup Focus

**Monday (Day 1):**
- Kickoff: Review algorithm spike outputs from Phase 0
- Start A1 (gauge mapping) and A5 (distribution) in parallel
- Set up test fixtures and test data

**Tuesday (Day 2):**
- Continue A1 and A5
- Begin A3 (cylinder) on second backend engineer
- Review sphere algorithm approach

**Wednesday (Day 3):**
- Complete A1 (gauge mapping)
- A5 (distribution) in progress
- A3 (cylinder) in progress
- Start A2 (sphere compiler) using completed A1

**Thursday (Day 4):**
- Complete A5 (distribution)
- A2 (sphere) in progress, using A5
- Complete A3 (cylinder)
- Start A6 (US/UK translator)
- Begin TEST-1 (sphere unit tests)

**Friday (Day 5):**
- Complete A2 (sphere compiler)
- Complete A6 (translator)
- Continue TEST-1 (sphere tests)
- Sprint 2 demo: Show working sphere and cylinder generation
- Sprint 2 retrospective

#### Sprint 2 Demo Objectives

- **Demo Item 1:** Generate a 10 cm sphere pattern with 14/16 gauge; show DSL output
- **Demo Item 2:** Generate an 8 cm cylinder with caps; show cap rounds vs. body rounds
- **Demo Item 3:** Show even distribution output for various stitch counts
- **Demo Item 4:** Demonstrate US → UK term translation for sample pattern

#### Sprint 2 Success Criteria

- [ ] Sphere compiler generates valid patterns
- [ ] Cylinder compiler generates valid patterns with correct cap dimensions
- [ ] Gauge mapping and distribution algorithms work correctly
- [ ] First round of unit tests written for sphere
- [ ] No critical blockers for Sprint 3

---

### Sprint 3 (Partial): Cone Compiler & Testing (Week 4)

**Sprint Goal:** Complete cone compiler; finish comprehensive test coverage; meet performance benchmarks

**Sprint Duration:** 1 week (5 working days)
**Sprint Capacity:** ~45-50 story points
**Team:** 2 backend engineers, 1 QA engineer

**Note:** Sprint 3 spans Week 4-5. Phase 1 concludes at the end of Week 4, so only Week 4 stories are included here. Week 5 stories begin Phase 2 (Visualization).

#### Sprint 3 Stories (Phase 1 Portion)

**Backend Engineering Track:**

| Story ID | Title | Assignee | Effort | Status |
|----------|-------|----------|--------|--------|
| A4 | Cone/tapered compiler (Bresenham) | Backend Engineer 1 | 13 pt | Sprint 3 |

**Testing Track:**

| Story ID | Title | Assignee | Effort | Status |
|----------|-------|----------|--------|--------|
| TEST-1 | Unit tests: Sphere (completion) | QA Engineer + BE1 | 4 pt remaining | Sprint 3 |
| TEST-2 | Unit tests: Cylinder | QA Engineer + BE2 | 6 pt | Sprint 3 |
| TEST-3 | Unit tests: Cone | QA Engineer + BE1 | 6 pt | Sprint 3 |
| TEST-4 | Unit tests: Algorithms | QA Engineer | 6 pt | Sprint 3 |
| TEST-5 | Performance benchmarks | QA Engineer + BE2 | 3 pt | Sprint 3 |

**Total Sprint 3 Allocation (Phase 1):** 38 story points

#### Sprint 3 Daily Standup Focus (Week 4)

**Monday (Day 1):**
- Start A4 (cone compiler) with focus on Bresenham distribution
- Complete TEST-1 (sphere unit tests)
- Begin TEST-2 (cylinder tests)

**Tuesday (Day 2):**
- A4 (cone) in progress
- Complete TEST-2 (cylinder tests)
- Begin TEST-4 (algorithm tests)

**Wednesday (Day 3):**
- Continue A4 (cone compiler)
- Complete TEST-4 (algorithm tests)
- Begin TEST-3 (cone tests) with stub compiler

**Thursday (Day 4):**
- Complete A4 (cone compiler)
- Continue TEST-3 (cone tests) with real compiler
- Begin TEST-5 (performance benchmarks)

**Friday (Day 5):**
- Complete TEST-3 and TEST-5
- Code review for all Phase 1 work
- Phase 1 demo and retrospective
- Phase 1 exit criteria review

#### Sprint 3 Demo Objectives (End of Phase 1)

- **Demo Item 1:** Generate a tapered limb pattern (6 cm → 2 cm over 8 cm); show smooth taper
- **Demo Item 2:** Run full test suite; show 80%+ coverage report
- **Demo Item 3:** Run performance benchmarks; show all shapes < 200ms
- **Demo Item 4:** Demonstrate all three shapes with US and UK terminology

#### Sprint 3 Success Criteria (Phase 1 Exit)

- [ ] Cone compiler generates valid tapered patterns
- [ ] Full test suite passes with 80%+ coverage
- [ ] Performance benchmarks meet < 200ms target
- [ ] All Phase 1 exit criteria met (see Phase Exit Criteria section)
- [ ] Code review approved and merged to main branch

---

## Technical Implementation Details

### Architecture Overview

The pattern engine is implemented as a standalone Python package (`knit_wit_engine`) that can be used by both the FastAPI backend and standalone scripts. The architecture follows object-oriented principles with clear separation of concerns.

```
knit_wit_engine/
├── __init__.py
├── algorithms/
│   ├── __init__.py
│   ├── gauge.py           # Gauge conversions, yardage estimation
│   ├── distribution.py    # Even distribution, Bresenham
│   └── translator.py      # US ↔ UK term translation
├── shapes/
│   ├── __init__.py
│   ├── base.py            # ShapeCompiler abstract base class
│   ├── sphere.py          # SphereCompiler
│   ├── cylinder.py        # CylinderCompiler
│   └── cone.py            # ConeCompiler
├── models/
│   ├── __init__.py
│   ├── dsl.py             # PatternDSL, Round, Operation Pydantic models
│   └── requests.py        # GenerateRequest, Gauge models
└── tests/
    ├── unit/
    │   ├── test_sphere.py
    │   ├── test_cylinder.py
    │   ├── test_cone.py
    │   └── test_algorithms.py
    └── fixtures/
        └── sample_patterns.py
```

### Key Algorithms

#### 1. Gauge Mapping & Yardage Estimation

**File:** `knit_wit_engine/algorithms/gauge.py`

**Purpose:** Convert user-provided gauge specifications (stitches per 10cm, rows per 10cm) into parameters for pattern generation. Estimate yarn yardage based on stitch count and yarn weight.

**Algorithm:**

```python
def gauge_to_stitch_length(gauge: Gauge, yarn_weight: str) -> float:
    """
    Calculate average stitch length in cm.

    Args:
        gauge: Gauge object with sts_per_10cm and rows_per_10cm
        yarn_weight: One of 'Baby', 'DK', 'Worsted', 'Bulky'

    Returns:
        Average stitch length in cm
    """
    # Base stitch length from gauge
    base_length = 10.0 / gauge.sts_per_10cm

    # Yarn weight factor (empirical)
    weight_factors = {
        'Baby': 0.5,
        'DK': 0.6,
        'Worsted': 0.7,
        'Bulky': 0.9
    }
    factor = weight_factors.get(yarn_weight, 0.7)

    return base_length * factor

def estimate_yardage(stitch_count: int, stitch_length: float) -> float:
    """
    Estimate yarn yardage in meters.

    Args:
        stitch_count: Total number of stitches in pattern
        stitch_length: Average stitch length in cm

    Returns:
        Estimated yardage in meters, including 10% waste factor
    """
    total_cm = stitch_count * stitch_length
    total_meters = total_cm / 100.0

    # Add 10% waste factor
    return total_meters * 1.1
```

**Test Cases:**
- Standard gauge (14 sts/10cm) with worsted yarn
- Fine gauge (18 sts/10cm) with DK yarn
- Coarse gauge (10 sts/10cm) with bulky yarn
- Edge cases: very fine (24 sts/10cm), very coarse (6 sts/10cm)

---

#### 2. Even Distribution Algorithm

**File:** `knit_wit_engine/algorithms/distribution.py`

**Purpose:** Distribute increases or decreases evenly around a round's circumference to avoid visible columns or stacking.

**Algorithm:**

```python
def even_distribution(total_stitches: int, num_changes: int, offset: int = 0) -> List[int]:
    """
    Calculate stitch indices for evenly distributed changes.

    Uses a Bresenham-like line-drawing algorithm to space changes as evenly as possible.

    Args:
        total_stitches: Total number of stitches in the round
        num_changes: Number of increases or decreases to place
        offset: Starting offset (for jittering across rounds)

    Returns:
        List of stitch indices (1-indexed) where changes occur
    """
    if num_changes <= 0:
        return []
    if num_changes >= total_stitches:
        # One change per stitch
        return list(range(1, total_stitches + 1))

    indices = []
    gap = total_stitches / num_changes
    position = offset

    for i in range(num_changes):
        # Round to nearest integer position
        stitch_index = int(round(position + gap))
        if stitch_index > total_stitches:
            stitch_index -= total_stitches  # Wrap around
        indices.append(stitch_index)
        position += gap

    return sorted(indices)

def jitter_offset(round_number: int, base_offset: int = 0) -> int:
    """
    Calculate jittered offset for consecutive rounds to avoid column stacking.

    Args:
        round_number: Current round number (1-indexed)
        base_offset: Base offset to add to jitter

    Returns:
        Offset value for even_distribution
    """
    # Simple jitter: alternate offset by half-gap
    jitter = (round_number % 2) * 3
    return base_offset + jitter
```

**Example:**

```python
# Distribute 6 increases evenly in 36 stitches
indices = even_distribution(36, 6)
# Result: [6, 12, 18, 24, 30, 36]
# Every 6th stitch is an increase

# With offset (for next round)
indices_r2 = even_distribution(42, 7, offset=3)
# Result: [9, 15, 21, 27, 33, 39, 45]
# Offset prevents column stacking
```

**Test Cases:**
- Perfect division: 36 stitches, 6 changes → every 6th stitch
- Imperfect division: 37 stitches, 6 changes → gaps of 6 and 7
- Edge cases: 1 change, total_stitches changes, 0 changes
- Offset behavior across multiple rounds

---

#### 3. Sphere Compiler Algorithm

**File:** `knit_wit_engine/shapes/sphere.py`
**Class:** `SphereCompiler(ShapeCompiler)`

**Purpose:** Generate a complete sphere pattern with even increases and decreases in spiral rounds.

**Algorithm Steps:**

1. **Calculate Parameters:**
   - radius = diameter / 2
   - equator_stitches = π × diameter × (gauge.sts_per_10cm / 10)
   - equator_rounds = gauge.rows_per_10cm × radius / 10

2. **Increase Phase:**
   - Start: Magic ring with 6 sc
   - Target: Reach equator_stitches over increase_rounds
   - Each round: Calculate increments needed: `(target - current) / remaining_rounds`
   - Use `even_distribution()` to place increases evenly
   - Jitter offset each round to avoid columns

3. **Steady Phase (Optional):**
   - 1-2 rounds at equator_stitches (no increases)
   - Provides structural stability at widest point

4. **Decrease Phase:**
   - Mirror the increase phase in reverse
   - Distribute decreases evenly using `even_distribution()`
   - End: Close with 6 stitches, pull tight

**Pseudocode:**

```python
class SphereCompiler(ShapeCompiler):
    def generate(self, request: GenerateRequest) -> PatternDSL:
        # 1. Calculate parameters
        radius = request.diameter / 2
        equator_stitches = self._calc_equator_stitches(request.diameter, request.gauge)
        increase_rounds = self._calc_increase_rounds(equator_stitches, request.gauge)

        rounds = []
        current_stitches = 6

        # 2. Magic ring start
        rounds.append(Round(
            round_number=1,
            operations=[MagicRing(6)],
            stitch_count=6,
            instructions="MR 6 sc"
        ))

        # 3. Increase phase
        for r in range(2, increase_rounds + 2):
            remaining_rounds = increase_rounds + 2 - r
            target_increase = (equator_stitches - current_stitches) // remaining_rounds

            # Distribute increases evenly
            offset = jitter_offset(r)
            inc_indices = even_distribution(current_stitches, target_increase, offset)

            # Build operations list
            operations = self._build_operations(current_stitches, inc_indices)
            new_stitch_count = current_stitches + target_increase

            rounds.append(Round(
                round_number=r,
                operations=operations,
                stitch_count=new_stitch_count,
                instructions=self._format_instructions(operations)
            ))

            current_stitches = new_stitch_count

        # 4. Steady rounds (1-2 rounds at equator)
        for r in range(increase_rounds + 2, increase_rounds + 4):
            rounds.append(Round(
                round_number=r,
                operations=[SingleCrochet(equator_stitches)],
                stitch_count=equator_stitches,
                instructions=f"{equator_stitches} sc"
            ))

        # 5. Decrease phase (mirror of increase)
        decrease_rounds = increase_rounds
        for r in range(increase_rounds + 4, increase_rounds + decrease_rounds + 4):
            remaining_rounds = decrease_rounds - (r - increase_rounds - 4)
            target_decrease = (current_stitches - 6) // remaining_rounds

            # Distribute decreases evenly
            offset = jitter_offset(r)
            dec_indices = even_distribution(current_stitches, target_decrease, offset)

            operations = self._build_decrease_operations(current_stitches, dec_indices)
            new_stitch_count = current_stitches - target_decrease

            rounds.append(Round(
                round_number=r,
                operations=operations,
                stitch_count=new_stitch_count,
                instructions=self._format_instructions(operations)
            ))

            current_stitches = new_stitch_count

        # 6. Close
        rounds.append(Round(
            round_number=len(rounds) + 1,
            operations=[FinishOff()],
            stitch_count=6,
            instructions="Finish off, weave in ends"
        ))

        # 7. Build complete DSL
        return PatternDSL(
            shape='sphere',
            rounds=rounds,
            metadata=self._build_metadata(request)
        )
```

**Key Implementation Details:**
- **Even spacing:** `even_distribution()` prevents clustering
- **Jittering:** Offset changes per round to avoid visible columns
- **Flexibility:** Algorithm adapts to any gauge and diameter
- **Performance:** O(n) where n = number of rounds (typically 20-50)

**Test Cases:**
- Standard 10 cm sphere, 14/16 gauge → verify equator stitch count
- Small 5 cm sphere → verify no negative rounds
- Large 20 cm sphere → verify performance < 200ms
- Different gauges (10, 14, 18, 22 sts/10cm)

---

#### 4. Cylinder Compiler Algorithm

**File:** `knit_wit_engine/shapes/cylinder.py`
**Class:** `CylinderCompiler(ShapeCompiler)`

**Purpose:** Generate a cylinder pattern with optional hemisphere caps (top and bottom).

**Algorithm Steps:**

1. **Calculate Parameters:**
   - cap_rounds = gauge.rows_per_10cm × (diameter / 4) / 10  [hemisphere = quarter of sphere]
   - body_rounds = gauge.rows_per_10cm × height / 10
   - circumference_stitches = π × diameter × (gauge.sts_per_10cm / 10)

2. **Bottom Cap (if enabled):**
   - Use same algorithm as sphere increase phase
   - Start: Magic ring 6 sc
   - End: circumference_stitches

3. **Body:**
   - Repeat circumference_stitches sc for body_rounds rounds
   - No increases or decreases

4. **Top Cap (if enabled):**
   - Mirror of bottom cap (decrease phase)
   - Start: circumference_stitches
   - End: 6 sc, close

**Pseudocode:**

```python
class CylinderCompiler(ShapeCompiler):
    def generate(self, request: GenerateRequest) -> PatternDSL:
        # 1. Calculate parameters
        diameter = request.diameter
        height = request.height
        has_caps = request.options.get('caps', True)

        circumference_stitches = self._calc_circumference(diameter, request.gauge)
        cap_rounds = self._calc_cap_rounds(diameter, request.gauge) if has_caps else 0
        body_rounds = self._calc_body_rounds(height, request.gauge)

        rounds = []
        round_num = 1

        # 2. Bottom cap (if enabled)
        if has_caps:
            cap_rounds_list = self._generate_hemisphere_cap(
                start_stitches=6,
                end_stitches=circumference_stitches,
                num_rounds=cap_rounds,
                start_round=round_num
            )
            rounds.extend(cap_rounds_list)
            round_num += len(cap_rounds_list)
        else:
            # Start with a flat circle if no cap
            rounds.append(Round(
                round_number=round_num,
                operations=[ChainLoop(circumference_stitches)],
                stitch_count=circumference_stitches,
                instructions=f"Ch {circumference_stitches}, join"
            ))
            round_num += 1

        # 3. Body (constant stitch count)
        for i in range(body_rounds):
            rounds.append(Round(
                round_number=round_num,
                operations=[SingleCrochet(circumference_stitches)],
                stitch_count=circumference_stitches,
                instructions=f"{circumference_stitches} sc"
            ))
            round_num += 1

        # 4. Top cap (if enabled)
        if has_caps:
            cap_rounds_list = self._generate_hemisphere_cap(
                start_stitches=circumference_stitches,
                end_stitches=6,
                num_rounds=cap_rounds,
                start_round=round_num,
                direction='decrease'
            )
            rounds.extend(cap_rounds_list)
            round_num += len(cap_rounds_list)

            # Close
            rounds.append(Round(
                round_number=round_num,
                operations=[FinishOff()],
                stitch_count=6,
                instructions="Finish off, weave in ends"
            ))

        return PatternDSL(
            shape='cylinder',
            rounds=rounds,
            metadata=self._build_metadata(request)
        )

    def _generate_hemisphere_cap(self, start_stitches, end_stitches,
                                   num_rounds, start_round, direction='increase'):
        """Helper to generate cap rounds (reusable for top/bottom)."""
        # Similar logic to sphere increase/decrease phase
        # Uses even_distribution() for spacing
        # Returns list of Round objects
        pass
```

**Key Implementation Details:**
- **Reusable caps:** `_generate_hemisphere_cap()` works for both top and bottom
- **Optional caps:** User can choose closed cylinder (with caps) or tube (no caps)
- **Body simplicity:** Constant stitch count = fast generation
- **Performance:** O(n) where n = cap_rounds + body_rounds

**Test Cases:**
- 8 cm diameter, 10 cm height with caps → verify cap dimensions
- Tube (no caps) → verify flat start and open end
- Very tall cylinder → verify body rounds scale correctly
- Different gauges

---

#### 5. Cone/Tapered Compiler Algorithm

**File:** `knit_wit_engine/shapes/cone.py`
**Class:** `ConeCompiler(ShapeCompiler)`

**Purpose:** Generate a tapered pattern that smoothly transitions from one diameter to another without stacking deltas.

**Algorithm Steps:**

1. **Calculate Parameters:**
   - start_stitches = π × diameter_start × (gauge.sts_per_10cm / 10)
   - end_stitches = π × diameter_end × (gauge.sts_per_10cm / 10)
   - total_rounds = gauge.rows_per_10cm × height / 10
   - delta_total = start_stitches - end_stitches

2. **Bresenham Distribution:**
   - Decide which rounds need a delta (increase or decrease)
   - Use Bresenham line-drawing logic to space deltas evenly
   - Formula: `target_delta(round) = round(delta_total × round / total_rounds)`

3. **Per-Round Delta Placement:**
   - For each round, determine how many stitches to add/remove
   - Use `even_distribution()` to place deltas around circumference
   - Jitter offset to avoid column stacking

**Algorithm Pseudocode:**

```python
class ConeCompiler(ShapeCompiler):
    def generate(self, request: GenerateRequest) -> PatternDSL:
        # 1. Calculate parameters
        diameter_start = request.diameter_start
        diameter_end = request.diameter_end
        height = request.height

        start_stitches = self._calc_circumference(diameter_start, request.gauge)
        end_stitches = self._calc_circumference(diameter_end, request.gauge)
        total_rounds = self._calc_rounds(height, request.gauge)

        delta_total = start_stitches - end_stitches
        direction = 'decrease' if delta_total > 0 else 'increase'
        delta_total = abs(delta_total)

        rounds = []
        current_stitches = start_stitches
        cumulative_delta = 0

        # 2. Starting round
        rounds.append(Round(
            round_number=1,
            operations=[ChainLoop(start_stitches)],
            stitch_count=start_stitches,
            instructions=f"Ch {start_stitches}, join"
        ))

        # 3. Taper rounds (Bresenham distribution)
        for r in range(2, total_rounds + 1):
            # Calculate target delta up to this round
            target_cumulative = round(delta_total * (r - 1) / total_rounds)

            # How many deltas to apply this round?
            round_delta = target_cumulative - cumulative_delta

            if round_delta > 0:
                # Apply delta(s) this round
                offset = jitter_offset(r)
                delta_indices = even_distribution(current_stitches, round_delta, offset)

                if direction == 'decrease':
                    operations = self._build_decrease_operations(current_stitches, delta_indices)
                    new_stitch_count = current_stitches - round_delta
                else:
                    operations = self._build_increase_operations(current_stitches, delta_indices)
                    new_stitch_count = current_stitches + round_delta

                cumulative_delta += round_delta
            else:
                # No delta this round
                operations = [SingleCrochet(current_stitches)]
                new_stitch_count = current_stitches

            rounds.append(Round(
                round_number=r,
                operations=operations,
                stitch_count=new_stitch_count,
                instructions=self._format_instructions(operations)
            ))

            current_stitches = new_stitch_count

        # 4. Finish
        rounds.append(Round(
            round_number=total_rounds + 1,
            operations=[FinishOff()],
            stitch_count=end_stitches,
            instructions="Finish off, weave in ends"
        ))

        return PatternDSL(
            shape='cone',
            rounds=rounds,
            metadata=self._build_metadata(request)
        )
```

**Bresenham Logic Explained:**

The key insight is to use a line-drawing algorithm to decide which rounds receive a delta:

```
Target line: from (0, 0) to (total_rounds, delta_total)
For each round r:
  ideal_y = delta_total * r / total_rounds
  actual_y = cumulative_delta
  if round(ideal_y) > actual_y:
    apply 1 delta this round
```

This ensures deltas are spaced as evenly as possible across rounds, avoiding clustering.

**Key Implementation Details:**
- **Monotonic taper:** Stitch count changes smoothly from start to end
- **No stacking:** Bresenham + jittering prevent visible columns
- **Flexible direction:** Works for both tapering in (decrease) and out (increase)
- **Performance:** O(n) where n = total_rounds

**Test Cases:**
- 6 cm → 2 cm over 8 cm height → verify monotonic decrease, no stacking (AC-G-2)
- 2 cm → 6 cm over 8 cm height → verify monotonic increase
- Very gradual taper (10 cm → 9 cm over 20 cm)
- Steep taper (8 cm → 2 cm over 5 cm)

---

#### 6. US ↔ UK Translator

**File:** `knit_wit_engine/algorithms/translator.py`

**Purpose:** Translate stitch terminology between US and UK conventions.

**Implementation:**

```python
# US → UK mappings (for MVP stitches only)
US_TO_UK = {
    'sc': 'dc',          # single crochet → double crochet
    'inc': 'inc',        # increase (same term)
    'dec': 'dec',        # decrease (same term)
    'ch': 'ch',          # chain (same term)
    'slst': 'ss',        # slip stitch → slip stitch (ss)
    'MR': 'MR',          # magic ring (same term)
}

UK_TO_US = {v: k for k, v in US_TO_UK.items()}

def translate_term(term: str, from_convention: str, to_convention: str) -> str:
    """
    Translate a crochet term between US and UK conventions.

    Args:
        term: The term to translate (e.g., 'sc', 'dc')
        from_convention: 'US' or 'UK'
        to_convention: 'US' or 'UK'

    Returns:
        Translated term

    Raises:
        ValueError: If term is unknown or conventions are invalid
    """
    if from_convention == to_convention:
        return term

    if from_convention == 'US' and to_convention == 'UK':
        if term not in US_TO_UK:
            raise ValueError(f"Unknown US term: {term}")
        return US_TO_UK[term]

    if from_convention == 'UK' and to_convention == 'US':
        if term not in UK_TO_US:
            raise ValueError(f"Unknown UK term: {term}")
        return UK_TO_US[term]

    raise ValueError(f"Invalid conventions: {from_convention}, {to_convention}")

def translate_pattern_dsl(dsl: PatternDSL, to_convention: str) -> PatternDSL:
    """
    Translate all terms in a PatternDSL to target convention.

    Args:
        dsl: PatternDSL object
        to_convention: 'US' or 'UK'

    Returns:
        New PatternDSL with translated terms
    """
    # Deep copy DSL
    translated_dsl = dsl.copy(deep=True)

    # Translate operations in each round
    for round in translated_dsl.rounds:
        for op in round.operations:
            op.stitch_type = translate_term(
                op.stitch_type,
                dsl.metadata.convention,
                to_convention
            )

    translated_dsl.metadata.convention = to_convention
    return translated_dsl
```

**Test Cases:**
- Translate 'sc' US → UK → 'dc'
- Translate 'inc' (same in both)
- Translate full pattern DSL (sphere) from US to UK
- Error handling for unknown terms

---

### Data Models (Pydantic)

**File:** `knit_wit_engine/models/dsl.py`

```python
from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class Operation(BaseModel):
    """Represents a single stitch operation."""
    type: Literal['sc', 'inc', 'dec', 'ch', 'slst', 'MR', 'finish']
    count: int = 1
    detail: Optional[str] = None  # e.g., "2 sc in same st"

class Round(BaseModel):
    """Represents a single round in the pattern."""
    round_number: int
    operations: List[Operation]
    stitch_count: int
    instructions: str  # Human-readable text

class Metadata(BaseModel):
    """Pattern metadata."""
    shape: str
    diameter: Optional[float] = None
    height: Optional[float] = None
    gauge: dict
    convention: Literal['US', 'UK'] = 'US'
    yarn_weight: Optional[str] = None
    estimated_yardage: Optional[float] = None

class PatternDSL(BaseModel):
    """Complete pattern in DSL format."""
    shape: str
    rounds: List[Round]
    metadata: Metadata
```

**File:** `knit_wit_engine/models/requests.py`

```python
from pydantic import BaseModel, Field
from typing import Optional, Literal

class Gauge(BaseModel):
    """Gauge specification."""
    sts_per_10cm: float = Field(..., gt=0, description="Stitches per 10 cm")
    rows_per_10cm: float = Field(..., gt=0, description="Rows per 10 cm")

class GenerateRequest(BaseModel):
    """Request to generate a pattern."""
    shape: Literal['sphere', 'cylinder', 'cone']
    diameter: Optional[float] = Field(None, gt=0, description="Diameter in cm")
    diameter_start: Optional[float] = Field(None, gt=0, description="Start diameter for cone")
    diameter_end: Optional[float] = Field(None, gt=0, description="End diameter for cone")
    height: Optional[float] = Field(None, gt=0, description="Height in cm")
    gauge: Gauge
    stitch_type: Literal['sc'] = 'sc'  # MVP: only sc supported
    round_mode: Literal['spiral', 'joined'] = 'spiral'  # MVP: only spiral
    convention: Literal['US', 'UK'] = 'US'
    yarn_weight: Optional[str] = 'Worsted'
    options: Optional[dict] = {}
```

---

### Testing Strategy

#### Unit Testing (pytest)

**Coverage Goals:**
- Pattern engine: 80%+ line coverage
- Algorithms: 90%+ coverage
- Test each shape compiler independently

**Key Test Files:**

**`tests/unit/test_sphere.py`:**
```python
import pytest
from knit_wit_engine.shapes.sphere import SphereCompiler
from knit_wit_engine.models.requests import GenerateRequest, Gauge

def test_sphere_10cm_sc_spiral_gauge_14_16():
    """Test standard 10 cm sphere with 14/16 gauge."""
    compiler = SphereCompiler()
    request = GenerateRequest(
        shape='sphere',
        diameter=10,
        gauge=Gauge(sts_per_10cm=14, rows_per_10cm=16),
        stitch_type='sc',
        round_mode='spiral',
        convention='US'
    )

    dsl = compiler.generate(request)

    # Verify DSL structure
    assert dsl.shape == 'sphere'
    assert len(dsl.rounds) > 10
    assert dsl.rounds[0].stitch_count == 6  # Magic ring start

    # Verify equator stitches
    max_stitches = max(r.stitch_count for r in dsl.rounds)
    expected_equator = round(3.14159 * 10 * 14 / 10)  # π × d × gauge / 10
    assert abs(max_stitches - expected_equator) <= 2  # Tolerance: ±2 stitches

    # Verify monotonic increase then decrease
    stitch_counts = [r.stitch_count for r in dsl.rounds]
    equator_index = stitch_counts.index(max_stitches)

    # Increase phase should be monotonic increasing
    assert all(stitch_counts[i] <= stitch_counts[i+1]
               for i in range(equator_index))

    # Decrease phase should be monotonic decreasing
    assert all(stitch_counts[i] >= stitch_counts[i+1]
               for i in range(equator_index, len(stitch_counts) - 1))

def test_sphere_even_distribution():
    """Test that increases are evenly distributed (no visible columns)."""
    compiler = SphereCompiler()
    request = GenerateRequest(
        shape='sphere',
        diameter=10,
        gauge=Gauge(sts_per_10cm=14, rows_per_10cm=16)
    )

    dsl = compiler.generate(request)

    # Extract increase positions from each round
    for round in dsl.rounds[1:10]:  # Check first 10 rounds
        inc_ops = [op for op in round.operations if op.type == 'inc']
        if len(inc_ops) > 1:
            # Verify spacing is roughly even
            # (Detailed implementation checks gap variance)
            assert True  # Placeholder for detailed check

def test_sphere_performance():
    """Test that generation completes in < 200ms."""
    import time

    compiler = SphereCompiler()
    request = GenerateRequest(
        shape='sphere',
        diameter=10,
        gauge=Gauge(sts_per_10cm=14, rows_per_10cm=16)
    )

    start = time.time()
    dsl = compiler.generate(request)
    elapsed = time.time() - start

    assert elapsed < 0.2  # 200ms
```

**`tests/unit/test_algorithms.py`:**
```python
from knit_wit_engine.algorithms.distribution import even_distribution, jitter_offset
from knit_wit_engine.algorithms.gauge import estimate_yardage
from knit_wit_engine.algorithms.translator import translate_term

def test_even_distribution_perfect_division():
    """Test even distribution with perfect division."""
    indices = even_distribution(36, 6)
    assert indices == [6, 12, 18, 24, 30, 36]

    # Verify even spacing
    gaps = [indices[i+1] - indices[i] for i in range(len(indices) - 1)]
    assert all(gap == 6 for gap in gaps)

def test_even_distribution_imperfect_division():
    """Test even distribution with imperfect division."""
    indices = even_distribution(37, 6)
    assert len(indices) == 6

    # Gaps should be 6 or 7 (differ by at most 1)
    gaps = [indices[i+1] - indices[i] for i in range(len(indices) - 1)]
    assert all(gap in [6, 7] for gap in gaps)

def test_even_distribution_edge_cases():
    """Test edge cases."""
    # Zero changes
    assert even_distribution(36, 0) == []

    # One change per stitch
    assert len(even_distribution(10, 10)) == 10

    # Single change
    assert len(even_distribution(36, 1)) == 1

def test_translate_us_to_uk():
    """Test US → UK term translation."""
    assert translate_term('sc', 'US', 'UK') == 'dc'
    assert translate_term('inc', 'US', 'UK') == 'inc'
    assert translate_term('slst', 'US', 'UK') == 'ss'

def test_translate_uk_to_us():
    """Test UK → US term translation."""
    assert translate_term('dc', 'UK', 'US') == 'sc'

def test_estimate_yardage():
    """Test yardage estimation."""
    # 100 stitches, 0.7 cm each = 70 cm = 0.7 m
    # With 10% waste = 0.77 m
    yardage = estimate_yardage(100, 0.7)
    assert abs(yardage - 0.77) < 0.01
```

#### Performance Benchmarking

**File:** `tests/unit/test_performance.py`

```python
import pytest
import time
from knit_wit_engine.shapes import SphereCompiler, CylinderCompiler, ConeCompiler
from knit_wit_engine.models.requests import GenerateRequest, Gauge

@pytest.mark.benchmark
def test_benchmark_sphere_10cm():
    """Benchmark sphere generation."""
    compiler = SphereCompiler()
    request = GenerateRequest(
        shape='sphere',
        diameter=10,
        gauge=Gauge(sts_per_10cm=14, rows_per_10cm=16)
    )

    # Run 100 times for statistical average
    times = []
    for _ in range(100):
        start = time.perf_counter()
        dsl = compiler.generate(request)
        elapsed = time.perf_counter() - start
        times.append(elapsed)

    avg_time = sum(times) / len(times)
    max_time = max(times)

    print(f"\nSphere 10cm benchmark:")
    print(f"  Average: {avg_time*1000:.2f} ms")
    print(f"  Max: {max_time*1000:.2f} ms")

    assert avg_time < 0.2  # 200ms
    assert max_time < 0.3  # 300ms worst case

# Similar benchmarks for cylinder and cone
```

---

## Success Criteria

### Phase 1 Success Criteria

Phase 1 is considered successful when all of the following criteria are met:

- [ ] **Sphere Compiler Complete:** `SphereCompiler.generate()` produces valid patterns for all test cases
- [ ] **Cylinder Compiler Complete:** `CylinderCompiler.generate()` produces valid patterns with correct cap dimensions
- [ ] **Cone Compiler Complete:** `ConeCompiler.generate()` produces smooth tapers with no stacked deltas
- [ ] **Test Coverage:** Unit test coverage > 80% for pattern-engine package
- [ ] **Performance Targets:** All shape compilers generate patterns in < 200ms for typical inputs
- [ ] **Acceptance Criteria Met:**
  - AC-G-1: 10 cm sphere (14/16 gauge) has correct equator stitch count (±1)
  - AC-G-2: Tapered limb (6 cm → 2 cm over 8 cm) has monotonic taper, no stacking
- [ ] **Code Review Approved:** All code reviewed and approved by backend lead
- [ ] **Documentation Complete:** Docstrings and inline comments present for all complex functions
- [ ] **CI/CD Green:** All tests pass in CI/CD pipeline

### Technical Quality Criteria

- [ ] **Maintainability:** Code follows Python PEP 8 style guidelines
- [ ] **Modularity:** Clear separation between algorithms, compilers, and models
- [ ] **Error Handling:** Graceful handling of edge cases (e.g., invalid gauge, negative dimensions)
- [ ] **Type Safety:** Pydantic models validate all inputs
- [ ] **Performance Profiling:** Profiling data collected and documented

### Demo Readiness

- [ ] **Demo Data:** Sample patterns prepared for all three shapes
- [ ] **Demo Script:** Step-by-step demo script prepared
- [ ] **Visualization Stubs:** Temporary CLI scripts to display DSL output for demo

---

## Dependencies & Blockers

### Dependencies

#### Internal Dependencies (from Phase 0)

| Dependency | Source | Status | Impact if Delayed |
|-----------|--------|--------|------------------|
| **Algorithm Spike Complete** | Phase 0 (ARCH-1) | ✅ Complete | HIGH - Core math must be validated |
| **Monorepo Initialized** | Phase 0 (SETUP-1) | ✅ Complete | HIGH - Cannot commit code |
| **CI/CD Pipeline** | Phase 0 (SETUP-2) | ✅ Complete | MEDIUM - Manual testing possible |
| **Pattern Engine Package Init** | Phase 0 (SETUP-4) | ✅ Complete | HIGH - No code structure |
| **DSL Schema Finalized** | Phase 0 (ARCH-2) | ✅ Complete | HIGH - Cannot define output format |

#### External Dependencies

| Dependency | Type | Status | Mitigation |
|-----------|------|--------|-----------|
| **Python 3.11+** | Runtime | Required | Use pyenv or conda for version management |
| **pytest 7+** | Testing | Required | Install via pip/poetry |
| **Pydantic v2** | Validation | Required | Pin version in requirements.txt |
| **NumPy** | Optional (math utils) | Nice-to-have | Can use standard library if needed |

### Known Blockers

| Blocker | Probability | Impact | Mitigation Plan | Owner |
|---------|-------------|--------|----------------|-------|
| **Algorithm bugs in complex shapes** | High | High | Pair programming on cone compiler; extensive unit tests | Backend Lead |
| **Performance regression on large patterns** | Medium | Medium | Profile early and often; cache intermediate results | Backend Engineer 1 |
| **Gauge assumptions prove incorrect** | Medium | Medium | Feedback loop with PRD author; allow parameter tweaking | Product Owner |
| **Test coverage falling behind** | Medium | Low | Reserve last 2 days of sprint for testing; pair QA with engineers | QA Engineer |
| **Bresenham logic difficult to implement** | Low | High | Research existing implementations; consult with algorithm expert | Backend Engineer 2 |

### Risk Mitigation Actions

- **Daily Standups:** Quick sync on blockers (15 minutes max)
- **Pair Programming:** Complex algorithms (sphere, cone) developed in pairs
- **Code Reviews:** All PRs reviewed within 24 hours
- **Spike Time:** Reserve 10% of sprint capacity for spikes if needed

---

## Risks

### Technical Risks

| Risk | Probability | Impact | Mitigation Strategy | Contingency Plan |
|------|-------------|--------|-------------------|------------------|
| **Sphere increase distribution creates visible columns** | High | High | Use jittered offsets per round; visual inspection tests | Manual pattern testing; adjust jitter algorithm |
| **Cone taper has stacked deltas despite Bresenham** | Medium | High | Unit tests verify no stacking; visual diagram checks | Increase jitter; manual pattern review |
| **Gauge calculations inaccurate for edge cases** | Medium | Medium | Test with real-world gauge samples; adjust formulas | Provide manual override parameters |
| **Performance regression with large patterns (50+ rounds)** | Medium | Medium | Benchmark continuously; profile hot paths | Optimize algorithms; cache computations |
| **Pydantic validation too strict** | Low | Low | Thorough schema testing; allow reasonable ranges | Adjust validation rules |

### Process Risks

| Risk | Probability | Impact | Mitigation Strategy | Contingency Plan |
|------|-------------|--------|-------------------|------------------|
| **Backend engineer availability (sick leave, etc.)** | Medium | High | Cross-training; pairing sessions | Extend sprint by 2-3 days |
| **Test coverage falling behind development** | Medium | Medium | Write tests alongside code; reserve test time | Add test-only day at end of sprint |
| **Scope creep (adding HDC/DC stitches)** | Low | Medium | Strict adherence to MVP scope; defer to v1.1 | Push back; document as future work |
| **Code review bottleneck** | Low | Low | Review PRs within 24 hours; distribute reviews | Backend lead prioritizes reviews |

### External Risks

| Risk | Probability | Impact | Mitigation Strategy | Contingency Plan |
|------|-------------|--------|-------------------|------------------|
| **Python 3.11 incompatibility on some systems** | Low | Medium | Test on multiple platforms; use Docker | Fallback to Python 3.10 |
| **Pydantic v2 breaking changes** | Very Low | Low | Pin version; monitor release notes | Downgrade to v1 if needed |

---

## Phase Exit Criteria

Phase 1 is complete and ready to transition to Phase 2 when **ALL** of the following exit criteria are met:

### Functional Exit Criteria

- [ ] **All Three Shape Compilers Working:**
  - Sphere compiler generates valid patterns for at least 3 different gauges
  - Cylinder compiler generates patterns with caps and without caps
  - Cone compiler generates smooth tapers for at least 3 different taper ratios

- [ ] **Acceptance Criteria Validated:**
  - AC-G-1: 10 cm sphere (14/16 gauge) equator stitch count matches expected (±1)
  - AC-G-2: Cone (6 cm → 2 cm over 8 cm) has monotonic taper, no stacking

- [ ] **Algorithm Utilities Complete:**
  - Gauge mapping and yardage estimation working
  - Even distribution algorithm tested and verified
  - US ↔ UK translator handles all MVP terms

### Quality Exit Criteria

- [ ] **Test Coverage:**
  - Unit test coverage > 80% for pattern-engine package
  - All critical paths covered by tests
  - Performance benchmarks documented

- [ ] **Code Review:**
  - All PRs reviewed and approved
  - No outstanding code review comments
  - Code follows Python style guidelines

- [ ] **Performance:**
  - All shape compilers complete generation in < 200ms for typical inputs
  - Performance benchmarks meet targets
  - No obvious performance bottlenecks

### Documentation Exit Criteria

- [ ] **Code Documentation:**
  - All public functions have docstrings
  - Complex algorithms have inline comments
  - README updated with usage examples

- [ ] **Test Documentation:**
  - Test cases documented
  - Test fixtures explained
  - Benchmark results recorded

### Process Exit Criteria

- [ ] **Demo Complete:**
  - Phase 1 demo presented to stakeholders
  - Feedback collected and documented
  - Demo scripts saved for future reference

- [ ] **Retrospective Complete:**
  - Sprint retrospective conducted
  - Action items documented
  - Lessons learned recorded

- [ ] **Handoff Ready:**
  - Phase 2 dependencies identified
  - Known issues documented
  - Transition plan to Phase 2 reviewed

### CI/CD Exit Criteria

- [ ] **CI/CD Pipeline Green:**
  - All tests pass in CI/CD
  - No failing builds on main branch
  - Deployment to dev environment successful

- [ ] **Branch Strategy:**
  - Feature branches merged to main
  - No outstanding merge conflicts
  - Release branch created for Phase 1 milestone

---

## Next Phase Preview

### Phase 2: Visualization Foundation (Weeks 5-7)

**Overview:**
Phase 2 builds on the pattern engine to create an interactive visualization system. Users will be able to see their generated patterns rendered as step-by-step diagrams.

**Key Dependencies from Phase 1:**
- PatternDSL output format (from all compilers)
- Test patterns for visualization development
- Performance benchmarks (baseline for visualization overhead)

**Phase 2 Goals:**
- Implement `Visualizer.dsl_to_frames()` to convert DSL to render primitives
- Build React Native SVG renderer component
- Create round scrubber and step controls
- Implement stitch highlighting and tooltips

**Phase 2 Stories:**
- EPIC B: Visualization (Stories B1-B9)
- EPIC D: App Shell & Navigation (Stories D1-D8)

**Transition Planning:**
- Backend Engineer 1 transitions to visualization backend support (B1)
- Backend Engineer 2 available for visualization optimization and bug fixes
- Frontend engineers onboard with pattern engine understanding

**Phase 1 → Phase 2 Handoff:**
- **Handoff Meeting:** End of Week 4 (Friday afternoon)
- **Attendees:** Backend lead, frontend lead, product owner
- **Agenda:**
  - Demo Phase 1 deliverables
  - Review Phase 1 known issues and limitations
  - Walk through PatternDSL structure and examples
  - Discuss Phase 2 visualization requirements
  - Identify integration points

**Phase 2 Preparation:**
- [ ] Export sample PatternDSL files for all three shapes
- [ ] Document DSL schema with examples
- [ ] Create mock render primitives for frontend team
- [ ] Set up frontend development environment
- [ ] Review Phase 2 design mockups

---

## Appendix

### A. Story Details

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
- Convert user gauge (sts/10cm, rows/10cm) into stitches per centimeter and rows per centimeter
- Estimate yardage based on stitch count × average stitch length + 10% waste factor
- Support common yarn weights (Baby, DK, Worsted, Bulky) with typical stitch lengths

**Acceptance Criteria:**
- [ ] `gauge_to_stitch_length(gauge: Gauge, yarn_weight: str) -> float` returns stitch length in cm
- [ ] `estimate_yardage(stitch_count: int, stitch_length: float) -> float` returns meters ± 10%
- [ ] Unit tests verify conversions against known values
- [ ] Handles edge cases (very fine gauge, very coarse gauge)
- [ ] Performance: < 1ms per call

**Technical Notes:**
- Implement in `knit_wit_engine/algorithms/gauge.py`
- Use data from standard crochet gauge references
- Stitch length formula: `yarn_weight_factor × (10 / gauge.sts_per_10cm)`
- Consider building a small YAML lookup table for yarn weights

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
- Algorithm: See Technical Implementation Details section above

**Dependencies:**
- A1 (Gauge mapping)
- A5 (Even distribution algorithm)

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
- Algorithm: See Technical Implementation Details section above

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
- Algorithm: See Technical Implementation Details section above (Bresenham detail)

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
- Algorithm: See Technical Implementation Details section above

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

### B. References

**Related Documents:**
- [Knit-Wit PRD](/Users/miethe/dev/homelab/development/ai-scratchpad/knit-wit/project_plans/mvp/knit-wit-prd.md)
- [Implementation Plan](/Users/miethe/dev/homelab/development/ai-scratchpad/knit-wit/project_plans/mvp/implementation-plan.md)
- Phase 0: Project Setup & Architecture (to be created)
- Phase 2: Visualization Foundation (to be created)

**External References:**
- [Crochet Gauge Guide](https://www.craftyarncouncil.com/standards/crochet-gauge)
- [Bresenham's Line Algorithm](https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [pytest Documentation](https://docs.pytest.org/)

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-01-05 | Documentation Team | Initial Phase 1 plan created |

---

**Document Status:** FINAL
**Next Review:** After Phase 1 completion (End of Week 4)
**Owner:** Backend Lead

---

**END OF PHASE 1 PLAN**
