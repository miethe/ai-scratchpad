# QA-3: Tablet Testing - Phase 4 Sprint 8

**Story**: QA-3 - Tablet Testing (iPad Air 4th gen, Samsung Galaxy Tab S7)
**Sprint**: Sprint 8 (Weeks 12-13)
**Effort**: 5 story points
**Owner**: QA Engineer
**Status**: Test Plan
**Created**: 2025-11-14

---

## Executive Summary

This test plan validates critical user flows on tablet devices in both portrait and landscape orientations. Tablet testing ensures responsive layout, appropriate touch targets, and accessibility features work correctly on larger screens.

**Scope:**
- 2 tablet devices: iPad Air (4th gen), Samsung Galaxy Tab S7
- 2 OS versions: iPadOS 17, Android 11
- 2 orientations: Portrait, Landscape
- 5 critical flows (same as phone testing)
- Touch target verification for tablet-specific requirements
- Landscape orientation-specific behavior

**Success Criteria:**
- All flows pass in portrait and landscape
- Layout responsiveness verified
- Touch targets appropriate for tablet use
- Accessibility maintained on larger screens
- No orientation-change crashes

---

## Test Matrix

### iPad Air (4th gen)

| Orientation | Generate | Visualize | Export | Kid Mode | Settings | Portrait | Landscape |
|-------------|----------|-----------|--------|----------|----------|----------|-----------|
| **Portrait** | ☐ | ☐ | ☐ | ☐ | ☐ | Pending | N/A |
| **Landscape** | ☐ | ☐ | ☐ | ☐ | ☐ | N/A | Pending |

### Samsung Galaxy Tab S7

| Orientation | Generate | Visualize | Export | Kid Mode | Settings | Portrait | Landscape |
|-------------|----------|-----------|--------|----------|----------|----------|-----------|
| **Portrait** | ☐ | ☐ | ☐ | ☐ | ☐ | Pending | N/A |
| **Landscape** | ☐ | ☐ | ☐ | ☐ | ☐ | N/A | Pending |

**Device Specifications:**

| Model | Screen Size | Processor | RAM | OS | Release |
|-------|-------------|-----------|-----|-------|---------|
| **iPad Air (4th gen)** | 10.9" | A14 Bionic | 4GB | iPadOS 15-17 | 2022 |
| **Samsung Tab S7** | 11.0" | Snapdragon 865 | 6GB | Android 11-13 | 2020 |

---

## Layout & Responsiveness

### Portrait Orientation

#### Responsive Layout Checklist

- [ ] Content fills screen appropriately (not wasted white space)
- [ ] Text is readable at standard zoom (not too small)
- [ ] Touch targets remain minimum size (44pt iOS / 48dp Android)
- [ ] Forms don't require excessive scrolling
- [ ] Navigation accessible (doesn't scroll off)
- [ ] Bottom navigation (if present) not cut off
- [ ] Keyboard doesn't cover important content
- [ ] Landscape buttons/text don't appear cramped

#### Screen-Specific Tests

**Home Screen:**
- [ ] Logo/branding centered and appropriately sized
- [ ] "Generate" button centered and tappable
- [ ] Welcome text readable
- [ ] Navigation buttons spaced appropriately

**Generator Screen:**
- [ ] Form fields visible without excessive scrolling
- [ ] Labels visible above inputs
- [ ] "Generate" button at bottom remains accessible
- [ ] Field widths appropriate for touch input
- [ ] Dropdown lists fully visible

**Visualization Screen:**
- [ ] SVG diagram centered and scaled appropriately
- [ ] Legend visible (not cut off)
- [ ] Round scrubber/buttons accessible at bottom
- [ ] Stitch count visible
- [ ] Navigation buttons (previous/next) positioned clearly

**Settings Screen:**
- [ ] All toggles and selectors visible
- [ ] Labels and descriptions clear
- [ ] No content cut off at bottom
- [ ] Back button accessible

### Landscape Orientation

#### Orientation Change Behavior

- [ ] Orientation lock disabled: app rotates smoothly
- [ ] Orientation lock enabled: app doesn't interfere
- [ ] Landscape layout loads correctly
- [ ] Previous state preserved during rotation
- [ ] No crashes or ANR during rotation

#### Landscape-Specific Layout

**Generator Screen (Landscape):**
- [ ] Form fields arranged horizontally or with multi-column layout
- [ ] All fields visible without excessive scrolling
- [ ] "Generate" button easily accessible
- [ ] Field widths appropriate for landscape

**Visualization Screen (Landscape):**
- [ ] SVG diagram enlarged to utilize horizontal space
- [ ] Legend repositioned if needed (left/right sidebar option)
- [ ] Round controls accessible (bottom or side)
- [ ] Additional space used effectively
- [ ] No horizontal scrolling required

**Settings Screen (Landscape):**
- [ ] Toggles and selectors properly arranged
- [ ] All settings visible without scrolling
- [ ] Proper use of horizontal space

#### Multi-Column Considerations

- [ ] Consider if split-view is appropriate for larger screens
- [ ] Master-detail layout (if applicable) works in landscape
- [ ] Sufficient white space without wasted layout
- [ ] Touch targets don't become too large

---

## Critical Flow Test Cases

### Flow 1: Generate Pattern (Tablet-Specific)

#### Portrait Orientation

**Test Steps:**
1. [ ] Home screen displays properly
2. [ ] Tap "Generate" button
3. [ ] Generator screen appears with good layout
4. [ ] Select "Sphere" shape
5. [ ] Set parameters (10cm, 14/16 gauge)
6. [ ] Tap "Generate"
7. [ ] Pattern appears in visualization

**Expected Results:**
- [ ] Form fields easy to fill on tablet
- [ ] Touch targets comfortably spaced (not cramped)
- [ ] Generation completes < 200ms
- [ ] All content visible without excessive scrolling

#### Landscape Orientation

**Test Steps:**
1. [ ] Rotate device to landscape
2. [ ] Layout adapts without crashes
3. [ ] All form fields still visible
4. [ ] Previous values preserved
5. [ ] Tap "Generate"
6. [ ] Pattern appears correctly

**Expected Results:**
- [ ] Layout efficiently uses landscape space
- [ ] No content cut off
- [ ] Rotation smooth and natural
- [ ] Performance maintained

#### Rotation Stress Test

**Test Steps:**
1. [ ] Start in portrait
2. [ ] Rotate to landscape
3. [ ] Rotate back to portrait
4. [ ] Repeat 3 times rapidly
5. [ ] App should handle gracefully

**Expected Results:**
- [ ] No crashes or freezing
- [ ] No memory leaks
- [ ] State preserved through rotations
- [ ] FPS remains smooth

---

### Flow 2: Navigation in Visualization (Landscape Focus)

#### Landscape Visualization

**Test Steps:**

1. [ ] Portrait: Generate pattern and view visualization
2. [ ] Rotate to landscape
3. [ ] SVG expands to use screen width
4. [ ] Legend repositioned appropriately
5. [ ] Navigate rounds using controls
6. [ ] Use scrubber slider
7. [ ] Tap on stitches in diagram

**Expected Results:**
- [ ] Larger visualization easier to read/interact with
- [ ] All navigation controls accessible
- [ ] Scrubber has adequate space for accurate dragging
- [ ] Touch targets (on stitches) easier to tap accurately
- [ ] Performance maintained in landscape

#### Multi-Touch Support (iPad-Specific)

**Test Steps:**
1. [ ] Landscape mode with visualization visible
2. [ ] Attempt pinch-zoom on SVG (if supported)
3. [ ] Attempt two-finger swipe for previous/next round (if supported)
4. [ ] Regular tap-to-select stitches still works

**Expected Results:**
- [ ] Multi-touch gestures work as intended or gracefully ignored
- [ ] No unintended behavior from multi-touch
- [ ] Single-touch navigation still responsive

---

### Flow 3: Export on Tablet

#### Portrait Export

**Test Steps:**
1. [ ] Pattern visible in visualization
2. [ ] Tap "Export"
3. [ ] Select "PDF"
4. [ ] Confirm export
5. [ ] Verify file saved

**Expected Results:**
- [ ] Export dialog fits on screen
- [ ] All buttons tappable
- [ ] PDF generated correctly

#### Landscape Export

**Test Steps:**
1. [ ] Rotate to landscape
2. [ ] Tap "Export"
3. [ ] Select "PDF"
4. [ ] Export dialog appears
5. [ ] Confirm export

**Expected Results:**
- [ ] Dialog properly positioned in landscape
- [ ] All content visible
- [ ] Export completes successfully

#### File Management (iPad-Specific)

**Test Steps:**
1. [ ] PDF exports to Files app location
2. [ ] PDF accessible in Files app
3. [ ] Can open PDF from Files app
4. [ ] Can share PDF via Mail/Messages

**Expected Results:**
- [ ] iOS file management integration works
- [ ] PDF discoverable and accessible

---

### Flow 4: Kid Mode on Tablet

#### Portrait Kid Mode

**Test Steps:**
1. [ ] Navigate to Settings
2. [ ] Enable Kid Mode
3. [ ] Verify UI changes
4. [ ] Touch targets enlarged (56x56pt minimum)
5. [ ] All elements tappable

**Expected Results:**
- [ ] Touch targets comfortably spaced
- [ ] No elements too close together
- [ ] Text larger and more readable
- [ ] Colors bright and engaging

#### Landscape Kid Mode

**Test Steps:**
1. [ ] In Kid Mode, rotate to landscape
2. [ ] Verify layout adapts
3. [ ] Touch targets still meet minimum (56x56pt)
4. [ ] No cramping or overlapping

**Expected Results:**
- [ ] Landscape layout also respects Kid Mode minimums
- [ ] Extra horizontal space used effectively
- [ ] Larger elements don't break layout

---

### Flow 5: Settings on Tablet

#### Portrait Settings

**Test Steps:**
1. [ ] Navigate to Settings
2. [ ] All toggles and selectors visible
3. [ ] Sufficient scrolling if needed
4. [ ] Labels clear and descriptive
5. [ ] Test terminology toggle
6. [ ] Test high contrast toggle

**Expected Results:**
- [ ] All settings accessible
- [ ] Changes apply immediately
- [ ] No scrolling glitches

#### Landscape Settings

**Test Steps:**
1. [ ] Rotate to landscape
2. [ ] Settings screen adapts
3. [ ] All options visible
4. [ ] Toggles still accessible
5. [ ] Test terminology and contrast changes

**Expected Results:**
- [ ] Landscape layout efficient
- [ ] No content cut off
- [ ] Settings remain persistent

---

## Touch Target Verification

### Tablet Touch Target Standards

**Standard touch targets:**
- iPhone/iPad: 44x44 points minimum
- Android tablets: 48x48 dp minimum
- Kid Mode: 56x56 points/dp minimum

### Touch Target Audit Checklist

- [ ] All buttons: minimum 44x44pt (iOS) / 48x48dp (Android)
- [ ] Form inputs: minimum 44x44pt / 48x48dp
- [ ] Interactive icons: minimum 44x44pt / 48x48dp
- [ ] Checkboxes: minimum 44x44pt / 48x48dp
- [ ] Radio buttons: minimum 44x44pt / 48x48dp
- [ ] Slider/scrubber: minimum 44x44pt tall for dragging
- [ ] SVG stitch tappable: minimum 44x44pt hit area (or close approximation)
- [ ] Kid Mode: all targets 56x56pt minimum
- [ ] Spacing between targets: 8pt minimum

### Spacing Verification

- [ ] No targets accidentally tappable when aiming for different target
- [ ] Sufficient padding around each interactive element
- [ ] Landscape mode maintains proper spacing

---

## Accessibility on Tablets

### VoiceOver (iPad) Testing

**Additional iPad Tests:**
- [ ] Two-finger swipe gestures work with VoiceOver
- [ ] Rotor navigation works (if implemented)
- [ ] Landscape mode maintains VoiceOver functionality
- [ ] All elements announcements clear and helpful
- [ ] SVG diagram description comprehensive

### TalkBack (Android Tablet) Testing

**Additional Android Tablet Tests:**
- [ ] Local context menu (when swiping down then right)
- [ ] Custom actions available (if implemented)
- [ ] Landscape mode maintains TalkBack functionality
- [ ] All elements properly labeled
- [ ] Reading order logical in landscape

### Larger Screen Accessibility

- [ ] Text scaling still works (up to 200%)
- [ ] Focus indicators visible on larger screen
- [ ] Color contrast maintained
- [ ] High contrast mode works in landscape

---

## Performance on Tablets

### Generation Performance

| Device | Expected | Acceptable |
|--------|----------|-----------|
| iPad Air | <150ms | <200ms |
| Tab S7 | <150ms | <200ms |

**Note**: Tablets may be faster than phones due to larger RAM and newer processors.

### Navigation Performance

| Device | Target FPS | Min Acceptable |
|--------|-----------|----------------|
| iPad Air | 60 | 55 |
| Tab S7 | 60 | 55 |

**Note**: Larger screens may increase SVG rendering cost. Monitor FPS during visualization.

### Memory Usage

**Targets:**
- Idle: < 50MB
- With pattern: < 100MB
- Peak: < 150MB

---

## Orientation Change Handling

### Automatic Rotation

**Test Steps:**
1. [ ] Device rotation lock OFF
2. [ ] Open app in portrait
3. [ ] Rotate device to landscape
4. [ ] Verify layout changes
5. [ ] Rotate back to portrait
6. [ ] Verify layout restores

**Expected Results:**
- [ ] Layout changes smoothly
- [ ] No crashes
- [ ] No memory leaks
- [ ] State preserved (e.g., current round)

### Locked Orientation

**Test Steps:**
1. [ ] Device rotation lock ON
2. [ ] App respects lock
3. [ ] No forced rotation
4. [ ] Functionality unchanged

**Expected Results:**
- [ ] App doesn't override device rotation setting
- [ ] All features work in single orientation

---

## Keyboard & External Input (iPad)

### iPad Keyboard Testing

- [ ] External keyboard connection recognized
- [ ] All form fields keyboard-accessible
- [ ] Tab navigation works
- [ ] Enter submits forms
- [ ] Escape dismisses dialogs
- [ ] Keyboard appearance/dismissal smooth

### Split-View & Multitasking (iPad-Specific)

**If tablet supports split-view:**

- [ ] App works correctly when split-view active
- [ ] Content adapts to narrower width
- [ ] App doesn't crash when resizing split-view
- [ ] Performance acceptable with split-view

---

## Test Environment Setup

### iPad Air Setup

1. **Device Configuration:**
   - [ ] Update to iPadOS 17
   - [ ] Connect to test WiFi
   - [ ] Enable Airplane Mode toggle (if needed for testing)
   - [ ] Disable auto-lock: Settings → Display & Brightness → Auto-Lock → Never

2. **App Installation:**
   - [ ] Install via Testflight or direct build
   - [ ] Clear app data before starting
   - [ ] Verify app version

3. **Accessibility Setup:**
   - [ ] Enable VoiceOver: Settings → Accessibility → VoiceOver → On
   - [ ] Configure shortcut: Settings → Accessibility → Accessibility Shortcut → VoiceOver

### Samsung Tab S7 Setup

1. **Device Configuration:**
   - [ ] Update to Android 11+ (preferably Android 13)
   - [ ] Connect to test WiFi
   - [ ] Enable Developer Options
   - [ ] Disable auto-lock: Settings → Display → Lock screen → Lock time → Never

2. **App Installation:**
   - [ ] Install APK or via Play beta
   - [ ] Clear app data
   - [ ] Verify app version

3. **Accessibility Setup:**
   - [ ] Enable TalkBack: Settings → Accessibility → TalkBack → On
   - [ ] Configure volume key shortcut: Settings → Accessibility → Volume key shortcut

### Testing Tools

- [ ] Tablet device
- [ ] Landscape stand/holder (for hands-free testing)
- [ ] Bluetooth keyboard (for iPad external keyboard testing)
- [ ] Screen recording app
- [ ] Color Contrast Analyzer app (if needed)

---

## Test Execution Checklist

### Pre-Test

- [ ] Both tablets updated to target OS versions
- [ ] Test app installed on both tablets
- [ ] WiFi connectivity verified
- [ ] Device orientation lock toggle accessible
- [ ] VoiceOver/TalkBack setup complete
- [ ] Test environment documented

### Portrait Testing

- [ ] All 5 flows tested in portrait
- [ ] Layout responsive without excessive scrolling
- [ ] Touch targets verified
- [ ] Navigation smooth and responsive
- [ ] Results recorded in portrait column

### Landscape Testing

- [ ] All 5 flows tested in landscape
- [ ] Layout adapts correctly
- [ ] No content cut off
- [ ] Touch targets maintained
- [ ] Performance acceptable
- [ ] Results recorded in landscape column

### Accessibility Testing

- [ ] VoiceOver/TalkBack navigation tested
- [ ] Both orientations tested with screen readers
- [ ] Touch targets verified for accessibility
- [ ] Color contrast maintained

### Post-Test

- [ ] Summarize findings
- [ ] Document orientation-specific issues
- [ ] Create issues for failures
- [ ] Update test matrix
- [ ] Generate test report

---

## Sign-Off

| Role | Date | Notes |
|------|------|-------|
| QA Engineer | ☐ | |
| Frontend Lead | ☐ | |

**Test Execution Time Estimate**: 3-4 hours (40-60 minutes per flow × 5 flows × 2 orientations)

---

**Related Documentation:**
- [Phase 4 Plan](../../../project_plans/mvp/phases/phase-4.md)
- [Accessibility Checklist](../../../accessibility/accessibility-checklist.md)
- [Testing Procedures](../../../accessibility/testing-procedures.md)
- [QA-1 iOS Test Plan](./sprint-8-qa1-ios-test-plan.md)
- [QA-2 Android Test Plan](./sprint-8-qa2-android-test-plan.md)
