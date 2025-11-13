import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import ParseScreen from '../../src/screens/ParseScreen';
import { patternApi } from '../../src/services/api';
import type { RootStackScreenProps } from '../../src/types';
import type { PatternDSL } from '../../src/types';

// Mock the API service
jest.mock('../../src/services/api', () => ({
  patternApi: {
    parse: jest.fn(),
  },
}));

// Mock navigation
const mockNavigate = jest.fn();
const mockNavigation = {
  navigate: mockNavigate,
  goBack: jest.fn(),
  addListener: jest.fn(),
  removeListener: jest.fn(),
  canGoBack: jest.fn(() => false),
  dispatch: jest.fn(),
  getId: jest.fn(),
  isFocused: jest.fn(() => true),
  reset: jest.fn(),
  setOptions: jest.fn(),
  setParams: jest.fn(),
  getState: jest.fn(),
  getParent: jest.fn(),
} as any;

const mockRoute = {
  key: 'Parse-test',
  name: 'Parse' as const,
  params: undefined,
  path: undefined,
};

const mockDSL: PatternDSL = {
  meta: {
    version: '0.1',
    units: 'cm',
    terms: 'US',
    stitch: 'sc',
    round_mode: 'spiral',
    gauge: {
      sts_per_10cm: 14,
      rows_per_10cm: 16,
    },
  },
  object: {
    type: 'sphere',
    params: { diameter: 10 },
  },
  rounds: [
    {
      r: 1,
      ops: [
        { op: 'MR', count: 1 },
        { op: 'sc', count: 6 },
      ],
      stitches: 6,
    },
    {
      r: 2,
      ops: [{ op: 'inc', count: 6 }],
      stitches: 12,
    },
    {
      r: 3,
      ops: [{ op: 'sc', count: 1 }, { op: 'inc', count: 1 }],
      stitches: 18,
    },
  ],
  materials: {
    yarn_weight: 'Worsted',
    hook_size_mm: 4.0,
    yardage_estimate: 25,
  },
  notes: ['Work in a spiral; use a stitch marker.'],
};

describe('ParseScreen', () => {
  beforeEach(() => {
    mockNavigate.mockClear();
    (patternApi.parse as jest.Mock).mockClear();
  });

  it('renders the screen with title and input', () => {
    const { getByText, getByLabelText } = render(
      <ParseScreen navigation={mockNavigation} route={mockRoute} />
    );

    expect(getByText('Parse Pattern')).toBeTruthy();
    expect(getByText('Paste your crochet pattern below to validate and visualize it.')).toBeTruthy();
    expect(getByLabelText('Pattern text input')).toBeTruthy();
  });

  it('renders validate button', () => {
    const { getByLabelText } = render(
      <ParseScreen navigation={mockNavigation} route={mockRoute} />
    );

    expect(getByLabelText('Validate pattern')).toBeTruthy();
  });

  it('allows text input', () => {
    const { getByLabelText } = render(
      <ParseScreen navigation={mockNavigation} route={mockRoute} />
    );

    const input = getByLabelText('Pattern text input');
    fireEvent.changeText(input, 'R1: MR 6 sc (6)');

    expect(input.props.value).toBe('R1: MR 6 sc (6)');
  });

  it('shows error when validating empty pattern', async () => {
    const { getByLabelText, getByText } = render(
      <ParseScreen navigation={mockNavigation} route={mockRoute} />
    );

    const validateButton = getByLabelText('Validate pattern');
    fireEvent.press(validateButton);

    await waitFor(() => {
      expect(getByText('Please enter a pattern to validate')).toBeTruthy();
    });
  });

  it('calls API and shows success state on valid pattern', async () => {
    (patternApi.parse as jest.Mock).mockResolvedValue({
      dsl: mockDSL,
      validation: {
        valid: true,
        errors: [],
      },
    });

    const { getByLabelText, getByText } = render(
      <ParseScreen navigation={mockNavigation} route={mockRoute} />
    );

    const input = getByLabelText('Pattern text input');
    fireEvent.changeText(input, 'R1: MR 6 sc (6)\nR2: inc x6 (12)');

    const validateButton = getByLabelText('Validate pattern');
    fireEvent.press(validateButton);

    await waitFor(() => {
      expect(patternApi.parse).toHaveBeenCalledWith('R1: MR 6 sc (6)\nR2: inc x6 (12)');
    });

    await waitFor(() => {
      expect(getByText('Pattern is valid!')).toBeTruthy();
    });
  });

  it('shows preview of first 3 rounds on success', async () => {
    (patternApi.parse as jest.Mock).mockResolvedValue({
      dsl: mockDSL,
      validation: {
        valid: true,
        errors: [],
      },
    });

    const { getByLabelText, getByText } = render(
      <ParseScreen navigation={mockNavigation} route={mockRoute} />
    );

    const input = getByLabelText('Pattern text input');
    fireEvent.changeText(input, 'R1: MR 6 sc (6)');

    const validateButton = getByLabelText('Validate pattern');
    fireEvent.press(validateButton);

    await waitFor(() => {
      expect(getByText('Pattern Preview:')).toBeTruthy();
      expect(getByText('Round 1: 6 stitches')).toBeTruthy();
      expect(getByText('Round 2: 12 stitches')).toBeTruthy();
      expect(getByText('Round 3: 18 stitches')).toBeTruthy();
    });
  });

  it('shows visualize button after successful validation', async () => {
    (patternApi.parse as jest.Mock).mockResolvedValue({
      dsl: mockDSL,
      validation: {
        valid: true,
        errors: [],
      },
    });

    const { getByLabelText } = render(
      <ParseScreen navigation={mockNavigation} route={mockRoute} />
    );

    const input = getByLabelText('Pattern text input');
    fireEvent.changeText(input, 'R1: MR 6 sc (6)');

    const validateButton = getByLabelText('Validate pattern');
    fireEvent.press(validateButton);

    await waitFor(() => {
      expect(getByLabelText('Visualize pattern')).toBeTruthy();
    });
  });

  it('navigates to Visualization screen when visualize button pressed', async () => {
    (patternApi.parse as jest.Mock).mockResolvedValue({
      dsl: mockDSL,
      validation: {
        valid: true,
        errors: [],
      },
    });

    const { getByLabelText } = render(
      <ParseScreen navigation={mockNavigation} route={mockRoute} />
    );

    const input = getByLabelText('Pattern text input');
    fireEvent.changeText(input, 'R1: MR 6 sc (6)');

    const validateButton = getByLabelText('Validate pattern');
    fireEvent.press(validateButton);

    await waitFor(() => {
      expect(getByLabelText('Visualize pattern')).toBeTruthy();
    });

    const visualizeButton = getByLabelText('Visualize pattern');
    fireEvent.press(visualizeButton);

    expect(mockNavigate).toHaveBeenCalledWith('Visualization', { pattern: mockDSL });
  });

  it('shows error state with validation errors', async () => {
    (patternApi.parse as jest.Mock).mockResolvedValue({
      dsl: null,
      validation: {
        valid: false,
        errors: [
          { message: 'Invalid stitch count', line: 1 },
          { message: 'Missing round number', line: 2 },
        ],
      },
    });

    const { getByLabelText, getByText } = render(
      <ParseScreen navigation={mockNavigation} route={mockRoute} />
    );

    const input = getByLabelText('Pattern text input');
    fireEvent.changeText(input, 'Invalid pattern');

    const validateButton = getByLabelText('Validate pattern');
    fireEvent.press(validateButton);

    await waitFor(() => {
      expect(getByText('Validation Errors')).toBeTruthy();
      expect(getByText('Line 1: Invalid stitch count')).toBeTruthy();
      expect(getByText('Line 2: Missing round number')).toBeTruthy();
    });
  });

  it('handles network errors gracefully', async () => {
    (patternApi.parse as jest.Mock).mockRejectedValue(new Error('Network error'));

    const { getByLabelText, getByText } = render(
      <ParseScreen navigation={mockNavigation} route={mockRoute} />
    );

    const input = getByLabelText('Pattern text input');
    fireEvent.changeText(input, 'R1: MR 6 sc (6)');

    const validateButton = getByLabelText('Validate pattern');
    fireEvent.press(validateButton);

    await waitFor(() => {
      expect(getByText('Validation Errors')).toBeTruthy();
    });

    // Check that error message is displayed (checking for the actual error message shown)
    await waitFor(() => {
      expect(getByText('Network error')).toBeTruthy();
    });
  });

  it('shows loading state during validation', async () => {
    (patternApi.parse as jest.Mock).mockImplementation(
      () => new Promise((resolve) => setTimeout(() => resolve({ dsl: mockDSL, validation: { valid: true, errors: [] } }), 100))
    );

    const { getByLabelText } = render(
      <ParseScreen navigation={mockNavigation} route={mockRoute} />
    );

    const input = getByLabelText('Pattern text input');
    fireEvent.changeText(input, 'R1: MR 6 sc (6)');

    const validateButton = getByLabelText('Validate pattern');
    fireEvent.press(validateButton);

    // The button should be disabled during loading
    // We can verify by checking the disabled prop directly
    expect(validateButton.props.disabled).toBeTruthy();
  });

  it('has proper accessibility labels', () => {
    const { getByLabelText } = render(
      <ParseScreen navigation={mockNavigation} route={mockRoute} />
    );

    expect(getByLabelText('Parse pattern screen')).toBeTruthy();
    expect(getByLabelText('Pattern text input')).toBeTruthy();
    expect(getByLabelText('Validate pattern')).toBeTruthy();
  });
});
