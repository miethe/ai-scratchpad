import React from 'react';
import { render } from '@testing-library/react-native';
import App from '../App';

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

describe('App', () => {
  it('renders without crashing', () => {
    const { root } = render(<App />);
    expect(root).toBeTruthy();
  });
});
