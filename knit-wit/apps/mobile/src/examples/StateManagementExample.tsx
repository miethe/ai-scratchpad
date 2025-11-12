/**
 * State Management Example
 *
 * This file demonstrates how to use Zustand stores in Knit-Wit components.
 * It shows best practices for subscribing to state, updating state, and
 * combining multiple stores.
 *
 * This is a reference implementation - not used in production but serves
 * as documentation for developers.
 */

import React from 'react';
import { View, Text, Button, Switch, StyleSheet } from 'react-native';
import { useSettingsStore, usePatternStore, useVisualizationStore } from '../stores';
import type { PatternRequest } from '../types';

/**
 * Example 1: Simple state subscription
 * Shows how to subscribe to a single value from a store
 */
export function SimpleExample() {
  const kidMode = useSettingsStore((state) => state.kidMode);
  const setKidMode = useSettingsStore((state) => state.setKidMode);

  return (
    <View style={styles.container}>
      <Text>Kid Mode: {kidMode ? 'ON' : 'OFF'}</Text>
      <Switch value={kidMode} onValueChange={setKidMode} />
    </View>
  );
}

/**
 * Example 2: Multiple state values
 * Shows how to subscribe to multiple values from a single store
 */
export function MultipleValuesExample() {
  const { kidMode, darkMode, setKidMode, setDarkMode } = useSettingsStore((state) => ({
    kidMode: state.kidMode,
    darkMode: state.darkMode,
    setKidMode: state.setKidMode,
    setDarkMode: state.setDarkMode,
  }));

  return (
    <View style={styles.container}>
      <View style={styles.row}>
        <Text>Kid Mode</Text>
        <Switch value={kidMode} onValueChange={setKidMode} />
      </View>
      <View style={styles.row}>
        <Text>Dark Mode</Text>
        <Switch value={darkMode} onValueChange={setDarkMode} />
      </View>
    </View>
  );
}

/**
 * Example 3: Async actions
 * Shows how to handle async state updates (pattern generation)
 */
export function AsyncExample() {
  const { currentPattern, isGenerating, error, generatePattern } = usePatternStore((state) => ({
    currentPattern: state.currentPattern,
    isGenerating: state.isGenerating,
    error: state.error,
    generatePattern: state.generatePattern,
  }));

  const handleGenerate = async () => {
    const request: PatternRequest = {
      shape: 'sphere',
      diameter: 10,
      units: 'cm',
      gauge: { sts_per_10cm: 14, rows_per_10cm: 16 },
      stitch: 'sc',
      terms: 'US',
    };

    await generatePattern(request);
  };

  return (
    <View style={styles.container}>
      <Button
        title={isGenerating ? 'Generating...' : 'Generate Pattern'}
        onPress={handleGenerate}
        disabled={isGenerating}
      />

      {error && <Text style={styles.error}>{error}</Text>}

      {currentPattern && (
        <View style={styles.result}>
          <Text>Pattern Type: {currentPattern.object.type}</Text>
          <Text>Rounds: {currentPattern.rounds.length}</Text>
          <Text>Yarn: {currentPattern.materials.yarn_weight}</Text>
        </View>
      )}
    </View>
  );
}

/**
 * Example 4: Visualization controls
 * Shows how to use the visualization store for interactive controls
 */
export function VisualizationControlsExample() {
  const {
    currentRound,
    totalRounds,
    zoomLevel,
    nextRound,
    prevRound,
    zoomIn,
    zoomOut,
    resetVisualization,
  } = useVisualizationStore((state) => ({
    currentRound: state.currentRound,
    totalRounds: state.totalRounds,
    zoomLevel: state.zoomLevel,
    nextRound: state.nextRound,
    prevRound: state.prevRound,
    zoomIn: state.zoomIn,
    zoomOut: state.zoomOut,
    resetVisualization: state.resetVisualization,
  }));

  return (
    <View style={styles.container}>
      <View style={styles.row}>
        <Button title="Previous" onPress={prevRound} disabled={currentRound === 1} />
        <Text>Round {currentRound}</Text>
        <Button title="Next" onPress={nextRound} disabled={currentRound === totalRounds} />
      </View>

      <View style={styles.row}>
        <Button title="-" onPress={zoomOut} />
        <Text>{Math.round(zoomLevel * 100)}%</Text>
        <Button title="+" onPress={zoomIn} />
      </View>

      <Button title="Reset View" onPress={resetVisualization} />
    </View>
  );
}

/**
 * Example 5: Combining multiple stores
 * Shows how to use settings from one store to influence actions in another
 */
export function CombinedStoresExample() {
  // Get default settings
  const defaultUnits = useSettingsStore((state) => state.defaultUnits);
  const defaultTerms = useSettingsStore((state) => state.defaultTerminology);

  // Get pattern actions
  const generatePattern = usePatternStore((state) => state.generatePattern);
  const isGenerating = usePatternStore((state) => state.isGenerating);

  const handleGenerate = async () => {
    const request: PatternRequest = {
      shape: 'sphere',
      diameter: 10,
      units: defaultUnits, // Use setting from SettingsStore
      gauge: { sts_per_10cm: 14, rows_per_10cm: 16 },
      stitch: 'sc',
      terms: defaultTerms, // Use setting from SettingsStore
    };

    await generatePattern(request);
  };

  return (
    <View style={styles.container}>
      <Text>Using settings: {defaultUnits}, {defaultTerms}</Text>
      <Button
        title={isGenerating ? 'Generating...' : 'Generate with Defaults'}
        onPress={handleGenerate}
        disabled={isGenerating}
      />
    </View>
  );
}

/**
 * Example 6: Display preferences
 * Shows how to use visualization display preferences
 */
export function DisplayPreferencesExample() {
  const {
    highlightChanges,
    showStitchCount,
    showRoundNumbers,
    setHighlightChanges,
    setShowStitchCount,
    setShowRoundNumbers,
  } = useVisualizationStore((state) => ({
    highlightChanges: state.highlightChanges,
    showStitchCount: state.showStitchCount,
    showRoundNumbers: state.showRoundNumbers,
    setHighlightChanges: state.setHighlightChanges,
    setShowStitchCount: state.setShowStitchCount,
    setShowRoundNumbers: state.setShowRoundNumbers,
  }));

  return (
    <View style={styles.container}>
      <View style={styles.row}>
        <Text>Highlight Changes</Text>
        <Switch value={highlightChanges} onValueChange={setHighlightChanges} />
      </View>
      <View style={styles.row}>
        <Text>Show Stitch Count</Text>
        <Switch value={showStitchCount} onValueChange={setShowStitchCount} />
      </View>
      <View style={styles.row}>
        <Text>Show Round Numbers</Text>
        <Switch value={showRoundNumbers} onValueChange={setShowRoundNumbers} />
      </View>
    </View>
  );
}

/**
 * Example 7: Accessing state outside components
 * Shows how to get state in utility functions or event handlers
 */
export function exportCurrentPattern() {
  // Access store outside of React components
  const { currentPattern } = usePatternStore.getState();

  if (!currentPattern) {
    throw new Error('No pattern to export');
  }

  // Export logic would go here
  console.log('Exporting pattern:', currentPattern.object.type);

  return currentPattern;
}

/**
 * Example 8: Batch updates for performance
 * Shows how to update multiple state values efficiently
 */
export function BatchUpdateExample() {
  const resetAll = () => {
    // Batch update multiple stores at once
    useSettingsStore.setState({
      kidMode: false,
      darkMode: false,
      defaultUnits: 'cm',
      defaultTerminology: 'US',
    });

    useVisualizationStore.setState({
      currentRound: 1,
      zoomLevel: 1.0,
      panOffset: { x: 0, y: 0 },
    });

    usePatternStore.setState({
      currentPattern: null,
      error: null,
    });
  };

  return (
    <View style={styles.container}>
      <Button title="Reset All Settings" onPress={resetAll} />
    </View>
  );
}

// Styles
const styles = StyleSheet.create({
  container: {
    padding: 16,
    gap: 12,
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 8,
  },
  error: {
    color: 'red',
    fontSize: 14,
  },
  result: {
    padding: 12,
    backgroundColor: '#f0f0f0',
    borderRadius: 8,
    gap: 4,
  },
});
