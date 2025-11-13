import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { colors } from '../../theme/colors';
import { spacing } from '../../theme/spacing';
import { typography } from '../../theme/typography';

export const Legend: React.FC = () => {
  const legendItems = [
    { color: colors.success, label: 'Increase', description: '2 sc in same stitch' },
    { color: colors.error, label: 'Decrease', description: 'sc2tog' },
    { color: colors.gray500, label: 'Normal', description: 'Regular stitch' },
  ];

  return (
    <View
      style={styles.container}
      accessible={true}
      accessibilityRole="none"
      accessibilityLabel="Stitch type legend"
    >
      <Text
        style={styles.title}
        accessibilityRole="header"
        accessibilityLevel={3}
      >
        Legend
      </Text>
      {legendItems.map((item, index) => (
        <View
          key={index}
          style={styles.item}
          accessible={true}
          accessibilityRole="text"
          accessibilityLabel={`${item.label}: ${item.description}`}
        >
          <View
            style={[styles.colorBox, { backgroundColor: item.color }]}
            accessible={false}
          />
          <View style={styles.textContainer}>
            <Text style={styles.label}>{item.label}</Text>
            <Text style={styles.description}>{item.description}</Text>
          </View>
        </View>
      ))}
    </View>
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
  title: {
    fontSize: typography.sizes.md,
    fontWeight: 'bold',
    color: colors.gray900,
    marginBottom: spacing.sm,
  },
  item: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: spacing.xs,
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
  description: {
    fontSize: typography.sizes.xs,
    color: colors.gray600,
  },
});
