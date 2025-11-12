import React from 'react';
import { View, StyleSheet, Dimensions } from 'react-native';
import Svg, { Circle, Line, G } from 'react-native-svg';
import type { VisualizationFrame } from '../../types/visualization';

interface SVGRendererProps {
  frame: VisualizationFrame;
  width?: number;
  height?: number;
  onStitchTap?: (nodeId: string) => void;
}

export const SVGRenderer = React.memo<SVGRendererProps>(({
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

  // Color mapping for stitch types
  const getStitchColor = (highlight: string): string => {
    switch (highlight) {
      case 'increase':
        return '#10B981'; // Green (WCAG AA compliant)
      case 'decrease':
        return '#EF4444'; // Red (WCAG AA compliant)
      default:
        return '#6B7280'; // Gray
    }
  };

  // Find node by ID for edge rendering
  const findNode = (id: string) => frame.nodes.find(n => n.id === id);

  return (
    <View style={styles.container}>
      <Svg width={width} height={height}>
        <G transform={`translate(${centerX}, ${centerY}) scale(${scale})`}>
          {/* Render edges first (behind nodes) */}
          {frame.edges.map((edge, idx) => {
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
                strokeWidth={1.5}
              />
            );
          })}

          {/* Render nodes (foreground) */}
          {frame.nodes.map((node) => (
            <Circle
              key={node.id}
              cx={node.position[0]}
              cy={node.position[1]}
              r={8}
              fill={getStitchColor(node.highlight)}
              stroke="#FFFFFF"
              strokeWidth={2}
              onPress={() => onStitchTap?.(node.id)}
              // Accessibility
              accessibilityLabel={`Stitch ${node.id}, type ${node.stitch_type}`}
            />
          ))}
        </G>
      </Svg>
    </View>
  );
});

SVGRenderer.displayName = 'SVGRenderer';

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
});
