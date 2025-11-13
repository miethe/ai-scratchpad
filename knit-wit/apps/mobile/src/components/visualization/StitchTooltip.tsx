import React from 'react';
import { View, Text, StyleSheet, Modal, TouchableOpacity } from 'react-native';
import type { RenderNode } from '../../types/visualization';
import { colors } from '../../theme/colors';
import { spacing } from '../../theme/spacing';
import { typography } from '../../theme/typography';

interface StitchTooltipProps {
  visible: boolean;
  node: RenderNode | null;
  onClose: () => void;
}

export const StitchTooltip: React.FC<StitchTooltipProps> = ({
  visible,
  node,
  onClose,
}) => {
  if (!visible || !node) return null;

  const getStitchName = (type: string): string => {
    const names: Record<string, string> = {
      sc: 'Single Crochet',
      inc: 'Increase (2 sc in same stitch)',
      dec: 'Decrease (sc2tog)',
      hdc: 'Half Double Crochet',
      dc: 'Double Crochet',
    };
    return names[type] || type.toUpperCase();
  };

  const getHighlightBadge = (highlight: string) => {
    if (highlight === 'normal') return null;

    const badgeStyle = highlight === 'increase'
      ? styles.increaseBadge
      : styles.decreaseBadge;

    const badgeText = highlight === 'increase' ? 'Increase' : 'Decrease';

    return (
      <View
        style={[styles.badge, badgeStyle]}
        accessible={false}
      >
        <Text style={styles.badgeText}>{badgeText}</Text>
      </View>
    );
  };

  const stitchName = getStitchName(node.stitch_type);
  const highlightType = node.highlight === 'normal' ? '' : `, ${node.highlight}`;
  const modalLabel = `Stitch details: ${stitchName}${highlightType}. Stitch ID: ${node.id}`;

  return (
    <Modal
      visible={visible}
      transparent
      animationType="fade"
      onRequestClose={onClose}
      accessibilityViewIsModal
      accessible={true}
      accessibilityLabel={modalLabel}
    >
      <TouchableOpacity
        style={styles.overlay}
        activeOpacity={1}
        onPress={onClose}
        accessibilityRole="button"
        accessibilityLabel="Close stitch details"
        accessibilityHint="Tap anywhere to close this tooltip"
        accessible={true}
      >
        <View
          style={styles.tooltip}
          accessible={true}
          accessibilityRole="none"
          accessibilityLabel={modalLabel}
        >
          <View style={styles.header}>
            <Text
              style={styles.stitchType}
              accessible={true}
              accessibilityRole="text"
              accessibilityLabel={`Stitch type: ${node.stitch_type.toUpperCase()}`}
            >
              {node.stitch_type.toUpperCase()}
            </Text>
            {getHighlightBadge(node.highlight)}
          </View>

          <Text
            style={styles.stitchName}
            accessible={true}
            accessibilityRole="text"
          >
            {stitchName}
          </Text>

          <Text
            style={styles.nodeId}
            accessible={true}
            accessibilityRole="text"
            accessibilityLabel={`Stitch identifier: ${node.id}`}
          >
            {node.id}
          </Text>

          <View
            style={styles.positionContainer}
            accessible={true}
            accessibilityRole="text"
            accessibilityLabel={`Position: ${node.position[0].toFixed(1)}, ${node.position[1].toFixed(1)}`}
          >
            <Text style={styles.positionLabel}>Position:</Text>
            <Text style={styles.positionValue}>
              ({node.position[0].toFixed(1)}, {node.position[1].toFixed(1)})
            </Text>
          </View>
        </View>
      </TouchableOpacity>
    </Modal>
  );
};

const styles = StyleSheet.create({
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  tooltip: {
    backgroundColor: colors.white,
    borderRadius: 12,
    padding: spacing.lg,
    minWidth: 240,
    maxWidth: 320,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 8,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: spacing.xs,
  },
  stitchType: {
    fontSize: typography.sizes.xl,
    fontWeight: 'bold',
    color: colors.gray900,
    marginRight: spacing.sm,
  },
  badge: {
    paddingHorizontal: spacing.sm,
    paddingVertical: 4,
    borderRadius: 12,
  },
  increaseBadge: {
    backgroundColor: '#D1FAE5', // Light green
  },
  decreaseBadge: {
    backgroundColor: '#FEE2E2', // Light red
  },
  badgeText: {
    fontSize: typography.sizes.xs,
    fontWeight: '600',
    color: colors.gray700,
  },
  stitchName: {
    fontSize: typography.sizes.md,
    color: colors.gray600,
    marginBottom: spacing.sm,
  },
  nodeId: {
    fontSize: typography.sizes.sm,
    color: colors.gray400,
    marginBottom: spacing.md,
  },
  positionContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  positionLabel: {
    fontSize: typography.sizes.sm,
    color: colors.gray500,
    marginRight: spacing.xs,
  },
  positionValue: {
    fontSize: typography.sizes.sm,
    color: colors.gray700,
    fontFamily: 'monospace',
  },
});
