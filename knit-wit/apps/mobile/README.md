# Knit-Wit Mobile App

React Native/Expo mobile application for generating parametric crochet patterns with interactive visualization.

## Tech Stack

- **Framework**: React Native 0.81 + Expo SDK 54
- **Language**: TypeScript (strict mode)
- **Navigation**: React Navigation 6 (Stack + Bottom Tabs)
- **State Management**: Zustand
- **HTTP Client**: Axios
- **Rendering**: react-native-svg
- **Testing**: Jest + React Native Testing Library
- **Linting**: ESLint + Prettier

## Prerequisites

- Node.js 18+
- pnpm 8+
- Expo CLI (installed automatically)
- iOS Simulator (macOS) or Android Emulator
- Expo Go app (for physical device testing)

## Getting Started

### Installation

From the repository root:

```bash
# Install all dependencies
pnpm install

# Or install mobile app dependencies only
pnpm --filter mobile install
```

### Development

```bash
# Start Expo dev server (from repo root)
pnpm --filter mobile dev

# Or from apps/mobile directory
pnpm dev

# Start with specific platform
pnpm android  # Opens Android emulator
pnpm ios      # Opens iOS simulator (macOS only)
pnpm web      # Opens in browser
```

### Running on Physical Device

1. Install Expo Go app from App Store/Play Store
2. Start dev server: `pnpm dev`
3. Scan QR code with Expo Go

### Testing

```bash
# Run all tests
pnpm test

# Watch mode
pnpm test:watch

# Coverage report
pnpm test:coverage
```

### Linting & Formatting

```bash
# Lint code
pnpm lint

# Auto-fix lint issues
pnpm lint:fix

# Format code
pnpm format

# Check formatting
pnpm format:check

# Type check
pnpm typecheck
```

## Project Structure

```
apps/mobile/
├── src/
│   ├── components/       # Reusable UI components
│   ├── screens/          # Screen components
│   │   ├── HomeScreen.tsx
│   │   ├── GenerateScreen.tsx
│   │   └── SettingsScreen.tsx
│   ├── navigation/       # Navigation configuration
│   │   ├── RootNavigator.tsx
│   │   └── MainTabNavigator.tsx
│   ├── stores/           # Zustand state stores
│   │   ├── useSettingsStore.ts
│   │   └── usePatternStore.ts
│   ├── services/         # API clients and external services
│   │   └── api.ts
│   ├── hooks/            # Custom React hooks
│   ├── types/            # TypeScript type definitions
│   │   ├── navigation.ts
│   │   └── pattern.ts
│   └── theme/            # Design tokens and styling
│       ├── colors.ts
│       ├── typography.ts
│       ├── spacing.ts
│       └── index.ts
├── assets/               # Static assets (images, fonts)
├── __tests__/            # Test files
├── App.tsx               # Root component
├── index.ts              # Entry point
├── app.json              # Expo configuration
├── package.json          # Dependencies and scripts
├── tsconfig.json         # TypeScript configuration
├── .eslintrc.js          # ESLint configuration
├── .prettierrc           # Prettier configuration
└── README.md
```

## Available Screens

### Home Screen

- Welcome message and app description
- Quick start card to navigate to pattern generator
- Feature highlights (parametric patterns, visualization, exports, terminology)

### Generate Screen

- Shape selection (sphere, cylinder, cone)
- Dimension inputs (diameter, height)
- Units toggle (cm/in)
- Terminology toggle (US/UK)
- Generate button (placeholder for API integration)

### Settings Screen

- Kid Mode toggle (simplified UI, future feature)
- Dark Mode toggle (future feature)
- Default terminology preference
- App version and build info
- Documentation and issue reporting links

## Key Features

### Type Safety

- Strict TypeScript mode enabled
- Comprehensive type definitions for navigation, patterns, and API
- Path aliases configured (`@/`, `@screens/`, etc.)

### Accessibility

- WCAG AA compliance
- Screen reader labels on all interactive elements
- Minimum touch target sizes (44x44 points)
- High contrast color ratios
- Semantic HTML roles

### Design System

- Consistent color palette with semantic naming
- Typography scale following Material Design
- 4px grid spacing system
- Touch target size constants for accessibility
- Reusable shadow styles for iOS/Android

### Navigation

- Stack Navigator (root level)
- Bottom Tab Navigator (main screens)
- Type-safe navigation props
- Accessibility labels on all navigation elements

### State Management

- Zustand stores for settings and patterns
- Persistent settings (future: AsyncStorage)
- Pattern generation history (in-memory for MVP)
- Error handling and loading states

## API Integration

The app includes placeholder API service (`src/services/api.ts`) ready for backend integration:

```typescript
import { patternApi } from '@services';

// Generate pattern
const result = await patternApi.generate({
  shape: 'sphere',
  diameter: 10,
  units: 'cm',
  // ... other params
});
```

Configure API base URL via environment variable:

```bash
EXPO_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## Testing Strategy

- **Unit Tests**: Component logic, hooks, stores
- **Integration Tests**: Navigation flows, API interactions
- **Coverage Target**: 60%+ (lines, branches, functions)

Example test:

```typescript
import { render, fireEvent } from '@testing-library/react-native';
import HomeScreen from '@screens/HomeScreen';

test('navigates to Generate screen on button press', () => {
  const navigate = jest.fn();
  const { getByLabelText } = render(
    <HomeScreen navigation={{ navigate }} />
  );

  fireEvent.press(getByLabelText('Start generating a pattern'));
  expect(navigate).toHaveBeenCalledWith('Generate');
});
```

## Known Issues & Future Work

### MVP Phase 0 Limitations

- API integration is placeholder (mock data)
- Kid Mode UI not implemented
- Dark mode not implemented
- No pattern visualization yet
- No export functionality yet
- No pattern persistence (in-memory only)

### Upcoming Phases

- **Phase 1**: Backend API integration, real pattern generation
- **Phase 2**: SVG visualization engine, round-by-round rendering
- **Phase 3**: Export to PDF/SVG/JSON
- **Phase 4**: Kid Mode implementation
- **Phase 5**: Pattern persistence with AsyncStorage
- **Phase 6**: Advanced features (pattern history, favorites)

## Code Quality Standards

### TypeScript

- Strict mode enabled
- No `any` types (use `unknown` if necessary)
- Explicit return types for functions
- Interface over type for object shapes

### React Best Practices

- Functional components only
- Hooks for state and side effects
- Memoization for expensive computations (React.memo, useMemo)
- Proper cleanup in useEffect

### Accessibility

- All touchable elements have `accessibilityLabel`
- All touchable elements have `accessibilityRole`
- Proper `accessibilityHint` for complex interactions
- `accessibilityState` for toggles and selected items

### Performance

- Lazy loading for screens
- Optimized images (future)
- FlatList for long lists
- Avoid inline styles where possible

## Troubleshooting

### Metro bundler won't start

```bash
# Clear Metro cache
pnpm start --clear

# Or manually
rm -rf .expo node_modules
pnpm install
```

### TypeScript errors

```bash
# Run type checker
pnpm typecheck

# Check tsconfig.json path aliases
```

### ESLint issues

```bash
# Auto-fix what's possible
pnpm lint:fix

# Check .eslintrc.js configuration
```

### Hot reload not working

- Shake device and enable Fast Refresh
- Or restart dev server: `r` in terminal

## Environment Variables

Create `.env` file (not committed to git):

```bash
EXPO_PUBLIC_API_URL=http://localhost:8000/api/v1
# Add other environment-specific config
```

## Building for Production

```bash
# Build for iOS (requires macOS)
eas build --platform ios

# Build for Android
eas build --platform android

# Submit to stores
eas submit --platform ios
eas submit --platform android
```

See [Expo EAS documentation](https://docs.expo.dev/eas/) for build configuration.

## Contributing

1. Follow existing code structure and naming conventions
2. Write tests for new features
3. Run linters before committing
4. Ensure TypeScript compilation passes
5. Test on both iOS and Android (or use Expo Go)

## Resources

- [Expo Documentation](https://docs.expo.dev/)
- [React Native Documentation](https://reactnative.dev/)
- [React Navigation Documentation](https://reactnavigation.org/)
- [Zustand Documentation](https://zustand-demo.pmnd.rs/)
- [TypeScript Documentation](https://www.typescriptlang.org/)

## License

MIT License - See repository root for details
