import React, { createContext, useContext, useMemo } from 'react';
import type { ReactNode } from 'react';
import { useSettingsStore } from '../stores/useSettingsStore';
import type { Theme } from './types';
import { createTheme } from './themes';

interface ThemeContextValue {
  theme: Theme;
}

const ThemeContext = createContext<ThemeContextValue | undefined>(undefined);

export interface ThemeProviderProps {
  children: ReactNode;
}

export function ThemeProvider({ children }: ThemeProviderProps) {
  const { kidMode, darkMode, dyslexiaFont } = useSettingsStore();

  const theme = useMemo(() => {
    return createTheme({
      mode: kidMode && darkMode ? 'kidModeDark' : kidMode ? 'kidMode' : darkMode ? 'darkMode' : 'default',
      useDyslexiaFont: dyslexiaFont,
    });
  }, [kidMode, darkMode, dyslexiaFont]);

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
