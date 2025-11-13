import React, { useEffect, useRef } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, AccessibilityInfo } from 'react-native';
import Slider from '@react-native-community/slider';
import { useVisualizationStore } from '../../stores/useVisualizationStore';
import { colors } from '../../theme/colors';
import { spacing } from '../../theme/spacing';
import { typography } from '../../theme/typography';

export const RoundScrubber: React.FC = () => {
  const { currentRound, totalRounds, prevRound, nextRound, jumpToRound, frames } =
    useVisualizationStore();

  const previousRoundRef = useRef(currentRound);

  // Announce round changes to screen readers
  useEffect(() => {
    if (previousRoundRef.current !== currentRound && frames.length > 0) {
      const currentFrame = frames[currentRound - 1];
      const stitchCount = currentFrame?.stitch_count || 0;
      const message = `Round ${currentRound} of ${totalRounds}, ${stitchCount} stitches`;
      AccessibilityInfo.announceForAccessibility(message);
      previousRoundRef.current = currentRound;
    }
  }, [currentRound, totalRounds, frames]);

  if (totalRounds === 0) return null;

  const isPrevDisabled = currentRound === 1;
  const isNextDisabled = currentRound === totalRounds;
  const currentFrame = frames[currentRound - 1];
  const stitchCount = currentFrame?.stitch_count || 0;

  return (
    <View
      style={styles.container}
      accessible={true}
      accessibilityRole="none"
      accessibilityLabel="Round navigation controls"
    >
      {/* Previous button */}
      <TouchableOpacity
        onPress={prevRound}
        disabled={isPrevDisabled}
        style={[styles.button, isPrevDisabled && styles.buttonDisabled]}
        accessibilityRole="button"
        accessibilityLabel="Previous round"
        accessibilityHint={isPrevDisabled ? 'Already at first round' : 'Go to previous round'}
        accessibilityState={{ disabled: isPrevDisabled }}
        accessible={true}
      >
        <Text
          style={[styles.buttonText, isPrevDisabled && styles.buttonTextDisabled]}
          accessible={false}
        >
          ←
        </Text>
      </TouchableOpacity>

      {/* Slider */}
      <View style={styles.sliderContainer}>
        <Slider
          style={styles.slider}
          minimumValue={1}
          maximumValue={totalRounds}
          step={1}
          value={currentRound}
          onValueChange={jumpToRound}
          minimumTrackTintColor={colors.primary}
          maximumTrackTintColor={colors.gray300}
          thumbTintColor={colors.primary}
          accessibilityLabel={`Round ${currentRound} of ${totalRounds}, ${stitchCount} stitches`}
          accessibilityRole="adjustable"
          accessibilityHint="Swipe up to go to next round, swipe down to go to previous round"
          accessible={true}
        />
        <Text
          style={styles.label}
          accessible={true}
          accessibilityRole="text"
          accessibilityLabel={`Currently viewing round ${currentRound} of ${totalRounds}`}
        >
          Round {currentRound} of {totalRounds}
        </Text>
      </View>

      {/* Next button */}
      <TouchableOpacity
        onPress={nextRound}
        disabled={isNextDisabled}
        style={[styles.button, isNextDisabled && styles.buttonDisabled]}
        accessibilityRole="button"
        accessibilityLabel="Next round"
        accessibilityHint={isNextDisabled ? 'Already at last round' : 'Go to next round'}
        accessibilityState={{ disabled: isNextDisabled }}
        accessible={true}
      >
        <Text
          style={[styles.buttonText, isNextDisabled && styles.buttonTextDisabled]}
          accessible={false}
        >
          →
        </Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    backgroundColor: colors.white,
    borderTopWidth: 1,
    borderTopColor: colors.gray200,
  },
  button: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: colors.primary,
    alignItems: 'center',
    justifyContent: 'center',
  },
  buttonDisabled: {
    backgroundColor: colors.gray300,
  },
  buttonText: {
    color: colors.white,
    fontSize: 24,
    fontWeight: 'bold',
  },
  buttonTextDisabled: {
    color: colors.gray500,
  },
  sliderContainer: {
    flex: 1,
    marginHorizontal: spacing.md,
  },
  slider: {
    width: '100%',
    height: 40,
  },
  label: {
    textAlign: 'center',
    fontSize: typography.sizes.sm,
    color: colors.gray600,
    marginTop: 4,
  },
});
