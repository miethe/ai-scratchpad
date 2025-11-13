import React from 'react';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { RootNavigator } from './src/navigation';
import { ThemeProvider } from './src/theme';
import { ConsentPrompt } from './src/components/telemetry/ConsentPrompt';

export default function App() {
  return (
    <SafeAreaProvider>
      <ThemeProvider>
        <ConsentPrompt />
        <RootNavigator />
        <StatusBar style="auto" />
      </ThemeProvider>
    </SafeAreaProvider>
  );
}
