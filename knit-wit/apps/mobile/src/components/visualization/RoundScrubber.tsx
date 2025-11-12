import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import Slider from '@react-native-community/slider';
import { useVisualizationStore } from '../../stores/useVisualizationStore';
import { colors } from '../../theme/colors';
import { spacing } from '../../theme/spacing';
import { typography } from '../../theme/typography';

export const RoundScrubber: React.FC = () => {
  const { currentRound, totalRounds, prevRound, nextRound, jumpToRound } =
    useVisualizationStore();

  if (totalRounds === 0) return null;

  const isPrevDisabled = currentRound === 1;
  const isNextDisabled = currentRound === totalRounds;

  return (
    <View style={styles.container}>
      {/* Previous button */}
      <TouchableOpacity
        onPress={prevRound}
        disabled={isPrevDisabled}
        style={[styles.button, isPrevDisabled && styles.buttonDisabled]}
        accessibilityRole="button"
        accessibilityLabel="Previous round"
        accessibilityState={{ disabled: isPrevDisabled }}
      >
        <Text style={[styles.buttonText, isPrevDisabled && styles.buttonTextDisabled]}>
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
          accessibilityLabel={`Round ${currentRound} of ${totalRounds}`}
          accessibilityRole="adjustable"
        />
        <Text style={styles.label}>
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
        accessibilityState={{ disabled: isNextDisabled }}
      >
        <Text style={[styles.buttonText, isNextDisabled && styles.buttonTextDisabled]}>
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
