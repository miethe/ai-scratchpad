const React = require('react');

// Don't use requireActual since it causes issues with native modules
// Instead, provide minimal mocks for what we need

const Platform = {
  OS: 'ios',
  select: (options) => {
    return options.ios || options.default;
  },
};

const StyleSheet = {
  create: (styles) => styles,
  flatten: (style) => {
    if (Array.isArray(style)) {
      return style.reduce((acc, s) => Object.assign(acc, StyleSheet.flatten(s)), {});
    }
    return style || {};
  },
};

const Dimensions = {
  get: jest.fn(() => ({ width: 375, height: 812 })),
  addEventListener: jest.fn(),
  removeEventListener: jest.fn(),
};

const AccessibilityInfo = {
  announceForAccessibility: jest.fn(),
  isReduceMotionEnabled: jest.fn(() => Promise.resolve(false)),
  isScreenReaderEnabled: jest.fn(() => Promise.resolve(false)),
  addEventListener: jest.fn(),
  removeEventListener: jest.fn(),
};

const View = 'View';
const Text = 'Text';
const TouchableOpacity = 'TouchableOpacity';
const ActivityIndicator = 'ActivityIndicator';
const Modal = 'Modal';
const ScrollView = 'ScrollView';
const Button = 'Button';
const Image = 'Image';
const TextInput = 'TextInput';

module.exports = {
  Platform,
  StyleSheet,
  Dimensions,
  AccessibilityInfo,
  View,
  Text,
  TouchableOpacity,
  ActivityIndicator,
  Modal,
  ScrollView,
  Button,
  Image,
  TextInput,
};
