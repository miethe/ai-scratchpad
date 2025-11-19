import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useSettingsStore } from '../stores/useSettingsStore';
import { colors, kidModeColors, spacing, borderRadius, shadows, typography } from '../theme';

export default function HomeScreen() {
  const navigate = useNavigate();
  const { kidMode } = useSettingsStore();

  const theme = kidMode ? kidModeColors : colors;

  const handleStartGenerating = () => {
    navigate('/generate');
  };

  const handleParsePattern = () => {
    navigate('/parse');
  };

  const features = kidMode ? [
    { title: 'Custom Patterns', description: 'Tell us the size you want and we make the pattern for you' },
    { title: 'Step by Step', description: 'See pictures for each step of your pattern' },
    { title: 'Save Your Pattern', description: 'Save as PDF or picture to use later' },
    { title: 'Easy Words', description: 'Use simple crochet words that are easy to understand' },
  ] : [
    { title: 'Parametric Patterns', description: 'Specify dimensions and gauge to generate custom patterns' },
    { title: 'Interactive Visualization', description: 'Step-by-step SVG diagrams for each round' },
    { title: 'Multiple Exports', description: 'Save as PDF, SVG, or JSON for different uses' },
    { title: 'US/UK Terminology', description: 'Toggle between US and UK crochet terms' },
  ];

  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: colors.background,
      padding: spacing.lg,
    }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        {/* Header */}
        <header style={{ marginBottom: spacing.xl }}>
          <h1 style={{
            fontSize: typography.fontSize['3xl'],
            fontWeight: typography.fontWeight.bold,
            color: theme.textPrimary,
            marginBottom: spacing.sm,
          }}>
            Welcome to Knit-Wit
          </h1>
          <p style={{
            fontSize: typography.fontSize.lg,
            color: colors.textSecondary,
            lineHeight: typography.lineHeight.relaxed,
          }}>
            {kidMode
              ? 'Make your own crochet patterns! Pick a shape, and we will show you how to make it step by step.'
              : 'Generate custom crochet patterns for geometric shapes with interactive step-by-step guidance.'}
          </p>
        </header>

        {/* Quick Start Section */}
        <section style={{ marginBottom: spacing.xl }}>
          <h2 style={{
            fontSize: typography.fontSize['2xl'],
            fontWeight: typography.fontWeight.semibold,
            color: colors.textPrimary,
            marginBottom: spacing.md,
          }}>
            {kidMode ? 'Get Started' : 'Quick Start'}
          </h2>

          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
            gap: spacing.md,
          }}>
            <button
              onClick={handleStartGenerating}
              style={{
                backgroundColor: colors.surface,
                border: 'none',
                borderRadius: borderRadius.lg,
                padding: spacing.lg,
                boxShadow: shadows.md,
                cursor: 'pointer',
                textAlign: 'left',
                transition: 'transform 150ms ease-in-out, box-shadow 150ms ease-in-out',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-2px)';
                e.currentTarget.style.boxShadow = shadows.lg;
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.boxShadow = shadows.md;
              }}
              aria-label={kidMode ? 'Make a pattern' : 'Start generating a pattern'}
            >
              <h3 style={{
                fontSize: typography.fontSize.xl,
                fontWeight: typography.fontWeight.semibold,
                color: theme.primary,
                marginBottom: spacing.sm,
              }}>
                {kidMode ? 'Make a Pattern' : 'Generate Pattern'}
              </h3>
              <p style={{
                fontSize: typography.fontSize.base,
                color: colors.textSecondary,
                lineHeight: typography.lineHeight.relaxed,
              }}>
                {kidMode
                  ? 'Pick a shape like a ball, tube, or cone and make your own pattern'
                  : 'Create a new crochet pattern for spheres, cylinders, or cones'}
              </p>
            </button>

            <button
              onClick={handleParsePattern}
              style={{
                backgroundColor: colors.surface,
                border: 'none',
                borderRadius: borderRadius.lg,
                padding: spacing.lg,
                boxShadow: shadows.md,
                cursor: 'pointer',
                textAlign: 'left',
                transition: 'transform 150ms ease-in-out, box-shadow 150ms ease-in-out',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-2px)';
                e.currentTarget.style.boxShadow = shadows.lg;
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.boxShadow = shadows.md;
              }}
              aria-label={kidMode ? 'Check a pattern' : 'Parse existing pattern'}
            >
              <h3 style={{
                fontSize: typography.fontSize.xl,
                fontWeight: typography.fontWeight.semibold,
                color: theme.primary,
                marginBottom: spacing.sm,
              }}>
                {kidMode ? 'Check a Pattern' : 'Parse Pattern'}
              </h3>
              <p style={{
                fontSize: typography.fontSize.base,
                color: colors.textSecondary,
                lineHeight: typography.lineHeight.relaxed,
              }}>
                {kidMode
                  ? 'See if your pattern works and view it step by step'
                  : 'Validate and visualize an existing crochet pattern'}
              </p>
            </button>
          </div>
        </section>

        {/* Features Section */}
        <section>
          <h2 style={{
            fontSize: typography.fontSize['2xl'],
            fontWeight: typography.fontWeight.semibold,
            color: colors.textPrimary,
            marginBottom: spacing.md,
          }}>
            {kidMode ? 'What You Can Do' : 'Features'}
          </h2>

          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
            gap: spacing.md,
          }}>
            {features.map((feature, index) => (
              <div
                key={index}
                style={{
                  backgroundColor: colors.surfaceSecondary,
                  padding: spacing.md,
                  borderRadius: borderRadius.md,
                }}
              >
                <h3 style={{
                  fontSize: typography.fontSize.lg,
                  fontWeight: typography.fontWeight.medium,
                  color: colors.textPrimary,
                  marginBottom: spacing.xs,
                }}>
                  {feature.title}
                </h3>
                <p style={{
                  fontSize: typography.fontSize.sm,
                  color: colors.textSecondary,
                  lineHeight: typography.lineHeight.relaxed,
                }}>
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}
