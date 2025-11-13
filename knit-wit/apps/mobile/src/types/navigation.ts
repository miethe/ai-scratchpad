import type { BottomTabScreenProps } from '@react-navigation/bottom-tabs';
import type { CompositeScreenProps, NavigatorScreenParams } from '@react-navigation/native';
import type { NativeStackScreenProps } from '@react-navigation/native-stack';
import type { PatternDSL } from './pattern';

/**
 * Root Stack Navigator params
 */
export type RootStackParamList = {
  Main: NavigatorScreenParams<MainTabParamList>;
  Parse: undefined;
  Visualization: { pattern: PatternDSL };
  Export: { pattern: PatternDSL };
  // Future screens like onboarding, pattern detail, etc.
  // PatternDetail: { patternId: string };
  // Onboarding: undefined;
};

/**
 * Main Tab Navigator params
 */
export type MainTabParamList = {
  Home: undefined;
  Generate: undefined;
  Settings: undefined;
};

/**
 * Root Stack screen props
 */
export type RootStackScreenProps<T extends keyof RootStackParamList> = NativeStackScreenProps<
  RootStackParamList,
  T
>;

/**
 * Main Tab screen props
 */
export type MainTabScreenProps<T extends keyof MainTabParamList> = CompositeScreenProps<
  BottomTabScreenProps<MainTabParamList, T>,
  RootStackScreenProps<keyof RootStackParamList>
>;

/**
 * Navigation prop type helper
 */
declare global {
  namespace ReactNavigation {
    interface RootParamList extends RootStackParamList {}
  }
}
