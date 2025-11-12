import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import { Text, View } from 'react-native';
import { ErrorBoundary } from '../../src/components/common/ErrorBoundary';

// Component that throws an error
const ThrowError = ({ shouldThrow }: { shouldThrow: boolean }) => {
  if (shouldThrow) {
    throw new Error('Test error message');
  }
  return <Text>No error</Text>;
};

describe('ErrorBoundary', () => {
  // Suppress console.error for these tests
  const originalError = console.error;
  beforeAll(() => {
    console.error = jest.fn();
  });

  afterAll(() => {
    console.error = originalError;
  });

  it('renders children when there is no error', () => {
    const { getByText } = render(
      <ErrorBoundary>
        <Text>Child component</Text>
      </ErrorBoundary>
    );

    expect(getByText('Child component')).toBeTruthy();
  });

  it('renders error UI when an error is thrown', () => {
    const { getByText } = render(
      <ErrorBoundary>
        <ThrowError shouldThrow={true} />
      </ErrorBoundary>
    );

    expect(getByText('Something went wrong')).toBeTruthy();
    expect(getByText('Test error message')).toBeTruthy();
  });

  it('renders "Try Again" button when error occurs', () => {
    const { getByRole } = render(
      <ErrorBoundary>
        <ThrowError shouldThrow={true} />
      </ErrorBoundary>
    );

    const button = getByRole('button');
    expect(button).toBeTruthy();
    expect(button.props.accessibilityLabel).toBe('Try again');
  });

  it('calls onReset when "Try Again" button is pressed', () => {
    const onReset = jest.fn();
    const { getByRole, rerender } = render(
      <ErrorBoundary onReset={onReset}>
        <ThrowError shouldThrow={true} />
      </ErrorBoundary>
    );

    const button = getByRole('button');
    fireEvent.press(button);

    expect(onReset).toHaveBeenCalledTimes(1);
  });

  it('resets error state when "Try Again" is pressed', () => {
    let shouldThrow = true;
    const { getByRole, getByText, rerender } = render(
      <ErrorBoundary>
        <ThrowError shouldThrow={shouldThrow} />
      </ErrorBoundary>
    );

    // Error should be displayed
    expect(getByText('Something went wrong')).toBeTruthy();

    // Fix the error and press Try Again
    shouldThrow = false;
    const button = getByRole('button');
    fireEvent.press(button);

    // Need to rerender with fixed component
    rerender(
      <ErrorBoundary>
        <ThrowError shouldThrow={shouldThrow} />
      </ErrorBoundary>
    );

    // Should show "No error" text now
    expect(getByText('No error')).toBeTruthy();
  });

  it('renders custom fallback when provided', () => {
    const customFallback = (
      <View>
        <Text>Custom error UI</Text>
      </View>
    );

    const { getByText } = render(
      <ErrorBoundary fallback={customFallback}>
        <ThrowError shouldThrow={true} />
      </ErrorBoundary>
    );

    expect(getByText('Custom error UI')).toBeTruthy();
  });

  it('displays default error message when error.message is undefined', () => {
    const ThrowErrorWithoutMessage = () => {
      const error: any = new Error();
      error.message = undefined;
      throw error;
    };

    const { getByText } = render(
      <ErrorBoundary>
        <ThrowErrorWithoutMessage />
      </ErrorBoundary>
    );

    expect(getByText('An unexpected error occurred')).toBeTruthy();
  });

  it('has proper accessibility attributes', () => {
    const { getByRole, getByText } = render(
      <ErrorBoundary>
        <ThrowError shouldThrow={true} />
      </ErrorBoundary>
    );

    const button = getByRole('button');
    expect(button.props.accessibilityLabel).toBe('Try again');
    expect(button.props.accessibilityHint).toBe('Attempts to recover from the error');

    const errorMessage = getByText('Test error message');
    expect(errorMessage.props.accessibilityRole).toBe('alert');
  });

  it('button has minimum touch target size', () => {
    const { getByRole } = render(
      <ErrorBoundary>
        <ThrowError shouldThrow={true} />
      </ErrorBoundary>
    );

    const button = getByRole('button');
    const styles = button.props.style;

    // Check that minHeight and minWidth are at least 48 (comfortable touch target)
    expect(styles.minHeight).toBeGreaterThanOrEqual(48);
    expect(styles.minWidth).toBeGreaterThanOrEqual(48);
  });
});
