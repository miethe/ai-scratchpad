# Phase 4: Kid Mode & Accessibility

**Duration:** Weeks 12–13 (Sprint 8)
**Team:** Frontend Lead + Accessibility Specialist + 1 Frontend Engineer + QA Lead
**Capacity:** ~70-80 story points
**Status:** Planned

---

## Phase Overview

Phase 4 focuses on making Knit-Wit accessible, inclusive, and child-friendly. This phase implements comprehensive accessibility features to meet WCAG AA compliance standards, along with a specialized Kid Mode that simplifies the interface for young learners and beginners.

Accessibility is a core value of Knit-Wit, ensuring that makers of all abilities can use the app comfortably. This includes users with visual impairments, motor difficulties, dyslexia, and other accessibility needs, as well as children learning to crochet.

### Phase Context

**Preceding Phase:**
- Phase 3 (Weeks 8-11): Full Feature Implementation complete with generation, visualization, export, and parsing features functional

**Following Phase:**
- Phase 5 (Weeks 14-15): QA & Polish begins with comprehensive accessibility audits and cross-device testing

**Critical Path:**
This phase is NOT on the critical path but is essential for MVP launch. Accessibility compliance and Kid Mode are core product differentiators and regulatory requirements.

---

## Goals & Deliverables

### Primary Goals

1. **WCAG AA Compliance:** Meet Web Content Accessibility Guidelines 2.1 Level AA across all app features
2. **Kid Mode Implementation:** Simplified UI variant with child-friendly language and larger interactive elements
3. **Screen Reader Support:** Full coverage of all interactive elements with appropriate ARIA labels and announcements
4. **Visual Accessibility:** High-contrast mode, dyslexia-friendly font options, and verified color contrast ratios
5. **Motor Accessibility:** Left-handed support, larger tap targets, and keyboard navigation

### Key Deliverables

- [ ] Kid Mode toggle in settings with theme override system
- [ ] Beginner-friendly copy rewrite for all stitch terminology
- [ ] Larger tap targets (minimum 44x44pt) in Kid Mode
- [ ] Animated stitch explanations (2-3 second micro-animations)
- [ ] Accessibility settings screen (text size, contrast, fonts, handedness)
- [ ] Screen reader labels and announcements for all interactive elements
- [ ] Color palette verification with WCAG AA contrast ratios
- [ ] High-contrast mode implementation
- [ ] Left-handed layout support
- [ ] Dyslexia-friendly font option (OpenDyslexic or Lexend)
- [ ] Keyboard navigation support (all screens)
- [ ] Accessibility documentation and testing guidelines

### Success Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| WCAG AA Compliance | 0 critical issues | axe DevTools + Lighthouse |
| Color Contrast (Normal Text) | ≥ 4.5:1 | WebAIM Contrast Checker |
| Color Contrast (Large Text) | ≥ 3:1 | WebAIM Contrast Checker |
| Screen Reader Coverage | 100% of interactive elements | Manual testing on iOS/Android |
| Tap Target Size (Kid Mode) | ≥ 44x44pt | UI component measurement |
| Animation Duration | 2-3 seconds | Performance profiling |
| Keyboard Navigation | 100% of screens accessible | Manual testing |

---

## Epic Breakdown

### EPIC E: Kid Mode & Accessibility

**Owner:** Frontend Lead + Accessibility Specialist
**Duration:** Weeks 12–13 (Sprint 8)
**Total Effort:** ~75 story points
**Priority:** P0 (MVP Requirement)

**Epic Overview:**

Make Knit-Wit approachable for children and ensure WCAG AA compliance for all users. Implement a simplified UI variant, animated explanations, large buttons, comprehensive screen reader support, and visual accessibility features including high-contrast mode and dyslexia-friendly fonts.

**Epic Goals:**

- Kid Mode toggle in settings activates child-friendly UI with simplified language
- All interactive elements accessible via keyboard and screen reader
- Color contrast meets or exceeds WCAG AA requirements (4.5:1 normal, 3:1 large)
- Explanatory micro-animations help visual learners understand stitches
- High-contrast mode and dyslexia font options available
- Left-handed layout support for improved usability

**Stories:**

| ID | Title | Effort | Priority | Dependencies | Assignee |
|----|-------|--------|----------|--------------|----------|
| E1 | Kid Mode toggle & theme system | 3 pt | P0 | None | Frontend Eng 1 |
| E2 | Beginner-friendly copy rewrite | 8 pt | P0 | E1 | Content + Frontend Lead |
| E3 | Larger tap targets (Kid Mode) | 5 pt | P0 | E1 | Frontend Eng 1 |
| E4 | Animated stitch explanations | 13 pt | P1 | E1 | Frontend Eng 2 |
| E5 | Accessibility settings screen | 8 pt | P0 | None | Frontend Lead |
| E6 | Screen reader labels (full coverage) | 13 pt | P0 | E5 | Frontend Lead |
| E7 | Color palette verification (WCAG AA) | 5 pt | P0 | None | Frontend + QA |
| E8 | High-contrast mode implementation | 8 pt | P0 | E5, E7 | Frontend Eng 1 |
| E9 | Left-handed layout support | 5 pt | P1 | E5 | Frontend Eng 2 |
| E10 | Dyslexia-friendly font option | 5 pt | P1 | E5 | Frontend Eng 1 |
| E11 | Keyboard navigation (all screens) | 8 pt | P0 | E6 | Frontend Lead |

**Total Story Points:** 81 points

**Acceptance Criteria:**

- **AC-E-1:** Kid Mode activates from settings; UI shows larger buttons, simplified language, and bright colors
- **AC-E-2:** Keyboard navigation works on all screens; focus indicators are visible; tab order is logical
- **AC-E-3:** Screen reader announces all interactive elements with descriptive labels
- **AC-E-4:** Color contrast ratios verified: 4.5:1 for normal text, 3:1 for large text (18pt+)
- **AC-E-5:** High-contrast mode increases contrast to 7:1 minimum
- **AC-E-6:** Stitch explanation animations complete in 2-3 seconds; loop smoothly
- **AC-E-7:** Left-handed mode mirrors layout appropriately
- **AC-E-8:** Dyslexia font applies to all body text when enabled
- **AC-E-9:** All tap targets in Kid Mode are ≥ 44x44pt (Apple HIG minimum)
- **AC-E-10:** Settings persist across app restarts

---

## Sprint Plan

### Sprint 8: Kid Mode & Accessibility (Weeks 12–13)

**Sprint Goal:** WCAG AA compliant app with functional Kid Mode

**Sprint Duration:** 2 weeks (10 working days)

**Team Capacity:**
- Frontend Lead: 40 pts (accessibility architecture + screen readers)
- Frontend Engineer 1: 35 pts (Kid Mode + visual accessibility)
- Frontend Engineer 2: 30 pts (animations + left-handed support)
- QA Lead: 15 pts (accessibility audits + testing)
- **Total Capacity:** ~120 pts (includes buffer for iteration)

**Planned Stories:**

#### Week 12 (Days 1-5)

**Day 1-2: Foundation & Settings**
- E1 (3pt): Kid Mode toggle & theme system
- E5 (8pt): Accessibility settings screen
- E7 (5pt): Color palette verification

**Day 3-5: Core Accessibility Features**
- E6 (13pt): Screen reader labels (full coverage)
- E8 (8pt): High-contrast mode implementation
- E10 (5pt): Dyslexia-friendly font option

**Week 12 Total:** ~42 pts

#### Week 13 (Days 6-10)

**Day 6-7: Kid Mode Implementation**
- E2 (8pt): Beginner-friendly copy rewrite
- E3 (5pt): Larger tap targets (Kid Mode)

**Day 8-10: Polish & Advanced Features**
- E4 (13pt): Animated stitch explanations
- E9 (5pt): Left-handed layout support
- E11 (8pt): Keyboard navigation (all screens)

**Week 13 Total:** ~39 pts

**Demo Objectives:**
- Kid Mode toggle works; UI is noticeably simplified and child-friendly
- Screen reader navigation demonstrated on iOS and Android
- High-contrast mode increases readability significantly
- WCAG AA checklist reviewed with 0 critical issues
- Keyboard navigation demonstrated on all screens

---

## Technical Implementation

### Accessibility Architecture

**1. Theme System Enhancement**

Extend the existing theme system to support multiple accessibility variants:

```typescript
// theme/AccessibilityTheme.ts
interface AccessibilityConfig {
  kidMode: boolean;
  highContrast: boolean;
  dyslexiaFont: boolean;
  textSize: 'default' | 'large' | 'xlarge';
  leftHanded: boolean;
}

interface ThemeColors {
  // Standard colors (WCAG AA compliant)
  primary: string;           // 4.5:1 contrast
  secondary: string;
  background: string;
  text: string;

  // High contrast overrides (WCAG AAA)
  highContrast: {
    primary: string;         // 7:1 contrast
    secondary: string;
    background: string;
    text: string;
  };

  // Kid Mode overrides (bright, friendly)
  kidMode: {
    primary: string;
    secondary: string;
    accent: string;
  };
}
```

**2. Kid Mode Implementation**

Create a context provider for Kid Mode settings:

```typescript
// context/KidModeContext.tsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface KidModeContextValue {
  kidMode: boolean;
  setKidMode: (enabled: boolean) => Promise<void>;
  getKidFriendlyText: (key: string) => string;
}

const KidModeContext = createContext<KidModeContextValue | undefined>(undefined);

export const KidModeProvider: React.FC = ({ children }) => {
  const [kidMode, setKidModeState] = useState(false);

  // Load Kid Mode preference on mount
  useEffect(() => {
    AsyncStorage.getItem('kidMode').then(value => {
      if (value === 'true') setKidModeState(true);
    });
  }, []);

  const setKidMode = async (enabled: boolean) => {
    setKidModeState(enabled);
    await AsyncStorage.setItem('kidMode', String(enabled));
  };

  const getKidFriendlyText = (key: string) => {
    if (!kidMode) return standardText[key];
    return kidFriendlyText[key] || standardText[key];
  };

  return (
    <KidModeContext.Provider value={{ kidMode, setKidMode, getKidFriendlyText }}>
      {children}
    </KidModeContext.Provider>
  );
};

export const useKidMode = () => {
  const context = useContext(KidModeContext);
  if (!context) throw new Error('useKidMode must be used within KidModeProvider');
  return context;
};
```

**3. Copy Rewrite Strategy**

Map standard crochet terminology to kid-friendly language:

```typescript
// constants/terminology.ts
export const standardText = {
  'stitch.inc': 'increase (inc)',
  'stitch.inc.description': 'Work 2 stitches in same stitch',
  'stitch.dec': 'decrease (dec)',
  'stitch.dec.description': 'Combine 2 stitches into 1 stitch',
  'stitch.sc': 'single crochet (sc)',
  'stitch.ch': 'chain (ch)',
  'round.label': 'Round',
  'gauge.stitches': 'Stitches per 10cm',
};

export const kidFriendlyText = {
  'stitch.inc': 'Add two stitches in one spot',
  'stitch.inc.description': 'Put your hook in one stitch and make two stitches!',
  'stitch.dec': 'Combine two into one',
  'stitch.dec.description': 'Take two stitches and turn them into one stitch',
  'stitch.sc': 'Single crochet',
  'stitch.ch': 'Chain',
  'round.label': 'Step',
  'gauge.stitches': 'How many stitches fit in 10cm',
};
```

**4. Larger Tap Targets (Kid Mode)**

Apply size overrides when Kid Mode is active:

```typescript
// components/shared/Button.tsx
import { useKidMode } from '../../context/KidModeContext';

export const Button: React.FC<ButtonProps> = ({ children, onPress, style, ...props }) => {
  const { kidMode } = useKidMode();

  const buttonStyle = [
    styles.button,
    kidMode && styles.kidModeButton,  // Increased padding and size
    style,
  ];

  return (
    <TouchableOpacity
      style={buttonStyle}
      onPress={onPress}
      accessibilityRole="button"
      {...props}
    >
      <Text style={[styles.buttonText, kidMode && styles.kidModeText]}>
        {children}
      </Text>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  button: {
    minHeight: 40,
    minWidth: 60,
    paddingHorizontal: 16,
    paddingVertical: 8,
  },
  kidModeButton: {
    minHeight: 56,      // Increased from 40
    minWidth: 88,       // Increased from 60
    paddingHorizontal: 24,
    paddingVertical: 16,
    borderRadius: 12,   // Larger, friendlier rounded corners
  },
  buttonText: {
    fontSize: 16,
  },
  kidModeText: {
    fontSize: 20,       // Larger, more readable
    fontWeight: '600',  // Slightly bolder
  },
});
```

**5. Animated Stitch Explanations**

Create micro-animations showing how stitches work:

```typescript
// components/education/StitchAnimation.tsx
import React, { useEffect, useRef } from 'react';
import { Animated, View } from 'react-native';
import Svg, { Circle, Path } from 'react-native-svg';

interface StitchAnimationProps {
  stitchType: 'inc' | 'dec' | 'sc' | 'ch';
  duration?: number;  // milliseconds, default 2500
}

export const StitchAnimation: React.FC<StitchAnimationProps> = ({
  stitchType,
  duration = 2500
}) => {
  const animationProgress = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    // Loop animation
    Animated.loop(
      Animated.sequence([
        Animated.timing(animationProgress, {
          toValue: 1,
          duration: duration,
          useNativeDriver: true,
        }),
        Animated.delay(500),  // Pause before loop
      ])
    ).start();
  }, [duration]);

  const renderAnimation = () => {
    switch (stitchType) {
      case 'inc':
        return <IncreaseAnimation progress={animationProgress} />;
      case 'dec':
        return <DecreaseAnimation progress={animationProgress} />;
      case 'sc':
        return <SingleCrochetAnimation progress={animationProgress} />;
      case 'ch':
        return <ChainAnimation progress={animationProgress} />;
    }
  };

  return (
    <View style={styles.container}>
      {renderAnimation()}
    </View>
  );
};

// Example: Increase animation showing one stitch becoming two
const IncreaseAnimation: React.FC<{ progress: Animated.Value }> = ({ progress }) => {
  const splitProgress = progress.interpolate({
    inputRange: [0, 0.5, 1],
    outputRange: [0, 1, 1],
  });

  return (
    <Svg width={200} height={200} viewBox="0 0 200 200">
      {/* Base stitch */}
      <Circle cx={100} cy={100} r={20} fill="#6366f1" />

      {/* First new stitch */}
      <AnimatedCircle
        cx={progress.interpolate({
          inputRange: [0, 0.5, 1],
          outputRange: [100, 80, 80],
        })}
        cy={70}
        r={16}
        fill="#22c55e"
        opacity={splitProgress}
      />

      {/* Second new stitch */}
      <AnimatedCircle
        cx={progress.interpolate({
          inputRange: [0, 0.5, 1],
          outputRange: [100, 120, 120],
        })}
        cy={70}
        r={16}
        fill="#22c55e"
        opacity={splitProgress}
      />
    </Svg>
  );
};
```

**6. Screen Reader Support**

Comprehensive accessibility labels:

```typescript
// components/visualization/PatternViewer.tsx
import { AccessibilityInfo } from 'react-native';

export const PatternViewer: React.FC<PatternViewerProps> = ({ pattern, currentRound }) => {
  const announceRoundChange = (roundNumber: number) => {
    const roundData = pattern.rounds[roundNumber - 1];
    const announcement = `Round ${roundNumber}. ${roundData.stitches.length} stitches. ${roundData.description}`;
    AccessibilityInfo.announceForAccessibility(announcement);
  };

  return (
    <View accessible accessibilityLabel="Pattern visualization">
      <View
        accessible
        accessibilityRole="adjustable"
        accessibilityLabel={`Round ${currentRound} of ${pattern.rounds.length}`}
        accessibilityHint="Swipe up or down to change rounds"
        accessibilityValue={{ text: `Round ${currentRound}`, min: 1, max: pattern.rounds.length }}
      >
        {/* Round display */}
      </View>

      <View accessibilityRole="group" accessibilityLabel="Playback controls">
        <TouchableOpacity
          accessibilityRole="button"
          accessibilityLabel="Previous round"
          accessibilityHint="Go to previous round"
          onPress={handlePrevious}
        >
          <Icon name="chevron-left" />
        </TouchableOpacity>

        <TouchableOpacity
          accessibilityRole="button"
          accessibilityLabel={isPlaying ? "Pause" : "Play"}
          accessibilityHint={isPlaying ? "Pause automatic progression" : "Start automatic progression"}
          onPress={togglePlayback}
        >
          <Icon name={isPlaying ? "pause" : "play"} />
        </TouchableOpacity>

        <TouchableOpacity
          accessibilityRole="button"
          accessibilityLabel="Next round"
          accessibilityHint="Go to next round"
          onPress={handleNext}
        >
          <Icon name="chevron-right" />
        </TouchableOpacity>
      </View>
    </View>
  );
};
```

**7. High-Contrast Mode**

Implement high-contrast color overrides:

```typescript
// theme/colors.ts
export const colors = {
  // Standard theme (WCAG AA: 4.5:1)
  standard: {
    background: '#ffffff',
    surface: '#f5f5f5',
    text: '#1f2937',        // 4.5:1 on white
    textSecondary: '#6b7280', // 4.5:1 on white
    primary: '#6366f1',
    primaryText: '#ffffff',
    border: '#d1d5db',
  },

  // High-contrast theme (WCAG AAA: 7:1)
  highContrast: {
    background: '#000000',
    surface: '#1a1a1a',
    text: '#ffffff',        // 21:1 on black
    textSecondary: '#e5e5e5', // 15:1 on black
    primary: '#ffff00',     // 19:1 on black
    primaryText: '#000000',
    border: '#ffffff',
  },

  // Kid Mode theme (bright, friendly)
  kidMode: {
    background: '#fef3c7',  // Warm yellow
    surface: '#ffffff',
    text: '#1f2937',
    primary: '#f59e0b',     // Bright orange
    secondary: '#8b5cf6',   // Purple
    accent: '#10b981',      // Green
  },
};
```

**8. Accessibility Settings Screen**

Comprehensive settings for all accessibility options:

```typescript
// screens/SettingsScreen.tsx
export const AccessibilitySettingsScreen: React.FC = () => {
  const { kidMode, setKidMode } = useKidMode();
  const { highContrast, setHighContrast } = useAccessibility();
  const { dyslexiaFont, setDyslexiaFont } = useAccessibility();
  const { textSize, setTextSize } = useAccessibility();
  const { leftHanded, setLeftHanded } = useAccessibility();

  return (
    <ScrollView accessibilityRole="list">
      <SettingSection title="Display">
        <SettingToggle
          label="Kid Mode"
          description="Simplified language and larger buttons"
          value={kidMode}
          onValueChange={setKidMode}
          accessibilityLabel="Toggle Kid Mode"
        />

        <SettingToggle
          label="High Contrast"
          description="Increased contrast for better visibility"
          value={highContrast}
          onValueChange={setHighContrast}
          accessibilityLabel="Toggle High Contrast Mode"
        />

        <SettingToggle
          label="Dyslexia-Friendly Font"
          description="Use OpenDyslexic font for easier reading"
          value={dyslexiaFont}
          onValueChange={setDyslexiaFont}
          accessibilityLabel="Toggle Dyslexia Font"
        />

        <SettingPicker
          label="Text Size"
          description="Adjust text size for readability"
          value={textSize}
          options={[
            { label: 'Default', value: 'default' },
            { label: 'Large', value: 'large' },
            { label: 'Extra Large', value: 'xlarge' },
          ]}
          onValueChange={setTextSize}
          accessibilityLabel="Select text size"
        />
      </SettingSection>

      <SettingSection title="Layout">
        <SettingToggle
          label="Left-Handed Mode"
          description="Mirror layout for left-handed users"
          value={leftHanded}
          onValueChange={setLeftHanded}
          accessibilityLabel="Toggle Left-Handed Mode"
        />
      </SettingSection>
    </ScrollView>
  );
};
```

**9. Left-Handed Layout Support**

Apply layout mirroring when left-handed mode is enabled:

```typescript
// utils/layoutUtils.ts
import { I18nManager } from 'react-native';

export const applyLeftHandedLayout = (leftHanded: boolean) => {
  // Force RTL layout for left-handed mode
  I18nManager.forceRTL(leftHanded);
  I18nManager.allowRTL(leftHanded);
};

// components/visualization/StitchDiagram.tsx
export const StitchDiagram: React.FC = ({ pattern }) => {
  const { leftHanded } = useAccessibility();

  // Mirror x-coordinates for left-handed layout
  const mirrorX = (x: number, width: number) => {
    return leftHanded ? width - x : x;
  };

  return (
    <Svg width={width} height={height}>
      {pattern.stitches.map((stitch, idx) => (
        <Circle
          key={idx}
          cx={mirrorX(stitch.x, width)}
          cy={stitch.y}
          r={stitchRadius}
          fill={getStitchColor(stitch.type)}
        />
      ))}
    </Svg>
  );
};
```

**10. Keyboard Navigation**

Ensure full keyboard accessibility on all screens:

```typescript
// hooks/useKeyboardNavigation.ts
import { useEffect } from 'react';
import { Keyboard } from 'react-native';

export const useKeyboardNavigation = (
  onNext: () => void,
  onPrevious: () => void,
  onActivate: () => void
) => {
  useEffect(() => {
    const subscription = Keyboard.addListener('keyPress', (e) => {
      switch (e.key) {
        case 'ArrowRight':
        case 'Tab':
          onNext();
          break;
        case 'ArrowLeft':
        case 'Shift+Tab':
          onPrevious();
          break;
        case 'Enter':
        case ' ':
          onActivate();
          break;
      }
    });

    return () => subscription.remove();
  }, [onNext, onPrevious, onActivate]);
};

// Usage in PatternViewer
export const PatternViewer: React.FC = () => {
  useKeyboardNavigation(
    () => nextRound(),
    () => previousRound(),
    () => togglePlayback()
  );

  // ... component implementation
};
```

### WCAG AA Compliance Checklist

**Perceivable:**
- [ ] **1.1.1 Non-text Content:** All images have alt text; SVG diagrams have descriptions
- [ ] **1.3.1 Info and Relationships:** Semantic HTML/RN components; proper heading hierarchy
- [ ] **1.3.2 Meaningful Sequence:** Logical reading order; navigation flow makes sense
- [ ] **1.3.3 Sensory Characteristics:** Instructions don't rely solely on shape/color/position
- [ ] **1.4.1 Use of Color:** Color is not the only means of conveying information
- [ ] **1.4.3 Contrast (Minimum):** 4.5:1 for normal text, 3:1 for large text (18pt+)
- [ ] **1.4.4 Resize Text:** Text can be resized up to 200% without loss of functionality
- [ ] **1.4.5 Images of Text:** Avoid images of text (use actual text)

**Operable:**
- [ ] **2.1.1 Keyboard:** All functionality available via keyboard
- [ ] **2.1.2 No Keyboard Trap:** Focus can move away from all components
- [ ] **2.1.4 Character Key Shortcuts:** Single-key shortcuts can be turned off/remapped
- [ ] **2.2.1 Timing Adjustable:** Time limits can be extended or disabled
- [ ] **2.2.2 Pause, Stop, Hide:** Auto-playing content can be paused/stopped
- [ ] **2.3.1 Three Flashes:** Nothing flashes more than 3 times per second
- [ ] **2.4.1 Bypass Blocks:** Skip navigation links or landmarks present
- [ ] **2.4.2 Page Titled:** Each screen has descriptive title
- [ ] **2.4.3 Focus Order:** Tab order is logical and intuitive
- [ ] **2.4.4 Link Purpose:** Purpose of each link clear from context
- [ ] **2.4.5 Multiple Ways:** Multiple ways to navigate (tabs, search, menu)
- [ ] **2.4.6 Headings and Labels:** Headings and labels are descriptive
- [ ] **2.4.7 Focus Visible:** Keyboard focus is clearly visible
- [ ] **2.5.1 Pointer Gestures:** All multi-point/path-based gestures have single-pointer alternative
- [ ] **2.5.2 Pointer Cancellation:** Functions triggered on up-event or can be aborted
- [ ] **2.5.3 Label in Name:** Accessible name includes visible label text
- [ ] **2.5.4 Motion Actuation:** Motion-triggered actions can be disabled or alternative exists

**Understandable:**
- [ ] **3.1.1 Language of Page:** Primary language declared
- [ ] **3.1.2 Language of Parts:** Language changes are marked
- [ ] **3.2.1 On Focus:** Focus doesn't trigger unexpected context changes
- [ ] **3.2.2 On Input:** Input doesn't cause unexpected context changes
- [ ] **3.2.3 Consistent Navigation:** Navigation is consistent across screens
- [ ] **3.2.4 Consistent Identification:** Components with same function labeled consistently
- [ ] **3.3.1 Error Identification:** Errors are clearly identified and described
- [ ] **3.3.2 Labels or Instructions:** Labels/instructions provided for user input
- [ ] **3.3.3 Error Suggestion:** Suggestions provided for input errors
- [ ] **3.3.4 Error Prevention:** Submissions are reversible, checked, or confirmed

**Robust:**
- [ ] **4.1.1 Parsing:** No major HTML/markup errors
- [ ] **4.1.2 Name, Role, Value:** All UI components have accessible names and roles
- [ ] **4.1.3 Status Messages:** Status messages communicated to screen readers

### Testing Tools & Process

**Automated Testing:**
```bash
# Install accessibility testing tools
pnpm add -D @testing-library/react-native @testing-library/jest-native

# Run accessibility audits
pnpm test:a11y

# Use axe-core for web testing
pnpm add -D @axe-core/react

# Use Lighthouse CI for automated audits
pnpm add -D @lhci/cli
```

**Manual Testing:**

1. **iOS VoiceOver Testing:**
   - Enable VoiceOver: Settings > Accessibility > VoiceOver
   - Navigate entire app using gestures
   - Verify all elements are announced correctly
   - Check focus order and navigation

2. **Android TalkBack Testing:**
   - Enable TalkBack: Settings > Accessibility > TalkBack
   - Navigate entire app using gestures
   - Verify announcements and focus
   - Test with various Android versions

3. **Keyboard Navigation Testing:**
   - Connect external keyboard to device
   - Navigate using Tab, Shift+Tab, Arrow keys
   - Verify focus indicators are visible
   - Test activation with Enter/Space

4. **Color Contrast Testing:**
   - Use WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/
   - Verify all text meets 4.5:1 (normal) or 3:1 (large)
   - Test in high-contrast mode for 7:1 compliance

5. **Text Scaling Testing:**
   - Increase device text size to maximum
   - Verify no text is clipped or overlaps
   - Ensure layout adapts appropriately

---

## Success Criteria

### Phase 4 Success Criteria (Exit Gates)

**Functional Requirements:**
- [ ] Kid Mode toggle works; activating shows noticeably simplified UI
- [ ] All stitch terminology has kid-friendly alternatives
- [ ] Tap targets in Kid Mode are ≥ 44x44pt (measured)
- [ ] At least 3 animated stitch explanations implemented (inc, dec, sc)
- [ ] Accessibility settings screen functional with all options
- [ ] Screen reader announces all interactive elements correctly
- [ ] High-contrast mode implemented with 7:1+ contrast ratios
- [ ] Left-handed mode mirrors layout appropriately
- [ ] Dyslexia-friendly font option applies to all text
- [ ] Keyboard navigation works on all screens

**Accessibility Compliance:**
- [ ] WCAG AA automated audit: 0 critical issues, < 5 warnings
- [ ] Color contrast verified: all text meets 4.5:1 (normal) or 3:1 (large)
- [ ] Screen reader testing passed on both iOS (VoiceOver) and Android (TalkBack)
- [ ] Keyboard navigation tested: all screens accessible, focus visible
- [ ] Text scaling tested: content readable at 200% text size
- [ ] No auto-playing content without pause/stop controls

**Performance:**
- [ ] Stitch animations run at 60fps without dropped frames
- [ ] Theme switching (Kid Mode, high-contrast) is instant (< 100ms)
- [ ] Settings changes persist across app restarts
- [ ] No performance regression from accessibility features

**Documentation:**
- [ ] Accessibility features documented in user guide
- [ ] WCAG AA compliance report generated
- [ ] Accessibility testing checklist completed
- [ ] Known accessibility issues logged with workarounds

---

## Dependencies & Blockers

### Dependencies

**Internal Dependencies:**
- Settings screen infrastructure (from Phase 3)
- Theme system and design tokens established
- All screens and components implemented (Phase 3 complete)
- AsyncStorage or similar persistence mechanism

**External Dependencies:**
- OpenDyslexic or Lexend font licensed and available
- React Native accessibility APIs (built-in)
- Accessibility testing tools (axe DevTools, Lighthouse)

### Potential Blockers

| Blocker | Impact | Mitigation Strategy | Owner |
|---------|--------|---------------------|-------|
| Dyslexia font licensing delays | Medium | Use system fonts as fallback; defer to post-MVP | Frontend Lead |
| Screen reader API differences iOS/Android | Medium | Abstract platform differences; prioritize iOS if needed | Frontend Lead |
| Animation performance on low-end devices | Medium | Provide reduced-motion option; optimize animations | Frontend Eng 2 |
| Design resources for Kid Mode not ready | High | Work with designer early; use simplified existing designs | Product Owner |
| WCAG audit reveals major issues | High | Start audits early (Week 12 Day 1); iterate quickly | QA Lead |

---

## Risks

### Technical Risks

| Risk | Probability | Impact | Mitigation | Owner |
|------|-------------|--------|-----------|-------|
| **Scope creep on animations** | Medium | Medium | Time-box to 5 hours per animation; MVP can use simple fades | Frontend Eng 2 |
| **Screen reader implementation complex** | Medium | High | Start with critical screens; defer non-essential screens to Phase 5 | Frontend Lead |
| **Performance regression from accessibility features** | Low | High | Profile after implementation; optimize hot paths | Frontend Lead |
| **WCAG audit failures late in phase** | Medium | High | Integrate audits from Day 1; fix incrementally | QA Lead |
| **Theme switching causes layout bugs** | Medium | Medium | Test theme switching thoroughly; use snapshot tests | Frontend Eng 1 |

### Resource Risks

| Risk | Probability | Impact | Mitigation | Owner |
|------|-------------|--------|-----------|-------|
| **Accessibility specialist availability** | Medium | High | Frontend Lead has WCAG knowledge; hire consultant if needed | Product Owner |
| **Content writing for kid-friendly copy** | Medium | Medium | Involve team in copy review; iterate based on feedback | Frontend Lead |
| **Designer bandwidth for Kid Mode designs** | Low | Medium | Use existing design system with modifications | Product Owner |

### User Experience Risks

| Risk | Probability | Impact | Mitigation | Owner |
|------|-------------|--------|-----------|-------|
| **Kid Mode feels patronizing to older users** | Low | Medium | Clear toggle; default OFF; market as "beginner mode" | Product Owner |
| **High-contrast mode affects branding** | Low | Low | Brand colors remain in standard mode; high-contrast is opt-in | Design Lead |
| **Animations distracting or annoying** | Medium | Medium | Allow disabling; respect reduced-motion preference | Frontend Eng 2 |

---

## Phase Exit Criteria

### Must-Have (Blocking Phase 5)

- [ ] Kid Mode toggle functional with simplified UI
- [ ] WCAG AA compliance: 0 critical issues (axe DevTools)
- [ ] Screen reader labels on all interactive elements
- [ ] Color contrast verified: all text meets 4.5:1 or 3:1
- [ ] Accessibility settings screen complete and functional
- [ ] High-contrast mode implemented
- [ ] Keyboard navigation working on critical screens (Home, Generate, Visualize)

### Should-Have (Before MVP Launch)

- [ ] Animated stitch explanations (at least 3 stitches)
- [ ] Left-handed mode functional
- [ ] Dyslexia-friendly font option working
- [ ] Keyboard navigation on all screens (including Settings, Export)
- [ ] Manual screen reader testing completed (iOS + Android)

### Nice-to-Have (Can Defer to v1.1)

- [ ] Animated stitch explanations for all 20+ stitch types
- [ ] Voice control integration (Siri, Google Assistant)
- [ ] Haptic feedback for accessibility
- [ ] Additional Kid Mode themes (animals, space, etc.)

---

## Next Phase Preview

### Phase 5: QA & Polish (Weeks 14-15)

**Focus:** Comprehensive QA, accessibility audits, performance optimization, bug fixes

**Key Activities:**
- Cross-device testing (iOS 14+, Android 10+, tablets)
- Comprehensive accessibility audit (automated + manual)
- Performance profiling and optimization
- Bug triage and resolution
- Documentation updates

**Accessibility-Specific Activities:**
- Full WCAG AA manual audit
- Screen reader testing on multiple devices
- Keyboard navigation testing on all screens
- Color contrast verification for all color combinations
- Text scaling testing at multiple sizes
- Reduced motion preference testing

**Deliverables:**
- Accessibility audit report with zero critical issues
- Cross-device test results
- Performance benchmarks meeting targets
- Bug list triaged and prioritized
- Updated documentation with accessibility guidelines

**Success Criteria:**
- WCAG AA compliance: 0 critical issues, < 5 warnings
- Screen reader testing passed on iOS and Android
- All high-priority bugs fixed
- Performance targets met (generation < 200ms, visualization > 50fps)

---

## Appendix

### Accessibility Resources

**WCAG Guidelines:**
- WCAG 2.1 Overview: https://www.w3.org/WAI/WCAG21/quickref/
- Understanding WCAG 2.1: https://www.w3.org/WAI/WCAG21/Understanding/
- How to Meet WCAG (Quick Reference): https://www.w3.org/WAI/WCAG21/quickref/

**Testing Tools:**
- axe DevTools: https://www.deque.com/axe/devtools/
- WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/
- WAVE Accessibility Tool: https://wave.webaim.org/
- Lighthouse (Chrome DevTools): Built-in
- React Native Accessibility API: https://reactnative.dev/docs/accessibility

**React Native Resources:**
- Accessibility Guide: https://reactnative.dev/docs/accessibility
- VoiceOver Testing: https://developer.apple.com/documentation/accessibility/voiceover
- TalkBack Testing: https://support.google.com/accessibility/android/answer/6283677

**Fonts:**
- OpenDyslexic: https://opendyslexic.org/
- Lexend: https://www.lexend.com/
- System Font Stack: Use platform defaults when possible

### Kid Mode Copy Examples

**Standard vs Kid-Friendly Terminology:**

| Standard | Kid-Friendly |
|----------|--------------|
| "Work 2 sc in next st" | "Make 2 stitches in the next spot" |
| "Sc2tog" | "Combine 2 stitches into 1" |
| "Ch 2, turn" | "Make 2 chains, then flip your work" |
| "Insert hook in indicated st" | "Put your hook in the stitch" |
| "Fasten off" | "Cut the yarn and pull through" |
| "Skip next st" | "Jump over the next stitch" |
| "Gauge: 14 sts/10cm" | "How tight: 14 stitches fit in 10cm" |
| "Round 5: [Inc, 3 sc] × 6" | "Step 5: Do this 6 times: Add 1, then 3 regular" |

### Color Palette Contrast Ratios

**Standard Theme (WCAG AA Compliant):**

| Element | Foreground | Background | Contrast Ratio | WCAG Level |
|---------|-----------|-----------|----------------|-----------|
| Body Text | #1f2937 | #ffffff | 14.2:1 | AAA |
| Secondary Text | #6b7280 | #ffffff | 4.6:1 | AA |
| Primary Button Text | #ffffff | #6366f1 | 7.5:1 | AAA |
| Link Text | #2563eb | #ffffff | 8.6:1 | AAA |
| Error Text | #dc2626 | #ffffff | 5.9:1 | AA |
| Success Text | #16a34a | #ffffff | 4.5:1 | AA |

**High-Contrast Theme (WCAG AAA Compliant):**

| Element | Foreground | Background | Contrast Ratio | WCAG Level |
|---------|-----------|-----------|----------------|-----------|
| Body Text | #ffffff | #000000 | 21:1 | AAA |
| Secondary Text | #e5e5e5 | #000000 | 15.3:1 | AAA |
| Primary Button Text | #000000 | #ffff00 | 19.6:1 | AAA |
| Link Text | #00ffff | #000000 | 16.8:1 | AAA |
| Error Text | #ff6b6b | #000000 | 7.2:1 | AAA |
| Success Text | #51cf66 | #000000 | 10.1:1 | AAA |

**Kid Mode Theme (WCAG AA Compliant, Bright & Friendly):**

| Element | Foreground | Background | Contrast Ratio | WCAG Level |
|---------|-----------|-----------|----------------|-----------|
| Body Text | #1f2937 | #fef3c7 | 12.1:1 | AAA |
| Primary Button Text | #ffffff | #f59e0b | 4.7:1 | AA |
| Secondary Button Text | #ffffff | #8b5cf6 | 7.1:1 | AAA |
| Accent Text | #ffffff | #10b981 | 4.8:1 | AA |

---

## Document Metadata

**Document Version:** 1.0
**Last Updated:** 2025-11-05
**Owner:** Frontend Lead + Accessibility Specialist
**Status:** Approved for Planning
**Related Documents:**
- [Implementation Plan](../implementation-plan.md)
- [Phase 3: Full Feature Implementation](./phase-3.md)
- [Phase 5: QA & Polish](./phase-5.md)
- [Accessibility Guidelines](../../docs/frontend/accessibility.md)

---

**End of Phase 4: Kid Mode & Accessibility Plan**
