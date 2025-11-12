// Custom Jest setup file
// Provides minimal setup for React Native testing

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
