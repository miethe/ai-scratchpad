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

const dyslexiaFontFamily = {
  regular: 'OpenDyslexic-Regular',
  medium: 'OpenDyslexic-Bold', // OpenDyslexic doesn't have medium, use bold
  bold: 'OpenDyslexic-Bold',
};

/**
 * Get font family based on dyslexia font preference
 */
export function getFontFamily(useDyslexiaFont: boolean) {
  return useDyslexiaFont ? dyslexiaFontFamily : fontFamily;
}

/**
 * Create typography styles with optional dyslexia font
 */
export function createTypography(useDyslexiaFont: boolean = false) {
  const fonts = getFontFamily(useDyslexiaFont);

  return {
    // Display styles
    displayLarge: {
      fontFamily: fonts.bold,
      fontSize: 57,
      lineHeight: 64,
      fontWeight: '700' as const,
    },
    displayMedium: {
      fontFamily: fonts.bold,
      fontSize: 45,
      lineHeight: 52,
      fontWeight: '700' as const,
    },
    displaySmall: {
      fontFamily: fonts.bold,
      fontSize: 36,
      lineHeight: 44,
      fontWeight: '700' as const,
    },

    // Headline styles
    headlineLarge: {
      fontFamily: fonts.bold,
      fontSize: 32,
      lineHeight: 40,
      fontWeight: '700' as const,
    },
    headlineMedium: {
      fontFamily: fonts.bold,
      fontSize: 28,
      lineHeight: 36,
      fontWeight: '700' as const,
    },
    headlineSmall: {
      fontFamily: fonts.bold,
      fontSize: 24,
      lineHeight: 32,
      fontWeight: '700' as const,
    },

    // Title styles
    titleLarge: {
      fontFamily: fonts.medium,
      fontSize: 22,
      lineHeight: 28,
      fontWeight: '600' as const,
    },
    titleMedium: {
      fontFamily: fonts.medium,
      fontSize: 16,
      lineHeight: 24,
      fontWeight: '600' as const,
    },
    titleSmall: {
      fontFamily: fonts.medium,
      fontSize: 14,
      lineHeight: 20,
      fontWeight: '600' as const,
    },

    // Body styles
    bodyLarge: {
      fontFamily: fonts.regular,
      fontSize: 16,
      lineHeight: 24,
      fontWeight: '400' as const,
    },
    bodyMedium: {
      fontFamily: fonts.regular,
      fontSize: 14,
      lineHeight: 20,
      fontWeight: '400' as const,
    },
    bodySmall: {
      fontFamily: fonts.regular,
      fontSize: 12,
      lineHeight: 16,
      fontWeight: '400' as const,
    },

    // Label styles
    labelLarge: {
      fontFamily: fonts.medium,
      fontSize: 14,
      lineHeight: 20,
      fontWeight: '500' as const,
    },
    labelMedium: {
      fontFamily: fonts.medium,
      fontSize: 12,
      lineHeight: 16,
      fontWeight: '500' as const,
    },
    labelSmall: {
      fontFamily: fonts.medium,
      fontSize: 11,
      lineHeight: 16,
      fontWeight: '500' as const,
    },

    // Font sizes (for direct fontSize usage)
    sizes: {
      xs: 11,
      sm: 12,
      md: 14,
      lg: 16,
      xl: 22,
      xxl: 28,
    },
  } as const;
}

// Default typography export (backwards compatibility)
export const typography = createTypography(false);

export type TypographyStyle = keyof typeof typography;
