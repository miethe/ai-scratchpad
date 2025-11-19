import React from 'react';
import { useSettingsStore } from '../stores/useSettingsStore';
import { colors, spacing, borderRadius, typography } from '../theme';

export default function SettingsScreen() {
  const {
    kidMode,
    units,
    terminology,
    theme,
    highContrast,
    reducedMotion,
    fontSize,
    setKidMode,
    setUnits,
    setTerminology,
    setTheme,
    setHighContrast,
    setReducedMotion,
    setFontSize,
    resetSettings,
  } = useSettingsStore();

  return (
    <div style={{ minHeight: '100vh', backgroundColor: colors.background, padding: spacing.lg }}>
      <div style={{ maxWidth: '800px', margin: '0 auto' }}>
        <h1 style={{
          fontSize: typography.fontSize['3xl'],
          fontWeight: typography.fontWeight.bold,
          color: colors.textPrimary,
          marginBottom: spacing.xl,
        }}>
          Settings
        </h1>

        <div style={{ display: 'flex', flexDirection: 'column', gap: spacing.lg }}>
          {/* Kid Mode */}
          <div style={{ backgroundColor: colors.surface, padding: spacing.lg, borderRadius: borderRadius.lg }}>
            <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
              <input
                type="checkbox"
                checked={kidMode}
                onChange={(e) => setKidMode(e.target.checked)}
                style={{ marginRight: spacing.md, width: '20px', height: '20px' }}
              />
              <div>
                <div style={{ fontSize: typography.fontSize.lg, fontWeight: typography.fontWeight.semibold, color: colors.textPrimary }}>
                  Kid Mode
                </div>
                <div style={{ fontSize: typography.fontSize.sm, color: colors.textSecondary }}>
                  Simplified interface with larger buttons and easier words
                </div>
              </div>
            </label>
          </div>

          {/* Units */}
          <div style={{ backgroundColor: colors.surface, padding: spacing.lg, borderRadius: borderRadius.lg }}>
            <div style={{ marginBottom: spacing.sm, fontSize: typography.fontSize.lg, fontWeight: typography.fontWeight.semibold, color: colors.textPrimary }}>
              Units
            </div>
            <div style={{ display: 'flex', gap: spacing.sm }}>
              {(['cm', 'in'] as const).map((u) => (
                <button
                  key={u}
                  onClick={() => setUnits(u)}
                  style={{
                    flex: 1,
                    padding: spacing.md,
                    backgroundColor: units === u ? colors.primary : colors.surfaceSecondary,
                    color: units === u ? colors.textInverse : colors.textPrimary,
                    border: 'none',
                    borderRadius: borderRadius.md,
                    cursor: 'pointer',
                  }}
                >
                  {u === 'cm' ? 'Centimeters' : 'Inches'}
                </button>
              ))}
            </div>
          </div>

          {/* Terminology */}
          <div style={{ backgroundColor: colors.surface, padding: spacing.lg, borderRadius: borderRadius.lg }}>
            <div style={{ marginBottom: spacing.sm, fontSize: typography.fontSize.lg, fontWeight: typography.fontWeight.semibold, color: colors.textPrimary }}>
              Crochet Terminology
            </div>
            <div style={{ display: 'flex', gap: spacing.sm }}>
              {(['US', 'UK'] as const).map((term) => (
                <button
                  key={term}
                  onClick={() => setTerminology(term)}
                  style={{
                    flex: 1,
                    padding: spacing.md,
                    backgroundColor: terminology === term ? colors.primary : colors.surfaceSecondary,
                    color: terminology === term ? colors.textInverse : colors.textPrimary,
                    border: 'none',
                    borderRadius: borderRadius.md,
                    cursor: 'pointer',
                  }}
                >
                  {term}
                </button>
              ))}
            </div>
          </div>

          {/* Theme */}
          <div style={{ backgroundColor: colors.surface, padding: spacing.lg, borderRadius: borderRadius.lg }}>
            <div style={{ marginBottom: spacing.sm, fontSize: typography.fontSize.lg, fontWeight: typography.fontWeight.semibold, color: colors.textPrimary }}>
              Theme
            </div>
            <div style={{ display: 'flex', gap: spacing.sm }}>
              {(['light', 'dark', 'system'] as const).map((t) => (
                <button
                  key={t}
                  onClick={() => setTheme(t)}
                  style={{
                    flex: 1,
                    padding: spacing.md,
                    backgroundColor: theme === t ? colors.primary : colors.surfaceSecondary,
                    color: theme === t ? colors.textInverse : colors.textPrimary,
                    border: 'none',
                    borderRadius: borderRadius.md,
                    cursor: 'pointer',
                  }}
                >
                  {t.charAt(0).toUpperCase() + t.slice(1)}
                </button>
              ))}
            </div>
          </div>

          {/* Accessibility */}
          <div style={{ backgroundColor: colors.surface, padding: spacing.lg, borderRadius: borderRadius.lg }}>
            <h2 style={{ marginBottom: spacing.md, fontSize: typography.fontSize.xl, fontWeight: typography.fontWeight.semibold, color: colors.textPrimary }}>
              Accessibility
            </h2>

            <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer', marginBottom: spacing.md }}>
              <input
                type="checkbox"
                checked={highContrast}
                onChange={(e) => setHighContrast(e.target.checked)}
                style={{ marginRight: spacing.md, width: '20px', height: '20px' }}
              />
              <div>
                <div style={{ fontSize: typography.fontSize.base, fontWeight: typography.fontWeight.medium, color: colors.textPrimary }}>
                  High Contrast
                </div>
              </div>
            </label>

            <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer', marginBottom: spacing.md }}>
              <input
                type="checkbox"
                checked={reducedMotion}
                onChange={(e) => setReducedMotion(e.target.checked)}
                style={{ marginRight: spacing.md, width: '20px', height: '20px' }}
              />
              <div>
                <div style={{ fontSize: typography.fontSize.base, fontWeight: typography.fontWeight.medium, color: colors.textPrimary }}>
                  Reduced Motion
                </div>
              </div>
            </label>

            <div>
              <div style={{ marginBottom: spacing.sm, fontSize: typography.fontSize.base, fontWeight: typography.fontWeight.medium, color: colors.textPrimary }}>
                Font Size
              </div>
              <div style={{ display: 'flex', gap: spacing.sm }}>
                {(['small', 'medium', 'large'] as const).map((size) => (
                  <button
                    key={size}
                    onClick={() => setFontSize(size)}
                    style={{
                      flex: 1,
                      padding: spacing.sm,
                      backgroundColor: fontSize === size ? colors.primary : colors.surfaceSecondary,
                      color: fontSize === size ? colors.textInverse : colors.textPrimary,
                      border: 'none',
                      borderRadius: borderRadius.md,
                      cursor: 'pointer',
                    }}
                  >
                    {size.charAt(0).toUpperCase() + size.slice(1)}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Reset */}
          <button
            onClick={resetSettings}
            style={{
              padding: spacing.md,
              backgroundColor: colors.surfaceSecondary,
              color: colors.textPrimary,
              border: 'none',
              borderRadius: borderRadius.md,
              cursor: 'pointer',
              fontSize: typography.fontSize.base,
            }}
          >
            Reset to Defaults
          </button>
        </div>
      </div>
    </div>
  );
}
