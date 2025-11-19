import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { Units, Terminology } from '../types';

interface SettingsState {
  // User preferences
  kidMode: boolean;
  units: Units;
  terminology: Terminology;
  theme: 'light' | 'dark' | 'system';

  // Accessibility
  highContrast: boolean;
  reducedMotion: boolean;
  fontSize: 'small' | 'medium' | 'large';

  // Actions
  setKidMode: (enabled: boolean) => void;
  setUnits: (units: Units) => void;
  setTerminology: (terminology: Terminology) => void;
  setTheme: (theme: 'light' | 'dark' | 'system') => void;
  setHighContrast: (enabled: boolean) => void;
  setReducedMotion: (enabled: boolean) => void;
  setFontSize: (size: 'small' | 'medium' | 'large') => void;

  // Reset
  resetSettings: () => void;
}

const defaultSettings = {
  kidMode: false,
  units: 'cm' as Units,
  terminology: 'US' as Terminology,
  theme: 'system' as const,
  highContrast: false,
  reducedMotion: false,
  fontSize: 'medium' as const,
};

export const useSettingsStore = create<SettingsState>()(
  persist(
    (set) => ({
      ...defaultSettings,

      setKidMode: (enabled) => set({ kidMode: enabled }),
      setUnits: (units) => set({ units }),
      setTerminology: (terminology) => set({ terminology }),
      setTheme: (theme) => set({ theme }),
      setHighContrast: (enabled) => set({ highContrast: enabled }),
      setReducedMotion: (enabled) => set({ reducedMotion: enabled }),
      setFontSize: (size) => set({ fontSize: size }),

      resetSettings: () => set(defaultSettings),
    }),
    {
      name: 'knit-wit-settings',
    }
  )
);
