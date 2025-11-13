// Legacy exports for backward compatibility
export { colors, type ColorKey } from './colors';
export { typography, type TypographyStyle } from './typography';
export {
  spacing,
  borderRadius,
  touchTargets,
  type SpacingKey,
  type BorderRadiusKey,
} from './spacing';

/**
 * Common shadow styles for iOS and Android
 */
export const shadows = {
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
} as const;

export type ShadowSize = keyof typeof shadows;

// New theme system exports
export { ThemeProvider, useTheme } from './ThemeProvider';
export { defaultTheme, kidModeTheme, darkModeTheme, kidModeDarkTheme } from './themes';
export type {
  Theme,
  ThemeMode,
  ThemeColors,
  ThemeTypography,
  ThemeSpacing,
  ThemeBorderRadius,
  ThemeTouchTargets,
  ThemeShadows,
} from './types';
