import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useSettingsStore } from '../stores/useSettingsStore';
import { patternApi } from '../services/api';
import type { ShapeType, Units, Terminology } from '../types';
import { colors, kidModeColors, spacing, borderRadius, shadows, typography } from '../theme';

export default function GenerateScreen() {
  const navigate = useNavigate();
  const { kidMode } = useSettingsStore();
  const [shape, setShape] = useState<ShapeType>('sphere');
  const [diameter, setDiameter] = useState('10');
  const [height, setHeight] = useState('15');
  const [units, setUnits] = useState<Units>('cm');
  const [terminology, setTerminology] = useState<Terminology>('US');
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const theme = kidMode ? kidModeColors : colors;

  const getShapeLabel = (s: ShapeType) => {
    if (!kidMode) return s.charAt(0).toUpperCase() + s.slice(1);
    return s === 'sphere' ? 'Ball' : s === 'cylinder' ? 'Tube' : 'Cone';
  };

  const handleGenerate = async () => {
    setGenerating(true);
    setError(null);

    try {
      const response = await patternApi.generate({
        shape,
        diameter: parseFloat(diameter),
        height: shape !== 'sphere' ? parseFloat(height) : undefined,
        units,
        gauge: { sts_per_10cm: 14, rows_per_10cm: 16 },
        stitch: 'sc',
        terms: terminology,
      });

      // Navigate to visualization screen with the pattern
      navigate('/visualize', { state: { pattern: response.dsl } });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate pattern');
    } finally {
      setGenerating(false);
    }
  };

  const shapes: ShapeType[] = ['sphere', 'cylinder', 'cone'];

  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: colors.background,
      padding: spacing.lg,
    }}>
      <div style={{ maxWidth: '800px', margin: '0 auto' }}>
        <header style={{ marginBottom: spacing.xl }}>
          <h1 style={{
            fontSize: typography.fontSize['3xl'],
            fontWeight: typography.fontWeight.bold,
            color: colors.textPrimary,
            marginBottom: spacing.sm,
          }}>
            {kidMode ? 'Make a Pattern' : 'Generate Pattern'}
          </h1>
          <p style={{
            fontSize: typography.fontSize.lg,
            color: colors.textSecondary,
          }}>
            {kidMode
              ? 'Pick a shape and tell us how big you want it'
              : 'Configure your crochet pattern parameters'}
          </p>
        </header>

        <form onSubmit={(e) => { e.preventDefault(); handleGenerate(); }}>
          {/* Shape Selection */}
          <div style={{ marginBottom: spacing.lg }}>
            <label style={{
              display: 'block',
              fontSize: typography.fontSize.lg,
              fontWeight: typography.fontWeight.medium,
              color: colors.textPrimary,
              marginBottom: spacing.sm,
            }}>
              {kidMode ? 'Pick a Shape' : 'Shape'}
            </label>
            <div style={{ display: 'flex', gap: spacing.sm }}>
              {shapes.map((s) => (
                <button
                  key={s}
                  type="button"
                  onClick={() => setShape(s)}
                  style={{
                    flex: 1,
                    padding: spacing.md,
                    backgroundColor: shape === s ? theme.primary : colors.surfaceSecondary,
                    color: shape === s ? colors.textInverse : colors.textPrimary,
                    border: 'none',
                    borderRadius: borderRadius.md,
                    fontSize: typography.fontSize.base,
                    fontWeight: typography.fontWeight.medium,
                    cursor: 'pointer',
                    minHeight: '44px',
                  }}
                  aria-pressed={shape === s}
                >
                  {getShapeLabel(s)}
                </button>
              ))}
            </div>
          </div>

          {/* Diameter Input */}
          <div style={{ marginBottom: spacing.lg }}>
            <label style={{
              display: 'block',
              fontSize: typography.fontSize.lg,
              fontWeight: typography.fontWeight.medium,
              color: colors.textPrimary,
              marginBottom: spacing.sm,
            }}>
              {kidMode ? 'How Wide?' : 'Diameter'}
            </label>
            <div style={{ display: 'flex', gap: spacing.sm }}>
              <input
                type="number"
                value={diameter}
                onChange={(e) => setDiameter(e.target.value)}
                step="0.1"
                min="1"
                style={{
                  flex: 1,
                  padding: spacing.md,
                  backgroundColor: colors.surface,
                  border: `1px solid ${colors.border}`,
                  borderRadius: borderRadius.md,
                  fontSize: typography.fontSize.base,
                  color: colors.textPrimary,
                  minHeight: '44px',
                }}
                placeholder="10"
                aria-label={kidMode ? 'How wide input' : 'Diameter input'}
              />
              <div style={{ display: 'flex', backgroundColor: colors.surfaceSecondary, borderRadius: borderRadius.md, overflow: 'hidden' }}>
                {(['cm', 'in'] as Units[]).map((u) => (
                  <button
                    key={u}
                    type="button"
                    onClick={() => setUnits(u)}
                    style={{
                      padding: `${spacing.md} ${spacing.lg}`,
                      backgroundColor: units === u ? theme.primary : 'transparent',
                      color: units === u ? colors.textInverse : colors.textPrimary,
                      border: 'none',
                      fontSize: typography.fontSize.base,
                      fontWeight: typography.fontWeight.medium,
                      cursor: 'pointer',
                      minHeight: '44px',
                      minWidth: '60px',
                    }}
                    aria-pressed={units === u}
                  >
                    {u}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Height Input (for cylinder/cone) */}
          {(shape === 'cylinder' || shape === 'cone') && (
            <div style={{ marginBottom: spacing.lg }}>
              <label style={{
                display: 'block',
                fontSize: typography.fontSize.lg,
                fontWeight: typography.fontWeight.medium,
                color: colors.textPrimary,
                marginBottom: spacing.sm,
              }}>
                {kidMode ? 'How Tall?' : 'Height'}
              </label>
              <input
                type="number"
                value={height}
                onChange={(e) => setHeight(e.target.value)}
                step="0.1"
                min="1"
                style={{
                  width: '100%',
                  padding: spacing.md,
                  backgroundColor: colors.surface,
                  border: `1px solid ${colors.border}`,
                  borderRadius: borderRadius.md,
                  fontSize: typography.fontSize.base,
                  color: colors.textPrimary,
                  minHeight: '44px',
                }}
                placeholder="15"
                aria-label={kidMode ? 'How tall input' : 'Height input'}
              />
            </div>
          )}

          {/* Terminology Toggle */}
          <div style={{ marginBottom: spacing.xl }}>
            <label style={{
              display: 'block',
              fontSize: typography.fontSize.lg,
              fontWeight: typography.fontWeight.medium,
              color: colors.textPrimary,
              marginBottom: spacing.sm,
            }}>
              {kidMode ? 'Stitch Names' : 'Crochet Terminology'}
            </label>
            <div style={{ display: 'flex', gap: spacing.sm }}>
              {(['US', 'UK'] as Terminology[]).map((term) => (
                <button
                  key={term}
                  type="button"
                  onClick={() => setTerminology(term)}
                  style={{
                    flex: 1,
                    padding: spacing.md,
                    backgroundColor: terminology === term ? theme.primary : colors.surfaceSecondary,
                    color: terminology === term ? colors.textInverse : colors.textPrimary,
                    border: 'none',
                    borderRadius: borderRadius.md,
                    fontSize: typography.fontSize.base,
                    fontWeight: typography.fontWeight.medium,
                    cursor: 'pointer',
                    minHeight: '44px',
                  }}
                  aria-pressed={terminology === term}
                >
                  {term}
                </button>
              ))}
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <div style={{
              padding: spacing.md,
              backgroundColor: '#FEE2E2',
              borderRadius: borderRadius.md,
              marginBottom: spacing.lg,
            }}>
              <p style={{ color: colors.error, fontSize: typography.fontSize.sm }}>
                {error}
              </p>
            </div>
          )}

          {/* Generate Button */}
          <button
            type="submit"
            disabled={generating}
            style={{
              width: '100%',
              padding: spacing.lg,
              backgroundColor: generating ? colors.surfaceSecondary : theme.primary,
              color: colors.textInverse,
              border: 'none',
              borderRadius: borderRadius.lg,
              fontSize: typography.fontSize.xl,
              fontWeight: typography.fontWeight.semibold,
              cursor: generating ? 'not-allowed' : 'pointer',
              boxShadow: shadows.md,
              minHeight: '56px',
            }}
            aria-label={generating ? 'Generating pattern...' : 'Generate pattern'}
          >
            {generating ? 'Generating...' : kidMode ? 'Make My Pattern' : 'Generate Pattern'}
          </button>
        </form>
      </div>
    </div>
  );
}
