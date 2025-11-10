import { create } from 'zustand';
import type { Units, Terminology } from '../types';

interface SettingsState {
  // Appearance
  kidMode: boolean;
  darkMode: boolean;

  // Pattern defaults
  defaultUnits: Units;
  defaultTerminology: Terminology;

  // Actions
  setKidMode: (enabled: boolean) => void;
  setDarkMode: (enabled: boolean) => void;
  setDefaultUnits: (units: Units) => void;
  setDefaultTerminology: (terminology: Terminology) => void;
}

export const useSettingsStore = create<SettingsState>((set) => ({
  // Initial state
  kidMode: false,
  darkMode: false,
  defaultUnits: 'cm',
  defaultTerminology: 'US',

  // Actions
  setKidMode: (enabled) => set({ kidMode: enabled }),
  setDarkMode: (enabled) => set({ darkMode: enabled }),
  setDefaultUnits: (units) => set({ defaultUnits: units }),
  setDefaultTerminology: (terminology) => set({ defaultTerminology: terminology }),
}));
