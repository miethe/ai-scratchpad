import React from 'react';
import { View, Text, StyleSheet, ScrollView, Switch, TouchableOpacity, AccessibilityInfo } from 'react-native';
import { MainTabScreenProps } from '../types';
import { colors, typography, spacing, shadows, touchTargets } from '../theme';
import { useSettingsStore } from '../stores/useSettingsStore';

type Props = MainTabScreenProps<'Settings'>;

export default function SettingsScreen({ navigation }: Props) {
  const {
    kidMode,
    darkMode,
    defaultUnits,
    defaultTerminology,
    setKidMode,
    setDarkMode,
    setDefaultUnits,
    setDefaultTerminology,
  } = useSettingsStore();

  const handleKidModeToggle = (value: boolean) => {
    setKidMode(value);
    AccessibilityInfo.announceForAccessibility(
      `Kid Mode ${value ? 'enabled' : 'disabled'}`
    );
  };

  const handleDarkModeToggle = (value: boolean) => {
    setDarkMode(value);
    AccessibilityInfo.announceForAccessibility(
      `Dark Mode ${value ? 'enabled' : 'disabled'}`
    );
  };

  const handleTerminologyToggle = (value: boolean) => {
    const newTerminology = value ? 'US' : 'UK';
    setDefaultTerminology(newTerminology);
    AccessibilityInfo.announceForAccessibility(
      `Terminology changed to ${newTerminology}`
    );
  };

  const handleUnitsToggle = (value: boolean) => {
    const newUnits = value ? 'cm' : 'in';
    setDefaultUnits(newUnits);
    AccessibilityInfo.announceForAccessibility(
      `Units changed to ${value ? 'metric centimeters' : 'imperial inches'}`
    );
  };

  return (
    <ScrollView
      style={styles.container}
      contentContainerStyle={styles.content}
      accessibilityLabel="Settings screen"
      accessible={true}
    >
      <View style={styles.header}>
        <Text style={styles.title} accessibilityRole="header">
          Settings
        </Text>
        <Text
          style={styles.subtitle}
          accessible={true}
          accessibilityRole="text"
        >
          Customize your Knit-Wit experience
        </Text>
      </View>

      <View style={styles.section}>
        <Text
          style={styles.sectionTitle}
          accessibilityRole="header"
          accessibilityLevel={2}
        >
          Appearance
        </Text>

        <SettingRow
          label="Kid Mode"
          description="Simplified UI with beginner-friendly language"
          value={kidMode}
          onValueChange={handleKidModeToggle}
          testID="kid-mode-toggle"
        />

        <SettingRow
          label="Dark Mode"
          description="Use dark theme throughout the app"
          value={darkMode}
          onValueChange={handleDarkModeToggle}
          testID="dark-mode-toggle"
        />
      </View>

      <View style={styles.section}>
        <Text
          style={styles.sectionTitle}
          accessibilityRole="header"
          accessibilityLevel={2}
        >
          Pattern Defaults
        </Text>

        <SettingRow
          label="US Terminology"
          description="Use US crochet terms (turn off for UK terms)"
          value={defaultTerminology === 'US'}
          onValueChange={handleTerminologyToggle}
          testID="us-terminology-toggle"
        />

        <SettingRow
          label="Metric Units (cm)"
          description="Use metric units (turn off for imperial/inches)"
          value={defaultUnits === 'cm'}
          onValueChange={handleUnitsToggle}
          testID="metric-units-toggle"
        />
      </View>

      <View style={styles.section}>
        <Text
          style={styles.sectionTitle}
          accessibilityRole="header"
          accessibilityLevel={2}
        >
          About
        </Text>

        <View
          style={styles.infoCard}
          accessible={true}
          accessibilityRole="text"
          accessibilityLabel="Version 1.0.0 MVP"
        >
          <Text style={styles.infoLabel}>Version</Text>
          <Text style={styles.infoValue}>1.0.0 (MVP)</Text>
        </View>

        <View
          style={styles.infoCard}
          accessible={true}
          accessibilityRole="text"
          accessibilityLabel="Build: Development"
        >
          <Text style={styles.infoLabel}>Build</Text>
          <Text style={styles.infoValue}>Development</Text>
        </View>

        <TouchableOpacity
          style={styles.linkButton}
          accessibilityRole="button"
          accessibilityLabel="View documentation"
          accessibilityHint="Opens documentation in browser"
          accessible={true}
        >
          <Text style={styles.linkButtonText}>Documentation</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.linkButton}
          accessibilityRole="button"
          accessibilityLabel="Report an issue"
          accessibilityHint="Opens issue tracker in browser"
          accessible={true}
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
  const stateLabel = value ? 'enabled' : 'disabled';
  const fullLabel = `${label}, ${stateLabel}. ${description}`;

  return (
    <View
      style={styles.settingRow}
      accessible={true}
      accessibilityRole="none"
      accessibilityLabel={fullLabel}
    >
      <View style={styles.settingText}>
        <Text
          style={[styles.settingLabel, disabled && styles.settingLabelDisabled]}
          accessible={false}
        >
          {label}
        </Text>
        <Text
          style={styles.settingDescription}
          accessible={false}
        >
          {description}
        </Text>
      </View>
      <Switch
        value={value}
        onValueChange={onValueChange}
        testID={testID}
        disabled={disabled}
        trackColor={{ false: colors.gray300, true: colors.primaryLight }}
        thumbColor={value ? colors.primary : colors.gray50}
        ios_backgroundColor={colors.gray300}
        accessibilityLabel={`${label} switch`}
        accessibilityHint={`Double tap to ${value ? 'disable' : 'enable'} ${label}`}
        accessibilityState={{ checked: value, disabled }}
        accessibilityRole="switch"
        accessible={true}
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
