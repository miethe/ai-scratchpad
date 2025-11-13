# Phase 3 Context: Full Feature Implementation

**Last Updated**: 2025-11-13
**Status**: Not Started
**Branch**: `claude/phase-3-implementation-011CV4ZM3qsWS5J9Ct8zTvt8`

---

## Current State

**Active Task**: Phase initialization
**Current Sprint**: Sprint 5 (Weeks 8-9) - not yet started
**Next Story**: C1 (Text parser backend) or D7 (Settings persistence)

**Recent Commit**:
- `e3bcaad` - Merge Phase 2 completion (visualization features complete)
- Phase 2 delivered: RN/Expo app shell, SVG rendering, round scrubber, tooltips, legend, accessibility labels

**Environment**:
- Python 3.11+, FastAPI backend
- React Native/Expo frontend
- Pattern engine: knit-wit-engine (DSL v0.1)

---

## Phase Scope Summary

Phase 3 delivers end-to-end user flows: pattern generation → visualization → professional exports.

**Core Features**:
1. **Parsing**: Text patterns → PatternDSL (bracket/repeat grammar)
2. **Export**: PDF (professional layout), SVG (editable), PNG (raster), JSON (DSL)
3. **Kid Mode**: Simplified UI, 56×56 dp tap targets, beginner copy (Grade 4-5)
4. **Accessibility**: WCAG AA compliance, screen readers, colorblind palettes, dyslexia font
5. **Telemetry**: Opt-in analytics, privacy-respecting event pipeline

**Epics**: C (Parsing & I/O), D (Settings completion), E (Kid Mode & Accessibility), F (Telemetry)
**Total Effort**: ~141 story points across 3 sprints

---

## Key Implementation Patterns

### Backend Architecture

**Parser Service** (`app/services/parser_service.py`):
- Input: Text with bracket/repeat syntax (e.g., `R3: [2 sc, inc] x6 (18)`)
- Algorithm: Regex-based tokenization → PatternDSL construction
- Output: Validated PatternDSL JSON
- Error handling: User-friendly messages for unsupported syntax

**Export Service** (`app/services/export_service.py`):
- PDF: ReportLab/WeasyPrint (cover, materials, pattern, diagrams)
- SVG: Export visualization frames (per-round or composite)
- PNG: Pillow rasterization (72 DPI screen, 300 DPI print)
- JSON: PatternDSL serialization (round-trip compatible)

**Telemetry Service** (`app/services/telemetry_service.py`):
- Anonymous event logging (no PII)
- Events: generation, visualization, export
- Backend pipeline with 90-day retention

**API Endpoints**:
- `POST /api/v1/parser/parse` - Text → DSL
- `POST /api/v1/export/pdf` - DSL → PDF
- `POST /api/v1/export/svg` - DSL → SVG (per-round or composite)
- `POST /api/v1/export/json` - DSL → JSON

### Frontend Architecture

**Settings Persistence** (`src/services/settingsStorage.ts`):
- AsyncStorage for preferences (terminology, units, theme, Kid Mode, telemetry)
- Settings applied consistently across app

**Kid Mode Theme** (`src/theme/kidModeTheme.ts`):
- Bright, safe colors (pink, yellow, cream)
- Larger typography (16-32px, increased from 12-20px)
- Friendly font (Comic Sans or similar)
- 56×56 dp minimum tap targets (up from 44×44)

**Accessibility Theme** (`src/theme/accessibilityTheme.ts`):
- High contrast mode (4.5:1 text, 3:1 UI)
- Colorblind palettes (patterns + symbols, not just color)
- Dyslexia font option (OpenDyslexic)
- prefers-reduced-motion support

**Export Screen** (`src/screens/ExportScreen.tsx`):
- Format selection: PDF, SVG, PNG, JSON
- Download via react-native-fs
- Preview thumbnails for visual formats

**Parse Screen** (`src/screens/ParseScreen.tsx`):
- Text input with syntax highlighting
- Real-time validation feedback
- Error messages with suggested fixes

**Accessibility Components** (`src/components/accessibility/`):
- ARIA labels on all interactive elements
- Screen reader announcements (round changes, stitch types)
- Keyboard navigation (external keyboard support)
- Focus indicators visible

**Telemetry Client** (`src/services/telemetryClient.ts`):
- Frontend SDK for event tracking
- Respects opt-out preference
- Consent prompt on first run

---

## Critical Decisions

### Parsing Strategy
- **Approach**: Limited grammar (bracket/repeat only) for MVP
- **Unsupported**: Nested brackets, complex colorwork, stitch modifiers
- **Error Handling**: Friendly messages, suggest DSL generation instead
- **Validation**: Stitch count consistency checks

### Export Formats
- **PDF**: ReportLab for programmatic generation (vs. WeasyPrint HTML → PDF)
- **Size Target**: <5MB for typical patterns (10-50 rounds)
- **Performance**: <5s generation time (pytest-benchmark verification)
- **SVG**: Editable in Illustrator/Inkscape (clean paths, no rasterization)

### Accessibility Prioritization
- **WCAG AA**: 100% compliance on critical paths (generation, visualization, export)
- **Screen Readers**: NVDA, JAWS (desktop), VoiceOver (mobile)
- **Testing**: axe-core automated + manual audits
- **Colorblind**: Patterns/symbols in legend, not just color reliance

### Telemetry Privacy
- **Opt-In Required**: Consent prompt on first run (GDPR compliance)
- **No PII**: Anonymous events only (no user IDs, IP addresses, patterns)
- **Retention**: 90-day window, auto-purge older data
- **Transparency**: Clear privacy policy in settings

---

## Technical Gotchas

### Backend

**Parser Pitfalls**:
- Regex complexity: Test edge cases (no spaces, nested parens, typos)
- Stitch count validation: Ensure computed stitches match declared totals
- Unsupported syntax: Clear error messages, not generic "parse failed"

**Export Challenges**:
- PDF fonts: Embed fonts to avoid missing glyphs
- SVG size: Large patterns (100+ rounds) may generate huge files
- PNG resolution: Balance file size vs. print quality (300 DPI default)

**Telemetry Concerns**:
- PII leakage: Never log pattern content, user notes, or dimensions
- Consent enforcement: Check opt-in flag before every event
- Debugging: Log events locally in dev mode for verification

### Frontend

**Kid Mode**:
- Typography scaling: Ensure text doesn't overflow buttons/containers
- Copy tone: Grade 4-5 reading level (Flesch-Kincaid 80+)
- Animations: Respect prefers-reduced-motion (disable if set)

**Accessibility**:
- Focus traps: Ensure keyboard nav doesn't get stuck in modals
- Screen reader verbosity: Balance detail vs. overwhelming users
- Color contrast: Test in real-world lighting (not just DevTools)
- Touch targets: Use hitSlop for small visual elements

**Settings Persistence**:
- AsyncStorage limits: ~6MB total, avoid storing large data
- Sync timing: Load settings before rendering UI to avoid flicker
- Defaults: Graceful fallback if settings fail to load

---

## Testing Strategy

### Backend Tests

**Parser Tests** (`tests/unit/test_parser_service.py`):
- Canonical patterns: `R3: [2 sc, inc] x6 (18)` → correct DSL
- Edge cases: No spaces, mixed case, typos
- Error handling: Invalid syntax returns user-friendly errors
- Stitch count validation: Computed vs. declared consistency

**Export Tests** (`tests/unit/test_export_service.py`):
- PDF generation: Valid PDF structure, <5MB, <5s
- SVG export: Valid XML, editable in Inkscape
- PNG export: Correct dimensions, 300 DPI
- JSON export: Round-trip DSL serialization

**Integration Tests** (`tests/integration/test_export_api.py`):
- E2E: Generate pattern → export PDF → verify file
- Error cases: Invalid DSL → 400 error with details

### Frontend Tests

**Component Tests** (`__tests__/screens/ExportScreen.test.tsx`):
- Format selection: Buttons render, state updates
- Download: Mock API, verify file saved
- Error handling: Failed export shows error message

**Accessibility Tests** (`__tests__/accessibility/a11y.test.tsx`):
- axe-core audit: 0 critical issues
- ARIA labels: All interactive elements labeled
- Keyboard nav: Tab order correct, no focus traps
- Screen reader: Announcements match UI state

**Coverage Targets**:
- Backend: 80%+ (pytest-cov)
- Frontend: 60%+ (Jest coverage)

---

## Sprint 5 Focus (Weeks 8-9)

**Goal**: Parser functional + PDF export + Settings persistence

**Key Stories**:
- C1: Text parser backend (13 pt) - BE Lead
- C3: PDF export endpoint (13 pt) - BE Eng
- D7: Settings persistence (8 pt) - FE Lead
- D8: Terminology/units toggles (5 pt) - FE Eng
- D9: Theme system refactor (5 pt) - FE Eng

**Demo Deliverables**:
- Parse `R3: [2 sc, inc] x6` → PatternDSL JSON
- Generate sphere → PDF with diagrams
- Export screen with format selection
- Settings persist across app restart

---

## Quick Reference

### Environment Setup

**Backend**:
```bash
cd apps/api
uvicorn app.main:app --reload
```

**Frontend**:
```bash
cd apps/mobile
pnpm dev
```

**Tests**:
```bash
# Backend
pytest apps/api/tests/

# Frontend
pnpm --filter mobile test
```

### Key Files (Phase 3 Scope)

**Backend**:
- `apps/api/app/services/parser_service.py` - Parser logic
- `apps/api/app/services/export_service.py` - Export generators
- `apps/api/app/api/routes/parser.py` - Parser endpoint
- `apps/api/app/api/routes/export.py` - Export endpoints
- `apps/api/app/services/telemetry_service.py` - Event pipeline

**Frontend**:
- `apps/mobile/src/screens/ExportScreen.tsx` - Export UI
- `apps/mobile/src/screens/ParseScreen.tsx` - Parse UI
- `apps/mobile/src/screens/SettingsScreen.tsx` - Settings
- `apps/mobile/src/theme/kidModeTheme.ts` - Kid Mode theme
- `apps/mobile/src/theme/accessibilityTheme.ts` - A11y theme
- `apps/mobile/src/services/telemetryClient.ts` - Events SDK

### Pattern DSL Structure

```json
{
  "meta": {"version": "0.1", "terms": "US", "stitch": "sc"},
  "object": {"type": "sphere", "params": {"diameter": 10}},
  "rounds": [
    {"r": 1, "ops": [{"op": "MR", "count": 1}], "stitches": 6}
  ],
  "materials": {"hook_size_mm": 4.0, "yardage_estimate": 25}
}
```

### Parser Example

**Input**: `R3: [2 sc, inc] x6 (18)`

**Output**:
```json
{
  "r": 3,
  "ops": [
    {"op": "seq", "ops": [
      {"op": "sc", "count": 2},
      {"op": "inc", "count": 1}
    ], "repeat": 6, "count": 18}
  ],
  "stitches": 18
}
```

---

## Phase Dependencies

**Blocked By**:
- Phase 2 completion: Visualization frames, SVG rendering, round scrubber (COMPLETE)

**Blocks**:
- Phase 4: QA & Polish (Weeks 12-15) - needs export, accessibility, settings complete

**Integration Points**:
- D7-D9 (settings) → E1 (Kid Mode toggle)
- D9 (theme system) → E1, E4-E7 (accessibility themes)
- C3-C5 (export endpoints) → C6 (export screen)
- F1 (backend events) → F2 (frontend client)

---

## Notes for AI Agents

**Token Optimization**:
- Load this context file first (~1800 tokens)
- Reference Phase 3 plan (`docs/project_plans/mvp/phases/phase-3.md`) for full story details
- Check progress tracker (`../progress/phase-3-progress.md`) for completion status

**Common Queries**:
- "What's the current sprint?" → Sprint 5 (not started)
- "What's the parser syntax?" → Bracket/repeat: `[ops] xN`
- "What's the accessibility target?" → WCAG AA: 100% critical paths
- "What's the Kid Mode tap target?" → 56×56 dp minimum

**Phase Completion**:
Phase 3 ends when all success criteria met (parser, exports, Kid Mode, WCAG AA, telemetry opt-in functional) and Sprint 7 demo delivered.
