import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { colors } from '../../theme/colors';
import { typography } from '../../theme/typography';
import { spacing } from '../../theme/spacing';
import { borderRadius } from '../../theme/spacing';
import type { PaperSize } from '../../services/exportService';

interface PaperSizeOption {
  size: PaperSize;
  label: string;
  dimensions: string;
}

interface PaperSizeSelectorProps {
  selectedSize: PaperSize;
  onSelectSize: (size: PaperSize) => void;
}

const PAPER_SIZE_OPTIONS: PaperSizeOption[] = [
  {
    size: 'A4',
    label: 'A4',
    dimensions: '210 × 297 mm',
  },
  {
    size: 'letter',
    label: 'Letter',
    dimensions: '8.5 × 11 in',
  },
];

export const PaperSizeSelector: React.FC<PaperSizeSelectorProps> = ({
  selectedSize,
  onSelectSize,
}) => {
  return (
    <View style={styles.container}>
      <Text style={styles.label}>Paper Size</Text>
      <View style={styles.optionsRow}>
        {PAPER_SIZE_OPTIONS.map((option) => {
          const isSelected = selectedSize === option.size;

          return (
            <TouchableOpacity
              key={option.size}
              style={[
                styles.sizeButton,
                isSelected && styles.sizeButtonSelected,
              ]}
              onPress={() => onSelectSize(option.size)}
              accessible={true}
              accessibilityRole="radio"
              accessibilityState={{ selected: isSelected }}
              accessibilityLabel={`${option.label} paper size, ${option.dimensions}`}
              accessibilityHint={`Select ${option.label} paper size for PDF export`}
            >
              <View style={styles.radioOuter}>
                {isSelected && <View style={styles.radioInner} />}
              </View>
              <View style={styles.sizeInfo}>
                <Text
                  style={[
                    styles.sizeLabel,
                    isSelected && styles.sizeLabelSelected,
                  ]}
                >
                  {option.label}
                </Text>
                <Text style={styles.sizeDimensions}>{option.dimensions}</Text>
              </View>
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
  optionsRow: {
    flexDirection: 'row',
    gap: spacing.md,
  },
  sizeButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.surface,
    borderRadius: borderRadius.md,
    padding: spacing.md,
    borderWidth: 2,
    borderColor: colors.border,
    minHeight: 56, // Accessibility touch target
  },
  sizeButtonSelected: {
    borderColor: colors.primary,
    backgroundColor: colors.primaryLight + '10', // 10% opacity
  },
  radioOuter: {
    width: 24,
    height: 24,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: colors.gray400,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: spacing.sm,
  },
  radioInner: {
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: colors.primary,
  },
  sizeInfo: {
    flex: 1,
  },
  sizeLabel: {
    ...typography.bodyMedium,
    fontWeight: '600',
    color: colors.textPrimary,
  },
  sizeLabelSelected: {
    color: colors.primary,
  },
  sizeDimensions: {
    ...typography.bodySmall,
    color: colors.textSecondary,
    marginTop: 2,
  },
});
