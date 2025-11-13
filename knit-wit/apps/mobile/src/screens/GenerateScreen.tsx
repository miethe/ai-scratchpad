import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  TextInput,
  Alert,
  AccessibilityInfo,
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

  const handleShapeChange = (newShape: ShapeType) => {
    setShape(newShape);
    AccessibilityInfo.announceForAccessibility(`Shape changed to ${newShape}`);
  };

  const handleUnitsChange = (newUnits: Units) => {
    setUnits(newUnits);
    AccessibilityInfo.announceForAccessibility(`Units changed to ${newUnits}`);
  };

  const handleTerminologyChange = (newTerminology: Terminology) => {
    setTerminology(newTerminology);
    AccessibilityInfo.announceForAccessibility(`Terminology changed to ${newTerminology}`);
  };

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
      accessible={true}
    >
      <View style={styles.header}>
        <Text style={styles.title} accessibilityRole="header">
          Generate Pattern
        </Text>
        <Text
          style={styles.subtitle}
          accessible={true}
          accessibilityRole="text"
        >
          Configure your crochet pattern parameters
        </Text>
      </View>

      <View style={styles.form}>
        {/* Shape Selection */}
        <View style={styles.formSection}>
          <Text
            style={styles.label}
            accessibilityRole="header"
            accessibilityLevel={2}
          >
            Shape
          </Text>
          <View
            style={styles.buttonGroup}
            accessible={true}
            accessibilityRole="radiogroup"
            accessibilityLabel="Shape selection"
          >
            {(['sphere', 'cylinder', 'cone'] as ShapeType[]).map((s) => (
              <TouchableOpacity
                key={s}
                style={[styles.button, shape === s && styles.buttonActive]}
                onPress={() => handleShapeChange(s)}
                accessibilityRole="radio"
                accessibilityLabel={`${s.charAt(0).toUpperCase() + s.slice(1)} shape`}
                accessibilityState={{ selected: shape === s, checked: shape === s }}
                accessibilityHint={`Select ${s} shape for pattern`}
                accessible={true}
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
          <Text
            style={styles.label}
            accessibilityRole="header"
            accessibilityLevel={2}
          >
            Diameter
          </Text>
          <View style={styles.inputRow}>
            <TextInput
              style={styles.input}
              value={diameter}
              onChangeText={setDiameter}
              keyboardType="decimal-pad"
              placeholder="10"
              accessibilityLabel="Diameter input"
              accessibilityHint="Enter the diameter for your pattern in centimeters or inches"
              accessibilityRole="none"
              accessible={true}
            />
            <View
              style={styles.unitToggle}
              accessible={true}
              accessibilityRole="radiogroup"
              accessibilityLabel="Unit selection"
            >
              {(['cm', 'in'] as Units[]).map((u) => (
                <TouchableOpacity
                  key={u}
                  style={[styles.unitButton, units === u && styles.unitButtonActive]}
                  onPress={() => handleUnitsChange(u)}
                  accessibilityRole="radio"
                  accessibilityLabel={`${u === 'cm' ? 'Centimeters' : 'Inches'}`}
                  accessibilityState={{ selected: units === u, checked: units === u }}
                  accessibilityHint={`Set units to ${u === 'cm' ? 'centimeters' : 'inches'}`}
                  accessible={true}
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
            <Text
              style={styles.label}
              accessibilityRole="header"
              accessibilityLevel={2}
            >
              Height
            </Text>
            <View style={styles.inputRow}>
              <TextInput
                style={styles.input}
                value={height}
                onChangeText={setHeight}
                keyboardType="decimal-pad"
                placeholder="15"
                accessibilityLabel="Height input"
                accessibilityHint={`Enter the height for your ${shape} pattern`}
                accessibilityRole="none"
                accessible={true}
              />
            </View>
          </View>
        )}

        {/* Terminology Toggle */}
        <View style={styles.formSection}>
          <Text
            style={styles.label}
            accessibilityRole="header"
            accessibilityLevel={2}
          >
            Crochet Terminology
          </Text>
          <View
            style={styles.buttonGroup}
            accessible={true}
            accessibilityRole="radiogroup"
            accessibilityLabel="Terminology selection"
          >
            {(['US', 'UK'] as Terminology[]).map((term) => (
              <TouchableOpacity
                key={term}
                style={[styles.button, terminology === term && styles.buttonActive]}
                onPress={() => handleTerminologyChange(term)}
                accessibilityRole="radio"
                accessibilityLabel={`${term} terminology`}
                accessibilityState={{ selected: terminology === term, checked: terminology === term }}
                accessibilityHint={`Use ${term} crochet terminology`}
                accessible={true}
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
          accessibilityHint="Creates a crochet pattern with the specified parameters and navigates to visualization"
          accessible={true}
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
