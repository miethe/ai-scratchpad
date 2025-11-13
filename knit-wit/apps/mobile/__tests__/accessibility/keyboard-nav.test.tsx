/**
 * Keyboard Navigation Tests
 *
 * Tests keyboard navigation support across all screens and components
 * Validates tab order, focus indicators, keyboard shortcuts, and modal focus traps
 *
 * @see Story E5: Keyboard Navigation
 */

import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import { Platform } from 'react-native';
import HomeScreen from '../../src/screens/HomeScreen';
import GenerateScreen from '../../src/screens/GenerateScreen';
import { ExportScreen } from '../../src/screens/ExportScreen';
import SettingsScreen from '../../src/screens/SettingsScreen';
import { RoundScrubber } from '../../src/components/visualization/RoundScrubber';
import { AnimatedTooltip } from '../../src/components/kidmode/AnimatedTooltip';
import { useVisualizationStore } from '../../src/stores/useVisualizationStore';
import { useSettingsStore } from '../../src/stores/useSettingsStore';
import type { VisualizationFrame } from '../../src/types/visualization';

// Mock services and stores
jest.mock('../../src/services/api');
jest.mock('../../src/services/exportService');
jest.mock('../../src/stores/useVisualizationStore');
jest.mock('../../src/stores/useSettingsStore');

// Mock navigation
const mockNavigation = {
  navigate: jest.fn(),
  goBack: jest.fn(),
  dispatch: jest.fn(),
  setParams: jest.fn(),
  addListener: jest.fn(() => jest.fn()),
  removeListener: jest.fn(),
  canGoBack: jest.fn(() => false),
  isFocused: jest.fn(() => true),
  push: jest.fn(),
  replace: jest.fn(),
  pop: jest.fn(),
  popToTop: jest.fn(),
  setOptions: jest.fn(),
  reset: jest.fn(),
  getParent: jest.fn(),
  getState: jest.fn(),
  getId: jest.fn(),
};

const mockRoute = {
  key: 'test-key',
  name: 'Home' as const,
  params: undefined,
};

describe('Keyboard Navigation', () => {
  beforeEach(() => {
    jest.clearAllMocks();

    // Mock store defaults
    (useVisualizationStore as unknown as jest.Mock).mockReturnValue({
      frames: [],
      currentRound: 1,
      totalRounds: 0,
      prevRound: jest.fn(),
      nextRound: jest.fn(),
      jumpToRound: jest.fn(),
      loading: false,
      error: null,
      setFrames: jest.fn(),
      setLoading: jest.fn(),
      setError: jest.fn(),
    });

    (useSettingsStore as unknown as jest.Mock).mockReturnValue({
      kidMode: false,
      darkMode: false,
      defaultUnits: 'cm',
      defaultTerminology: 'US',
      setKidMode: jest.fn(),
      setDarkMode: jest.fn(),
      setDefaultUnits: jest.fn(),
      setDefaultTerminology: jest.fn(),
    });
  });

  describe('Focus Indicators', () => {
    it('shows focus indicator on HomeScreen cards when focused', () => {
      const { getByLabelText } = render(
        <HomeScreen navigation={mockNavigation} route={mockRoute} />
      );

      const makePatternCard = getByLabelText('Start generating a pattern');

      // Simulate focus event
      fireEvent(makePatternCard, 'focus');

      // Focus indicator should be applied (2px border with high contrast)
      expect(makePatternCard.props.style).toContainEqual(
        expect.objectContaining({
          borderWidth: 2,
          borderColor: expect.any(String),
        })
      );
    });

    it('removes focus indicator on blur', () => {
      const { getByLabelText } = render(
        <HomeScreen navigation={mockNavigation} route={mockRoute} />
      );

      const makePatternCard = getByLabelText('Start generating a pattern');

      // Focus then blur
      fireEvent(makePatternCard, 'focus');
      fireEvent(makePatternCard, 'blur');

      // Focus indicator should not be in final style
      const styles = Array.isArray(makePatternCard.props.style)
        ? makePatternCard.props.style
        : [makePatternCard.props.style];

      const hasFocusBorder = styles.some(
        (style: any) => style?.borderWidth === 2
      );

      expect(hasFocusBorder).toBeFalsy();
    });

    it('shows focus indicator on RoundScrubber navigation buttons', () => {
      const mockFrames: VisualizationFrame[] = [
        {
          round_number: 1,
          nodes: [],
          edges: [],
          stitch_count: 6,
          highlights: [],
        },
        {
          round_number: 2,
          nodes: [],
          edges: [],
          stitch_count: 12,
          highlights: [],
        },
      ];

      (useVisualizationStore as unknown as jest.Mock).mockReturnValue({
        frames: mockFrames,
        currentRound: 1,
        totalRounds: 2,
        prevRound: jest.fn(),
        nextRound: jest.fn(),
        jumpToRound: jest.fn(),
      });

      const { getByLabelText } = render(<RoundScrubber />);

      const nextButton = getByLabelText('Next round');
      fireEvent(nextButton, 'focus');

      expect(nextButton.props.style).toContainEqual(
        expect.objectContaining({
          borderWidth: 2,
        })
      );
    });

    it('shows focus indicator on export button', () => {
      const mockPattern = {
        meta: { version: '0.1', units: 'cm', terms: 'US', stitch: 'sc', round_mode: 'spiral' },
        object: { type: 'sphere', params: { diameter: 10 } },
        rounds: [],
        materials: { yarn_weight: 'Worsted', hook_size_mm: 4.0 },
      };

      const exportRoute = {
        key: 'test-key',
        name: 'Export' as const,
        params: { pattern: mockPattern },
      };

      const { getByLabelText } = render(
        <ExportScreen navigation={mockNavigation} route={exportRoute} />
      );

      const exportButton = getByLabelText(/Export pattern/);
      fireEvent(exportButton, 'focus');

      expect(exportButton.props.style).toContainEqual(
        expect.objectContaining({
          borderWidth: 2,
        })
      );
    });
  });

  describe('RoundScrubber Keyboard Shortcuts', () => {
    beforeEach(() => {
      // Mock platform to be web for keyboard event tests
      Platform.OS = 'web' as any;
    });

    it('navigates to previous round with Arrow Left key', () => {
      const mockPrevRound = jest.fn();
      const mockFrames: VisualizationFrame[] = [
        { round_number: 1, nodes: [], edges: [], stitch_count: 6, highlights: [] },
        { round_number: 2, nodes: [], edges: [], stitch_count: 12, highlights: [] },
      ];

      (useVisualizationStore as unknown as jest.Mock).mockReturnValue({
        frames: mockFrames,
        currentRound: 2,
        totalRounds: 2,
        prevRound: mockPrevRound,
        nextRound: jest.fn(),
        jumpToRound: jest.fn(),
      });

      render(<RoundScrubber />);

      // Simulate ArrowLeft key press
      const event = new KeyboardEvent('keydown', { key: 'ArrowLeft' });
      window.dispatchEvent(event);

      expect(mockPrevRound).toHaveBeenCalled();
    });

    it('navigates to next round with Arrow Right key', () => {
      const mockNextRound = jest.fn();
      const mockFrames: VisualizationFrame[] = [
        { round_number: 1, nodes: [], edges: [], stitch_count: 6, highlights: [] },
        { round_number: 2, nodes: [], edges: [], stitch_count: 12, highlights: [] },
      ];

      (useVisualizationStore as unknown as jest.Mock).mockReturnValue({
        frames: mockFrames,
        currentRound: 1,
        totalRounds: 2,
        prevRound: jest.fn(),
        nextRound: mockNextRound,
        jumpToRound: jest.fn(),
      });

      render(<RoundScrubber />);

      // Simulate ArrowRight key press
      const event = new KeyboardEvent('keydown', { key: 'ArrowRight' });
      window.dispatchEvent(event);

      expect(mockNextRound).toHaveBeenCalled();
    });

    it('jumps to first round with Home key', () => {
      const mockJumpToRound = jest.fn();
      const mockFrames: VisualizationFrame[] = [
        { round_number: 1, nodes: [], edges: [], stitch_count: 6, highlights: [] },
        { round_number: 2, nodes: [], edges: [], stitch_count: 12, highlights: [] },
        { round_number: 3, nodes: [], edges: [], stitch_count: 18, highlights: [] },
      ];

      (useVisualizationStore as unknown as jest.Mock).mockReturnValue({
        frames: mockFrames,
        currentRound: 3,
        totalRounds: 3,
        prevRound: jest.fn(),
        nextRound: jest.fn(),
        jumpToRound: mockJumpToRound,
      });

      render(<RoundScrubber />);

      // Simulate Home key press
      const event = new KeyboardEvent('keydown', { key: 'Home' });
      window.dispatchEvent(event);

      expect(mockJumpToRound).toHaveBeenCalledWith(1);
    });

    it('jumps to last round with End key', () => {
      const mockJumpToRound = jest.fn();
      const mockFrames: VisualizationFrame[] = [
        { round_number: 1, nodes: [], edges: [], stitch_count: 6, highlights: [] },
        { round_number: 2, nodes: [], edges: [], stitch_count: 12, highlights: [] },
        { round_number: 3, nodes: [], edges: [], stitch_count: 18, highlights: [] },
      ];

      (useVisualizationStore as unknown as jest.Mock).mockReturnValue({
        frames: mockFrames,
        currentRound: 1,
        totalRounds: 3,
        prevRound: jest.fn(),
        nextRound: jest.fn(),
        jumpToRound: mockJumpToRound,
      });

      render(<RoundScrubber />);

      // Simulate End key press
      const event = new KeyboardEvent('keydown', { key: 'End' });
      window.dispatchEvent(event);

      expect(mockJumpToRound).toHaveBeenCalledWith(3);
    });

    it('does not navigate when at boundaries', () => {
      const mockPrevRound = jest.fn();
      const mockNextRound = jest.fn();
      const mockFrames: VisualizationFrame[] = [
        { round_number: 1, nodes: [], edges: [], stitch_count: 6, highlights: [] },
      ];

      (useVisualizationStore as unknown as jest.Mock).mockReturnValue({
        frames: mockFrames,
        currentRound: 1,
        totalRounds: 1,
        prevRound: mockPrevRound,
        nextRound: mockNextRound,
        jumpToRound: jest.fn(),
      });

      render(<RoundScrubber />);

      // Try to go previous when at first round
      const leftEvent = new KeyboardEvent('keydown', { key: 'ArrowLeft' });
      window.dispatchEvent(leftEvent);
      expect(mockPrevRound).not.toHaveBeenCalled();

      // Try to go next when at last round
      const rightEvent = new KeyboardEvent('keydown', { key: 'ArrowRight' });
      window.dispatchEvent(rightEvent);
      expect(mockNextRound).not.toHaveBeenCalled();
    });
  });

  describe('Modal Focus Trap and Escape Key', () => {
    beforeEach(() => {
      Platform.OS = 'web' as any;
    });

    it('closes AnimatedTooltip with Escape key', () => {
      const mockOnClose = jest.fn();

      render(
        <AnimatedTooltip
          visible={true}
          type="increase"
          onClose={mockOnClose}
        />
      );

      // Simulate Escape key press
      const event = new KeyboardEvent('keydown', { key: 'Escape' });
      window.dispatchEvent(event);

      expect(mockOnClose).toHaveBeenCalled();
    });

    it('does not close tooltip on other keys', () => {
      const mockOnClose = jest.fn();

      render(
        <AnimatedTooltip
          visible={true}
          type="increase"
          onClose={mockOnClose}
        />
      );

      // Simulate non-Escape key press
      const event = new KeyboardEvent('keydown', { key: 'Enter' });
      window.dispatchEvent(event);

      expect(mockOnClose).not.toHaveBeenCalled();
    });

    it('tooltip close button has focus indicator', () => {
      const mockOnClose = jest.fn();

      const { getByLabelText } = render(
        <AnimatedTooltip
          visible={true}
          type="increase"
          onClose={mockOnClose}
        />
      );

      const closeButton = getByLabelText('Close tooltip');
      fireEvent(closeButton, 'focus');

      expect(closeButton.props.style).toContainEqual(
        expect.objectContaining({
          borderWidth: 2,
        })
      );
    });
  });

  describe('Tab Order', () => {
    it('HomeScreen has logical tab order', () => {
      const { getAllByRole } = render(
        <HomeScreen navigation={mockNavigation} route={mockRoute} />
      );

      const buttons = getAllByRole('button');

      // Should have "Make Pattern" and "Check Pattern" buttons
      expect(buttons.length).toBeGreaterThanOrEqual(2);

      // First interactive element should be "Make Pattern"
      expect(buttons[0].props.accessibilityLabel).toContain('generating');
    });

    it('GenerateScreen has logical tab order', () => {
      const { getAllByRole } = render(
        <GenerateScreen navigation={mockNavigation} route={mockRoute} />
      );

      const radios = getAllByRole('radio');
      const buttons = getAllByRole('button');

      // Should have shape selection radios
      expect(radios.length).toBeGreaterThan(0);

      // Generate button should be last
      const generateButton = buttons.find(b =>
        b.props.accessibilityLabel?.includes('Generate')
      );
      expect(generateButton).toBeTruthy();
    });
  });

  describe('Accessibility Hints for Keyboard Navigation', () => {
    it('RoundScrubber buttons mention arrow key shortcuts in hints', () => {
      const mockFrames: VisualizationFrame[] = [
        { round_number: 1, nodes: [], edges: [], stitch_count: 6, highlights: [] },
        { round_number: 2, nodes: [], edges: [], stitch_count: 12, highlights: [] },
      ];

      (useVisualizationStore as unknown as jest.Mock).mockReturnValue({
        frames: mockFrames,
        currentRound: 1,
        totalRounds: 2,
        prevRound: jest.fn(),
        nextRound: jest.fn(),
        jumpToRound: jest.fn(),
      });

      const { getByLabelText } = render(<RoundScrubber />);

      const nextButton = getByLabelText('Next round');
      expect(nextButton.props.accessibilityHint).toContain('arrow key');
    });

    it('Tooltip mentions Escape key in hint', () => {
      const { getByLabelText } = render(
        <AnimatedTooltip
          visible={true}
          type="increase"
          onClose={jest.fn()}
        />
      );

      const closeButton = getByLabelText('Close tooltip');
      expect(closeButton.props.accessibilityHint).toContain('Escape');
    });
  });

  describe('Focus Indicator Contrast', () => {
    it('focus indicator has sufficient contrast (3:1 ratio)', () => {
      const { getByLabelText } = render(
        <HomeScreen navigation={mockNavigation} route={mockRoute} />
      );

      const card = getByLabelText('Start generating a pattern');
      fireEvent(card, 'focus');

      // Focus indicator uses colors.info (#3B82F6)
      // Against white background, this provides > 3:1 contrast
      const style = Array.isArray(card.props.style)
        ? card.props.style.find((s: any) => s?.borderColor)
        : card.props.style;

      expect(style?.borderColor).toBe('#3B82F6'); // colors.info
      expect(style?.borderWidth).toBe(2);
    });
  });

  describe('No Focus Traps on Main Screens', () => {
    it('can navigate out of HomeScreen elements with Tab', () => {
      const { getAllByRole } = render(
        <HomeScreen navigation={mockNavigation} route={mockRoute} />
      );

      const buttons = getAllByRole('button');

      // All buttons should be accessible and focusable
      buttons.forEach(button => {
        expect(button.props.accessible).not.toBe(false);
      });
    });

    it('can navigate out of GenerateScreen elements with Tab', () => {
      const { getAllByRole } = render(
        <GenerateScreen navigation={mockNavigation} route={mockRoute} />
      );

      const interactiveElements = [
        ...getAllByRole('radio'),
        ...getAllByRole('button'),
      ];

      // All interactive elements should be accessible
      interactiveElements.forEach(element => {
        expect(element.props.accessible).not.toBe(false);
      });
    });
  });

  describe('Platform-Specific Behavior', () => {
    it('keyboard shortcuts only work on web platform', () => {
      Platform.OS = 'android' as any;

      const mockNextRound = jest.fn();
      const mockFrames: VisualizationFrame[] = [
        { round_number: 1, nodes: [], edges: [], stitch_count: 6, highlights: [] },
        { round_number: 2, nodes: [], edges: [], stitch_count: 12, highlights: [] },
      ];

      (useVisualizationStore as unknown as jest.Mock).mockReturnValue({
        frames: mockFrames,
        currentRound: 1,
        totalRounds: 2,
        prevRound: jest.fn(),
        nextRound: mockNextRound,
        jumpToRound: jest.fn(),
      });

      render(<RoundScrubber />);

      // Keyboard events should not trigger navigation on non-web platforms
      const event = new KeyboardEvent('keydown', { key: 'ArrowRight' });
      window.dispatchEvent(event);

      expect(mockNextRound).not.toHaveBeenCalled();
    });
  });
});
