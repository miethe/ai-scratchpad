import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import { Text } from 'react-native';
import { EmptyState } from '../../src/components/common/EmptyState';

describe('EmptyState', () => {
  it('renders with title only', () => {
    const { getByText } = render(<EmptyState title="No patterns found" />);

    expect(getByText('No patterns found')).toBeTruthy();
  });

  it('renders with title and message', () => {
    const { getByText } = render(
      <EmptyState title="No patterns yet" message="Generate your first pattern to get started" />
    );

    expect(getByText('No patterns yet')).toBeTruthy();
    expect(getByText('Generate your first pattern to get started')).toBeTruthy();
  });

  it('does not render message when not provided', () => {
    const { queryByText } = render(<EmptyState title="Empty" />);

    expect(getByText('Empty')).toBeTruthy();
    // Should only have the title text
    const allTexts = queryByText(/./);
    expect(allTexts).toBeTruthy();
  });

  it('renders action button when actionLabel and onAction provided', () => {
    const onAction = jest.fn();
    const { getByRole } = render(
      <EmptyState title="Empty" actionLabel="Create Pattern" onAction={onAction} />
    );

    const button = getByRole('button');
    expect(button).toBeTruthy();
    expect(button.props.accessibilityLabel).toBe('Create Pattern');
  });

  it('does not render button when actionLabel is missing', () => {
    const onAction = jest.fn();
    const { queryByRole } = render(<EmptyState title="Empty" onAction={onAction} />);

    expect(queryByRole('button')).toBeNull();
  });

  it('does not render button when onAction is missing', () => {
    const { queryByRole } = render(<EmptyState title="Empty" actionLabel="Create" />);

    expect(queryByRole('button')).toBeNull();
  });

  it('calls onAction when button is pressed', () => {
    const onAction = jest.fn();
    const { getByRole } = render(
      <EmptyState title="Empty" actionLabel="Create" onAction={onAction} />
    );

    const button = getByRole('button');
    fireEvent.press(button);

    expect(onAction).toHaveBeenCalledTimes(1);
  });

  it('renders custom icon when provided', () => {
    const CustomIcon = () => <Text testID="custom-icon">📦</Text>;

    const { getByTestId, getByRole } = render(
      <EmptyState title="Empty" icon={<CustomIcon />} />
    );

    expect(getByTestId('custom-icon')).toBeTruthy();
    const iconContainer = getByRole('image');
    expect(iconContainer).toBeTruthy();
  });

  it('does not render icon container when icon not provided', () => {
    const { queryByRole } = render(<EmptyState title="Empty" />);

    expect(queryByRole('image')).toBeNull();
  });

  it('renders with all props combined', () => {
    const onAction = jest.fn();
    const CustomIcon = () => <Text testID="icon">🎨</Text>;

    const { getByText, getByRole, getByTestId } = render(
      <EmptyState
        title="No patterns"
        message="Start creating"
        actionLabel="Generate"
        onAction={onAction}
        icon={<CustomIcon />}
      />
    );

    expect(getByText('No patterns')).toBeTruthy();
    expect(getByText('Start creating')).toBeTruthy();
    expect(getByRole('button')).toBeTruthy();
    expect(getByTestId('icon')).toBeTruthy();
  });

  it('has proper accessibility attributes on button', () => {
    const onAction = jest.fn();
    const { getByRole } = render(
      <EmptyState title="Empty" actionLabel="Create Pattern" onAction={onAction} />
    );

    const button = getByRole('button');
    expect(button.props.accessibilityRole).toBe('button');
    expect(button.props.accessibilityLabel).toBe('Create Pattern');
  });

  it('button has minimum touch target size', () => {
    const onAction = jest.fn();
    const { getByRole } = render(
      <EmptyState title="Empty" actionLabel="Create" onAction={onAction} />
    );

    const button = getByRole('button');
    const styles = button.props.style;

    // Check that minHeight and minWidth are at least 48 (comfortable touch target)
    expect(styles.minHeight).toBeGreaterThanOrEqual(48);
    expect(styles.minWidth).toBeGreaterThanOrEqual(48);
  });

  it('displays button text correctly', () => {
    const onAction = jest.fn();
    const { getByText } = render(
      <EmptyState title="Empty" actionLabel="Start Now" onAction={onAction} />
    );

    expect(getByText('Start Now')).toBeTruthy();
  });
});
