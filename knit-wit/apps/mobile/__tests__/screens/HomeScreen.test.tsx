import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import HomeScreen from '../../src/screens/HomeScreen';
import type { MainTabScreenProps } from '../../src/types';

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
  key: 'Home-test',
  name: 'Home' as const,
  params: undefined,
  path: undefined,
};

describe('HomeScreen', () => {
  beforeEach(() => {
    mockNavigate.mockClear();
  });

  it('renders welcome message', () => {
    const { getByText } = render(
      <HomeScreen navigation={mockNavigation} route={mockRoute} />
    );

    expect(getByText('Welcome to Knit-Wit')).toBeTruthy();
  });

  it('renders feature list', () => {
    const { getByText } = render(
      <HomeScreen navigation={mockNavigation} route={mockRoute} />
    );

    expect(getByText('Parametric Patterns')).toBeTruthy();
    expect(getByText('Interactive Visualization')).toBeTruthy();
    expect(getByText('Multiple Exports')).toBeTruthy();
    expect(getByText('US/UK Terminology')).toBeTruthy();
  });

  it('navigates to Generate screen when generate button pressed', () => {
    const { getByLabelText } = render(
      <HomeScreen navigation={mockNavigation} route={mockRoute} />
    );

    const generateButton = getByLabelText('Start generating a pattern');
    fireEvent.press(generateButton);

    expect(mockNavigate).toHaveBeenCalledWith('Generate');
  });

  it('navigates to Parse screen when parse button pressed', () => {
    const { getByLabelText } = render(
      <HomeScreen navigation={mockNavigation} route={mockRoute} />
    );

    const parseButton = getByLabelText('Parse existing pattern');
    fireEvent.press(parseButton);

    expect(mockNavigate).toHaveBeenCalledWith('Parse');
  });

  it('has proper accessibility labels', () => {
    const { getByLabelText } = render(
      <HomeScreen navigation={mockNavigation} route={mockRoute} />
    );

    expect(getByLabelText('Home screen')).toBeTruthy();
    expect(getByLabelText('Start generating a pattern')).toBeTruthy();
    expect(getByLabelText('Parse existing pattern')).toBeTruthy();
  });
});
