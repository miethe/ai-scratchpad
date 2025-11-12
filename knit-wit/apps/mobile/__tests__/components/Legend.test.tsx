import React from 'react';
import { render } from '@testing-library/react-native';
import { Legend } from '../../src/components/visualization/Legend';

describe('Legend', () => {
  it('renders all legend items', () => {
    const { getByText } = render(<Legend />);

    expect(getByText('Legend')).toBeTruthy();
    expect(getByText('Increase')).toBeTruthy();
    expect(getByText('Decrease')).toBeTruthy();
    expect(getByText('Normal')).toBeTruthy();
  });

  it('displays descriptions for each item', () => {
    const { getByText } = render(<Legend />);

    expect(getByText('2 sc in same stitch')).toBeTruthy();
    expect(getByText('sc2tog')).toBeTruthy();
    expect(getByText('Regular stitch')).toBeTruthy();
  });

  it('has accessibility labels', () => {
    const { getByLabelText } = render(<Legend />);

    expect(getByLabelText('Increase: 2 sc in same stitch')).toBeTruthy();
    expect(getByLabelText('Decrease: sc2tog')).toBeTruthy();
    expect(getByLabelText('Normal: Regular stitch')).toBeTruthy();
  });

  it('renders with correct styling', () => {
    const { getByText } = render(<Legend />);
    const title = getByText('Legend');

    expect(title).toBeTruthy();
    expect(title.props.style).toMatchObject({
      fontSize: 14,
      fontWeight: 'bold',
    });
  });
});
