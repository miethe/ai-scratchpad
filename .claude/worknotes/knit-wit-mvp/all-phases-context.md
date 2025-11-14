# Knit-Wit MVP - All Phases Context

**Purpose**: Running log of context, decisions, blockers, and insights during Phase 4 execution
**Audience**: AI agents across turns
**Format**: Append new entries at end; keep concise

---

## Current Phase Status

**Phase**: 4 (QA, Polish & Optimization)
**Sprint**: Sprint 8 (starting)
**Week**: 12-13 of 16
**Last Updated**: 2025-11-14

**Active Focus**:
- Cross-device testing (iOS, Android, tablets, web)
- WCAG AA accessibility audit
- Performance baseline profiling
- Bug triage from Phase 3 completion

**Phase Entry Conditions Met**:
- ✓ Phase 3 complete (all MVP features implemented)
- ✓ Pattern generation, visualization, export functional
- ✓ Kid Mode, accessibility features, telemetry operational
- ✓ Settings persistence working

---

## Architecture Context

### Tech Stack (Phases 0-3)

**Backend**:
- FastAPI 0.104+ on Python 3.11+
- Pattern engine: Standalone Python package (`knit_wit_engine`)
- DSL: Pydantic v2 models (JSON serializable)
- Export: ReportLab (PDF), Pillow (PNG)
- Testing: pytest, 93% coverage on pattern engine

**Frontend**:
- React Native 0.73+ with Expo SDK 51+
- State: Zustand (global), AsyncStorage (persistence)
- Navigation: React Navigation 6+
- Rendering: react-native-svg (diagrams)
- Testing: Jest + React Native Testing Library

**Infrastructure**:
- Monorepo: pnpm workspaces
- CI/CD: GitHub Actions
- Dev env: Docker Compose

### Key Design Decisions (Phases 0-3)

**Pattern Engine Architecture**:
- Decision: Standalone Python library, no FastAPI dependencies
- Rationale: Testability, reusability, performance isolation
- Impact: Can profile and optimize engine separately from API layer

**Visualization Approach**:
- Decision: DSL → RenderPrimitive → SVG (2-stage conversion)
- Rationale: Separation of pattern logic from rendering logic
- Impact: Backend computes node positions, frontend just renders

**Accessibility Strategy**:
- Decision: WCAG AA baseline from start (Phase 0), not retrofitted
- Rationale: Cheaper to build accessible than fix later
- Impact: ARIA labels on all components, color contrast verified early

**Kid Mode Implementation**:
- Decision: Separate theme system, not feature flags
- Rationale: Cleaner separation, easier to test/maintain
- Impact: Kid Mode is a complete UI variant, not patches

---

## Key Decisions Made

### Phase 4 Planning (Pre-Sprint 8)

**2025-11-14**: Phase 4 delegation strategy defined
- QA tasks → task-completion-validator, debugger
- Accessibility → ui-engineer, frontend-developer
- Performance → python-pro (backend), frontend-developer (frontend)
- Bug fixes → debugger + appropriate specialist
- Documentation → documentation-writer
- Monitoring → backend-architect, python-pro

**Rationale**: Leverage specialized agents for domain expertise

---

## Blockers & Resolutions

*No blockers yet (Phase 4 starting)*

### Template for Future Blockers

**[DATE] - Blocker: [Brief Description]**
- **Impact**: [What's blocked]
- **Root Cause**: [Why blocked]
- **Resolution**: [How unblocked]
- **Owner**: [Who resolved]

---

## Testing Observations

### Phase 1-3 Test Coverage

**Pattern Engine (Phase 1)**:
- Unit test coverage: 93%
- Performance: < 200ms generation (all shapes)
- Edge cases: Small/large dimensions, unusual gauges handled

**Visualization (Phase 2)**:
- Component tests: 60%+ coverage
- Manual FPS testing: 60 FPS on iPhone 11+, Pixel 4+
- Integration: Backend → Frontend API calls functional

**Export (Phase 3)**:
- PDF generation: < 5s for typical patterns
- SVG/PNG export: Functional but not performance-optimized
- JSON DSL: Round-trip compatible

**Accessibility (Phase 3)**:
- ARIA labels: Present on all interactive elements
- Screen reader: Basic announcements working
- Color contrast: Not yet verified against WCAG AA
- Keyboard nav: Partially implemented

### Known Test Gaps (To Address in Phase 4)

- Cross-device testing: Limited to simulators/emulators
- Accessibility: No formal WCAG AA audit yet
- Performance: No profiling on low-spec devices (iPhone SE, Samsung A10)
- E2E: No automated E2E tests (manual testing only)
- Regression: No regression suite (risk of breaking Phase 1-3 features)

---

## Performance Findings

### Backend Performance (Phase 1)

**Pattern Generation Times** (pytest-benchmark):
- Sphere (10cm, 14/16 gauge): ~80ms (target: < 200ms) ✓
- Cylinder (8×12cm): ~95ms ✓
- Cone (6→2cm, 8cm height): ~110ms ✓

**Optimization Opportunities** (Not yet addressed):
- Compiler instance caching: Not implemented (each request creates new compiler)
- Gauge calculation memoization: Not implemented
- DSL construction overhead: Pydantic validation on hot path

### Frontend Performance (Phase 2-3)

**SVG Rendering** (React DevTools Profiler):
- Mount time: ~150ms (target: < 200ms) ✓
- Update time: ~50ms per round change ✓
- Frame rate: 60 FPS on iPhone 12 (verified)

**Optimization Opportunities** (Not yet addressed):
- SVG virtualization: Rendering all nodes, not just visible
- Component memoization: Some expensive components not React.memo'd
- Bundle size: Not yet optimized (APK/IPA size unknown)

---

## Architectural Insights

### Pattern DSL Stability

**Version**: v0.1 (from Phase 1)
**Format**: JSON with Pydantic validation
**Status**: Stable, no breaking changes needed for MVP

**Key Insight**: DSL design from Phase 0 held up well through Phase 3. No major schema changes needed.

**Future Considerations** (Post-MVP):
- Add `joined_rounds` support (v1.1)
- Add HDC/DC stitch types (v1.1)
- Add colorwork/stripes (v1.1)

### Zustand State Management

**Implementation**: Phase 2
**Stores**: `visualizationStore`, `settingsStore`, `exportStore`
**Status**: Working well, no performance issues

**Key Insight**: Zustand's simplicity paid off. No need for Redux complexity for MVP scope.

---

## Integration Points

### Backend ↔ Frontend API

**Endpoints Implemented** (Phase 2-3):
- `POST /api/v1/patterns/generate` - Pattern generation
- `POST /api/v1/visualization/frames` - DSL → visualization frames
- `POST /api/v1/export/pdf` - PDF export
- `POST /api/v1/export/svg` - SVG export
- `POST /api/v1/export/json` - JSON DSL export
- `POST /api/v1/parser/parse` - Text → DSL parsing

**API Stability**: No breaking changes during Phase 2-3. Contract from Phase 0 held.

### Frontend ↔ AsyncStorage

**Implemented** (Phase 3):
- Settings persistence (terminology, units, Kid Mode, theme)
- Telemetry consent

**Works**: Settings survive app restarts, no data loss observed

---

## Accessibility Architecture

### Current Implementation (Phase 3)

**ARIA Labels**: Present on all buttons, inputs, navigation
**Screen Reader**: Basic announcements (round changes, stitch types)
**Color Contrast**: Not formally verified (Phase 4 task)
**Keyboard Nav**: Partial (tab order, focus indicators)
**Colorblind Support**: Palette with patterns, not color-only

### Known Gaps (Phase 4 Focus)

- No axe-core audit run yet
- Manual keyboard navigation not fully tested
- Color contrast ratios not measured (WCAG AA requires 4.5:1, 3:1)
- Screen reader testing limited to iOS VoiceOver (no NVDA/JAWS testing)

---

## Risk Register

### Phase 4 Risks

**R1: Critical bugs discovered late**
- **Probability**: Medium
- **Impact**: High (launch delay)
- **Mitigation**: Early cross-device testing (Sprint 8), daily bug triage

**R2: Performance targets not met**
- **Probability**: Medium
- **Impact**: High (poor UX)
- **Mitigation**: Profiling in Sprint 8, optimization buffer in Sprint 9

**R3: WCAG AA compliance fails**
- **Probability**: Low
- **Impact**: High (legal/ethical)
- **Mitigation**: Automated audits early (Sprint 8), manual testing by specialists

**R4: E2E automation blocked**
- **Probability**: Low
- **Impact**: Medium (manual testing burden)
- **Mitigation**: Start Detox setup early, fallback to manual critical path

---

## Notes for Future Phases

### For Phase 5 (Launch Preparation)

**Pre-requisites from Phase 4**:
- All P0 bugs fixed
- WCAG AA audit passed (0 critical issues)
- Performance targets met (< 200ms, 60 FPS)
- Documentation complete

**Deployment Considerations**:
- Backend: Railway/Render (TBD)
- Frontend: Netlify/Vercel or EAS (TBD)
- Monitoring: Grafana/Datadog (TBD)
- Error tracking: Sentry (configured in Sprint 9)

### Post-MVP (v1.1+)

**Deferred Features** (explicitly scoped out of MVP):
- HDC/DC stitches
- Joined rounds (vs. spiral only)
- Colorwork and stripes
- User accounts and pattern persistence
- Community features

**Technical Debt to Address**:
- Backend compiler instance caching
- Frontend SVG virtualization
- Bundle size optimization
- Database for pattern storage (currently stateless)
- Redis caching for distributed deployments

---

## Appendix: Quick Reference

### Phase 4 Sprint Goals

**Sprint 8 (Weeks 12-13)**: Cross-device testing, accessibility audit, performance profiling
**Sprint 9 (Weeks 13-14)**: Optimization, bug fixes, accessibility remediation
**Sprint 10 (Weeks 14-15)**: E2E automation, documentation, final polish

### Phase 4 Exit Criteria Checklist

- [ ] Cross-device testing complete
- [ ] WCAG AA: 0 critical issues
- [ ] Performance: < 200ms, 60 FPS
- [ ] 0 critical bugs (P0)
- [ ] E2E tests automated
- [ ] Documentation complete

### Key Contacts (Placeholder)

- Backend Lead: [TBD]
- Frontend Lead: [TBD]
- QA Lead: [TBD]
- Product Lead: [TBD]

---

## Template for New Entries

**[DATE] - [Topic]: [Brief Note]**
- **Context**: [Background]
- **Decision/Finding**: [What happened]
- **Impact**: [Implications]
- **Next Steps**: [Actions]

---

*End of current context. Append new entries below as Phase 4 progresses.*
