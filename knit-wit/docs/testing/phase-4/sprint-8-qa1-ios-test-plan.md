# QA-1: iOS Smoke Tests - Phase 4 Sprint 8

**Story**: QA-1 - iOS Smoke Tests (iPhone 12, 14, SE)
**Sprint**: Sprint 8 (Weeks 12-13)
**Effort**: 8 story points
**Owner**: QA Lead
**Status**: Test Plan
**Created**: 2025-11-14

---

## Executive Summary

This test plan validates critical user flows across three iPhone models and three iOS versions to ensure production readiness. Testing focuses on core functionality, accessibility compliance, and performance on target devices.

**Scope:**
- 3 devices: iPhone 12, 14, SE
- 3 OS versions: iOS 14, 16, 17
- 5 critical flows
- Accessibility verification per A11Y-1 audit findings

**Success Criteria:**
- All critical flows pass on all device/OS combinations
- Zero P0 (critical) bugs found
- WCAG AA accessibility requirements met
- Performance within targets

---

## Test Matrix

| Device | OS | Generate | Visualize | Export | Kid Mode | Settings | Status |
|--------|----|----|----|----|----|----|--------|
| iPhone 12 | iOS 17 | ☐ | ☐ | ☐ | ☐ | ☐ | Pending |
| iPhone 12 | iOS 16 | ☐ | ☐ | ☐ | ☐ | ☐ | Pending |
| iPhone 14 | iOS 17 | ☐ | ☐ | ☐ | ☐ | ☐ | Pending |
| iPhone 14 | iOS 16 | ☐ | ☐ | ☐ | ☐ | ☐ | Pending |
| iPhone SE | iOS 17 | ☐ | ☐ | ☐ | ☐ | ☐ | Pending |
| iPhone SE | iOS 14 | ☐ | ☐ | ☐ | ☐ | ☐ | Pending |

**Device Specifications:**

| Model | Screen Size | Processor | RAM | Storage | Release |
|-------|-------------|-----------|-----|---------|---------|
| **iPhone SE (3rd gen)** | 4.7" | A15 Bionic | 3GB | 64GB | 2022 |
| **iPhone 12** | 6.1" | A14 Bionic | 4GB | 64GB | 2020 |
| **iPhone 14** | 6.1" | A15 Bionic | 6GB | 128GB | 2022 |

---

## Critical Flow Test Cases

### Flow 1: Generate Sphere Pattern (Default Gauge)

**Objective**: Verify pattern generation works across devices with acceptable performance

#### Test Steps

1. **Open App**
   - [ ] App launches without crashing
   - [ ] Home screen displays correctly
   - [ ] "Generate" button is tappable (touch target ≥ 44x44pt)

2. **Navigate to Generator**
   - [ ] Tap "Generate" button
   - [ ] Generator screen appears within 500ms
   - [ ] All form fields are visible
   - [ ] Layout adapts to device screen size

3. **Select Sphere Shape**
   - [ ] Tap "Shape" selector
   - [ ] Dropdown shows all available shapes
   - [ ] "Sphere" option is visible and tappable
   - [ ] Tap "Sphere" to select

4. **Set Default Parameters**
   - [ ] Diameter field shows: `10` (cm)
   - [ ] Gauge preset available: `14/16` (sts/rows per 10cm)
   - [ ] Units selector shows: `cm`
   - [ ] Terminology shows: `US`
   - [ ] Fields validate without errors

5. **Generate Pattern**
   - [ ] Tap "Generate" button
   - [ ] Loading indicator appears
   - [ ] Generation completes within 200ms (target)
   - [ ] Visualization screen appears with sphere pattern
   - [ ] No crashes or error messages

#### Expected Results

- ✓ Pattern generates for all device/OS combinations
- ✓ Generation time < 200ms on all devices
- ✓ Sphere appears with correct proportions
- ✓ Round count matches expected (approximately 12-14 rounds for 10cm sphere)
- ✓ Stitch count visible for Round 1

#### Pass Criteria

- All devices: ✓ Pattern visible within 200ms
- All devices: ✓ No crashes or error modals
- iPhone SE: ✓ Performance acceptable (may be slower, <500ms acceptable)

#### Known Issues from Sprint 8 Audit

**PERF-2 Issue**: Generation may be slow on iPhone SE with complex patterns. Current baseline: acceptable for MVP.

**Expected**: Generation time on iPhone SE up to 250ms for standard sphere is acceptable.

---

### Flow 2: Navigate Visualization (First → Last Round)

**Objective**: Verify round navigation is smooth and performant across devices

#### Test Steps

1. **Start at Round 1**
   - [ ] App shows "Round 1" clearly
   - [ ] Stitch count displayed (should be 6 for standard sphere)
   - [ ] SVG visualization renders
   - [ ] Legend shows increase/decrease indicators

2. **Navigate Forward**
   - [ ] Tap "Next Round" button (or swipe)
   - [ ] Round number increments: 1 → 2
   - [ ] Visualization updates smoothly
   - [ ] Response time < 50ms
   - [ ] No visual glitches or flashing

3. **Navigate to Middle**
   - [ ] Tap round scrubber slider
   - [ ] Drag to approximately middle round
   - [ ] Navigation responds instantly
   - [ ] Correct round displays

4. **Jump to Last Round**
   - [ ] Tap "Last Round" button (if available)
   - [ ] OR drag scrubber to end
   - [ ] Visualization jumps to final round
   - [ ] Correct round number shows
   - [ ] Stitch count and visualization match

5. **Navigate Backwards**
   - [ ] Tap "Previous Round" button repeatedly
   - [ ] Rounds decrement: last → ... → 1
   - [ ] Each navigation smooth (<50ms)
   - [ ] No stuttering or frame drops
   - [ ] All rounds render correctly

#### Expected Results

- ✓ All navigation responsive (<50ms)
- ✓ 60 FPS maintained on iPhone 12/14
- ✓ 45+ FPS on iPhone SE
- ✓ No visual glitches
- ✓ Correct round data displayed

#### Pass Criteria

- iPhone 12/14: ✓ 60 FPS sustained navigation
- iPhone SE: ✓ 45+ FPS, <50ms response time
- All: ✓ No stuttering or frame drops

#### Known Issues from Sprint 8 Audit

**PERF-2**: Frame rate may drop below 60 FPS on iPhone SE due to SVGRenderer rendering all nodes. Current state: acceptable for MVP. Target optimization for Sprint 9.

---

### Flow 3: Export to PDF

**Objective**: Verify PDF export completes successfully with reasonable performance

#### Test Steps

1. **Prepare Pattern**
   - [ ] Have a generated sphere pattern visible
   - [ ] Can be any gauge/size

2. **Navigate to Export**
   - [ ] Tap "Export" button
   - [ ] Export options appear (PDF, SVG, JSON)
   - [ ] All options are tappable

3. **Select PDF Export**
   - [ ] Tap "PDF" option
   - [ ] Export dialog appears
   - [ ] File name is pre-filled (e.g., "sphere-10cm.pdf")
   - [ ] Export button is ready

4. **Confirm Export**
   - [ ] Tap "Export" or "Download"
   - [ ] Loading indicator appears
   - [ ] Success message: "PDF exported successfully"
   - [ ] Progress shows or completes within 3 seconds

5. **Verify File**
   - [ ] File appears in Files app
   - [ ] File size is reasonable (< 5MB for standard pattern)
   - [ ] File is readable in PDF viewer
   - [ ] Pattern visualization is visible in PDF
   - [ ] Instructions are legible

#### Expected Results

- ✓ PDF generated successfully
- ✓ Export time < 3 seconds
- ✓ File size < 5MB
- ✓ PDF readable and complete
- ✓ Success message displayed

#### Pass Criteria

- All devices: ✓ Export completes without error
- iPhone 12/14: ✓ Export < 2 seconds
- iPhone SE: ✓ Export < 4 seconds (acceptable)
- All: ✓ PDF opens and displays correctly

#### Known Issues from Sprint 8 Audit

**PERF-2**: PDF export may take 4-8 seconds on iPhone SE with low memory. Current state: acceptable. No blocking issue.

**Issue**: Memory pressure may cause slowdown. Monitor for crashes.

---

### Flow 4: Toggle Kid Mode

**Objective**: Verify Kid Mode activation and functionality

#### Test Steps

1. **Navigate to Settings**
   - [ ] Tap "Settings" button
   - [ ] Settings screen appears
   - [ ] All options visible

2. **Find Kid Mode Toggle**
   - [ ] Locate "Kid Mode" toggle switch
   - [ ] Current state shows (on/off)
   - [ ] Toggle is tappable (44x44pt minimum)

3. **Enable Kid Mode**
   - [ ] Tap Kid Mode toggle
   - [ ] Toggle switches to "on" state
   - [ ] UI immediately changes:
     - [ ] Font sizes increase
     - [ ] Colors become brighter/more saturated
     - [ ] Touch targets enlarge (56x56pt minimum)
     - [ ] Copy simplifies (e.g., "Add Stitches" instead of "Increase")

4. **Verify Kid Mode UI**
   - [ ] Navigation simplified (fewer options visible)
   - [ ] Instructions use beginner-friendly language
   - [ ] Animations are present and smooth
   - [ ] All buttons clearly visible

5. **Disable Kid Mode**
   - [ ] Tap Kid Mode toggle again
   - [ ] Toggle switches to "off" state
   - [ ] UI reverts to normal mode:
     - [ ] Font sizes return to standard
     - [ ] Colors revert to standard palette
     - [ ] Touch targets normalize
     - [ ] Copy reverts to standard terminology

#### Expected Results

- ✓ Kid Mode toggles instantly
- ✓ All UI changes applied immediately
- ✓ No crashes or visual glitches
- ✓ Touch targets meet Kid Mode minimums (56x56pt)
- ✓ Color contrast maintained (WCAG AA)

#### Pass Criteria

- All devices: ✓ Kid Mode toggles without delay
- All devices: ✓ UI updates correctly
- All devices: ✓ Touch targets meet 56x56pt minimum
- All devices: ✓ Accessibility maintained (A11Y-1 verified)

#### Known Issues from Sprint 8 Audit

**A11Y-1**: Kid Mode colors should be verified for contrast. Current status: colors meet WCAG AA (4.5:1 for text). Verified in audit.

---

### Flow 5: Settings - Terminology & High Contrast

**Objective**: Verify settings persistence and feature toggling

#### Test Steps

1. **Navigate to Settings**
   - [ ] Settings screen visible
   - [ ] All toggles and selectors visible

2. **Toggle Terminology (US ↔ UK)**
   - [ ] Find "Terminology" selector
   - [ ] Current setting shown (US or UK)
   - [ ] Tap selector to change
   - [ ] Available options: US, UK
   - [ ] Select opposite terminology

3. **Verify Terminology Change**
   - [ ] Go back to pattern (or generate new one)
   - [ ] Instructions now show UK terminology:
     - [ ] "sc" → "dc" (single crochet → double crochet equivalent)
     - [ ] "dc" → "tr" (double crochet → treble)
     - [ ] Other stitches translated correctly
   - [ ] Return to Settings

4. **Toggle High Contrast Mode**
   - [ ] Find "High Contrast" toggle
   - [ ] Current state shown (on/off)
   - [ ] Tap to toggle
   - [ ] UI immediately updates with higher contrast:
     - [ ] Text color intensifies
     - [ ] Background colors may brighten/darken
     - [ ] Focus indicators become more prominent
     - [ ] All text should meet 7:1+ contrast (enhanced)

5. **Verify Persistence**
   - [ ] Close app completely
   - [ ] Reopen app
   - [ ] Settings should be preserved:
     - [ ] Terminology setting saved
     - [ ] High Contrast setting saved
     - [ ] Kid Mode setting saved (if applicable)

#### Expected Results

- ✓ Settings toggle instantly
- ✓ UI updates reflect setting changes
- ✓ Settings persist across app restarts
- ✓ High Contrast meets or exceeds 7:1 contrast
- ✓ Terminology translations correct

#### Pass Criteria

- All devices: ✓ Settings toggle without delay
- All devices: ✓ Settings persist after app restart
- All devices: ✓ High Contrast contrast ratio ≥ 7:1
- All devices: ✓ Terminology correctly translated

#### Known Issues from Sprint 8 Audit

**A11Y-1**: High Contrast mode verified. Current implementation meets WCAG AAA for text (7:1+).

**Note**: Settings may not persist if device runs out of storage. Expected: iOS typically has sufficient storage.

---

## Accessibility Checkpoints

### Screen Reader Testing (VoiceOver)

**Required for All Devices:**

- [ ] Home screen buttons announced correctly
- [ ] "Generate" → announced as button, clear label
- [ ] Form inputs have associated labels
- [ ] "Sphere" shape selected via VoiceOver
- [ ] Round navigation announced: "Round 1 of 12"
- [ ] Stitch count announced with round change
- [ ] Export dialog fully navigable
- [ ] Kid Mode toggle announces state: "on" or "off"
- [ ] Settings options labeled clearly

**Navigation Order Check:**
- [ ] Reading order matches visual layout
- [ ] No skipped interactive elements
- [ ] Focus moves logically through screens

### Keyboard Navigation

- [ ] All interactive elements reachable via Tab
- [ ] Focus indicator visible (minimum 2px)
- [ ] Tab order is logical
- [ ] Escape dismisses modals/dialogs
- [ ] Return/Space activates buttons

### Touch Target Verification

- [ ] All buttons: 44x44pt minimum
- [ ] Form inputs: 44x44pt minimum
- [ ] Kid Mode targets: 56x56pt minimum
- [ ] Spacing between targets: 8pt minimum

### Color Contrast

- [ ] Primary text: 4.5:1 (WCAG AA)
- [ ] High Contrast mode: 7:1+ (WCAG AAA)
- [ ] Error messages: 7.2:1
- [ ] Focus indicators: 3:1 minimum

### Dynamic Content Announcements

- [ ] Pattern generation completion announced
- [ ] Round changes announced
- [ ] Settings changes confirmed
- [ ] Error messages announced
- [ ] Export completion announced

---

## Test Environment Setup

### Device Preparation

1. **iOS Device Configuration:**
   - [ ] Update to target OS version
   - [ ] Enable Developer Mode (if iOS 16+)
   - [ ] Connect to test network (WiFi)
   - [ ] Clear app cache before first test
   - [ ] Enable VoiceOver for accessibility testing

2. **App Installation:**
   - [ ] Install test build (Testflight or direct)
   - [ ] Clear app data before starting
   - [ ] Verify app version in Settings

3. **VoiceOver Setup:**
   - [ ] Enable: Settings → Accessibility → VoiceOver → On
   - [ ] Enable Practice Mode: Settings → Accessibility → VoiceOver → VoiceOver Practice
   - [ ] Configure shortcut: Settings → Accessibility → Accessibility Shortcut → VoiceOver

### Testing Tools

- [ ] iPhone device (physical or simulator)
- [ ] Xcode Accessibility Inspector (for deeper debugging)
- [ ] Color Contrast Analyzer app (if needed)
- [ ] Files app (to verify PDF export)
- [ ] Screen recorder (to document issues)

---

## Performance Benchmarks

### Generation Time

**Target: < 200ms (p95)**

| Device | Expected | Acceptable |
|--------|----------|-----------|
| iPhone 14 | <100ms | <150ms |
| iPhone 12 | <120ms | <180ms |
| iPhone SE | <150ms | <200ms |

### Navigation Time

**Target: < 50ms response time, 60 FPS (45+ on SE)**

| Device | Target FPS | Min Acceptable |
|--------|-----------|----------------|
| iPhone 14 | 60 | 60 |
| iPhone 12 | 60 | 55 |
| iPhone SE | 60 | 45 |

### Export Time

**Target: < 3 seconds**

| Device | Expected | Acceptable |
|--------|----------|-----------|
| iPhone 14 | <2s | <2.5s |
| iPhone 12 | <2.5s | <3s |
| iPhone SE | <3s | <4s |

---

## Bug Severity Levels

| Level | Response | Example |
|-------|----------|---------|
| **P0 (Critical)** | Fix before release | App crash, pattern doesn't generate, export fails completely |
| **P1 (High)** | Fix before launch | Generation slow (>500ms), FPS drops below target, UI unresponsive |
| **P2 (Medium)** | Fix post-launch | Visual glitch, minor animation issue, unclear label |
| **P3 (Low)** | Backlog | Cosmetic issue, edge case scenario |

---

## Test Execution Checklist

### Pre-Test

- [ ] All devices prepared and updated
- [ ] Test build installed on all devices
- [ ] Internet connectivity verified
- [ ] Test environment documented (OS versions, build number)
- [ ] Test start time recorded

### During Test

- [ ] Run each flow on each device systematically
- [ ] Record results in test matrix
- [ ] Screenshot failures with context
- [ ] Note device-specific behavior
- [ ] Time each flow execution

### Post-Test

- [ ] Summarize findings
- [ ] Create issues for any failures
- [ ] Document known limitations
- [ ] Update test matrix with results
- [ ] Generate test report

---

## Sign-Off

| Role | Date | Notes |
|------|------|-------|
| QA Lead | ☐ | |
| Frontend Lead | ☐ | |
| Product Lead | ☐ | |

**Test Execution Time Estimate**: 4-6 hours per person (40-60 minutes per flow × 5 flows × 6 device/OS combinations)

---

**Related Documentation:**
- [Phase 4 Plan](../../../project_plans/mvp/phases/phase-4.md)
- [Accessibility Checklist](../../../accessibility/accessibility-checklist.md)
- [Testing Procedures](../../../accessibility/testing-procedures.md)
- [Sprint 8 Performance Analysis](../../../performance/sprint-8-analysis.md)
