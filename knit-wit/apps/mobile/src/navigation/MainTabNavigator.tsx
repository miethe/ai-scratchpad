import React, { Suspense, lazy } from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Platform } from 'react-native';
import { MainTabParamList } from '../types';
import { colors, typography } from '../theme';
import { ScreenLoader } from '../components/common';

// Code-split tab screens for reduced initial bundle size
// Home screen is loaded eagerly as it's the initial route
import HomeScreen from '../screens/HomeScreen';

// Generate and Settings screens are lazy-loaded
const GenerateScreen = lazy(() => import('../screens/GenerateScreen'));
const SettingsScreen = lazy(() => import('../screens/SettingsScreen'));

const Tab = createBottomTabNavigator<MainTabParamList>();

export default function MainTabNavigator() {
  return (
    <Tab.Navigator
      screenOptions={{
        headerShown: true,
        tabBarActiveTintColor: colors.primary,
        tabBarInactiveTintColor: colors.gray500,
        tabBarStyle: {
          backgroundColor: colors.surface,
          borderTopColor: colors.border,
          borderTopWidth: 1,
          paddingBottom: Platform.OS === 'ios' ? 20 : 8,
          paddingTop: 8,
          height: Platform.OS === 'ios' ? 88 : 64,
        },
        tabBarLabelStyle: {
          ...typography.labelMedium,
        },
        headerStyle: {
          backgroundColor: colors.surface,
          elevation: 2,
          shadowOpacity: 0.1,
        },
        headerTitleStyle: {
          ...typography.titleLarge,
          color: colors.textPrimary,
        },
      }}
    >
      <Tab.Screen
        name="Home"
        component={HomeScreen}
        options={{
          title: 'Home',
          tabBarLabel: 'Home',
          tabBarAccessibilityLabel: 'Home tab',
          // Tab icons will be added when we integrate icon library
          // For now, React Navigation will show labels
        }}
      />
      <Tab.Screen
        name="Generate"
        options={{
          title: 'Generate',
          tabBarLabel: 'Generate',
          tabBarAccessibilityLabel: 'Generate pattern tab',
        }}
      >
        {() => (
          <Suspense fallback={<ScreenLoader />}>
            <GenerateScreen />
          </Suspense>
        )}
      </Tab.Screen>
      <Tab.Screen
        name="Settings"
        options={{
          title: 'Settings',
          tabBarLabel: 'Settings',
          tabBarAccessibilityLabel: 'Settings tab',
        }}
      >
        {() => (
          <Suspense fallback={<ScreenLoader />}>
            <SettingsScreen />
          </Suspense>
        )}
      </Tab.Screen>
    </Tab.Navigator>
  );
}
