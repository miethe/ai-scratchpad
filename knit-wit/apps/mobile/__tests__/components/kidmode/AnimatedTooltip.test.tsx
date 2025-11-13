/**
 * Tests for AnimatedTooltip Component
 *
 * @see Story E3: Beginner Copy and Animations
 */

import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import { AccessibilityInfo } from 'react-native';
import { AnimatedTooltip } from '../../../src/components/kidmode/AnimatedTooltip';

// Mock AccessibilityInfo
jest.mock('react-native/Libraries/Components/AccessibilityInfo/AccessibilityInfo', () => ({
  isReduceMotionEnabled: jest.fn().mockResolvedValue(false),
}));

describe('AnimatedTooltip', () => {
  const mockOnClose = jest.fn();

  beforeEach(() => {
    mockOnClose.mockClear();
  });

  describe('Rendering', () => {
    it('renders increase tooltip when visible', () => {
      const { getByText } = render(
        <AnimatedTooltip
          visible={true}
          type="increase"
          onClose={mockOnClose}
        />
      );

      expect(getByText('Add Stitches')).toBeTruthy();
      expect(
        getByText(/To make your project bigger, you add more stitches/)
      ).toBeTruthy();
    });

    it('renders decrease tooltip when visible', () => {
      const { getByText } = render(
        <AnimatedTooltip
          visible={true}
          type="decrease"
          onClose={mockOnClose}
        />
      );

      expect(getByText('Remove Stitches')).toBeTruthy();
      expect(
        getByText(/To make your project smaller, you take away stitches/)
      ).toBeTruthy();
    });

    it('renders magic ring tooltip when visible', () => {
      const { getByText } = render(
        <AnimatedTooltip
          visible={true}
          type="magicRing"
          onClose={mockOnClose}
        />
      );

      expect(getByText('Start Loop')).toBeTruthy();
      expect(
        getByText(/The magic ring is a special way to start/)
      ).toBeTruthy();
    });

    it('does not render when not visible', () => {
      const { queryByText } = render(
        <AnimatedTooltip
          visible={false}
          type="increase"
          onClose={mockOnClose}
        />
      );

      expect(queryByText('Add Stitches')).toBeNull();
    });
  });

  describe('Interaction', () => {
    it('calls onClose when close button is pressed', () => {
      const { getByText } = render(
        <AnimatedTooltip
          visible={true}
          type="increase"
          onClose={mockOnClose}
        />
      );

      const closeButton = getByText('Got It!');
      fireEvent.press(closeButton);

      expect(mockOnClose).toHaveBeenCalledTimes(1);
    });

    it('calls onClose when backdrop is pressed', () => {
      const { getByTestId, UNSAFE_getByType } = render(
        <AnimatedTooltip
          visible={true}
          type="increase"
          onClose={mockOnClose}
        />
      );

      // Find the outer TouchableWithoutFeedback (backdrop)
      const modal = UNSAFE_getByType(require('react-native').Modal);
      const backdrop = modal.props.children;

      fireEvent.press(backdrop);

      expect(mockOnClose).toHaveBeenCalledTimes(1);
    });
  });

  describe('Custom Content', () => {
    it('renders custom title when provided', () => {
      const { getByText, queryByText } = render(
        <AnimatedTooltip
          visible={true}
          type="increase"
          title="Custom Title"
          onClose={mockOnClose}
        />
      );

      expect(getByText('Custom Title')).toBeTruthy();
      expect(queryByText('Add Stitches')).toBeNull();
    });

    it('renders custom description when provided', () => {
      const { getByText } = render(
        <AnimatedTooltip
          visible={true}
          type="increase"
          description="Custom description text"
          onClose={mockOnClose}
        />
      );

      expect(getByText('Custom description text')).toBeTruthy();
    });
  });

  describe('Accessibility', () => {
    it('checks reduce motion preference on mount', async () => {
      render(
        <AnimatedTooltip
          visible={true}
          type="increase"
          onClose={mockOnClose}
        />
      );

      await waitFor(() => {
        expect(AccessibilityInfo.isReduceMotionEnabled).toHaveBeenCalled();
      });
    });

    it('has proper accessibility labels for increase tooltip', () => {
      const { getByLabelText } = render(
        <AnimatedTooltip
          visible={true}
          type="increase"
          onClose={mockOnClose}
        />
      );

      expect(
        getByLabelText(/Add stitches tooltip/)
      ).toBeTruthy();
    });

    it('has proper accessibility labels for decrease tooltip', () => {
      const { getByLabelText } = render(
        <AnimatedTooltip
          visible={true}
          type="decrease"
          onClose={mockOnClose}
        />
      );

      expect(
        getByLabelText(/Remove stitches tooltip/)
      ).toBeTruthy();
    });

    it('has proper accessibility labels for magic ring tooltip', () => {
      const { getByLabelText } = render(
        <AnimatedTooltip
          visible={true}
          type="magicRing"
          onClose={mockOnClose}
        />
      );

      expect(
        getByLabelText(/Start loop tooltip/)
      ).toBeTruthy();
    });

    it('close button has proper accessibility hint', () => {
      const { getByLabelText } = render(
        <AnimatedTooltip
          visible={true}
          type="increase"
          onClose={mockOnClose}
        />
      );

      const closeButton = getByLabelText('Close tooltip');
      expect(closeButton).toBeTruthy();
    });
  });

  describe('Content Readability', () => {
    it('increase description uses simple language', () => {
      const { getByText } = render(
        <AnimatedTooltip
          visible={true}
          type="increase"
          onClose={mockOnClose}
        />
      );

      const description = getByText(/To make your project bigger/);
      expect(description).toBeTruthy();

      // Check for Grade 4-5 appropriate words (no complex terms)
      const text = description.props.children;
      expect(text).not.toMatch(/parametric|generate|increment/i);
      expect(text).toMatch(/bigger|add|stitches/i);
    });

    it('decrease description uses simple language', () => {
      const { getByText } = render(
        <AnimatedTooltip
          visible={true}
          type="decrease"
          onClose={mockOnClose}
        />
      );

      const description = getByText(/To make your project smaller/);
      expect(description).toBeTruthy();

      const text = description.props.children;
      expect(text).not.toMatch(/parametric|generate|decrement/i);
      expect(text).toMatch(/smaller|take away|stitches/i);
    });

    it('magic ring description uses simple language', () => {
      const { getByText } = render(
        <AnimatedTooltip
          visible={true}
          type="magicRing"
          onClose={mockOnClose}
        />
      );

      const description = getByText(/The magic ring is a special way to start/);
      expect(description).toBeTruthy();

      const text = description.props.children;
      expect(text).not.toMatch(/initialize|commence|construct/i);
      expect(text).toMatch(/start|loop|pull|tight/i);
    });
  });
});
