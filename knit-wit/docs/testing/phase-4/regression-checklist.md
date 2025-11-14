# BUG-4: Regression Testing Checklist - Phase 4 Sprint 10

**Story**: BUG-4 - Regression Testing Checklist (Final Verification)
**Sprint**: Sprint 10 (Weeks 14-15)
**Effort**: 5 story points
**Owner**: QA Lead + Dev Team
**Status**: Pre-Release Testing Checklist
**Created**: 2025-11-14

---

## Executive Summary

Comprehensive pre-release checklist ensuring all MVP features from Phases 0-3 work correctly, bug fixes from Sprint 9 are verified, and optimizations don't introduce regressions. Use this checklist for final testing before MVP release.

**Scope:**
- All critical user flows (Phases 0-3)
- Sprint 9 bug fix verification
- Optimization regression testing
- Performance and accessibility verification
- Cross-device and cross-OS validation

**Timeline**: 4-6 hours for complete manual testing on all platforms

---

## Part 1: Pre-Testing Setup

### Environment Verification

- [ ] **Latest build** installed on all test devices
- [ ] **Clean app state**: Uninstall and reinstall (don't upgrade)
- [ ] **Device OS versions**:
  - [ ] iPhone (iOS 14, 16, 17): SE, 12, 14
  - [ ] Android (12, 13, 14): Pixel 5a, Samsung A10
  - [ ] Tablet (iPad Air, Galaxy Tab S7)
- [ ] **Test data**: Use standard test patterns (sphere 10cm, cylinder 8cm, cone 6cm)
- [ ] **Test environment**: Backend API accessible and responsive
- [ ] **Connectivity**: WiFi and mobile data both tested

### Tester Information

| Role | Tester | Device | OS Version | Date | Status |
|------|--------|--------|-----------|------|--------|
| QA Lead | | | | | ☐ |
| iOS Tester | | iPhone | iOS | | ☐ |
| Android Tester | | Pixel | Android | | ☐ |
| Accessibility Tester | | | | | ☐ |

---

## Part 2: Critical User Flows

### FLOW-1: Generate Sphere Pattern (Default)

**Expected Path**: Home → Generate → Select Sphere (default) → Generate → Visualize

**Test Steps**:
- [ ] App opens to Home screen cleanly
- [ ] "Generate" button responsive
- [ ] Generator screen loads with Sphere pre-selected
- [ ] Default parameters shown: 10cm diameter, 14/16 gauge, US terminology
- [ ] "Generate" button generates pattern (< 500ms total)
- [ ] Visualization screen appears with SVG sphere
- [ ] Round 1 shows 6 stitches (magic ring)
- [ ] Rounds increment logically (6 → 8 → 10 → ...)

**Expected Result**: Sphere pattern with ~12-14 rounds visible
**Device Coverage**: ☐ iPhone SE (iOS 14) | ☐ iPhone 12 (iOS 16) | ☐ iPhone 14 (iOS 17) | ☐ Pixel 5a | ☐ Samsung A10 | ☐ iPad Air
**Status**: ☐ PASS | ☐ FAIL

**If Failed**: Document issue number and severity

---

### FLOW-2: Generate Cylinder with Custom Gauge

**Expected Path**: Home → Generate → Select Cylinder → Set 8cm diameter → Set 12/14 gauge → Generate → Visualize

**Test Steps**:
- [ ] Navigator to Generator
- [ ] Select "Cylinder" from shape dropdown
- [ ] Set diameter: 8 cm (accepts value, no validation error)
- [ ] Set gauge: 12 stitches / 14 rows per 10cm
- [ ] Custom gauge accepted without validation error
- [ ] Generate cylinder pattern
- [ ] Visualization shows cylindrical structure
- [ ] Circumference stitches match custom gauge

**Expected Result**: Cylinder with custom gauge applied
**Device Coverage**: ☐ iPhone 12 | ☐ Pixel 5a | ☐ iPad
**Status**: ☐ PASS | ☐ FAIL

---

### FLOW-3: Round-by-Round Navigation

**Expected Path**: Visualization → Navigate rounds → Scrub to different round → Sequential navigation

**Test Steps**:
- [ ] Pattern visible with round navigator
- [ ] **Next Round button**: Advances from Round 1 → 2 → 3 (updates < 50ms)
- [ ] **Previous Round button**: Reverses from Round 3 → 2 → 1
- [ ] **Round info updated**: "Round X of Y", stitch count updates correctly
- [ ] **Scrubber/slider**: Draggable to any round, jumps correctly
- [ ] **Visual feedback**: Smooth transitions, no stuttering or frame drops on iPhone SE

**Expected Result**: Smooth round navigation at 60 FPS (min 50 FPS on low-end)
**Device Coverage**: ☐ iPhone SE | ☐ iPhone 14 | ☐ Pixel 5a
**Status**: ☐ PASS | ☐ FAIL

**Performance Note**: Frame rate monitoring with DevTools (target 60 FPS, acceptable 50+ FPS)

---

### FLOW-4: Multi-Format Export

#### FLOW-4a: PDF Export

**Expected Path**: Visualization → Export → Select PDF → Confirm → Download

**Test Steps**:
- [ ] Export button responsive on visualization screen
- [ ] Export options dialog shows: PDF, SVG, JSON, PNG
- [ ] **PDF export**: Starts within 100ms, completes < 3s
- [ ] **Success message**: Shows "PDF ready" or similar
- [ ] **File created**: PDF accessible in Files app / Downloads
- [ ] **PDF quality**: Opens in PDF viewer, shows pattern and instructions
- [ ] **File size**: < 5MB for standard pattern

**Expected Result**: Valid PDF with pattern diagram and instructions
**Device Coverage**: ☐ iPhone 12 | ☐ Pixel 5a | ☐ Tablet
**Status**: ☐ PASS | ☐ FAIL

#### FLOW-4b: SVG Export

**Test Steps**:
- [ ] SVG export option selectable
- [ ] SVG file created (.svg extension)
- [ ] File opens in web browsers (Chrome, Safari)
- [ ] Visualization matches on-screen version
- [ ] File size < 500KB

**Status**: ☐ PASS | ☐ FAIL

#### FLOW-4c: JSON Export

**Test Steps**:
- [ ] JSON export creates .json file
- [ ] JSON is valid, parseable (test with JSON validator)
- [ ] DSL v0.1 schema verified:
  - [ ] `meta` section: version, units, terms, gauge, stitch
  - [ ] `object` section: type (sphere/cylinder/cone), params
  - [ ] `rounds` array: populated with operations (MR, sc, inc, dec)
  - [ ] `materials` section: yarn_weight, hook_size_mm, yardage_estimate
- [ ] Operations match expected stitch types

**Status**: ☐ PASS | ☐ FAIL

#### FLOW-4d: PNG Export

**Test Steps**:
- [ ] PNG export creates image file
- [ ] Image opens in photo viewer
- [ ] Visualization screenshot captured correctly
- [ ] Image quality acceptable (not pixelated)

**Status**: ☐ PASS | ☐ FAIL

---

### FLOW-5: Kid Mode Toggle & Functionality

**Expected Path**: Settings → Enable Kid Mode → Verify UI changes → Disable Kid Mode → Verify revert

**Test Steps**:
- [ ] Settings screen accessible from Home
- [ ] Kid Mode toggle found and functional
- [ ] **Enable Kid Mode**:
  - [ ] Font sizes increase (min 18px for body text)
  - [ ] All buttons enlarge (min 56x56pt)
  - [ ] Colors become saturated/brighter
  - [ ] Touch targets meet 56x56pt minimum
  - [ ] Copy simplifies (e.g., "Diameter" → "Size: how big?")
- [ ] **Generate pattern in Kid Mode**:
  - [ ] Pattern generates with simplified instructions
  - [ ] Tooltip copy child-friendly ("Add Stitch" instead of "Increase")
- [ ] **Disable Kid Mode**:
  - [ ] UI reverts to standard sizes
  - [ ] Font sizes return to normal
  - [ ] Copy reverts to technical terminology
  - [ ] No crashes or visual glitches

**Expected Result**: Smooth Kid Mode toggle, all UI updates applied correctly
**Device Coverage**: ☐ iPhone 12 | ☐ Pixel 5a | ☐ Tablet
**Status**: ☐ PASS | ☐ FAIL

---

### FLOW-6: Settings Persistence

**Expected Path**: Change Settings → Close App → Reopen → Verify persistence

**Test Steps**:
- [ ] Navigate to Settings
- [ ] **Terminology**: Change from US to UK
- [ ] **Kid Mode**: Enable (toggle on)
- [ ] **High Contrast**: Enable (toggle on)
- [ ] Return to Home, generate pattern, verify all settings applied
- [ ] **Close app completely** (force quit, not just background)
- [ ] **Reopen app**
- [ ] Navigate to Settings
- [ ] **Verify persistence**:
  - [ ] Terminology: UK (not reset to US)
  - [ ] Kid Mode: ON (not reset to OFF)
  - [ ] High Contrast: ON
- [ ] Generate pattern, verify settings still applied

**Expected Result**: All settings survive app restart
**Device Coverage**: ☐ iPhone SE | ☐ Pixel 5a
**Status**: ☐ PASS | ☐ FAIL

---

### FLOW-7: Terminology Translation (US ↔ UK)

**Expected Path**: Generate pattern US → Settings change to UK → Verify stitch abbreviations translate

**Test Steps**:
- [ ] Generate pattern with US terminology
- [ ] Verify stitches shown: "sc" (single crochet), "inc" (increase), "dec" (decrease)
- [ ] Navigate to Settings
- [ ] Change Terminology to UK
- [ ] Return to pattern
- [ ] **Stitch translations verified**:
  - [ ] "sc" (US) → "dc" (UK double crochet)
  - [ ] Instructions reflect UK equivalent
- [ ] **Change back to US**
- [ ] Stitches revert to US abbreviations

**Expected Result**: Terminology switches instantly, translations accurate
**Device Coverage**: ☐ iPhone 12 | ☐ Pixel 5a
**Status**: ☐ PASS | ☐ FAIL

---

## Part 3: Sprint 9 Bug Fix Verification

### Bug Fixes from Sprint 9 - Confirm Resolved

| Bug ID | Description | Test Steps | Status |
|--------|-------------|-----------|--------|
| **S9-BUG-1** | SVG rendering jank on iPhone SE | Generate large pattern (100+ stitches), navigate rounds, verify 50+ FPS | ☐ PASS ☐ FAIL |
| **S9-BUG-2** | PDF export timeout on slow networks | Generate sphere, export PDF with 3G throttling, should complete < 10s | ☐ PASS ☐ FAIL |
| **S9-BUG-3** | Kid Mode text overflow on small screens | Enable Kid Mode on iPhone SE, verify all text wraps correctly | ☐ PASS ☐ FAIL |
| **S9-BUG-4** | VoiceOver not announcing round changes | Enable VoiceOver, navigate rounds, verify "Round X of Y" announced | ☐ PASS ☐ FAIL |
| **S9-BUG-5** | Settings not persisting on Android | Change settings on Pixel 5a, restart app, verify persistence | ☐ PASS ☐ FAIL |
| **S9-BUG-6** | Export dialog cut off on iPad (landscape) | Rotate iPad to landscape, open export dialog, verify all options visible | ☐ PASS ☐ FAIL |
| **S9-BUG-7** | Gauge error messages unclear | Try invalid gauge (50), verify error message is actionable | ☐ PASS ☐ FAIL |
| **S9-BUG-8** | Invalid parameter values accepted | Try diameter -5, verify rejected with clear error | ☐ PASS ☐ FAIL |

**Summary**: ☐ All bugs verified fixed | ☐ Regression issues found (document below)

---

## Part 4: Performance Verification

### Generation Performance

- [ ] **Pattern generation time** (target < 200ms server-side):
  - [ ] Sphere (10cm): ~50-100ms
  - [ ] Cylinder (8cm): ~50-100ms
  - [ ] Cone (6cm): ~50-100ms
  - [ ] *Note: Total time including network = 200-500ms*

- [ ] **Visualization rendering** (target < 100ms per frame):
  - [ ] Round navigation: Smooth transitions, no visible lag
  - [ ] Scrubber interaction: Responsive during drag
  - [ ] Frame rate: 50+ FPS on iPhone SE, 60 FPS on modern devices

### Export Performance

- [ ] **PDF export** (target < 3 seconds):
  - [ ] Sphere (10cm): ~1-2 seconds
  - [ ] Cylinder (8cm): ~1-2 seconds
  - [ ] Large pattern (100+ stitches): < 3 seconds

- [ ] **SVG/JSON export** (target < 500ms):
  - [ ] All patterns export quickly
  - [ ] No visible lag or UI freeze

### Network Performance

- [ ] **API Response Times** (p95 target < 500ms):
  - [ ] Test on WiFi: < 300ms
  - [ ] Test on 4G: < 500ms
  - [ ] Test on 3G: < 1s

---

## Part 5: Accessibility Compliance (WCAG AA)

### Color Contrast Ratios

- [ ] **Normal mode**: All text ≥ 4.5:1 (WCAG AA)
  - [ ] Home buttons: test with Accessibility Inspector
  - [ ] Generator labels: verify contrast
  - [ ] Visualization metadata: readable on all backgrounds
  - [ ] Export options: sufficient contrast

- [ ] **High Contrast mode**: All text ≥ 7:1 (WCAG AAA)
  - [ ] Enable High Contrast in Settings
  - [ ] Verify text appears darker/more saturated
  - [ ] Re-measure all critical text
  - [ ] Verify colors different from normal mode

- [ ] **Kid Mode colors**: Verify accessible and distinct
  - [ ] Increase highlights: distinct from normal stitches
  - [ ] Decrease highlights: distinct color
  - [ ] All colors pass 3:1 minimum for UI components

### Touch Target Sizing

- [ ] **Normal mode**: All interactive elements ≥ 44x44pt (iOS) / 48x48dp (Android)
  - [ ] Buttons: Generate, Settings, Next/Previous, Export
  - [ ] Input fields: diameter, gauge entries
  - [ ] Toggle switches: accessible and easy to tap
  - [ ] Scrubber: draggable and responsive

- [ ] **Kid Mode**: All interactive elements ≥ 56x56pt
  - [ ] Measure with Accessibility Inspector
  - [ ] Verify on actual devices (not just simulator)
  - [ ] Test touch response: no misses or accidental adjacent taps

### Screen Reader Support (VoiceOver / TalkBack)

#### iOS (VoiceOver)

- [ ] **Home Screen**:
  - [ ] "Generate button" announced
  - [ ] "Settings button" announced

- [ ] **Generator Screen**:
  - [ ] Shape selector: "Sphere selected" announced when tapped
  - [ ] Diameter input: label clear ("Diameter (cm)" or "Size: how big?" in Kid Mode)
  - [ ] Generate button: "Generate, button" announced

- [ ] **Visualization Screen**:
  - [ ] Round info: "Round 1 of 12" announced
  - [ ] Stitch count: "Stitches: 6" announced
  - [ ] Round navigation: New round announced when changed
  - [ ] Stitch nodes: Each announced with role and position (may need grouping)

- [ ] **Export Screen**:
  - [ ] Options announced: "PDF option", "SVG option", etc.
  - [ ] Export button: Responds to double-tap activation

- [ ] **Settings Screen**:
  - [ ] Toggle states announced: "Kid Mode, switch, off" / "...on"
  - [ ] Setting changes announced: "High Contrast, off" (when toggled)

#### Android (TalkBack)

- [ ] Perform same tests with TalkBack enabled
- [ ] Gestures work: Swipe right/left for navigation, double-tap to activate
- [ ] All labels announced clearly
- [ ] Reading order logical

**Status**: ☐ VoiceOver tested | ☐ TalkBack tested | ☐ All pass

### Keyboard Navigation (with external keyboard)

- [ ] **Tab navigation**: Move between all interactive elements
- [ ] **Focus indicators**: Visible at all times (2px+ outline)
- [ ] **Enter/Space**: Activate buttons
- [ ] **All major flows** navigable with keyboard only
- [ ] **Tab order**: Logical and predictable (left-to-right, top-to-bottom)

**Status**: ☐ PASS | ☐ FAIL

---

## Part 6: Cross-Device Validation

### Device Test Matrix

Complete testing on minimum these devices:

#### iOS Devices
- [ ] **iPhone SE (3rd gen)** - 4.7" small screen
  - [ ] iOS 14.x: Generate → Visualize → Export (PDF) → Settings
  - [ ] Issues found: ____________________
  - [ ] Status: ☐ PASS | ☐ FAIL

- [ ] **iPhone 12** - 6.1" standard screen
  - [ ] iOS 16.x: All flows
  - [ ] Status: ☐ PASS | ☐ FAIL

- [ ] **iPhone 14** - 6.1" notched screen
  - [ ] iOS 17.x: All flows, safe area handling
  - [ ] Status: ☐ PASS | ☐ FAIL

#### Android Devices
- [ ] **Pixel 5a** - 6.0" standard screen
  - [ ] Android 13: All flows
  - [ ] Status: ☐ PASS | ☐ FAIL

- [ ] **Samsung A10** - Low-end device
  - [ ] Android 12: Performance validation (may show frame drops - acceptable if < 5 frames/s)
  - [ ] Status: ☐ PASS | ☐ FAIL

#### Tablets
- [ ] **iPad Air (4th gen)** - 10.9" tablet
  - [ ] Landscape mode: UI adapts correctly
  - [ ] Full-screen visualization: works as expected
  - [ ] Status: ☐ PASS | ☐ FAIL

- [ ] **Galaxy Tab S7** - 11" tablet
  - [ ] Landscape mode: UI responsive
  - [ ] Status: ☐ PASS | ☐ FAIL

### Device-Specific Issues Log

| Device | OS | Issue | Severity | Action |
|--------|----|----|---|--------|
| | | | | |

---

## Part 7: Error Handling

### Invalid Input Handling

- [ ] **Invalid diameter** (-5): Rejected with clear message: "Diameter must be 0.5-50 cm"
- [ ] **Invalid gauge** (50 sts/10cm): Rejected: "Gauge must be 6-25 stitches per 10cm"
- [ ] **Empty diameter field**: Cannot generate (error shown)
- [ ] **Non-numeric diameter**: Rejected with validation error
- [ ] **Extreme values** (1000cm diameter): Rejected with max value error

### Network Error Handling

- [ ] **No network connection**: Clear error message, can retry after connection restored
- [ ] **Slow network** (5+ seconds): Loading state shown, user can cancel
- [ ] **API timeout**: Clear error: "Server response took too long. Try again."
- [ ] **API error (500)**: Clear error: "Server error. Please try again later."

### Edge Cases

- [ ] **Very small patterns** (1cm diameter): Generates correctly, renders without errors
- [ ] **Very large patterns** (50cm diameter): Generates with reasonable stitch count, doesn't crash
- [ ] **Extreme gauge** (6 sts/10cm): Generates with very small stitches, renders
- [ ] **Pattern with 100+ stitches**: Renders without significant lag

**Status**: ☐ All error cases handled | ☐ Issues found (document below)

---

## Part 8: Final Verification

### App Stability

- [ ] **No crashes** during full test execution
- [ ] **Memory leaks**: Monitor memory usage over 30 minutes of use
  - [ ] Generate 5 patterns sequentially: Memory should not grow > 50MB
  - [ ] No low-memory warnings on iPhone SE

- [ ] **Background behavior**: App handles background/foreground transitions
  - [ ] Send app to background, wait 30s, return to foreground
  - [ ] Pattern state preserved
  - [ ] No visual glitches

### Security & Privacy

- [ ] **No sensitive data** stored in debug logs
- [ ] **API credentials** not exposed in network traffic
- [ ] **User input sanitized**: Test with special characters (©, emoji, <script>)
- [ ] **Pattern DSL** doesn't expose unintended data

### Documentation & Help

- [ ] **User guide** accessible and helpful (if included)
- [ ] **Error messages** are clear and actionable
- [ ] **Empty states** provide guidance
- [ ] **Tooltips** (if implemented) helpful and non-intrusive

---

## Part 9: Sign-Off & Issue Log

### Issues Found During Testing

| Issue ID | Description | Severity | Device | Steps to Reproduce | Status |
|----------|-------------|----------|--------|-------------------|--------|
| | | | | | |
| | | | | | |

**Severity Levels:**
- **P0 (Critical)**: Blocks release, data loss, crash
- **P1 (High)**: Major feature broken, significant UX issue
- **P2 (Medium)**: Minor feature issue, workaround available
- **P3 (Low)**: Polish item, cosmetic issue

---

### Release Readiness Assessment

| Category | Status | Sign-Off |
|----------|--------|----------|
| **Critical Flows** | ☐ All PASS | ☐ QA Lead |
| **Bug Fixes Verified** | ☐ All verified | ☐ Dev Lead |
| **Performance Targets Met** | ☐ Yes | ☐ Perf Lead |
| **Accessibility Compliance** | ☐ WCAG AA | ☐ A11Y Lead |
| **Cross-Device Testing** | ☐ Complete | ☐ QA Lead |
| **No P0 Issues** | ☐ Confirmed | ☐ Release Manager |

### Final Release Sign-Off

#### Product Lead
- Date: _______________
- Sign-Off: ☐ APPROVE RELEASE | ☐ HOLD FOR FIXES
- Comments: ________________________________________________

#### QA Lead
- Date: _______________
- Sign-Off: ☐ APPROVE RELEASE | ☐ HOLD FOR FIXES
- Comments: ________________________________________________

#### Development Lead
- Date: _______________
- Sign-Off: ☐ APPROVE RELEASE | ☐ HOLD FOR FIXES
- Comments: ________________________________________________

#### Release Manager
- Date: _______________
- Sign-Off: ☐ APPROVED FOR RELEASE | ☐ RELEASE BLOCKED
- Comments: ________________________________________________

---

## Quick Reference

### Test Duration Estimates
- **Smoke test** (critical flows only): 1 hour
- **Standard regression test**: 3-4 hours
- **Full comprehensive test** (all platforms): 6+ hours

### What to Test First (Priority Order)
1. FLOW-1: Generate Sphere (happy path)
2. FLOW-2: Export PDF (critical feature)
3. FLOW-3: Round Navigation (core UX)
4. FLOW-4: Settings Persistence (data integrity)
5. FLOW-5: Kid Mode (accessibility for kids)
6. Bug fixes from Sprint 9
7. Performance and accessibility
8. Edge cases and error handling

### Common Issues to Watch For
- Frame drops during round navigation on iPhone SE
- PDF export timeout on slow networks
- Settings not persisting after app force-quit
- VoiceOver not announcing round changes
- Touch targets too small in normal mode
- Text overflow in Kid Mode on small screens

### Quick Test Commands

```bash
# Run automated regression tests (if E2E suite exists)
pnpm --filter mobile test:e2e:regression

# Generate test pattern (sphere 10cm)
# Home → Generate → Sphere (default) → Generate

# Performance profiling (React DevTools)
# Measure frame rate during round navigation
# Target: 60 FPS (acceptable: 50+ FPS on low-end)

# Accessibility check
# Settings → Accessibility Inspector
# Measure contrast ratios and touch target sizes
```

---

## Related Documentation

- [Complete Regression Test Suite (QA-6)](./qa-6-regression-test-suite.md)
- [Sprint 9 Bug Fixes](../../../.claude/progress/knit-wit-phase-4/phase-4-sprint-9-bug-fixes.md)
- [Minor Polish Items (BUG-3)](./polish-items.md)
- [Accessibility Testing Procedures](../accessibility/testing-procedures.md)
- [Performance Analysis Sprint 9](../performance/sprint-9-perf-3-implementation.md)

---

**Regression Checklist Version**: 1.0
**Last Updated**: 2025-11-14
**Ready for MVP Release**: Yes (after all sign-offs)
**Next Review**: Post-release (v1.1 planning)
