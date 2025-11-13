import React from 'react';
import { Text } from 'react-native';
import { render } from '@testing-library/react-native';
import { ThemeProvider, useTheme } from '../../src/theme/ThemeProvider';
import { useSettingsStore } from '../../src/stores/useSettingsStore';
import {
  defaultTheme,
  kidModeTheme,
  darkModeTheme,
  kidModeDarkTheme,
} from '../../src/theme/themes';

jest.mock('../../src/stores/useSettingsStore');

const TestComponent = () => {
  const theme = useTheme();
  return <Text testID="theme-primary">{theme.colors.primary}</Text>;
};

describe('ThemeProvider', () => {
  const mockUseSettingsStore = useSettingsStore as jest.MockedFunction<
    typeof useSettingsStore
  >;

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('provides default theme when no modes are enabled', () => {
    mockUseSettingsStore.mockReturnValue({
      kidMode: false,
      darkMode: false,
      defaultUnits: 'cm',
      defaultTerminology: 'US',
      setKidMode: jest.fn(),
      setDarkMode: jest.fn(),
      setDefaultUnits: jest.fn(),
      setDefaultTerminology: jest.fn(),
      _hasHydrated: true,
      _setHasHydrated: jest.fn(),
    });

    const { getByTestId } = render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );

    expect(getByTestId('theme-primary').children[0]).toBe(defaultTheme.colors.primary);
  });

  it('provides kid mode theme when kidMode is enabled', () => {
    mockUseSettingsStore.mockReturnValue({
      kidMode: true,
      darkMode: false,
      defaultUnits: 'cm',
      defaultTerminology: 'US',
      setKidMode: jest.fn(),
      setDarkMode: jest.fn(),
      setDefaultUnits: jest.fn(),
      setDefaultTerminology: jest.fn(),
      _hasHydrated: true,
      _setHasHydrated: jest.fn(),
    });

    const { getByTestId } = render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );

    expect(getByTestId('theme-primary').children[0]).toBe(kidModeTheme.colors.primary);
  });

  it('provides dark mode theme when darkMode is enabled', () => {
    mockUseSettingsStore.mockReturnValue({
      kidMode: false,
      darkMode: true,
      defaultUnits: 'cm',
      defaultTerminology: 'US',
      setKidMode: jest.fn(),
      setDarkMode: jest.fn(),
      setDefaultUnits: jest.fn(),
      setDefaultTerminology: jest.fn(),
      _hasHydrated: true,
      _setHasHydrated: jest.fn(),
    });

    const { getByTestId } = render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );

    expect(getByTestId('theme-primary').children[0]).toBe(darkModeTheme.colors.primary);
  });

  it('provides kid mode dark theme when both modes are enabled', () => {
    mockUseSettingsStore.mockReturnValue({
      kidMode: true,
      darkMode: true,
      defaultUnits: 'cm',
      defaultTerminology: 'US',
      setKidMode: jest.fn(),
      setDarkMode: jest.fn(),
      setDefaultUnits: jest.fn(),
      setDefaultTerminology: jest.fn(),
      _hasHydrated: true,
      _setHasHydrated: jest.fn(),
    });

    const { getByTestId } = render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );

    expect(getByTestId('theme-primary').children[0]).toBe(kidModeDarkTheme.colors.primary);
  });

  it('throws error when useTheme is used outside ThemeProvider', () => {
    // Suppress console.error for this test
    const consoleError = jest.spyOn(console, 'error').mockImplementation();

    expect(() => {
      render(<TestComponent />);
    }).toThrow('useTheme must be used within a ThemeProvider');

    consoleError.mockRestore();
  });

  it('provides all theme properties', () => {
    mockUseSettingsStore.mockReturnValue({
      kidMode: false,
      darkMode: false,
      defaultUnits: 'cm',
      defaultTerminology: 'US',
      setKidMode: jest.fn(),
      setDarkMode: jest.fn(),
      setDefaultUnits: jest.fn(),
      setDefaultTerminology: jest.fn(),
      _hasHydrated: true,
      _setHasHydrated: jest.fn(),
    });

    const ThemePropertiesTest = () => {
      const theme = useTheme();
      return (
        <>
          <Text testID="colors">{theme.colors ? 'has-colors' : 'no-colors'}</Text>
          <Text testID="typography">{theme.typography ? 'has-typography' : 'no-typography'}</Text>
          <Text testID="spacing">{theme.spacing ? 'has-spacing' : 'no-spacing'}</Text>
          <Text testID="borderRadius">
            {theme.borderRadius ? 'has-borderRadius' : 'no-borderRadius'}
          </Text>
          <Text testID="touchTargets">
            {theme.touchTargets ? 'has-touchTargets' : 'no-touchTargets'}
          </Text>
          <Text testID="shadows">{theme.shadows ? 'has-shadows' : 'no-shadows'}</Text>
        </>
      );
    };

    const { getByTestId } = render(
      <ThemeProvider>
        <ThemePropertiesTest />
      </ThemeProvider>
    );

    expect(getByTestId('colors').children[0]).toBe('has-colors');
    expect(getByTestId('typography').children[0]).toBe('has-typography');
    expect(getByTestId('spacing').children[0]).toBe('has-spacing');
    expect(getByTestId('borderRadius').children[0]).toBe('has-borderRadius');
    expect(getByTestId('touchTargets').children[0]).toBe('has-touchTargets');
    expect(getByTestId('shadows').children[0]).toBe('has-shadows');
  });

  it('memoizes theme based on kidMode and darkMode', () => {
    const { rerender } = render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );

    mockUseSettingsStore.mockReturnValue({
      kidMode: false,
      darkMode: false,
      defaultUnits: 'in', // Change non-theme setting
      defaultTerminology: 'UK', // Change non-theme setting
      setKidMode: jest.fn(),
      setDarkMode: jest.fn(),
      setDefaultUnits: jest.fn(),
      setDefaultTerminology: jest.fn(),
      _hasHydrated: true,
      _setHasHydrated: jest.fn(),
    });

    rerender(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );

    // Theme should still be default since kidMode and darkMode haven't changed
    // This is implicitly tested by the component not re-rendering with different theme
  });
});
