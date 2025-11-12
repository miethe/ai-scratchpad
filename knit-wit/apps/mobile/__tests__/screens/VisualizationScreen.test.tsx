import React from 'react';
import { render, waitFor } from '@testing-library/react-native';
import { VisualizationScreen } from '../../src/screens/VisualizationScreen';
import { patternApi } from '../../src/services/api';
import type { PatternDSL } from '../../src/types/pattern';
import type { VisualizationResponse } from '../../src/types/visualization';

// Mock the API
jest.mock('../../src/services/api');

// Mock the store
jest.mock('../../src/stores/useVisualizationStore', () => ({
  useVisualizationStore: jest.fn(() => ({
    frames: [],
    currentRound: 1,
    loading: false,
    error: null,
    setFrames: jest.fn(),
    setLoading: jest.fn(),
    setError: jest.fn(),
  })),
}));

const mockPatternApi = patternApi as jest.Mocked<typeof patternApi>;

describe('VisualizationScreen', () => {
  const mockPattern: PatternDSL = {
    meta: {
      version: '0.1',
      units: 'cm',
      terms: 'US',
      stitch: 'sc',
      round_mode: 'spiral',
      gauge: { sts_per_10cm: 14, rows_per_10cm: 16 },
    },
    object: {
      type: 'sphere',
      params: { diameter: 10 },
    },
    rounds: [
      {
        r: 1,
        ops: [{ op: 'sc', count: 6 }],
        stitches: 6,
      },
    ],
    materials: {
      yarn_weight: 'Worsted',
      hook_size_mm: 4.0,
      yardage_estimate: 25,
    },
    notes: [],
  };

  const mockRoute = {
    params: { pattern: mockPattern },
  };

  const mockResponse: VisualizationResponse = {
    frames: [
      {
        round_number: 1,
        nodes: [
          { id: 'r1s0', stitch_type: 'sc', position: [100, 0], highlight: 'normal' },
          { id: 'r1s1', stitch_type: 'sc', position: [0, 100], highlight: 'normal' },
        ],
        edges: [{ source: 'r1s0', target: 'r1s1' }],
        stitch_count: 6,
        highlights: [],
      },
    ],
    total_rounds: 1,
    shape_type: 'sphere',
  };

  beforeEach(() => {
    jest.clearAllMocks();

    // Reset the store mock to default state
    const { useVisualizationStore } = require('../../src/stores/useVisualizationStore');
    useVisualizationStore.mockReturnValue({
      frames: [],
      currentRound: 1,
      loading: true,
      error: null,
      setFrames: jest.fn(),
      setLoading: jest.fn(),
      setError: jest.fn(),
    });
  });

  it('shows loading state initially', () => {
    const { getByText } = render(<VisualizationScreen route={mockRoute} />);

    expect(getByText('Generating visualization...')).toBeTruthy();
  });

  it('loads visualization on mount', async () => {
    mockPatternApi.visualize.mockResolvedValue(mockResponse);

    const mockSetFrames = jest.fn();
    const mockSetLoading = jest.fn();
    const { useVisualizationStore } = require('../../src/stores/useVisualizationStore');
    useVisualizationStore.mockReturnValue({
      frames: [],
      currentRound: 1,
      loading: false,
      error: null,
      setFrames: mockSetFrames,
      setLoading: mockSetLoading,
      setError: jest.fn(),
    });

    render(<VisualizationScreen route={mockRoute} />);

    await waitFor(() => {
      expect(mockPatternApi.visualize).toHaveBeenCalledWith(mockPattern);
    });
  });

  it('displays error message on API failure', async () => {
    mockPatternApi.visualize.mockRejectedValue(new Error('Network error'));

    const { useVisualizationStore } = require('../../src/stores/useVisualizationStore');
    useVisualizationStore.mockReturnValue({
      frames: [],
      currentRound: 1,
      loading: false,
      error: 'Network error',
      setFrames: jest.fn(),
      setLoading: jest.fn(),
      setError: jest.fn(),
    });

    const { getByText } = render(<VisualizationScreen route={mockRoute} />);

    expect(getByText('Network error')).toBeTruthy();
  });

  it('shows retry button on error', async () => {
    mockPatternApi.visualize.mockRejectedValue(new Error('Network error'));

    const { useVisualizationStore } = require('../../src/stores/useVisualizationStore');
    useVisualizationStore.mockReturnValue({
      frames: [],
      currentRound: 1,
      loading: false,
      error: 'Network error',
      setFrames: jest.fn(),
      setLoading: jest.fn(),
      setError: jest.fn(),
    });

    const { getByLabelText } = render(<VisualizationScreen route={mockRoute} />);

    const retryButton = getByLabelText('Retry connection');
    expect(retryButton).toBeTruthy();
  });

  it('displays no data message when frames are empty', () => {
    const { useVisualizationStore } = require('../../src/stores/useVisualizationStore');
    useVisualizationStore.mockReturnValue({
      frames: [],
      currentRound: 1,
      loading: false,
      error: null,
      setFrames: jest.fn(),
      setLoading: jest.fn(),
      setError: jest.fn(),
    });

    const { getByText } = render(<VisualizationScreen route={mockRoute} />);

    expect(getByText('No visualization data available')).toBeTruthy();
  });

  it('renders SVGRenderer when frames are loaded', () => {
    const { useVisualizationStore } = require('../../src/stores/useVisualizationStore');
    useVisualizationStore.mockReturnValue({
      frames: mockResponse.frames,
      currentRound: 1,
      loading: false,
      error: null,
      setFrames: jest.fn(),
      setLoading: jest.fn(),
      setError: jest.fn(),
    });

    const { getByLabelText } = render(<VisualizationScreen route={mockRoute} />);

    // SVGRenderer should render nodes with accessibility labels
    expect(getByLabelText('Stitch r1s0, type sc')).toBeTruthy();
  });

  it('handles different rounds correctly', () => {
    const multiRoundFrames = [
      {
        round_number: 1,
        nodes: [{ id: 'r1s0', stitch_type: 'sc', position: [0, 0], highlight: 'normal' }],
        edges: [],
        stitch_count: 6,
        highlights: [],
      },
      {
        round_number: 2,
        nodes: [
          { id: 'r2s0', stitch_type: 'inc', position: [0, 0], highlight: 'increase' },
        ],
        edges: [],
        stitch_count: 12,
        highlights: ['r2s0'],
      },
    ];

    const { useVisualizationStore } = require('../../src/stores/useVisualizationStore');
    useVisualizationStore.mockReturnValue({
      frames: multiRoundFrames,
      currentRound: 2,
      loading: false,
      error: null,
      setFrames: jest.fn(),
      setLoading: jest.fn(),
      setError: jest.fn(),
    });

    const { getByLabelText } = render(<VisualizationScreen route={mockRoute} />);

    // Should render round 2 nodes
    expect(getByLabelText('Stitch r2s0, type inc')).toBeTruthy();
  });

  it('calls setFrames with shape type on successful load', async () => {
    mockPatternApi.visualize.mockResolvedValue(mockResponse);

    const mockSetFrames = jest.fn();
    const { useVisualizationStore } = require('../../src/stores/useVisualizationStore');
    useVisualizationStore.mockReturnValue({
      frames: [],
      currentRound: 1,
      loading: false,
      error: null,
      setFrames: mockSetFrames,
      setLoading: jest.fn(),
      setError: jest.fn(),
    });

    render(<VisualizationScreen route={mockRoute} />);

    await waitFor(() => {
      expect(mockSetFrames).toHaveBeenCalledWith(
        mockResponse.frames,
        mockResponse.shape_type
      );
    });
  });

  it('sets error state when API call fails with non-Error object', async () => {
    mockPatternApi.visualize.mockRejectedValue('String error');

    const mockSetError = jest.fn();
    const { useVisualizationStore } = require('../../src/stores/useVisualizationStore');
    useVisualizationStore.mockReturnValue({
      frames: [],
      currentRound: 1,
      loading: false,
      error: null,
      setFrames: jest.fn(),
      setLoading: jest.fn(),
      setError: mockSetError,
    });

    render(<VisualizationScreen route={mockRoute} />);

    await waitFor(() => {
      expect(mockSetError).toHaveBeenCalledWith('Failed to load visualization');
    });
  });

  it('clears loading state after successful load', async () => {
    mockPatternApi.visualize.mockResolvedValue(mockResponse);

    const mockSetLoading = jest.fn();
    const { useVisualizationStore } = require('../../src/stores/useVisualizationStore');
    useVisualizationStore.mockReturnValue({
      frames: [],
      currentRound: 1,
      loading: false,
      error: null,
      setFrames: jest.fn(),
      setLoading: mockSetLoading,
      setError: jest.fn(),
    });

    render(<VisualizationScreen route={mockRoute} />);

    await waitFor(() => {
      expect(mockSetLoading).toHaveBeenCalledWith(false);
    });
  });

  it('clears loading state after failed load', async () => {
    mockPatternApi.visualize.mockRejectedValue(new Error('Failed'));

    const mockSetLoading = jest.fn();
    const { useVisualizationStore } = require('../../src/stores/useVisualizationStore');
    useVisualizationStore.mockReturnValue({
      frames: [],
      currentRound: 1,
      loading: false,
      error: null,
      setFrames: jest.fn(),
      setLoading: mockSetLoading,
      setError: jest.fn(),
    });

    render(<VisualizationScreen route={mockRoute} />);

    await waitFor(() => {
      expect(mockSetLoading).toHaveBeenCalledWith(false);
    });
  });
});
