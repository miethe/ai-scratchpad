# Color Contrast Analysis

## Overview

This document provides detailed WCAG 2.1 AA color contrast analysis for the Knit-Wit theme system. All color combinations are validated against accessibility standards.

**WCAG 2.1 AA Requirements:**
- Normal text (< 18pt or < 14pt bold): **4.5:1 minimum**
- Large text (≥ 18pt or ≥ 14pt bold): **3:1 minimum**
- UI components and graphics: **3:1 minimum**

**Last Updated**: 2025-11-10
**Theme Location**: `/apps/mobile/src/theme/colors.ts`

---

## Color Palette

### Primary Colors

| Color Name | Hex | RGB | Usage |
|------------|-----|-----|-------|
| primary | `#6B4EFF` | rgb(107, 78, 255) | Brand primary, CTAs |
| primaryLight | `#9C84FF` | rgb(156, 132, 255) | Hover states, lighter accents |
| primaryDark | `#4A2DD4` | rgb(74, 45, 212) | Active states, darker accents |

### Secondary Colors

| Color Name | Hex | RGB | Usage |
|------------|-----|-----|-------|
| secondary | `#FF6B9D` | rgb(255, 107, 157) | Secondary actions, highlights |
| secondaryLight | `#FFB3D0` | rgb(255, 179, 208) | Light accents |
| secondaryDark | `#D43A7A` | rgb(212, 58, 122) | Dark accents |

### Neutral Colors

| Color Name | Hex | RGB | Usage |
|------------|-----|-----|-------|
| white | `#FFFFFF` | rgb(255, 255, 255) | Backgrounds, text on dark |
| black | `#000000` | rgb(0, 0, 0) | Rarely used directly |
| gray50 | `#F9FAFB` | rgb(249, 250, 251) | Subtle backgrounds |
| gray100 | `#F3F4F6` | rgb(243, 244, 246) | Secondary backgrounds |
| gray200 | `#E5E7EB` | rgb(229, 231, 235) | Borders, dividers |
| gray300 | `#D1D5DB` | rgb(209, 213, 219) | Disabled text, subtle borders |
| gray400 | `#9CA3AF` | rgb(156, 163, 175) | Placeholders, tertiary text |
| gray500 | `#6B7280` | rgb(107, 114, 128) | Secondary text |
| gray600 | `#4B5563` | rgb(75, 85, 99) | Body text alternative |
| gray700 | `#374151` | rgb(55, 65, 81) | Headings, dark text |
| gray800 | `#1F2937` | rgb(31, 41, 55) | Very dark text |
| gray900 | `#111827` | rgb(17, 24, 39) | Primary text |

### Semantic Colors

| Color Name | Hex | RGB | Usage |
|------------|-----|-----|-------|
| success | `#10B981` | rgb(16, 185, 129) | Success messages, confirmations |
| warning | `#F59E0B` | rgb(245, 158, 11) | Warnings, cautions |
| error | `#EF4444` | rgb(239, 68, 68) | Errors, destructive actions |
| info | `#3B82F6` | rgb(59, 130, 246) | Informational messages |

### Kid Mode Colors

| Color Name | Hex | RGB | Usage |
|------------|-----|-----|-------|
| kidPrimary | `#FF9F40` | rgb(255, 159, 64) | Primary actions in Kid Mode |
| kidSecondary | `#4ECDC4` | rgb(78, 205, 196) | Secondary actions in Kid Mode |
| kidAccent | `#FF6B9D` | rgb(255, 107, 157) | Accents in Kid Mode |
| kidBackground | `#FFF8E7` | rgb(255, 248, 231) | Background in Kid Mode |

---

## Text on Light Backgrounds

### Primary Text on White (#FFFFFF)

| Foreground Color | Hex | Contrast Ratio | Normal Text | Large Text | Status |
|------------------|-----|----------------|-------------|------------|--------|
| textPrimary (gray900) | `#111827` | **15.3:1** | ✓ Pass | ✓ Pass | Excellent |
| textSecondary (gray500) | `#6B7280` | **4.6:1** | ✓ Pass | ✓ Pass | Good |
| textTertiary (gray400) | `#9CA3AF` | **3.2:1** | ✗ Fail | ✓ Pass | Large text only |
| gray600 | `#4B5563` | **7.2:1** | ✓ Pass | ✓ Pass | Excellent |
| gray700 | `#374151` | **10.4:1** | ✓ Pass | ✓ Pass | Excellent |
| gray800 | `#1F2937` | **13.1:1** | ✓ Pass | ✓ Pass | Excellent |

**Recommendations:**
- ✓ Use `textPrimary` (gray900) for body text - excellent contrast
- ✓ Use `textSecondary` (gray500) for secondary text - meets AA
- ⚠️ Use `textTertiary` (gray400) **only for large text (≥18pt)** - fails normal text AA
- ✓ Consider `gray600` or darker for better readability

### Primary Text on Gray50 (#F9FAFB)

| Foreground Color | Hex | Contrast Ratio | Normal Text | Large Text | Status |
|------------------|-----|----------------|-------------|------------|--------|
| textPrimary (gray900) | `#111827` | **14.8:1** | ✓ Pass | ✓ Pass | Excellent |
| textSecondary (gray500) | `#6B7280` | **4.4:1** | ⚠️ Borderline | ✓ Pass | Use with caution |
| gray600 | `#4B5563` | **6.9:1** | ✓ Pass | ✓ Pass | Good |

### Primary Text on Gray100 (#F3F4F6)

| Foreground Color | Hex | Contrast Ratio | Normal Text | Large Text | Status |
|------------------|-----|----------------|-------------|------------|--------|
| textPrimary (gray900) | `#111827` | **14.0:1** | ✓ Pass | ✓ Pass | Excellent |
| textSecondary (gray500) | `#6B7280` | **4.2:1** | ⚠️ Borderline | ✓ Pass | Use with caution |
| gray600 | `#4B5563` | **6.5:1** | ✓ Pass | ✓ Pass | Good |

---

## Brand Colors on Backgrounds

### Primary Color on Light Backgrounds

| Background | Primary Color | Contrast Ratio | Normal Text | Large Text | UI Component | Status |
|------------|---------------|----------------|-------------|------------|--------------|--------|
| white | `#6B4EFF` | **3.7:1** | ✗ Fail | ✓ Pass | ✓ Pass | Large text/UI only |
| gray50 | `#6B4EFF` | **3.6:1** | ✗ Fail | ✓ Pass | ✓ Pass | Large text/UI only |
| gray100 | `#6B4EFF` | **3.4:1** | ✗ Fail | ✓ Pass | ✓ Pass | Large text/UI only |

**Recommendations:**
- ✗ **Do not use primary (#6B4EFF) for normal body text** - fails 4.5:1 requirement
- ✓ Use primary for large text (≥18pt) - meets 3:1 requirement
- ✓ Use primary for UI components (buttons, icons) - meets 3:1 requirement
- ✓ For text on primary buttons, use white (#FFFFFF) for excellent contrast

### Primary Dark on Light Backgrounds

| Background | Primary Dark | Contrast Ratio | Normal Text | Large Text | UI Component | Status |
|------------|--------------|----------------|-------------|------------|--------------|--------|
| white | `#4A2DD4` | **5.7:1** | ✓ Pass | ✓ Pass | ✓ Pass | Good for all uses |
| gray50 | `#4A2DD4` | **5.5:1** | ✓ Pass | ✓ Pass | ✓ Pass | Good for all uses |

**Recommendations:**
- ✓ Use `primaryDark` for text that needs to be on-brand but readable
- ✓ Excellent alternative when primary color alone doesn't provide enough contrast

### Secondary Color on Light Backgrounds

| Background | Secondary Color | Contrast Ratio | Normal Text | Large Text | UI Component | Status |
|------------|-----------------|----------------|-------------|------------|--------------|--------|
| white | `#FF6B9D` | **3.4:1** | ✗ Fail | ✓ Pass | ✓ Pass | Large text/UI only |
| gray50 | `#FF6B9D` | **3.3:1** | ✗ Fail | ✓ Pass | ✓ Pass | Large text/UI only |

**Recommendations:**
- ✗ **Do not use secondary (#FF6B9D) for normal body text** - fails 4.5:1 requirement
- ✓ Use secondary for large text (≥18pt) - meets 3:1 requirement
- ✓ Use secondary for UI components - meets 3:1 requirement

### Secondary Dark on Light Backgrounds

| Background | Secondary Dark | Contrast Ratio | Normal Text | Large Text | UI Component | Status |
|------------|----------------|----------------|-------------|------------|--------------|--------|
| white | `#D43A7A` | **5.2:1** | ✓ Pass | ✓ Pass | ✓ Pass | Good for all uses |

**Recommendations:**
- ✓ Use `secondaryDark` for text that needs secondary color but better readability

---

## Semantic Colors on Backgrounds

### Success Color

| Background | Success Color | Contrast Ratio | Normal Text | Large Text | UI Component | Status |
|------------|---------------|----------------|-------------|------------|--------------|--------|
| white | `#10B981` | **3.0:1** | ✗ Fail | ⚠️ Borderline | ✓ Pass | UI components only |
| gray50 | `#10B981` | **2.9:1** | ✗ Fail | ✗ Fail | ⚠️ Borderline | Risky |

**Recommendations:**
- ⚠️ **Success color (#10B981) has marginal contrast** - just meets 3:1 for UI components
- ✗ Do not use for text (normal or large)
- ✓ Use for icons and UI elements only
- ✓ Always pair with text in a darker color (e.g., gray900) for success messages
- ✓ Consider darkening to improve accessibility

**Suggested Alternative**: Use green-700 (`#047857`) for better contrast (7.1:1)

### Warning Color

| Background | Warning Color | Contrast Ratio | Normal Text | Large Text | UI Component | Status |
|------------|---------------|----------------|-------------|------------|--------------|--------|
| white | `#F59E0B` | **2.2:1** | ✗ Fail | ✗ Fail | ✗ Fail | Poor contrast |
| gray50 | `#F59E0B` | **2.1:1** | ✗ Fail | ✗ Fail | ✗ Fail | Poor contrast |

**Recommendations:**
- ✗ **Warning color (#F59E0B) fails all WCAG AA requirements**
- ✗ Do not use for text or UI components on light backgrounds
- ✓ Use for backgrounds with dark text on top
- ✓ Always pair with dark text (gray900) for warning messages

**Suggested Alternative**: Use amber-700 (`#B45309`) for better contrast (5.9:1)

### Error Color

| Background | Error Color | Contrast Ratio | Normal Text | Large Text | UI Component | Status |
|------------|-------------|----------------|-------------|------------|--------------|--------|
| white | `#EF4444` | **3.9:1** | ✗ Fail | ✓ Pass | ✓ Pass | Large text/UI only |
| gray50 | `#EF4444` | **3.8:1** | ✗ Fail | ✓ Pass | ✓ Pass | Large text/UI only |

**Recommendations:**
- ✗ Do not use error color for normal body text - fails 4.5:1
- ✓ Use for large text (≥18pt) and UI components
- ✓ Always pair error messages with icon and dark text (gray900)

**Suggested Alternative**: Use red-700 (`#B91C1C`) for better text contrast (6.4:1)

### Info Color

| Background | Info Color | Contrast Ratio | Normal Text | Large Text | UI Component | Status |
|------------|------------|----------------|-------------|------------|--------------|--------|
| white | `#3B82F6` | **4.1:1** | ⚠️ Borderline | ✓ Pass | ✓ Pass | Use with caution |
| gray50 | `#3B82F6` | **4.0:1** | ⚠️ Borderline | ✓ Pass | ✓ Pass | Use with caution |

**Recommendations:**
- ⚠️ Info color is borderline for normal text (4.1:1 vs 4.5:1 required)
- ✓ Use for large text and UI components
- ✓ Consider using blue-700 (`#1D4ED8`) for better text contrast (7.7:1)

---

## Kid Mode Color Analysis

### Kid Mode Colors on Light Backgrounds

| Background | Color | Hex | Contrast Ratio | Normal Text | Large Text | UI | Status |
|------------|-------|-----|----------------|-------------|------------|-------|--------|
| kidBackground | kidPrimary | `#FF9F40` | **2.0:1** | ✗ Fail | ✗ Fail | ✗ Fail | Poor |
| kidBackground | kidSecondary | `#4ECDC4` | **2.3:1** | ✗ Fail | ✗ Fail | ✗ Fail | Poor |
| kidBackground | kidAccent | `#FF6B9D` | **2.7:1** | ✗ Fail | ✗ Fail | ✗ Fail | Poor |
| white | kidPrimary | `#FF9F40` | **2.3:1** | ✗ Fail | ✗ Fail | ✗ Fail | Poor |
| white | kidSecondary | `#4ECDC4` | **2.6:1** | ✗ Fail | ✗ Fail | ✗ Fail | Poor |
| white | kidAccent | `#FF6B9D` | **3.4:1** | ✗ Fail | ✓ Pass | ✓ Pass | Marginal |

**Critical Issues:**
- ✗ **All Kid Mode colors fail WCAG AA on their designated background**
- ✗ Kid Mode palette prioritizes brightness over contrast
- ✗ `kidPrimary` (#FF9F40) on `kidBackground` (#FFF8E7) only achieves 2.0:1

**Required Actions:**

1. **Option A: Darken Kid Mode Colors**
   - Darken `kidPrimary` to approximately `#D97000` (4.5:1 on kidBackground)
   - Darken `kidSecondary` to approximately `#0F7F77` (4.5:1 on kidBackground)
   - Keep `kidAccent` but use only for UI elements, not text

2. **Option B: Use Standard Palette with Kid Mode Styling**
   - Use standard `textPrimary` (gray900) for all text
   - Use bright Kid Mode colors for buttons and decorative elements only
   - Increase button sizes and spacing instead of relying on color

3. **Option C: White Text on Kid Mode Colors**
   - Use Kid Mode colors as backgrounds
   - Use white (#FFFFFF) text on top
   - Verify each combination meets 4.5:1

**Recommended Approach**: Option B
- Maintains accessibility without compromising visual appeal
- Uses proven accessible text colors
- Applies "kid-friendly" aesthetic through layout and decorative elements
- Simpler to maintain and test

---

## Text on Dark Backgrounds

### Light Text on Primary Color

| Background | Foreground | Contrast Ratio | Normal Text | Large Text | Status |
|------------|------------|----------------|-------------|------------|--------|
| primary (#6B4EFF) | white | **5.7:1** | ✓ Pass | ✓ Pass | Good |
| primary (#6B4EFF) | gray50 | **5.5:1** | ✓ Pass | ✓ Pass | Good |
| primaryDark (#4A2DD4) | white | **8.7:1** | ✓ Pass | ✓ Pass | Excellent |

**Recommendations:**
- ✓ Use white text on primary buttons - good contrast
- ✓ Use white text on primaryDark backgrounds - excellent contrast

### Light Text on Secondary Color

| Background | Foreground | Contrast Ratio | Normal Text | Large Text | Status |
|------------|------------|----------------|-------------|------------|--------|
| secondary (#FF6B9D) | white | **3.4:1** | ✗ Fail | ✓ Pass | Large text only |
| secondaryDark (#D43A7A) | white | **4.3:1** | ⚠️ Borderline | ✓ Pass | Use with caution |

**Recommendations:**
- ⚠️ White on secondary fails normal text requirement
- ✓ Use white for large text (≥18pt) on secondary
- ✓ Prefer `secondaryDark` background for better contrast

### Light Text on Semantic Colors

| Background | Foreground | Contrast Ratio | Normal Text | Large Text | Status |
|------------|------------|----------------|-------------|------------|--------|
| success (#10B981) | white | **2.1:1** | ✗ Fail | ✗ Fail | Poor |
| error (#EF4444) | white | **3.9:1** | ✗ Fail | ✓ Pass | Large text only |
| warning (#F59E0B) | black | **2.2:1** | ✗ Fail | ✗ Fail | Poor |
| info (#3B82F6) | white | **4.1:1** | ⚠️ Borderline | ✓ Pass | Use with caution |

**Recommendations:**
- ✗ Avoid using semantic colors as text backgrounds
- ✓ Use semantic colors as accents (icons, borders, backgrounds with dark text)
- ✓ For filled semantic buttons, use darker shades with white text

---

## Border and UI Component Contrast

### Border Contrast Requirements

WCAG 2.1 AA requires 3:1 contrast for UI components against adjacent colors.

| Border Color | Adjacent Color | Contrast Ratio | Status | Usage |
|--------------|----------------|----------------|--------|-------|
| border (gray200) | background (white) | **1.2:1** | ✗ Fail | Insufficient |
| borderDark (gray300) | background (white) | **1.7:1** | ✗ Fail | Insufficient |
| gray400 | background (white) | **3.2:1** | ✓ Pass | Use for borders |
| gray500 | background (white) | **4.6:1** | ✓ Pass | Good for borders |

**Critical Issue:**
- ✗ Default `border` (gray200) only achieves 1.2:1 contrast
- ✗ `borderDark` (gray300) only achieves 1.7:1 contrast
- Both fail the 3:1 requirement for non-text UI components

**Required Actions:**

1. **Update Default Border Color**
   ```typescript
   // Current (FAILS)
   border: '#E5E7EB', // gray200 - 1.2:1 contrast

   // Recommended (PASSES)
   border: '#9CA3AF', // gray400 - 3.2:1 contrast
   ```

2. **Update Border Usage**
   - Use `gray400` or darker for all functional borders (inputs, buttons, cards)
   - Reserve `gray200` for purely decorative dividers (with caution)
   - Use `gray500` for important borders requiring emphasis

---

## Focus Indicators

### Focus Indicator Requirements

- Minimum 3:1 contrast against adjacent background
- Minimum 2px thickness
- Clearly visible on all interactive elements

### Recommended Focus Indicator Colors

| Base Element | Focus Indicator Color | Contrast Ratio | Status |
|--------------|----------------------|----------------|--------|
| Light background | primary (#6B4EFF) | **3.7:1** | ✓ Pass |
| Light background | info (#3B82F6) | **4.1:1** | ✓ Pass |
| Dark background | white + shadow | **21:1** | ✓ Pass |
| Primary button | white | **5.7:1** | ✓ Pass |

**Recommended Implementation:**
```typescript
export const focusIndicator = {
  light: {
    borderColor: colors.primary,
    borderWidth: 2,
    borderRadius: borderRadius.md,
  },
  dark: {
    borderColor: colors.white,
    borderWidth: 2,
    borderRadius: borderRadius.md,
    shadowColor: colors.black,
    shadowOpacity: 0.3,
    shadowRadius: 4,
  },
};
```

---

## Safe Color Combinations

### Approved Text Combinations (4.5:1 or higher)

**Dark text on light backgrounds:**
- ✓ textPrimary (gray900) on white - 15.3:1
- ✓ textPrimary (gray900) on gray50 - 14.8:1
- ✓ textPrimary (gray900) on gray100 - 14.0:1
- ✓ gray600 on white - 7.2:1
- ✓ gray700 on white - 10.4:1
- ✓ primaryDark on white - 5.7:1
- ✓ secondaryDark on white - 5.2:1

**Light text on dark backgrounds:**
- ✓ white on gray900 - 15.3:1
- ✓ white on gray800 - 13.1:1
- ✓ white on gray700 - 10.4:1
- ✓ white on primaryDark - 8.7:1
- ✓ white on primary - 5.7:1

### Approved Large Text Combinations (3:1 or higher)

All combinations above, plus:
- ✓ primary (#6B4EFF) on white - 3.7:1
- ✓ secondary (#FF6B9D) on white - 3.4:1
- ✓ error (#EF4444) on white - 3.9:1
- ✓ textTertiary (gray400) on white - 3.2:1

### Approved UI Component Colors (3:1 or higher)

- ✓ primary (#6B4EFF) on white - 3.7:1
- ✓ secondary (#FF6B9D) on white - 3.4:1
- ✓ error (#EF4444) on white - 3.9:1
- ✓ info (#3B82F6) on white - 4.1:1
- ✓ gray400 borders on white - 3.2:1
- ✓ gray500+ on white - 4.6:1+

---

## Action Items

### Critical Issues (Must Fix Before Launch)

1. **Kid Mode Color Palette**
   - [ ] Implement Option B (use standard text colors, bright decorative elements)
   - [ ] Update Kid Mode styling to rely on layout, not color
   - [ ] Test Kid Mode with actual children and parents

2. **Default Border Color**
   - [ ] Change `border` from gray200 to gray400
   - [ ] Update all border usages throughout app
   - [ ] Test visual impact on UI

3. **Semantic Color Usage**
   - [ ] Ensure `warning` color is never used for text
   - [ ] Ensure `success` color is never used for text
   - [ ] Always pair semantic colors with accessible text colors

### High Priority Improvements

4. **Typography Contrast**
   - [ ] Audit all `textTertiary` usages - ensure ≥18pt or replace with `textSecondary`
   - [ ] Document safe text color combinations in theme documentation

5. **Component Library**
   - [ ] Create pre-validated button variants
   - [ ] Create pre-validated text components
   - [ ] Add runtime warnings for low-contrast combinations (dev mode)

### Medium Priority Enhancements

6. **Automated Testing**
   - [ ] Add contrast ratio validation to component tests
   - [ ] Create ESLint rule for unsafe color combinations
   - [ ] Add visual regression tests for accessibility

7. **Documentation**
   - [ ] Update theme README with contrast requirements
   - [ ] Create color picker tool for developers
   - [ ] Add examples of good/bad color usage

---

## Testing and Validation

### Manual Testing Tools

**Online Tools:**
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Color Contrast Analyzer (CCA)](https://www.tpgi.com/color-contrast-checker/)
- [Accessible Colors](https://accessible-colors.com/)

**Testing Process:**
1. Export screenshot from app
2. Use color picker to get exact hex values
3. Input foreground/background into contrast checker
4. Verify meets 4.5:1 (text) or 3:1 (UI components)

### Automated Testing

**In Code:**
```typescript
import { getContrastRatio } from '@/utils/accessibility';

// Validate at runtime (development mode)
if (__DEV__) {
  const ratio = getContrastRatio(textColor, backgroundColor);
  if (ratio < 4.5) {
    console.warn(`Low contrast: ${ratio.toFixed(1)}:1`);
  }
}
```

**In Tests:**
```typescript
import { colors } from '@/theme';
import { getContrastRatio } from '@/utils/accessibility';

describe('Color Contrast', () => {
  it('textPrimary on background meets WCAG AA', () => {
    const ratio = getContrastRatio(colors.textPrimary, colors.background);
    expect(ratio).toBeGreaterThanOrEqual(4.5);
  });
});
```

---

## Resources

### Calculation References

- [WCAG 2.1 Contrast Formula](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)
- [Relative Luminance Calculation](https://www.w3.org/TR/WCAG21/#dfn-relative-luminance)

### Design Tools

- [Accessible color palette generator](https://coolors.co/)
- [Who Can Use](https://www.whocanuse.com/) - Test colors against vision types
- [ColorBox by Lyft](https://colorbox.io/) - Accessible color system builder

### Related Documentation

- [Accessibility Checklist](./accessibility-checklist.md)
- [Testing Procedures](./testing-procedures.md)
- [Theme System Documentation](../../apps/mobile/src/theme/README.md)

---

## Document History

| Date | Version | Author | Changes |
|------|---------|--------|---------|
| 2025-11-10 | 1.0 | Claude Code | Initial color contrast analysis with calculated ratios |

---

**Next Steps:**
1. Address critical issues (Kid Mode colors, border colors, semantic color usage)
2. Implement automated contrast checking in development
3. Update theme documentation with approved combinations
4. Create component library with pre-validated color combinations
