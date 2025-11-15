# QA-6: Regression Test Suite - Phase 4 Sprint 10

**Story**: QA-6 - Regression Test Suite (All MVP Features)
**Sprint**: Sprint 10 (Weeks 14-15)
**Effort**: 8 story points
**Owner**: QA Lead
**Status**: Test Plan & Matrix
**Created**: 2025-11-14

---

## Executive Summary

This document defines the comprehensive regression test suite covering all features developed across Phases 0-3 of the Knit-Wit MVP. The regression suite ensures that new features, bug fixes, and refactoring do not break existing functionality.

**Scope:**
- Complete test matrix across all MVP features
- Test cases for each feature with acceptance criteria
- Regression test execution schedule
- Integration with CI/CD pipeline
- Known issues and workarounds

**Success Criteria:**
- All regression tests documented and actionable
- Tests can be executed manually and automatically
- Nightly test execution in CI completes in < 45 minutes
- Pre-release regression testing takes 4-6 hours
- All P0 and P1 issues resolved before release

---

## Part 1: Feature Inventory (Phases 0-3)

### Phase 0: Core Foundation
- **P0-F1**: Application bootstrap and initialization
- **P0-F2**: Navigation between Home, Generate, Visualize, Export, Settings screens
- **P0-F3**: React Native/Expo setup and mobile deployment

### Phase 1: Pattern Generation (MVP Core)
- **P1-F1**: Sphere generation with gauge calculations
- **P1-F2**: Cylinder generation with parametric dimensions
- **P1-F3**: Cone/tapered shape generation
- **P1-F4**: Pattern DSL v0.1 generation and validation
- **P1-F5**: Gauge and yardage calculations
- **P1-F6**: US/UK terminology translation

### Phase 2: Interactive Visualization
- **P2-F1**: SVG circle visualization (sphere structure)
- **P2-F2**: Round-by-round navigation (previous/next/scrubber)
- **P2-F3**: Stitch count and round metadata display
- **P2-F4**: Increase/decrease highlighting
- **P2-F5**: Tooltip hover information
- **P2-F6**: Full-screen visualization mode

### Phase 3: Multi-Format Export & Accessibility
- **P3-F1**: PDF export with pattern instructions
- **P3-F2**: SVG export (raw visualization)
- **P3-F3**: JSON export (Pattern DSL format)
- **P3-F4**: PNG export (screenshot of pattern)
- **P3-F5**: Kid Mode (simplified UI and copy)
- **P3-F6**: High Contrast mode (accessibility)
- **P3-F7**: Settings persistence (local storage)
- **P3-F8**: WCAG AA accessibility compliance
- **P3-F9**: VoiceOver/TalkBack support

---

## Part 2: Complete Regression Test Matrix

### Test Coverage by Feature Area

| Feature | Smoke Test | Functional Test | Accessibility Test | Performance Test | Regression Test |
|---------|-----------|-----------------|-------------------|-----------------|-----------------|
| Pattern Generation | ✓ | ✓ | ✓ | ✓ | ✓ |
| Visualization | ✓ | ✓ | ✓ | ✓ | ✓ |
| Export (Multi-format) | ✓ | ✓ | ✓ | ✓ | ✓ |
| Kid Mode | ✓ | ✓ | ✓ | — | ✓ |
| Settings & Persistence | ✓ | ✓ | ✓ | — | ✓ |
| Accessibility Features | — | ✓ | ✓ | — | ✓ |
| Error Handling | — | ✓ | — | — | ✓ |
| Network & API | — | ✓ | — | ✓ | ✓ |

---

## Part 3: Detailed Regression Test Cases

### Feature Group 1: Pattern Generation

#### Test Case RG-1.1: Sphere Generation with Default Parameters

**Test ID**: RG-1.1
**Feature**: P1-F1, P1-F5 (Sphere Generation, Gauge Calculation)
**Priority**: P0 (Critical)
**Platforms**: iOS, Android, Tablet

**Preconditions:**
- App installed and running
- Home screen visible
- No patterns currently loaded

**Steps:**
1. Tap "Generate" button on home screen
2. Verify Generator screen loads (< 500ms)
3. Verify "Sphere" is pre-selected
4. Verify default parameters displayed:
   - Diameter: 10 cm
   - Gauge: 14 sts / 16 rows per 10cm
   - Units: cm
   - Terminology: US
5. Tap "Generate" button
6. Wait for loading indicator to clear
7. Verify pattern generated (< 200ms server-side, < 500ms total)
8. Verify Visualization screen displays

**Expected Results:**
- Sphere pattern appears with 12-14 rounds
- Round 1 shows 6 stitches (magic ring)
- Rounds increment logically
- SVG visualization displays sphere shape
- No error messages shown

**Pass Criteria:**
- Pattern visible within 500ms
- No crashes or error dialogs
- Stitch count matches expected values
- Generation time logged for performance tracking

**Execution**: Manual + Automated (E2E test)
**Frequency**: Every PR (automated), Weekly (manual)

---

#### Test Case RG-1.2: Cylinder Generation with Custom Gauge

**Test ID**: RG-1.2
**Feature**: P1-F2, P1-F5 (Cylinder Generation, Gauge)
**Priority**: P1 (High)
**Platforms**: iOS, Android

**Preconditions:**
- Home screen displayed
- Generator accessible

**Steps:**
1. Navigate to Generator
2. Select "Cylinder" from shape dropdown
3. Set diameter: 8 cm
4. Set gauge: 12 sts / 14 rows per 10cm
5. Verify parameters accepted (no validation errors)
6. Tap "Generate"
7. Verify cylinder pattern generated
8. Verify visual structure shows even circumference

**Expected Results:**
- Cylinder with 8cm diameter created
- Custom gauge applied correctly
- Yardage calculation reflects custom gauge
- Pattern structure looks cylindrical (even width across rounds)

**Pass Criteria:**
- Pattern generated successfully
- Custom gauge visible in pattern metadata
- No gauge-related errors

**Known Issues:**
- None currently documented

**Execution**: Manual + Automated
**Frequency**: Per Sprint

---

#### Test Case RG-1.3: Cone Generation with Tapering

**Test ID**: RG-1.3
**Feature**: P1-F3, P1-F5 (Cone Generation, Gauge)
**Priority**: P1 (High)
**Platforms**: iOS, Android

**Preconditions:**
- Generator screen accessible

**Steps:**
1. Navigate to Generator
2. Select "Cone" shape
3. Set diameter: 6 cm
4. Set height: 10 cm (if applicable)
5. Set gauge: standard (14/16)
6. Tap "Generate"
7. Verify cone pattern generated with decreases
8. Verify tapered structure (getting narrower toward point)

**Expected Results:**
- Cone pattern with proper decrease distribution
- Tapered shape visible in visualization
- Pattern DSL shows increase then decrease phases

**Pass Criteria:**
- Cone structure correct (widening then narrowing)
- No crashes during generation
- Decrease operations present and valid

**Execution**: Manual + Automated
**Frequency**: Per Sprint

---

#### Test Case RG-1.4: Invalid Gauge Rejection

**Test ID**: RG-1.4
**Feature**: P1-F5 (Gauge Validation)
**Priority**: P1 (High)
**Platforms**: All

**Preconditions:**
- Generator screen open

**Steps:**
1. Set gauge to invalid value: "50/50" (unreasonably high)
2. Tap "Generate"
3. Verify error message displayed
4. Verify pattern NOT generated
5. Verify error message readable and actionable

**Expected Results:**
- Error dialog appears: "Gauge values must be between 6 and 25 sts/rows per 10cm"
- No generation attempt made
- User can correct and try again

**Pass Criteria:**
- Error prevents invalid pattern generation
- Message is clear to user
- User can return and retry

**Execution**: Manual + Automated
**Frequency**: Per Sprint

---

#### Test Case RG-1.5: Pattern DSL Validation

**Test ID**: RG-1.5
**Feature**: P1-F4 (Pattern DSL)
**Priority**: P0 (Critical)
**Platforms**: All

**Preconditions:**
- Pattern generated and ready for export/visualization

**Steps:**
1. Export pattern as JSON
2. Parse JSON and verify structure
3. Verify required fields present:
   - meta (version, units, terms, stitch, gauge)
   - object (type, params)
   - rounds (array of rounds with operations)
   - materials (yarn_weight, hook_size_mm, yardage_estimate)
4. Verify round operations are valid (MR, sc, inc, dec, etc.)

**Expected Results:**
- JSON is valid and well-formed
- All required fields present
- No malformed operations
- DSL version correct (0.1)

**Pass Criteria:**
- JSON parses without errors
- All required sections present
- Operations match expected stitch types

**Execution**: Automated (JSON schema validation)
**Frequency**: Every generation

---

### Feature Group 2: Interactive Visualization

#### Test Case RG-2.1: Round Navigation - Sequential

**Test ID**: RG-2.1
**Feature**: P2-F2 (Round Navigation)
**Priority**: P0 (Critical)
**Platforms**: All

**Preconditions:**
- Pattern generated and visible
- On Round 1

**Steps:**
1. Verify "Round 1" displayed
2. Tap "Next Round" button
3. Verify display updates to "Round 2" (< 50ms)
4. Verify stitch count updates
5. Repeat for rounds 2 → 3 → last round
6. Tap "Previous Round"
7. Verify round decrements correctly
8. Navigate back to Round 1

**Expected Results:**
- Each round navigation < 50ms
- Round numbers increment/decrement correctly
- Stitch counts match pattern DSL
- No visual glitches or stuttering

**Pass Criteria:**
- Smooth navigation (no frame drops)
- Correct round data displayed
- No crashes

**Execution**: Manual + Automated
**Frequency**: Every PR (automated)

---

#### Test Case RG-2.2: Round Navigation - Scrubber/Slider

**Test ID**: RG-2.2
**Feature**: P2-F2 (Round Navigation)
**Priority**: P1 (High)
**Platforms**: All (especially tablet)

**Preconditions:**
- Pattern visible with scrubber slider

**Steps:**
1. Locate round scrubber (horizontal slider)
2. Drag to middle position
3. Verify correct middle round displays
4. Drag to end position (last round)
5. Verify last round displays
6. Drag to start (Round 1)
7. Verify Round 1 displays

**Expected Results:**
- Smooth scrubber dragging (no stuttering)
- Correct round at each position
- Responsive to touch during drag

**Pass Criteria:**
- Scrubber works smoothly
- Rounds update correctly
- No ANR or jank

**Execution**: Manual (scrubber requires fine touch control)
**Frequency**: Per Sprint

---

#### Test Case RG-2.3: Stitch Highlighting - Increases

**Test ID**: RG-2.3
**Feature**: P2-F4 (Increase/Decrease Highlighting)
**Priority**: P1 (High)
**Platforms**: All

**Preconditions:**
- Pattern with visible increases (e.g., Sphere Round 2+)

**Steps:**
1. Navigate to round with increases
2. Verify stitch positions highlighted differently for increases
3. Verify legend shows increase indicator
4. Verify color contrast meets WCAG AA (4.5:1)
5. Navigate to next round
6. Verify highlighting updated correctly

**Expected Results:**
- Increases highlighted visually distinct
- Legend clearly indicates increase type
- Color contrast sufficient for visibility

**Pass Criteria:**
- Highlights visible and consistent
- Accessible color choices

**Execution**: Manual + Automated (color contrast check)
**Frequency**: Per Sprint

---

#### Test Case RG-2.4: Tooltip Information Display

**Test ID**: RG-2.4
**Feature**: P2-F5 (Tooltip Hover/Tap Info)
**Priority**: P2 (Medium)
**Platforms**: All

**Preconditions:**
- Pattern visualized

**Steps:**
1. (iOS) Long-press on a stitch node
2. (Android) Long-press on a stitch node
3. Verify tooltip appears with stitch info:
   - Operation (sc, inc, dec, etc.)
   - Position in round
   - Stitch count total
4. Verify tooltip is readable
5. Dismiss tooltip

**Expected Results:**
- Tooltip appears with accurate information
- Tooltip readable and non-intrusive
- Dismisses on tap elsewhere

**Pass Criteria:**
- Tooltip information correct
- Readable and accessible

**Execution**: Manual
**Frequency**: Per Sprint

---

#### Test Case RG-2.5: Full-Screen Visualization

**Test ID**: RG-2.5
**Feature**: P2-F6 (Full-Screen Mode)
**Priority**: P2 (Medium)
**Platforms**: All

**Preconditions:**
- Pattern visible in normal view

**Steps:**
1. Tap full-screen button (if available)
2. Verify pattern expands to full screen
3. Verify controls minimized or hidden
4. Verify visualization still responsive
5. Tap exit full-screen
6. Verify normal layout restored

**Expected Results:**
- Full-screen provides larger view
- Visualization quality maintained
- Controls still accessible for navigation

**Pass Criteria:**
- Full-screen works correctly
- Exit restores proper layout

**Execution**: Manual
**Frequency**: Per Sprint

---

### Feature Group 3: Multi-Format Export

#### Test Case RG-3.1: PDF Export - Basic

**Test ID**: RG-3.1
**Feature**: P3-F1 (PDF Export)
**Priority**: P0 (Critical)
**Platforms**: iOS, Android

**Preconditions:**
- Pattern generated and visible
- Sufficient device storage (> 50MB free)

**Steps:**
1. Tap "Export" button
2. Verify export options appear (PDF, SVG, JSON, PNG)
3. Select "PDF" option
4. Verify export dialog shows with defaults
5. Tap "Export" / "Download"
6. Verify loading indicator appears
7. Wait for export to complete (< 3s)
8. Verify success message displayed
9. Open Files app
10. Verify PDF file exists in Downloads
11. Open PDF in viewer
12. Verify pattern visible and complete
13. Verify instructions text readable

**Expected Results:**
- PDF exports successfully
- File size < 5MB for standard pattern
- PDF opens and displays correctly
- Pattern diagram and instructions visible
- No corrupt or missing pages

**Pass Criteria:**
- Export completes without error
- File accessible and readable
- Content complete and correct

**Execution**: Manual + Automated (E2E)
**Frequency**: Every PR (automated smoke), Weekly (manual complete test)

---

#### Test Case RG-3.2: PDF Export - Include Diagram Option

**Test ID**: RG-3.2
**Feature**: P3-F1 (PDF Export with Options)
**Priority**: P1 (High)
**Platforms**: iOS, Android

**Preconditions:**
- Pattern ready for export

**Steps:**
1. Start PDF export process
2. Verify options available (if implemented):
   - Include diagram
   - Include instructions
   - Paper size (A4, Letter, etc.)
3. Toggle "Include Diagram" option
4. Complete export
5. Open PDF
6. If diagram included: verify SVG visualization present
7. If diagram excluded: verify only text present

**Expected Results:**
- Options respected in exported PDF
- File size appropriate for selected options
- Content matches selected options

**Pass Criteria:**
- Options work correctly
- PDF content reflects selection

**Execution**: Manual
**Frequency**: Per Sprint

---

#### Test Case RG-3.3: SVG Export - File Format

**Test ID**: RG-3.3
**Feature**: P3-F2 (SVG Export)
**Priority**: P1 (High)
**Platforms**: iOS, Android

**Preconditions:**
- Pattern visible

**Steps:**
1. Select "SVG" export option
2. Confirm export
3. Verify file saved as .svg
4. Open SVG file in viewer (Chrome, etc.)
5. Verify visualization displays correctly
6. Verify interactive elements work (if applicable)

**Expected Results:**
- SVG file valid and well-formed
- Visualization matches on-screen version
- File size reasonable (< 500KB)

**Pass Criteria:**
- SVG exports successfully
- File opens in standard SVG viewers
- Content matches visualization

**Execution**: Manual + Automated
**Frequency**: Per Sprint

---

#### Test Case RG-3.4: JSON Export - Pattern DSL

**Test ID**: RG-3.4
**Feature**: P3-F3 (JSON Export)
**Priority**: P1 (High)
**Platforms**: All

**Preconditions:**
- Pattern generated

**Steps:**
1. Select "JSON" export option
2. Complete export
3. Open JSON file in text editor
4. Verify JSON is valid (can be parsed)
5. Verify structure matches DSL v0.1 schema
6. Verify all fields present:
   - meta.version = "0.1"
   - object.type = shape name
   - rounds array populated
   - operations valid
7. Copy JSON content
8. (Optional) Validate against schema

**Expected Results:**
- JSON file valid and well-formed
- Structure matches DSL specification
- All required fields present
- Can be parsed and validated

**Pass Criteria:**
- JSON valid and complete
- Matches DSL schema
- Can be re-imported (future feature)

**Execution**: Automated (JSON schema validation)
**Frequency**: Every generation

---

#### Test Case RG-3.5: PNG Export - Screenshot

**Test ID**: RG-3.5
**Feature**: P3-F4 (PNG Export)
**Priority**: P2 (Medium)
**Platforms**: iOS, Android

**Preconditions:**
- Pattern visible

**Steps:**
1. Select "PNG" export option
2. Confirm export
3. Verify file saved as .png
4. Open PNG in image viewer
5. Verify visualization screenshot captured
6. Verify image quality good (not pixelated)
7. Verify aspect ratio correct

**Expected Results:**
- PNG file created successfully
- Image shows pattern visualization
- Quality appropriate for screen resolution
- File size reasonable

**Pass Criteria:**
- PNG exports without error
- Image quality acceptable
- File opens in image viewers

**Execution**: Manual
**Frequency**: Per Sprint

---

### Feature Group 4: Kid Mode

#### Test Case RG-4.1: Kid Mode Toggle - Enable/Disable

**Test ID**: RG-4.1
**Feature**: P3-F5 (Kid Mode)
**Priority**: P1 (High)
**Platforms**: All

**Preconditions:**
- Settings screen accessible
- Kid Mode currently disabled

**Steps:**
1. Navigate to Settings
2. Find "Kid Mode" toggle
3. Tap toggle to enable
4. Verify UI immediately changes:
   - Font sizes increase (18px+ minimum)
   - Colors become brighter/more saturated
   - All buttons and touch targets enlarge (56x56pt minimum)
5. Verify toggle shows "ON" state
6. Tap toggle again to disable
7. Verify UI reverts to standard:
   - Font sizes return to normal
   - Colors revert
   - Touch targets shrink back

**Expected Results:**
- Immediate UI updates when toggling
- All elements properly sized
- Toggle state clearly visible
- No lag or visual glitches

**Pass Criteria:**
- Kid Mode toggles smoothly
- All UI changes applied consistently
- Touch targets meet Kid Mode requirements

**Execution**: Manual + Automated
**Frequency**: Per Sprint

---

#### Test Case RG-4.2: Kid Mode - Terminology

**Test ID**: RG-4.2
**Feature**: P3-F5 (Kid Mode, Beginner Copy)
**Priority**: P2 (Medium)
**Platforms**: All

**Preconditions:**
- Kid Mode enabled
- Pattern generated

**Steps:**
1. Generate a pattern with Kid Mode on
2. View Visualization screen
3. Verify instructions use simplified language:
   - "Add Stitches" instead of "Increase"
   - "Remove Stitches" instead of "Decrease"
   - Clear, beginner-friendly explanations
4. Verify tooltip text simplified
5. Disable Kid Mode
6. Verify copy reverts to standard terminology

**Expected Results:**
- All text in Kid Mode uses beginner language
- Standard mode shows technical terminology
- Terminology switches correctly when toggling

**Pass Criteria:**
- Kid Mode copy is child-friendly and clear
- Standard terminology present in normal mode

**Execution**: Manual
**Frequency**: Per Sprint

---

#### Test Case RG-4.3: Kid Mode - Touch Targets

**Test ID**: RG-4.3
**Feature**: P3-F5 (Kid Mode, Touch Accessibility)
**Priority**: P1 (High)
**Platforms**: All

**Preconditions:**
- Kid Mode enabled

**Steps:**
1. Measure all interactive elements using Accessibility Inspector
2. Verify all buttons meet 56x56pt minimum (iOS) or 56x56 dp (Android)
3. Verify spacing between targets at least 8pt/dp
4. Verify touch areas properly respond to touch
5. Test on actual device (not just simulator)

**Expected Results:**
- All touch targets meet or exceed minimum size
- Spacing prevents accidental taps
- Touch response is accurate

**Pass Criteria:**
- All targets ≥ 56x56pt/dp in Kid Mode
- Spacing adequate to prevent misses

**Execution**: Manual (requires measurement tools)
**Frequency**: Per Sprint

---

### Feature Group 5: Settings & Persistence

#### Test Case RG-5.1: Settings Persistence - App Restart

**Test ID**: RG-5.1
**Feature**: P3-F7 (Settings Persistence)
**Priority**: P1 (High)
**Platforms**: All

**Preconditions:**
- Settings accessible

**Steps:**
1. Navigate to Settings
2. Change "Terminology" to "UK"
3. Enable "Kid Mode"
4. Enable "High Contrast"
5. Exit Settings and navigate app
6. Close app completely (force quit)
7. Reopen app
8. Navigate to Settings
9. Verify all settings persisted:
   - Terminology: UK (not US)
   - Kid Mode: ON
   - High Contrast: ON

**Expected Results:**
- All settings preserved after app restart
- Settings apply to app on reopen
- No resets to defaults

**Pass Criteria:**
- Settings survive app close/reopen
- All toggles and selections persist

**Execution**: Manual + Automated
**Frequency**: Per Sprint

---

#### Test Case RG-5.2: Terminology Change - Pattern Update

**Test ID**: RG-5.2
**Feature**: P3-F7, P1-F6 (Settings, Terminology Translation)
**Priority**: P1 (High)
**Platforms**: All

**Preconditions:**
- Pattern generated with US terminology

**Steps:**
1. View pattern with US terminology (sc, inc, dec, etc.)
2. Navigate to Settings
3. Change "Terminology" to "UK"
4. Return to pattern
5. Verify instructions now show UK terminology:
   - "sc" → "dc" (UK equivalent)
   - "inc" → "inc" (same)
   - "dec" → "dec" (same)
   - All stitch abbreviations translated
6. Change back to US
7. Verify terminology reverts

**Expected Results:**
- Terminology change immediately reflected in pattern
- Correct UK stitch definitions used
- Change persists across app sessions

**Pass Criteria:**
- Terminology translation accurate
- UI reflects setting immediately

**Execution**: Manual + Automated
**Frequency**: Per Sprint

---

#### Test Case RG-5.3: High Contrast Mode - Contrast Ratio Verification

**Test ID**: RG-5.3
**Feature**: P3-F6 (High Contrast Mode)
**Priority**: P1 (High)
**Platforms**: All

**Preconditions:**
- Settings accessible

**Steps:**
1. Enable "High Contrast" mode
2. Take screenshots of each screen
3. Use Accessibility Inspector or Color Contrast Analyzer
4. Measure contrast ratios for:
   - Primary text on backgrounds: should be ≥ 7:1 (WCAG AAA)
   - Interactive elements: ≥ 3:1 minimum
   - Borders/focus indicators: ≥ 3:1
5. Verify all critical elements meet WCAG AAA (7:1)
6. Disable High Contrast
7. Verify contrast drops to WCAG AA (4.5:1) for text

**Expected Results:**
- High Contrast mode: all text ≥ 7:1
- Normal mode: text ≥ 4.5:1
- Sufficient for users with low vision

**Pass Criteria:**
- High Contrast meets WCAG AAA (7:1+)
- Normal mode meets WCAG AA (4.5:1+)

**Execution**: Manual (requires contrast measurement tools)
**Frequency**: Per Sprint

---

### Feature Group 6: Accessibility Features

#### Test Case RG-6.1: VoiceOver Navigation (iOS)

**Test ID**: RG-6.1
**Feature**: P3-F8, P3-F9 (Accessibility, VoiceOver)
**Priority**: P1 (High)
**Platforms**: iOS only

**Preconditions:**
- VoiceOver enabled
- Home screen visible

**Steps:**
1. Enable VoiceOver (Settings → Accessibility → VoiceOver → On)
2. Use two-finger swipe to start VoiceOver gesture
3. Navigate each screen using VoiceOver gestures:
   - One finger swipe right/left to move between elements
   - Two finger double-tap to activate
4. Verify announced labels:
   - Home screen: "Generate button", "Settings button"
   - Generator: "Shape selector, Sphere selected", "Diameter input"
   - Visualization: "Round 1 of 12", "Stitch count: 6"
   - Export: "PDF option", "SVG option"
5. Verify reading order follows visual layout
6. Test all major interactions via VoiceOver

**Expected Results:**
- All elements announced clearly
- Labels are meaningful and descriptive
- Reading order is logical
- All major flows navigable via VoiceOver

**Pass Criteria:**
- Complete VoiceOver navigation possible
- All labels present and meaningful
- No skipped interactive elements

**Execution**: Manual (VoiceOver requires human testing)
**Frequency**: Per Sprint

---

#### Test Case RG-6.2: TalkBack Navigation (Android)

**Test ID**: RG-6.2
**Feature**: P3-F8, P3-F9 (Accessibility, TalkBack)
**Priority**: P1 (High)
**Platforms**: Android only

**Preconditions:**
- TalkBack enabled
- Home screen visible

**Steps:**
1. Enable TalkBack (Settings → Accessibility → TalkBack → On)
2. Navigate using TalkBack gestures:
   - Swipe right to next element
   - Swipe left to previous element
   - Double-tap to activate
3. Verify announced information:
   - Button roles announced ("button")
   - Toggles announce state ("on/off")
   - Input fields announce purpose
   - Round navigation announces "Round X of Y"
4. Test all major flows with TalkBack

**Expected Results:**
- All elements announced clearly with TalkBack
- Roles properly communicated
- All interactions accessible
- Reading order logical

**Pass Criteria:**
- Complete TalkBack navigation possible
- All labels present and descriptive
- No inaccessible elements

**Execution**: Manual (TalkBack requires human testing)
**Frequency**: Per Sprint

---

#### Test Case RG-6.3: Keyboard Navigation Support

**Test ID**: RG-6.3
**Feature**: P3-F8, P3-F9 (Accessibility, Keyboard)
**Priority**: P2 (Medium)
**Platforms**: All (with external keyboard)

**Preconditions:**
- External keyboard connected (iPad, Android tablet)
- App running

**Steps:**
1. Connect external keyboard
2. Use Tab key to navigate between elements
3. Verify logical tab order
4. Verify focus indicators visible (minimum 2px)
5. Use Return/Space to activate buttons
6. Use Escape to dismiss modals (if implemented)
7. Test all major flows with keyboard only

**Expected Results:**
- Tab navigation works through all screens
- Focus indicators always visible
- All buttons activate with Return/Space
- Tab order is logical and predictable

**Pass Criteria:**
- Complete keyboard navigation possible
- Focus indicators always visible
- Logical, predictable tab order

**Execution**: Manual (requires external keyboard)
**Frequency**: Per Sprint

---

#### Test Case RG-6.4: Touch Target Size Verification

**Test ID**: RG-6.4
**Feature**: P3-F8, P3-F9 (Accessibility, Touch Targets)
**Priority**: P1 (High)
**Platforms**: All

**Preconditions:**
- App running

**Steps:**
1. Use Accessibility Inspector to measure all interactive elements
2. Verify minimum sizes:
   - Normal mode: 44x44pt (iOS) / 48x48 dp (Android)
   - Kid Mode: 56x56pt (iOS) / 56x56 dp (Android)
3. Verify spacing between targets: minimum 8pt/dp
4. Test touch response accuracy
5. Verify no targets are too small to tap

**Expected Results:**
- All buttons meet or exceed minimum size
- Spacing prevents accidental adjacent taps
- Touch response accurate and reliable

**Pass Criteria:**
- Normal mode: all targets ≥ 44x44 pt/dp
- Kid Mode: all targets ≥ 56x56 pt/dp
- Spacing ≥ 8pt/dp between targets

**Execution**: Manual (requires measurement tools) + Automated (accessibility scanner)
**Frequency**: Per Sprint

---

### Feature Group 7: Error Handling

#### Test Case RG-7.1: Network Error Handling

**Test ID**: RG-7.1
**Feature**: Error Handling, Network Resilience
**Priority**: P2 (Medium)
**Platforms**: All

**Preconditions:**
- App running
- Network available

**Steps:**
1. Enable Airplane Mode (or disable WiFi)
2. Attempt to generate pattern
3. Verify clear error message displayed (if API call needed)
4. Disable Airplane Mode
5. Retry generation
6. Verify pattern generates successfully

**Expected Results:**
- Clear error message on network failure
- User can retry after connection restored
- No crashes or hung app

**Pass Criteria:**
- Error message is user-friendly
- Recovery possible without app restart

**Execution**: Manual
**Frequency**: Per Sprint

---

#### Test Case RG-7.2: Invalid Input Error Messages

**Test ID**: RG-7.2
**Feature**: Error Handling, Input Validation
**Priority**: P2 (Medium)
**Platforms**: All

**Preconditions:**
- Generator screen open

**Steps:**
1. Try invalid diameter: -5
2. Verify error message: "Diameter must be greater than 0"
3. Try invalid diameter: 0
4. Verify error message
5. Try invalid gauge: "abc"
6. Verify error message: "Gauge must be numeric"
7. Try diameter too large: 1000
8. Verify error message: "Maximum diameter is 50cm"

**Expected Results:**
- Clear error for each invalid input
- Prevents invalid pattern generation
- User can correct and retry

**Pass Criteria:**
- All error messages clear and actionable
- Validation prevents bad patterns

**Execution**: Manual + Automated
**Frequency**: Per Sprint

---

#### Test Case RG-7.3: Out-of-Memory Handling

**Test ID**: RG-7.3
**Feature**: Error Handling, Memory Management
**Priority**: P3 (Low)
**Platforms**: iOS (iPhone SE), Android (low-memory devices)

**Preconditions:**
- Device with limited RAM (iPhone SE, Samsung A10)
- App running

**Steps:**
1. Generate very large patterns (extreme parameters)
2. Monitor for memory pressure
3. If out-of-memory condition occurs:
   - Verify app doesn't crash
   - Verify error message displayed
   - Verify user can return to home screen

**Expected Results:**
- App handles memory pressure gracefully
- No crashes even under extreme load
- User can continue using app

**Pass Criteria:**
- No crashes on low-memory devices
- Graceful degradation if needed

**Execution**: Manual (low-priority, test on low-memory devices)
**Frequency**: Per release

---

## Part 4: Regression Test Execution Schedule

### Nightly Automated Tests (GitHub Actions)

**Frequency**: Every night at 2:00 AM UTC
**Duration**: Should complete in < 45 minutes
**Platforms**: iOS (primary), Android (secondary)
**Coverage**: All P0 and P1 flows

**Test Suite:**
- RG-1.1: Sphere Generation (P0)
- RG-1.4: Invalid Gauge Rejection (P1)
- RG-1.5: Pattern DSL Validation (P0)
- RG-2.1: Round Navigation (P0)
- RG-3.1: PDF Export (P0)
- RG-4.1: Kid Mode Toggle (P1)
- RG-5.1: Settings Persistence (P1)

**Expected Result**: All tests pass; notify team if any failure

---

### Pre-Release Regression Testing (Manual)

**Frequency**: Before each release candidate (RC)
**Duration**: 4-6 hours for full manual test
**Platforms**: iOS (iPhone 12, 14, SE), Android (Pixel 5a, Samsung A10), Tablet (iPad Air, Galaxy Tab S7)
**Coverage**: All P0, P1, and P2 flows

**Test Suite**: All test cases in this document

**Success Criteria:**
- All P0 tests pass on all device/OS combinations
- All P1 tests pass on iOS and primary Android device
- All P2 tests pass on at least one device
- No new issues found
- Known issues logged and documented

---

### Sprint-End Regression Testing

**Frequency**: End of each sprint (before sprint demo)
**Duration**: 2-3 hours
**Platforms**: iOS + primary Android device
**Coverage**: All features changed in sprint + P0/P1 core flows

**Test Suite**: Focus on changed features, sample P0/P1 core flows

**Expected Result**: No P0/P1 regressions; log any issues found

---

### Ad-Hoc Regression Testing

**Trigger**:
- After each major bug fix
- After refactoring
- After dependency upgrades
- On request from development team

**Scope**: Affected feature + core flows (P0 minimum)
**Duration**: 30-60 minutes
**Platforms**: Primary platform for issue

---

## Part 5: Known Issues & Workarounds

### PERF-2: SVG Rendering Performance

**Description**: On low-end devices (iPhone SE, Samsung A10), complex patterns (100+ stitches) may show frame drops during round navigation.

**Affected Tests**: RG-2.1, RG-2.2
**Severity**: P2 (affects experience but doesn't break functionality)
**Workaround**: Generate simpler patterns for testing on low-end devices
**Status**: Acceptable for MVP; target optimization for Phase 4 Sprint 11

### A11Y-1: High Contrast Mode Color Selection

**Description**: Some color combinations in High Contrast mode initially didn't meet WCAG AAA (7:1).

**Affected Tests**: RG-5.3, RG-6.3
**Severity**: P1 (accessibility issue)
**Resolution**: Colors updated to meet WCAG AAA; verified in Sprint 8 audit
**Status**: RESOLVED

### Storage-1: Limited Storage on Samsung A10

**Description**: Samsung A10 with 32GB storage may have limited space for testing multiple PDF exports.

**Affected Tests**: RG-3.1, RG-3.2
**Severity**: P3 (environmental issue, not app issue)
**Workaround**: Delete previous test files before running full export tests
**Status**: Documented; not an app bug

---

## Part 6: Regression Test Report Template

### Test Execution Report

**Report Date**: [Date]
**Test Scope**: [Which features/test cases]
**Test Duration**: [Time spent]
**Test Environment**: [Platforms and OS versions tested]
**Build Version**: [App version number]

### Summary

**Total Test Cases**: XX
**Passed**: XX ✓
**Failed**: XX ✗
**Skipped**: XX ○
**Pass Rate**: XX%

**Critical Issues Found**: [Count and severity]
**Known Issues Hit**: [List any known issues encountered]

### Results by Feature Group

| Feature Group | Status | Details |
|---------------|--------|---------|
| Pattern Generation | ✓ PASS | All P0/P1 tests passed |
| Visualization | ✓ PASS | Round navigation smooth on all devices |
| Export | ✗ FAIL | PDF export fails on iOS 14 (see issue #123) |
| Kid Mode | ✓ PASS | All toggles and touch targets verified |
| Settings | ✓ PASS | Persistence verified across app restart |
| Accessibility | ✓ PASS | VoiceOver navigation verified on iOS |
| Error Handling | ✓ PASS | Invalid inputs rejected correctly |

### Issues Found

**Issue #1**: PDF export fails on iOS 14 (REGRESSION)
- Test Case: RG-3.1
- Device: iPhone SE (iOS 14)
- Steps: Generate sphere, tap Export, select PDF, tap Export
- Expected: PDF downloads successfully
- Actual: Error dialog "Export failed"
- Severity: P0
- Status: NEW - requires investigation

### Recommendations

1. Investigate iOS 14 PDF export issue (may be WebKit compatibility)
2. Add PDF export test to nightly CI for iOS variants
3. Verify fix works before next release

### Sign-Off

| Role | Date | Notes |
|------|------|-------|
| QA Lead | ☐ | |
| Product Lead | ☐ | |
| Release Manager | ☐ | |

---

## Related Documentation

- [E2E Framework Setup (QA-5)](./qa-5-e2e-framework-setup.md)
- [Cross-Device Test Report Template (QA-7)](./qa-7-cross-device-test-report-template.md)
- [Phase 4 Sprint 8 iOS Test Plan](./sprint-8-qa1-ios-test-plan.md)
- [Phase 4 Sprint 8 Android Test Plan](./sprint-8-qa2-android-test-plan.md)
- [Testing Strategy](../../../project_plans/mvp/supporting-docs/testing-strategy.md)
- [Knit-Wit CLAUDE.md](../../../CLAUDE.md)

---

**Regression Test Suite Version**: 1.0
**Last Updated**: 2025-11-14
**Next Review**: Sprint 11 (post-release)
