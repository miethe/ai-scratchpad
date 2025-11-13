import React, { useEffect, useState } from 'react';
import { View, StyleSheet, Text } from 'react-native';
import { SVGRenderer } from '../components/visualization/SVGRenderer';
import { RoundScrubber } from '../components/visualization/RoundScrubber';
import { StitchTooltip } from '../components/visualization/StitchTooltip';
import { Legend } from '../components/visualization/Legend';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { NetworkError } from '../components/common/NetworkError';
import { useVisualizationStore } from '../stores/useVisualizationStore';
import { useSettingsStore } from '../stores/useSettingsStore';
import { patternApi } from '../services/api';
import type { PatternDSL } from '../types/pattern';
import { colors } from '../theme/colors';
import { typography } from '../theme/typography';
import { spacing } from '../theme/spacing';

interface VisualizationScreenProps {
  route: {
    params: {
      pattern: PatternDSL;
    };
  };
}

export const VisualizationScreen: React.FC<VisualizationScreenProps> = ({ route }) => {
  const { pattern } = route.params;
  const { kidMode } = useSettingsStore();

  const {
    frames,
    currentRound,
    loading,
    error,
    setFrames,
    setLoading,
    setError,
  } = useVisualizationStore();

  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  const [tooltipVisible, setTooltipVisible] = useState(false);

  useEffect(() => {
    loadVisualization();
  }, [pattern]);

  const loadVisualization = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await patternApi.visualize(pattern);
      setFrames(response.frames, response.shape_type);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to load visualization';
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  const handleStitchTap = (nodeId: string) => {
    setSelectedNodeId(nodeId);
    setTooltipVisible(true);
  };

  const handleCloseTooltip = () => {
    setTooltipVisible(false);
    setSelectedNodeId(null);
  };

  if (loading) {
    return (
      <View
        style={styles.centerContainer}
        importantForAccessibility="yes"
        accessibilityLiveRegion="polite"
      >
        <LoadingSpinner
          size="large"
          message={kidMode ? 'Drawing your pattern...' : 'Generating visualization...'}
        />
      </View>
    );
  }

  if (error) {
    return (
      <View
        style={styles.centerContainer}
        importantForAccessibility="yes"
        accessibilityLiveRegion="assertive"
      >
        <NetworkError message={error} onRetry={loadVisualization} />
      </View>
    );
  }

  const currentFrame = frames[currentRound - 1]; // Convert 1-indexed to 0-indexed

  const selectedNode = selectedNodeId
    ? currentFrame?.nodes.find(n => n.id === selectedNodeId) || null
    : null;

  if (!currentFrame) {
    return (
      <View style={styles.centerContainer}>
        <Text style={styles.noDataText}>
          {kidMode
            ? 'No picture to show right now'
            : 'No visualization data available'}
        </Text>
      </View>
    );
  }

  const roundLabel = kidMode ? 'Step' : 'Round';

  return (
    <View
      style={styles.container}
      accessibilityLabel={
        kidMode
          ? `Pattern steps view`
          : `Pattern visualization screen`
      }
    >
      <View
        style={styles.renderContainer}
        accessibilityLabel={
          kidMode
            ? `Picture of ${roundLabel} ${currentFrame.round_number}`
            : `Visualization of round ${currentFrame.round_number}`
        }
      >
        <SVGRenderer
          frame={currentFrame}
          onStitchTap={handleStitchTap}
        />
        <Legend />
      </View>

      <RoundScrubber />

      <StitchTooltip
        visible={tooltipVisible}
        node={selectedNode}
        onClose={handleCloseTooltip}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: colors.background,
  },
  renderContainer: {
    flex: 1,
    position: 'relative',
  },
  noDataText: {
    ...typography.bodyMedium,
    color: colors.textSecondary,
    textAlign: 'center',
    padding: spacing.xl,
  },
});
