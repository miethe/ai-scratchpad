import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import { NetworkError } from '../../src/components/common/NetworkError';

describe('NetworkError', () => {
  it('renders with default message', () => {
    const { getByText } = render(<NetworkError />);

    expect(getByText('Connection Error')).toBeTruthy();
    expect(getByText('Network connection failed')).toBeTruthy();
  });

  it('renders with custom message', () => {
    const customMessage = 'Unable to reach server';
    const { getByText } = render(<NetworkError message={customMessage} />);

    expect(getByText('Connection Error')).toBeTruthy();
    expect(getByText(customMessage)).toBeTruthy();
  });

  it('renders warning icon', () => {
    const { getByRole, getByText } = render(<NetworkError />);

    const icon = getByRole('image');
    expect(icon).toBeTruthy();
    expect(icon.props.accessibilityLabel).toBe('Warning');
    expect(getByText('⚠️')).toBeTruthy();
  });

  it('renders retry button when onRetry provided', () => {
    const onRetry = jest.fn();
    const { getByRole } = render(<NetworkError onRetry={onRetry} />);

    const button = getByRole('button');
    expect(button).toBeTruthy();
    expect(button.props.accessibilityLabel).toBe('Retry connection');
  });

  it('does not render retry button when onRetry not provided', () => {
    const { queryByRole } = render(<NetworkError />);

    // Should have image role (icon) but not button role
    expect(queryByRole('image')).toBeTruthy();
    expect(queryByRole('button')).toBeNull();
  });

  it('calls onRetry when retry button is pressed', () => {
    const onRetry = jest.fn();
    const { getByRole } = render(<NetworkError onRetry={onRetry} />);

    const button = getByRole('button');
    fireEvent.press(button);

    expect(onRetry).toHaveBeenCalledTimes(1);
  });

  it('calls onRetry multiple times when pressed multiple times', () => {
    const onRetry = jest.fn();
    const { getByRole } = render(<NetworkError onRetry={onRetry} />);

    const button = getByRole('button');
    fireEvent.press(button);
    fireEvent.press(button);
    fireEvent.press(button);

    expect(onRetry).toHaveBeenCalledTimes(3);
  });

  it('has proper accessibility attributes', () => {
    const onRetry = jest.fn();
    const { getByRole, getByText } = render(<NetworkError onRetry={onRetry} />);

    const button = getByRole('button');
    expect(button.props.accessibilityRole).toBe('button');
    expect(button.props.accessibilityLabel).toBe('Retry connection');
    expect(button.props.accessibilityHint).toBe('Attempts to reconnect to the network');

    const message = getByText('Network connection failed');
    expect(message.props.accessibilityRole).toBe('alert');
  });

  it('button has minimum touch target size', () => {
    const onRetry = jest.fn();
    const { getByRole } = render(<NetworkError onRetry={onRetry} />);

    const button = getByRole('button');
    const styles = button.props.style;

    // Check that minHeight and minWidth are at least 48 (comfortable touch target)
    expect(styles.minHeight).toBeGreaterThanOrEqual(48);
    expect(styles.minWidth).toBeGreaterThanOrEqual(48);
  });

  it('displays "Retry" button text', () => {
    const onRetry = jest.fn();
    const { getByText } = render(<NetworkError onRetry={onRetry} />);

    expect(getByText('Retry')).toBeTruthy();
  });

  it('renders with custom message and retry callback', () => {
    const customMessage = 'Connection timeout';
    const onRetry = jest.fn();
    const { getByText, getByRole } = render(
      <NetworkError message={customMessage} onRetry={onRetry} />
    );

    expect(getByText('Connection Error')).toBeTruthy();
    expect(getByText(customMessage)).toBeTruthy();

    const button = getByRole('button');
    fireEvent.press(button);
    expect(onRetry).toHaveBeenCalledTimes(1);
  });

  it('message has alert role for screen readers', () => {
    const { getByText } = render(<NetworkError />);

    const message = getByText('Network connection failed');
    expect(message.props.accessibilityRole).toBe('alert');
  });
});
