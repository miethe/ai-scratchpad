import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { colors } from '../../theme/colors';
import { spacing } from '../../theme/spacing';
import { typography } from '../../theme/typography';
import { useSettingsStore } from '../../stores/useSettingsStore';
import { AnimatedTooltip, type TooltipType } from '../kidmode/AnimatedTooltip';
import { kidModeTheme } from '../../theme/kidModeTheme';

export const Legend: React.FC = () => {
  const { kidMode } = useSettingsStore();
  const [tooltipVisible, setTooltipVisible] = useState(false);
  const [tooltipType, setTooltipType] = useState<TooltipType>('increase');

  const handleInfoPress = (type: TooltipType) => {
    setTooltipType(type);
    setTooltipVisible(true);
  };

  const legendItems = [
    {
      color: colors.success,
      label: kidMode ? 'Add Stitches' : 'Increase',
      description: kidMode ? 'Make it bigger' : '2 sc in same stitch',
      tooltipType: 'increase' as TooltipType,
    },
    {
      color: colors.error,
      label: kidMode ? 'Remove Stitches' : 'Decrease',
      description: kidMode ? 'Make it smaller' : 'sc2tog',
      tooltipType: 'decrease' as TooltipType,
    },
    {
      color: colors.gray500,
      label: kidMode ? 'Regular Stitch' : 'Normal',
      description: kidMode ? 'Keep same size' : 'Regular stitch',
      tooltipType: null,
    },
  ];

  return (
    <>
      <View
        style={[
          styles.container,
          kidMode && styles.containerKidMode,
        ]}
        accessible={true}
        accessibilityRole="none"
        accessibilityLabel={
          kidMode ? 'Stitch types guide' : 'Stitch type legend'
        }
      >
        <Text
          style={[
            styles.title,
            kidMode && styles.titleKidMode,
          ]}
          accessibilityRole="header"
          accessibilityLevel={3}
        >
          {kidMode ? 'Stitch Types' : 'Legend'}
        </Text>
        {legendItems.map((item, index) => (
          <View
            key={index}
            style={[
              styles.item,
              kidMode && styles.itemKidMode,
            ]}
            accessible={true}
            accessibilityRole="text"
            accessibilityLabel={`${item.label}: ${item.description}`}
          >
            <View
              style={[styles.colorBox, { backgroundColor: item.color }]}
              accessible={false}
            />
            <View style={styles.textContainer}>
              <Text
                style={[
                  styles.label,
                  kidMode && styles.labelKidMode,
                ]}
              >
                {item.label}
              </Text>
              <Text
                style={[
                  styles.description,
                  kidMode && styles.descriptionKidMode,
                ]}
              >
                {item.description}
              </Text>
            </View>
            {kidMode && item.tooltipType && (
              <TouchableOpacity
                style={styles.infoButton}
                onPress={() => handleInfoPress(item.tooltipType!)}
                accessible={true}
                accessibilityRole="button"
                accessibilityLabel={`Learn more about ${item.label}`}
                accessibilityHint="Shows an animation explaining this stitch type"
              >
                <Text style={styles.infoButtonText}>?</Text>
              </TouchableOpacity>
            )}
          </View>
        ))}
      </View>

      {kidMode && (
        <AnimatedTooltip
          visible={tooltipVisible}
          type={tooltipType}
          onClose={() => setTooltipVisible(false)}
        />
      )}
    </>
  );
};

const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    top: spacing.md,
    right: spacing.md,
    backgroundColor: colors.white,
    borderRadius: 8,
    padding: spacing.md,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
    minWidth: 180,
  },
  containerKidMode: {
    backgroundColor: kidModeTheme.colors.surface,
    borderRadius: kidModeTheme.borderRadius.lg,
    padding: kidModeTheme.spacing.md,
    borderWidth: 2,
    borderColor: kidModeTheme.colors.primary,
    minWidth: 220,
    ...kidModeTheme.shadows.lg,
  },
  title: {
    fontSize: typography.sizes.md,
    fontWeight: 'bold',
    color: colors.gray900,
    marginBottom: spacing.sm,
  },
  titleKidMode: {
    ...kidModeTheme.typography.titleLarge,
    color: kidModeTheme.colors.textPrimary,
    marginBottom: kidModeTheme.spacing.sm,
  },
  item: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: spacing.xs,
  },
  itemKidMode: {
    marginBottom: kidModeTheme.spacing.sm,
    minHeight: kidModeTheme.touchTargets.minimum,
  },
  colorBox: {
    width: 16,
    height: 16,
    borderRadius: 8,
    marginRight: spacing.sm,
    borderWidth: 1,
    borderColor: colors.white,
  },
  textContainer: {
    flex: 1,
  },
  label: {
    fontSize: typography.sizes.sm,
    fontWeight: '600',
    color: colors.gray800,
  },
  labelKidMode: {
    ...kidModeTheme.typography.bodyLarge,
    fontWeight: '600',
    color: kidModeTheme.colors.textPrimary,
  },
  description: {
    fontSize: typography.sizes.xs,
    color: colors.gray600,
  },
  descriptionKidMode: {
    ...kidModeTheme.typography.bodySmall,
    color: kidModeTheme.colors.textSecondary,
  },
  infoButton: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: kidModeTheme.colors.info,
    justifyContent: 'center',
    alignItems: 'center',
    marginLeft: kidModeTheme.spacing.xs,
    ...kidModeTheme.shadows.sm,
  },
  infoButtonText: {
    ...kidModeTheme.typography.titleMedium,
    color: kidModeTheme.colors.textInverse,
    fontWeight: '700',
  },
});
