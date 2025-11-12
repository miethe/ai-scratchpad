# Phase 2 Working Context

**Purpose:** Token-efficient context for resuming work across AI turns

---

## Current State

**Branch:** claude/knit-wit-phase-2-execution-011CV4LWr8SZAdY5kgB9D5NV
**Last Commit:** d5cf59e - fix formatting
**Current Task:** Sprint 3 kickoff - D1 (navigation) and B1 (DSL → frames) in parallel
**Progress:** 0/98 story points completed (0%)

---

## Key Decisions

### Architecture

**Visualization Layout:**
- Polar coordinate system: `angle = (2π / stitch_count) * idx`
- Position calculation: `x = radius * cos(angle)`, `y = radius * sin(angle)`
- Circular layout represents crochet worked in the round

**React Navigation:**
- Stack (Root) + Tabs (Main) + Modal (Visualization)
- Structure: RootNavigator → MainTabs → [Home, Generate, Settings] + VisualizationModal
- React Navigation 6+ with TypeScript

**State Management:**
- Zustand (3 store slices): visualizationStore, settingsStore, patternStore
- No Provider boilerplate, TypeScript-friendly
- Store methods: setFrames, setCurrentRound, nextRound, prevRound, jumpToRound

**SVG Rendering:**
- react-native-svg version 14.x (stable with Expo SDK 51+)
- Rendering order: edges first (behind), then nodes (on top)
- React.memo for performance optimization

### API Contract

**VisualizationResponse:**
```typescript
interface RenderNode {
  id: string;                          // "r3s12"
  stitch_type: string;                 // "sc", "inc", "dec"
  position: [number, number];          // [x, y] coordinates
  highlight: "normal" | "increase" | "decrease";
}

interface RenderEdge {
  source: string;                      // Node ID
  target: string;                      // Node ID
}

interface VisualizationFrame {
  round_number: number;
  nodes: RenderNode[];
  edges: RenderEdge[];
  stitch_count: number;
  highlights: string[];                // Node IDs with highlighting
}

interface VisualizationResponse {
  frames: VisualizationFrame[];
  total_rounds: number;
  shape_type: string;
}
```

**Endpoint:** `POST /api/v1/visualization/frames`
**Performance Target:** < 100ms compilation

### UI Patterns

**Stitch Highlighting (Colorblind-Friendly):**
- Green (#10B981): Increases
- Red (#EF4444): Decreases
- Gray (#6B7280): Normal stitches

**Touch Targets:**
- Minimum: 48×48 dp (exceeds 44×44 WCAG AAA)
- Applies to: Previous/Next buttons, stitch nodes, scrubber thumb

**Accessibility:**
- WCAG AA baseline: 4.5:1 text contrast, 3:1 UI contrast
- axe-core automated testing + VoiceOver/TalkBack manual testing
- Target: 0 critical issues

### Performance Constraints

**MVP Limits:**
- < 50 rounds per pattern
- < 100 stitches per round
- Defers optimization to Phase 3

**Targets:**
- Frame compilation: < 100ms (backend)
- SVG rendering: 60 FPS (frontend, iPhone 11+/Pixel 4+)
- E2E pattern load: < 500ms

---

## Important Learnings

**React Native SVG:**
- Use stable version 14.x with Expo SDK 51+
- G (group) component for transforms: `<G transform="translate(...) scale(...)">`
- Render order matters: edges before nodes for proper layering

**Performance:**
- React.memo prevents unnecessary SVG re-renders during round navigation
- Frame-by-frame data structure enables lazy rendering and caching
- Scale calculation: `scale = Math.min(width, height) / 250` (fits viewport)

**Accessibility:**
- axe-core catches automated issues (contrast, labels, roles)
- Manual testing required for screen reader announcements (round changes, stitch selection)
- accessibilityLabel + accessibilityRole on all interactive components

**API Design:**
- Frame array enables scrubber navigation without re-computation
- Node IDs follow pattern: `r{round}s{stitch}` (e.g., "r3s12")
- Edge closing: last node → first node completes circular connection

---

## Quick Reference

### Environment Setup

```bash
# Working directory
cd /home/user/ai-scratchpad/knit-wit

# Frontend dev (when mobile app created)
pnpm --filter mobile dev

# Backend dev (existing)
cd apps/api && uv run fastapi dev app/main.py

# Backend tests
cd apps/api && uv run pytest

# Frontend tests (when mobile app created)
pnpm --filter mobile test

# Type checking
pnpm --filter mobile typecheck
```

### Key Files (Planned)

**Backend (To Be Created):**
- `apps/api/app/services/visualization_service.py` - DSL → frames converter
- `apps/api/app/models/visualization.py` - RenderNode, RenderEdge, VisualizationFrame models
- `apps/api/app/api/routes/visualization.py` - POST /visualization/frames endpoint
- `tests/unit/test_visualization_service.py` - Unit tests
- `tests/integration/test_visualization_api.py` - API contract tests

**Frontend (To Be Created):**
- `apps/mobile/` - New Expo app (React Native)
- `apps/mobile/src/navigation/RootNavigator.tsx` - Navigation stack
- `apps/mobile/src/context/visualizationStore.ts` - Zustand stores
- `apps/mobile/src/components/visualization/SVGRenderer.tsx` - SVG rendering engine
- `apps/mobile/src/components/visualization/RoundScrubber.tsx` - Navigation controls
- `apps/mobile/src/components/visualization/StitchTooltip.tsx` - Tooltip modal
- `apps/mobile/src/components/visualization/Legend.tsx` - Color key overlay
- `apps/mobile/src/screens/VisualizationScreen.tsx` - Main visualization UI
- `apps/mobile/src/screens/SettingsScreen.tsx` - Settings UI
- `apps/mobile/src/services/apiClient.ts` - HTTP client with error handling
- `apps/mobile/__tests__/components/SVGRenderer.test.tsx` - Component tests

**Existing (Phase 1):**
- `packages/knit-wit-engine/src/dsl.py` - PatternDSL schema
- `packages/knit-wit-engine/src/compilers/` - Sphere, cylinder, cone compilers

---

## Phase Scope Summary

Phase 2 establishes visualization foundation for interactive pattern rendering. Backend converts PatternDSL to frame-by-frame render primitives (RenderNode + RenderEdge); frontend renders as interactive SVG with step-by-step controls.

**Success Metric:** SVG renders at 60 FPS on mid-range devices (iPhone 11+, Pixel 4+)

**Critical Path:** B1 → B2 → B3 → (B4, B5, B6, B7, B8)

**Key Integration Point:** Backend /visualization/frames endpoint → Frontend apiClient → Zustand store → SVGRenderer component

---

## Agent Delegation Matrix

| Story | Agent(s) | Sprint | Priority | Dependencies |
|-------|----------|--------|----------|--------------|
| D1 | mobile-app-builder | S3 | P0 | Phase 1 (blocks all FE) |
| D2 | frontend-developer | S3 | P0 | D1 |
| D3 | frontend-developer | S3 | P0 | D1 |
| D4 | frontend-developer + ui-engineer | S3 | P1 | D1, D2 |
| D5 | ui-engineer | S3 | P1 | D1 |
| D6 | ui-engineer | S3 | P1 | D3 |
| B1 | python-backend-engineer + backend-architect | S3 | P0 | Phase 1 (blocks B2) |
| B2 | python-backend-engineer + backend-architect | S3 | P0 | B1 |
| B3 | frontend-developer + frontend-architect | S4 | P0 | B2, D1 (blocks B4-B8) |
| B4 | ui-engineer | S4 | P0 | B3 |
| B5 | frontend-developer + ui-engineer | S4 | P0 | B3 |
| B6 | ui-engineer | S4 | P1 | B3 |
| B7 | ui-engineer | S4 | P1 | B5 |
| B8 | ui-engineer + frontend-developer | S4 | P0 | B3 |

**Parallel Work (Sprint 3):**
- B1 (backend) + D1 (frontend) - No dependencies
- B2 (backend) + D2/D3 (frontend) - After B1/D1 complete
- D4/D5/D6 (frontend polish) - After core infrastructure

**Parallel Work (Sprint 4):**
- B4, B5, B6, B7, B8 (frontend) - All depend on B3, can parallelize after

---

## Next Steps (Sprint 3 Kickoff)

**Immediate Tasks:**
1. **D1** (mobile-app-builder): Create Expo app shell with React Navigation
   - Set up RootNavigator with Stack + Tabs
   - Create placeholder screens: Home, Generate, Visualize, Settings
   - Configure TypeScript, ESLint, Prettier

2. **B1** (python-backend-engineer): Implement DSL → frames converter
   - Create visualization_service.py with dsl_to_frames method
   - Implement polar coordinate layout algorithm
   - Create RenderNode, RenderEdge, VisualizationFrame models
   - Write unit tests for simple round conversion

**Success Indicators:**
- D1 complete: `pnpm --filter mobile dev` runs on iOS/Android simulators
- B1 complete: Unit tests pass for sphere/cylinder/cone frame conversion

---

**Document Version:** 1.0
**Last Updated:** 2025-11-12
**Status:** Active
**Token Count:** ~1800 tokens (under 2000 target)
