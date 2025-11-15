# Dyslexia Font Feature - Fixes Required

## Quick Summary

The dyslexia font feature is **architecturally complete** but has **2 critical bugs** that prevent it from working:

1. ❌ Font files are missing
2. ❌ Screens don't use dynamic theme

**Estimated fix time:** 3.5 hours

---

## Fix #1: Add Font Files (P0 - CRITICAL)

### Problem
Font files referenced in `app.json` don't exist in the repository.

### Impact
- App may crash when dyslexia font enabled
- Feature is completely non-functional

### Solution

**Step 1: Download Fonts**
1. Go to https://opendyslexic.org/
2. Click "Download" or navigate to download page
3. Download the OpenDyslexic font package

**Step 2: Extract Required Files**
From the downloaded package, extract:
- `OpenDyslexic-Regular.ttf`
- `OpenDyslexic-Bold.ttf`

**Step 3: Copy to Project**
```bash
cp OpenDyslexic-Regular.ttf /home/user/ai-scratchpad/knit-wit/apps/mobile/assets/fonts/
cp OpenDyslexic-Bold.ttf /home/user/ai-scratchpad/knit-wit/apps/mobile/assets/fonts/
```

**Step 4: Verify**
```bash
ls -la /home/user/ai-scratchpad/knit-wit/apps/mobile/assets/fonts/
# Should show: OpenDyslexic-Regular.ttf, OpenDyslexic-Bold.ttf, README.md
```

**Step 5: Test**
```bash
cd /home/user/ai-scratchpad/knit-wit/apps/mobile
pnpm run dev
# Check console for font loading errors
```

### License
- OpenDyslexic uses OFL (Open Font License)
- Free for commercial use
- No attribution required (but recommended in app credits)

---

## Fix #2: Update Screens to Use Dynamic Theme (P1 - HIGH)

### Problem
All screens import static `typography` instead of using the `useTheme()` hook. This prevents theme changes from applying.

### Impact
- Toggling dyslexia font has no visual effect
- Theme system is bypassed
- Feature appears broken to users

### Solution

Update 6 screens to use dynamic theme. Pattern for each screen:

#### Affected Files
1. HomeScreen.tsx
2. GenerateScreen.tsx
3. ParseScreen.tsx
4. VisualizationScreen.tsx
5. ExportScreen.tsx
6. SettingsScreen.tsx

#### Migration Pattern

**BEFORE (Incorrect):**
```typescript
import { colors, typography, spacing, shadows } from '../theme';

export default function HomeScreen({ navigation }: Props) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  title: {
    ...typography.displaySmall,
    color: colors.textPrimary,
  }
});
```

**AFTER (Correct):**
```typescript
import { useTheme } from '../theme';
import type { Theme } from '../theme';

export default function HomeScreen({ navigation }: Props) {
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
    container: {
      flex: 1,
      backgroundColor: theme.colors.background,
    },
    title: {
      ...theme.typography.displaySmall,
      color: theme.colors.textPrimary,
    }
  });
}
```

#### Step-by-Step for Each Screen

1. **Update imports**
   ```typescript
   // Remove:
   import { colors, typography, spacing, shadows } from '../theme';

   // Add:
   import { useTheme } from '../theme';
   import type { Theme } from '../theme';
   ```

2. **Add useTheme hook**
   ```typescript
   export default function ScreenName({ navigation }: Props) {
     const theme = useTheme();
     // ... other hooks ...
   ```

3. **Create styles function**
   ```typescript
   // Move StyleSheet.create() into a function
   function createStyles(theme: Theme) {
     return StyleSheet.create({
       // ... styles using theme ...
     });
   }
   ```

4. **Call styles function**
   ```typescript
   export default function ScreenName({ navigation }: Props) {
     const theme = useTheme();
     const styles = createStyles(theme);
     // ... rest of component ...
   }
   ```

5. **Update all style references**
   ```typescript
   // Change all instances:
   colors.primary → theme.colors.primary
   typography.bodyLarge → theme.typography.bodyLarge
   spacing.md → theme.spacing.md
   shadows.sm → theme.shadows.sm
   ```

6. **Update components using theme values**
   ```typescript
   // If settings store is used for colors/typography:
   const { kidMode } = useSettingsStore();

   // Use theme instead:
   const theme = useTheme();
   // Theme already includes kidMode colors/typography
   ```

### Testing Checklist (Per Screen)

After updating each screen:

- [ ] Component compiles without TypeScript errors
- [ ] Screen renders correctly
- [ ] Toggle dyslexia font in Settings
- [ ] Navigate to updated screen
- [ ] Verify text changes to OpenDyslexic font
- [ ] Toggle off, verify text reverts to system font
- [ ] Check all text elements (titles, body, labels)
- [ ] Verify no layout breaks or overflow
- [ ] Test with Kid Mode enabled + dyslexia font
- [ ] Test with Dark Mode enabled + dyslexia font

---

## Verification Steps

After both fixes applied:

### 1. Build Test
```bash
cd /home/user/ai-scratchpad/knit-wit/apps/mobile
pnpm install
pnpm run dev
# Check console for errors
```

### 2. Visual Test

1. Open app in simulator/device
2. Go to Settings > Appearance
3. Toggle "Dyslexia-Friendly Font" ON
4. Navigate through all screens:
   - [ ] Home - titles, descriptions
   - [ ] Generate - form labels, inputs
   - [ ] Parse - pattern text
   - [ ] Visualization - round labels
   - [ ] Export - format labels
   - [ ] Settings - all labels

5. Verify all text uses OpenDyslexic font
6. Toggle OFF
7. Verify all text reverts to system font

### 3. Persistence Test

1. Enable dyslexia font
2. Close app completely
3. Reopen app
4. Verify font is still OpenDyslexic
5. Navigate to different screens
6. Verify font persists across all screens

### 4. Accessibility Test

1. Enable VoiceOver (iOS) or TalkBack (Android)
2. Navigate to Settings
3. Toggle dyslexia font
4. Verify announcement: "Dyslexia-friendly font enabled"
5. Toggle off
6. Verify announcement: "Dyslexia-friendly font disabled"

### 5. Combination Test

Test dyslexia font with other settings:
- [ ] Dyslexia font + Kid Mode
- [ ] Dyslexia font + Dark Mode
- [ ] Dyslexia font + Kid Mode + Dark Mode
- [ ] All combinations render correctly

---

## Performance Checklist

- [ ] Theme switch completes in < 100ms
- [ ] No visible lag when toggling
- [ ] No memory leaks (use React DevTools Profiler)
- [ ] Bundle size increase is acceptable (~200KB)
- [ ] Font loads on first app launch

---

## Common Pitfalls

### ❌ Don't Do This
```typescript
// Importing static typography
import { typography } from '../theme';

// Using static typography in styles
const styles = StyleSheet.create({
  title: { ...typography.displaySmall }
});
```

### ✓ Do This
```typescript
// Import useTheme hook
import { useTheme } from '../theme';

// Use dynamic theme
const theme = useTheme();
const styles = createStyles(theme);

function createStyles(theme: Theme) {
  return StyleSheet.create({
    title: { ...theme.typography.displaySmall }
  });
}
```

### ❌ Don't Do This
```typescript
// Mixing static imports with theme
const { kidMode } = useSettingsStore();
const theme = useTheme();

const color = kidMode ? colors.primary : colors.secondary; // ← Static colors
```

### ✓ Do This
```typescript
// Use theme for everything
const theme = useTheme();

const color = theme.colors.primary; // ← Theme already knows about kidMode
```

---

## Expected Outcome

After both fixes:

1. **User toggles dyslexia font ON**
   - All text immediately changes to OpenDyslexic
   - No app restart needed
   - Change is visible across all screens

2. **User toggles dyslexia font OFF**
   - All text immediately reverts to system font
   - No app restart needed

3. **User closes and reopens app**
   - Setting persists
   - Font remains as user selected

4. **Screen reader users**
   - Hear clear announcements on toggle
   - Can navigate all screens with correct font

---

## Questions?

See full documentation:
- **Technical Details:** `/home/user/ai-scratchpad/knit-wit/docs/accessibility/dyslexia-support.md`
- **User Guide:** `/home/user/ai-scratchpad/knit-wit/docs/accessibility/user-guide.md`
- **Verification Report:** `/home/user/ai-scratchpad/knit-wit/docs/accessibility/A11Y-5-verification-report.md`

---

*Last updated: 2025-11-14*
