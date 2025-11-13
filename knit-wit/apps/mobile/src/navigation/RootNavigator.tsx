import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { RootStackParamList } from '../types';
import MainTabNavigator from './MainTabNavigator';
import ParseScreen from '../screens/ParseScreen';
import { VisualizationScreen } from '../screens/VisualizationScreen';
import { ExportScreen } from '../screens/ExportScreen';

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
          component={ParseScreen}
          options={{
            headerShown: true,
            title: 'Parse Pattern',
          }}
        />
        <Stack.Screen
          name="Visualization"
          component={VisualizationScreen}
          options={{
            headerShown: true,
            title: 'Pattern Visualization',
          }}
        />
        <Stack.Screen
          name="Export"
          component={ExportScreen}
          options={{
            headerShown: true,
            title: 'Export Pattern',
          }}
        />
        {/* Future screens can be added here */}
        {/* <Stack.Screen name="PatternDetail" component={PatternDetailScreen} /> */}
        {/* <Stack.Screen name="Onboarding" component={OnboardingScreen} /> */}
      </Stack.Navigator>
    </NavigationContainer>
  );
}
