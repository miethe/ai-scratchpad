import { renderHook, act } from '@testing-library/react-native';
import { useSettingsStore } from '../../src/stores/useSettingsStore';

describe('useSettingsStore', () => {
  beforeEach(() => {
    // Reset store state before each test
    const { result } = renderHook(() => useSettingsStore());
    act(() => {
      result.current.setKidMode(false);
      result.current.setDarkMode(false);
      result.current.setDefaultUnits('cm');
      result.current.setDefaultTerminology('US');
    });
  });

  it('has correct initial state', () => {
    const { result } = renderHook(() => useSettingsStore());

    expect(result.current.kidMode).toBe(false);
    expect(result.current.darkMode).toBe(false);
    expect(result.current.defaultUnits).toBe('cm');
    expect(result.current.defaultTerminology).toBe('US');
  });

  it('can toggle Kid Mode', () => {
    const { result } = renderHook(() => useSettingsStore());

    act(() => {
      result.current.setKidMode(true);
    });

    expect(result.current.kidMode).toBe(true);
  });

  it('can toggle Dark Mode', () => {
    const { result } = renderHook(() => useSettingsStore());

    act(() => {
      result.current.setDarkMode(true);
    });

    expect(result.current.darkMode).toBe(true);
  });

  it('can change default units', () => {
    const { result } = renderHook(() => useSettingsStore());

    act(() => {
      result.current.setDefaultUnits('in');
    });

    expect(result.current.defaultUnits).toBe('in');
  });

  it('can change default terminology', () => {
    const { result } = renderHook(() => useSettingsStore());

    act(() => {
      result.current.setDefaultTerminology('UK');
    });

    expect(result.current.defaultTerminology).toBe('UK');
  });
});
