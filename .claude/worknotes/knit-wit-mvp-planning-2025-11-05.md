# Knit-Wit MVP Planning Session — Worknotes
**Date:** November 5, 2025
**Session Type:** Initial MVP Planning & Artifact Creation
**Status:** Complete

---

## Session Overview

Initial MVP planning and specification session for Knit-Wit, a mobile-first crochet pattern generator and visualizer. Focus was on:
1. Problem/solution definition
2. Feature scope and architecture design
3. Creating comprehensive PRD and implementation plan
4. Establishing technical foundation for Phase 0

**Artifacts Created:** 3 major documents + directory structure
**Duration:** Single planning session (November 5, 2025)

---

## Artifacts Created

### 1. PRD Document (`/knit-wit/project_plans/mvp/prd.md`)
**Purpose:** Comprehensive product requirements specification for MVP

**Sections:**
- Problem statement: "Writing/reading crochet patterns is tedious"
- Solution: Pattern generation (sphere/cylinder/cone) + interactive visualization
- User personas: Beginner Becky, Intermediate Ivy, Expert Eli, Parent/Teacher Pat
- 18 detailed requirement sections covering functions, UX, algorithms, acceptance criteria
- Open questions captured for future decision-making

**Key Deliverables Defined:**
- Geometric shape generation (sphere, ellipsoid, cylinder, cone)
- Per-round visualization with step-by-step guides
- PDF/SVG exports with branded covers
- Kid Mode with simplified UX
- US/UK terminology toggle

### 2. Implementation Plan (`/knit-wit/project_plans/mvp/implementation-plan.md`)
**Purpose:** Tactical execution guide for development team

**Contains:**
- 16-week timeline across 6 major phases
- 2-week sprint structure with milestone targets
- Team structure recommendations (4-6 person squad)
- Epic breakdown (EPIC A-D covering engine, visualization, parsing, app shell)
- Definition of Ready/Done criteria
- Testing strategy and DevOps approach

**Phase Structure:**
- Phase 0: Prep & Architecture (1 week)
- Phase 1: Setup & Infrastructure (2 weeks)
- Phase 2: Pattern Engine Core (2 weeks)
- Phase 3: Visualization Alpha (3 weeks)
- Phase 4: Full Features (4 weeks)
- Phase 5: QA & Polish (2 weeks)
- Phase 6: Launch Readiness (1 week)

### 3. Initial PRD (`/knit-wit/project_plans/initialization/initial-prd.md`)
**Purpose:** Original concept document capturing initial problem/solution

---

## Key Learnings & Decisions

### Architecture Decisions

**Frontend Stack: React Native (Expo)**
- Rationale: Mobile-first requirement, code reuse across iOS/Android
- Alternative considered: React Native Web (rejected for better native UX)
- Rendering: react-native-svg or Skia for pattern diagrams

**Backend Stack: Python + FastAPI**
- Rationale: Fits project norms, excellent async support, rapid API development
- Core library: Separate "pattern-compiler" Python module
- Stateless design in MVP (assets streamed, optional ephemeral storage later)

**Pattern DSL v0.1: JSON-based**
- Operations vocabulary: MR (magic ring), sc, hdc (future), inc, dec, slst, ch, seq, repeat
- Metadata: units, terms (US/UK), gauge, stitch type, round mode
- Round objects: r (index), ops (ordered operations), stitches (post-round count)
- Handedness: Frontend rendering flag; DSL remains neutral

### Algorithm Choices

**Increase Distribution (Bresenham-style)**
- Problem: Avoid stacked columns of increases/decreases
- Solution: Modular spacing with jitter based on round index
- Formula: For ΔS increases on S stitches, place roughly every ⌊S/ΔS⌋ stitches

**Sphere Generation**
- Rounds to equator: k_eq ≈ round(g_r × (D/2) / 10)
- Increase by computed initial stitch count (typically 6) per round until equator
- Optional steady rounds
- Mirror decreases on second half
- Gauge directly impacts stitch distribution

**Cone/Tapered Limb**
- Linear taper from S_0 to S_1 across K rounds
- Distribute ±1 deltas using Bresenham-like spacing
- Prevents stacking of changes per round

**Gauge Mapping**
- g_s = stitches per 10 cm
- g_r = rows per 10 cm
- Flat disc initial stitch count: I ≈ round(2π × g_s / g_r) — typically 6

### Technical Rationale

**Why Pattern-Compiler as Separate Library:**
- Decouples generation logic from API
- Enables future desktop/CLI tool usage
- Easier testing and reuse across platforms
- Follows Unix philosophy (do one thing well)

**Why Stateless Backend:**
- Simplifies deployment and scaling
- Assets generated on demand
- Privacy-respecting (no server-side pattern storage in MVP)

**Why Limited Text Parser MVP:**
- Full crochet pattern syntax is complex (hundreds of regional variants)
- MVP supports canonical bracket/repeat syntax only
- Clear error reporting + manual edit mode for unsupported patterns
- Future v1.1 can expand grammar

---

## Risks Identified

### R1: Gauge Variance → Shape Drift
**Impact:** User expectation mismatch (finished object too large/small)
**Mitigation:** Force gauge confirmation flow, show ±size tolerance, hook adjustment guidance

### R2: External Pattern Text Variance
**Impact:** Parser fails on common patterns not in MVP grammar
**Mitigation:** Minimal grammar + friendly errors + manual edit mode

### R3: Visual Comprehension for Beginners
**Impact:** Even with diagrams, true beginners struggle to understand stitches
**Mitigation:** Micro-animations ("What is an increase?"), glossary links, Kid Mode hints

### R4: Performance on Mid-Range Mobile Devices
**Mitigation:** SVG rendering optimization, lazy loading of large patterns, progressive enhancement

---

## Open Questions / Decisions Needed

### For V1.1 Scope Decision
1. **HDC/DC stitches in MVP or deferred?**
   - Current: MVP supports sc only, hdc/dc planned for v1.1
   - Question: Does user feedback suggest earlier inclusion?

2. **Joined rounds timing**
   - Current: Spiral rounds only in MVP
   - Decision: Include joined round support in Phase 4 or defer to v1.1?

3. **Gauge preset library**
   - Option A: Bake in 20-30 common yarn weight presets (Worsted, DK, etc.)
   - Option B: Manual gauge entry only, build preset system later
   - Impact: UX complexity vs. user convenience

### Technical Clarifications
4. **PDF export branding**
   - How much customization in MVP? (Cover design, colors, footer)
   - Static template or dynamic generation?

5. **Visualization frame count limits**
   - Definition of done says "reliably render 50+ rounds"
   - Any anticipated patterns exceeding 100 rounds? (Rare but possible)

---

## Next Steps (Immediate Actions)

### Phase 0: Setup & Preparation (Week 1)
1. Create Git monorepo structure with appropriate directory layout
2. Set up CI/CD pipeline (GitHub Actions or equivalent)
3. Create Python project scaffold for pattern-compiler library
4. Create React Native/Expo project scaffold
5. Create FastAPI backend scaffold
6. Initialize shared documentation structure (docs/, CONTRIBUTING.md)

### First Sprint Planning
1. Review PRD with full team and capture clarifying questions
2. Define Definition of Ready for stories
3. Create GitHub issues for Phase 1 epics
4. Set up project tracking (Kanban board or similar)
5. Assign Phase 1 technical leads (1 backend, 1 frontend)

### Repository Scaffolding
1. Monorepo structure: `/backend`, `/frontend`, `/pattern-compiler`
2. Shared types/schemas: Consider OpenAPI/TypeScript generation from Pydantic models
3. Development documentation: Setup guides for each component
4. Local development environment: Docker Compose or similar for PostgreSQL, Redis (future)

---

## Technical Foundation Summary

### Core Technologies (Locked)
- **Frontend:** React Native + Expo, react-native-svg
- **Backend:** FastAPI, Python 3.10+
- **Pattern Engine:** Python module (pattern-compiler)
- **Data Format:** JSON DSL v0.1
- **Exports:** PDF (via reportlab or similar), SVG, JSON

### Architecture Layers (MVP)
1. **Router Layer** (`/routers`): HTTP validation, request parsing
2. **Service Layer** (`/services`): Business logic, orchestration
3. **Engine Layer** (`pattern-compiler`): Pure pattern generation
4. **Models** (`/models`): SQLAlchemy ORM (minimal in MVP)
5. **Frontend Components**: Screens, forms, visualization renderer

### MVP Scope Boundaries
- **Included:** Sphere, cylinder (with caps), cone/tapered shapes, single-color patterns
- **Deferred v1.1:** HDC/DC stitches, joined rounds, stripes, multi-part assemblies
- **Out of scope:** Community, marketplace, AI-assisted design, photo-to-pattern

---

## Definition of Done (MVP)

### Code Completeness
- [ ] Sphere, cylinder, cone compilers implemented and unit tested
- [ ] 50+ round visualization passes performance (< 50ms per round)
- [ ] Text parser handles canonical bracket syntax with 95%+ accuracy
- [ ] PDF export passes A4/Letter print test and mobile rendering test
- [ ] All accessibility checks (WCAG AA, voice-over, contrast)

### Quality Gates
- [ ] Unit test coverage > 80% (pattern-compiler)
- [ ] Integration tests for all API endpoints
- [ ] Smoke tests on iOS and Android (current-generation devices)
- [ ] No console errors in production build
- [ ] Performance audit: all pages < 3s load on 4G

### Documentation
- [ ] API documentation (OpenAPI/Swagger)
- [ ] Pattern DSL specification with examples
- [ ] User-facing help/glossary
- [ ] Developer onboarding guide

---

## Team & Roles

### Recommended Structure
- **Backend Lead:** Pattern engine architecture, algorithm validation
- **Backend Engineer:** API implementation, export functionality
- **Frontend Lead:** RN/Expo setup, navigation, accessibility
- **Frontend Engineer:** Visualization, UI polish, Kid Mode
- **QA Lead:** Test strategy, accessibility audits
- **DevOps (shared):** CI/CD, deployment

### Meeting Cadence
- Daily standup: 15 min
- Sprint planning: 2 hrs (every 2 weeks)
- Sprint review/demo: 1.5 hrs (every 2 weeks)
- Retrospective: 1 hr (every 2 weeks)
- Architecture sync: 1 hr (weekly as needed)

---

## Document References

All planning artifacts stored at:
- **PRD:** `/knit-wit/project_plans/mvp/prd.md`
- **Implementation Plan:** `/knit-wit/project_plans/mvp/implementation-plan.md`
- **Initial Concept:** `/knit-wit/project_plans/initialization/initial-prd.md`

Future session notes should reference this worknote and update sections as decisions are made.

---

**Session Complete:** November 5, 2025
