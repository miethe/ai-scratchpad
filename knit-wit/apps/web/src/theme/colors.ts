export const colors = {
  // Primary brand colors
  primary: '#6366F1',
  primaryLight: '#A5B4FC',
  primaryDark: '#4338CA',

  // Secondary
  secondary: '#EC4899',
  secondaryLight: '#F9A8D4',
  secondaryDark: '#BE185D',

  // Background
  background: '#FFFFFF',
  surface: '#F9FAFB',
  surfaceSecondary: '#F3F4F6',

  // Text
  textPrimary: '#111827',
  textSecondary: '#6B7280',
  textInverse: '#FFFFFF',

  // Borders
  border: '#E5E7EB',
  borderFocus: '#6366F1',

  // Status
  success: '#10B981',
  warning: '#F59E0B',
  error: '#EF4444',
  info: '#3B82F6',

  // Visualization colors
  stitchNormal: '#6366F1',
  stitchIncrease: '#10B981',
  stitchDecrease: '#EF4444',
  edgeColor: '#9CA3AF',
} as const;

export const darkColors = {
  ...colors,
  background: '#111827',
  surface: '#1F2937',
  surfaceSecondary: '#374151',
  textPrimary: '#F9FAFB',
  textSecondary: '#D1D5DB',
  border: '#374151',
} as const;

export const kidModeColors = {
  ...colors,
  primary: '#F97316',
  primaryLight: '#FDBA74',
  primaryDark: '#EA580C',
  secondary: '#F472B6',
  secondaryLight: '#FBCFE8',
  secondaryDark: '#EC4899',
} as const;

export type ColorKey = keyof typeof colors;
