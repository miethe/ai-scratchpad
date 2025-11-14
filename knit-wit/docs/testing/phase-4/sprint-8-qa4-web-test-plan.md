# QA-4: Web Browser Testing - Phase 4 Sprint 8

**Story**: QA-4 - Web Browser Testing (Chrome, Safari, Firefox)
**Sprint**: Sprint 8 (Weeks 12-13)
**Effort**: 5 story points
**Owner**: QA Engineer
**Status**: Test Plan
**Created**: 2025-11-14

---

## Executive Summary

This test plan validates critical user flows across modern web browsers and platforms to ensure React Native web compatibility and responsive design. Testing focuses on browser-specific behaviors, keyboard navigation, and accessibility on desktop environments.

**Scope:**
- 3 browsers: Chrome 120+, Safari 17+, Firefox 120+
- 2 platforms: macOS, Windows
- 5 critical flows (same as mobile testing)
- Keyboard navigation verification
- Responsive design validation (desktop viewport)
- Browser-specific accessibility features

**Success Criteria:**
- All critical flows pass on all browser/platform combinations
- Keyboard navigation fully functional
- Responsive layout at multiple viewport sizes
- No console errors or warnings
- Performance acceptable

---

## Browser & Platform Matrix

| Browser | macOS | Windows | Chrome | Safari | Firefox | Status |
|---------|-------|---------|--------|--------|---------|--------|
| **Chrome 120+** | ☐ | ☐ | ✓ | - | - | Pending |
| **Safari 17+** | ☐ | - | - | ✓ | - | Pending |
| **Firefox 120+** | ☐ | ☐ | - | - | ✓ | Pending |

**Browser Specifications:**

| Browser | Version | Rendering Engine | Platform Support |
|---------|---------|------------------|------------------|
| **Chrome** | 120+ | Blink | macOS, Windows |
| **Safari** | 17+ | WebKit | macOS only |
| **Firefox** | 120+ | Gecko | macOS, Windows |

**Test Viewport Sizes:**
- Desktop: 1920x1080 (standard)
- Laptop: 1440x900 (common laptop size)
- Tablet in browser: 1024x768 (iPad-like)

---

## Critical Flow Test Cases

### Flow 1: Generate Sphere Pattern (Web)

#### Chrome Testing

**Test Steps:**

1. **Open in Chrome**
   - [ ] Navigate to app URL
   - [ ] Page loads within 2 seconds
   - [ ] No console errors (F12 → Console)
   - [ ] Home screen visible and interactive

2. **Interact with Generate Button**
   - [ ] Home page buttons visible and clickable
   - [ ] "Generate" button has proper hover state
   - [ ] Button cursor changes to pointer on hover
   - [ ] Click "Generate" button

3. **Generator Form**
   - [ ] Form fields render correctly
   - [ ] Input fields have visible borders
   - [ ] Labels associated with inputs
   - [ ] Dropdown works on click
   - [ ] Select "Sphere" from dropdown

4. **Set Parameters**
   - [ ] Diameter field: 10 cm (default or pre-filled)
   - [ ] Gauge field: 14/16 (default or pre-filled)
   - [ ] All fields accept input without issues
   - [ ] Form validation works (error messages appear if invalid)

5. **Generate Pattern**
   - [ ] Click "Generate" button
   - [ ] Loading state visible (spinner or text)
   - [ ] Pattern generates within 200ms server time + network latency
   - [ ] Visualization appears without errors
   - [ ] No console errors or warnings

**Expected Results:**
- ✓ Form renders and functions correctly
- ✓ Pattern generates successfully
- ✓ Visualization appears with sphere shape
- ✓ No console errors or warnings
- ✓ Page responsive and interactive

**Performance Target:**
- Page load: < 2 seconds
- Form interaction: < 100ms response
- Pattern generation: < 250ms (client) + network

#### Safari Testing

**Test Steps:**

1. **Open in Safari**
   - [ ] Navigate to app URL
   - [ ] Page loads successfully
   - [ ] No Safari-specific console warnings
   - [ ] Layout renders correctly (may differ from Chrome)

2. **Repeat Flow 1 Steps 2-5**
   - [ ] All interactions work identically to Chrome
   - [ ] Performance similar or better (Safari optimized for macOS)
   - [ ] No Safari-specific issues

**Safari-Specific Considerations:**
- [ ] WebKit engine may render CSS differently
- [ ] Touch events may behave differently with trackpad
- [ ] Gesture support (if implemented) works

#### Firefox Testing

**Test Steps:**

1. **Open in Firefox**
   - [ ] Navigate to app URL
   - [ ] Page loads successfully
   - [ ] No Firefox-specific console warnings
   - [ ] Layout renders correctly

2. **Repeat Flow 1 Steps 2-5**
   - [ ] All interactions work
   - [ ] Performance acceptable
   - [ ] No Firefox-specific issues

**Firefox-Specific Considerations:**
- [ ] Gecko engine may render differently
- [ ] Input handling may differ

---

### Flow 2: Navigate Visualization (Keyboard Focus)

#### Keyboard Navigation Testing (All Browsers)

**Objective**: Verify full keyboard accessibility of visualization controls

**Test Steps:**

1. **Access Visualization**
   - [ ] Generate a pattern as in Flow 1
   - [ ] Visualization screen appears
   - [ ] SVG diagram visible

2. **Tab Navigation**
   - [ ] Press Tab key
   - [ ] Focus moves to next interactive element
   - [ ] Focus indicator visible (must have 2px outline minimum)
   - [ ] Tab through all buttons: Previous, Next, Export, Settings
   - [ ] Tab order is logical (left to right, top to bottom)

3. **Navigate Rounds with Keyboard**
   - [ ] Tab to "Previous Round" button
   - [ ] Press Enter key
   - [ ] Round decrements
   - [ ] SVG visualization updates
   - [ ] Round number text changes

4. **Next Round Navigation**
   - [ ] Tab to "Next Round" button
   - [ ] Press Enter (or Space)
   - [ ] Round increments
   - [ ] Visualization updates
   - [ ] Correct round displayed

5. **Scrubber Slider Keyboard Control**
   - [ ] Tab to round scrubber slider
   - [ ] Use Arrow Left/Right keys to adjust
   - [ ] Each arrow press adjusts slider
   - [ ] Visualization updates with slider movement
   - [ ] Holding arrow keys allows rapid navigation

6. **Shift+Tab Backward Navigation**
   - [ ] While in controls, press Shift+Tab
   - [ ] Focus moves backward through elements
   - [ ] Tab order reverses correctly

#### Focus Indicator Verification

**All Browsers:**
- [ ] Focus outline visible on all interactive elements
- [ ] Outline color has 3:1 contrast with background
- [ ] Outline thickness minimum 2px
- [ ] Outline not cut off by container boundaries
- [ ] Focus outline appears on keyboard Tab, not on mouse click (optional but preferred)

#### Keyboard Shortcuts (If Implemented)

- [ ] Left Arrow: Previous round (if supported)
- [ ] Right Arrow: Next round (if supported)
- [ ] Home/End: Jump to first/last round (if supported)
- [ ] Escape: Close modals/dialogs (if applicable)

**Expected Results:**
- ✓ All elements keyboard accessible
- ✓ Logical tab order
- ✓ Visible focus indicators
- ✓ Keyboard shortcuts work intuitively
- ✓ No keyboard traps

---

### Flow 3: Export to PDF (Desktop)

#### Web Export Behavior

**Test Steps:**

1. **Initiate Export**
   - [ ] Generate pattern
   - [ ] Click "Export" button
   - [ ] Export menu/dialog appears
   - [ ] "PDF" option visible

2. **Select PDF Export**
   - [ ] Click "PDF" option
   - [ ] Dialog appears with file name
   - [ ] Default name: "sphere-10cm.pdf" (or similar)
   - [ ] "Export" or "Save" button ready

3. **Complete Export**
   - [ ] Click "Export" button
   - [ ] Browser download begins
   - [ ] File appears in Downloads folder
   - [ ] File name correct
   - [ ] File size reasonable (< 5MB)

4. **Verify PDF**
   - [ ] Open downloaded PDF in browser or PDF viewer
   - [ ] Pattern visualization visible
   - [ ] Instructions legible
   - [ ] No corrupt data or missing content

#### Browser-Specific Export Behavior

**Chrome & Firefox (Windows):**
- [ ] Download goes to Downloads folder
- [ ] No additional prompts
- [ ] File saved with correct name

**Chrome & Firefox (macOS):**
- [ ] Download goes to Downloads folder (or Safari's chosen location)
- [ ] File saved correctly

**Safari (macOS):**
- [ ] Download handled by Safari
- [ ] File may be saved to Downloads or Desktop (user's choice)
- [ ] PDF opens correctly in Preview (or user's PDF app)

**Expected Results:**
- ✓ Export completes without errors
- ✓ File downloads successfully
- ✓ File is readable PDF
- ✓ Content complete and correct

---

### Flow 4: Toggle Kid Mode (Web)

**Test Steps:**

1. **Access Settings**
   - [ ] Click "Settings" button or link
   - [ ] Settings screen/panel appears

2. **Locate Kid Mode Toggle**
   - [ ] Find "Kid Mode" toggle or switch
   - [ ] Current state visible (on/off)
   - [ ] Toggle is clickable and large enough (44x44px minimum)

3. **Enable Kid Mode**
   - [ ] Click Kid Mode toggle
   - [ ] Toggle visual state changes
   - [ ] UI updates immediately:
     - [ ] Font sizes increase
     - [ ] Colors become more saturated/brighter
     - [ ] Touch targets/buttons enlarge (visually)
     - [ ] Simplified language appears
     - [ ] Animations (if any) appear

4. **Verify Kid Mode Styles**
   - [ ] Entire page reflects Kid Mode styling
   - [ ] All text larger and easier to read
   - [ ] Color scheme more vibrant
   - [ ] No layout issues from font size changes
   - [ ] SVG visualization still displays correctly

5. **Disable Kid Mode**
   - [ ] Click Kid Mode toggle again
   - [ ] UI reverts to normal styling
   - [ ] Font sizes normalize
   - [ ] Colors revert to standard palette

#### Responsive Design Check (Kid Mode)

- [ ] Kid Mode works at desktop viewport sizes
- [ ] Layout doesn't break with larger fonts
- [ ] No horizontal scrolling introduced
- [ ] Touch targets (even for mouse) appropriately sized

**Expected Results:**
- ✓ Kid Mode toggles instantly (< 100ms)
- ✓ All UI elements update correctly
- ✓ No visual glitches or layout breaks
- ✓ Proper contrast maintained in Kid Mode
- ✓ Settings persist on page reload

---

### Flow 5: Settings - Terminology & High Contrast (Web)

**Test Steps:**

1. **Navigate to Settings**
   - [ ] Settings page accessible
   - [ ] All options visible

2. **Terminology Toggle**
   - [ ] Find "Terminology" selector (dropdown or radio buttons)
   - [ ] Current setting displayed (US or UK)
   - [ ] Click to change
   - [ ] Opposite terminology selected
   - [ ] Close selector

3. **Verify Terminology Change**
   - [ ] Generate pattern or view existing one
   - [ ] Instructions now in UK terminology
   - [ ] Stitch abbreviations: sc → dc, dc → tr, etc.
   - [ ] All translations correct

4. **High Contrast Mode Toggle**
   - [ ] Find "High Contrast" toggle
   - [ ] Current state visible
   - [ ] Click toggle to enable
   - [ ] UI updates with enhanced contrast:
     - [ ] Text color intensifies
     - [ ] Background colors adjust
     - [ ] Focus indicators more visible
     - [ ] All text meets 7:1+ contrast

5. **Test Settings Persistence**
   - [ ] Verify settings applied
   - [ ] Reload page (F5 or Cmd+R)
   - [ ] Settings should persist:
     - [ ] Terminology still UK (if changed)
     - [ ] High Contrast still on (if enabled)
     - [ ] Kid Mode still on (if enabled)

#### High Contrast Contrast Ratio Verification

- [ ] Primary text: 7:1+ (WCAG AAA enhanced)
- [ ] Interactive elements: 3:1+ minimum
- [ ] Focus indicators: 3:1+ contrast

**Expected Results:**
- ✓ Settings toggle instantly
- ✓ UI updates reflect settings
- ✓ High Contrast achieves 7:1+ ratio
- ✓ Settings persist via localStorage
- ✓ All combinations work together (Kid Mode + High Contrast)

---

## Accessibility Testing (Web)

### Screen Reader Testing

#### Chrome (Windows) - NVDA

**Test Steps:**
1. [ ] Download and install NVDA (free screen reader)
2. [ ] Open app in Chrome
3. [ ] Start NVDA (Insert+N or activate)
4. [ ] Navigate using arrow keys

**Checks:**
- [ ] Home screen heading announced
- [ ] Buttons announced with role and label
- [ ] Form fields have associated labels
- [ ] Input instructions provided
- [ ] Dropdown announces options
- [ ] Navigation elements announced
- [ ] Round changes announced during visualization

#### Safari (macOS) - VoiceOver

**Test Steps:**
1. [ ] Enable VoiceOver: Cmd+F5
2. [ ] Open app in Safari
3. [ ] Navigate using arrow keys and VO (Ctrl+Option)

**Checks:**
- [ ] Same as NVDA checks above
- [ ] Safari-specific gestures work (if applicable)
- [ ] Web content accessible with Safari reader

#### Firefox - Built-in Accessibility

**Test Steps:**
1. [ ] Right-click on problematic content
2. [ ] Inspect with Firefox Accessibility Inspector
3. [ ] Review accessibility tree

**Checks:**
- [ ] Proper ARIA labels where needed
- [ ] Semantic HTML used
- [ ] No accessibility tree errors

### Keyboard Navigation

**All Browsers:**

- [ ] Tab to all interactive elements
- [ ] Shift+Tab navigates backwards
- [ ] Enter/Space activates buttons
- [ ] Arrow keys navigate sliders/selectors
- [ ] Escape closes dialogs (if present)
- [ ] Focus visible on all elements
- [ ] No keyboard traps (can Tab away from any element)
- [ ] Tab order logical

### Color Contrast

- [ ] All text: 4.5:1 minimum (WCAG AA)
- [ ] Large text (18pt+): 3:1 minimum
- [ ] Interactive elements: 3:1 minimum
- [ ] High Contrast mode: 7:1+ (WCAG AAA)
- [ ] Focus indicators: 3:1 against adjacent colors

### Touch Target Sizing (for Trackpad/Touch-Enabled Devices)

- [ ] Buttons: minimum 44x44px
- [ ] Form inputs: minimum 44x44px
- [ ] Interactive icons: minimum 44x44px
- [ ] Slider: minimum 44px tall for dragging
- [ ] Spacing between targets: 8px minimum

### Content & Semantics

- [ ] Page title descriptive
- [ ] Headings form logical hierarchy
- [ ] Lists use proper semantic markup
- [ ] Form labels associated with inputs
- [ ] Error messages linked to inputs
- [ ] Success feedback provided
- [ ] No flashing content (< 3 flashes/second)

---

## Responsive Design Validation

### Viewport Sizes to Test

| Viewport | Width | Device Type | Test |
|----------|-------|-------------|------|
| Desktop | 1920x1080 | Large monitor | ☐ |
| Laptop | 1440x900 | Typical laptop | ☐ |
| Tablet | 1024x768 | Tablet-like in browser | ☐ |
| Mobile | 375x667 | iPhone SE (web version) | ☐ |

### Chrome DevTools Testing

**How to test:**
1. Open DevTools (F12)
2. Toggle device toolbar (Ctrl+Shift+M)
3. Select different device presets
4. Verify layout at each size

### Responsiveness Checklist

At each viewport size:
- [ ] Content fits without horizontal scrolling
- [ ] Text is readable (not too small)
- [ ] Touch/click targets appropriately sized
- [ ] Navigation accessible (not hidden)
- [ ] Images/SVG scale appropriately
- [ ] Forms don't require excessive scrolling
- [ ] Layout switches cleanly (no awkward breakpoints)

---

## Browser Compatibility Issues

### Known Issues by Browser

#### Chrome-Specific

- [ ] Verify localStorage works (for settings persistence)
- [ ] Check support for CSS Flexbox/Grid
- [ ] Verify SVG rendering accuracy

#### Safari-Specific

- [ ] WebKit CSS differences (e.g., `-webkit-` prefixes)
- [ ] Potential input type support differences
- [ ] Touch behavior on trackpad (if applicable)
- [ ] localStorage behavior

#### Firefox-Specific

- [ ] Gecko rendering differences
- [ ] Check for Firefox-specific console warnings
- [ ] Verify image loading and caching

---

## Console & Network Analysis

### Console Inspection

**Developer Tools (F12):**

- [ ] No JavaScript errors (red X)
- [ ] No critical warnings
- [ ] API calls succeed (check Network tab)
- [ ] Network requests < 1 second per request
- [ ] No 404 or 500 errors
- [ ] CSP (Content Security Policy) violations (if any) noted

### Network Performance

- [ ] Initial page load: < 2 seconds (on broadband)
- [ ] API calls: < 500ms response time
- [ ] Asset loading: images, CSS, JS load efficiently
- [ ] No unnecessary requests
- [ ] Caching headers set correctly

---

## Browser Features Testing

### LocalStorage / SessionStorage

- [ ] Settings saved to localStorage
- [ ] Settings persist after page reload
- [ ] Settings persist after browser restart
- [ ] Clearing browser data resets settings
- [ ] No errors in console regarding storage

### Service Workers (If Implemented)

- [ ] Service worker registers successfully
- [ ] Offline functionality (if implemented) works
- [ ] Cache strategy appropriate
- [ ] Update mechanism works

### Web APIs

- [ ] File download API works (for PDF export)
- [ ] Touch events (if supporting touch on desktop) work
- [ ] Resize events handled properly
- [ ] Scroll events smooth

---

## Test Environment Setup

### Browser Installation

**Chrome:**
- [ ] Install Chrome 120+ or later
- [ ] Update to latest version
- [ ] Install browser extensions (if needed): WAVE, axe DevTools

**Safari (macOS):**
- [ ] macOS 13+ with Safari 17+
- [ ] Update to latest Safari version

**Firefox:**
- [ ] Install Firefox 120+ or later
- [ ] Update to latest version
- [ ] Install accessibility plugin (if needed)

### Development Tools

- [ ] DevTools/Inspector available (F12)
- [ ] Network tab visible
- [ ] Console tab visible
- [ ] Device emulation/responsive mode available
- [ ] Accessibility inspector available (if applicable)

### Testing Tools

- [ ] NVDA (Windows screen reader) - free download
- [ ] WAVE browser extension (Chrome/Firefox) for accessibility audits
- [ ] axe DevTools (Chrome/Firefox) for detailed audits
- [ ] Color Contrast Analyzer
- [ ] Screen recording software (if documenting issues)

---

## Test Execution Checklist

### Pre-Test Setup

- [ ] All browsers installed and updated
- [ ] Development tools available (F12)
- [ ] Test app URL accessible
- [ ] Test environment documented (browser versions, OS versions)
- [ ] Network connection stable
- [ ] Screen recording setup (if needed)

### Chrome Testing

- [ ] Verify page load (< 2 seconds)
- [ ] Test all 5 flows
- [ ] Keyboard navigation complete
- [ ] Check console for errors/warnings
- [ ] Test at 3 viewport sizes
- [ ] Record results

### Safari Testing (macOS)

- [ ] Repeat Chrome testing on Safari
- [ ] Note any differences
- [ ] Test Safari-specific features
- [ ] VoiceOver accessibility testing

### Firefox Testing

- [ ] Repeat Chrome testing on Firefox
- [ ] Check for Firefox-specific issues
- [ ] Console analysis

### Cross-Browser Issues

- [ ] Document any browser-specific failures
- [ ] Note if issue is browser or platform-specific
- [ ] Prioritize fixes based on browser usage

### Accessibility Testing

- [ ] NVDA (Windows) or VoiceOver (Mac) screen reader testing
- [ ] WAVE or axe audit for automated checks
- [ ] Keyboard navigation complete
- [ ] High contrast testing
- [ ] Results recorded

### Post-Test

- [ ] Summarize findings by browser
- [ ] Create issues for failures (note browser/OS)
- [ ] Document known limitations
- [ ] Generate test report
- [ ] Compare performance across browsers

---

## Performance Benchmarks

### Page Load Time

| Metric | Target | Acceptable |
|--------|--------|-----------|
| First Contentful Paint (FCP) | < 1s | < 1.5s |
| Largest Contentful Paint (LCP) | < 2.5s | < 3.5s |
| Cumulative Layout Shift (CLS) | < 0.1 | < 0.25 |

### Interaction Speed

| Action | Target | Acceptable |
|--------|--------|-----------|
| Button click response | < 100ms | < 200ms |
| Form input | < 50ms | < 100ms |
| Round navigation | < 50ms | < 100ms |
| Export completion | < 3s | < 5s |

---

## Sign-Off

| Role | Date | Notes |
|------|------|-------|
| QA Engineer | ☐ | |
| Frontend Lead | ☐ | |

**Test Execution Time Estimate**: 3-4 hours (30-40 minutes per browser/OS combination × 9 combinations)

---

**Related Documentation:**
- [Phase 4 Plan](../../../project_plans/mvp/phases/phase-4.md)
- [Accessibility Checklist](../../../accessibility/accessibility-checklist.md)
- [Testing Procedures](../../../accessibility/testing-procedures.md)
- [QA-1 iOS Test Plan](./sprint-8-qa1-ios-test-plan.md)
- [QA-2 Android Test Plan](./sprint-8-qa2-android-test-plan.md)
- [QA-3 Tablet Test Plan](./sprint-8-qa3-tablet-test-plan.md)
