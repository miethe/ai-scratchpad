import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  TextInput,
  Alert,
} from 'react-native';
import { MainTabScreenProps } from '../types';
import type { ShapeType, Units, Terminology } from '../types';
import { colors, typography, spacing, shadows, touchTargets } from '../theme';

type Props = MainTabScreenProps<'Generate'>;

export default function GenerateScreen({ navigation }: Props) {
  const [shape, setShape] = useState<ShapeType>('sphere');
  const [diameter, setDiameter] = useState('10');
  const [height, setHeight] = useState('15');
  const [units, setUnits] = useState<Units>('cm');
  const [terminology, setTerminology] = useState<Terminology>('US');

  const handleGenerate = () => {
    // Placeholder for pattern generation
    // This will be connected to the API in later phases
    Alert.alert(
      'Pattern Generation',
      `Generating ${shape} pattern with diameter ${diameter}${units}`,
      [{ text: 'OK' }]
    );
  };

  return (
    <ScrollView
      style={styles.container}
      contentContainerStyle={styles.content}
      accessibilityLabel="Pattern generator screen"
    >
      <View style={styles.header}>
        <Text style={styles.title} accessibilityRole="header">
          Generate Pattern
        </Text>
        <Text style={styles.subtitle}>Configure your crochet pattern parameters</Text>
      </View>

      <View style={styles.form}>
        {/* Shape Selection */}
        <View style={styles.formSection}>
          <Text style={styles.label}>Shape</Text>
          <View style={styles.buttonGroup}>
            {(['sphere', 'cylinder', 'cone'] as ShapeType[]).map((s) => (
              <TouchableOpacity
                key={s}
                style={[styles.button, shape === s && styles.buttonActive]}
                onPress={() => setShape(s)}
                accessibilityRole="button"
                accessibilityLabel={`Select ${s} shape`}
                accessibilityState={{ selected: shape === s }}
              >
                <Text style={[styles.buttonText, shape === s && styles.buttonTextActive]}>
                  {s.charAt(0).toUpperCase() + s.slice(1)}
                </Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        {/* Diameter Input */}
        <View style={styles.formSection}>
          <Text style={styles.label}>Diameter</Text>
          <View style={styles.inputRow}>
            <TextInput
              style={styles.input}
              value={diameter}
              onChangeText={setDiameter}
              keyboardType="decimal-pad"
              placeholder="10"
              accessibilityLabel="Diameter input"
              accessibilityHint="Enter the diameter for your pattern"
            />
            <View style={styles.unitToggle}>
              {(['cm', 'in'] as Units[]).map((u) => (
                <TouchableOpacity
                  key={u}
                  style={[styles.unitButton, units === u && styles.unitButtonActive]}
                  onPress={() => setUnits(u)}
                  accessibilityRole="button"
                  accessibilityLabel={`Set units to ${u}`}
                  accessibilityState={{ selected: units === u }}
                >
                  <Text style={[styles.unitText, units === u && styles.unitTextActive]}>{u}</Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>
        </View>

        {/* Height Input (for cylinder/cone) */}
        {(shape === 'cylinder' || shape === 'cone') && (
          <View style={styles.formSection}>
            <Text style={styles.label}>Height</Text>
            <View style={styles.inputRow}>
              <TextInput
                style={styles.input}
                value={height}
                onChangeText={setHeight}
                keyboardType="decimal-pad"
                placeholder="15"
                accessibilityLabel="Height input"
                accessibilityHint="Enter the height for your pattern"
              />
            </View>
          </View>
        )}

        {/* Terminology Toggle */}
        <View style={styles.formSection}>
          <Text style={styles.label}>Crochet Terminology</Text>
          <View style={styles.buttonGroup}>
            {(['US', 'UK'] as Terminology[]).map((term) => (
              <TouchableOpacity
                key={term}
                style={[styles.button, terminology === term && styles.buttonActive]}
                onPress={() => setTerminology(term)}
                accessibilityRole="button"
                accessibilityLabel={`Set terminology to ${term}`}
                accessibilityState={{ selected: terminology === term }}
              >
                <Text style={[styles.buttonText, terminology === term && styles.buttonTextActive]}>
                  {term}
                </Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        {/* Generate Button */}
        <TouchableOpacity
          style={styles.generateButton}
          onPress={handleGenerate}
          accessibilityRole="button"
          accessibilityLabel="Generate pattern"
          accessibilityHint="Creates a pattern with the specified parameters"
        >
          <Text style={styles.generateButtonText}>Generate Pattern</Text>
        </TouchableOpacity>
      </View>
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
  },
  header: {
    marginBottom: spacing.xl,
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
  form: {
    gap: spacing.lg,
  },
  formSection: {
    gap: spacing.sm,
  },
  label: {
    ...typography.titleMedium,
    color: colors.textPrimary,
  },
  buttonGroup: {
    flexDirection: 'row',
    gap: spacing.sm,
  },
  button: {
    flex: 1,
    paddingVertical: spacing.md,
    paddingHorizontal: spacing.md,
    backgroundColor: colors.surfaceSecondary,
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: touchTargets.minimum,
  },
  buttonActive: {
    backgroundColor: colors.primary,
  },
  buttonText: {
    ...typography.labelLarge,
    color: colors.textPrimary,
  },
  buttonTextActive: {
    color: colors.textInverse,
  },
  inputRow: {
    flexDirection: 'row',
    gap: spacing.sm,
  },
  input: {
    flex: 1,
    backgroundColor: colors.surface,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 8,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.md,
    ...typography.bodyLarge,
    color: colors.textPrimary,
    minHeight: touchTargets.minimum,
  },
  unitToggle: {
    flexDirection: 'row',
    backgroundColor: colors.surfaceSecondary,
    borderRadius: 8,
    overflow: 'hidden',
  },
  unitButton: {
    paddingVertical: spacing.md,
    paddingHorizontal: spacing.lg,
    minHeight: touchTargets.minimum,
    justifyContent: 'center',
  },
  unitButtonActive: {
    backgroundColor: colors.primary,
  },
  unitText: {
    ...typography.labelLarge,
    color: colors.textPrimary,
  },
  unitTextActive: {
    color: colors.textInverse,
  },
  generateButton: {
    backgroundColor: colors.primary,
    paddingVertical: spacing.md,
    paddingHorizontal: spacing.lg,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: touchTargets.comfortable,
    marginTop: spacing.md,
    ...shadows.md,
  },
  generateButtonText: {
    ...typography.titleLarge,
    color: colors.textInverse,
  },
});
