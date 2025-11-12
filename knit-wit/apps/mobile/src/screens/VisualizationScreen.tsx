import React, { useEffect, useState } from 'react';
import { View, StyleSheet, Text } from 'react-native';
import { SVGRenderer } from '../components/visualization/SVGRenderer';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { NetworkError } from '../components/common/NetworkError';
import { useVisualizationStore } from '../stores/useVisualizationStore';
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
    // TODO: Show tooltip in B6
  };

  if (loading) {
    return (
      <View style={styles.centerContainer}>
        <LoadingSpinner size="large" message="Generating visualization..." />
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.centerContainer}>
        <NetworkError message={error} onRetry={loadVisualization} />
      </View>
    );
  }

  const currentFrame = frames[currentRound - 1]; // Convert 1-indexed to 0-indexed

  if (!currentFrame) {
    return (
      <View style={styles.centerContainer}>
        <Text style={styles.noDataText}>No visualization data available</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.renderContainer}>
        <SVGRenderer
          frame={currentFrame}
          onStitchTap={handleStitchTap}
        />
      </View>

      {/* RoundScrubber will be added in B4 */}
      {/* Legend will be added in B7 */}
      {/* StitchTooltip will be added in B6 */}
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
