// Custom Jest setup file
// Provides minimal setup for React Native

// Define __DEV__ for React Native
global.__DEV__ = true;

// Mock Platform
jest.mock('react-native/Libraries/Utilities/Platform', () => ({
  OS: 'ios',
  select: (options) => options.ios || options.default,
}));

// Mock native modules
global.__reanimatedWorkletInit = () => {};

// Set up fake timers for animations
global.requestAnimationFrame = (cb) => {
  return setTimeout(cb, 0);
};

global.cancelAnimationFrame = (id) => {
  clearTimeout(id);
};

// Mock console methods to reduce noise in tests
global.console = {
  ...console,
  error: jest.fn(),
  warn: jest.fn(),
};

// Mock @react-native-community/slider
jest.mock('@react-native-community/slider', () => {
  const React = require('react');
  return {
    __esModule: true,
    default: jest.fn().mockImplementation((props) => {
      return React.createElement('Slider', props);
    }),
  };
});
