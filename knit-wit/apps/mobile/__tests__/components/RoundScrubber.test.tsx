import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import { RoundScrubber } from '../../src/components/visualization/RoundScrubber';
import { useVisualizationStore } from '../../src/stores/useVisualizationStore';

jest.mock('../../src/stores/useVisualizationStore');

describe('RoundScrubber', () => {
  const mockPrevRound = jest.fn();
  const mockNextRound = jest.fn();
  const mockJumpToRound = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
    (useVisualizationStore as unknown as jest.Mock).mockReturnValue({
      currentRound: 2,
      totalRounds: 5,
      prevRound: mockPrevRound,
      nextRound: mockNextRound,
      jumpToRound: mockJumpToRound,
    });
  });

  it('renders correctly', () => {
    const { getByText } = render(<RoundScrubber />);
    expect(getByText('Round 2 of 5')).toBeTruthy();
  });

  it('calls prevRound when previous button pressed', () => {
    const { getByLabelText } = render(<RoundScrubber />);
    fireEvent.press(getByLabelText('Previous round'));
    expect(mockPrevRound).toHaveBeenCalled();
  });

  it('calls nextRound when next button pressed', () => {
    const { getByLabelText } = render(<RoundScrubber />);
    fireEvent.press(getByLabelText('Next round'));
    expect(mockNextRound).toHaveBeenCalled();
  });

  it('disables previous button at round 1', () => {
    (useVisualizationStore as unknown as jest.Mock).mockReturnValue({
      currentRound: 1,
      totalRounds: 5,
      prevRound: mockPrevRound,
      nextRound: mockNextRound,
      jumpToRound: mockJumpToRound,
    });

    const { getByLabelText } = render(<RoundScrubber />);
    const prevButton = getByLabelText('Previous round');
    expect(prevButton.props.accessibilityState.disabled).toBe(true);
  });

  it('disables next button at last round', () => {
    (useVisualizationStore as unknown as jest.Mock).mockReturnValue({
      currentRound: 5,
      totalRounds: 5,
      prevRound: mockPrevRound,
      nextRound: mockNextRound,
      jumpToRound: mockJumpToRound,
    });

    const { getByLabelText } = render(<RoundScrubber />);
    const nextButton = getByLabelText('Next round');
    expect(nextButton.props.accessibilityState.disabled).toBe(true);
  });

  it('returns null when totalRounds is 0', () => {
    (useVisualizationStore as unknown as jest.Mock).mockReturnValue({
      currentRound: 0,
      totalRounds: 0,
      prevRound: mockPrevRound,
      nextRound: mockNextRound,
      jumpToRound: mockJumpToRound,
    });

    const { queryByText, queryByLabelText } = render(<RoundScrubber />);
    expect(queryByText(/Round \d+ of \d+/)).toBeNull();
    expect(queryByLabelText('Previous round')).toBeNull();
    expect(queryByLabelText('Next round')).toBeNull();
  });
});
