# Frontend State Management

## Overview

Knit-Wit uses **Zustand** for global state management in the React Native mobile application. Zustand was chosen for its:

- **Minimal boilerplate**: Simple API with no providers or context wrappers
- **TypeScript-first**: Excellent type inference and safety
- **Performance**: Fine-grained reactivity with automatic render optimization
- **DevTools**: Built-in Redux DevTools integration
- **React Native compatibility**: Works seamlessly with React Native and Expo
- **Small bundle size**: ~1KB minified and gzipped

## Architecture Principles

### Clean Separation of Concerns

Each store manages a distinct domain of application state:

| Store | Responsibility | Persistence |
|-------|---------------|-------------|
| **Settings** | User preferences and app configuration | AsyncStorage (future) |
| **Pattern** | Pattern generation and history | Memory only (MVP) |
| **Visualization** | Viewing state and display preferences | Memory only |

### Type Safety

All stores use TypeScript strict mode with:
- Explicit interface definitions for state shape
- Typed action functions
- No implicit `any` types
- Full IDE autocomplete support

### Performance Optimization

- **Selector-based subscriptions**: Components only re-render when specific state slices change
- **Atomic updates**: State changes are batched automatically
- **Immutable updates**: Zustand uses immer-style updates internally
- **No unnecessary renders**: Fine-grained reactivity prevents cascading updates

## Store Inventory

### 1. Settings Store (`useSettingsStore`)

**Location**: `apps/mobile/src/stores/useSettingsStore.ts`

**Purpose**: Manages user preferences and application configuration that persists across sessions.

**State Shape**:

```typescript
interface SettingsState {
  // Appearance
  kidMode: boolean;
  darkMode: boolean;

  // Pattern defaults
  defaultUnits: Units;
  defaultTerminology: Terminology;

  // Actions
  setKidMode: (enabled: boolean) => void;
  setDarkMode: (enabled: boolean) => void;
  setDefaultUnits: (units: Units) => void;
  setDefaultTerminology: (terminology: Terminology) => void;
}
```

**Default Values**:
- `kidMode`: `false`
- `darkMode`: `false`
- `defaultUnits`: `'cm'`
- `defaultTerminology`: `'US'`

**Usage Example**:

```typescript
import { useSettingsStore } from '../stores';

function SettingsScreen() {
  // Subscribe to specific state slices
  const kidMode = useSettingsStore((state) => state.kidMode);
  const setKidMode = useSettingsStore((state) => state.setKidMode);

  // Or subscribe to multiple values
  const { darkMode, setDarkMode } = useSettingsStore((state) => ({
    darkMode: state.darkMode,
    setDarkMode: state.setDarkMode,
  }));

  return (
    <View>
      <Switch value={kidMode} onValueChange={setKidMode} />
      <Switch value={darkMode} onValueChange={setDarkMode} />
    </View>
  );
}
```

**Future Enhancements**:
- AsyncStorage persistence for settings
- Export preferences (PDF/SVG options)
- Language/locale preferences
- Accessibility settings (font scaling, high contrast)

---

### 2. Pattern Store (`usePatternStore`)

**Location**: `apps/mobile/src/stores/usePatternStore.ts`

**Purpose**: Manages pattern generation state, current pattern data, and recent pattern history.

**State Shape**:

```typescript
interface PatternState {
  // Current pattern state
  currentPattern: PatternDSL | null;
  isGenerating: boolean;
  error: string | null;

  // Pattern history (for MVP, kept in memory only)
  recentPatterns: PatternDSL[];

  // Actions
  generatePattern: (request: PatternRequest) => Promise<void>;
  clearPattern: () => void;
  setError: (error: string | null) => void;
  addToHistory: (pattern: PatternDSL) => void;
}
```

**Default Values**:
- `currentPattern`: `null`
- `isGenerating`: `false`
- `error`: `null`
- `recentPatterns`: `[]`

**Usage Example**:

```typescript
import { usePatternStore } from '../stores';
import type { PatternRequest } from '../types';

function GenerateScreen() {
  const { currentPattern, isGenerating, error, generatePattern } = usePatternStore(
    (state) => ({
      currentPattern: state.currentPattern,
      isGenerating: state.isGenerating,
      error: state.error,
      generatePattern: state.generatePattern,
    })
  );

  const handleGenerate = async () => {
    const request: PatternRequest = {
      shape: 'sphere',
      diameter: 10,
      units: 'cm',
      gauge: { sts_per_10cm: 14, rows_per_10cm: 16 },
      stitch: 'sc',
      terms: 'US',
    };

    await generatePattern(request);
  };

  return (
    <View>
      <Button onPress={handleGenerate} disabled={isGenerating}>
        {isGenerating ? 'Generating...' : 'Generate Pattern'}
      </Button>
      {error && <Text style={styles.error}>{error}</Text>}
      {currentPattern && <PatternViewer pattern={currentPattern} />}
    </View>
  );
}
```

**Implementation Notes**:

The `generatePattern` action is async and handles the full lifecycle:

```typescript
generatePattern: async (request: PatternRequest) => {
  set({ isGenerating: true, error: null });
  try {
    // API call to backend (placeholder for MVP)
    const response = await patternApi.generate(request);
    set({ currentPattern: response.dsl, isGenerating: false });
    get().addToHistory(response.dsl);
  } catch (error) {
    set({
      error: error instanceof Error ? error.message : 'Failed to generate pattern',
      isGenerating: false,
    });
  }
}
```

**Pattern History**:

Recent patterns are stored in memory (max 10):

```typescript
addToHistory: (pattern) => {
  const { recentPatterns } = get();
  const updated = [pattern, ...recentPatterns].slice(0, 10);
  set({ recentPatterns: updated });
}
```

**Future Enhancements**:
- Backend API integration (replace mock)
- Pattern persistence (database storage)
- Pattern favorites/bookmarks
- Pattern search and filtering
- Pattern versioning and revisions

---

### 3. Visualization Store (`useVisualizationStore`)

**Location**: `apps/mobile/src/stores/useVisualizationStore.ts`

**Purpose**: Manages the interactive visualization state including current round, zoom/pan controls, and display preferences.

**State Shape**:

```typescript
interface VisualizationState {
  // Current viewing state
  currentRound: number;
  zoomLevel: number;
  isPanning: boolean;
  panOffset: { x: number; y: number };

  // Display preferences
  highlightChanges: boolean;
  showStitchCount: boolean;
  showRoundNumbers: boolean;
  animationSpeed: 'slow' | 'medium' | 'fast';

  // Visualization mode
  viewMode: '2D' | '3D';

  // Actions
  setCurrentRound: (round: number) => void;
  nextRound: () => void;
  previousRound: () => void;
  setZoomLevel: (level: number) => void;
  zoomIn: () => void;
  zoomOut: () => void;
  resetZoom: () => void;
  setPanning: (isPanning: boolean) => void;
  setPanOffset: (offset: { x: number; y: number }) => void;
  resetPan: () => void;
  setHighlightChanges: (enabled: boolean) => void;
  setShowStitchCount: (enabled: boolean) => void;
  setShowRoundNumbers: (enabled: boolean) => void;
  setAnimationSpeed: (speed: 'slow' | 'medium' | 'fast') => void;
  setViewMode: (mode: '2D' | '3D') => void;
  resetVisualization: () => void;
}
```

**Default Values**:
- `currentRound`: `0`
- `zoomLevel`: `1.0`
- `isPanning`: `false`
- `panOffset`: `{ x: 0, y: 0 }`
- `highlightChanges`: `true`
- `showStitchCount`: `true`
- `showRoundNumbers`: `true`
- `animationSpeed`: `'medium'`
- `viewMode`: `'2D'`

**Constants**:
- `DEFAULT_ZOOM`: `1.0`
- `MIN_ZOOM`: `0.5`
- `MAX_ZOOM`: `3.0`
- `ZOOM_STEP`: `0.25`

**Usage Example**:

```typescript
import { useVisualizationStore } from '../stores';

function VisualizationScreen() {
  const {
    currentRound,
    zoomLevel,
    nextRound,
    previousRound,
    zoomIn,
    zoomOut,
  } = useVisualizationStore((state) => ({
    currentRound: state.currentRound,
    zoomLevel: state.zoomLevel,
    nextRound: state.nextRound,
    previousRound: state.previousRound,
    zoomIn: state.zoomIn,
    zoomOut: state.zoomOut,
  }));

  return (
    <View>
      <SVGVisualization round={currentRound} zoom={zoomLevel} />

      <View style={styles.controls}>
        <Button onPress={previousRound} disabled={currentRound === 0}>
          Previous Round
        </Button>
        <Text>Round {currentRound + 1}</Text>
        <Button onPress={nextRound}>Next Round</Button>
      </View>

      <View style={styles.zoomControls}>
        <Button onPress={zoomOut}>-</Button>
        <Text>{Math.round(zoomLevel * 100)}%</Text>
        <Button onPress={zoomIn}>+</Button>
      </View>
    </View>
  );
}
```

**Zoom Clamping**:

Zoom level is automatically clamped to safe bounds:

```typescript
setZoomLevel: (level) => {
  const clampedZoom = Math.max(MIN_ZOOM, Math.min(MAX_ZOOM, level));
  set({ zoomLevel: clampedZoom });
}
```

**Round Navigation**:

Round navigation prevents negative values:

```typescript
setCurrentRound: (round) => set({ currentRound: Math.max(0, round) }),
previousRound: () => {
  const { currentRound } = get();
  set({ currentRound: Math.max(0, currentRound - 1) });
}
```

**Future Enhancements**:
- 3D visualization support (three.js/react-three-fiber)
- Touch gesture controls (pinch-to-zoom, pan)
- Animation playback controls
- Screenshot/export current view
- Comparison mode (side-by-side rounds)

---

## Common Patterns

### 1. Subscribing to State

**Subscribe to a single value**:

```typescript
const kidMode = useSettingsStore((state) => state.kidMode);
```

**Subscribe to multiple values** (creates a new object on every render):

```typescript
const { kidMode, darkMode } = useSettingsStore((state) => ({
  kidMode: state.kidMode,
  darkMode: state.darkMode,
}));
```

**Subscribe to multiple values (optimized)** using `shallow` comparison:

```typescript
import { shallow } from 'zustand/shallow';

const { kidMode, darkMode } = useSettingsStore(
  (state) => ({ kidMode: state.kidMode, darkMode: state.darkMode }),
  shallow
);
```

### 2. Accessing State Outside Components

Use the store's `getState()` method:

```typescript
import { usePatternStore } from '../stores';

export async function exportPattern() {
  const { currentPattern } = usePatternStore.getState();

  if (!currentPattern) {
    throw new Error('No pattern to export');
  }

  // Export logic...
}
```

### 3. Setting State Directly

Use `setState()` for direct updates (useful in utilities):

```typescript
useVisualizationStore.setState({ currentRound: 0, zoomLevel: 1.0 });
```

### 4. Computed/Derived State

Create selector functions for derived state:

```typescript
// In a separate file: stores/selectors.ts
export const selectTotalPatterns = (state: PatternState) =>
  state.recentPatterns.length;

export const selectHasPattern = (state: PatternState) =>
  state.currentPattern !== null;

// Usage
import { usePatternStore } from '../stores';
import { selectHasPattern } from '../stores/selectors';

const hasPattern = usePatternStore(selectHasPattern);
```

### 5. Combining Multiple Stores

Components can subscribe to multiple stores:

```typescript
function PatternGenerator() {
  const defaultUnits = useSettingsStore((state) => state.defaultUnits);
  const defaultTerms = useSettingsStore((state) => state.defaultTerminology);
  const generatePattern = usePatternStore((state) => state.generatePattern);

  const handleGenerate = async (shape: ShapeType, diameter: number) => {
    await generatePattern({
      shape,
      diameter,
      units: defaultUnits,
      terms: defaultTerms,
      // ... other params
    });
  };

  return <GenerateForm onSubmit={handleGenerate} />;
}
```

---

## Adding New State

### Step 1: Decide Which Store

Ask yourself:
- **Is this user preference?** → Settings Store
- **Is this pattern-related data?** → Pattern Store
- **Is this visualization UI state?** → Visualization Store
- **None of the above?** → Create a new store

### Step 2: Update the Interface

Add your state to the appropriate store interface:

```typescript
interface SettingsState {
  // Existing state...

  // New state
  exportFormat: 'pdf' | 'svg' | 'json';

  // Actions
  setExportFormat: (format: 'pdf' | 'svg' | 'json') => void;
}
```

### Step 3: Add Initial State

```typescript
export const useSettingsStore = create<SettingsState>((set) => ({
  // Existing state...

  // New state
  exportFormat: 'pdf',

  // Actions
  setExportFormat: (format) => set({ exportFormat: format }),
}));
```

### Step 4: Use in Components

```typescript
const { exportFormat, setExportFormat } = useSettingsStore((state) => ({
  exportFormat: state.exportFormat,
  setExportFormat: state.setExportFormat,
}));
```

---

## Creating a New Store

If none of the existing stores fit your needs, create a new one:

### Template

```typescript
// apps/mobile/src/stores/useMyStore.ts
import { create } from 'zustand';

interface MyState {
  // State shape
  myValue: string;
  myNumber: number;

  // Actions
  setMyValue: (value: string) => void;
  incrementNumber: () => void;
  reset: () => void;
}

const INITIAL_STATE = {
  myValue: 'default',
  myNumber: 0,
};

export const useMyStore = create<MyState>((set, get) => ({
  // Initial state
  ...INITIAL_STATE,

  // Actions
  setMyValue: (value) => set({ myValue: value }),

  incrementNumber: () => {
    const { myNumber } = get();
    set({ myNumber: myNumber + 1 });
  },

  reset: () => set(INITIAL_STATE),
}));
```

### Register in Index

```typescript
// apps/mobile/src/stores/index.ts
export { useSettingsStore } from './useSettingsStore';
export { usePatternStore } from './usePatternStore';
export { useVisualizationStore } from './useVisualizationStore';
export { useMyStore } from './useMyStore'; // Add new store
```

---

## Testing State

### Unit Testing Stores

```typescript
// __tests__/stores/useSettingsStore.test.ts
import { renderHook, act } from '@testing-library/react-native';
import { useSettingsStore } from '../../stores';

describe('useSettingsStore', () => {
  it('should toggle kid mode', () => {
    const { result } = renderHook(() => useSettingsStore());

    expect(result.current.kidMode).toBe(false);

    act(() => {
      result.current.setKidMode(true);
    });

    expect(result.current.kidMode).toBe(true);
  });

  it('should update default units', () => {
    const { result } = renderHook(() => useSettingsStore());

    act(() => {
      result.current.setDefaultUnits('in');
    });

    expect(result.current.defaultUnits).toBe('in');
  });
});
```

### Integration Testing with Components

```typescript
// __tests__/screens/SettingsScreen.test.tsx
import { render, fireEvent } from '@testing-library/react-native';
import { SettingsScreen } from '../../screens/SettingsScreen';
import { useSettingsStore } from '../../stores';

describe('SettingsScreen', () => {
  beforeEach(() => {
    // Reset store state before each test
    useSettingsStore.setState({
      kidMode: false,
      darkMode: false,
      defaultUnits: 'cm',
      defaultTerminology: 'US',
    });
  });

  it('should toggle kid mode when switch is pressed', () => {
    const { getByTestId } = render(<SettingsScreen />);
    const kidModeSwitch = getByTestId('kid-mode-switch');

    fireEvent(kidModeSwitch, 'valueChange', true);

    expect(useSettingsStore.getState().kidMode).toBe(true);
  });
});
```

---

## Performance Best Practices

### 1. Use Selectors Wisely

**Bad** (entire store re-renders component):
```typescript
const store = useSettingsStore();
return <Text>{store.kidMode}</Text>;
```

**Good** (only re-renders when kidMode changes):
```typescript
const kidMode = useSettingsStore((state) => state.kidMode);
return <Text>{kidMode}</Text>;
```

### 2. Memoize Complex Selectors

```typescript
import { useMemo } from 'react';

const selector = useMemo(
  () => (state: PatternState) => ({
    hasPattern: state.currentPattern !== null,
    isReady: !state.isGenerating && state.error === null,
  }),
  []
);

const { hasPattern, isReady } = usePatternStore(selector, shallow);
```

### 3. Avoid Creating New Objects in Selectors

**Bad** (creates new array every time):
```typescript
const patterns = usePatternStore((state) =>
  state.recentPatterns.slice(0, 5)
);
```

**Good** (use shallow comparison):
```typescript
import { shallow } from 'zustand/shallow';

const patterns = usePatternStore(
  (state) => state.recentPatterns.slice(0, 5),
  shallow
);
```

### 4. Batch Related Updates

**Bad** (triggers multiple re-renders):
```typescript
setCurrentRound(5);
setZoomLevel(2.0);
setPanOffset({ x: 10, y: 20 });
```

**Good** (single re-render):
```typescript
useVisualizationStore.setState({
  currentRound: 5,
  zoomLevel: 2.0,
  panOffset: { x: 10, y: 20 },
});
```

---

## DevTools Integration

### Setup (Development Only)

Install Redux DevTools middleware:

```bash
pnpm add -D @redux-devtools/extension
```

Create store with DevTools:

```typescript
import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

interface MyState {
  // ... state definition
}

export const useMyStore = create<MyState>()(
  devtools(
    (set, get) => ({
      // ... implementation
    }),
    { name: 'MyStore' }
  )
);
```

### Time Travel Debugging

With DevTools enabled, you can:
- Inspect state at any point in time
- Replay actions
- Import/export state snapshots
- Monitor performance

---

## Persistence (Future)

### AsyncStorage Middleware

For settings that should persist across app restarts:

```typescript
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

export const useSettingsStore = create<SettingsState>()(
  persist(
    (set) => ({
      // ... state implementation
    }),
    {
      name: 'settings-storage',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
```

This will automatically:
- Save state to AsyncStorage on changes
- Restore state on app launch
- Handle serialization/deserialization

---

## Migration Guide

### From useState to Zustand

**Before** (component-local state):
```typescript
function MyComponent() {
  const [kidMode, setKidMode] = useState(false);

  return <Switch value={kidMode} onValueChange={setKidMode} />;
}
```

**After** (global Zustand state):
```typescript
// In stores/useSettingsStore.ts
interface SettingsState {
  kidMode: boolean;
  setKidMode: (enabled: boolean) => void;
}

export const useSettingsStore = create<SettingsState>((set) => ({
  kidMode: false,
  setKidMode: (enabled) => set({ kidMode: enabled }),
}));

// In component
function MyComponent() {
  const { kidMode, setKidMode } = useSettingsStore((state) => ({
    kidMode: state.kidMode,
    setKidMode: state.setKidMode,
  }));

  return <Switch value={kidMode} onValueChange={setKidMode} />;
}
```

---

## Troubleshooting

### Issue: Component not re-rendering

**Symptom**: State changes but component doesn't update

**Solution**: Check your selector - you might be subscribing to the entire store instead of specific values:

```typescript
// Wrong - subscribes to entire store
const store = useSettingsStore();

// Right - subscribes to specific value
const kidMode = useSettingsStore((state) => state.kidMode);
```

### Issue: Too many re-renders

**Symptom**: Performance issues, console warnings about max update depth

**Solution**: You might be creating new objects in your selector:

```typescript
// Wrong - creates new object every render
const config = useSettingsStore((state) => ({
  units: state.defaultUnits,
  terms: state.defaultTerminology,
}));

// Right - use shallow comparison
import { shallow } from 'zustand/shallow';

const config = useSettingsStore(
  (state) => ({
    units: state.defaultUnits,
    terms: state.defaultTerminology,
  }),
  shallow
);
```

### Issue: State not persisting

**Symptom**: Settings reset on app restart

**Solution**: Implement persistence middleware (see Persistence section above)

### Issue: TypeScript errors with store

**Symptom**: Type errors when using store

**Solution**: Ensure you're using the typed hook correctly:

```typescript
// Wrong - loses type information
const store = useSettingsStore();

// Right - maintains full type safety
const kidMode = useSettingsStore((state) => state.kidMode);
```

---

## References

- [Zustand Documentation](https://docs.pmnd.rs/zustand)
- [React Native Performance](https://reactnative.dev/docs/performance)
- [TypeScript Best Practices](https://www.typescriptlang.org/docs/handbook/react.html)
- [Testing React Native](https://reactnative.dev/docs/testing-overview)

---

## Summary

Knit-Wit's state management architecture provides:

1. **Three specialized stores** for distinct domains
2. **Type-safe** operations with full TypeScript support
3. **Performance-optimized** with fine-grained subscriptions
4. **Developer-friendly** with minimal boilerplate
5. **Testable** with comprehensive testing utilities
6. **Scalable** with clear patterns for extending functionality

When working with state:
- Use the appropriate store for your domain
- Subscribe to specific values, not entire stores
- Test state changes in isolation
- Follow the established patterns for consistency
- Document new state additions

For questions or architectural discussions, refer to the planning documents in `project_plans/mvp/` or consult the development team.
