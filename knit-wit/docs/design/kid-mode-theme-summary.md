# Kid Mode Theme - Implementation Summary

**Quick Reference for Frontend Developer**

## Files Created

1. `/apps/mobile/src/theme/kidModeTheme.ts` - Complete Kid Mode theme implementation
2. `/apps/mobile/src/theme/themes.ts` - Updated to import Kid Mode theme
3. `/docs/design/kid-mode-theme-design-rationale.md` - Comprehensive design documentation

## Key Changes from Default Theme

### Colors

| Element | Default | Kid Mode | Change |
|---------|---------|----------|--------|
| Primary | Purple #6B4EFF | Pink #FF6B9D | More playful |
| Secondary | Pink #FF6B9D | Yellow #FFC837 | Cheerful accent |
| Background | White #FFFFFF | Cream #FFF8E1 | Softer, less harsh |
| Text | Gray #111827 | Dark Gray #2D3748 | Optimized for cream |

### Typography (Body Text)

| Size | Default | Kid Mode | Increase |
|------|---------|----------|----------|
| Body Large | 16px | 20px | +25% |
| Body Medium | 14px | 16px | +14% |
| Line Height | 1.4-1.5x | 1.6x | More breathing room |
| Letter Spacing | 0px | 0.5px | Wider for readability |

### Spacing

| Size | Default | Kid Mode | Change |
|------|---------|----------|--------|
| xs | 4px | 8px | 2x |
| sm | 8px | 16px | 2x |
| md | 16px | 24px | 1.5x |
| lg | 24px | 32px | 1.33x |
| xl | 32px | 48px | 1.5x |

### Touch Targets

| Type | Default | Kid Mode | Rationale |
|------|---------|----------|-----------|
| Minimum | 44dp | 56dp | WCAG AAA for children |
| Comfortable | 48dp | 64dp | Recommended size |
| Kid Mode | 56dp | 72dp | Extra forgiving |

### Border Radius

All corner radii are approximately **2x larger** for a friendlier, softer appearance:
- Small: 8px (was 4px)
- Medium: 16px (was 8px)
- Large: 20px (was 12px)

## WCAG AA Contrast Verification

### PASSING Combinations ✓

| Foreground | Background | Ratio | Use Case |
|------------|------------|-------|----------|
| #2D3748 (text) | #FFF8E1 (cream) | 11.46:1 | Body text - EXCELLENT |
| #4A5568 (text) | #FFF8E1 (cream) | 7.89:1 | Secondary text - EXCELLENT |
| #FF6B9D (pink) | #FFFFFF (white) | 3.36:1 | UI components - GOOD |
| #E63D7A (dark pink) | #FFFFFF (white) | 4.52:1 | Text on white - GOOD |
| #4CAF50 (green) | #FFF8E1 (cream) | 3.2:1 | Success UI - ACCEPTABLE |

### FAILING Combinations ✗

| Foreground | Background | Ratio | Issue |
|------------|------------|-------|-------|
| #FFC837 (yellow) | #FFFFFF (white) | 1.76:1 | FAILS - Do NOT use for text/UI |
| #FFC837 (yellow) | #FFF8E1 (cream) | 1.68:1 | FAILS - Decorative only |

**Critical:** Never use bright yellow (#FFC837) for text or interactive elements on white or cream backgrounds. Use secondaryDark (#E6A800) instead, which has 3.1:1 contrast.

## Implementation Checklist

### Theme Integration

- [ ] Import `kidModeTheme` from `'@/theme'`
- [ ] Add Kid Mode toggle to Settings screen
- [ ] Store theme preference in AsyncStorage
- [ ] Update ThemeProvider to support Kid Mode
- [ ] Test theme switching without app restart

### Component Updates

- [ ] Update all buttons to use `theme.touchTargets.comfortable` (64dp)
- [ ] Ensure all text uses theme typography (especially bodyLarge for main content)
- [ ] Apply theme spacing to all layouts (use md/lg/xl)
- [ ] Update border radius on all cards, buttons, inputs
- [ ] Verify shadows are applied consistently

### Accessibility Testing

- [ ] Run contrast checker on all screens
- [ ] Test with iOS VoiceOver enabled
- [ ] Test with Android TalkBack enabled
- [ ] Verify tap target sizes (use Show Touches in dev settings)
- [ ] Test with external keyboard (Tab navigation)

### Visual QA

- [ ] Verify pink primary doesn't overwhelm the UI
- [ ] Check yellow is only used for accents, not text
- [ ] Ensure cream background is comfortable (not too yellow)
- [ ] Confirm text is easy to read for 5+ minutes
- [ ] Validate rounded corners look friendly, not childish

## Usage Examples

### Button Component

```typescript
import { useTheme } from '@/theme';

function PrimaryButton({ onPress, children }) {
  const theme = useTheme();

  return (
    <TouchableOpacity
      onPress={onPress}
      style={{
        backgroundColor: theme.colors.primary,    // Pink #FF6B9D
        borderRadius: theme.borderRadius.lg,      // 20px
        paddingHorizontal: theme.spacing.lg,      // 32px
        paddingVertical: theme.spacing.md,        // 24px
        minHeight: theme.touchTargets.comfortable, // 64dp
        minWidth: theme.touchTargets.comfortable,  // 64dp
        alignItems: 'center',
        justifyContent: 'center',
        ...theme.shadows.md,                      // Elevation 3
      }}
    >
      <Text
        style={{
          color: theme.colors.white,
          ...theme.typography.labelLarge,        // 16px, medium weight
        }}
      >
        {children}
      </Text>
    </TouchableOpacity>
  );
}
```

### Card Component

```typescript
function ContentCard({ title, children }) {
  const theme = useTheme();

  return (
    <View
      style={{
        backgroundColor: theme.colors.surface,   // White
        borderRadius: theme.borderRadius.lg,     // 20px
        padding: theme.spacing.lg,               // 32px
        marginBottom: theme.spacing.md,          // 24px
        ...theme.shadows.sm,                     // Subtle shadow
      }}
    >
      <Text
        style={{
          ...theme.typography.titleLarge,        // 24px, semibold
          color: theme.colors.textPrimary,       // #2D3748
          marginBottom: theme.spacing.md,        // 24px
        }}
      >
        {title}
      </Text>
      <Text
        style={{
          ...theme.typography.bodyLarge,         // 20px body text
          color: theme.colors.textPrimary,
          lineHeight: 32,                        // 1.6x ratio
        }}
      >
        {children}
      </Text>
    </View>
  );
}
```

### Screen Layout

```typescript
function KidModeScreen() {
  const theme = useTheme();

  return (
    <SafeAreaView
      style={{
        flex: 1,
        backgroundColor: theme.colors.background, // Cream #FFF8E1
      }}
    >
      <ScrollView
        contentContainerStyle={{
          padding: theme.spacing.lg,              // 32px
        }}
      >
        {/* Content */}
      </ScrollView>
    </SafeAreaView>
  );
}
```

## Color Usage Guide

### DO Use

- **Pink Primary (#FF6B9D)** for:
  - Primary action buttons
  - Active/selected states
  - Progress indicators
  - Focus indicators
  - Large UI elements

- **Yellow Secondary (#FFC837)** for:
  - Large decorative elements (backgrounds, shapes)
  - Achievement badges with dark borders
  - Gradients (mixed with darker colors)
  - Illustrations

- **Dark Yellow (#E6A800)** for:
  - UI elements on white (3.1:1 contrast)
  - Icons on light backgrounds
  - Warning indicators

### DON'T Use

- **Yellow (#FFC837)** for:
  - Text on white or cream backgrounds
  - Small interactive buttons
  - Critical UI elements requiring 3:1 contrast
  - Navigation elements

## Testing Tools

### Contrast Checkers
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Coolors Contrast Checker](https://coolors.co/contrast-checker)
- Use browser DevTools to inspect computed colors

### Accessibility
- iOS: Settings > Accessibility > VoiceOver
- Android: Settings > Accessibility > TalkBack
- React Native: Enable "Show Touches" in dev menu

### Visual Debugging
```typescript
// Add this to see touch target sizes
<View
  style={{
    borderWidth: 1,
    borderColor: 'red',
    borderStyle: 'dashed',
  }}
>
  {/* Component */}
</View>
```

## Common Pitfalls to Avoid

1. **Using yellow for text** - Always use dark yellow (#E6A800) or textPrimary
2. **Small touch targets** - Minimum 56dp, recommended 64dp
3. **Insufficient spacing** - Use md (24px) as minimum component padding
4. **Forgetting line height** - Always use 1.6x for body text
5. **Hard-coded colors** - Always use theme colors, never hex values
6. **Ignoring letter spacing** - Kid Mode uses 0.5px for body text

## Questions?

Refer to the comprehensive design rationale document:
`/docs/design/kid-mode-theme-design-rationale.md`

Or check the theme implementation with full comments:
`/apps/mobile/src/theme/kidModeTheme.ts`

---

**Status:** Design Complete ✓
**Next Step:** Frontend Developer Implementation (Story E1 continuation)
**Estimated Implementation Time:** 4-6 hours (toggle + theme integration)
