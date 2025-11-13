import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TextInput,
  TouchableOpacity,
  ActivityIndicator,
  Platform,
} from 'react-native';
import { RootStackScreenProps } from '../types';
import { colors, typography, spacing, shadows } from '../theme';
import { patternApi, ParserResponse } from '../services/api';
import type { PatternDSL } from '../types';

type Props = RootStackScreenProps<'Parse'>;

const EXAMPLE_PATTERN = `R1: MR 6 sc (6)
R2: inc x6 (12)
R3: [sc, inc] x6 (18)`;

interface ValidationState {
  isValidating: boolean;
  isValid: boolean | null;
  errors: Array<{ message: string; line?: number }>;
  parsedDSL: PatternDSL | null;
}

export default function ParseScreen({ navigation }: Props) {
  const [patternText, setPatternText] = useState('');
  const [validation, setValidation] = useState<ValidationState>({
    isValidating: false,
    isValid: null,
    errors: [],
    parsedDSL: null,
  });

  const handleValidate = async () => {
    if (!patternText.trim()) {
      setValidation({
        isValidating: false,
        isValid: false,
        errors: [{ message: 'Please enter a pattern to validate' }],
        parsedDSL: null,
      });
      return;
    }

    setValidation((prev) => ({ ...prev, isValidating: true }));

    try {
      const response: ParserResponse = await patternApi.parse(patternText);

      setValidation({
        isValidating: false,
        isValid: response.validation.valid,
        errors: response.validation.errors,
        parsedDSL: response.validation.valid ? response.dsl : null,
      });
    } catch (error: any) {
      const errorMessage =
        error.response?.data?.error?.message ||
        error.message ||
        'Failed to validate pattern. Please check your connection and try again.';

      setValidation({
        isValidating: false,
        isValid: false,
        errors: [{ message: errorMessage }],
        parsedDSL: null,
      });
    }
  };

  const handleVisualize = () => {
    if (validation.parsedDSL) {
      navigation.navigate('Visualization', { pattern: validation.parsedDSL });
    }
  };

  const renderValidationResult = () => {
    if (validation.isValid === null) {
      return null;
    }

    if (validation.isValid && validation.parsedDSL) {
      return (
        <View style={styles.successContainer}>
          <View style={styles.successHeader}>
            <View style={styles.successIcon}>
              <Text style={styles.successIconText}>✓</Text>
            </View>
            <Text style={styles.successTitle}>Pattern is valid!</Text>
          </View>

          <View style={styles.previewContainer}>
            <Text style={styles.previewTitle}>Pattern Preview:</Text>
            {validation.parsedDSL.rounds.slice(0, 3).map((round) => (
              <Text key={round.r} style={styles.previewText}>
                Round {round.r}: {round.stitches} stitches
              </Text>
            ))}
            {validation.parsedDSL.rounds.length > 3 && (
              <Text style={styles.previewMore}>
                ... and {validation.parsedDSL.rounds.length - 3} more rounds
              </Text>
            )}
          </View>
        </View>
      );
    }

    return (
      <View style={styles.errorContainer}>
        <View style={styles.errorHeader}>
          <View style={styles.errorIcon}>
            <Text style={styles.errorIconText}>✕</Text>
          </View>
          <Text style={styles.errorTitle}>Validation Errors</Text>
        </View>

        <View style={styles.errorList}>
          {validation.errors.map((error, index) => (
            <View key={index} style={styles.errorItem}>
              <Text style={styles.errorText}>
                {error.line ? `Line ${error.line}: ` : ''}
                {error.message}
              </Text>
            </View>
          ))}
        </View>
      </View>
    );
  };

  return (
    <ScrollView
      style={styles.container}
      contentContainerStyle={styles.content}
      keyboardShouldPersistTaps="handled"
      accessibilityLabel="Parse pattern screen"
    >
      <View style={styles.header}>
        <Text style={styles.title} accessibilityRole="header">
          Parse Pattern
        </Text>
        <Text style={styles.subtitle}>
          Paste your crochet pattern below to validate and visualize it.
        </Text>
      </View>

      <View style={styles.inputSection}>
        <Text style={styles.inputLabel}>Pattern Text</Text>
        <TextInput
          style={styles.textInput}
          value={patternText}
          onChangeText={setPatternText}
          placeholder={EXAMPLE_PATTERN}
          placeholderTextColor={colors.textTertiary}
          multiline
          textAlignVertical="top"
          accessibilityLabel="Pattern text input"
          accessibilityHint="Enter your crochet pattern here"
        />
      </View>

      <TouchableOpacity
        style={[
          styles.button,
          styles.validateButton,
          validation.isValidating && styles.buttonDisabled,
        ]}
        onPress={handleValidate}
        disabled={validation.isValidating}
        accessibilityRole="button"
        accessibilityLabel="Validate pattern"
        accessibilityHint="Check if the pattern is valid"
      >
        {validation.isValidating ? (
          <ActivityIndicator color={colors.white} />
        ) : (
          <Text style={styles.buttonText}>Validate Pattern</Text>
        )}
      </TouchableOpacity>

      {renderValidationResult()}

      {validation.isValid && validation.parsedDSL && (
        <TouchableOpacity
          style={[styles.button, styles.visualizeButton]}
          onPress={handleVisualize}
          accessibilityRole="button"
          accessibilityLabel="Visualize pattern"
          accessibilityHint="View the pattern visualization"
        >
          <Text style={styles.buttonText}>Visualize Pattern</Text>
        </TouchableOpacity>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  content: {
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.lg,
    paddingBottom: spacing.xl,
  },
  header: {
    marginBottom: spacing.lg,
  },
  title: {
    ...typography.displaySmall,
    color: colors.textPrimary,
    marginBottom: spacing.sm,
  },
  subtitle: {
    ...typography.bodyLarge,
    color: colors.textSecondary,
  },
  inputSection: {
    marginBottom: spacing.lg,
  },
  inputLabel: {
    ...typography.titleMedium,
    color: colors.textPrimary,
    marginBottom: spacing.sm,
  },
  textInput: {
    backgroundColor: colors.surface,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: colors.border,
    padding: spacing.md,
    minHeight: 200,
    ...typography.bodyMedium,
    fontFamily: Platform.OS === 'ios' ? 'Courier' : 'monospace',
    color: colors.textPrimary,
  },
  button: {
    backgroundColor: colors.primary,
    borderRadius: 8,
    paddingVertical: spacing.md,
    paddingHorizontal: spacing.lg,
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: 48,
    ...shadows.sm,
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  buttonText: {
    ...typography.titleMedium,
    color: colors.white,
  },
  validateButton: {
    marginBottom: spacing.lg,
  },
  visualizeButton: {
    backgroundColor: colors.secondary,
    marginTop: spacing.lg,
  },
  successContainer: {
    backgroundColor: colors.surface,
    borderRadius: 12,
    padding: spacing.lg,
    borderLeftWidth: 4,
    borderLeftColor: colors.success,
    ...shadows.md,
  },
  successHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: spacing.md,
  },
  successIcon: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: colors.success,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: spacing.sm,
  },
  successIconText: {
    color: colors.white,
    fontSize: 20,
    fontWeight: 'bold',
  },
  successTitle: {
    ...typography.titleLarge,
    color: colors.success,
  },
  previewContainer: {
    marginTop: spacing.sm,
  },
  previewTitle: {
    ...typography.titleMedium,
    color: colors.textPrimary,
    marginBottom: spacing.xs,
  },
  previewText: {
    ...typography.bodyMedium,
    color: colors.textSecondary,
    marginBottom: spacing.xs,
  },
  previewMore: {
    ...typography.bodySmall,
    color: colors.textTertiary,
    fontStyle: 'italic',
    marginTop: spacing.xs,
  },
  errorContainer: {
    backgroundColor: colors.surface,
    borderRadius: 12,
    padding: spacing.lg,
    borderLeftWidth: 4,
    borderLeftColor: colors.error,
    ...shadows.md,
  },
  errorHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: spacing.md,
  },
  errorIcon: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: colors.error,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: spacing.sm,
  },
  errorIconText: {
    color: colors.white,
    fontSize: 20,
    fontWeight: 'bold',
  },
  errorTitle: {
    ...typography.titleLarge,
    color: colors.error,
  },
  errorList: {
    gap: spacing.sm,
  },
  errorItem: {
    paddingLeft: spacing.sm,
  },
  errorText: {
    ...typography.bodyMedium,
    color: colors.textPrimary,
  },
});
