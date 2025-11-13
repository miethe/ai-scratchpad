import React from 'react';
import { render } from '@testing-library/react-native';
import App from '../App';

// Mock expo-status-bar
jest.mock('expo-status-bar', () => ({
  StatusBar: () => null,
}));

// Mock react-native-safe-area-context
jest.mock('react-native-safe-area-context', () => {
  const inset = { top: 0, right: 0, bottom: 0, left: 0 };
  return {
    SafeAreaProvider: ({ children }: { children: React.ReactNode }) => children,
    SafeAreaConsumer: ({ children }: { children: (insets: typeof inset) => React.ReactNode }) =>
      children(inset),
    useSafeAreaInsets: () => inset,
  };
});

// Mock navigation
jest.mock('../src/navigation', () => ({
  RootNavigator: () => null,
}));

// Mock theme
jest.mock('../src/theme', () => ({
  ThemeProvider: ({ children }: { children: React.ReactNode }) => children,
  useTheme: () => ({
    colors: {
      surface: '#FFFFFF',
      textPrimary: '#111827',
      textSecondary: '#6B7280',
      textInverse: '#FFFFFF',
      primary: '#6B4EFF',
      gray200: '#E5E7EB',
    },
    typography: {
      titleLarge: { fontFamily: 'System', fontSize: 22, lineHeight: 28, fontWeight: '600' },
      bodyLarge: { fontFamily: 'System', fontSize: 16, lineHeight: 24, fontWeight: '400' },
      labelLarge: { fontFamily: 'System', fontSize: 14, lineHeight: 20, fontWeight: '500' },
    },
    spacing: { sm: 8, md: 16, lg: 24 },
    borderRadius: { md: 8, lg: 12 },
    touchTargets: { comfortable: 48 },
    shadows: {
      lg: {
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.15,
        shadowRadius: 8,
        elevation: 5,
      },
    },
  }),
}));

// Mock ConsentPrompt
jest.mock('../src/components/telemetry/ConsentPrompt', () => ({
  ConsentPrompt: () => null,
}));

describe('App', () => {
  it('renders without crashing', () => {
    // Should not throw an error
    expect(() => render(<App />)).not.toThrow();
  });
});
