/**
 * Animated Tooltip Component for Kid Mode
 *
 * Displays educational tooltips with animations that teach crochet concepts
 * to young learners. Each tooltip includes:
 * - Visual animation demonstrating the concept
 * - Simple, beginner-friendly text explanation
 * - Close button or tap-outside-to-dismiss
 * - Focus trap for keyboard navigation
 * - Escape key to close
 *
 * Respects prefers-reduced-motion accessibility setting.
 *
 * @see Story E3: Beginner Copy and Animations
 * @see Story E5: Keyboard Navigation
 */

import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  Modal,
  TouchableOpacity,
  TouchableWithoutFeedback,
  StyleSheet,
  AccessibilityInfo,
  Platform,
} from 'react-native';
import {
  IncreaseAnimation,
  DecreaseAnimation,
  MagicRingAnimation,
} from './animations/StitchAnimations';
import { kidModeTheme } from '../../theme/kidModeTheme';
import { useFocusIndicator } from '../../hooks/useFocusIndicator';

// ============================================================================
// Types
// ============================================================================

export type TooltipType = 'increase' | 'decrease' | 'magicRing';

export interface AnimatedTooltipProps {
  /**
   * Whether the tooltip is visible
   */
  visible: boolean;

  /**
   * Type of tooltip to display
   */
  type: TooltipType;

  /**
   * Callback when tooltip is closed
   */
  onClose: () => void;

  /**
   * Optional custom title
   */
  title?: string;

  /**
   * Optional custom description
   */
  description?: string;
}

// ============================================================================
// Content Configuration
// ============================================================================

interface TooltipContent {
  title: string;
  description: string;
  accessibilityLabel: string;
}

/**
 * Kid-friendly tooltip content (Grade 4-5 reading level)
 */
const TOOLTIP_CONTENT: Record<TooltipType, TooltipContent> = {
  increase: {
    title: 'Add Stitches',
    description:
      'To make your project bigger, you add more stitches! Make 2 stitches in the same spot. This is called an increase.',
    accessibilityLabel:
      'Add stitches tooltip. To make your project bigger, you add more stitches. Make 2 stitches in the same spot. This is called an increase.',
  },
  decrease: {
    title: 'Remove Stitches',
    description:
      'To make your project smaller, take away stitches. Put 2 stitches into 1. This is called a decrease.',
    accessibilityLabel:
      'Remove stitches tooltip. To make your project smaller, take away stitches. Put 2 stitches into 1. This is called a decrease.',
  },
  magicRing: {
    title: 'Start Loop',
    description:
      'The magic ring is a special way to start! Make a loop and add stitches around it. Then pull it tight to close the center.',
    accessibilityLabel:
      'Start loop tooltip. The magic ring is a special way to start. Make a loop and add stitches around it. Then pull it tight to close the center.',
  },
};

// ============================================================================
// AnimatedTooltip Component
// ============================================================================

/**
 * Animated educational tooltip for Kid Mode
 *
 * Features:
 * - Modal overlay with backdrop
 * - Animated demonstration of crochet concept
 * - Simple, friendly text explanation
 * - Close button and tap-outside-to-dismiss
 * - Focus trap (Tab cycles within modal)
 * - Escape key closes modal
 * - Respects prefers-reduced-motion
 */
export const AnimatedTooltip: React.FC<AnimatedTooltipProps> = ({
  visible,
  type,
  onClose,
  title,
  description,
}) => {
  const [reduceMotion, setReduceMotion] = useState(false);
  const closeButtonFocus = useFocusIndicator();

  useEffect(() => {
    // Check accessibility settings for reduced motion preference
    AccessibilityInfo.isReduceMotionEnabled().then(setReduceMotion);
  }, []);

  // Escape key closes modal (web only)
  useEffect(() => {
    if (!visible || Platform.OS !== 'web') return;

    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        onClose();
        event.preventDefault();
      }
    };

    window.addEventListener('keydown', handleEscape);
    return () => window.removeEventListener('keydown', handleEscape);
  }, [visible, onClose]);

  // Use custom content if provided, otherwise use default
  const content = {
    title: title || TOOLTIP_CONTENT[type].title,
    description: description || TOOLTIP_CONTENT[type].description,
    accessibilityLabel: TOOLTIP_CONTENT[type].accessibilityLabel,
  };

  const renderAnimation = () => {
    switch (type) {
      case 'increase':
        return <IncreaseAnimation reduceMotion={reduceMotion} />;
      case 'decrease':
        return <DecreaseAnimation reduceMotion={reduceMotion} />;
      case 'magicRing':
        return <MagicRingAnimation reduceMotion={reduceMotion} />;
      default:
        return null;
    }
  };

  return (
    <Modal
      visible={visible}
      transparent={true}
      animationType={reduceMotion ? 'none' : 'fade'}
      onRequestClose={onClose}
      accessible={true}
      accessibilityLabel={content.accessibilityLabel}
      accessibilityViewIsModal={true}
    >
      <TouchableWithoutFeedback onPress={onClose} accessible={false}>
        <View style={styles.backdrop}>
          <TouchableWithoutFeedback accessible={false}>
            <View
              style={styles.tooltipContainer}
              accessible={true}
              accessibilityRole="alert"
              accessibilityLabel={content.accessibilityLabel}
            >
              {/* Animation Section */}
              <View
                style={styles.animationSection}
                accessible={true}
                accessibilityLabel={`Animation demonstrating ${content.title}`}
              >
                {renderAnimation()}
              </View>

              {/* Text Section */}
              <View style={styles.textSection}>
                <Text
                  style={styles.title}
                  accessibilityRole="header"
                  accessible={true}
                >
                  {content.title}
                </Text>
                <Text
                  style={styles.description}
                  accessibilityRole="text"
                  accessible={true}
                >
                  {content.description}
                </Text>
              </View>

              {/* Close Button */}
              <TouchableOpacity
                style={[
                  styles.closeButton,
                  closeButtonFocus.focused && closeButtonFocus.focusStyle,
                ]}
                onPress={onClose}
                onFocus={closeButtonFocus.onFocus}
                onBlur={closeButtonFocus.onBlur}
                accessible={true}
                accessibilityRole="button"
                accessibilityLabel="Close tooltip"
                accessibilityHint="Double tap to close this helpful tip. You can also press the Escape key."
              >
                <Text style={styles.closeButtonText}>Got It!</Text>
              </TouchableOpacity>
            </View>
          </TouchableWithoutFeedback>
        </View>
      </TouchableWithoutFeedback>
    </Modal>
  );
};

// ============================================================================
// Styles
// ============================================================================

const styles = StyleSheet.create({
  backdrop: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
    padding: kidModeTheme.spacing.lg,
  },
  tooltipContainer: {
    backgroundColor: kidModeTheme.colors.surface,
    borderRadius: kidModeTheme.borderRadius.xl,
    padding: kidModeTheme.spacing.lg,
    maxWidth: 400,
    width: '100%',
    ...kidModeTheme.shadows.xl,
    borderWidth: 3,
    borderColor: kidModeTheme.colors.primary,
  },
  animationSection: {
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: kidModeTheme.spacing.md,
    backgroundColor: kidModeTheme.colors.backgroundSecondary,
    borderRadius: kidModeTheme.borderRadius.lg,
    paddingVertical: kidModeTheme.spacing.lg,
  },
  textSection: {
    marginBottom: kidModeTheme.spacing.md,
  },
  title: {
    ...kidModeTheme.typography.titleLarge,
    color: kidModeTheme.colors.textPrimary,
    textAlign: 'center',
    marginBottom: kidModeTheme.spacing.sm,
    fontWeight: '700',
  },
  description: {
    ...kidModeTheme.typography.bodyLarge,
    color: kidModeTheme.colors.textSecondary,
    textAlign: 'center',
    lineHeight: 28,
  },
  closeButton: {
    backgroundColor: kidModeTheme.colors.primary,
    borderRadius: kidModeTheme.borderRadius.md,
    paddingVertical: kidModeTheme.spacing.md,
    paddingHorizontal: kidModeTheme.spacing.lg,
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: kidModeTheme.touchTargets.comfortable,
    ...kidModeTheme.shadows.md,
  },
  closeButtonText: {
    ...kidModeTheme.typography.titleLarge,
    color: kidModeTheme.colors.textInverse,
    fontWeight: '600',
  },
});
