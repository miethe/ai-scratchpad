/**
 * Hook for managing focus indicators on interactive elements
 *
 * Provides consistent focus styling across the app for keyboard navigation
 * Focus indicator: 2px border with high contrast (3:1 ratio)
 *
 * @see Story E5: Keyboard Navigation
 */

import { useState } from 'react';
import { ViewStyle } from 'react-native';
import { colors } from '../theme/colors';

interface FocusIndicatorStyle {
  focused: boolean;
  onFocus: () => void;
  onBlur: () => void;
  focusStyle: ViewStyle;
}

/**
 * Custom hook for managing focus state and styling
 *
 * @returns Focus state, handlers, and style object
 *
 * @example
 * ```tsx
 * const { focused, onFocus, onBlur, focusStyle } = useFocusIndicator();
 *
 * <TouchableOpacity
 *   onFocus={onFocus}
 *   onBlur={onBlur}
 *   style={[styles.button, focused && focusStyle]}
 * >
 *   <Text>Click me</Text>
 * </TouchableOpacity>
 * ```
 */
export const useFocusIndicator = (): FocusIndicatorStyle => {
  const [focused, setFocused] = useState(false);

  const onFocus = () => setFocused(true);
  const onBlur = () => setFocused(false);

  const focusStyle: ViewStyle = {
    borderWidth: 2,
    borderColor: colors.info, // #3B82F6 - High contrast blue (3:1 ratio)
    borderStyle: 'solid',
  };

  return {
    focused,
    onFocus,
    onBlur,
    focusStyle,
  };
};

/**
 * Focus indicator style constant for use in StyleSheet
 * Can be used directly without the hook when focus state is managed elsewhere
 */
export const focusIndicatorStyle: ViewStyle = {
  borderWidth: 2,
  borderColor: colors.info,
  borderStyle: 'solid',
};
