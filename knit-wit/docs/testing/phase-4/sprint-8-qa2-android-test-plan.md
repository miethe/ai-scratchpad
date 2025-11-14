# QA-2: Android Smoke Tests - Phase 4 Sprint 8

**Story**: QA-2 - Android Smoke Tests (Pixel 5a, Samsung A10, OnePlus Nord)
**Sprint**: Sprint 8 (Weeks 12-13)
**Effort**: 8 story points
**Owner**: QA Lead
**Status**: Test Plan
**Created**: 2025-11-14

---

## Executive Summary

This test plan validates critical user flows across three Android phone models and multiple Android versions to ensure production readiness. Testing focuses on core functionality, platform-specific behaviors, accessibility compliance, and performance on target devices.

**Scope:**
- 3 devices: Pixel 5a, Samsung Galaxy A10, OnePlus Nord
- 3 OS versions: Android 10, 11, 12, 13
- 5 critical flows (identical to iOS QA-1)
- Accessibility verification per A11Y-1 audit findings

**Success Criteria:**
- All critical flows pass on all device/OS combinations
- Zero P0 (critical) bugs found
- WCAG AA accessibility requirements met
- Android-specific issues documented

---

## Test Matrix

| Device | OS | Generate | Visualize | Export | Kid Mode | Settings | Status |
|--------|----|----|----|----|----|----|--------|
| Pixel 5a | Android 13 | ☐ | ☐ | ☐ | ☐ | ☐ | Pending |
| Pixel 5a | Android 12 | ☐ | ☐ | ☐ | ☐ | ☐ | Pending |
| Samsung A10 | Android 11 | ☐ | ☐ | ☐ | ☐ | ☐ | Pending |
| Samsung A10 | Android 10 | ☐ | ☐ | ☐ | ☐ | ☐ | Pending |
| OnePlus Nord | Android 13 | ☐ | ☐ | ☐ | ☐ | ☐ | Pending |
| OnePlus Nord | Android 12 | ☐ | ☐ | ☐ | ☐ | ☐ | Pending |

**Device Specifications:**

| Model | Screen Size | Processor | RAM | Storage | Release |
|-------|-------------|-----------|-----|---------|---------|
| **Samsung A10** | 6.2" | Exynos 7884B | 2GB | 32GB | 2019 |
| **OnePlus Nord** | 6.44" | Snapdragon 765G | 8GB | 128GB | 2020 |
| **Pixel 5a** | 6.34" | Snapdragon 765G | 6GB | 128GB | 2020 |

**Device Tier Classification:**
- **Low-end**: Samsung A10 (2GB RAM, older processor)
- **Mid-range**: Pixel 5a, OnePlus Nord (6-8GB RAM, modern processors)

---

## Critical Flow Test Cases

### Flow 1: Generate Sphere Pattern (Default Gauge)

**Objective**: Verify pattern generation works across diverse Android devices and versions

#### Test Steps

1. **Open App**
   - [ ] App launches without crashing
   - [ ] Home screen displays correctly
   - [ ] "Generate" button is tappable (minimum 48x48 dp)
   - [ ] Navigation drawer (if present) works correctly
   - [ ] Status bar doesn't cover content

2. **Navigate to Generator**
   - [ ] Tap "Generate" button
   - [ ] Generator screen appears within 500ms
   - [ ] All form fields are visible and scrollable
   - [ ] Back button returns to home
   - [ ] Keyboard appears when tapping text inputs

3. **Select Sphere Shape**
   - [ ] Tap "Shape" selector dropdown
   - [ ] All shapes display in dropdown
   - [ ] "Sphere" is visible and tappable
   - [ ] Dropdown closes after selection
   - [ ] Selected shape displays in field

4. **Set Default Parameters**
   - [ ] Diameter: `10` cm
   - [ ] Gauge: `14/16` sts/rows per 10cm
   - [ ] Units: cm (verify selector)
   - [ ] Terminology: US (verify selector)
   - [ ] No validation errors shown

5. **Generate Pattern**
   - [ ] Tap "Generate" button
   - [ ] Loading indicator appears and animates
   - [ ] Generation completes within 200ms (target)
   - [ ] Success: Visualization screen appears with sphere
   - [ ] No error toasts or crash dialogs
   - [ ] Pattern displays completely

#### Expected Results

- ✓ Pattern generates for all device/OS combinations
- ✓ Generation time < 200ms on Pixel 5a / OnePlus Nord
- ✓ Generation time < 300ms on Samsung A10 (low-end exception)
- ✓ Sphere visualization appears with correct proportions
- ✓ Round count approximately 12-14 for 10cm sphere
- ✓ Stitch count visible for Round 1

#### Pass Criteria

- Mid-range devices: ✓ Generation < 200ms
- Low-end device: ✓ Generation < 300ms
- All devices: ✓ No crashes or error dialogs
- All devices: ✓ Pattern visible and complete

#### Known Issues from Sprint 8 Audit

**PERF-2**: Samsung A10 (2GB RAM) may show slower performance. Current baseline: acceptable (<300ms).

**Memory**: Monitor for out-of-memory errors on Samsung A10 with large patterns. Likely not an issue for standard gauge patterns.

---

### Flow 2: Navigate Visualization (First → Last Round)

**Objective**: Verify smooth round navigation across Android device spectrum

#### Test Steps

1. **Verify Initial State**
   - [ ] Pattern shows Round 1
   - [ ] Stitch count displayed (6 for standard sphere)
   - [ ] SVG visualization renders
   - [ ] Legend shows increase/decrease
   - [ ] Navigation buttons visible (Previous, Next)

2. **Swipe Navigation (Android-specific)**
   - [ ] Swipe right on visualization
   - [ ] Round number should decrement (if implemented)
   - [ ] OR use Previous button
   - [ ] Visualization updates smoothly
   - [ ] No visual artifacts

3. **Forward Navigation**
   - [ ] Tap "Next Round" button or swipe left
   - [ ] Round increments: 1 → 2 → 3 → ...
   - [ ] Response time < 50ms
   - [ ] Visualization updates smoothly
   - [ ] Stitch counts update correctly

4. **Scrubber/Slider Navigation**
   - [ ] Locate round scrubber (horizontal slider)
   - [ ] Drag slider to approximate middle
   - [ ] Visualization jumps to correct round
   - [ ] Round number updates immediately
   - [ ] No stuttering during drag

5. **Jump to Extremes**
   - [ ] Drag scrubber all the way right (last round)
   - [ ] Last round displays correctly
   - [ ] Drag scrubber all the way left (round 1)
   - [ ] Round 1 displays correctly

#### Expected Results

- ✓ All navigation responsive (<50ms)
- ✓ Pixel 5a / OnePlus Nord: 60 FPS during navigation
- ✓ Samsung A10: 45+ FPS acceptable
- ✓ Correct round data displays
- ✓ Stitch counts accurate
- ✓ No visual glitches or flickering

#### Pass Criteria

- Pixel 5a / OnePlus Nord: ✓ 60 FPS sustained
- Samsung A10: ✓ 45+ FPS minimum
- All devices: ✓ <50ms response per tap/swipe
- All devices: ✓ No crashes or ANR (Application Not Responding)

#### Known Issues from Sprint 8 Audit

**PERF-2**: Samsung A10 may experience frame drops due to SVGRenderer rendering all nodes without virtualization. Current state: acceptable for MVP.

**Expected FPS drop**: Samsung A10 may drop to 30-45 FPS on complex patterns (100+ stitches). Standard patterns (30-50 stitches) should maintain 45+ FPS.

---

### Flow 3: Export to PDF

**Objective**: Verify PDF export on Android devices with varying storage capabilities

#### Test Steps

1. **Start with Generated Pattern**
   - [ ] Have a sphere pattern visible
   - [ ] Can be any standard gauge/size

2. **Access Export Menu**
   - [ ] Tap "Export" or menu button
   - [ ] Export options appear (PDF, SVG, JSON)
   - [ ] PDF option tappable
   - [ ] Dialog or bottom sheet displays

3. **Select PDF Export**
   - [ ] Tap "PDF" option
   - [ ] Export dialog appears
   - [ ] File name pre-filled (e.g., "sphere-10cm.pdf")
   - [ ] Save location selected (Downloads folder typical)
   - [ ] Export button enabled

4. **Confirm Export**
   - [ ] Tap "Export" / "Save" button
   - [ ] Loading spinner appears
   - [ ] Export progress shown (if applicable)
   - [ ] Completion notification displayed: "PDF exported successfully"
   - [ ] Time < 3 seconds

5. **Verify File**
   - [ ] Open Files app or Downloads folder
   - [ ] PDF file visible in list
   - [ ] File size reasonable (< 5MB)
   - [ ] Open PDF in viewer
   - [ ] Pattern visualization visible
   - [ ] Instructions legible
   - [ ] No corrupt data

#### Expected Results

- ✓ PDF exports without error
- ✓ Export time < 3 seconds
- ✓ File accessible in Downloads
- ✓ PDF opens and displays correctly
- ✓ No notification spam (single completion notification)

#### Pass Criteria

- Pixel 5a / OnePlus Nord: ✓ Export < 2 seconds
- Samsung A10: ✓ Export < 4 seconds
- All devices: ✓ File saved successfully
- All devices: ✓ PDF readable in standard viewers

#### Known Issues from Sprint 8 Audit

**Storage**: Samsung A10 may have limited storage (32GB). Ensure sufficient space before testing export.

**File Format**: Verify PDF opens in Google Drive, Adobe Reader, Chrome PDF viewer (common Android PDF apps).

---

### Flow 4: Toggle Kid Mode

**Objective**: Verify Kid Mode works identically on Android as iOS

#### Test Steps

1. **Navigate to Settings**
   - [ ] Tap Settings button or menu option
   - [ ] Settings screen opens
   - [ ] All toggles visible (may need scrolling)

2. **Locate Kid Mode Toggle**
   - [ ] Find "Kid Mode" toggle switch
   - [ ] Current state visible (on/off)
   - [ ] Toggle is tappable (48x48 dp minimum)
   - [ ] Label text clear: "Kid Mode"

3. **Enable Kid Mode**
   - [ ] Tap Kid Mode toggle
   - [ ] Toggle visual state changes
   - [ ] UI updates immediately:
     - [ ] Font sizes increase (18px+ body text)
     - [ ] Colors become brighter and more saturated
     - [ ] Touch targets enlarge (56x56 dp minimum)
     - [ ] Simplified copy visible (e.g., "Add Stitches" not "Increase")
     - [ ] Animations appear (if applicable)

4. **Verify Kid Mode Appearance**
   - [ ] Navigate away from Settings
   - [ ] Entire UI reflects Kid Mode
   - [ ] All interactive elements larger
   - [ ] Navigation simplified
   - [ ] Instructions beginner-friendly
   - [ ] Material Design components work correctly

5. **Disable Kid Mode**
   - [ ] Return to Settings
   - [ ] Tap Kid Mode toggle again
   - [ ] Toggle switches off
   - [ ] UI reverts to standard mode:
     - [ ] Font sizes normalize
     - [ ] Colors return to standard palette
     - [ ] Touch targets standard size
     - [ ] Copy reverts to standard terminology

#### Expected Results

- ✓ Kid Mode toggles instantly (< 500ms)
- ✓ All UI elements update correctly
- ✓ No crashes or visual glitches
- ✓ Touch targets meet Kid Mode 56x56 dp minimum
- ✓ Color contrast maintained (WCAG AA minimum)
- ✓ Animations smooth and appropriate

#### Pass Criteria

- All devices: ✓ Toggle responds immediately
- All devices: ✓ UI updates visible within 500ms
- All devices: ✓ Touch targets meet minimums
- All devices: ✓ No accessibility regressions (A11Y-1)

#### Known Issues from Sprint 8 Audit

**A11Y-1**: Kid Mode colors verified for WCAG AA (4.5:1 text contrast). No issues found.

---

### Flow 5: Settings - Terminology & High Contrast

**Objective**: Verify settings toggles and persistence on Android

#### Test Steps

1. **Open Settings**
   - [ ] Settings screen displays
   - [ ] All options visible (scroll if needed)
   - [ ] Settings panel/activity loads cleanly

2. **Change Terminology (US ↔ UK)**
   - [ ] Find "Terminology" option (dropdown or selector)
   - [ ] Current setting displayed
   - [ ] Tap to open selector
   - [ ] Options available: US, UK
   - [ ] Select opposite option
   - [ ] Selector closes and updates

3. **Verify Terminology Change**
   - [ ] Go back to home or open pattern
   - [ ] Generate new pattern or view existing
   - [ ] Instructions now in UK terminology:
     - [ ] "sc" → "dc" (single crochet → double crochet UK equivalent)
     - [ ] All stitch abbreviations updated
   - [ ] Return to Settings

4. **Enable High Contrast Mode**
   - [ ] Find "High Contrast" toggle
   - [ ] Current state visible
   - [ ] Tap toggle to enable
   - [ ] UI updates with enhanced contrast:
     - [ ] Text color intensifies or brightens
     - [ ] Background colors adjust
     - [ ] Focus indicators more prominent
     - [ ] All text meets 7:1+ contrast

5. **Test Persistence**
   - [ ] Tap back/home to leave Settings
   - [ ] Navigate app (change patterns, screens)
   - [ ] Return to Settings
   - [ ] Verify settings still applied:
     - [ ] Terminology still UK (or US if changed back)
     - [ ] High Contrast still enabled
     - [ ] Kid Mode state preserved
   - [ ] Close app completely
   - [ ] Reopen app
   - [ ] All settings should persist

#### Expected Results

- ✓ Settings toggle instantly (<100ms)
- ✓ UI reflects changes immediately
- ✓ High Contrast ≥ 7:1 text contrast
- ✓ Settings persist across activity restarts
- ✓ Settings persist across app close/reopen
- ✓ All functionality works in each setting combination

#### Pass Criteria

- All devices: ✓ Settings toggle instantly
- All devices: ✓ Settings persist after app close
- All devices: ✓ High Contrast contrast ≥ 7:1
- All devices: ✓ Terminology correctly applied
- Samsung A10: ✓ Settings work with limited RAM

#### Known Issues from Sprint 8 Audit

**A11Y-1**: High Contrast verified to meet WCAG AAA (7:1+). No issues.

**Persistence**: SharedPreferences (Android standard) should reliably persist settings. No known issues expected.

---

## Android-Specific Considerations

### System Navigation

- [ ] Back button behavior correct (goes back vs. exits app appropriately)
- [ ] Back button works in all screens
- [ ] System gestures (if enabled) don't interfere
- [ ] Navigation bar doesn't cover content

### Permissions

- [ ] File write permission requested for PDF export (if not using scoped storage)
- [ ] Camera/microphone permissions not requested unnecessarily
- [ ] Storage permissions appropriate
- [ ] Permission dialogs appear only when necessary

### System Features

- [ ] Respects system font size setting (but scales reasonably)
- [ ] Respects system dark mode setting (if implemented)
- [ ] Notification badges work (if implemented)
- [ ] Wake lock behavior appropriate (doesn't keep device awake unnecessarily)

### Material Design

- [ ] Components follow Material 3 design (if using Material library)
- [ ] Ripple effects appear on touch
- [ ] Bottom sheet (if used) behaves correctly
- [ ] Navigation drawer (if present) works properly
- [ ] Floating action buttons (if used) positioned correctly

---

## Accessibility Checkpoints (TalkBack)

### Screen Reader Testing

**Required for All Devices:**

- [ ] Home screen buttons announced with TalkBack
- [ ] "Generate" button: role announced as button
- [ ] Form inputs: labels read before field
- [ ] Dropdown selections announced
- [ ] "Sphere" shape selected via TalkBack navigation
- [ ] Round navigation: "Round 1 of 12" announced
- [ ] Stitch count announced with round change
- [ ] Export dialog navigable with TalkBack
- [ ] PDF export completion announced
- [ ] Kid Mode toggle: state announced (on/off)
- [ ] Settings options properly labeled

### Touch Exploration

- [ ] All interactive elements explorable via touch
- [ ] Reading order follows visual layout
- [ ] No skipped interactive elements
- [ ] Element descriptions clear and concise

### Keyboard Navigation (External Keyboard)

- [ ] All elements reachable via Tab
- [ ] Tab order logical and predictable
- [ ] Shift+Tab navigates backwards
- [ ] Enter/Space activates buttons
- [ ] Escape dismisses dialogs (if supported)

### Touch Target Verification

- [ ] All buttons: 48x48 dp minimum (Android)
- [ ] Form inputs: 48x48 dp minimum
- [ ] Kid Mode targets: 56x56 dp minimum
- [ ] Spacing between targets: 8dp minimum

### Color Contrast

- [ ] Primary text: 4.5:1 (WCAG AA) on standard background
- [ ] High Contrast mode: 7:1+ (WCAG AAA)
- [ ] Error messages: high contrast
- [ ] Focus indicators: 3:1 minimum

### Dynamic Content

- [ ] Toast messages readable
- [ ] Snackbars announced
- [ ] Loading states announced
- [ ] Error dialogs announced
- [ ] Completion messages announced

---

## Test Environment Setup

### Device Preparation

1. **Android Device Configuration:**
   - [ ] Update to target OS version
   - [ ] Connect to test WiFi network
   - [ ] Enable Developer Options: Settings → About → tap Build number 7x
   - [ ] Enable USB Debugging: Settings → Developer Options → USB Debugging
   - [ ] Clear app cache: Settings → Apps → [App Name] → Storage → Clear Cache

2. **App Installation:**
   - [ ] Install test APK using adb or Google Play beta
   - [ ] Verify app version in Settings → Apps → [App Name]
   - [ ] Grant necessary permissions when prompted
   - [ ] Clear app data before starting tests: Settings → Apps → [App Name] → Storage → Clear Data

3. **TalkBack Setup:**
   - [ ] Enable: Settings → Accessibility → TalkBack → On
   - [ ] Enable Volume Key shortcut: Settings → Accessibility → TalkBack → Volume key shortcut
   - [ ] (Optional) Enable TalkBack Tutorial

### Testing Tools

- [ ] Android device (physical or emulator)
- [ ] Android Studio (for Logcat debugging if needed)
- [ ] Android Accessibility Scanner (Play Store)
- [ ] Files app or My Files (to verify PDF export)
- [ ] PDF viewer (Google Drive, Adobe Reader, or native viewer)
- [ ] Screen recording app (to document issues)

---

## Performance Benchmarks

### Generation Time

**Target: < 200ms (p95)**

| Device | Expected | Acceptable |
|--------|----------|-----------|
| Pixel 5a | <120ms | <180ms |
| OnePlus Nord | <120ms | <180ms |
| Samsung A10 | <200ms | <300ms |

### Navigation Time

**Target: < 50ms, 60 FPS (45+ on low-end)**

| Device | Target FPS | Min Acceptable |
|--------|-----------|----------------|
| Pixel 5a | 60 | 55 |
| OnePlus Nord | 60 | 55 |
| Samsung A10 | 60 | 45 |

### Export Time

**Target: < 3 seconds**

| Device | Expected | Acceptable |
|--------|----------|-----------|
| Pixel 5a | <2s | <2.5s |
| OnePlus Nord | <2s | <2.5s |
| Samsung A10 | <3s | <4s |

---

## Bug Severity Levels

| Level | Response | Example |
|-------|----------|---------|
| **P0 (Critical)** | Fix before release | App crash, pattern doesn't generate, export fails completely, ANR |
| **P1 (High)** | Fix before launch | Generation slow (>500ms), FPS below minimum, UI unresponsive, permissions broken |
| **P2 (Medium)** | Fix post-launch | Visual glitch, minor animation stuttering, unclear label |
| **P3 (Low)** | Backlog | Cosmetic issue, edge case scenario |

---

## Test Execution Checklist

### Pre-Test

- [ ] All devices prepared and updated to target OS versions
- [ ] Test APK installed on all devices
- [ ] WiFi connectivity verified
- [ ] Device storage: > 1GB free (for PDF export testing)
- [ ] Test environment documented (device model, OS version, build number)
- [ ] Test start time recorded

### During Test

- [ ] Execute each flow systematically
- [ ] Run through all device/OS combinations
- [ ] Record results in test matrix
- [ ] Screenshot failures with context (include device info)
- [ ] Note platform-specific behavior
- [ ] Time each flow execution
- [ ] Test with TalkBack enabled (separate pass)

### Post-Test

- [ ] Summarize findings and issues
- [ ] Create GitHub issues for failures
- [ ] Categorize by severity (P0, P1, P2, P3)
- [ ] Document known platform-specific limitations
- [ ] Update test matrix with results
- [ ] Generate comprehensive test report

---

## Sign-Off

| Role | Date | Notes |
|------|------|-------|
| QA Lead | ☐ | |
| Backend Lead | ☐ | |
| Product Lead | ☐ | |

**Test Execution Time Estimate**: 4-6 hours (40-60 minutes per flow × 5 flows × 6 device/OS combinations)

---

**Related Documentation:**
- [Phase 4 Plan](../../../project_plans/mvp/phases/phase-4.md)
- [Accessibility Checklist](../../../accessibility/accessibility-checklist.md)
- [Testing Procedures](../../../accessibility/testing-procedures.md)
- [Sprint 8 Performance Analysis](../../../performance/sprint-8-analysis.md)
