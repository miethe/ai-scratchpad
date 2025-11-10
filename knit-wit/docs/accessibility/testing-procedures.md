# Accessibility Testing Procedures

## Overview

This document provides step-by-step testing procedures for validating WCAG 2.1 AA compliance in the Knit-Wit React Native application.

**Target**: WCAG 2.1 Level AA
**Platforms**: iOS, Android
**Testing Frequency**: Every PR, pre-release, quarterly audits

---

## Table of Contents

1. [Testing Tools Setup](#testing-tools-setup)
2. [Automated Testing](#automated-testing)
3. [Manual Testing](#manual-testing)
4. [Screen Reader Testing](#screen-reader-testing)
5. [Keyboard Navigation Testing](#keyboard-navigation-testing)
6. [Visual Accessibility Testing](#visual-accessibility-testing)
7. [Pre-Release Checklist](#pre-release-checklist)
8. [Issue Reporting](#issue-reporting)

---

## Testing Tools Setup

### Required Tools

#### Development Tools

1. **React Native Testing Library**
   ```bash
   pnpm add -D @testing-library/react-native @testing-library/jest-native
   ```

2. **ESLint Accessibility Plugin**
   ```bash
   pnpm add -D eslint-plugin-react-native-a11y
   ```

   Add to `.eslintrc.js`:
   ```javascript
   {
     "plugins": ["react-native-a11y"],
     "extends": ["plugin:react-native-a11y/all"]
   }
   ```

3. **Jest Accessibility Matchers**
   ```javascript
   // jest-setup.js
   import '@testing-library/jest-native/extend-expect';
   ```

#### iOS Testing Tools

1. **Xcode Accessibility Inspector**
   - Built into Xcode
   - Location: Xcode → Developer Tools → Accessibility Inspector
   - Use for: Inspecting accessibility properties, audit scans

2. **VoiceOver**
   - Built into iOS
   - Enable: Settings → Accessibility → VoiceOver
   - Practice mode: Settings → Accessibility → VoiceOver → VoiceOver Practice

#### Android Testing Tools

1. **Accessibility Scanner**
   - Download: [Play Store](https://play.google.com/store/apps/details?id=com.google.android.apps.accessibility.auditor)
   - Use for: On-device accessibility audits

2. **TalkBack**
   - Built into Android
   - Enable: Settings → Accessibility → TalkBack

3. **Android Studio Layout Inspector**
   - Built into Android Studio
   - Use for: Inspecting view hierarchy and accessibility properties

#### Cross-Platform Tools

1. **Color Contrast Analyzer (Desktop)**
   - Download: [TPGi CCA](https://www.tpgi.com/color-contrast-checker/)
   - Use for: Manual contrast verification

2. **WebAIM Contrast Checker (Online)**
   - URL: https://webaim.org/resources/contrastchecker/
   - Use for: Quick contrast checks

---

## Automated Testing

### Unit Tests for Accessibility

#### Basic Accessibility Test Template

```typescript
import { render } from '@testing-library/react-native';
import { Button } from '@/components/Button';

describe('Button Accessibility', () => {
  it('has accessible label', () => {
    const { getByLabelText } = render(
      <Button onPress={() => {}}>Generate Pattern</Button>
    );

    expect(getByLabelText('Generate Pattern')).toBeTruthy();
  });

  it('has correct accessibility role', () => {
    const { getByRole } = render(
      <Button onPress={() => {}}>Generate Pattern</Button>
    );

    expect(getByRole('button')).toBeTruthy();
  });

  it('communicates disabled state', () => {
    const { getByRole } = render(
      <Button disabled onPress={() => {}}>Generate Pattern</Button>
    );

    const button = getByRole('button');
    expect(button).toHaveAccessibilityState({ disabled: true });
  });

  it('has minimum touch target size', () => {
    const { getByRole } = render(
      <Button onPress={() => {}}>Generate Pattern</Button>
    );

    const button = getByRole('button');
    const { width, height } = button.props.style;

    expect(width).toBeGreaterThanOrEqual(44);
    expect(height).toBeGreaterThanOrEqual(44);
  });
});
```

#### Color Contrast Test Template

```typescript
import { colors } from '@/theme';
import { getContrastRatio } from '@/utils/accessibility';

describe('Color Contrast - Text on Backgrounds', () => {
  it('textPrimary on background meets WCAG AA', () => {
    const ratio = getContrastRatio(colors.textPrimary, colors.background);
    expect(ratio).toBeGreaterThanOrEqual(4.5);
  });

  it('textSecondary on background meets WCAG AA', () => {
    const ratio = getContrastRatio(colors.textSecondary, colors.background);
    expect(ratio).toBeGreaterThanOrEqual(4.5);
  });

  it('primary color on background meets UI component requirement', () => {
    const ratio = getContrastRatio(colors.primary, colors.background);
    expect(ratio).toBeGreaterThanOrEqual(3.0);
  });
});

describe('Color Contrast - Borders', () => {
  it('border color on background meets WCAG AA', () => {
    const ratio = getContrastRatio(colors.border, colors.background);
    expect(ratio).toBeGreaterThanOrEqual(3.0);
  });
});
```

#### Form Accessibility Test Template

```typescript
import { render } from '@testing-library/react-native';
import { TextInput } from '@/components/TextInput';

describe('TextInput Accessibility', () => {
  it('has associated label', () => {
    const { getByLabelText } = render(
      <TextInput label="Diameter (cm)" value="" onChangeText={() => {}} />
    );

    expect(getByLabelText('Diameter (cm)')).toBeTruthy();
  });

  it('announces errors to screen readers', () => {
    const { getByA11yState } = render(
      <TextInput
        label="Diameter (cm)"
        value="invalid"
        error="Must be a positive number"
        onChangeText={() => {}}
      />
    );

    // Error state should be communicated
    const input = getByA11yState({ invalid: true });
    expect(input).toBeTruthy();
  });

  it('has correct keyboard type', () => {
    const { getByLabelText } = render(
      <TextInput
        label="Diameter (cm)"
        value=""
        keyboardType="numeric"
        onChangeText={() => {}}
      />
    );

    const input = getByLabelText('Diameter (cm)');
    expect(input.props.keyboardType).toBe('numeric');
  });
});
```

### Running Automated Tests

```bash
# Run all accessibility tests
pnpm test -- --testPathPattern=accessibility

# Run with coverage
pnpm test -- --coverage --testPathPattern=accessibility

# Run in watch mode
pnpm test -- --watch --testPathPattern=accessibility
```

### ESLint Accessibility Checks

```bash
# Lint entire project
pnpm lint

# Lint specific file
pnpm lint apps/mobile/src/components/Button.tsx

# Auto-fix issues
pnpm lint --fix
```

**Common ESLint Rules:**
- `react-native-a11y/has-accessibility-props` - Ensure touchables have labels
- `react-native-a11y/has-valid-accessibility-role` - Valid role values
- `react-native-a11y/no-nested-touchables` - Avoid nested interactive elements
- `react-native-a11y/has-accessibility-hint` - Provide hints for complex actions

---

## Manual Testing

### Device Testing Setup

#### iOS Setup

1. **Enable Developer Settings**
   - Connect device to Mac
   - Open Xcode
   - Window → Devices and Simulators
   - Enable "UI Automation"

2. **Configure Accessibility Shortcuts**
   - Settings → Accessibility → Accessibility Shortcut
   - Select: VoiceOver, Zoom, Display Accommodations
   - Triple-click side button to toggle

3. **Install Test Build**
   ```bash
   # Development build
   pnpm --filter mobile ios

   # TestFlight build (for stakeholder testing)
   pnpm --filter mobile ios:release
   ```

#### Android Setup

1. **Enable Developer Options**
   - Settings → About phone
   - Tap "Build number" 7 times
   - Settings → System → Developer options

2. **Install Accessibility Scanner**
   - Play Store → Search "Accessibility Scanner"
   - Install and grant permissions

3. **Configure Accessibility Shortcuts**
   - Settings → Accessibility
   - Enable volume key shortcut for TalkBack

4. **Install Test Build**
   ```bash
   # Development build
   pnpm --filter mobile android

   # Release build (for testing)
   pnpm --filter mobile android:release
   ```

### Visual Inspection Checklist

#### Color and Contrast

- [ ] Open app in bright sunlight - verify all text readable
- [ ] Check all interactive elements have visible boundaries
- [ ] Verify focus indicators are clearly visible
- [ ] Check error messages are distinguishable without color alone
- [ ] Verify success states use icons/text, not just color

#### Typography

- [ ] All body text is at least 16px
- [ ] Line height is adequate (1.5x minimum)
- [ ] Text is not too wide (max 80 characters per line)
- [ ] Headings are visually distinct from body text
- [ ] Font weights are appropriate (not too light)

#### Touch Targets

- [ ] All buttons are at least 44x44pt
- [ ] Interactive icons are at least 44x44pt
- [ ] Spacing between targets is adequate (8px minimum)
- [ ] Kid Mode targets are at least 56x56pt

#### Layout and Spacing

- [ ] Content does not overflow containers
- [ ] Scrollable areas are clearly indicated
- [ ] Important content is above the fold
- [ ] White space is adequate between sections

---

## Screen Reader Testing

### iOS VoiceOver Testing

#### VoiceOver Gestures Quick Reference

| Gesture | Action |
|---------|--------|
| Swipe right | Next element |
| Swipe left | Previous element |
| Double tap | Activate element |
| Three-finger swipe left/right | Navigate pages |
| Two-finger swipe up | Read all from top |
| Two-finger tap | Pause/resume speech |
| Rotor (two-finger rotate) | Change navigation mode |

#### VoiceOver Testing Workflow

1. **Enable VoiceOver**
   - Settings → Accessibility → VoiceOver → On
   - Or: Triple-click side button (if shortcut configured)

2. **Launch Knit-Wit App**
   - Navigate to app icon (swipe right/left)
   - Double-tap to open

3. **Test Home Screen**
   - [ ] VoiceOver announces screen title
   - [ ] All buttons are announced with clear labels
   - [ ] Tab order is logical (top to bottom, left to right)
   - [ ] Images have appropriate labels or are marked decorative
   - [ ] Navigation elements are properly identified

4. **Test Form Inputs**
   - [ ] Input labels are read before fields
   - [ ] Input types are announced (text field, number field, etc.)
   - [ ] Placeholder text does not replace labels
   - [ ] Error messages are announced
   - [ ] Success states are announced

5. **Test Navigation**
   - [ ] Back button is clearly labeled
   - [ ] Navigation destinations are announced
   - [ ] Current screen is identifiable
   - [ ] Breadcrumbs are readable

6. **Test Interactive Elements**
   - [ ] Buttons announce role ("button")
   - [ ] Toggles announce state (on/off)
   - [ ] Disabled elements announce disabled state
   - [ ] Loading states are announced

7. **Test Pattern Visualization**
   - [ ] SVG diagrams have text alternatives
   - [ ] Round numbers are announced
   - [ ] Stitch instructions are readable
   - [ ] Navigation between rounds is clear

8. **Test Kid Mode**
   - [ ] Kid Mode activation is announced
   - [ ] Simplified instructions are read correctly
   - [ ] All interactive elements are accessible
   - [ ] Visual aids have appropriate descriptions

**Record Issues:**
- Note element that failed
- Record what was announced vs. what should be announced
- Screenshot or screen recording if helpful

#### Common VoiceOver Issues

| Issue | Fix |
|-------|-----|
| Element skipped | Add `accessible={true}` |
| Wrong label | Update `accessibilityLabel` |
| Redundant announcement | Use `accessibilityElementsHidden` on decorative parent |
| Wrong reading order | Adjust view hierarchy or use `accessibilityViewIsModal` |
| Not announcing state changes | Use `accessibilityLiveRegion="polite"` |

### Android TalkBack Testing

#### TalkBack Gestures Quick Reference

| Gesture | Action |
|---------|--------|
| Swipe right | Next element |
| Swipe left | Previous element |
| Double tap | Activate element |
| Swipe down then right | Read from next item |
| Swipe up then down | Read from top |
| Two-finger swipe down | Pause/resume |

#### TalkBack Testing Workflow

1. **Enable TalkBack**
   - Settings → Accessibility → TalkBack → On
   - Or: Volume up + Volume down (if shortcut configured)

2. **Test Same Scenarios as VoiceOver**
   - Follow iOS VoiceOver testing workflow above
   - Note any Android-specific issues

3. **Android-Specific Checks**
   - [ ] Material Design components work correctly
   - [ ] Android keyboard navigation works
   - [ ] Back button behavior is accessible
   - [ ] Toast messages are announced
   - [ ] Bottom sheets are navigable

**Record Issues:**
- Compare behavior with iOS VoiceOver
- Note Android-specific problems
- Check if issue is platform-specific or universal

---

## Keyboard Navigation Testing

### External Keyboard Setup

#### iOS External Keyboard

1. **Connect Bluetooth Keyboard**
   - Settings → Bluetooth → Pair keyboard

2. **Enable Full Keyboard Access**
   - Settings → Accessibility → Keyboards → Full Keyboard Access → On

3. **Configure Keyboard Shortcuts**
   - Settings → Accessibility → Keyboards → Full Keyboard Access → Commands

#### Android External Keyboard

1. **Connect Keyboard**
   - Settings → Connected devices → Pair new device

2. **Enable Accessibility Features**
   - Settings → Accessibility → Switch Access (optional)

### Keyboard Testing Workflow

1. **Basic Navigation**
   - [ ] Tab moves focus forward through interactive elements
   - [ ] Shift+Tab moves focus backward
   - [ ] Focus indicator is clearly visible on all elements
   - [ ] Focus order is logical and matches visual order
   - [ ] No keyboard traps (can always Tab away)

2. **Activation**
   - [ ] Enter activates buttons
   - [ ] Space activates buttons
   - [ ] Enter submits forms
   - [ ] Escape dismisses modals/dialogs

3. **Form Controls**
   - [ ] Arrow keys work in dropdowns
   - [ ] Arrow keys work in sliders
   - [ ] Space toggles checkboxes
   - [ ] Tab moves between form fields
   - [ ] Required field validation works with keyboard

4. **Navigation**
   - [ ] Keyboard shortcuts work (if implemented)
   - [ ] Skip navigation links work (if implemented)
   - [ ] Nested navigation is accessible

5. **Modal Dialogs**
   - [ ] Focus moves into modal when opened
   - [ ] Focus is trapped within modal
   - [ ] Escape closes modal
   - [ ] Focus returns to trigger element when closed

**Common Keyboard Issues:**

| Issue | Fix |
|-------|-----|
| Can't Tab to element | Ensure `focusable={true}` or interactive component |
| Wrong tab order | Adjust view hierarchy |
| No focus indicator | Add focus styles |
| Can't exit modal | Implement keyboard event listeners for Escape |
| Skip navigation needed | Add skip links for long content |

---

## Visual Accessibility Testing

### Text Scaling Test

#### iOS Text Scaling

1. **Adjust Text Size**
   - Settings → Accessibility → Display & Text Size → Larger Text
   - Move slider to maximum

2. **Test App**
   - [ ] All text scales appropriately
   - [ ] No horizontal scrolling required
   - [ ] No text clipping or truncation
   - [ ] Layout adapts to larger text
   - [ ] Touch targets remain accessible
   - [ ] Critical information remains visible

3. **Test at Multiple Scales**
   - Default (100%)
   - 150%
   - 200% (maximum required by WCAG AA)

#### Android Text Scaling

1. **Adjust Font Size**
   - Settings → Display → Font size → Largest

2. **Test App**
   - Same checklist as iOS above

### Display Accommodations Test

#### iOS Display & Text Size Settings

Test with these settings enabled:

1. **Bold Text**
   - Settings → Accessibility → Display & Text Size → Bold Text
   - [ ] All text remains readable
   - [ ] No layout issues from bolder fonts

2. **Reduce Transparency**
   - Settings → Accessibility → Display & Text Size → Reduce Transparency
   - [ ] Overlays remain visible
   - [ ] Content behind overlays is not distracting

3. **Increase Contrast**
   - Settings → Accessibility → Display & Text Size → Increase Contrast
   - [ ] All content benefits from increased contrast
   - [ ] No visual regressions

4. **Color Filters**
   - Settings → Accessibility → Display & Text Size → Color Filters
   - Test each filter:
     - [ ] Grayscale
     - [ ] Red/Green Filter (Protanopia)
     - [ ] Green/Red Filter (Deuteranopia)
     - [ ] Blue/Yellow Filter (Tritanopia)
   - Verify: Information not conveyed by color alone

#### Android Accessibility Settings

1. **High Contrast Text**
   - Settings → Accessibility → High contrast text
   - [ ] All text remains readable

2. **Color Correction**
   - Settings → Accessibility → Color correction
   - Test each mode (same as iOS Color Filters)

3. **Remove Animations**
   - Settings → Accessibility → Remove animations
   - [ ] App functions without animations
   - [ ] Loading states are clear
   - [ ] Transitions don't break without animation

### Motion and Animation Test

1. **Enable Reduce Motion**
   - iOS: Settings → Accessibility → Motion → Reduce Motion
   - Android: Settings → Accessibility → Remove animations

2. **Test App**
   - [ ] Essential animations are simplified or removed
   - [ ] Non-essential animations are removed
   - [ ] Page transitions still work
   - [ ] Loading states are clear
   - [ ] No flashing content (< 3 flashes/second)

### Low Vision Simulation

**Tools:**
- [Who Can Use](https://www.whocanuse.com/) - Simulate vision types
- iOS Simulator → Accessibility Inspector → Color vision
- Chrome extension: NoCoffee Vision Simulator

**Test Scenarios:**
- [ ] Low contrast vision
- [ ] Color blindness (Protanopia, Deuteranopia, Tritanopia)
- [ ] Blurred vision
- [ ] Light sensitivity

---

## Pre-Release Checklist

### Before Every Release

#### Automated Checks
- [ ] All accessibility unit tests pass
- [ ] ESLint accessibility rules pass with no warnings
- [ ] Color contrast tests pass
- [ ] No accessibility regressions from previous build

#### Manual Checks (iOS)
- [ ] VoiceOver test completed on physical device
- [ ] Keyboard navigation test completed
- [ ] Text scaling test completed (up to 200%)
- [ ] Display accommodations test completed
- [ ] Reduce motion test completed

#### Manual Checks (Android)
- [ ] TalkBack test completed on physical device
- [ ] Keyboard navigation test completed
- [ ] Font size test completed (largest setting)
- [ ] High contrast test completed
- [ ] Remove animations test completed

#### Kid Mode Specific
- [ ] All Kid Mode screens pass accessibility tests
- [ ] Touch targets are 56x56pt minimum
- [ ] Language is age-appropriate and clear
- [ ] Visual aids have text alternatives

#### Documentation
- [ ] Known accessibility issues documented
- [ ] Workarounds documented (if any)
- [ ] Accessibility statement updated
- [ ] Release notes include accessibility improvements

---

## Issue Reporting

### Accessibility Issue Template

```markdown
## Accessibility Issue

**Severity**: [Critical / High / Medium / Low]
**WCAG Criterion**: [e.g., 1.4.3 Contrast (Minimum)]
**Platform**: [iOS / Android / Both]
**Screen**: [e.g., Home Screen, Pattern Generator]

### Description
[Clear description of the issue]

### Steps to Reproduce
1. Enable [VoiceOver / TalkBack / specific setting]
2. Navigate to [screen]
3. Perform [action]
4. Observe [problem]

### Expected Behavior
[What should happen]

### Actual Behavior
[What actually happens]

### Screenshots/Videos
[If applicable]

### Device Information
- Device: [iPhone 15 Pro / Pixel 8 / etc.]
- OS Version: [iOS 17.1 / Android 14 / etc.]
- App Version: [1.0.0]

### Suggested Fix
[If known]

### Related Issues
[Link to related issues]
```

### Severity Definitions

| Severity | Definition | Examples |
|----------|------------|----------|
| **Critical** | Completely blocks accessibility for some users | No screen reader labels, keyboard trap, < 3:1 contrast |
| **High** | Major barrier but workaround exists | Difficult navigation, poor labels, < 4.5:1 text contrast |
| **Medium** | Frustrating but manageable | Suboptimal labels, minor navigation issues |
| **Low** | Minor inconvenience | Slightly awkward wording, non-critical missing hints |

### Issue Tracking

Create issues with label: `accessibility`

**Priority Order:**
1. Critical + Production → Immediate fix
2. Critical + Pre-release → Block release
3. High → Next sprint
4. Medium → Backlog (prioritize for next major release)
5. Low → Backlog (address as time allows)

---

## Accessibility Regression Prevention

### PR Checklist

Every PR that touches UI must include:

- [ ] Accessibility props added/updated for new interactive elements
- [ ] Color contrast verified for new color combinations
- [ ] Touch targets meet minimum size requirements
- [ ] Screen reader labels tested (VoiceOver or TalkBack)
- [ ] Keyboard navigation tested (if applicable)
- [ ] Accessibility unit tests added/updated

### Continuous Monitoring

**Weekly:**
- Review accessibility ESLint warnings
- Address new accessibility issues

**Bi-weekly:**
- Spot check random screens with screen reader
- Review accessibility backlog

**Quarterly:**
- Full accessibility audit
- Update documentation
- Review and update testing procedures
- Team accessibility training refresh

---

## Resources

### Tools and Extensions

- [Xcode Accessibility Inspector](https://developer.apple.com/library/archive/documentation/Accessibility/Conceptual/AccessibilityMacOSX/OSXAXTestingApps.html)
- [Android Accessibility Scanner](https://play.google.com/store/apps/details?id=com.google.android.apps.accessibility.auditor)
- [Color Contrast Analyzer](https://www.tpgi.com/color-contrast-checker/)
- [React Native Testing Library](https://callstack.github.io/react-native-testing-library/)

### Learning Resources

- [React Native Accessibility](https://reactnative.dev/docs/accessibility)
- [iOS Accessibility](https://developer.apple.com/accessibility/)
- [Android Accessibility](https://developer.android.com/guide/topics/ui/accessibility)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

### Related Documentation

- [Accessibility Checklist](./accessibility-checklist.md)
- [Color Contrast Analysis](./color-contrast-analysis.md)

---

## Document History

| Date | Version | Author | Changes |
|------|---------|--------|---------|
| 2025-11-10 | 1.0 | Claude Code | Initial testing procedures document |

---

**Next Steps:**
1. Set up automated testing in CI/CD pipeline
2. Schedule team training on testing procedures
3. Create testing schedule (weekly, bi-weekly, quarterly)
4. Integrate accessibility testing into PR workflow
