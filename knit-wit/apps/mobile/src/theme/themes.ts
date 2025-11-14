import type { Theme, ThemeColors, ThemeShadows, ThemeMode } from './types';
import { createTypography } from './typography';

const defaultColors: ThemeColors = {
  // Primary palette
  primary: '#6B4EFF',
  primaryLight: '#9C84FF',
  primaryDark: '#4A2DD4',

  // Secondary palette
  secondary: '#FF6B9D',
  secondaryLight: '#FFB3D0',
  secondaryDark: '#D43A7A',

  // Neutrals
  white: '#FFFFFF',
  black: '#000000',
  gray50: '#F9FAFB',
  gray100: '#F3F4F6',
  gray200: '#E5E7EB',
  gray300: '#D1D5DB',
  gray400: '#9CA3AF',
  gray500: '#6B7280',
  gray600: '#4B5563',
  gray700: '#374151',
  gray800: '#1F2937',
  gray900: '#111827',

  // Semantic colors
  success: '#10B981',
  warning: '#F59E0B',
  error: '#EF4444',
  info: '#3B82F6',

  // Background colors
  background: '#FFFFFF',
  backgroundSecondary: '#F9FAFB',
  surface: '#FFFFFF',
  surfaceSecondary: '#F3F4F6',

  // Text colors
  textPrimary: '#111827',
  textSecondary: '#6B7280',
  textTertiary: '#9CA3AF',
  textInverse: '#FFFFFF',

  // Border colors
  border: '#E5E7EB',
  borderLight: '#F3F4F6',
  borderDark: '#D1D5DB',
};

const darkModeColors: ThemeColors = {
  ...defaultColors,
  // Dark Mode: inverted colors
  primary: '#9C84FF',
  primaryLight: '#C4B5FF',
  primaryDark: '#6B4EFF',

  secondary: '#FF9DB8',
  secondaryLight: '#FFD0E0',
  secondaryDark: '#FF6B9D',

  // Dark backgrounds
  background: '#0F1419',
  backgroundSecondary: '#1A1F29',
  surface: '#1F2937',
  surfaceSecondary: '#374151',

  // Dark text colors
  textPrimary: '#F9FAFB',
  textSecondary: '#D1D5DB',
  textTertiary: '#9CA3AF',
  textInverse: '#111827',

  // Dark borders
  border: '#374151',
  borderLight: '#4B5563',
  borderDark: '#1F2937',
};

const kidModeDarkColors: ThemeColors = {
  ...darkModeColors,
  // Kid Mode Dark: combine kid mode brightness with dark theme
  // Using the same pink primary as light Kid Mode for consistency
  primary: '#FF6B9D',
  primaryLight: '#FFB3D0',
  primaryDark: '#E63D7A',

  // Sunny yellow secondary
  secondary: '#FFC837',
  secondaryLight: '#FFE29F',
  secondaryDark: '#E6A800',

  background: '#1A1410',
  backgroundSecondary: '#2D2418',
  surface: '#2D2418',
  surfaceSecondary: '#3D3128',
};

const baseShadows: ThemeShadows = {
  sm: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
    elevation: 1,
  },
  md: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  lg: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 8,
    elevation: 5,
  },
  xl: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.2,
    shadowRadius: 16,
    elevation: 8,
  },
};

const darkShadows: ThemeShadows = {
  sm: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.3,
    shadowRadius: 2,
    elevation: 1,
  },
  md: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.4,
    shadowRadius: 4,
    elevation: 3,
  },
  lg: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.5,
    shadowRadius: 8,
    elevation: 5,
  },
  xl: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.6,
    shadowRadius: 16,
    elevation: 8,
  },
};

// Inline Kid Mode theme data (extracted from kidModeTheme.ts)
// This avoids importing the entire file for tree-shaking
const kidModeColors: ThemeColors = {
  primary: '#FF6B9D',
  primaryLight: '#FFB3D0',
  primaryDark: '#E63D7A',
  secondary: '#FFC837',
  secondaryLight: '#FFE29F',
  secondaryDark: '#E6A800',
  white: '#FFFFFF',
  black: '#000000',
  gray50: '#FAFAF9',
  gray100: '#F5F5F4',
  gray200: '#E7E5E4',
  gray300: '#D6D3D1',
  gray400: '#A8A29E',
  gray500: '#78716C',
  gray600: '#57534E',
  gray700: '#44403C',
  gray800: '#292524',
  gray900: '#1C1917',
  success: '#4CAF50',
  warning: '#FF9800',
  error: '#F44336',
  info: '#2196F3',
  background: '#FFF8E1',
  backgroundSecondary: '#FFECB3',
  surface: '#FFFFFF',
  surfaceSecondary: '#FFF8E1',
  textPrimary: '#2D3748',
  textSecondary: '#4A5568',
  textTertiary: '#718096',
  textInverse: '#FFFFFF',
  border: '#E2E8F0',
  borderLight: '#F7FAFC',
  borderDark: '#CBD5E0',
};

const kidModeSpacing = {
  xs: 8,
  sm: 16,
  md: 24,
  lg: 32,
  xl: 48,
  xxl: 64,
  xxxl: 80,
};

const kidModeBorderRadius = {
  none: 0,
  sm: 8,
  md: 16,
  lg: 20,
  xl: 24,
  xxl: 32,
  full: 9999,
};

const kidModeTouchTargets = {
  minimum: 56,
  comfortable: 64,
  kidMode: 72,
};

const kidModeShadows: ThemeShadows = {
  sm: {
    shadowColor: '#FF6B9D',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.08,
    shadowRadius: 3,
    elevation: 1,
  },
  md: {
    shadowColor: '#FF6B9D',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.12,
    shadowRadius: 6,
    elevation: 3,
  },
  lg: {
    shadowColor: '#FF6B9D',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.16,
    shadowRadius: 10,
    elevation: 5,
  },
  xl: {
    shadowColor: '#FF6B9D',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.20,
    shadowRadius: 20,
    elevation: 8,
  },
};

/**
 * Create a theme based on mode and dyslexia font preference
 */
export function createTheme(options: {
  mode: ThemeMode;
  useDyslexiaFont?: boolean;
}): Theme {
  const { mode, useDyslexiaFont = false } = options;
  const typography = createTypography(useDyslexiaFont);

  const baseTheme: Theme = {
    colors: defaultColors,
    typography,
    spacing: {
      xs: 4,
      sm: 8,
      md: 16,
      lg: 24,
      xl: 32,
      xxl: 48,
      xxxl: 64,
    },
    borderRadius: {
      none: 0,
      sm: 4,
      md: 8,
      lg: 12,
      xl: 16,
      xxl: 24,
      full: 9999,
    },
    touchTargets: {
      minimum: 44,
      comfortable: 48,
      kidMode: 56,
    },
    shadows: baseShadows,
  };

  switch (mode) {
    case 'kidMode':
      return {
        ...baseTheme,
        colors: kidModeColors,
        spacing: kidModeSpacing,
        borderRadius: kidModeBorderRadius,
        touchTargets: kidModeTouchTargets,
        shadows: kidModeShadows,
      };

    case 'darkMode':
      return {
        ...baseTheme,
        colors: darkModeColors,
        shadows: darkShadows,
      };

    case 'kidModeDark':
      return {
        ...baseTheme,
        colors: kidModeDarkColors,
        spacing: kidModeSpacing,
        borderRadius: kidModeBorderRadius,
        touchTargets: kidModeTouchTargets,
        shadows: darkShadows,
      };

    default:
      return baseTheme;
  }
}

// Legacy theme exports for backward compatibility
export const defaultTheme = createTheme({ mode: 'default' });
export const kidModeTheme = createTheme({ mode: 'kidMode' });
export const darkModeTheme = createTheme({ mode: 'darkMode' });
export const kidModeDarkTheme = createTheme({ mode: 'kidModeDark' });
