# Dyslexia Support - Technical Documentation

## Overview

Knit-Wit implements dyslexia-friendly typography using the OpenDyslexic font, which features weighted letter bottoms to help users with dyslexia distinguish letter shapes more easily. This document covers the technical implementation, current status, and required fixes.

## Current Implementation Status

**Overall Status:** PARTIALLY IMPLEMENTED - NEEDS FIXES

### What Works ✓

1. **State Management**
   - `dyslexiaFont` boolean stored in Zustand settings store
   - Persisted to AsyncStorage for cross-session consistency
   - Default value: `false`
   - Location: `/home/user/ai-scratchpad/knit-wit/apps/mobile/src/stores/useSettingsStore.ts`

2. **UI Toggle**
   - Settings screen includes toggle switch
   - Accessible labels for screen readers
   - Kid-friendly labels when Kid Mode enabled
   - Screen reader announcements on toggle
   - Location: `/home/user/ai-scratchpad/knit-wit/apps/mobile/src/screens/SettingsScreen.tsx` (lines 146-156)

3. **Theme Architecture**
   - `ThemeProvider` properly wires `dyslexiaFont` setting to theme creation
   - `createTheme()` accepts `useDyslexiaFont` parameter
   - `createTypography()` function switches font families based on flag
   - Locations:
     - `/home/user/ai-scratchpad/knit-wit/apps/mobile/src/theme/ThemeProvider.tsx`
     - `/home/user/ai-scratchpad/knit-wit/apps/mobile/src/theme/themes.ts`
     - `/home/user/ai-scratchpad/knit-wit/apps/mobile/src/theme/typography.ts`

4. **Typography System**
   - Complete typography scale defined with dyslexic font variants
   - Font families properly mapped:
     - Regular: `OpenDyslexic-Regular`
     - Medium: `OpenDyslexic-Bold` (OpenDyslexic lacks medium weight)
     - Bold: `OpenDyslexic-Bold`

5. **Expo Configuration**
   - `app.json` configured with expo-font plugin
   - Font paths correctly specified
   - Location: `/home/user/ai-scratchpad/knit-wit/apps/mobile/app.json` (lines 31-38)

### Critical Issues ❌

1. **Font Files Missing**
   - **Problem:** OpenDyslexic font files not present in assets directory
   - **Expected Files:**
     - `assets/fonts/OpenDyslexic-Regular.ttf`
     - `assets/fonts/OpenDyslexic-Bold.ttf`
   - **Current State:** Only `README.md` exists in fonts directory
   - **Impact:** App will crash or display system fallback when dyslexia font enabled
   - **Severity:** CRITICAL - Feature non-functional without font files

2. **Screens Not Consuming Dynamic Theme**
   - **Problem:** All screens import static `typography` export instead of using `useTheme()` hook
   - **Affected Screens:**
     - HomeScreen.tsx
     - GenerateScreen.tsx
     - ParseScreen.tsx
     - VisualizationScreen.tsx
     - ExportScreen.tsx
     - SettingsScreen.tsx
   - **Current Pattern:**
     ```typescript
     import { colors, typography, spacing, shadows } from '../theme';
     ```
   - **Required Pattern:**
     ```typescript
     import { useTheme } from '../theme';
     // Inside component:
     const theme = useTheme();
     // Use theme.typography instead of typography
     ```
   - **Impact:** Toggling dyslexia font has no visual effect
   - **Severity:** HIGH - Feature appears to work but doesn't actually apply font

3. **StyleSheet Definitions Use Static Typography**
   - **Problem:** All `StyleSheet.create()` calls reference static typography
   - **Example (SettingsScreen.tsx line 344):**
     ```typescript
     title: {
       ...typography.displaySmall,  // Static import
       color: colors.textPrimary,
     }
     ```
   - **Required Change:**
     ```typescript
     // Move styles inside component or use inline styles with theme
     const styles = StyleSheet.create({
       title: {
         ...theme.typography.displaySmall,  // Dynamic theme
         color: theme.colors.textPrimary,
       }
     });
     ```
   - **Impact:** Font changes require app restart (if they worked at all)
   - **Severity:** HIGH - Defeats reactive theme system

## Architecture

### Data Flow

```
User toggles switch
    ↓
setDyslexiaFont(true)
    ↓
useSettingsStore updates state + AsyncStorage
    ↓
ThemeProvider observes dyslexiaFont change
    ↓
createTheme({ useDyslexiaFont: true })
    ↓
createTypography(true) → returns OpenDyslexic fonts
    ↓
Theme context updates
    ↓
Components using useTheme() re-render ← CURRENTLY NOT IMPLEMENTED
    ↓
UI updates with new font
```

### Font Family Mapping

| Weight | Standard Font | Dyslexic Font |
|--------|--------------|---------------|
| Regular | System (iOS), Roboto (Android) | OpenDyslexic-Regular |
| Medium | System, Roboto-Medium | OpenDyslexic-Bold* |
| Bold | System, Roboto-Bold | OpenDyslexic-Bold |

*Note: OpenDyslexic doesn't have a medium weight, so bold is used for both medium and bold.

### Typography Styles Affected

All typography styles will use dyslexic fonts when enabled:
- Display styles: displayLarge, displayMedium, displaySmall
- Headline styles: headlineLarge, headlineMedium, headlineSmall
- Title styles: titleLarge, titleMedium, titleSmall
- Body styles: bodyLarge, bodyMedium, bodySmall
- Label styles: labelLarge, labelMedium, labelSmall

## Required Fixes

### Fix 1: Add Font Files (CRITICAL)

**Priority:** P0 (Blocks feature completely)

**Steps:**
1. Download OpenDyslexic fonts from https://opendyslexic.org/
2. Extract the following files from the download:
   - `OpenDyslexic-Regular.ttf`
   - `OpenDyslexic-Bold.ttf`
3. Copy files to `/home/user/ai-scratchpad/knit-wit/apps/mobile/assets/fonts/`
4. Verify files exist:
   ```bash
   ls -la /home/user/ai-scratchpad/knit-wit/apps/mobile/assets/fonts/
   # Should show: OpenDyslexic-Regular.ttf, OpenDyslexic-Bold.ttf, README.md
   ```
5. Test app launch to ensure fonts load without errors

**License Compliance:**
- OpenDyslexic is licensed under OFL (Open Font License)
- Free for commercial and personal use
- Attribution should be included in app credits
- License info: https://opendyslexic.org/about

**Validation:**
- App builds successfully
- No font loading errors in console
- Font files appear in Expo bundle

### Fix 2: Update Screens to Use Dynamic Theme (HIGH PRIORITY)

**Priority:** P1 (Feature doesn't work without this)

**Affected Files:**
- HomeScreen.tsx
- GenerateScreen.tsx
- ParseScreen.tsx
- VisualizationScreen.tsx
- ExportScreen.tsx
- SettingsScreen.tsx

**Before:**
```typescript
import { colors, typography, spacing, shadows } from '../theme';

export default function HomeScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  title: {
    ...typography.displaySmall,
    color: colors.textPrimary,
  }
});
```

**After:**
```typescript
import { useTheme } from '../theme';

export default function HomeScreen() {
  const theme = useTheme();

  const styles = createStyles(theme);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome</Text>
    </View>
  );
}

function createStyles(theme: Theme) {
  return StyleSheet.create({
    title: {
      ...theme.typography.displaySmall,
      color: theme.colors.textPrimary,
    }
  });
}
```

**Alternative Approach (Inline Styles):**
```typescript
export default function HomeScreen() {
  const theme = useTheme();

  return (
    <View style={{ flex: 1, backgroundColor: theme.colors.background }}>
      <Text style={[theme.typography.displaySmall, { color: theme.colors.textPrimary }]}>
        Welcome
      </Text>
    </View>
  );
}
```

**Migration Checklist:**
- [ ] HomeScreen.tsx - Update to use useTheme()
- [ ] GenerateScreen.tsx - Update to use useTheme()
- [ ] ParseScreen.tsx - Update to use useTheme()
- [ ] VisualizationScreen.tsx - Update to use useTheme()
- [ ] ExportScreen.tsx - Update to use useTheme()
- [ ] SettingsScreen.tsx - Update to use useTheme()

**Testing:**
- Toggle dyslexia font setting
- Verify all text updates immediately without app restart
- Check all screens render correctly with dyslexic font
- Verify no layout breaks or text overflow issues

### Fix 3: Component Library Updates (MEDIUM PRIORITY)

**Priority:** P2 (Affects reusable components)

Search for and update any reusable components that use static typography:

```bash
grep -r "import.*typography.*from.*theme" apps/mobile/src/components/
```

Update each component to use `useTheme()` hook.

## Testing Checklist

### Unit Tests
- [ ] Test `createTypography(false)` returns system fonts
- [ ] Test `createTypography(true)` returns OpenDyslexic fonts
- [ ] Test `createTheme({ useDyslexiaFont: true })` includes dyslexic typography
- [ ] Test settings store persists dyslexia font preference

### Integration Tests
- [ ] Test ThemeProvider propagates theme updates
- [ ] Test toggling setting triggers theme recreation
- [ ] Test theme context provides updated typography

### Manual Testing
- [ ] Toggle dyslexia font setting ON
  - All text should switch to OpenDyslexic immediately
  - No app restart required
  - Layout remains intact
- [ ] Toggle dyslexia font setting OFF
  - All text should revert to system fonts
  - No visual glitches
- [ ] Test with Kid Mode enabled
  - Dyslexia font should work in Kid Mode
  - Labels should say "Easier Reading Font"
- [ ] Test font rendering in all screens:
  - [ ] HomeScreen - titles, descriptions
  - [ ] GenerateScreen - form labels, input text
  - [ ] ParseScreen - pattern text display
  - [ ] VisualizationScreen - round labels, instructions
  - [ ] ExportScreen - export format labels
  - [ ] SettingsScreen - all setting labels and descriptions
- [ ] Test accessibility
  - [ ] Screen reader announces setting changes
  - [ ] Text remains readable at different font sizes
  - [ ] High contrast mode compatible

### Rendering Tests
- [ ] Test readability at minimum font size (labelSmall - 11pt)
- [ ] Test readability at maximum font size (displayLarge - 57pt)
- [ ] Verify no text overflow or clipping
- [ ] Test on different screen sizes (phone, tablet)
- [ ] Test with system font scaling (Settings > Display > Font Size)

### Performance Tests
- [ ] Measure theme switch performance (should be < 100ms)
- [ ] Verify no memory leaks from theme updates
- [ ] Check bundle size impact (fonts add ~200KB)

## Accessibility Considerations

### Screen Reader Support

**Current Implementation:**
```typescript
// SettingsScreen.tsx lines 50-57
const handleDyslexiaFontToggle = (value: boolean) => {
  setDyslexiaFont(value);
  AccessibilityInfo.announceForAccessibility(
    value
      ? (kidMode ? 'Easier reading font turned on' : 'Dyslexia-friendly font enabled')
      : (kidMode ? 'Easier reading font turned off' : 'Dyslexia-friendly font disabled')
  );
};
```

**Verification:**
- Toggle announces correctly for VoiceOver (iOS)
- Toggle announces correctly for TalkBack (Android)
- Announcement is clear and actionable
- Kid Mode uses simpler language

### WCAG Compliance

- **WCAG 2.1 Level AA - Text Spacing (1.4.12):** OpenDyslexic's spacing may need verification
- **WCAG 2.1 Level AA - Contrast (1.4.3):** Font choice doesn't affect contrast ratios
- **WCAG 2.1 Level AA - Resize Text (1.4.4):** Must test font scaling up to 200%

### Best Practices

1. **User Choice:** Font preference is user-controlled, not forced
2. **Persistence:** Setting persists across app sessions
3. **Immediate Feedback:** Changes apply immediately (once fixed)
4. **Kid-Friendly:** Simplified labels in Kid Mode
5. **No Layout Breaks:** Typography system maintains consistent line heights

## Known Limitations

1. **No Italic Variant:** OpenDyslexic italic not currently supported
2. **No Medium Weight:** OpenDyslexic medium uses bold as fallback
3. **Bundle Size:** Fonts add approximately 200KB to app bundle
4. **Platform Fonts:** Web version may need webfont configuration

## Future Enhancements

1. **Additional Fonts:** Consider Lexend, Atkinson Hyperlegible, or Comic Sans MS options
2. **Font Size Multiplier:** Add separate setting to increase all font sizes by 120%
3. **Line Spacing Control:** Allow users to increase line height for easier reading
4. **Letter Spacing:** Add option to increase letter spacing
5. **Reading Mode:** Combine dyslexia font with increased spacing and simplified layout

## References

- **OpenDyslexic:** https://opendyslexic.org/
- **License (OFL):** https://scripts.sil.org/cms/scripts/page.php?site_id=nrsi&id=OFL
- **Research:** https://opendyslexic.org/about#research
- **Expo Fonts:** https://docs.expo.dev/develop/user-interface/fonts/
- **WCAG 2.1:** https://www.w3.org/WAI/WCAG21/quickref/

## Version History

- **v1.0 (Phase 3):** Initial implementation - toggle, state, theme architecture
- **v1.1 (Phase 4 Sprint 9):** Verification and documentation
- **v1.2 (Planned):** Bug fixes - font files, screen updates, testing

## Maintainer Notes

**Code Owners:** Frontend team, Accessibility team

**Deployment Checklist:**
1. Ensure font files are committed to repository
2. Verify font files load correctly in Expo builds
3. Test on both iOS and Android devices
4. Validate accessibility with actual screen readers
5. Update user-facing documentation

**Monitoring:**
- Track usage of dyslexia font setting in telemetry
- Monitor for font loading errors
- Track user feedback on readability

---

*Last updated: 2025-11-14*
*Phase: 4, Sprint: 9, Story: A11Y-5*
