import React from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { MainTabScreenProps } from '../types';
import { colors, typography, spacing, shadows } from '../theme';

type Props = MainTabScreenProps<'Home'>;

export default function HomeScreen({ navigation }: Props) {
  const handleStartGenerating = () => {
    navigation.navigate('Generate');
  };

  const handleParsePattern = () => {
    navigation.navigate('Parse');
  };

  return (
    <ScrollView
      style={styles.container}
      contentContainerStyle={styles.content}
      accessibilityLabel="Home screen"
      accessible={true}
    >
      <View style={styles.header}>
        <Text style={styles.title} accessibilityRole="header">
          Welcome to Knit-Wit
        </Text>
        <Text
          style={styles.subtitle}
          accessible={true}
          accessibilityRole="text"
        >
          Generate custom crochet patterns for geometric shapes with interactive step-by-step
          guidance.
        </Text>
      </View>

      <View style={styles.section}>
        <Text
          style={styles.sectionTitle}
          accessibilityRole="header"
          accessibilityLevel={2}
        >
          Quick Start
        </Text>
        <TouchableOpacity
          style={styles.card}
          onPress={handleStartGenerating}
          accessibilityRole="button"
          accessibilityLabel="Start generating a pattern"
          accessibilityHint="Navigate to the pattern generator"
          accessible={true}
        >
          <View style={styles.cardContent}>
            <Text style={styles.cardTitle}>Generate Pattern</Text>
            <Text style={styles.cardDescription}>
              Create a new crochet pattern for spheres, cylinders, or cones
            </Text>
          </View>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.card}
          onPress={handleParsePattern}
          accessibilityRole="button"
          accessibilityLabel="Parse existing pattern"
          accessibilityHint="Navigate to the pattern parser to validate and visualize an existing pattern"
          accessible={true}
        >
          <View style={styles.cardContent}>
            <Text style={styles.cardTitle}>Parse Pattern</Text>
            <Text style={styles.cardDescription}>
              Validate and visualize an existing crochet pattern
            </Text>
          </View>
        </TouchableOpacity>
      </View>

      <View style={styles.section}>
        <Text
          style={styles.sectionTitle}
          accessibilityRole="header"
          accessibilityLevel={2}
        >
          Features
        </Text>
        <View
          style={styles.featureList}
          accessible={true}
          accessibilityRole="list"
        >
          <FeatureItem
            title="Parametric Patterns"
            description="Specify dimensions and gauge to generate custom patterns"
          />
          <FeatureItem
            title="Interactive Visualization"
            description="Step-by-step SVG diagrams for each round"
          />
          <FeatureItem
            title="Multiple Exports"
            description="Save as PDF, SVG, or JSON for different uses"
          />
          <FeatureItem
            title="US/UK Terminology"
            description="Toggle between US and UK crochet terms"
          />
        </View>
      </View>
    </ScrollView>
  );
}

interface FeatureItemProps {
  title: string;
  description: string;
}

function FeatureItem({ title, description }: FeatureItemProps) {
  return (
    <View
      style={styles.featureItem}
      accessible={true}
      accessibilityLabel={`${title}. ${description}`}
      accessibilityRole="text"
    >
      <Text style={styles.featureTitle}>{title}</Text>
      <Text style={styles.featureDescription}>{description}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  content: {
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.lg,
  },
  header: {
    marginBottom: spacing.xl,
  },
  title: {
    ...typography.displaySmall,
    color: colors.textPrimary,
    marginBottom: spacing.sm,
  },
  subtitle: {
    ...typography.bodyLarge,
    color: colors.textSecondary,
  },
  section: {
    marginBottom: spacing.xl,
  },
  sectionTitle: {
    ...typography.headlineSmall,
    color: colors.textPrimary,
    marginBottom: spacing.md,
  },
  card: {
    backgroundColor: colors.surface,
    borderRadius: 12,
    padding: spacing.lg,
    marginBottom: spacing.md,
    ...shadows.md,
  },
  cardContent: {
    gap: spacing.sm,
  },
  cardTitle: {
    ...typography.titleLarge,
    color: colors.primary,
  },
  cardDescription: {
    ...typography.bodyMedium,
    color: colors.textSecondary,
  },
  featureList: {
    gap: spacing.md,
  },
  featureItem: {
    backgroundColor: colors.surfaceSecondary,
    padding: spacing.md,
    borderRadius: 8,
  },
  featureTitle: {
    ...typography.titleMedium,
    color: colors.textPrimary,
    marginBottom: spacing.xs,
  },
  featureDescription: {
    ...typography.bodySmall,
    color: colors.textSecondary,
  },
});
