// Custom Jest setup file
// Provides minimal setup for React Native

// Define __DEV__ for React Native
global.__DEV__ = true;

// Set up environment variables FIRST before any imports
process.env.EXPO_PUBLIC_API_URL = 'http://localhost:8000/api/v1';

// Mock expo virtual environment
jest.mock('expo/virtual/env', () => ({
  env: process.env,
}), { virtual: true });

// Mock Dimensions before Platform to ensure it's available
const mockDimensions = {
  get: jest.fn(() => ({ width: 375, height: 812 })),
  addEventListener: jest.fn(),
  removeEventListener: jest.fn(),
};

jest.doMock('react-native/Libraries/Utilities/Dimensions', () => mockDimensions);

// Mock Platform
jest.mock('react-native/Libraries/Utilities/Platform', () => ({
  OS: 'ios',
  select: (options) => options.ios || options.default,
}));

// Mock AccessibilityInfo
jest.mock('react-native/Libraries/Components/AccessibilityInfo/AccessibilityInfo', () => ({
  announceForAccessibility: jest.fn(),
  isReduceMotionEnabled: jest.fn(() => Promise.resolve(false)),
  isScreenReaderEnabled: jest.fn(() => Promise.resolve(false)),
  addEventListener: jest.fn(),
  removeEventListener: jest.fn(),
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

// Mock react-native-svg
jest.mock('react-native-svg', () => {
  const React = require('react');
  return {
    __esModule: true,
    default: jest.fn().mockImplementation((props) => React.createElement('Svg', props)),
    Circle: jest.fn().mockImplementation((props) => React.createElement('Circle', props)),
    Line: jest.fn().mockImplementation((props) => React.createElement('Line', props)),
    G: jest.fn().mockImplementation((props) => React.createElement('G', props)),
    Rect: jest.fn().mockImplementation((props) => React.createElement('Rect', props)),
    Path: jest.fn().mockImplementation((props) => React.createElement('Path', props)),
  };
});

// Mock expo-file-system
jest.mock('expo-file-system', () => ({
  documentDirectory: 'file:///mock/document/',
  writeAsStringAsync: jest.fn().mockResolvedValue(undefined),
  EncodingType: {
    Base64: 'base64',
  },
}));

// Mock expo-sharing
jest.mock('expo-sharing', () => ({
  isAvailableAsync: jest.fn().mockResolvedValue(true),
  shareAsync: jest.fn().mockResolvedValue(undefined),
}));
