import React, { createContext, useContext, useMemo } from 'react';
import type { ReactNode } from 'react';
import { useSettingsStore } from '../stores/useSettingsStore';
import type { Theme } from './types';
import { defaultTheme, kidModeTheme, darkModeTheme, kidModeDarkTheme } from './themes';

interface ThemeContextValue {
  theme: Theme;
}

const ThemeContext = createContext<ThemeContextValue | undefined>(undefined);

export interface ThemeProviderProps {
  children: ReactNode;
}

export function ThemeProvider({ children }: ThemeProviderProps) {
  const { kidMode, darkMode } = useSettingsStore();

  const theme = useMemo(() => {
    if (kidMode && darkMode) {
      return kidModeDarkTheme;
    }
    if (kidMode) {
      return kidModeTheme;
    }
    if (darkMode) {
      return darkModeTheme;
    }
    return defaultTheme;
  }, [kidMode, darkMode]);

  const value = useMemo(() => ({ theme }), [theme]);

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

export function useTheme(): Theme {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context.theme;
}
