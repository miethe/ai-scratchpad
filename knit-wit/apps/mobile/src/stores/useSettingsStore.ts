import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';
import type { Units, Terminology } from '../types';

const SETTINGS_STORAGE_KEY = '@knit-wit/settings';

interface SettingsState {
  // Appearance
  kidMode: boolean;
  darkMode: boolean;
  dyslexiaFont: boolean;

  // Pattern defaults
  defaultUnits: Units;
  defaultTerminology: Terminology;

  // Internal state
  _hasHydrated: boolean;

  // Actions
  setKidMode: (enabled: boolean) => void;
  setDarkMode: (enabled: boolean) => void;
  setDyslexiaFont: (enabled: boolean) => void;
  setDefaultUnits: (units: Units) => void;
  setDefaultTerminology: (terminology: Terminology) => void;
  _setHasHydrated: (hasHydrated: boolean) => void;
}

interface PersistedSettings {
  kidMode: boolean;
  darkMode: boolean;
  dyslexiaFont: boolean;
  defaultUnits: Units;
  defaultTerminology: Terminology;
}

const defaultSettings: PersistedSettings = {
  kidMode: false,
  darkMode: false,
  dyslexiaFont: false,
  defaultUnits: 'cm',
  defaultTerminology: 'US',
};

async function loadSettings(): Promise<PersistedSettings> {
  try {
    const stored = await AsyncStorage.getItem(SETTINGS_STORAGE_KEY);
    if (stored) {
      return { ...defaultSettings, ...JSON.parse(stored) };
    }
  } catch (error) {
    console.error('Failed to load settings from storage:', error);
  }
  return defaultSettings;
}

async function saveSettings(settings: PersistedSettings): Promise<void> {
  try {
    await AsyncStorage.setItem(SETTINGS_STORAGE_KEY, JSON.stringify(settings));
  } catch (error) {
    console.error('Failed to save settings to storage:', error);
  }
}

export const useSettingsStore = create<SettingsState>((set, get) => ({
  // Initial state
  ...defaultSettings,
  _hasHydrated: false,

  // Actions
  setKidMode: (enabled) => {
    set({ kidMode: enabled });
    const { kidMode, darkMode, dyslexiaFont, defaultUnits, defaultTerminology } = get();
    saveSettings({ kidMode, darkMode, dyslexiaFont, defaultUnits, defaultTerminology });
  },
  setDarkMode: (enabled) => {
    set({ darkMode: enabled });
    const { kidMode, darkMode, dyslexiaFont, defaultUnits, defaultTerminology } = get();
    saveSettings({ kidMode, darkMode, dyslexiaFont, defaultUnits, defaultTerminology });
  },
  setDyslexiaFont: (enabled) => {
    set({ dyslexiaFont: enabled });
    const { kidMode, darkMode, dyslexiaFont, defaultUnits, defaultTerminology } = get();
    saveSettings({ kidMode, darkMode, dyslexiaFont, defaultUnits, defaultTerminology });
  },
  setDefaultUnits: (units) => {
    set({ defaultUnits: units });
    const { kidMode, darkMode, dyslexiaFont, defaultUnits, defaultTerminology } = get();
    saveSettings({ kidMode, darkMode, dyslexiaFont, defaultUnits, defaultTerminology });
  },
  setDefaultTerminology: (terminology) => {
    set({ defaultTerminology: terminology });
    const { kidMode, darkMode, dyslexiaFont, defaultUnits, defaultTerminology } = get();
    saveSettings({ kidMode, darkMode, dyslexiaFont, defaultUnits, defaultTerminology });
  },
  _setHasHydrated: (hasHydrated) => set({ _hasHydrated: hasHydrated }),
}));

// Initialize settings from storage on app start
loadSettings().then((settings) => {
  useSettingsStore.setState({
    ...settings,
    _hasHydrated: true,
  });
});
