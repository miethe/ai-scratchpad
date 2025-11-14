import React, { useMemo, useCallback, useEffect } from 'react';
import { View, StyleSheet, Dimensions, AccessibilityInfo } from 'react-native';
import Svg, { Circle, Line, G } from 'react-native-svg';
import type { VisualizationFrame, RenderNode } from '../../types/visualization';
import { debounce } from '../../utils/performance';

interface SVGRendererProps {
  frame: VisualizationFrame;
  width?: number;
  height?: number;
  onStitchTap?: (nodeId: string) => void;
}

/**
 * Calculate visible bounds for viewport culling
 * Returns a bounding box in SVG coordinate space
 */
const calculateVisibleBounds = (
  width: number,
  height: number,
  centerX: number,
  centerY: number,
  scale: number
) => {
  // Calculate the bounds in SVG coordinate space
  // Viewport dimensions in SVG coordinates
  const viewportWidth = width / scale;
  const viewportHeight = height / scale;

  // Add padding to ensure smooth edge transitions
  const padding = 50;

  return {
    minX: -viewportWidth / 2 - padding,
    maxX: viewportWidth / 2 + padding,
    minY: -viewportHeight / 2 - padding,
    maxY: viewportHeight / 2 + padding,
  };
};

/**
 * Check if a node is visible within the viewport bounds
 */
const isNodeVisible = (
  node: RenderNode,
  bounds: { minX: number; maxX: number; minY: number; maxY: number }
): boolean => {
  const [x, y] = node.position;
  return x >= bounds.minX && x <= bounds.maxX && y >= bounds.minY && y <= bounds.maxY;
};

/**
 * Determine level of detail based on scale factor
 * Returns detail level: 'minimal' | 'reduced' | 'full'
 */
const getLODLevel = (scale: number): 'minimal' | 'reduced' | 'full' => {
  if (scale < 0.5) return 'minimal';
  if (scale < 1.0) return 'reduced';
  return 'full';
};

/**
 * Get rendering parameters based on LOD level
 */
const getLODParams = (lodLevel: 'minimal' | 'reduced' | 'full') => {
  switch (lodLevel) {
    case 'minimal':
      return {
        nodeRadius: 4,
        nodeStroke: 0,
        nodeStrokeWidth: 0,
        edgeStrokeWidth: 0.5,
        showLabels: false,
      };
    case 'reduced':
      return {
        nodeRadius: 6,
        nodeStroke: '#FFFFFF',
        nodeStrokeWidth: 1,
        edgeStrokeWidth: 1,
        showLabels: false,
      };
    case 'full':
    default:
      return {
        nodeRadius: 8,
        nodeStroke: '#FFFFFF',
        nodeStrokeWidth: 2,
        edgeStrokeWidth: 1.5,
        showLabels: true,
      };
  }
};

export const SVGRenderer = React.memo<SVGRendererProps>(
  ({
    frame,
    width = Dimensions.get('window').width - 32,
    height = 400,
    onStitchTap,
  }) => {
    const centerX = width / 2;
    const centerY = height / 2;

    // Scale factor: backend uses radius=100, we scale to fit viewport
    // Leave 20% padding on each side
    const scale = Math.min(width, height) / 250;

    // Memoize color mapping function (prevents recreation on every render)
    const getStitchColor = useCallback((highlight: string): string => {
      switch (highlight) {
        case 'increase':
          return '#10B981'; // Green (WCAG AA compliant)
        case 'decrease':
          return '#EF4444'; // Red (WCAG AA compliant)
        default:
          return '#6B7280'; // Gray
      }
    }, []);

    // Create O(1) node lookup map instead of O(n) array.find()
    const nodeMap = useMemo(() => {
      return new Map(frame.nodes.map((n) => [n.id, n]));
    }, [frame.nodes]);

    // Memoized node lookup function
    const findNode = useCallback(
      (id: string) => nodeMap.get(id),
      [nodeMap]
    );

    // Debounce accessibility announcements to reduce overhead
    // Only announce after user stops navigating for 300ms
    const announceRoundChange = useMemo(
      () =>
        debounce((round: number, count: number) => {
          AccessibilityInfo.announceForAccessibility(
            `Round ${round}, ${count} stitches`
          );
        }, 300),
      []
    );

    useEffect(() => {
      if (frame) {
        announceRoundChange(frame.round_number, frame.stitch_count);
      }
    }, [frame.round_number, frame.stitch_count, announceRoundChange]);

    // Calculate viewport bounds for culling
    const visibleBounds = useMemo(
      () => calculateVisibleBounds(width, height, centerX, centerY, scale),
      [width, height, centerX, centerY, scale]
    );

    // Determine LOD level based on scale
    const lodLevel = useMemo(() => getLODLevel(scale), [scale]);
    const lodParams = useMemo(() => getLODParams(lodLevel), [lodLevel]);

    // Filter visible nodes (viewport culling)
    const visibleNodes = useMemo(
      () => frame.nodes.filter((node) => isNodeVisible(node, visibleBounds)),
      [frame.nodes, visibleBounds]
    );

    // Create a Set of visible node IDs for fast edge filtering
    const visibleNodeIds = useMemo(
      () => new Set(visibleNodes.map((n) => n.id)),
      [visibleNodes]
    );

    // Filter visible edges (only render if both source and target are visible)
    const visibleEdges = useMemo(
      () =>
        frame.edges.filter(
          (edge) =>
            visibleNodeIds.has(edge.source) && visibleNodeIds.has(edge.target)
        ),
      [frame.edges, visibleNodeIds]
    );

    // Memoize rendered edges with LOD
    const renderedEdges = useMemo(
      () =>
        visibleEdges.map((edge, idx) => {
          const source = findNode(edge.source);
          const target = findNode(edge.target);
          if (!source || !target) return null;

          return (
            <Line
              key={`edge-${idx}`}
              x1={source.position[0]}
              y1={source.position[1]}
              x2={target.position[0]}
              y2={target.position[1]}
              stroke="#D1D5DB"
              strokeWidth={lodParams.edgeStrokeWidth}
            />
          );
        }),
      [visibleEdges, findNode, lodParams.edgeStrokeWidth]
    );

    // Memoize rendered nodes with LOD
    const renderedNodes = useMemo(
      () =>
        visibleNodes.map((node) => {
          const highlightText =
            node.highlight === 'normal' ? 'normal' : node.highlight;
          const accessibilityLabel = `Stitch ${node.id}, ${node.stitch_type}, ${highlightText}`;

          return (
            <Circle
              key={node.id}
              cx={node.position[0]}
              cy={node.position[1]}
              r={lodParams.nodeRadius}
              fill={getStitchColor(node.highlight)}
              stroke={lodParams.nodeStroke}
              strokeWidth={lodParams.nodeStrokeWidth}
              onPress={() => onStitchTap?.(node.id)}
              // Accessibility
              accessibilityRole="button"
              accessibilityLabel={accessibilityLabel}
              accessibilityHint="Tap to view details"
            />
          );
        }),
      [
        visibleNodes,
        onStitchTap,
        getStitchColor,
        lodParams.nodeRadius,
        lodParams.nodeStroke,
        lodParams.nodeStrokeWidth,
      ]
    );

    return (
      <View style={styles.container}>
        <Svg width={width} height={height}>
          <G transform={`translate(${centerX}, ${centerY}) scale(${scale})`}>
            {/* Render edges first (behind nodes) */}
            {renderedEdges}

            {/* Render nodes (foreground) */}
            {renderedNodes}
          </G>
        </Svg>
      </View>
    );
  },
  (prevProps, nextProps) => {
    // Custom comparison: only re-render if frame round, dimensions, or tap handler changes
    // This prevents unnecessary re-renders when other state changes
    return (
      prevProps.frame.round_number === nextProps.frame.round_number &&
      prevProps.width === nextProps.width &&
      prevProps.height === nextProps.height &&
      prevProps.onStitchTap === nextProps.onStitchTap
    );
  }
);

SVGRenderer.displayName = 'SVGRenderer';

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
});
