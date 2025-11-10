# Accessibility Documentation

This directory contains comprehensive accessibility documentation for the Knit-Wit React Native application, targeting WCAG 2.1 Level AA compliance.

## Quick Start

**New to accessibility?** Start here:
1. Read [Accessibility Checklist](./accessibility-checklist.md) - Overview of all requirements
2. Review [Color Contrast Analysis](./color-contrast-analysis.md) - Safe color combinations
3. Follow [Testing Procedures](./testing-procedures.md) - How to test accessibility

**Before creating a PR:** Review the PR checklist in [Testing Procedures](./testing-procedures.md#pr-checklist)

**Before release:** Complete the [Pre-Release Checklist](./testing-procedures.md#pre-release-checklist)

---

## Documents Overview

### [Accessibility Checklist](./accessibility-checklist.md)
**Purpose**: Complete WCAG 2.1 AA baseline and implementation checklist

**Use this when:**
- Starting work on a new feature
- Reviewing accessibility requirements
- Conducting accessibility audits
- Training new team members

**Key Sections:**
- Color and contrast requirements
- Typography and readability standards
- Touch target sizes
- Screen reader support
- Keyboard navigation
- Forms and input accessibility
- Kid Mode requirements
- Testing and validation

---

### [Color Contrast Analysis](./color-contrast-analysis.md)
**Purpose**: Detailed color validation with calculated WCAG ratios

**Use this when:**
- Choosing colors for new UI elements
- Validating design mockups
- Debugging contrast issues
- Creating new theme variants

**Key Sections:**
- Complete color palette with contrast ratios
- Text on light backgrounds validation
- Brand colors accessibility analysis
- Semantic colors (success, warning, error, info)
- Kid Mode color issues and fixes
- Safe color combinations reference
- Action items for critical issues

**Critical Findings:**
- ✗ Kid Mode colors fail WCAG AA on designated backgrounds
- ✗ Default border color (gray200) insufficient contrast
- ✗ Warning color (#F59E0B) cannot be used for text
- ⚠️ textTertiary (gray400) only valid for large text (≥18pt)

---

### [Testing Procedures](./testing-procedures.md)
**Purpose**: Step-by-step testing workflows and tool setup

**Use this when:**
- Setting up local testing environment
- Testing new features for accessibility
- Preparing for release
- Investigating accessibility bugs
- Training QA team

**Key Sections:**
- Testing tools setup (iOS, Android, automated)
- Automated testing with React Native Testing Library
- Screen reader testing (VoiceOver, TalkBack)
- Keyboard navigation testing
- Visual accessibility testing (text scaling, color filters)
- Pre-release checklist
- Issue reporting template

---

## Quick Reference

### WCAG 2.1 AA Requirements

| Category | Requirement | How to Test |
|----------|-------------|-------------|
| **Text Contrast** | 4.5:1 minimum (normal text) | Color Contrast Analyzer |
| **Large Text Contrast** | 3:1 minimum (≥18pt) | Color Contrast Analyzer |
| **UI Components** | 3:1 minimum | Color Contrast Analyzer |
| **Touch Targets** | 44x44pt minimum | Manual inspection |
| **Kid Mode Targets** | 56x56pt minimum | Manual inspection |
| **Screen Reader** | Full navigation | VoiceOver/TalkBack |
| **Keyboard Nav** | All interactive elements | External keyboard |
| **Text Scaling** | 200% without loss | iOS/Android settings |

### Safe Color Combinations

**Text on Light Backgrounds (4.5:1+):**
- textPrimary (gray900) on white - **15.3:1** ✓
- textSecondary (gray500) on white - **4.6:1** ✓
- gray600 on white - **7.2:1** ✓
- primaryDark on white - **5.7:1** ✓
- secondaryDark on white - **5.2:1** ✓

**Large Text on Light Backgrounds (3:1+):**
- All above, plus:
- primary (#6B4EFF) on white - **3.7:1** ✓
- secondary (#FF6B9D) on white - **3.4:1** ✓
- error (#EF4444) on white - **3.9:1** ✓

**Avoid for Text:**
- ✗ textTertiary (gray400) for normal text - **3.2:1** (large text only)
- ✗ success (#10B981) - **3.0:1** (UI components only)
- ✗ warning (#F59E0B) - **2.2:1** (insufficient)
- ✗ All Kid Mode colors on kidBackground (see analysis doc)

### Common Accessibility Props

```typescript
<TouchableOpacity
  accessible={true}
  accessibilityLabel="Generate sphere pattern"
  accessibilityHint="Creates a new crochet pattern for a sphere shape"
  accessibilityRole="button"
  accessibilityState={{ disabled: false }}
>
  {/* Content */}
</TouchableOpacity>
```

### Testing Commands

```bash
# Run accessibility tests
pnpm test -- --testPathPattern=accessibility

# Lint accessibility
pnpm lint

# Run on device
pnpm --filter mobile ios
pnpm --filter mobile android
```

---

## Critical Action Items

Based on the [Color Contrast Analysis](./color-contrast-analysis.md), these issues must be addressed before launch:

### 1. Kid Mode Color Palette (Critical)
**Issue**: All Kid Mode colors fail WCAG AA on kidBackground
**Impact**: Kid Mode is not accessible to users with low vision
**Solution**: Implement Option B from analysis doc
- Use standard text colors (textPrimary, textSecondary)
- Apply Kid Mode styling through layout, spacing, and decorative elements
- Use bright colors for non-text UI elements only

**Files to update:**
- `/apps/mobile/src/theme/colors.ts` - Document Kid Mode usage
- Kid Mode screens - Update to use accessible text colors
- Kid Mode components - Larger sizes, simplified layouts

### 2. Default Border Color (Critical)
**Issue**: `border` (gray200) only achieves 1.2:1 contrast (needs 3:1)
**Impact**: Input fields and UI components invisible to some users
**Solution**: Update default border color

```typescript
// Current (FAILS)
border: '#E5E7EB', // gray200 - 1.2:1 contrast

// Recommended (PASSES)
border: '#9CA3AF', // gray400 - 3.2:1 contrast
```

**Files to update:**
- `/apps/mobile/src/theme/colors.ts`
- All components using `colors.border`

### 3. Semantic Color Usage (High Priority)
**Issue**: Warning, success colors fail as text colors
**Impact**: Error/success messages may not be readable
**Solution**: Always pair with accessible text color

```typescript
// Bad
<Text style={{ color: colors.warning }}>Warning message</Text>

// Good
<View style={{ backgroundColor: colors.warning }}>
  <Text style={{ color: colors.gray900 }}>Warning message</Text>
</View>

// Better
<View style={{ flexDirection: 'row', alignItems: 'center' }}>
  <Icon name="warning" color={colors.warning} />
  <Text style={{ color: colors.gray900 }}>Warning message</Text>
</View>
```

**Files to update:**
- Create reusable Alert/Message components with proper contrast
- Audit all usages of semantic colors

---

## Development Workflow

### For New Features

1. **Design Phase**
   - Choose colors from [Safe Color Combinations](./color-contrast-analysis.md#safe-color-combinations)
   - Ensure touch targets meet minimum sizes (44x44pt, 56x56pt for Kid Mode)
   - Plan keyboard navigation flow
   - Design screen reader experience

2. **Implementation Phase**
   - Add accessibility props to all interactive elements
   - Use semantic HTML/RN roles
   - Implement keyboard event handlers
   - Add accessibility tests

3. **Testing Phase**
   - Run automated accessibility tests
   - Test with VoiceOver (iOS) and TalkBack (Android)
   - Test keyboard navigation
   - Test at 200% text scale
   - Test with color filters enabled

4. **PR Phase**
   - Complete [PR Checklist](./testing-procedures.md#pr-checklist)
   - Document any accessibility considerations in PR description
   - Address reviewer feedback on accessibility

### For Bug Fixes

1. **Identify Issue**
   - Use [Issue Reporting Template](./testing-procedures.md#accessibility-issue-template)
   - Determine severity and WCAG criterion
   - Test on both iOS and Android

2. **Fix and Verify**
   - Implement fix
   - Add regression test
   - Verify fix with same testing method that found issue

3. **Prevent Regression**
   - Add automated test if possible
   - Update documentation if needed
   - Share learnings with team

---

## Testing Schedule

### Every PR
- Automated accessibility tests pass
- ESLint accessibility rules pass
- Manual spot check of changed screens

### Weekly
- Review accessibility ESLint warnings
- Spot check random screens with screen reader
- Address new accessibility issues

### Pre-Release
- Complete [Pre-Release Checklist](./testing-procedures.md#pre-release-checklist)
- Full screen reader test (iOS and Android)
- Full keyboard navigation test
- Text scaling test (200%)
- Display accommodations test

### Quarterly
- Comprehensive accessibility audit
- Update accessibility documentation
- Team training refresh
- Review and update safe color combinations
- Accessibility backlog grooming

---

## Resources

### Internal Documentation
- [Theme System](../../apps/mobile/src/theme/) - Color palette and typography
- [Component Library](../../apps/mobile/src/components/) - Accessible components
- [CLAUDE.md](../../CLAUDE.md) - Project-specific guidance

### WCAG Guidelines
- [WCAG 2.1 Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/)
- [Understanding WCAG 2.1](https://www.w3.org/WAI/WCAG21/Understanding/)
- [How to Meet WCAG](https://www.w3.org/WAI/WCAG21/quickref/)

### React Native Accessibility
- [React Native Accessibility API](https://reactnative.dev/docs/accessibility)
- [Accessibility Props](https://reactnative.dev/docs/accessibility#accessibility-properties)

### Platform Guidelines
- [iOS Accessibility](https://developer.apple.com/accessibility/)
- [Android Accessibility](https://developer.android.com/guide/topics/ui/accessibility)

### Testing Tools
- [Xcode Accessibility Inspector](https://developer.apple.com/library/archive/documentation/Accessibility/Conceptual/AccessibilityMacOSX/OSXAXTestingApps.html)
- [Android Accessibility Scanner](https://play.google.com/store/apps/details?id=com.google.android.apps.accessibility.auditor)
- [Color Contrast Analyzer](https://www.tpgi.com/color-contrast-checker/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)

### Learning Resources
- [Web Accessibility Initiative (WAI)](https://www.w3.org/WAI/)
- [A11y Project](https://www.a11yproject.com/)
- [Deque University](https://dequeuniversity.com/)

---

## Support

### Questions?
- Review documentation in this directory
- Check [CLAUDE.md](../../CLAUDE.md) for project patterns
- Ask in team chat with `#accessibility` tag
- Consult with accessibility specialist (if available)

### Found an Issue?
- Use [Issue Reporting Template](./testing-procedures.md#accessibility-issue-template)
- Label issue with `accessibility` tag
- Set severity (Critical/High/Medium/Low)
- Assign to appropriate milestone

### Accessibility Champions
- Each team should have an accessibility champion
- Champions: Review PRs for accessibility, provide guidance, stay updated on WCAG

---

## Document History

| Date | Version | Author | Changes |
|------|---------|--------|---------|
| 2025-11-10 | 1.0 | Claude Code | Initial accessibility documentation suite |

---

## Next Steps

1. **Immediate** (Before next PR):
   - Review critical action items above
   - Set up testing tools on your device
   - Run automated accessibility tests

2. **This Sprint**:
   - Fix Kid Mode color palette (Option B)
   - Update default border color
   - Audit semantic color usage
   - Create reusable Alert/Message components

3. **Next Sprint**:
   - Implement automated contrast checking in development
   - Add accessibility tests to CI/CD pipeline
   - Create component library with pre-validated variants
   - Schedule team accessibility training

4. **Ongoing**:
   - Follow development workflow for all new features
   - Complete testing schedule (weekly, pre-release, quarterly)
   - Keep documentation updated
   - Share learnings with team
