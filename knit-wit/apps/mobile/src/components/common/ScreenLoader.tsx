import React from 'react';
import { View, ActivityIndicator, StyleSheet } from 'react-native';
import { colors } from '../../theme';

/**
 * ScreenLoader - Loading fallback for lazy-loaded screens
 *
 * Provides a centered loading indicator while screen components are being loaded.
 * Used as Suspense fallback for code-split routes.
 */
export function ScreenLoader() {
  return (
    <View style={styles.container}>
      <ActivityIndicator size="large" color={colors.primary} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: colors.background,
  },
});

export default ScreenLoader;
