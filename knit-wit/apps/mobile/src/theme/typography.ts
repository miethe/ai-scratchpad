import { Platform } from 'react-native';

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

export const typography = {
  // Display styles
  displayLarge: {
    fontFamily: fontFamily.bold,
    fontSize: 57,
    lineHeight: 64,
    fontWeight: '700' as const,
  },
  displayMedium: {
    fontFamily: fontFamily.bold,
    fontSize: 45,
    lineHeight: 52,
    fontWeight: '700' as const,
  },
  displaySmall: {
    fontFamily: fontFamily.bold,
    fontSize: 36,
    lineHeight: 44,
    fontWeight: '700' as const,
  },

  // Headline styles
  headlineLarge: {
    fontFamily: fontFamily.bold,
    fontSize: 32,
    lineHeight: 40,
    fontWeight: '700' as const,
  },
  headlineMedium: {
    fontFamily: fontFamily.bold,
    fontSize: 28,
    lineHeight: 36,
    fontWeight: '700' as const,
  },
  headlineSmall: {
    fontFamily: fontFamily.bold,
    fontSize: 24,
    lineHeight: 32,
    fontWeight: '700' as const,
  },

  // Title styles
  titleLarge: {
    fontFamily: fontFamily.medium,
    fontSize: 22,
    lineHeight: 28,
    fontWeight: '600' as const,
  },
  titleMedium: {
    fontFamily: fontFamily.medium,
    fontSize: 16,
    lineHeight: 24,
    fontWeight: '600' as const,
  },
  titleSmall: {
    fontFamily: fontFamily.medium,
    fontSize: 14,
    lineHeight: 20,
    fontWeight: '600' as const,
  },

  // Body styles
  bodyLarge: {
    fontFamily: fontFamily.regular,
    fontSize: 16,
    lineHeight: 24,
    fontWeight: '400' as const,
  },
  bodyMedium: {
    fontFamily: fontFamily.regular,
    fontSize: 14,
    lineHeight: 20,
    fontWeight: '400' as const,
  },
  bodySmall: {
    fontFamily: fontFamily.regular,
    fontSize: 12,
    lineHeight: 16,
    fontWeight: '400' as const,
  },

  // Label styles
  labelLarge: {
    fontFamily: fontFamily.medium,
    fontSize: 14,
    lineHeight: 20,
    fontWeight: '500' as const,
  },
  labelMedium: {
    fontFamily: fontFamily.medium,
    fontSize: 12,
    lineHeight: 16,
    fontWeight: '500' as const,
  },
  labelSmall: {
    fontFamily: fontFamily.medium,
    fontSize: 11,
    lineHeight: 16,
    fontWeight: '500' as const,
  },
} as const;

export type TypographyStyle = keyof typeof typography;
