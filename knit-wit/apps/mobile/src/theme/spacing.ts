/**
 * Spacing scale following 4px grid system
 * All values are in pixels for React Native
 */
export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
  xxxl: 64,
} as const;

/**
 * Border radius values
 */
export const borderRadius = {
  none: 0,
  sm: 4,
  md: 8,
  lg: 12,
  xl: 16,
  xxl: 24,
  full: 9999,
} as const;

/**
 * Touch target sizes for accessibility
 * Minimum: 44x44 points (iOS), 48x48 dp (Android)
 */
export const touchTargets = {
  minimum: 44,
  comfortable: 48,
  kidMode: 56, // Larger targets for Kid Mode
} as const;

export type SpacingKey = keyof typeof spacing;
export type BorderRadiusKey = keyof typeof borderRadius;
