# Phase 4: QA, Polish & Optimization

**Knit-Wit MVP Implementation Plan**

**Phase Duration:** 4 weeks (Weeks 12-15)
**Sprints:** Sprint 8, Sprint 9, Sprint 10
**Capacity:** ~160-180 story points
**Team:** QA Lead + 2 engineers (backend + frontend) for fixes
**Priority:** P0 (Launch Blocker)

---

## Phase Overview

### Purpose

Phase 4 validates production readiness through comprehensive testing, accessibility compliance, performance optimization, and monitoring infrastructure. Success criteria: zero critical bugs, WCAG AA compliance, performance targets met, monitoring operational.

### Context

**Input:** Phase 3 complete (all MVP features implemented: pattern generation, visualization, export, Kid Mode, accessibility foundation, telemetry)
**Output:** Production-ready application meeting all non-functional requirements
**Next:** Phase 5 (Launch Preparation, Week 16)

### Goals

1. **Cross-Device Validation:** iOS 14+, Android 10+, tablets, web browsers - all critical flows pass
2. **Accessibility Compliance:** WCAG AA audit passes with 0 critical issues, < 5 warnings
3. **Performance Targets:** < 200ms generation, 60 FPS visualization, responsive UI
4. **Bug Resolution:** 0 critical bugs, all P1 bugs fixed or deferred with justification
5. **E2E Automation:** Critical paths automated (generate → visualize → export)
6. **Monitoring:** Production dashboards, logging, error tracking operational
7. **Documentation:** API docs, user guides, developer setup complete

### Non-Goals

- Production deployment (Phase 5)
- Marketing materials
- App store submissions
- v1.1+ features
- Multi-language support

---

## Testing Strategy

### Cross-Device Testing Matrix

| Platform | Devices | OS Versions | Orientations | Priority |
|----------|---------|-------------|--------------|----------|
| **iOS** | iPhone 12, 14, SE | iOS 14, 16, 17 | Portrait, Landscape | P0 |
| **iPad** | iPad Air 4th gen | iPadOS 17 | Both | P0 |
| **Android Phone** | Pixel 5a, Samsung A10, OnePlus Nord | Android 10-13 | Portrait, Landscape | P0 |
| **Android Tablet** | Samsung Galaxy Tab S7 | Android 11 | Both | P0 |
| **Web** | Chrome 120+, Safari 17+, Firefox 120+ | macOS, Windows | Desktop | P1 |

**Test Approach:**
- Manual smoke tests on all devices (critical flows)
- Automated E2E tests verify consistency
- Visual regression testing for layout issues
- Performance profiling on lowest-spec devices (iPhone SE, Samsung A10)

**Critical Flows:**
1. Generate sphere pattern (default gauge)
2. Navigate visualization (first → last round)
3. Export to PDF
4. Toggle Kid Mode
5. Settings: US ↔ UK terminology, high contrast mode

### Accessibility Testing

#### Automated Audits

**Tools:** axe DevTools, Lighthouse, React Native Accessibility Inspector

**Targets:**
- axe: 0 critical issues, < 5 warnings
- Lighthouse: Accessibility score ≥ 95
- Color contrast: All text meets WCAG AA (4.5:1 normal, 3:1 large/UI)

**Automated Checks:**
- ARIA labels on interactive elements
- Semantic HTML/RN components
- Focus order logical
- Color contrast ratios
- Alt text on images

#### Manual Testing

**Keyboard Navigation:**
- [ ] All controls reachable via Tab
- [ ] Focus indicators visible (minimum 2px outline, 3:1 contrast)
- [ ] Tab order follows visual layout
- [ ] Enter/Space activate buttons
- [ ] Escape dismisses modals

**Screen Readers:**

*iOS VoiceOver:*
- [ ] Buttons announce role + label
- [ ] Form inputs have descriptive labels
- [ ] Navigation announces screen changes
- [ ] Visualization provides round descriptions
- [ ] Swipe gestures work (next/previous round)

*Android TalkBack:*
- [ ] All controls have accessible names
- [ ] Focus order logical
- [ ] Announcements clear and concise
- [ ] Touch exploration functional

**Testing Scenarios:**
1. Generate pattern using only keyboard/screen reader
2. Navigate visualization without visual feedback
3. Export PDF and verify file name announced
4. Toggle settings and confirm state changes announced

#### Color Contrast Verification

**Minimum Ratios (WCAG AA):**
- Body text (< 18pt): 4.5:1
- Large text (≥ 18pt or 14pt bold): 3:1
- UI components (buttons, form borders): 3:1
- Focus indicators: 3:1

**Palette Validation:**

| Element | Foreground | Background | Ratio | Pass |
|---------|-----------|-----------|-------|------|
| Body text | #1a1a1a | #ffffff | 15.6:1 | ✓ |
| Button text | #ffffff | #0066cc | 7.2:1 | ✓ |
| Link text | #0066cc | #ffffff | 7.2:1 | ✓ |
| Disabled | #999999 | #ffffff | 3.2:1 | ✓ |
| Error | #cc0000 | #ffffff | 11.1:1 | ✓ |
| Success | #00aa00 | #ffffff | 4.1:1 | ✓ |

**Colorblind Simulation:**
- Test with protanopia, deuteranopia, tritanopia filters
- Verify increases/decreases distinguishable without color (use icons + text)

### Performance Benchmarking

#### Backend Profiling

**Tool:** Python cProfile + snakeviz

**Metrics:**
- Pattern generation time (p50, p95, p99)
- Hot spots in compilation (function call frequency, cumulative time)
- Memory allocation patterns

**Targets:**
- Sphere (10cm, gauge 14/16): < 150ms
- Cylinder (5cm dia, 10cm height): < 180ms
- Cone (6cm → 2cm, 8cm height): < 200ms
- Memory: < 50MB per request

**Optimization Strategies:**
1. Cache compiler instances (singleton pattern)
2. Memoize gauge calculations (lru_cache)
3. Optimize even_distribution() (called frequently)
4. Profile DSL construction (reduce object creation overhead)

**Profiling Script:**

```python
import cProfile
import pstats
from knit_wit_engine import SphereCompiler, GenerateRequest, Gauge

def profile_generation():
    profiler = cProfile.Profile()
    profiler.enable()

    compiler = SphereCompiler()
    request = GenerateRequest(
        shape='sphere', diameter=10,
        gauge=Gauge(sts_per_10cm=14, rows_per_10cm=16),
        stitch='sc', terms='US'
    )
    dsl = compiler.generate(request)

    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # Top 20 functions
```

#### Frontend Profiling

**Tools:** React DevTools Profiler, Flipper (React Native)

**Metrics:**
- Component render times (mount, update)
- Frame rates during visualization (FPS)
- Bundle sizes (APK, IPA)
- Memory usage during navigation

**Targets:**
- Visualization frame rate: ≥ 60 FPS on iPhone 12, Pixel 5a
- Round navigation: < 50ms render time
- APK size: < 50MB
- IPA size: < 100MB
- Memory: < 100MB during typical session

**Optimization Strategies:**
1. Virtualize SVG rendering (only render visible round)
2. Memoize expensive components (React.memo)
3. Code-split heavy modules (PDF export, parser)
4. Compress assets (images, fonts)
5. Tree-shake unused dependencies

**Profiling Approach:**

```typescript
import { Profiler } from 'react';

function onRenderCallback(
  id: string, phase: "mount" | "update",
  actualDuration: number
) {
  console.log(`${id} (${phase}): ${actualDuration}ms`);
}

export function VisualizationScreen() {
  return (
    <Profiler id="VisualizationScreen" onRender={onRenderCallback}>
      {/* Screen content */}
    </Profiler>
  );
}
```

#### Performance Benchmarks

**Test Cases:**

1. **Small Pattern (Sphere 5cm):**
   - Generation: < 100ms
   - Visualization: < 30ms per round
   - Export PDF: < 2s

2. **Medium Pattern (Sphere 10cm):**
   - Generation: < 150ms
   - Visualization: < 50ms per round
   - Export PDF: < 3s

3. **Large Pattern (Cylinder 20cm height):**
   - Generation: < 200ms
   - Visualization: < 100ms per round
   - Export PDF: < 5s

4. **Edge Case (100+ rounds):**
   - Generation: < 500ms
   - Visualization: Smooth scrolling (no jank)
   - Export PDF: < 10s

### E2E Automation

#### Framework Selection

**Options:**
- **Detox** (React Native native) - Recommended
- **Playwright** (Web fallback)

**Detox Advantages:**
- Native RN support (iOS, Android)
- Fast execution (runs on device/simulator)
- Less flaky than WebDriver-based tools
- Simulates real user interactions (tap, swipe, scroll)

#### Critical Flows to Automate

**Flow 1: Generate → Visualize**

```typescript
describe('Generate and Visualize Flow', () => {
  beforeAll(async () => {
    await device.launchApp();
  });

  it('should generate a sphere and visualize', async () => {
    await element(by.id('generateButton')).tap();
    await element(by.id('shapeSelect')).tap();
    await element(by.text('Sphere')).tap();
    await element(by.id('diameterInput')).typeText('10');
    await element(by.id('gaugeInput')).typeText('14/16');
    await element(by.id('submitButton')).tap();

    await waitFor(element(by.id('visualizationScreen')))
      .toBeVisible()
      .withTimeout(3000);

    await expect(element(by.text('Round 1'))).toBeVisible();
    await expect(element(by.id('patternFrame'))).toBeVisible();
  });
});
```

**Flow 2: Navigation**

```typescript
describe('Visualization Navigation', () => {
  it('should navigate rounds forward and back', async () => {
    // Assumes pattern already generated
    await element(by.id('nextRoundButton')).tap();
    await expect(element(by.text('Round 2'))).toBeVisible();

    await element(by.id('nextRoundButton')).tap();
    await expect(element(by.text('Round 3'))).toBeVisible();

    await element(by.id('prevRoundButton')).tap();
    await expect(element(by.text('Round 2'))).toBeVisible();
  });

  it('should jump to specific round via scrubber', async () => {
    await element(by.id('roundScrubber')).swipe('right', 'fast', 0.5);
    // Verify round number updated (specific assertion depends on implementation)
  });
});
```

**Flow 3: Export**

```typescript
describe('Export Flow', () => {
  it('should export pattern as PDF', async () => {
    await element(by.id('exportButton')).tap();
    await element(by.text('PDF')).tap();
    await element(by.id('downloadButton')).tap();

    await waitFor(element(by.text('PDF exported successfully')))
      .toBeVisible()
      .withTimeout(5000);
  });

  it('should export as SVG', async () => {
    await element(by.id('exportButton')).tap();
    await element(by.text('SVG')).tap();
    await element(by.id('downloadButton')).tap();

    await expect(element(by.text('SVG exported successfully'))).toBeVisible();
  });
});
```

**Flow 4: Settings & Accessibility**

```typescript
describe('Settings Flow', () => {
  it('should toggle Kid Mode', async () => {
    await element(by.id('settingsButton')).tap();
    await element(by.id('kidModeToggle')).tap();

    await device.pressBack();  // Android
    // or: await element(by.id('backButton')).tap();

    // Verify Kid Mode UI changes (larger text, simplified copy)
    await expect(element(by.id('kidModeIndicator'))).toBeVisible();
  });

  it('should toggle high contrast mode', async () => {
    await element(by.id('settingsButton')).tap();
    await element(by.id('highContrastToggle')).tap();

    await device.pressBack();

    // Verify contrast changes applied
    await expect(element(by.id('highContrastIndicator'))).toBeVisible();
  });

  it('should switch US ↔ UK terminology', async () => {
    await element(by.id('settingsButton')).tap();
    await element(by.id('terminologyToggle')).tap();

    await device.pressBack();

    // Verify terminology updated in pattern
    await expect(element(by.text('dc'))).toBeVisible();  // UK term for US sc
  });
});
```

#### Regression Test Suite

**Coverage:**
- All previously working features from Phases 1-3
- Edge cases discovered during development
- Bug fixes (verify no regressions)

**Automation Strategy:**
- Run E2E suite on every PR (smoke tests)
- Full regression suite nightly
- Manual verification for visual changes

---

## Sprint Plans

### Sprint 8: Cross-Device Testing + Accessibility Audit (Weeks 12-13)

**Duration:** 2 weeks
**Capacity:** ~85-95 story points
**Goal:** All devices tested; accessibility audit complete; performance baseline established

#### Stories

| ID | Title | Effort | Owner | Dependencies |
|----|-------|--------|-------|--------------|
| QA-1 | iOS smoke tests (iPhone 12, 14, SE) | 8 | QA Lead | Phase 3 complete |
| QA-2 | Android smoke tests (Pixel, Samsung, OnePlus) | 8 | QA Lead | Phase 3 complete |
| QA-3 | Tablet testing (iPad, Galaxy Tab) | 5 | QA Engineer | Phase 3 complete |
| QA-4 | Web browser testing (Chrome, Safari, Firefox) | 5 | QA Engineer | Phase 3 complete |
| A11Y-1 | WCAG AA automated audit (axe, Lighthouse) | 5 | Frontend Lead | Phase 3 complete |
| A11Y-2 | Manual accessibility review (keyboard, screen reader) | 8 | Frontend Engineer | A11Y-1 |
| A11Y-3 | Color contrast verification | 5 | Frontend Engineer | A11Y-1 |
| PERF-1 | Backend profiling (cProfile) | 5 | Backend Lead | Phase 3 complete |
| PERF-2 | Frontend profiling (React DevTools, Flipper) | 5 | Frontend Lead | Phase 3 complete |
| BUG-1 | Triage all open issues | 3 | QA Lead | QA-1, QA-2, QA-3 |
| MON-1 | Backend structured logging | 5 | Backend Engineer | None |
| DOC-1 | API documentation (OpenAPI/Swagger) | 5 | Backend Engineer | Phase 3 complete |

**Total:** 67 story points

#### Acceptance Criteria

- [ ] All devices tested; results documented in cross-device test report
- [ ] Accessibility audit identifies all issues (automated + manual)
- [ ] Performance profiling identifies hot spots
- [ ] Bug backlog triaged with priority labels (P0, P1, P2)
- [ ] Structured logging emits JSON logs with request IDs
- [ ] API docs auto-generated and published

#### Demo Objectives

- Show test results from iOS, Android, tablet, web
- Present accessibility findings (critical issues, warnings)
- Demonstrate profiling results (hot spots, optimization opportunities)
- Review bug triage (priorities, severity)
- Show structured logging in action

---

### Sprint 9: Optimization + Bug Fixes (Week 13-14)

**Duration:** 1 week
**Capacity:** ~50 story points
**Goal:** Performance targets met; critical bugs fixed; accessibility issues resolved

#### Stories

| ID | Title | Effort | Owner | Dependencies |
|----|-------|--------|-------|--------------|
| PERF-3 | SVG optimization (virtualization, LOD) | 8 | Frontend Lead | PERF-2 |
| PERF-4 | Backend caching (compiler instances, gauge) | 5 | Backend Engineer | PERF-1 |
| PERF-5 | Bundle size optimization (code-split, tree-shake) | 5 | Frontend Engineer | PERF-2 |
| BUG-2 | Fix all critical bugs (P0) | 21 | Full Team | BUG-1 |
| A11Y-4 | Fix accessibility issues | 8 | Frontend Engineer | A11Y-2, A11Y-3 |
| A11Y-5 | Dyslexia-friendly font testing | 3 | Frontend Engineer | A11Y-4 |
| MON-2 | Error tracking (Sentry) | 4 | Backend Engineer | None |

**Total:** 54 story points

#### Acceptance Criteria

- [ ] Backend generation < 200ms (p95)
- [ ] Frontend frame rate ≥ 60 FPS on mid-range devices
- [ ] Bundle sizes: APK < 50MB, IPA < 100MB
- [ ] Zero critical bugs (P0) remaining
- [ ] All accessibility critical issues fixed
- [ ] Error tracking captures exceptions with stack traces

#### Demo Objectives

- Demonstrate improved performance (generation time, FPS, bundle size)
- Show critical bug fixes with before/after
- Present accessibility remediation (audit re-run shows 0 critical)
- Demonstrate error tracking capturing and reporting failures

---

### Sprint 10: E2E Automation + Final Polish (Week 14-15)

**Duration:** 1 week
**Capacity:** ~45 story points
**Goal:** E2E tests automated; documentation complete; production-ready

#### Stories

| ID | Title | Effort | Owner | Dependencies |
|----|-------|--------|-------|--------------|
| QA-5 | E2E automation (Detox: generate → visualize → export) | 13 | QA Lead | QA-1, QA-2 |
| QA-6 | Regression test suite | 8 | QA Engineer | QA-5 |
| QA-7 | Cross-device test report | 5 | QA Lead | QA-1, QA-2, QA-3, QA-4 |
| BUG-3 | Minor polish (animations, spacing, copy) | 8 | Frontend Engineer | BUG-2 |
| BUG-4 | Regression testing (verify bug fixes) | 5 | QA Engineer | BUG-2, BUG-3 |
| MON-3 | Telemetry pipeline (opt-in, event tracking) | 8 | Full Stack Engineer | None |
| DOC-2 | User guide + FAQ | 8 | Tech Writer | Phase 3 complete |
| DOC-3 | Developer README updates | 5 | Backend Lead | Phase 3 complete |
| DOC-4 | Release notes | 3 | Product Lead | All stories |

**Total:** 63 story points

#### Acceptance Criteria

- [ ] E2E tests cover critical flows (generate, visualize, export, settings)
- [ ] Regression suite runs successfully (all tests pass)
- [ ] Cross-device test report documents all findings
- [ ] Minor polish applied (smooth animations, consistent spacing, clear copy)
- [ ] Telemetry opt-in functional; events tracked
- [ ] User guide covers pattern generation, visualization, export
- [ ] Developer README includes setup, architecture, contribution guide
- [ ] Release notes document MVP features, known issues

#### Demo Objectives

- Demonstrate E2E tests running (live execution)
- Show regression suite coverage
- Present telemetry dashboard with event tracking
- Review user guide and FAQ (content preview)
- Confirm Phase 4 exit criteria met (production-ready)

---

## Quality Gates & Launch Criteria

### Phase 4 Exit Criteria

**Testing:**
- [ ] Cross-device testing complete (iOS, Android, tablets, web)
- [ ] E2E automation covers critical flows (generate, visualize, export)
- [ ] Regression suite passes (100% of tests)
- [ ] Zero critical bugs (P0)
- [ ] All high-priority bugs (P1) fixed or explicitly deferred

**Accessibility:**
- [ ] WCAG AA compliance: 0 critical issues, < 5 warnings
- [ ] Manual keyboard navigation passes
- [ ] Screen reader testing complete (VoiceOver, TalkBack)
- [ ] Color contrast meets all WCAG AA ratios
- [ ] Dyslexia-friendly font option verified

**Performance:**
- [ ] Pattern generation < 200ms (p95)
- [ ] Visualization ≥ 60 FPS on mid-range devices
- [ ] Bundle sizes within limits (APK < 50MB, IPA < 100MB)
- [ ] Large patterns (100+ rounds) render smoothly

**Monitoring:**
- [ ] Structured logging operational (JSON, request IDs)
- [ ] Error tracking captures exceptions (Sentry or equivalent)
- [ ] Telemetry pipeline tracks key events (opt-in)
- [ ] Dashboards show API health, error rates, event volume

**Documentation:**
- [ ] API documentation auto-generated (OpenAPI/Swagger)
- [ ] User guide and FAQ complete
- [ ] Developer README updated (setup, architecture, contribution)
- [ ] Release notes finalized

### Bug Severity Levels

| Level | Description | SLA | Examples |
|-------|-------------|-----|----------|
| **P0 (Critical)** | App crashes, data loss, major UX broken | Fix immediately | Pattern generation crashes; visualization doesn't render |
| **P1 (High)** | Feature broken, workaround exists | Fix before launch | Export fails on specific devices; scrubber jumps incorrectly |
| **P2 (Medium)** | Minor issue, doesn't block usage | Fix post-launch | Visual glitch in Kid Mode; tooltip text truncated |
| **P3 (Low)** | Cosmetic, edge case | Backlog | Button hover color inconsistent |

**Launch Blockers:** Any P0 bug blocks launch. All P1 bugs must be fixed or explicitly deferred with Product Lead approval.

### Performance Thresholds

| Metric | Target | Measurement | Tool |
|--------|--------|-------------|------|
| Pattern generation | < 200ms (p95) | Server-side elapsed time | cProfile, logs |
| Visualization FPS | ≥ 60 FPS | Frame time during round navigation | Flipper, React DevTools |
| API response | < 500ms (p95) | HTTP request duration | FastAPI middleware, logs |
| Bundle size (APK) | < 50MB | Build artifact size | Android build output |
| Bundle size (IPA) | < 100MB | Build artifact size | Xcode build output |
| Memory usage | < 100MB | Runtime memory during session | Xcode Instruments, Android Profiler |

**Measurement Approach:**
- Backend: Instrument API endpoints with timing middleware
- Frontend: Use React DevTools Profiler + Flipper Performance plugin
- E2E: Automated performance tests in CI

---

## Deliverables

### Test Reports

**1. Cross-Device Test Report**

**Format:** Markdown document in `project_plans/mvp/test-reports/`

**Contents:**
- Test matrix (devices, OS versions, flows tested)
- Pass/fail status per device per flow
- Screenshots of failures
- Known issues and workarounds
- Recommendations for device support policy

**Example:**

```markdown
# Cross-Device Test Report

## Test Matrix

| Device | OS | Generate | Visualize | Export | Kid Mode | Settings |
|--------|----|----|----|----|----|----|
| iPhone 12 | iOS 16 | ✓ | ✓ | ✓ | ✓ | ✓ |
| iPhone SE | iOS 14 | ✓ | ✓ | ✗ (PDF export slow) | ✓ | ✓ |
| Pixel 5a | Android 13 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Samsung A10 | Android 10 | ✓ | ⚠ (FPS drops) | ✓ | ✓ | ✓ |

## Issues

**ISS-1 (P1):** PDF export on iPhone SE (iOS 14) takes 8+ seconds
- Repro: Generate large pattern (20cm sphere), export to PDF
- Root cause: Memory pressure on low-RAM device
- Fix: Optimize PDF generation (reduce image resolution)

**ISS-2 (P2):** Frame rate drops on Samsung A10 during visualization
- Repro: Navigate rapidly between rounds
- Root cause: GPU limitations on older device
- Fix: Reduce SVG complexity, implement LOD rendering
```

**2. Accessibility Audit Report**

**Format:** Markdown + JSON (axe results)

**Contents:**
- Automated audit results (axe, Lighthouse)
- Manual testing results (keyboard, screen reader)
- Color contrast verification
- Issues found (categorized by severity)
- Remediation status
- WCAG AA compliance statement

**3. Performance Benchmark Report**

**Format:** Markdown + CSV (raw data)

**Contents:**
- Backend profiling results (hot spots, optimization recommendations)
- Frontend profiling results (component render times, FPS)
- Bundle size analysis (breakdown by module)
- Performance test results (generation time, visualization FPS)
- Before/after comparisons for optimizations
- Recommendations for further improvements

### Bug Database

**Tool:** GitHub Issues with labels

**Labels:**
- `bug` - Defect
- `P0-critical`, `P1-high`, `P2-medium`, `P3-low` - Priority
- `accessibility`, `performance`, `ux` - Category
- `ios`, `android`, `web` - Platform
- `needs-triage`, `in-progress`, `fixed`, `wont-fix` - Status

**Triage Process:**
1. QA Lead creates issue for each bug found
2. Team triages in Sprint 8 (assign priority, owner)
3. P0/P1 bugs assigned to Sprint 9
4. Verification in Sprint 10 (regression testing)

### Monitoring & Dashboards

**Backend Monitoring**

**Tool:** Grafana + Prometheus (or Datadog, New Relic)

**Dashboards:**

1. **API Health:**
   - Request rate (requests/min)
   - Response time (p50, p95, p99)
   - Error rate (percentage)
   - Active requests

2. **Pattern Generation:**
   - Generation time by shape type
   - Success/failure rate
   - Gauge distribution (common gauges)

3. **System:**
   - CPU usage
   - Memory usage
   - Disk I/O
   - Network I/O

**Alerts:**
- Error rate > 1% for 5 minutes
- p95 response time > 1s for 5 minutes
- Service unavailable (5xx errors)

**Frontend Telemetry**

**Tool:** Custom backend endpoint + analytics dashboard

**Events Tracked:**
- `pattern_generated` (shape, gauge, success, generation_time_ms)
- `pattern_visualized` (total_rounds, rounds_viewed, session_duration_seconds)
- `pattern_exported` (format, success, file_size_bytes)
- `settings_changed` (setting_name, old_value, new_value)
- `error_occurred` (error_code, error_message, screen)

**Dashboard Metrics:**
- Events per hour/day
- Top shapes generated
- Export format distribution
- Error breakdown by type
- User engagement (session duration, rounds viewed)

### Documentation

**1. API Documentation**

**Tool:** FastAPI auto-generated OpenAPI/Swagger UI

**URL:** `https://api.knitwit.app/docs`

**Contents:**
- All endpoints with request/response schemas
- Authentication (if applicable)
- Error codes and messages
- Rate limits
- Examples

**2. User Guide**

**Location:** `docs/user-guide.md`

**Contents:**
- Introduction to Knit-Wit
- How to generate a pattern (step-by-step)
- Understanding the visualization
- Exporting patterns (PDF, SVG, JSON)
- Settings and customization
- Accessibility features
- Troubleshooting

**3. Developer Documentation**

**Location:** `README.md`, `docs/developer/`

**Contents:**
- Setup instructions (frontend, backend, full stack)
- Architecture overview
- Code structure and conventions
- Testing strategy
- Contributing guide
- Deployment process

**4. Release Notes**

**Location:** `CHANGELOG.md`, `docs/releases/mvp-v1.0.md`

**Contents:**
- MVP features (pattern generation, visualization, export, accessibility)
- Known issues and limitations
- Performance characteristics
- Browser/device support
- Upgrade instructions (if applicable)
- Future roadmap (v1.1+)

---

## Dependencies & Risks

### Dependencies

**Internal:**
- Phase 3 complete (all MVP features implemented)
- CI/CD pipeline operational (automated tests, builds)
- Staging environment available for testing

**External:**
- Physical devices available for testing (iOS, Android, tablets)
- Error tracking service provisioned (Sentry account, API key)
- Monitoring infrastructure set up (Grafana/Datadog)

### Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **Critical bugs found late** | High (launch delay) | Medium | Early cross-device testing (Sprint 8); daily bug triage |
| **Performance targets not met** | High (poor UX) | Medium | Profiling in Sprint 8; optimization buffer in Sprint 9 |
| **Accessibility compliance fails** | High (legal/ethical) | Low | Automated audits early; manual testing by specialists |
| **E2E automation blocked** | Medium (manual testing burden) | Low | Start Detox setup early; fallback to manual critical path testing |
| **Device availability** | Medium (incomplete testing) | Low | Secure devices in advance; use cloud testing services (BrowserStack) |
| **Documentation incomplete** | Low (poor onboarding) | Medium | Assign dedicated time; template documents early |

**Contingency Plans:**
- If critical bugs found: Extend Sprint 9 by 2-3 days; defer P2 bugs
- If performance targets missed: Descope non-critical features; add caching aggressively
- If accessibility fails: Dedicated sprint for remediation (post-launch if necessary, with disclosure)
- If E2E blocked: Manual test critical paths; automate post-launch

---

## Next Phase Preview

**Phase 5: Launch Preparation (Week 16)**

**Goals:**
- Final smoke tests and regression verification
- Production deployment (backend, frontend)
- Monitoring and alerting configured
- Go/no-go decision for public launch
- Launch communications (social, blog, docs site)

**Key Activities:**
- Staging → production deployment
- DNS configuration and SSL certificates
- Final security review
- Launch day monitoring (on-call rotation)
- Post-launch retrospective

**Success Criteria:**
- Production environment stable
- Monitoring shows healthy metrics
- Zero production incidents in first 24 hours
- User feedback collection operational

---

**Phase 4 Status:** Not Started
**Next Review:** Sprint 8 Retrospective (End of Week 13)
