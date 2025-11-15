import React from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ViewStyle,
} from 'react-native';
import { colors } from '../../theme/colors';
import { typography } from '../../theme/typography';
import { spacing } from '../../theme/spacing';
import { borderRadius } from '../../theme/spacing';
import { shadows } from '../../theme';
import type { ExportFormat } from '../../services/exportService';

interface FormatOption {
  format: ExportFormat;
  label: string;
  description: string;
  icon: string;
  available: boolean;
}

interface FormatSelectorProps {
  selectedFormat: ExportFormat | null;
  onSelectFormat: (format: ExportFormat) => void;
  estimatedSize?: string;
}

const FORMAT_OPTIONS: FormatOption[] = [
  {
    format: 'pdf',
    label: 'PDF Document',
    description: 'Print-ready pattern with instructions',
    icon: '📄',
    available: true,
  },
  {
    format: 'json',
    label: 'JSON Data',
    description: 'Machine-readable pattern format',
    icon: '{ }',
    available: true,
  },
  {
    format: 'svg',
    label: 'SVG Image',
    description: 'Scalable vector diagram',
    icon: '🖼️',
    available: true,
  },
  {
    format: 'png',
    label: 'PNG Image',
    description: 'Raster diagram for sharing',
    icon: '🖼️',
    available: true,
  },
];

export const FormatSelector: React.FC<FormatSelectorProps> = ({
  selectedFormat,
  onSelectFormat,
  estimatedSize,
}) => {
  return (
    <View style={styles.container}>
      <Text style={styles.label}>Export Format</Text>
      <View style={styles.optionsGrid}>
        {FORMAT_OPTIONS.map((option) => {
          const isSelected = selectedFormat === option.format;
          const isDisabled = !option.available;

          return (
            <TouchableOpacity
              key={option.format}
              style={[
                styles.formatCard,
                isSelected && styles.formatCardSelected,
                isDisabled && styles.formatCardDisabled,
              ]}
              onPress={() => !isDisabled && onSelectFormat(option.format)}
              disabled={isDisabled}
              accessible={true}
              accessibilityRole="radio"
              accessibilityState={{
                selected: isSelected,
                disabled: isDisabled,
              }}
              accessibilityLabel={`${option.label}. ${option.description}. ${
                isDisabled ? 'Not available yet' : ''
              }`}
              accessibilityHint={
                !isDisabled
                  ? `Select ${option.label} export format`
                  : undefined
              }
            >
              <View style={styles.formatHeader}>
                <Text
                  style={[
                    styles.formatIcon,
                    isDisabled && styles.formatIconDisabled,
                  ]}
                >
                  {option.icon}
                </Text>
                {isSelected && (
                  <View style={styles.checkmark}>
                    <Text style={styles.checkmarkText}>✓</Text>
                  </View>
                )}
              </View>
              <Text
                style={[
                  styles.formatLabel,
                  isSelected && styles.formatLabelSelected,
                  isDisabled && styles.formatLabelDisabled,
                ]}
              >
                {option.label}
              </Text>
              <Text
                style={[
                  styles.formatDescription,
                  isDisabled && styles.formatDescriptionDisabled,
                ]}
              >
                {option.description}
              </Text>
              {isDisabled && (
                <View style={styles.comingSoonBadge}>
                  <Text style={styles.comingSoonText}>Coming Soon</Text>
                </View>
              )}
              {isSelected && estimatedSize && !isDisabled && (
                <Text style={styles.estimatedSize}>≈ {estimatedSize}</Text>
              )}
            </TouchableOpacity>
          );
        })}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginBottom: spacing.lg,
  },
  label: {
    ...typography.bodyLarge,
    fontWeight: '600',
    color: colors.textPrimary,
    marginBottom: spacing.md,
  },
  optionsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.md,
  },
  formatCard: {
    flex: 1,
    minWidth: 150,
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.md,
    borderWidth: 2,
    borderColor: colors.border,
    ...shadows.sm,
  } as ViewStyle,
  formatCardSelected: {
    borderColor: colors.primary,
    backgroundColor: colors.primaryLight + '10', // 10% opacity
  },
  formatCardDisabled: {
    opacity: 0.5,
    backgroundColor: colors.gray100,
  },
  formatHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: spacing.sm,
  },
  formatIcon: {
    fontSize: 32,
  },
  formatIconDisabled: {
    opacity: 0.5,
  },
  checkmark: {
    width: 24,
    height: 24,
    borderRadius: 12,
    backgroundColor: colors.primary,
    justifyContent: 'center',
    alignItems: 'center',
  },
  checkmarkText: {
    color: colors.white,
    fontSize: 14,
    fontWeight: 'bold',
  },
  formatLabel: {
    ...typography.bodyMedium,
    fontWeight: '600',
    color: colors.textPrimary,
    marginBottom: spacing.xs,
  },
  formatLabelSelected: {
    color: colors.primary,
  },
  formatLabelDisabled: {
    color: colors.textTertiary,
  },
  formatDescription: {
    ...typography.bodySmall,
    color: colors.textSecondary,
    marginBottom: spacing.xs,
  },
  formatDescriptionDisabled: {
    color: colors.textTertiary,
  },
  comingSoonBadge: {
    backgroundColor: colors.warning + '20',
    borderRadius: borderRadius.sm,
    paddingHorizontal: spacing.xs,
    paddingVertical: 2,
    alignSelf: 'flex-start',
    marginTop: spacing.xs,
  },
  comingSoonText: {
    ...typography.labelSmall,
    color: colors.warning,
    fontWeight: '600',
  },
  estimatedSize: {
    ...typography.bodySmall,
    color: colors.textSecondary,
    marginTop: spacing.xs,
    fontStyle: 'italic',
  },
});
