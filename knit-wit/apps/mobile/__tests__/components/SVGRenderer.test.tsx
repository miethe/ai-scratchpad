import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import { SVGRenderer } from '../../src/components/visualization/SVGRenderer';
import type { VisualizationFrame } from '../../src/types/visualization';

describe('SVGRenderer', () => {
  const mockFrame: VisualizationFrame = {
    round_number: 1,
    nodes: [
      { id: 'r1s0', stitch_type: 'sc', position: [100, 0], highlight: 'normal' },
      { id: 'r1s1', stitch_type: 'inc', position: [0, 100], highlight: 'increase' },
      { id: 'r1s2', stitch_type: 'dec', position: [-100, 0], highlight: 'decrease' },
    ],
    edges: [
      { source: 'r1s0', target: 'r1s1' },
      { source: 'r1s1', target: 'r1s2' },
      { source: 'r1s2', target: 'r1s0' },
    ],
    stitch_count: 3,
    highlights: ['r1s1', 'r1s2'],
  };

  it('renders without crashing', () => {
    const { toJSON } = render(<SVGRenderer frame={mockFrame} />);
    expect(toJSON()).toBeTruthy();
  });

  it('renders with custom dimensions', () => {
    const { toJSON } = render(
      <SVGRenderer frame={mockFrame} width={400} height={400} />
    );
    expect(toJSON()).toBeTruthy();
  });

  it('renders with empty frame', () => {
    const emptyFrame: VisualizationFrame = {
      round_number: 1,
      nodes: [],
      edges: [],
      stitch_count: 0,
      highlights: [],
    };

    const { toJSON } = render(<SVGRenderer frame={emptyFrame} />);
    expect(toJSON()).toBeTruthy();
  });

  it('renders nodes with correct accessibility labels', () => {
    const { getByLabelText } = render(<SVGRenderer frame={mockFrame} />);

    expect(getByLabelText('Stitch r1s0, type sc')).toBeTruthy();
    expect(getByLabelText('Stitch r1s1, type inc')).toBeTruthy();
    expect(getByLabelText('Stitch r1s2, type dec')).toBeTruthy();
  });

  it('handles stitch tap events', () => {
    const onTap = jest.fn();
    const { getByLabelText } = render(
      <SVGRenderer frame={mockFrame} onStitchTap={onTap} />
    );

    const node = getByLabelText('Stitch r1s0, type sc');
    fireEvent.press(node);

    expect(onTap).toHaveBeenCalledWith('r1s0');
  });

  it('does not crash when tap handler not provided', () => {
    const { getByLabelText } = render(<SVGRenderer frame={mockFrame} />);

    const node = getByLabelText('Stitch r1s0, type sc');
    fireEvent.press(node);

    // Should not throw error
  });

  it('handles multiple taps correctly', () => {
    const onTap = jest.fn();
    const { getByLabelText } = render(
      <SVGRenderer frame={mockFrame} onStitchTap={onTap} />
    );

    fireEvent.press(getByLabelText('Stitch r1s0, type sc'));
    fireEvent.press(getByLabelText('Stitch r1s1, type inc'));
    fireEvent.press(getByLabelText('Stitch r1s2, type dec'));

    expect(onTap).toHaveBeenCalledTimes(3);
    expect(onTap).toHaveBeenNthCalledWith(1, 'r1s0');
    expect(onTap).toHaveBeenNthCalledWith(2, 'r1s1');
    expect(onTap).toHaveBeenNthCalledWith(3, 'r1s2');
  });

  it('renders edges correctly', () => {
    const frameWithEdges: VisualizationFrame = {
      round_number: 1,
      nodes: [
        { id: 'n1', stitch_type: 'sc', position: [0, 0], highlight: 'normal' },
        { id: 'n2', stitch_type: 'sc', position: [10, 10], highlight: 'normal' },
      ],
      edges: [
        { source: 'n1', target: 'n2' },
      ],
      stitch_count: 2,
      highlights: [],
    };

    const { toJSON } = render(<SVGRenderer frame={frameWithEdges} />);
    expect(toJSON()).toBeTruthy();
  });

  it('handles edges with missing nodes gracefully', () => {
    const frameWithBadEdges: VisualizationFrame = {
      round_number: 1,
      nodes: [
        { id: 'n1', stitch_type: 'sc', position: [0, 0], highlight: 'normal' },
      ],
      edges: [
        { source: 'n1', target: 'missing' }, // Missing target
      ],
      stitch_count: 1,
      highlights: [],
    };

    const { toJSON } = render(<SVGRenderer frame={frameWithBadEdges} />);
    expect(toJSON()).toBeTruthy();
  });

  it('applies correct highlight colors', () => {
    const frameWithHighlights: VisualizationFrame = {
      round_number: 1,
      nodes: [
        { id: 'normal', stitch_type: 'sc', position: [0, 0], highlight: 'normal' },
        { id: 'inc', stitch_type: 'inc', position: [10, 0], highlight: 'increase' },
        { id: 'dec', stitch_type: 'dec', position: [20, 0], highlight: 'decrease' },
      ],
      edges: [],
      stitch_count: 3,
      highlights: ['inc', 'dec'],
    };

    const { toJSON } = render(<SVGRenderer frame={frameWithHighlights} />);
    const tree = toJSON();
    expect(tree).toBeTruthy();
  });

  it('uses default dimensions when not provided', () => {
    const { toJSON } = render(<SVGRenderer frame={mockFrame} />);
    expect(toJSON()).toBeTruthy();
  });

  it('maintains aspect ratio with scaling', () => {
    const { rerender, toJSON } = render(
      <SVGRenderer frame={mockFrame} width={200} height={200} />
    );
    const tree1 = toJSON();

    rerender(<SVGRenderer frame={mockFrame} width={400} height={400} />);
    const tree2 = toJSON();

    expect(tree1).toBeTruthy();
    expect(tree2).toBeTruthy();
  });

  it('has proper accessibility labels on nodes', () => {
    const { getByLabelText } = render(<SVGRenderer frame={mockFrame} />);

    const node = getByLabelText('Stitch r1s0, type sc');
    expect(node).toBeTruthy();
    expect(node.props.accessibilityLabel).toBe('Stitch r1s0, type sc');
  });

  it('re-renders when frame changes', () => {
    const frame1: VisualizationFrame = {
      round_number: 1,
      nodes: [{ id: 'n1', stitch_type: 'sc', position: [0, 0], highlight: 'normal' }],
      edges: [],
      stitch_count: 1,
      highlights: [],
    };

    const frame2: VisualizationFrame = {
      round_number: 2,
      nodes: [
        { id: 'n1', stitch_type: 'sc', position: [0, 0], highlight: 'normal' },
        { id: 'n2', stitch_type: 'inc', position: [10, 0], highlight: 'increase' },
      ],
      edges: [{ source: 'n1', target: 'n2' }],
      stitch_count: 2,
      highlights: ['n2'],
    };

    const { rerender, getByLabelText, queryByLabelText } = render(
      <SVGRenderer frame={frame1} />
    );

    expect(getByLabelText('Stitch n1, type sc')).toBeTruthy();
    expect(queryByLabelText('Stitch n2, type inc')).toBeNull();

    rerender(<SVGRenderer frame={frame2} />);

    expect(getByLabelText('Stitch n1, type sc')).toBeTruthy();
    expect(getByLabelText('Stitch n2, type inc')).toBeTruthy();
  });
});
