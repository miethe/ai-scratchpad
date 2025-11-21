import React, { useMemo, useCallback, useEffect } from 'react';
import { View, StyleSheet, Dimensions, AccessibilityInfo } from 'react-native';
import Svg, { Circle, Line, G } from 'react-native-svg';
import type { VisualizationFrame, RenderNode } from '../../types/visualization';
import { debounce } from '../../utils/performance';

interface SVGRendererProps {
  frames: VisualizationFrame[];
  currentRound: number;
  width?: number;
  height?: number;
  onStitchTap?: (nodeId: string) => void;
}

/**
 * Apply isometric projection to 3D coordinates
 * Converts (x, y, z) to 2D screen coordinates using isometric projection
 */
const applyIsometricProjection = (
  x: number,
  y: number,
  z: number,
  angleDeg: number = 30
): [number, number] => {
  const angle = (angleDeg * Math.PI) / 180;

  // Isometric projection formula
  const screenX = (x - y) * Math.cos(angle);
  const screenY = (x + y) * Math.sin(angle) - z;

  return [screenX, screenY];
};

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
    frames,
    currentRound,
    width = Dimensions.get('window').width - 32,
    height = 400,
    onStitchTap,
  }) => {
    const centerX = width / 2;
    const centerY = height / 2;

    // Scale factor: backend uses radius=100, we scale to fit viewport
    // Leave 20% padding on each side
    const scale = Math.min(width, height) / 250;

    // Check if we have 3D data
    const has3DData = frames.length > 0 && frames[0].projection !== undefined;
    const projectionAngle = frames[0]?.projection?.angle_deg ?? 30;

    // Memoize color mapping function (prevents recreation on every render)
    const getStitchColor = useCallback((highlight: string, isCurrent: boolean): string => {
      const baseColor = (() => {
        switch (highlight) {
          case 'increase':
            return '#10B981'; // Green (WCAG AA compliant)
          case 'decrease':
            return '#EF4444'; // Red (WCAG AA compliant)
          default:
            return '#6B7280'; // Gray
        }
      })();

      // Slightly fade previous rounds (not current)
      return isCurrent ? baseColor : baseColor + 'CC'; // Add alpha for 80% opacity
    }, []);

    // Create O(1) node lookup map for all nodes across all frames
    const nodeMap = useMemo(() => {
      const map = new Map<string, { node: RenderNode; frameIndex: number }>();
      frames.forEach((frame, frameIndex) => {
        frame.nodes.forEach((node) => {
          map.set(node.id, { node, frameIndex });
        });
      });
      return map;
    }, [frames]);

    // Memoized node lookup function
    const findNode = useCallback(
      (id: string) => nodeMap.get(id)?.node,
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
      const currentFrame = frames[currentRound - 1];
      if (currentFrame) {
        announceRoundChange(currentFrame.round_number, currentFrame.stitch_count);
      }
    }, [currentRound, frames, announceRoundChange]);

    // Calculate viewport bounds for culling
    const visibleBounds = useMemo(
      () => calculateVisibleBounds(width, height, centerX, centerY, scale),
      [width, height, centerX, centerY, scale]
    );

    // Determine LOD level based on scale
    const lodLevel = useMemo(() => getLODLevel(scale), [scale]);
    const lodParams = useMemo(() => getLODParams(lodLevel), [lodLevel]);

    // Collect all nodes from cumulative frames with metadata
    const allNodesWithMeta = useMemo(() => {
      const nodesWithMeta: Array<{
        node: RenderNode;
        frameIndex: number;
        isCurrent: boolean;
        screenPosition: [number, number];
      }> = [];

      frames.forEach((frame, frameIndex) => {
        const isCurrent = frameIndex === currentRound - 1;

        frame.nodes.forEach((node) => {
          // Calculate screen position based on 3D or 2D coordinates
          let screenPosition: [number, number];

          if (has3DData && node.position_3d) {
            const [x3d, y3d, z3d] = node.position_3d;
            screenPosition = applyIsometricProjection(x3d, y3d, z3d, projectionAngle);
          } else {
            screenPosition = node.position;
          }

          nodesWithMeta.push({
            node,
            frameIndex,
            isCurrent,
            screenPosition,
          });
        });
      });

      // Sort by depth for proper layering (back to front)
      if (has3DData) {
        nodesWithMeta.sort((a, b) => {
          const depthA = a.node.depth_order ?? 0;
          const depthB = b.node.depth_order ?? 0;
          return depthA - depthB;
        });
      }

      return nodesWithMeta;
    }, [frames, currentRound, has3DData, projectionAngle]);

    // Filter visible nodes (viewport culling)
    const visibleNodesWithMeta = useMemo(
      () => allNodesWithMeta.filter((nodeMeta) => {
        const [x, y] = nodeMeta.screenPosition;
        return x >= visibleBounds.minX && x <= visibleBounds.maxX &&
               y >= visibleBounds.minY && y <= visibleBounds.maxY;
      }),
      [allNodesWithMeta, visibleBounds]
    );

    // Create a Set of visible node IDs for fast edge filtering
    const visibleNodeIds = useMemo(
      () => new Set(visibleNodesWithMeta.map((nm) => nm.node.id)),
      [visibleNodesWithMeta]
    );

    // Collect all edges from cumulative frames
    const allEdges = useMemo(() => {
      return frames.flatMap(frame => frame.edges);
    }, [frames]);

    // Filter visible edges (only render if both source and target are visible)
    const visibleEdges = useMemo(
      () =>
        allEdges.filter(
          (edge) =>
            visibleNodeIds.has(edge.source) && visibleNodeIds.has(edge.target)
        ),
      [allEdges, visibleNodeIds]
    );

    // Memoize rendered edges with LOD
    const renderedEdges = useMemo(
      () =>
        visibleEdges.map((edge, idx) => {
          const sourceData = nodeMap.get(edge.source);
          const targetData = nodeMap.get(edge.target);
          if (!sourceData || !targetData) return null;

          const sourceNode = sourceData.node;
          const targetNode = targetData.node;

          // Calculate screen positions for source and target
          let sourcePos: [number, number];
          let targetPos: [number, number];

          if (has3DData && sourceNode.position_3d && targetNode.position_3d) {
            sourcePos = applyIsometricProjection(
              sourceNode.position_3d[0],
              sourceNode.position_3d[1],
              sourceNode.position_3d[2],
              projectionAngle
            );
            targetPos = applyIsometricProjection(
              targetNode.position_3d[0],
              targetNode.position_3d[1],
              targetNode.position_3d[2],
              projectionAngle
            );
          } else {
            sourcePos = sourceNode.position;
            targetPos = targetNode.position;
          }

          return (
            <Line
              key={`edge-${idx}`}
              x1={sourcePos[0]}
              y1={sourcePos[1]}
              x2={targetPos[0]}
              y2={targetPos[1]}
              stroke="#D1D5DB"
              strokeWidth={lodParams.edgeStrokeWidth}
              opacity={0.5}
            />
          );
        }),
      [visibleEdges, nodeMap, has3DData, projectionAngle, lodParams.edgeStrokeWidth]
    );

    // Memoize rendered nodes with LOD and depth cues
    const renderedNodes = useMemo(
      () =>
        visibleNodesWithMeta.map((nodeMeta) => {
          const { node, isCurrent, screenPosition } = nodeMeta;
          const [x, y] = screenPosition;

          const highlightText =
            node.highlight === 'normal' ? 'normal' : node.highlight;
          const accessibilityLabel = `Stitch ${node.id}, ${node.stitch_type}, ${highlightText}`;

          // Apply depth cues if 3D data is available
          let radius = lodParams.nodeRadius;
          let opacity = 1.0;

          if (has3DData && node.depth_factor !== undefined) {
            // Scale radius from 60% to 100% based on depth
            radius = lodParams.nodeRadius * (0.6 + 0.4 * node.depth_factor);
            // Scale opacity from 70% to 100% based on depth
            opacity = 0.7 + 0.3 * node.depth_factor;
          }

          // Further reduce opacity for non-current rounds
          if (!isCurrent) {
            opacity *= 0.8;
          }

          return (
            <Circle
              key={node.id}
              cx={x}
              cy={y}
              r={radius}
              fill={getStitchColor(node.highlight, isCurrent)}
              stroke={lodParams.nodeStroke}
              strokeWidth={lodParams.nodeStrokeWidth}
              opacity={opacity}
              onPress={() => onStitchTap?.(node.id)}
              // Accessibility
              accessibilityRole="button"
              accessibilityLabel={accessibilityLabel}
              accessibilityHint="Tap to view details"
            />
          );
        }),
      [
        visibleNodesWithMeta,
        onStitchTap,
        getStitchColor,
        lodParams.nodeRadius,
        lodParams.nodeStroke,
        lodParams.nodeStrokeWidth,
        has3DData,
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
    // Custom comparison: only re-render if frames, current round, dimensions, or tap handler changes
    // This prevents unnecessary re-renders when other state changes
    return (
      prevProps.frames === nextProps.frames &&
      prevProps.currentRound === nextProps.currentRound &&
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
