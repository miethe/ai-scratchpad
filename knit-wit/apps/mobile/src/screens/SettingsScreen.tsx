import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, Switch, TouchableOpacity } from 'react-native';
import { MainTabScreenProps } from '../types';
import { colors, typography, spacing, shadows, touchTargets } from '../theme';

type Props = MainTabScreenProps<'Settings'>;

export default function SettingsScreen({ navigation }: Props) {
  const [kidMode, setKidMode] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [usTerminology, setUsTerminology] = useState(true);

  return (
    <ScrollView
      style={styles.container}
      contentContainerStyle={styles.content}
      accessibilityLabel="Settings screen"
    >
      <View style={styles.header}>
        <Text style={styles.title} accessibilityRole="header">
          Settings
        </Text>
        <Text style={styles.subtitle}>Customize your Knit-Wit experience</Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Appearance</Text>

        <SettingRow
          label="Kid Mode"
          description="Simplified UI with beginner-friendly language"
          value={kidMode}
          onValueChange={setKidMode}
          testID="kid-mode-toggle"
        />

        <SettingRow
          label="Dark Mode"
          description="Use dark theme throughout the app"
          value={darkMode}
          onValueChange={setDarkMode}
          testID="dark-mode-toggle"
          disabled
        />
        <Text style={styles.comingSoon}>Coming soon</Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Pattern Defaults</Text>

        <SettingRow
          label="US Terminology"
          description="Use US crochet terms (turn off for UK terms)"
          value={usTerminology}
          onValueChange={setUsTerminology}
          testID="us-terminology-toggle"
        />
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>About</Text>

        <View style={styles.infoCard}>
          <Text style={styles.infoLabel}>Version</Text>
          <Text style={styles.infoValue}>1.0.0 (MVP)</Text>
        </View>

        <View style={styles.infoCard}>
          <Text style={styles.infoLabel}>Build</Text>
          <Text style={styles.infoValue}>Development</Text>
        </View>

        <TouchableOpacity
          style={styles.linkButton}
          accessibilityRole="button"
          accessibilityLabel="View documentation"
          accessibilityHint="Opens documentation in browser"
        >
          <Text style={styles.linkButtonText}>Documentation</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.linkButton}
          accessibilityRole="button"
          accessibilityLabel="Report an issue"
          accessibilityHint="Opens issue tracker in browser"
        >
          <Text style={styles.linkButtonText}>Report an Issue</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}

interface SettingRowProps {
  label: string;
  description: string;
  value: boolean;
  onValueChange: (value: boolean) => void;
  testID?: string;
  disabled?: boolean;
}

function SettingRow({
  label,
  description,
  value,
  onValueChange,
  testID,
  disabled = false,
}: SettingRowProps) {
  return (
    <View style={styles.settingRow}>
      <View style={styles.settingText}>
        <Text style={[styles.settingLabel, disabled && styles.settingLabelDisabled]}>{label}</Text>
        <Text style={styles.settingDescription}>{description}</Text>
      </View>
      <Switch
        value={value}
        onValueChange={onValueChange}
        testID={testID}
        disabled={disabled}
        trackColor={{ false: colors.gray300, true: colors.primaryLight }}
        thumbColor={value ? colors.primary : colors.gray50}
        ios_backgroundColor={colors.gray300}
        accessibilityLabel={`${label} toggle`}
        accessibilityState={{ checked: value, disabled }}
      />
    </View>
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
  section: {
    marginBottom: spacing.xl,
  },
  sectionTitle: {
    ...typography.headlineSmall,
    color: colors.textPrimary,
    marginBottom: spacing.md,
  },
  settingRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: colors.surface,
    padding: spacing.md,
    borderRadius: 8,
    marginBottom: spacing.sm,
    minHeight: touchTargets.comfortable,
  },
  settingText: {
    flex: 1,
    marginRight: spacing.md,
  },
  settingLabel: {
    ...typography.titleMedium,
    color: colors.textPrimary,
    marginBottom: spacing.xs,
  },
  settingLabelDisabled: {
    color: colors.textTertiary,
  },
  settingDescription: {
    ...typography.bodySmall,
    color: colors.textSecondary,
  },
  comingSoon: {
    ...typography.labelSmall,
    color: colors.textTertiary,
    fontStyle: 'italic',
    marginTop: -spacing.xs,
    marginBottom: spacing.sm,
    paddingLeft: spacing.md,
  },
  infoCard: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: colors.surfaceSecondary,
    padding: spacing.md,
    borderRadius: 8,
    marginBottom: spacing.sm,
  },
  infoLabel: {
    ...typography.titleMedium,
    color: colors.textSecondary,
  },
  infoValue: {
    ...typography.bodyMedium,
    color: colors.textPrimary,
  },
  linkButton: {
    backgroundColor: colors.surface,
    padding: spacing.md,
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: spacing.sm,
    minHeight: touchTargets.minimum,
    ...shadows.sm,
  },
  linkButtonText: {
    ...typography.titleMedium,
    color: colors.primary,
  },
});
