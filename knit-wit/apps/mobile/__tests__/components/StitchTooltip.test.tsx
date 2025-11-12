import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import { StitchTooltip } from '../../src/components/visualization/StitchTooltip';
import type { RenderNode } from '../../src/types/visualization';

describe('StitchTooltip', () => {
  const mockNode: RenderNode = {
    id: 'r2s5',
    stitch_type: 'inc',
    position: [50.5, -30.2],
    highlight: 'increase',
  };

  const mockOnClose = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders when visible with valid node', () => {
    const { getByText } = render(
      <StitchTooltip visible={true} node={mockNode} onClose={mockOnClose} />
    );

    expect(getByText('INC')).toBeTruthy();
    expect(getByText('Increase (2 sc in same stitch)')).toBeTruthy();
    expect(getByText('r2s5')).toBeTruthy();
  });

  it('does not render when not visible', () => {
    const { queryByText } = render(
      <StitchTooltip visible={false} node={mockNode} onClose={mockOnClose} />
    );

    expect(queryByText('INC')).toBeNull();
  });

  it('does not render when node is null', () => {
    const { queryByText } = render(
      <StitchTooltip visible={true} node={null} onClose={mockOnClose} />
    );

    expect(queryByText('INC')).toBeNull();
  });

  it('calls onClose when overlay pressed', () => {
    const { getByLabelText } = render(
      <StitchTooltip visible={true} node={mockNode} onClose={mockOnClose} />
    );

    fireEvent.press(getByLabelText('Close tooltip'));
    expect(mockOnClose).toHaveBeenCalled();
  });

  it('displays increase badge for increase highlight', () => {
    const { getByText } = render(
      <StitchTooltip visible={true} node={mockNode} onClose={mockOnClose} />
    );

    expect(getByText('Increase')).toBeTruthy();
  });

  it('displays decrease badge for decrease highlight', () => {
    const decreaseNode: RenderNode = {
      ...mockNode,
      stitch_type: 'dec',
      highlight: 'decrease',
    };

    const { getByText } = render(
      <StitchTooltip visible={true} node={decreaseNode} onClose={mockOnClose} />
    );

    expect(getByText('Decrease')).toBeTruthy();
  });

  it('displays position coordinates', () => {
    const { getByText } = render(
      <StitchTooltip visible={true} node={mockNode} onClose={mockOnClose} />
    );

    expect(getByText('(50.5, -30.2)')).toBeTruthy();
  });

  it('displays correct stitch type for sc', () => {
    const scNode: RenderNode = {
      ...mockNode,
      stitch_type: 'sc',
      highlight: 'normal',
    };

    const { getByText } = render(
      <StitchTooltip visible={true} node={scNode} onClose={mockOnClose} />
    );

    expect(getByText('SC')).toBeTruthy();
    expect(getByText('Single Crochet')).toBeTruthy();
  });

  it('displays correct stitch type for dec', () => {
    const decNode: RenderNode = {
      ...mockNode,
      stitch_type: 'dec',
      highlight: 'normal',
    };

    const { getByText } = render(
      <StitchTooltip visible={true} node={decNode} onClose={mockOnClose} />
    );

    expect(getByText('DEC')).toBeTruthy();
    expect(getByText('Decrease (sc2tog)')).toBeTruthy();
  });

  it('displays uppercase stitch type for unknown types', () => {
    const unknownNode: RenderNode = {
      ...mockNode,
      stitch_type: 'xyz',
      highlight: 'normal',
    };

    const { getAllByText } = render(
      <StitchTooltip visible={true} node={unknownNode} onClose={mockOnClose} />
    );

    // Both stitch type header and name will show XYZ for unknown types
    const xyzElements = getAllByText('XYZ');
    expect(xyzElements.length).toBeGreaterThanOrEqual(1);
  });

  it('does not display badge for normal highlight', () => {
    const normalNode: RenderNode = {
      ...mockNode,
      highlight: 'normal',
    };

    const { queryByText } = render(
      <StitchTooltip visible={true} node={normalNode} onClose={mockOnClose} />
    );

    expect(queryByText('Increase')).toBeNull();
    expect(queryByText('Decrease')).toBeNull();
  });

  it('formats position coordinates with one decimal place', () => {
    const preciseNode: RenderNode = {
      ...mockNode,
      position: [123.456, -78.901],
    };

    const { getByText } = render(
      <StitchTooltip visible={true} node={preciseNode} onClose={mockOnClose} />
    );

    expect(getByText('(123.5, -78.9)')).toBeTruthy();
  });
});
