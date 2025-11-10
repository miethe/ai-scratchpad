export const colors = {
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

  // Kid Mode palette (brighter, friendlier)
  kidPrimary: '#FF9F40',
  kidSecondary: '#4ECDC4',
  kidAccent: '#FF6B9D',
  kidBackground: '#FFF8E7',
} as const;

export type ColorKey = keyof typeof colors;
