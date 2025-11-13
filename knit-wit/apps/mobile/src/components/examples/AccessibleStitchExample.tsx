/**
 * Accessible Stitch Visualization Example
 *
 * This example demonstrates how to use the colorblind-friendly palettes
 * with patterns and symbols to create fully accessible stitch visualizations.
 *
 * THIS IS AN EXAMPLE FILE - Not used in production, but provided as a
 * reference for developers implementing accessibility features.
 */

import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import Svg, { Circle, Text as SvgText } from 'react-native-svg';
import {
  colorblindPalettes,
  getStitchVisualization,
  AccessibilityPatternDefs,
  getPatternFill,
  type AccessibilityPalettes,
} from '../../theme';

/**
 * Example 1: Simple Stitch Circle
 *
 * Basic example showing a single stitch with color, pattern, and symbol.
 */
export function SimpleStitchExample() {
  const { color, pattern, symbol, description } = getStitchVisualization(
    'increase',
    'protanopia'
  );

  return (
    <Svg width={100} height={100} accessibilityLabel="Increase stitch example">
      <AccessibilityPatternDefs />

      {/* Base circle with color */}
      <Circle
        cx={50}
        cy={50}
        r={30}
        fill={color}
        accessibilityLabel={description}
      />

      {/* Pattern overlay (rendered via pattern defs) */}
      {/* Pattern is applied via fill in production code */}

      {/* Symbol overlay */}
      <SvgText
        x={50}
        y={50}
        fontSize={20}
        textAnchor="middle"
        alignmentBaseline="central"
        fill="#000"
        fontWeight="bold"
      >
        {symbol}
      </SvgText>
    </Svg>
  );
}

/**
 * Example 2: Multiple Stitches in a Row
 *
 * Shows how to render multiple stitches with different types in sequence.
 */
interface StitchRowProps {
  stitches: Array<'increase' | 'decrease' | 'normal'>;
  paletteType?: keyof AccessibilityPalettes;
}

export function StitchRowExample({ stitches, paletteType = 'protanopia' }: StitchRowProps) {
  const stitchSize = 40;
  const spacing = 10;
  const svgWidth = stitches.length * (stitchSize + spacing);

  return (
    <Svg
      width={svgWidth}
      height={stitchSize + 20}
      accessibilityLabel={`Row of ${stitches.length} stitches`}
    >
      <AccessibilityPatternDefs />

      {stitches.map((stitchType, index) => {
        const { color, symbol, description } = getStitchVisualization(
          stitchType,
          paletteType
        );
        const x = index * (stitchSize + spacing) + stitchSize / 2;
        const y = stitchSize / 2;

        return (
          <React.Fragment key={index}>
            <Circle
              cx={x}
              cy={y}
              r={stitchSize / 2 - 2}
              fill={color}
              stroke="#000"
              strokeWidth={1}
              accessibilityLabel={description}
            />
            <SvgText
              x={x}
              y={y}
              fontSize={16}
              textAnchor="middle"
              alignmentBaseline="central"
              fill="#000"
              fontWeight="bold"
            >
              {symbol}
            </SvgText>
          </React.Fragment>
        );
      })}
    </Svg>
  );
}

/**
 * Example 3: Palette Comparison
 *
 * Shows all palettes side-by-side for comparison and testing.
 */
export function PaletteComparisonExample() {
  const palettes: Array<keyof AccessibilityPalettes> = [
    'protanopia',
    'deuteranopia',
    'tritanopia',
    'highContrast',
  ];

  const stitchTypes: Array<'increase' | 'decrease' | 'normal'> = [
    'increase',
    'decrease',
    'normal',
  ];

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Colorblind Palette Comparison</Text>

      {palettes.map((paletteType) => (
        <View key={paletteType} style={styles.paletteSection}>
          <Text style={styles.paletteTitle}>
            {paletteType.charAt(0).toUpperCase() + paletteType.slice(1)}
          </Text>

          <View style={styles.stitchRow}>
            {stitchTypes.map((stitchType) => {
              const { color, symbol, description } = getStitchVisualization(
                stitchType,
                paletteType
              );

              return (
                <View key={stitchType} style={styles.stitchContainer}>
                  <Svg width={60} height={60}>
                    <AccessibilityPatternDefs />
                    <Circle
                      cx={30}
                      cy={30}
                      r={25}
                      fill={color}
                      accessibilityLabel={description}
                    />
                    <SvgText
                      x={30}
                      y={30}
                      fontSize={18}
                      textAnchor="middle"
                      alignmentBaseline="central"
                      fill="#000"
                      fontWeight="bold"
                    >
                      {symbol}
                    </SvgText>
                  </Svg>
                  <Text style={styles.stitchLabel}>{stitchType}</Text>
                </View>
              );
            })}
          </View>
        </View>
      ))}
    </View>
  );
}

/**
 * Example 4: With Pattern Overlay
 *
 * Demonstrates how to apply patterns to stitch visualizations.
 * NOTE: In production, patterns would be integrated into the fill property.
 */
export function StitchWithPatternExample() {
  const paletteType = 'protanopia';

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Stitches with Patterns</Text>

      <View style={styles.stitchRow}>
        {/* Increase with diagonal stripes */}
        <View style={styles.stitchContainer}>
          <Svg width={80} height={80}>
            <AccessibilityPatternDefs />
            <Circle
              cx={40}
              cy={40}
              r={35}
              fill={colorblindPalettes[paletteType].increase}
            />
            <Circle
              cx={40}
              cy={40}
              r={35}
              fill="url(#diagonal-stripes)"
            />
            <SvgText
              x={40}
              y={40}
              fontSize={24}
              textAnchor="middle"
              alignmentBaseline="central"
              fill="#000"
              fontWeight="bold"
            >
              ▲
            </SvgText>
          </Svg>
          <Text style={styles.stitchLabel}>Increase</Text>
        </View>

        {/* Decrease with crosshatch */}
        <View style={styles.stitchContainer}>
          <Svg width={80} height={80}>
            <AccessibilityPatternDefs />
            <Circle
              cx={40}
              cy={40}
              r={35}
              fill={colorblindPalettes[paletteType].decrease}
            />
            <Circle
              cx={40}
              cy={40}
              r={35}
              fill="url(#hash-pattern)"
            />
            <SvgText
              x={40}
              y={40}
              fontSize={24}
              textAnchor="middle"
              alignmentBaseline="central"
              fill="#000"
              fontWeight="bold"
            >
              ▼
            </SvgText>
          </Svg>
          <Text style={styles.stitchLabel}>Decrease</Text>
        </View>

        {/* Normal with solid fill */}
        <View style={styles.stitchContainer}>
          <Svg width={80} height={80}>
            <AccessibilityPatternDefs />
            <Circle
              cx={40}
              cy={40}
              r={35}
              fill={colorblindPalettes[paletteType].normal}
            />
            <SvgText
              x={40}
              y={40}
              fontSize={24}
              textAnchor="middle"
              alignmentBaseline="central"
              fill="#000"
              fontWeight="bold"
            >
              ●
            </SvgText>
          </Svg>
          <Text style={styles.stitchLabel}>Normal</Text>
        </View>
      </View>
    </View>
  );
}

/**
 * Example 5: Practical Crochet Round Visualization
 *
 * Shows how to use accessibility palettes in a realistic crochet round visualization.
 */
interface CrochetRoundProps {
  round: number;
  stitches: Array<'increase' | 'decrease' | 'normal'>;
  paletteType?: keyof AccessibilityPalettes;
}

export function CrochetRoundExample({
  round,
  stitches,
  paletteType = 'protanopia',
}: CrochetRoundProps) {
  const centerX = 150;
  const centerY = 150;
  const radius = 100;
  const stitchSize = 12;
  const angleStep = (2 * Math.PI) / stitches.length;

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Round {round}</Text>
      <Text style={styles.subtitle}>{stitches.length} stitches</Text>

      <Svg
        width={300}
        height={300}
        accessibilityLabel={`Round ${round} with ${stitches.length} stitches`}
      >
        <AccessibilityPatternDefs />

        {stitches.map((stitchType, index) => {
          const angle = index * angleStep - Math.PI / 2;
          const x = centerX + radius * Math.cos(angle);
          const y = centerY + radius * Math.sin(angle);

          const { color, symbol, description } = getStitchVisualization(
            stitchType,
            paletteType
          );

          return (
            <React.Fragment key={index}>
              <Circle
                cx={x}
                cy={y}
                r={stitchSize}
                fill={color}
                stroke="#000"
                strokeWidth={1}
                accessibilityLabel={description}
              />
              <SvgText
                x={x}
                y={y}
                fontSize={10}
                textAnchor="middle"
                alignmentBaseline="central"
                fill="#000"
                fontWeight="bold"
              >
                {symbol}
              </SvgText>
            </React.Fragment>
          );
        })}
      </Svg>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 16,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 14,
    color: '#666',
    marginBottom: 16,
  },
  paletteSection: {
    marginBottom: 24,
    padding: 12,
    backgroundColor: '#f5f5f5',
    borderRadius: 8,
  },
  paletteTitle: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 12,
  },
  stitchRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    flexWrap: 'wrap',
  },
  stitchContainer: {
    alignItems: 'center',
    marginHorizontal: 8,
    marginVertical: 8,
  },
  stitchLabel: {
    fontSize: 12,
    marginTop: 4,
    color: '#333',
  },
});

/**
 * Usage Examples in Documentation:
 *
 * 1. SIMPLE USAGE:
 * ```tsx
 * import { SimpleStitchExample } from './examples/AccessibleStitchExample';
 * <SimpleStitchExample />
 * ```
 *
 * 2. ROW OF STITCHES:
 * ```tsx
 * <StitchRowExample
 *   stitches={['normal', 'increase', 'normal', 'decrease', 'normal']}
 *   paletteType="protanopia"
 * />
 * ```
 *
 * 3. PALETTE COMPARISON:
 * ```tsx
 * <PaletteComparisonExample />
 * ```
 *
 * 4. CROCHET ROUND:
 * ```tsx
 * <CrochetRoundExample
 *   round={3}
 *   stitches={['normal', 'normal', 'increase', 'normal', 'normal', 'increase']}
 *   paletteType="tritanopia"
 * />
 * ```
 */

export default {
  SimpleStitchExample,
  StitchRowExample,
  PaletteComparisonExample,
  StitchWithPatternExample,
  CrochetRoundExample,
};
