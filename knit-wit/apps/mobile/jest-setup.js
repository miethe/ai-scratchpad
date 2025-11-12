// Custom Jest setup file
// Replaces problematic react-native/jest/setup.js

// Mock native modules if needed
global.__reanimatedWorkletInit = () => {};
