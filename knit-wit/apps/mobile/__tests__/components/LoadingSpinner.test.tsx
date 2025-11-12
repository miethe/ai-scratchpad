import React from 'react';
import { render } from '@testing-library/react-native';
import { LoadingSpinner } from '../../src/components/common/LoadingSpinner';
import { colors } from '../../src/theme/colors';

describe('LoadingSpinner', () => {
  it('renders correctly with default props', () => {
    const { getByRole } = render(<LoadingSpinner />);

    const spinner = getByRole('progressbar');
    expect(spinner).toBeTruthy();
    expect(spinner.props.accessibilityLabel).toBe('Loading');
  });

  it('renders with small size', () => {
    const { getByRole } = render(<LoadingSpinner size="small" />);

    const spinner = getByRole('progressbar');
    expect(spinner).toBeTruthy();
  });

  it('renders with large size', () => {
    const { getByRole } = render(<LoadingSpinner size="large" />);

    const spinner = getByRole('progressbar');
    expect(spinner).toBeTruthy();
  });

  it('renders with custom message', () => {
    const message = 'Loading pattern...';
    const { getByText, getByRole } = render(<LoadingSpinner message={message} />);

    const messageElement = getByText(message);
    expect(messageElement).toBeTruthy();

    const spinner = getByRole('progressbar');
    expect(spinner.props.accessibilityLabel).toBe(message);
  });

  it('does not render message when not provided', () => {
    const { queryByText } = render(<LoadingSpinner />);

    // There should be no text elements
    expect(queryByText(/./)).toBeNull();
  });

  it('renders with custom color', () => {
    const customColor = colors.secondary;
    const { getByRole } = render(<LoadingSpinner color={customColor} />);

    const spinner = getByRole('progressbar');
    expect(spinner).toBeTruthy();
  });

  it('uses default primary color when color not provided', () => {
    const { getByRole } = render(<LoadingSpinner />);

    const spinner = getByRole('progressbar');
    expect(spinner).toBeTruthy();
  });

  it('has proper accessibility attributes', () => {
    const message = 'Loading data...';
    const { getByRole, getByText } = render(<LoadingSpinner message={message} />);

    const spinner = getByRole('progressbar');
    expect(spinner.props.accessibilityLabel).toBe(message);

    const messageText = getByText(message);
    expect(messageText.props.accessibilityLiveRegion).toBe('polite');
  });

  it('renders with all props combined', () => {
    const message = 'Please wait...';
    const customColor = colors.info;
    const { getByRole, getByText } = render(
      <LoadingSpinner size="small" message={message} color={customColor} />
    );

    expect(getByRole('progressbar')).toBeTruthy();
    expect(getByText(message)).toBeTruthy();
  });
});
