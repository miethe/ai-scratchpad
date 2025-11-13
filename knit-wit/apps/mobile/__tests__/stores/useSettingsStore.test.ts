import { renderHook, act, waitFor } from '@testing-library/react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useSettingsStore } from '../../src/stores/useSettingsStore';

const SETTINGS_STORAGE_KEY = '@knit-wit/settings';

jest.mock('@react-native-async-storage/async-storage', () => ({
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
}));

describe('useSettingsStore', () => {
  beforeEach(async () => {
    jest.clearAllMocks();
    (AsyncStorage.getItem as jest.Mock).mockResolvedValue(null);
    (AsyncStorage.setItem as jest.Mock).mockResolvedValue(undefined);

    // Reset store state before each test
    const { result } = renderHook(() => useSettingsStore());
    act(() => {
      result.current.setKidMode(false);
      result.current.setDarkMode(false);
      result.current.setDefaultUnits('cm');
      result.current.setDefaultTerminology('US');
    });

    // Wait for async operations
    await waitFor(() => {
      expect(result.current._hasHydrated).toBe(true);
    }, { timeout: 1000 });
  });

  it('has correct initial state', () => {
    const { result } = renderHook(() => useSettingsStore());

    expect(result.current.kidMode).toBe(false);
    expect(result.current.darkMode).toBe(false);
    expect(result.current.defaultUnits).toBe('cm');
    expect(result.current.defaultTerminology).toBe('US');
  });

  it('can toggle Kid Mode', async () => {
    const { result } = renderHook(() => useSettingsStore());

    act(() => {
      result.current.setKidMode(true);
    });

    expect(result.current.kidMode).toBe(true);

    await waitFor(() => {
      expect(AsyncStorage.setItem).toHaveBeenCalledWith(
        SETTINGS_STORAGE_KEY,
        expect.stringContaining('"kidMode":true')
      );
    });
  });

  it('can toggle Dark Mode', async () => {
    const { result } = renderHook(() => useSettingsStore());

    act(() => {
      result.current.setDarkMode(true);
    });

    expect(result.current.darkMode).toBe(true);

    await waitFor(() => {
      expect(AsyncStorage.setItem).toHaveBeenCalledWith(
        SETTINGS_STORAGE_KEY,
        expect.stringContaining('"darkMode":true')
      );
    });
  });

  it('can change default units', async () => {
    const { result } = renderHook(() => useSettingsStore());

    act(() => {
      result.current.setDefaultUnits('in');
    });

    expect(result.current.defaultUnits).toBe('in');

    await waitFor(() => {
      expect(AsyncStorage.setItem).toHaveBeenCalledWith(
        SETTINGS_STORAGE_KEY,
        expect.stringContaining('"defaultUnits":"in"')
      );
    });
  });

  it('can change default terminology', async () => {
    const { result } = renderHook(() => useSettingsStore());

    act(() => {
      result.current.setDefaultTerminology('UK');
    });

    expect(result.current.defaultTerminology).toBe('UK');

    await waitFor(() => {
      expect(AsyncStorage.setItem).toHaveBeenCalledWith(
        SETTINGS_STORAGE_KEY,
        expect.stringContaining('"defaultTerminology":"UK"')
      );
    });
  });

  it('persists settings to AsyncStorage when changed', async () => {
    const { result } = renderHook(() => useSettingsStore());

    act(() => {
      result.current.setKidMode(true);
      result.current.setDarkMode(true);
      result.current.setDefaultUnits('in');
      result.current.setDefaultTerminology('UK');
    });

    await waitFor(() => {
      expect(AsyncStorage.setItem).toHaveBeenCalled();
    });

    const lastCall = (AsyncStorage.setItem as jest.Mock).mock.calls[
      (AsyncStorage.setItem as jest.Mock).mock.calls.length - 1
    ];

    expect(lastCall[0]).toBe(SETTINGS_STORAGE_KEY);

    const savedData = JSON.parse(lastCall[1]);
    expect(savedData).toEqual({
      kidMode: true,
      darkMode: true,
      defaultUnits: 'in',
      defaultTerminology: 'UK',
    });
  });

  it('loads settings from AsyncStorage on initialization', async () => {
    const storedSettings = {
      kidMode: true,
      darkMode: false,
      defaultUnits: 'in',
      defaultTerminology: 'UK',
    };

    (AsyncStorage.getItem as jest.Mock).mockResolvedValueOnce(
      JSON.stringify(storedSettings)
    );

    // Create a new store instance by re-importing
    jest.resetModules();
    const { useSettingsStore: freshStore } = require('../../src/stores/useSettingsStore');

    await waitFor(() => {
      const state = freshStore.getState();
      expect(state._hasHydrated).toBe(true);
    }, { timeout: 1000 });

    const state = freshStore.getState();
    expect(state.kidMode).toBe(true);
    expect(state.darkMode).toBe(false);
    expect(state.defaultUnits).toBe('in');
    expect(state.defaultTerminology).toBe('UK');
  });

  it('handles AsyncStorage errors gracefully', async () => {
    const consoleError = jest.spyOn(console, 'error').mockImplementation();

    (AsyncStorage.setItem as jest.Mock).mockRejectedValueOnce(
      new Error('Storage error')
    );

    const { result } = renderHook(() => useSettingsStore());

    act(() => {
      result.current.setKidMode(true);
    });

    await waitFor(() => {
      expect(consoleError).toHaveBeenCalledWith(
        'Failed to save settings to storage:',
        expect.any(Error)
      );
    });

    consoleError.mockRestore();
  });
});
