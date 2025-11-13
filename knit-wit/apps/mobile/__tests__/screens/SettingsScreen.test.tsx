import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import SettingsScreen from '../../src/screens/SettingsScreen';
import { useSettingsStore } from '../../src/stores/useSettingsStore';
import { telemetryClient } from '../../src/services/telemetryClient';

jest.mock('@react-native-async-storage/async-storage', () => ({
  getItem: jest.fn(),
  setItem: jest.fn(),
}));

jest.mock('../../src/stores/useSettingsStore');
jest.mock('../../src/services/telemetryClient', () => ({
  telemetryClient: {
    getConsent: jest.fn(),
    setConsent: jest.fn(),
  },
}));

const mockNavigation = {
  navigate: jest.fn(),
  goBack: jest.fn(),
  setOptions: jest.fn(),
} as any;

describe('SettingsScreen', () => {
  const mockUseSettingsStore = useSettingsStore as jest.MockedFunction<
    typeof useSettingsStore
  >;

  const defaultStoreValues = {
    kidMode: false,
    darkMode: false,
    dyslexiaFont: false,
    defaultUnits: 'cm' as const,
    defaultTerminology: 'US' as const,
    setKidMode: jest.fn(),
    setDarkMode: jest.fn(),
    setDyslexiaFont: jest.fn(),
    setDefaultUnits: jest.fn(),
    setDefaultTerminology: jest.fn(),
    _hasHydrated: true,
    _setHasHydrated: jest.fn(),
  };

  beforeEach(() => {
    jest.clearAllMocks();
    mockUseSettingsStore.mockReturnValue(defaultStoreValues);
    (telemetryClient.getConsent as jest.Mock).mockReturnValue(false);
    (AsyncStorage.getItem as jest.Mock).mockResolvedValue(null);
    (AsyncStorage.setItem as jest.Mock).mockResolvedValue(undefined);
  });

  it('renders correctly', () => {
    const { getByText } = render(<SettingsScreen navigation={mockNavigation} route={{} as any} />);

    expect(getByText('Settings')).toBeTruthy();
    expect(getByText('Customize your Knit-Wit experience')).toBeTruthy();
    expect(getByText('Appearance')).toBeTruthy();
    expect(getByText('Pattern Defaults')).toBeTruthy();
    expect(getByText('Privacy')).toBeTruthy();
    expect(getByText('About')).toBeTruthy();
  });

  it('displays Kid Mode toggle', () => {
    const { getByText, getByTestId } = render(
      <SettingsScreen navigation={mockNavigation} route={{} as any} />
    );

    expect(getByText('Kid Mode')).toBeTruthy();
    expect(getByText('Simplified interface for young learners with larger buttons and friendly colors')).toBeTruthy();
    expect(getByTestId('kid-mode-toggle')).toBeTruthy();
  });

  it('displays Dark Mode toggle', () => {
    const { getByText, getByTestId } = render(
      <SettingsScreen navigation={mockNavigation} route={{} as any} />
    );

    expect(getByText('Dark Mode')).toBeTruthy();
    expect(getByText('Use dark theme throughout the app')).toBeTruthy();
    expect(getByTestId('dark-mode-toggle')).toBeTruthy();
  });

  it('displays US Terminology toggle', () => {
    const { getByText, getByTestId } = render(
      <SettingsScreen navigation={mockNavigation} route={{} as any} />
    );

    expect(getByText('US Terminology')).toBeTruthy();
    expect(getByText('Use US crochet terms (turn off for UK terms)')).toBeTruthy();
    expect(getByTestId('us-terminology-toggle')).toBeTruthy();
  });

  it('displays Metric Units toggle', () => {
    const { getByText, getByTestId } = render(
      <SettingsScreen navigation={mockNavigation} route={{} as any} />
    );

    expect(getByText('Metric Units (cm)')).toBeTruthy();
    expect(getByText('Use metric units (turn off for imperial/inches)')).toBeTruthy();
    expect(getByTestId('metric-units-toggle')).toBeTruthy();
  });

  it('displays telemetry toggle', () => {
    const { getByText, getByTestId } = render(
      <SettingsScreen navigation={mockNavigation} route={{} as any} />
    );

    expect(getByText('Share Usage Data')).toBeTruthy();
    expect(getByText('Help us improve Knit-Wit by sharing anonymous usage data. No personal information is collected.')).toBeTruthy();
    expect(getByTestId('telemetry-toggle')).toBeTruthy();
  });

  it('loads telemetry consent state on mount', async () => {
    (telemetryClient.getConsent as jest.Mock).mockReturnValue(true);

    const { getByTestId } = render(<SettingsScreen navigation={mockNavigation} route={{} as any} />);

    await waitFor(() => {
      expect(telemetryClient.getConsent).toHaveBeenCalled();
      expect(getByTestId('telemetry-toggle').props.value).toBe(true);
    });
  });

  it('displays telemetry toggle with current consent state', async () => {
    (telemetryClient.getConsent as jest.Mock).mockReturnValue(false);

    const { getByTestId } = render(<SettingsScreen navigation={mockNavigation} route={{} as any} />);

    await waitFor(() => {
      expect(getByTestId('telemetry-toggle').props.value).toBe(false);
    });
  });

  it('calls telemetryClient.setConsent when toggle is changed', async () => {
    const { getByTestId } = render(<SettingsScreen navigation={mockNavigation} route={{} as any} />);

    const toggle = getByTestId('telemetry-toggle');

    // Enable telemetry
    fireEvent(toggle, 'onValueChange', true);

    await waitFor(() => {
      expect(telemetryClient.setConsent).toHaveBeenCalledWith(true);
    });

    // Disable telemetry
    fireEvent(toggle, 'onValueChange', false);

    await waitFor(() => {
      expect(telemetryClient.setConsent).toHaveBeenCalledWith(false);
    });
  });

  it('calls setKidMode when Kid Mode toggle is pressed', () => {
    const setKidMode = jest.fn();
    mockUseSettingsStore.mockReturnValue({
      ...defaultStoreValues,
      setKidMode,
    });

    const { getByTestId } = render(<SettingsScreen navigation={mockNavigation} route={{} as any} />);

    const toggle = getByTestId('kid-mode-toggle');
    fireEvent(toggle, 'onValueChange', true);

    expect(setKidMode).toHaveBeenCalledWith(true);
  });

  it('calls setDarkMode when Dark Mode toggle is pressed', () => {
    const setDarkMode = jest.fn();
    mockUseSettingsStore.mockReturnValue({
      ...defaultStoreValues,
      setDarkMode,
    });

    const { getByTestId } = render(<SettingsScreen navigation={mockNavigation} route={{} as any} />);

    const toggle = getByTestId('dark-mode-toggle');
    fireEvent(toggle, 'onValueChange', true);

    expect(setDarkMode).toHaveBeenCalledWith(true);
  });

  it('calls setDefaultTerminology when terminology toggle is pressed', () => {
    const setDefaultTerminology = jest.fn();
    mockUseSettingsStore.mockReturnValue({
      ...defaultStoreValues,
      defaultTerminology: 'US',
      setDefaultTerminology,
    });

    const { getByTestId } = render(<SettingsScreen navigation={mockNavigation} route={{} as any} />);

    const toggle = getByTestId('us-terminology-toggle');

    // Toggle to UK
    fireEvent(toggle, 'onValueChange', false);
    expect(setDefaultTerminology).toHaveBeenCalledWith('UK');

    // Toggle back to US
    fireEvent(toggle, 'onValueChange', true);
    expect(setDefaultTerminology).toHaveBeenCalledWith('US');
  });

  it('calls setDefaultUnits when units toggle is pressed', () => {
    const setDefaultUnits = jest.fn();
    mockUseSettingsStore.mockReturnValue({
      ...defaultStoreValues,
      defaultUnits: 'cm',
      setDefaultUnits,
    });

    const { getByTestId } = render(<SettingsScreen navigation={mockNavigation} route={{} as any} />);

    const toggle = getByTestId('metric-units-toggle');

    // Toggle to inches
    fireEvent(toggle, 'onValueChange', false);
    expect(setDefaultUnits).toHaveBeenCalledWith('in');

    // Toggle back to cm
    fireEvent(toggle, 'onValueChange', true);
    expect(setDefaultUnits).toHaveBeenCalledWith('cm');
  });

  it('reflects current store values in toggles', () => {
    mockUseSettingsStore.mockReturnValue({
      ...defaultStoreValues,
      kidMode: true,
      darkMode: true,
      defaultUnits: 'in',
      defaultTerminology: 'UK',
    });

    const { getByTestId } = render(<SettingsScreen navigation={mockNavigation} route={{} as any} />);

    expect(getByTestId('kid-mode-toggle').props.value).toBe(true);
    expect(getByTestId('dark-mode-toggle').props.value).toBe(true);
    expect(getByTestId('us-terminology-toggle').props.value).toBe(false); // UK = false
    expect(getByTestId('metric-units-toggle').props.value).toBe(false); // in = false
  });

  it('displays version and build information', () => {
    const { getByText } = render(<SettingsScreen navigation={mockNavigation} route={{} as any} />);

    expect(getByText('Version')).toBeTruthy();
    expect(getByText('1.0.0 (MVP)')).toBeTruthy();
    expect(getByText('Build')).toBeTruthy();
    expect(getByText('Development')).toBeTruthy();
  });

  it('displays documentation and issue report links', () => {
    const { getByText } = render(<SettingsScreen navigation={mockNavigation} route={{} as any} />);

    expect(getByText('Documentation')).toBeTruthy();
    expect(getByText('Report an Issue')).toBeTruthy();
  });

  it('has proper accessibility labels', () => {
    const { getByLabelText } = render(<SettingsScreen navigation={mockNavigation} route={{} as any} />);

    expect(getByLabelText('Settings screen')).toBeTruthy();
    expect(getByLabelText('Kid Mode toggle')).toBeTruthy();
    expect(getByLabelText('Dark Mode toggle')).toBeTruthy();
    expect(getByLabelText('US Terminology toggle')).toBeTruthy();
    expect(getByLabelText('Metric Units (cm) toggle')).toBeTruthy();
    expect(getByLabelText('Share Usage Data toggle')).toBeTruthy();
  });

  it('displays kid-friendly copy in Kid Mode', () => {
    mockUseSettingsStore.mockReturnValue({
      ...defaultStoreValues,
      kidMode: true,
    });

    const { getByText } = render(<SettingsScreen navigation={mockNavigation} route={{} as any} />);

    expect(getByText('Help us make the app better by sharing how you use it. No personal information is collected.')).toBeTruthy();
  });
});
