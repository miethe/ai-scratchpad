/**
 * Accessibility Patterns - SVG Pattern Components
 *
 * React Native SVG components for rendering colorblind-accessible stitch patterns.
 * These patterns provide visual redundancy alongside color to ensure information
 * is conveyed through multiple channels.
 *
 * Usage:
 * ```tsx
 * import { AccessibilityPatternDefs, getPatternFill } from './AccessibilityPatterns';
 *
 * <Svg>
 *   <AccessibilityPatternDefs />
 *   <Circle fill={getPatternFill('increase', '#0072B2')} />
 * </Svg>
 * ```
 */

import React from 'react';
import { Defs, Pattern, Path, Rect } from 'react-native-svg';
import { stitchPatterns } from './accessibilityTheme';

/**
 * AccessibilityPatternDefs Component
 *
 * Renders all SVG pattern definitions needed for colorblind-accessible
 * stitch visualization. This component should be included once at the
 * root level of any SVG that uses accessibility patterns.
 *
 * @example
 * ```tsx
 * <Svg width={300} height={300}>
 *   <AccessibilityPatternDefs />
 *   <Circle cx={150} cy={150} r={50} fill="url(#diagonal-stripes)" />
 * </Svg>
 * ```
 */
export function AccessibilityPatternDefs() {
  return (
    <Defs>
      {/* Increase Pattern: Diagonal Stripes */}
      <Pattern
        id={stitchPatterns.increase.id}
        patternUnits="userSpaceOnUse"
        width={stitchPatterns.increase.patternSize}
        height={stitchPatterns.increase.patternSize}
      >
        <Path
          d={stitchPatterns.increase.svgPath}
          stroke="#000000"
          strokeWidth={stitchPatterns.increase.strokeWidth}
          strokeOpacity={0.3}
        />
      </Pattern>

      {/* Decrease Pattern: Crosshatch */}
      <Pattern
        id={stitchPatterns.decrease.id}
        patternUnits="userSpaceOnUse"
        width={stitchPatterns.decrease.patternSize}
        height={stitchPatterns.decrease.patternSize}
      >
        <Path
          d={stitchPatterns.decrease.svgPath}
          stroke="#000000"
          strokeWidth={stitchPatterns.decrease.strokeWidth}
          strokeOpacity={0.3}
        />
      </Pattern>

      {/* Additional pattern variations with color overlays */}
      {/* These allow patterns to be visible on different background colors */}

      {/* Light background variant: Increase */}
      <Pattern
        id="diagonal-stripes-light"
        patternUnits="userSpaceOnUse"
        width={8}
        height={8}
      >
        <Path
          d="M0,8 L8,0"
          stroke="#000000"
          strokeWidth={2}
          strokeOpacity={0.2}
        />
      </Pattern>

      {/* Light background variant: Decrease */}
      <Pattern
        id="hash-pattern-light"
        patternUnits="userSpaceOnUse"
        width={8}
        height={8}
      >
        <Path
          d="M0,0 L8,8 M8,0 L0,8"
          stroke="#000000"
          strokeWidth={1}
          strokeOpacity={0.2}
        />
      </Pattern>

      {/* Dark background variant: Increase */}
      <Pattern
        id="diagonal-stripes-dark"
        patternUnits="userSpaceOnUse"
        width={8}
        height={8}
      >
        <Path
          d="M0,8 L8,0"
          stroke="#FFFFFF"
          strokeWidth={2}
          strokeOpacity={0.4}
        />
      </Pattern>

      {/* Dark background variant: Decrease */}
      <Pattern
        id="hash-pattern-dark"
        patternUnits="userSpaceOnUse"
        width={8}
        height={8}
      >
        <Path
          d="M0,0 L8,8 M8,0 L0,8"
          stroke="#FFFFFF"
          strokeWidth={1}
          strokeOpacity={0.4}
        />
      </Pattern>
    </Defs>
  );
}

/**
 * Get Pattern Fill URL
 *
 * Returns the appropriate pattern fill URL for a given stitch type.
 * Handles both the pattern URL and solid fills.
 *
 * @param stitchType - Type of stitch: 'increase', 'decrease', or 'normal'
 * @param baseColor - Base color to use if no pattern (for normal stitches)
 * @param variant - Pattern variant: 'default', 'light', or 'dark' background
 * @returns Fill value for SVG fill attribute
 *
 * @example
 * ```tsx
 * <Circle fill={getPatternFill('increase', '#0072B2')} />
 * <Circle fill={getPatternFill('normal', '#999999')} />
 * <Circle fill={getPatternFill('increase', '#0072B2', 'dark')} />
 * ```
 */
export function getPatternFill(
  stitchType: 'increase' | 'decrease' | 'normal',
  baseColor: string,
  variant: 'default' | 'light' | 'dark' = 'default'
): string {
  if (stitchType === 'normal') {
    // Normal stitches use solid color, no pattern
    return baseColor;
  }

  const patternId = stitchType === 'increase' ? 'diagonal-stripes' : 'hash-pattern';

  // Apply variant suffix if specified
  const suffix = variant !== 'default' ? `-${variant}` : '';

  return `url(#${patternId}${suffix})`;
}

/**
 * Combined Pattern and Color Fill
 *
 * Creates a composite fill that combines a base color with a pattern overlay.
 * This is achieved by rendering the pattern with transparency over the base color.
 *
 * Note: React Native SVG doesn't support layered fills in the same way as web SVG,
 * so we need to use the pattern with semi-transparent strokes over the colored shape.
 *
 * @param stitchType - Type of stitch
 * @param baseColor - Base color for the shape
 * @param isDarkMode - Whether the visualization is in dark mode
 * @returns Object with fill properties
 *
 * @example
 * ```tsx
 * const fillProps = getCombinedFill('increase', '#0072B2', false);
 * <Circle fill={fillProps.color} />
 * // Pattern is rendered via the AccessibilityPatternDefs component
 * ```
 */
export function getCombinedFill(
  stitchType: 'increase' | 'decrease' | 'normal',
  baseColor: string,
  isDarkMode: boolean = false
) {
  const variant = isDarkMode ? 'dark' : 'light';

  return {
    color: baseColor,
    pattern: getPatternFill(stitchType, baseColor, variant),
    hasPattern: stitchType !== 'normal',
  };
}

/**
 * Pattern Overlay Component
 *
 * Renders a pattern overlay on top of a colored shape.
 * This component is useful when you need to apply patterns to complex shapes
 * that can't use simple fill URLs.
 *
 * @example
 * ```tsx
 * <Svg>
 *   <AccessibilityPatternDefs />
 *   <Circle cx={50} cy={50} r={30} fill="#0072B2" />
 *   <PatternOverlay
 *     stitchType="increase"
 *     shape="circle"
 *     cx={50}
 *     cy={50}
 *     r={30}
 *   />
 * </Svg>
 * ```
 */
interface PatternOverlayProps {
  stitchType: 'increase' | 'decrease' | 'normal';
  shape: 'circle' | 'rect';
  isDarkMode?: boolean;
  // Circle props
  cx?: number;
  cy?: number;
  r?: number;
  // Rect props
  x?: number;
  y?: number;
  width?: number;
  height?: number;
}

export function PatternOverlay({
  stitchType,
  shape,
  isDarkMode = false,
  cx,
  cy,
  r,
  x,
  y,
  width,
  height,
}: PatternOverlayProps) {
  if (stitchType === 'normal') {
    // Normal stitches don't need pattern overlay
    return null;
  }

  const variant = isDarkMode ? 'dark' : 'light';
  const patternUrl = getPatternFill(stitchType, '#000000', variant);

  if (shape === 'circle' && cx !== undefined && cy !== undefined && r !== undefined) {
    return (
      <circle
        cx={cx}
        cy={cy}
        r={r}
        fill={patternUrl}
        pointerEvents="none"
      />
    );
  }

  if (shape === 'rect' && x !== undefined && y !== undefined && width !== undefined && height !== undefined) {
    return (
      <Rect
        x={x}
        y={y}
        width={width}
        height={height}
        fill={patternUrl}
        pointerEvents="none"
      />
    );
  }

  return null;
}

/**
 * Accessibility Legend Component
 *
 * Renders a legend showing all stitch types with their colors, patterns, and symbols.
 * This helps users understand the visualization without relying on color alone.
 *
 * @example
 * ```tsx
 * <AccessibilityLegend
 *   palette="protanopia"
 *   showSymbols={true}
 *   showPatterns={true}
 * />
 * ```
 */
interface AccessibilityLegendProps {
  palette: 'protanopia' | 'deuteranopia' | 'tritanopia' | 'highContrast';
  showSymbols?: boolean;
  showPatterns?: boolean;
  isDarkMode?: boolean;
}

// Note: This is a placeholder interface. The actual implementation would need
// to import colorblindPalettes and stitchSymbols from accessibilityTheme.ts
// and render them in a React Native View with appropriate styling.
export type { AccessibilityLegendProps };

/**
 * Usage Notes
 *
 * PERFORMANCE:
 * - Pattern definitions are lightweight and should be rendered once per SVG
 * - Patterns are reused across multiple elements without performance penalty
 * - For complex visualizations with hundreds of stitches, patterns are more
 *   efficient than rendering individual pattern elements
 *
 * ACCESSIBILITY:
 * - Always include AccessibilityPatternDefs when using patterns
 * - Provide aria-label or accessibilityLabel on parent SVG elements
 * - Consider including a text-based legend for screen reader users
 * - Test pattern visibility at target sizes (8×8 dp minimum)
 *
 * CUSTOMIZATION:
 * - Pattern opacity can be adjusted via strokeOpacity
 * - Pattern colors can be inverted for dark mode using variant props
 * - Custom patterns can be added by following the same structure
 *
 * TESTING:
 * - Verify patterns render correctly on both iOS and Android
 * - Test at various screen densities (1x, 2x, 3x)
 * - Validate pattern clarity when printed or exported as PDF
 * - Ensure patterns remain visible when shape is very small (< 10dp)
 */
