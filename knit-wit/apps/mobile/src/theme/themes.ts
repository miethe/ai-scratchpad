import { Platform } from 'react-native';
import type { Theme, ThemeColors, ThemeTypography, ThemeShadows } from './types';

const fontFamily = {
  regular: Platform.select({
    ios: 'System',
    android: 'Roboto',
    default: 'System',
  }),
  medium: Platform.select({
    ios: 'System',
    android: 'Roboto-Medium',
    default: 'System',
  }),
  bold: Platform.select({
    ios: 'System',
    android: 'Roboto-Bold',
    default: 'System',
  }),
};

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

const kidModeColors: ThemeColors = {
  ...defaultColors,
  // Kid Mode: bright, friendly colors
  primary: '#FF9F40', // Bright orange
  primaryLight: '#FFBD73',
  primaryDark: '#E67A00',

  secondary: '#FF6B9D', // Pink (already friendly)
  secondaryLight: '#FFB3D0',
  secondaryDark: '#D43A7A',

  // Accent color for highlights
  info: '#4ECDC4', // Turquoise

  // Warm, friendly background
  background: '#FFF8E7',
  backgroundSecondary: '#FFF0CC',
  surface: '#FFFFFF',
  surfaceSecondary: '#FFF8E7',
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
  primary: '#FFBD73',
  primaryLight: '#FFD9A3',
  primaryDark: '#FF9F40',

  secondary: '#FFB3D0',
  secondaryLight: '#FFD9E8',
  secondaryDark: '#FF9DB8',

  background: '#1A1410',
  backgroundSecondary: '#2D2418',
  surface: '#2D2418',
  surfaceSecondary: '#3D3128',
};

const baseTypography: ThemeTypography = {
  displayLarge: {
    fontFamily: fontFamily.bold,
    fontSize: 57,
    lineHeight: 64,
    fontWeight: '700',
  },
  displayMedium: {
    fontFamily: fontFamily.bold,
    fontSize: 45,
    lineHeight: 52,
    fontWeight: '700',
  },
  displaySmall: {
    fontFamily: fontFamily.bold,
    fontSize: 36,
    lineHeight: 44,
    fontWeight: '700',
  },
  headlineLarge: {
    fontFamily: fontFamily.bold,
    fontSize: 32,
    lineHeight: 40,
    fontWeight: '700',
  },
  headlineMedium: {
    fontFamily: fontFamily.bold,
    fontSize: 28,
    lineHeight: 36,
    fontWeight: '700',
  },
  headlineSmall: {
    fontFamily: fontFamily.bold,
    fontSize: 24,
    lineHeight: 32,
    fontWeight: '700',
  },
  titleLarge: {
    fontFamily: fontFamily.medium,
    fontSize: 22,
    lineHeight: 28,
    fontWeight: '600',
  },
  titleMedium: {
    fontFamily: fontFamily.medium,
    fontSize: 16,
    lineHeight: 24,
    fontWeight: '600',
  },
  titleSmall: {
    fontFamily: fontFamily.medium,
    fontSize: 14,
    lineHeight: 20,
    fontWeight: '600',
  },
  bodyLarge: {
    fontFamily: fontFamily.regular,
    fontSize: 16,
    lineHeight: 24,
    fontWeight: '400',
  },
  bodyMedium: {
    fontFamily: fontFamily.regular,
    fontSize: 14,
    lineHeight: 20,
    fontWeight: '400',
  },
  bodySmall: {
    fontFamily: fontFamily.regular,
    fontSize: 12,
    lineHeight: 16,
    fontWeight: '400',
  },
  labelLarge: {
    fontFamily: fontFamily.medium,
    fontSize: 14,
    lineHeight: 20,
    fontWeight: '500',
  },
  labelMedium: {
    fontFamily: fontFamily.medium,
    fontSize: 12,
    lineHeight: 16,
    fontWeight: '500',
  },
  labelSmall: {
    fontFamily: fontFamily.medium,
    fontSize: 11,
    lineHeight: 16,
    fontWeight: '500',
  },
};

const kidModeTypography: ThemeTypography = {
  ...baseTypography,
  // Kid Mode: larger, more readable fonts
  displayLarge: {
    ...baseTypography.displayLarge,
    fontSize: 64,
    lineHeight: 72,
  },
  displayMedium: {
    ...baseTypography.displayMedium,
    fontSize: 52,
    lineHeight: 60,
  },
  displaySmall: {
    ...baseTypography.displaySmall,
    fontSize: 42,
    lineHeight: 52,
  },
  bodyLarge: {
    ...baseTypography.bodyLarge,
    fontSize: 18,
    lineHeight: 28,
  },
  bodyMedium: {
    ...baseTypography.bodyMedium,
    fontSize: 16,
    lineHeight: 24,
  },
  bodySmall: {
    ...baseTypography.bodySmall,
    fontSize: 14,
    lineHeight: 20,
  },
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

export const defaultTheme: Theme = {
  colors: defaultColors,
  typography: baseTypography,
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

export const kidModeTheme: Theme = {
  ...defaultTheme,
  colors: kidModeColors,
  typography: kidModeTypography,
};

export const darkModeTheme: Theme = {
  ...defaultTheme,
  colors: darkModeColors,
  shadows: darkShadows,
};

export const kidModeDarkTheme: Theme = {
  ...defaultTheme,
  colors: kidModeDarkColors,
  typography: kidModeTypography,
  shadows: darkShadows,
};
