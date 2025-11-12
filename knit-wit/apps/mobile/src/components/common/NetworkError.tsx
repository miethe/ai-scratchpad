import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { colors } from '../../theme/colors';
import { typography } from '../../theme/typography';
import { spacing, touchTargets, borderRadius } from '../../theme/spacing';

interface NetworkErrorProps {
  message?: string;
  onRetry?: () => void;
}

export const NetworkError: React.FC<NetworkErrorProps> = ({
  message = 'Network connection failed',
  onRetry,
}) => {
  return (
    <View style={styles.container}>
      <Text style={styles.icon} accessibilityRole="image" accessibilityLabel="Warning">
        ⚠️
      </Text>
      <Text style={styles.title}>Connection Error</Text>
      <Text style={styles.message} accessibilityRole="alert">
        {message}
      </Text>
      {onRetry && (
        <TouchableOpacity
          style={styles.button}
          onPress={onRetry}
          accessibilityRole="button"
          accessibilityLabel="Retry connection"
          accessibilityHint="Attempts to reconnect to the network"
        >
          <Text style={styles.buttonText}>Retry</Text>
        </TouchableOpacity>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: spacing.xl,
    backgroundColor: colors.background,
  },
  icon: {
    fontSize: 48,
    marginBottom: spacing.md,
  },
  title: {
    ...typography.headlineSmall,
    color: colors.textPrimary,
    marginBottom: spacing.sm,
    textAlign: 'center',
  },
  message: {
    ...typography.bodyMedium,
    color: colors.textSecondary,
    marginBottom: spacing.xl,
    textAlign: 'center',
    maxWidth: 300,
  },
  button: {
    minHeight: touchTargets.comfortable,
    minWidth: touchTargets.comfortable,
    paddingHorizontal: spacing.xl,
    paddingVertical: spacing.md,
    backgroundColor: colors.primary,
    borderRadius: borderRadius.md,
    justifyContent: 'center',
    alignItems: 'center',
  },
  buttonText: {
    ...typography.labelLarge,
    color: colors.white,
  },
});
