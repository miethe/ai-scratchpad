/**
 * Stitch Animations for Kid Mode
 *
 * Visual animations that teach crochet concepts to young learners:
 * - Increase: Shows 1 stitch becoming 2 stitches
 * - Decrease: Shows 2 stitches becoming 1 stitch
 * - Magic Ring: Shows stitches forming a ring
 *
 * All animations respect prefers-reduced-motion accessibility setting.
 *
 * @see Story E3: Beginner Copy and Animations
 */

import React, { useEffect, useRef, useState } from 'react';
import { View, Animated, StyleSheet, AccessibilityInfo } from 'react-native';
import { kidModeTheme } from '../../../theme/kidModeTheme';

// ============================================================================
// StitchCircle Component
// ============================================================================

interface StitchCircleProps {
  /**
   * Color of the stitch circle
   */
  color: string;

  /**
   * Animated value for positioning
   */
  position?: Animated.ValueXY;

  /**
   * Animated value for scaling
   */
  scale?: Animated.Value;

  /**
   * Animated value for opacity
   */
  opacity?: Animated.Value;

  /**
   * Size of the circle in pixels
   * @default 24
   */
  size?: number;
}

/**
 * Individual stitch represented as a circle
 */
const StitchCircle: React.FC<StitchCircleProps> = ({
  color,
  position,
  scale,
  opacity,
  size = 24,
}) => {
  const animatedStyle = {
    width: size,
    height: size,
    borderRadius: size / 2,
    backgroundColor: color,
    transform: [
      ...(position ? [{ translateX: position.x }, { translateY: position.y }] : []),
      ...(scale ? [{ scale }] : []),
    ],
    opacity: opacity || 1,
  };

  return <Animated.View style={animatedStyle} accessible={false} />;
};

// ============================================================================
// IncreaseAnimation Component
// ============================================================================

export interface IncreaseAnimationProps {
  /**
   * Whether to reduce motion (accessibility)
   * @default false
   */
  reduceMotion?: boolean;

  /**
   * Size of stitches
   * @default 24
   */
  stitchSize?: number;
}

/**
 * Animation showing 1 stitch becoming 2 stitches
 *
 * Visual: Single circle splits and bounces into two circles
 * Duration: 1.5 seconds
 * Respects: prefers-reduced-motion
 */
export const IncreaseAnimation: React.FC<IncreaseAnimationProps> = ({
  reduceMotion = false,
  stitchSize = 24,
}) => {
  const position1 = useRef(new Animated.ValueXY({ x: 0, y: 0 })).current;
  const position2 = useRef(new Animated.ValueXY({ x: 0, y: 0 })).current;
  const scale1 = useRef(new Animated.Value(1)).current;
  const scale2 = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    if (reduceMotion) {
      // No animation - just show final state
      position1.setValue({ x: -20, y: 0 });
      position2.setValue({ x: 20, y: 0 });
      scale1.setValue(1);
      scale2.setValue(1);
      return;
    }

    // Start animation sequence
    const animate = () => {
      // Reset to initial state
      position1.setValue({ x: 0, y: 0 });
      position2.setValue({ x: 0, y: 0 });
      scale1.setValue(1);
      scale2.setValue(0);

      // Parallel animations
      Animated.sequence([
        // Step 1: First circle moves left and slightly grows (300ms)
        Animated.parallel([
          Animated.timing(position1, {
            toValue: { x: -20, y: 0 },
            duration: 300,
            useNativeDriver: true,
          }),
          Animated.timing(scale1, {
            toValue: 1.2,
            duration: 300,
            useNativeDriver: true,
          }),
        ]),
        // Step 2: Second circle appears with bounce (800ms)
        Animated.parallel([
          Animated.spring(position2, {
            toValue: { x: 20, y: 0 },
            friction: 5,
            tension: 40,
            useNativeDriver: true,
          }),
          Animated.spring(scale2, {
            toValue: 1,
            friction: 5,
            tension: 40,
            useNativeDriver: true,
          }),
          // First circle returns to normal size
          Animated.timing(scale1, {
            toValue: 1,
            duration: 300,
            useNativeDriver: true,
          }),
        ]),
        // Step 3: Brief pause (400ms)
        Animated.delay(400),
      ]).start(() => {
        // Loop animation
        animate();
      });
    };

    animate();
  }, [reduceMotion, position1, position2, scale1, scale2]);

  return (
    <View
      style={styles.animationContainer}
      accessibilityLabel="Increase animation showing one stitch becoming two stitches"
      accessible={true}
    >
      <StitchCircle
        color={kidModeTheme.colors.success}
        position={position1}
        scale={scale1}
        size={stitchSize}
      />
      <StitchCircle
        color={kidModeTheme.colors.success}
        position={position2}
        scale={scale2}
        size={stitchSize}
      />
    </View>
  );
};

// ============================================================================
// DecreaseAnimation Component
// ============================================================================

export interface DecreaseAnimationProps {
  /**
   * Whether to reduce motion (accessibility)
   * @default false
   */
  reduceMotion?: boolean;

  /**
   * Size of stitches
   * @default 24
   */
  stitchSize?: number;
}

/**
 * Animation showing 2 stitches becoming 1 stitch
 *
 * Visual: Two circles merge into one with shrink effect
 * Duration: 1.5 seconds
 * Respects: prefers-reduced-motion
 */
export const DecreaseAnimation: React.FC<DecreaseAnimationProps> = ({
  reduceMotion = false,
  stitchSize = 24,
}) => {
  const position1 = useRef(new Animated.ValueXY({ x: -20, y: 0 })).current;
  const position2 = useRef(new Animated.ValueXY({ x: 20, y: 0 })).current;
  const opacity2 = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    if (reduceMotion) {
      // No animation - just show final state
      position1.setValue({ x: 0, y: 0 });
      position2.setValue({ x: 0, y: 0 });
      opacity2.setValue(0);
      return;
    }

    // Start animation sequence
    const animate = () => {
      // Reset to initial state
      position1.setValue({ x: -20, y: 0 });
      position2.setValue({ x: 20, y: 0 });
      opacity2.setValue(1);

      Animated.sequence([
        // Step 1: Brief pause (300ms)
        Animated.delay(300),
        // Step 2: Both circles move toward center (600ms)
        Animated.parallel([
          Animated.timing(position1, {
            toValue: { x: 0, y: 0 },
            duration: 600,
            useNativeDriver: true,
          }),
          Animated.timing(position2, {
            toValue: { x: 0, y: 0 },
            duration: 600,
            useNativeDriver: true,
          }),
        ]),
        // Step 3: Second circle fades out (300ms)
        Animated.timing(opacity2, {
          toValue: 0,
          duration: 300,
          useNativeDriver: true,
        }),
        // Step 4: Brief pause (300ms)
        Animated.delay(300),
      ]).start(() => {
        // Loop animation
        animate();
      });
    };

    animate();
  }, [reduceMotion, position1, position2, opacity2]);

  return (
    <View
      style={styles.animationContainer}
      accessibilityLabel="Decrease animation showing two stitches becoming one stitch"
      accessible={true}
    >
      <StitchCircle
        color={kidModeTheme.colors.error}
        position={position1}
        size={stitchSize}
      />
      <StitchCircle
        color={kidModeTheme.colors.error}
        position={position2}
        opacity={opacity2}
        size={stitchSize}
      />
    </View>
  );
};

// ============================================================================
// MagicRingAnimation Component
// ============================================================================

export interface MagicRingAnimationProps {
  /**
   * Whether to reduce motion (accessibility)
   * @default false
   */
  reduceMotion?: boolean;

  /**
   * Size of stitches
   * @default 20
   */
  stitchSize?: number;

  /**
   * Number of stitches in the ring
   * @default 6
   */
  stitchCount?: number;
}

/**
 * Animation showing stitches forming a magic ring
 *
 * Visual: Circles appear and rotate into a circular formation
 * Duration: 2 seconds
 * Respects: prefers-reduced-motion
 */
export const MagicRingAnimation: React.FC<MagicRingAnimationProps> = ({
  reduceMotion = false,
  stitchSize = 20,
  stitchCount = 6,
}) => {
  const rotation = useRef(new Animated.Value(0)).current;
  const scales = useRef(
    Array.from({ length: stitchCount }, () => new Animated.Value(0))
  ).current;

  useEffect(() => {
    if (reduceMotion) {
      // No animation - just show final state
      scales.forEach((scale) => scale.setValue(1));
      rotation.setValue(1);
      return;
    }

    // Start animation sequence
    const animate = () => {
      // Reset to initial state
      scales.forEach((scale) => scale.setValue(0));
      rotation.setValue(0);

      // Stagger the appearance of each stitch
      const staggerDelay = 100;
      const stitchAnimations = scales.map((scale, index) =>
        Animated.sequence([
          Animated.delay(index * staggerDelay),
          Animated.spring(scale, {
            toValue: 1,
            friction: 5,
            tension: 40,
            useNativeDriver: true,
          }),
        ])
      );

      // Rotation animation
      const rotationAnimation = Animated.timing(rotation, {
        toValue: 1,
        duration: 2000,
        useNativeDriver: true,
      });

      Animated.parallel([...stitchAnimations, rotationAnimation]).start(() => {
        // Brief pause before restarting
        setTimeout(animate, 500);
      });
    };

    animate();
  }, [reduceMotion, rotation, scales, stitchCount]);

  const rotationInterpolate = rotation.interpolate({
    inputRange: [0, 1],
    outputRange: ['0deg', '360deg'],
  });

  // Calculate positions for stitches in a circle
  const radius = 40;
  const angleStep = (2 * Math.PI) / stitchCount;

  return (
    <View
      style={styles.animationContainer}
      accessibilityLabel="Magic ring animation showing stitches forming a circle"
      accessible={true}
    >
      <Animated.View
        style={{
          transform: [{ rotate: rotationInterpolate }],
        }}
      >
        {scales.map((scale, index) => {
          const angle = index * angleStep;
          const x = radius * Math.cos(angle);
          const y = radius * Math.sin(angle);

          return (
            <Animated.View
              key={index}
              style={{
                position: 'absolute',
                transform: [{ translateX: x }, { translateY: y }, { scale }],
              }}
            >
              <StitchCircle
                color={kidModeTheme.colors.info}
                size={stitchSize}
              />
            </Animated.View>
          );
        })}
      </Animated.View>
    </View>
  );
};

// ============================================================================
// Styles
// ============================================================================

const styles = StyleSheet.create({
  animationContainer: {
    width: 120,
    height: 120,
    justifyContent: 'center',
    alignItems: 'center',
    position: 'relative',
  },
});
