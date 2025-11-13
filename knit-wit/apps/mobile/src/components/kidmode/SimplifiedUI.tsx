/**
 * Simplified UI Components for Kid Mode
 *
 * These components provide larger touch targets, simplified interactions,
 * and friendly visual styling optimized for young learners (ages 8-12).
 *
 * Design Requirements:
 * - Touch targets: 56-64dp minimum (WCAG AAA)
 * - Large, readable text (20-24px)
 * - High contrast colors (WCAG AA compliant)
 * - Rounded, friendly aesthetics
 * - Clear visual feedback
 *
 * @see Story E2: Simplified UI Components
 */

import React from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  type ViewStyle,
  type TextStyle,
  type TextInputProps,
  type TouchableOpacityProps,
  AccessibilityInfo,
} from 'react-native';
import { kidModeTheme } from '../../theme/kidModeTheme';

// ============================================================================
// SimplifiedButton
// ============================================================================

export interface SimplifiedButtonProps extends Omit<TouchableOpacityProps, 'style'> {
  /**
   * Button text label
   */
  label: string;

  /**
   * Optional icon component to display before text
   */
  icon?: React.ReactNode;

  /**
   * Button variant - affects styling
   * @default 'primary'
   */
  variant?: 'primary' | 'secondary' | 'outline';

  /**
   * Button size - affects dimensions
   * @default 'comfortable'
   */
  size?: 'comfortable' | 'large';

  /**
   * Disabled state
   * @default false
   */
  disabled?: boolean;

  /**
   * Additional button style overrides
   */
  style?: ViewStyle;

  /**
   * Additional text style overrides
   */
  textStyle?: TextStyle;

  /**
   * Accessibility hint (what happens when pressed)
   */
  accessibilityHint?: string;
}

/**
 * SimplifiedButton Component
 *
 * Large, friendly button optimized for Kid Mode with:
 * - Minimum 64×64 dp touch target
 * - Large text (20-24px)
 * - Rounded corners (16px border radius)
 * - High contrast colors
 * - Shadow for depth
 * - Full accessibility support
 */
export const SimplifiedButton: React.FC<SimplifiedButtonProps> = ({
  label,
  icon,
  variant = 'primary',
  size = 'comfortable',
  disabled = false,
  style,
  textStyle,
  accessibilityHint,
  onPress,
  ...rest
}) => {
  const handlePress = (event: any) => {
    if (disabled || !onPress) return;

    // Announce button press for accessibility
    AccessibilityInfo.announceForAccessibility(`${label} pressed`);
    onPress(event);
  };

  const buttonStyle = [
    styles.simplifiedButton,
    size === 'large' && styles.simplifiedButtonLarge,
    variant === 'primary' && styles.simplifiedButtonPrimary,
    variant === 'secondary' && styles.simplifiedButtonSecondary,
    variant === 'outline' && styles.simplifiedButtonOutline,
    disabled && styles.simplifiedButtonDisabled,
    style,
  ];

  const labelStyle = [
    styles.simplifiedButtonText,
    size === 'large' && styles.simplifiedButtonTextLarge,
    variant === 'primary' && styles.simplifiedButtonTextPrimary,
    variant === 'secondary' && styles.simplifiedButtonTextSecondary,
    variant === 'outline' && styles.simplifiedButtonTextOutline,
    disabled && styles.simplifiedButtonTextDisabled,
    textStyle,
  ];

  return (
    <TouchableOpacity
      style={buttonStyle}
      onPress={handlePress}
      disabled={disabled}
      accessible={true}
      accessibilityRole="button"
      accessibilityLabel={label}
      accessibilityHint={accessibilityHint || `Press to ${label.toLowerCase()}`}
      accessibilityState={{ disabled }}
      {...rest}
    >
      {icon && <View style={styles.simplifiedButtonIcon}>{icon}</View>}
      <Text style={labelStyle}>{label}</Text>
    </TouchableOpacity>
  );
};

// ============================================================================
// SimplifiedCard
// ============================================================================

export interface SimplifiedCardProps {
  /**
   * Card content
   */
  children: React.ReactNode;

  /**
   * Optional card title
   */
  title?: string;

  /**
   * Card background color variant
   * @default 'default'
   */
  variant?: 'default' | 'primary' | 'secondary' | 'success' | 'info';

  /**
   * Whether the card is selected/active
   * @default false
   */
  selected?: boolean;

  /**
   * Whether the card is pressable
   * @default false
   */
  pressable?: boolean;

  /**
   * Callback when card is pressed (only if pressable=true)
   */
  onPress?: () => void;

  /**
   * Additional style overrides
   */
  style?: ViewStyle;

  /**
   * Accessibility label for the card
   */
  accessibilityLabel?: string;

  /**
   * Accessibility hint
   */
  accessibilityHint?: string;

  /**
   * Test ID for testing
   */
  testID?: string;
}

/**
 * SimplifiedCard Component
 *
 * Friendly card component optimized for Kid Mode with:
 * - Larger padding (24px)
 * - Bright colors from Kid Mode theme
 * - Rounded corners (20px)
 * - Clear visual hierarchy
 * - Shadow for depth
 * - Optional selection state
 */
export const SimplifiedCard: React.FC<SimplifiedCardProps> = ({
  children,
  title,
  variant = 'default',
  selected = false,
  pressable = false,
  onPress,
  style,
  accessibilityLabel,
  accessibilityHint,
  testID,
}) => {
  const cardStyle = [
    styles.simplifiedCard,
    variant === 'primary' && styles.simplifiedCardPrimary,
    variant === 'secondary' && styles.simplifiedCardSecondary,
    variant === 'success' && styles.simplifiedCardSuccess,
    variant === 'info' && styles.simplifiedCardInfo,
    selected && styles.simplifiedCardSelected,
    style,
  ];

  const content = (
    <>
      {title && <Text style={styles.simplifiedCardTitle}>{title}</Text>}
      {children}
    </>
  );

  if (pressable && onPress) {
    return (
      <TouchableOpacity
        style={cardStyle}
        onPress={onPress}
        accessible={true}
        accessibilityRole="button"
        accessibilityLabel={accessibilityLabel || title}
        accessibilityHint={accessibilityHint}
        accessibilityState={{ selected }}
        testID={testID}
      >
        {content}
      </TouchableOpacity>
    );
  }

  return (
    <View
      style={cardStyle}
      accessible={true}
      accessibilityLabel={accessibilityLabel || title}
      testID={testID}
    >
      {content}
    </View>
  );
};

// ============================================================================
// SimplifiedInput
// ============================================================================

export interface SimplifiedInputProps extends TextInputProps {
  /**
   * Input label (displayed above input)
   */
  label?: string;

  /**
   * Error message to display
   */
  error?: string;

  /**
   * Helper text to display below input
   */
  helperText?: string;

  /**
   * Additional container style
   */
  containerStyle?: ViewStyle;

  /**
   * Additional input style overrides
   */
  inputStyle?: TextStyle;

  /**
   * Test ID for testing
   */
  testID?: string;
}

/**
 * SimplifiedInput Component
 *
 * Large, friendly text input optimized for Kid Mode with:
 * - Minimum height 56dp
 * - Large text (20px)
 * - Clear placeholder text
 * - High contrast border
 * - Easy to focus
 * - Clear error states
 */
export const SimplifiedInput: React.FC<SimplifiedInputProps> = ({
  label,
  error,
  helperText,
  containerStyle,
  inputStyle,
  placeholder,
  value,
  onChangeText,
  testID,
  accessibilityLabel,
  accessibilityHint,
  ...rest
}) => {
  return (
    <View style={[styles.simplifiedInputContainer, containerStyle]}>
      {label && (
        <Text
          style={styles.simplifiedInputLabel}
          accessible={true}
          accessibilityRole="text"
        >
          {label}
        </Text>
      )}
      <TextInput
        style={[
          styles.simplifiedInput,
          error && styles.simplifiedInputError,
          inputStyle,
        ]}
        placeholder={placeholder}
        placeholderTextColor={kidModeTheme.colors.textTertiary}
        value={value}
        onChangeText={onChangeText}
        accessible={true}
        accessibilityLabel={accessibilityLabel || label || placeholder}
        accessibilityHint={accessibilityHint}
        testID={testID}
        {...rest}
      />
      {error && (
        <Text
          style={styles.simplifiedInputErrorText}
          accessible={true}
          accessibilityRole="alert"
          accessibilityLiveRegion="polite"
        >
          {error}
        </Text>
      )}
      {!error && helperText && (
        <Text
          style={styles.simplifiedInputHelperText}
          accessible={true}
          accessibilityRole="text"
        >
          {helperText}
        </Text>
      )}
    </View>
  );
};

// ============================================================================
// Styles
// ============================================================================

const styles = StyleSheet.create({
  // SimplifiedButton styles
  simplifiedButton: {
    minHeight: kidModeTheme.touchTargets.comfortable, // 64dp
    minWidth: kidModeTheme.touchTargets.comfortable,
    paddingVertical: kidModeTheme.spacing.md, // 24px
    paddingHorizontal: kidModeTheme.spacing.lg, // 32px
    borderRadius: 16, // Rounded corners
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    ...kidModeTheme.shadows.md, // Shadow for depth
  },
  simplifiedButtonLarge: {
    minHeight: kidModeTheme.touchTargets.kidMode, // 72dp
    minWidth: kidModeTheme.touchTargets.kidMode,
    paddingVertical: kidModeTheme.spacing.lg, // 32px
    paddingHorizontal: kidModeTheme.spacing.xl, // 48px
  },
  simplifiedButtonPrimary: {
    backgroundColor: kidModeTheme.colors.primary, // Bright pink
  },
  simplifiedButtonSecondary: {
    backgroundColor: kidModeTheme.colors.secondary, // Sunny yellow
  },
  simplifiedButtonOutline: {
    backgroundColor: 'transparent',
    borderWidth: 3,
    borderColor: kidModeTheme.colors.primary,
  },
  simplifiedButtonDisabled: {
    backgroundColor: kidModeTheme.colors.gray300,
    opacity: 0.6,
  },
  simplifiedButtonText: {
    ...kidModeTheme.typography.bodyLarge, // 20px
    fontWeight: '600',
    textAlign: 'center',
  },
  simplifiedButtonTextLarge: {
    ...kidModeTheme.typography.titleLarge, // 24px
  },
  simplifiedButtonTextPrimary: {
    color: kidModeTheme.colors.textInverse, // White
  },
  simplifiedButtonTextSecondary: {
    color: kidModeTheme.colors.textPrimary, // Dark gray
  },
  simplifiedButtonTextOutline: {
    color: kidModeTheme.colors.primary, // Pink
  },
  simplifiedButtonTextDisabled: {
    color: kidModeTheme.colors.textTertiary,
  },
  simplifiedButtonIcon: {
    marginRight: kidModeTheme.spacing.sm, // 16px
  },

  // SimplifiedCard styles
  simplifiedCard: {
    backgroundColor: kidModeTheme.colors.surface, // White
    borderRadius: 20, // Rounded corners
    padding: kidModeTheme.spacing.md, // 24px
    ...kidModeTheme.shadows.md, // Shadow for depth
    borderWidth: 2,
    borderColor: 'transparent',
  },
  simplifiedCardPrimary: {
    backgroundColor: kidModeTheme.colors.primaryLight + '20', // Light pink with opacity
    borderColor: kidModeTheme.colors.primary,
  },
  simplifiedCardSecondary: {
    backgroundColor: kidModeTheme.colors.secondaryLight + '40', // Light yellow with opacity
    borderColor: kidModeTheme.colors.secondaryDark,
  },
  simplifiedCardSuccess: {
    backgroundColor: kidModeTheme.colors.success + '15',
    borderColor: kidModeTheme.colors.success,
  },
  simplifiedCardInfo: {
    backgroundColor: kidModeTheme.colors.info + '15',
    borderColor: kidModeTheme.colors.info,
  },
  simplifiedCardSelected: {
    borderWidth: 4,
    borderColor: kidModeTheme.colors.primary,
    ...kidModeTheme.shadows.lg, // Stronger shadow when selected
  },
  simplifiedCardTitle: {
    ...kidModeTheme.typography.titleMedium, // 18px
    color: kidModeTheme.colors.textPrimary,
    marginBottom: kidModeTheme.spacing.sm, // 16px
    fontWeight: '600',
  },

  // SimplifiedInput styles
  simplifiedInputContainer: {
    marginBottom: kidModeTheme.spacing.md, // 24px
  },
  simplifiedInputLabel: {
    ...kidModeTheme.typography.titleSmall, // 16px
    color: kidModeTheme.colors.textPrimary,
    marginBottom: kidModeTheme.spacing.xs, // 8px
    fontWeight: '600',
  },
  simplifiedInput: {
    minHeight: kidModeTheme.touchTargets.minimum, // 56dp
    backgroundColor: kidModeTheme.colors.surface,
    borderWidth: 2,
    borderColor: kidModeTheme.colors.border,
    borderRadius: 12,
    paddingHorizontal: kidModeTheme.spacing.md, // 24px
    paddingVertical: kidModeTheme.spacing.sm, // 16px
    ...kidModeTheme.typography.bodyLarge, // 20px
    color: kidModeTheme.colors.textPrimary,
  },
  simplifiedInputError: {
    borderColor: kidModeTheme.colors.error,
    borderWidth: 3,
  },
  simplifiedInputErrorText: {
    ...kidModeTheme.typography.bodySmall, // 14px
    color: kidModeTheme.colors.error,
    marginTop: kidModeTheme.spacing.xs, // 8px
  },
  simplifiedInputHelperText: {
    ...kidModeTheme.typography.bodySmall, // 14px
    color: kidModeTheme.colors.textSecondary,
    marginTop: kidModeTheme.spacing.xs, // 8px
  },
});
