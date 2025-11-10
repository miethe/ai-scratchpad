# Accessibility Checklist

## Overview

This document establishes the WCAG 2.1 AA accessibility baseline for the Knit-Wit React Native application. All features must meet these requirements before release.

**Target Compliance**: WCAG 2.1 Level AA
**Last Updated**: 2025-11-10
**Responsible Team**: Frontend, QA

## Quick Reference

| Category | Standard | Priority |
|----------|----------|----------|
| Color Contrast | WCAG 2.1 AA | Critical |
| Touch Targets | 44x44pt minimum | Critical |
| Screen Reader | Full coverage | Critical |
| Keyboard Nav | External keyboard support | High |
| Focus Indicators | Visible on all interactive elements | High |
| Text Scaling | 200% without loss of functionality | High |

---

## 1. Color and Contrast

### 1.1 Text Contrast Requirements

**WCAG 2.1 AA Standards:**
- ✓ Normal text (< 18pt or < 14pt bold): **4.5:1 minimum**
- ✓ Large text (≥ 18pt or ≥ 14pt bold): **3:1 minimum**
- ✓ UI components and graphics: **3:1 minimum**

**Checklist:**

- [ ] All primary text (textPrimary) meets 4.5:1 contrast ratio
- [ ] All secondary text (textSecondary) meets 4.5:1 contrast ratio
- [ ] Large headings meet 3:1 minimum contrast ratio
- [ ] Interactive elements meet 3:1 minimum contrast ratio
- [ ] Error messages are distinguishable without color alone
- [ ] Success messages are distinguishable without color alone
- [ ] Focus indicators have 3:1 contrast against adjacent colors

### 1.2 Color Usage

- [ ] Color is not the only means of conveying information
- [ ] Status indicators use icons or text in addition to color
- [ ] Charts and diagrams use patterns or labels alongside color
- [ ] Links are distinguishable by more than color alone
- [ ] Kid Mode colors maintain WCAG AA compliance

**Reference**: See [Color Contrast Analysis](./color-contrast-analysis.md) for detailed calculations.

---

## 2. Typography and Readability

### 2.1 Font Requirements

**Base Font Sizes:**
- Body text: 16px minimum (bodyLarge)
- Small text: 14px minimum (bodyMedium)
- Labels: 12px minimum (labelMedium)
- Minimum allowed: 11px (labelSmall - use sparingly)

**Checklist:**

- [ ] Body text uses 16px (bodyLarge) as default
- [ ] Line height is at least 1.5x font size for body text
- [ ] Paragraph spacing is at least 2x font size
- [ ] Letter spacing is at least 0.12x font size
- [ ] Word spacing is at least 0.16x font size

### 2.2 Text Scaling

React Native supports text scaling via `allowFontScaling` prop.

- [ ] All text components have `allowFontScaling={true}` (default)
- [ ] Text scales up to 200% without horizontal scrolling
- [ ] Text scales up to 200% without text clipping
- [ ] UI layout adapts to larger text sizes
- [ ] Touch targets remain accessible at 200% scale
- [ ] Critical information remains visible at 200% scale

**Testing:**
```bash
# iOS: Settings → Accessibility → Display & Text Size → Larger Text
# Android: Settings → Display → Font size → Largest
```

### 2.3 Font Weight and Style

- [ ] Regular (400) used for body text
- [ ] Medium (500-600) used for emphasis
- [ ] Bold (700) used for headings
- [ ] No text relies solely on font style (italic) for meaning
- [ ] Font weights meet minimum contrast requirements

---

## 3. Touch Targets and Interactive Elements

### 3.1 Minimum Touch Target Sizes

**Standards:**
- iOS: 44x44 points minimum
- Android: 48x48 dp minimum
- Kid Mode: 56x56 points minimum

**Checklist:**

- [ ] All buttons meet 44x44pt minimum
- [ ] All interactive icons meet 44x44pt minimum
- [ ] All form inputs meet 44x44pt minimum
- [ ] All checkboxes and radio buttons meet 44x44pt minimum
- [ ] All sliders and interactive controls meet 44x44pt minimum
- [ ] Kid Mode interactive elements meet 56x56pt minimum
- [ ] Touch targets have adequate spacing (8px minimum between)

### 3.2 Touch Feedback

- [ ] All interactive elements provide visual feedback on touch
- [ ] Buttons show active/pressed state
- [ ] Links show active/pressed state
- [ ] Form inputs show focus state
- [ ] Loading states are clearly indicated
- [ ] Disabled states are visually distinct and non-interactive

---

## 4. Screen Reader Support

### 4.1 React Native Accessibility Props

All interactive elements must have appropriate accessibility props:

```typescript
<TouchableOpacity
  accessible={true}
  accessibilityLabel="Generate sphere pattern"
  accessibilityHint="Creates a new crochet pattern for a sphere shape"
  accessibilityRole="button"
  accessibilityState={{ disabled: false }}
/>
```

**Checklist:**

- [ ] All interactive elements have `accessible={true}`
- [ ] All buttons have descriptive `accessibilityLabel`
- [ ] All buttons have appropriate `accessibilityRole`
- [ ] Complex interactions have `accessibilityHint`
- [ ] Form inputs have associated labels
- [ ] Images have `accessibilityLabel` or are marked decorative
- [ ] Dynamic content changes are announced
- [ ] Error messages are announced to screen readers
- [ ] Loading states are announced to screen readers

### 4.2 Screen Reader Testing

**iOS VoiceOver:**
- [ ] All screens are navigable with VoiceOver
- [ ] Content is read in logical order
- [ ] Interactive elements are announced correctly
- [ ] Custom components have proper labels
- [ ] Gestures work with VoiceOver enabled

**Android TalkBack:**
- [ ] All screens are navigable with TalkBack
- [ ] Content is read in logical order
- [ ] Interactive elements are announced correctly
- [ ] Custom components have proper labels
- [ ] Gestures work with TalkBack enabled

### 4.3 Content Reading Order

- [ ] Content reading order matches visual order
- [ ] Headings are properly structured (h1 → h2 → h3)
- [ ] Lists are properly announced
- [ ] Tables (if used) have proper headers
- [ ] Forms have logical tab order

---

## 5. Keyboard Navigation

### 5.1 External Keyboard Support

React Native apps should support external keyboards on both iOS and Android.

**Checklist:**

- [ ] All interactive elements are keyboard accessible
- [ ] Tab order is logical and predictable
- [ ] Tab navigation cycles through all interactive elements
- [ ] Shift+Tab navigates backwards
- [ ] Enter/Space activates buttons
- [ ] Escape dismisses modals/dialogs
- [ ] Arrow keys navigate within components (dropdowns, lists)
- [ ] No keyboard traps (users can navigate away)

### 5.2 Focus Management

- [ ] Focus indicator is clearly visible (3:1 contrast minimum)
- [ ] Focus indicator has adequate thickness (2px minimum)
- [ ] Focus moves logically through the interface
- [ ] Focus is trapped within modals until dismissed
- [ ] Focus returns to trigger element when modal closes
- [ ] Skip navigation links provided for long content

---

## 6. Forms and Input

### 6.1 Form Accessibility

- [ ] All form inputs have associated labels
- [ ] Labels are visible and persistent (not placeholder-only)
- [ ] Required fields are clearly marked
- [ ] Error messages are associated with inputs
- [ ] Error messages explain how to fix the issue
- [ ] Success feedback is provided on form submission
- [ ] Form validation is accessible to screen readers

### 6.2 Input Types and Validation

- [ ] Appropriate keyboard types for input (numeric, email, etc.)
- [ ] Input constraints are communicated to users
- [ ] Autocomplete attributes used where appropriate
- [ ] Error prevention: confirmations for destructive actions
- [ ] Adequate time for form completion (no aggressive timeouts)

---

## 7. Content and Media

### 7.1 Images and Graphics

- [ ] All informative images have `accessibilityLabel`
- [ ] Decorative images have `accessibilityRole="none"` or `accessible={false}`
- [ ] Complex images (diagrams, charts) have text alternatives
- [ ] SVG pattern visualizations have text descriptions
- [ ] Alternative text is concise and descriptive
- [ ] Icons have labels or are supplemented with text

### 7.2 Text Content

- [ ] Language is set correctly (`accessibilityLanguage`)
- [ ] Headings are used to organize content
- [ ] Lists are properly structured
- [ ] Instructions do not rely on sensory characteristics (shape, position)
- [ ] No flashing content (seizure risk: < 3 flashes/second)
- [ ] Animations respect `prefers-reduced-motion` setting

---

## 8. Navigation and Wayfinding

### 8.1 Navigation Structure

- [ ] Navigation is consistent across screens
- [ ] Current location is clearly indicated
- [ ] Navigation labels are clear and descriptive
- [ ] Back navigation is available and predictable
- [ ] Breadcrumbs provided for deep navigation (if applicable)

### 8.2 Headings and Landmarks

- [ ] Each screen has a clear heading
- [ ] Headings form a logical hierarchy
- [ ] Major sections have appropriate headings
- [ ] Navigation landmarks are properly identified

---

## 9. Kid Mode Accessibility

Kid Mode has enhanced accessibility requirements for younger users and beginners.

### 9.1 Kid Mode Requirements

- [ ] Touch targets are 56x56pt minimum
- [ ] Color contrast meets WCAG AA (brighter palette validated)
- [ ] Fonts are larger (18px minimum for body text)
- [ ] Language is simplified and age-appropriate
- [ ] Instructions include visual aids
- [ ] Error messages are friendly and constructive
- [ ] Animations are slower and more deliberate
- [ ] Reduced cognitive load (fewer options visible)

---

## 10. Testing and Validation

### 10.1 Automated Testing Tools

**React Native:**
- [ ] `@testing-library/react-native` accessibility queries
- [ ] `jest-native` accessibility matchers
- [ ] ESLint plugin: `eslint-plugin-react-native-a11y`

**Platform-Specific:**
- [ ] iOS: Xcode Accessibility Inspector
- [ ] Android: Accessibility Scanner

**Cross-Platform:**
- [ ] axe DevTools Mobile (if available)
- [ ] Manual testing with actual devices

### 10.2 Manual Testing Checklist

**Screen Readers:**
- [ ] Test with iOS VoiceOver
- [ ] Test with Android TalkBack
- [ ] Test with external keyboard (iOS + Android)

**Visual Testing:**
- [ ] Test at 200% text scale
- [ ] Test with Display Accommodations (color filters, reduce transparency)
- [ ] Test with Reduce Motion enabled
- [ ] Test in bright sunlight (outdoor visibility)
- [ ] Test with low vision conditions

**Platform Settings:**
- [ ] iOS: Accessibility → Display & Text Size → Bold Text
- [ ] iOS: Accessibility → Motion → Reduce Motion
- [ ] Android: Accessibility → Font size
- [ ] Android: Accessibility → Remove animations

### 10.3 Testing Procedures

**Reference**: See [Testing Procedures](./testing-procedures.md) for detailed testing workflows.

---

## 11. Compliance Verification

### 11.1 Pre-Release Checklist

Before any release:

- [ ] Automated accessibility tests pass
- [ ] Manual screen reader testing completed
- [ ] Color contrast validation completed
- [ ] Keyboard navigation tested
- [ ] Text scaling tested (up to 200%)
- [ ] Kid Mode accessibility verified
- [ ] Documentation updated

### 11.2 Ongoing Monitoring

- [ ] Accessibility review included in PR checklist
- [ ] Automated tests run in CI/CD pipeline
- [ ] Quarterly accessibility audits scheduled
- [ ] User feedback on accessibility collected

---

## 12. Resources and References

### 12.1 WCAG Guidelines

- [WCAG 2.1 AA Guidelines](https://www.w3.org/WAI/WCAG21/quickref/?currentsidebar=%23col_customize&levels=aaa)
- [Understanding WCAG 2.1](https://www.w3.org/WAI/WCAG21/Understanding/)

### 12.2 React Native Accessibility

- [React Native Accessibility API](https://reactnative.dev/docs/accessibility)
- [React Native Accessibility Props](https://reactnative.dev/docs/accessibility#accessibility-properties)

### 12.3 Platform Guidelines

- [iOS Human Interface Guidelines - Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)
- [Android Accessibility Guidelines](https://developer.android.com/guide/topics/ui/accessibility)

### 12.4 Testing Tools

- [Xcode Accessibility Inspector](https://developer.apple.com/library/archive/documentation/Accessibility/Conceptual/AccessibilityMacOSX/OSXAXTestingApps.html)
- [Android Accessibility Scanner](https://play.google.com/store/apps/details?id=com.google.android.apps.accessibility.auditor)
- [Color Contrast Analyzer](https://www.tpgi.com/color-contrast-checker/)

### 12.5 Internal Documentation

- [Color Contrast Analysis](./color-contrast-analysis.md) - Detailed color validation
- [Testing Procedures](./testing-procedures.md) - Step-by-step testing workflows
- [Theme System](../../apps/mobile/src/theme/README.md) - Design system documentation

---

## Appendix A: Common Accessibility Issues

### Issue: Color Contrast Failures

**Problem**: Text or interactive elements don't meet 4.5:1 or 3:1 ratios.

**Solution**:
- Use darker text colors on light backgrounds
- Use lighter text colors on dark backgrounds
- Verify with Color Contrast Analyzer tool
- Reference approved color combinations in `color-contrast-analysis.md`

### Issue: Missing Accessibility Labels

**Problem**: Screen readers can't identify interactive elements.

**Solution**:
```typescript
// Bad
<TouchableOpacity onPress={handlePress}>
  <Icon name="plus" />
</TouchableOpacity>

// Good
<TouchableOpacity
  onPress={handlePress}
  accessible={true}
  accessibilityLabel="Add new pattern"
  accessibilityRole="button"
>
  <Icon name="plus" />
</TouchableOpacity>
```

### Issue: Small Touch Targets

**Problem**: Interactive elements are too small to tap accurately.

**Solution**:
```typescript
import { touchTargets } from '@/theme';

// Use minimum touch target size
<TouchableOpacity
  style={{
    minWidth: touchTargets.minimum,
    minHeight: touchTargets.minimum
  }}
>
  {/* Content */}
</TouchableOpacity>
```

### Issue: Text Scaling Breaks Layout

**Problem**: UI breaks when text is scaled to 200%.

**Solution**:
- Use flexible layouts (flexbox)
- Avoid fixed heights on text containers
- Test at maximum text scale
- Use `adjustsFontSizeToFit` sparingly for labels that must fit

---

## Appendix B: Accessibility Props Quick Reference

### Essential React Native Accessibility Props

| Prop | Purpose | Example |
|------|---------|---------|
| `accessible` | Marks element as accessible | `accessible={true}` |
| `accessibilityLabel` | Screen reader text | `accessibilityLabel="Generate pattern"` |
| `accessibilityHint` | Additional context | `accessibilityHint="Opens pattern generator"` |
| `accessibilityRole` | Element type | `accessibilityRole="button"` |
| `accessibilityState` | Current state | `accessibilityState={{ disabled: true }}` |
| `accessibilityValue` | Current value | `accessibilityValue={{ now: 50, min: 0, max: 100 }}` |
| `importantForAccessibility` | Visibility to screen readers | `importantForAccessibility="no"` |

### Common Accessibility Roles

- `button` - Clickable buttons
- `link` - Navigation links
- `header` - Section headers
- `text` - Static text
- `image` - Images
- `imagebutton` - Clickable images
- `adjustable` - Sliders, steppers
- `search` - Search inputs
- `checkbox` - Checkboxes
- `radio` - Radio buttons
- `none` - Decorative elements

---

## Document History

| Date | Version | Author | Changes |
|------|---------|--------|---------|
| 2025-11-10 | 1.0 | Claude Code | Initial accessibility baseline |

---

**Next Steps:**
1. Review and validate all color combinations → [Color Contrast Analysis](./color-contrast-analysis.md)
2. Set up automated testing → [Testing Procedures](./testing-procedures.md)
3. Integrate accessibility checks into PR workflow
4. Schedule team training on WCAG AA compliance
