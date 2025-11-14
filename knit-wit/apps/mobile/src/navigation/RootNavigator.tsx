import React, { Suspense, lazy } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { RootStackParamList } from '../types';
import { ScreenLoader } from '../components/common';
import MainTabNavigator from './MainTabNavigator';

// Code-split screens for reduced initial bundle size
// These screens are loaded on-demand when navigated to
const ParseScreen = lazy(() => import('../screens/ParseScreen'));
const VisualizationScreen = lazy(() =>
  import('../screens/VisualizationScreen').then(module => ({
    default: module.VisualizationScreen,
  }))
);
const ExportScreen = lazy(() =>
  import('../screens/ExportScreen').then(module => ({
    default: module.ExportScreen,
  }))
);

const Stack = createNativeStackNavigator<RootStackParamList>();

export default function RootNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        screenOptions={{
          headerShown: false,
        }}
      >
        <Stack.Screen name="Main" component={MainTabNavigator} />
        <Stack.Screen
          name="Parse"
          options={{
            headerShown: true,
            title: 'Parse Pattern',
          }}
        >
          {() => (
            <Suspense fallback={<ScreenLoader />}>
              <ParseScreen />
            </Suspense>
          )}
        </Stack.Screen>
        <Stack.Screen
          name="Visualization"
          options={{
            headerShown: true,
            title: 'Pattern Visualization',
          }}
        >
          {() => (
            <Suspense fallback={<ScreenLoader />}>
              <VisualizationScreen />
            </Suspense>
          )}
        </Stack.Screen>
        <Stack.Screen
          name="Export"
          options={{
            headerShown: true,
            title: 'Export Pattern',
          }}
        >
          {() => (
            <Suspense fallback={<ScreenLoader />}>
              <ExportScreen />
            </Suspense>
          )}
        </Stack.Screen>
        {/* Future screens can be added here */}
        {/* <Stack.Screen name="PatternDetail" component={PatternDetailScreen} /> */}
        {/* <Stack.Screen name="Onboarding" component={OnboardingScreen} /> */}
      </Stack.Navigator>
    </NavigationContainer>
  );
}
