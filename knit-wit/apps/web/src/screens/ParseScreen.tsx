import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useSettingsStore } from '../stores/useSettingsStore';
import { patternApi } from '../services/api';
import { colors, kidModeColors, spacing, borderRadius, typography, shadows } from '../theme';

export default function ParseScreen() {
  const navigate = useNavigate();
  const { kidMode } = useSettingsStore();
  const [patternText, setPatternText] = useState('');
  const [parsing, setParsing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const theme = kidMode ? kidModeColors : colors;

  const handleParse = async () => {
    setParsing(true);
    setError(null);

    try {
      const response = await patternApi.parse(patternText);

      if (response.validation.valid) {
        navigate('/visualize', { state: { pattern: response.dsl } });
      } else {
        setError(response.validation.errors.map(e => e.message).join('\n'));
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to parse pattern');
    } finally {
      setParsing(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', backgroundColor: colors.background, padding: spacing.lg }}>
      <div style={{ maxWidth: '800px', margin: '0 auto' }}>
        <header style={{ marginBottom: spacing.xl }}>
          <h1 style={{
            fontSize: typography.fontSize['3xl'],
            fontWeight: typography.fontWeight.bold,
            color: colors.textPrimary,
            marginBottom: spacing.sm,
          }}>
            {kidMode ? 'Check a Pattern' : 'Parse Pattern'}
          </h1>
          <p style={{
            fontSize: typography.fontSize.lg,
            color: colors.textSecondary,
          }}>
            {kidMode
              ? 'Paste your pattern here and we will show you if it works'
              : 'Paste your crochet pattern text to validate and visualize'}
          </p>
        </header>

        <div>
          <textarea
            value={patternText}
            onChange={(e) => setPatternText(e.target.value)}
            placeholder={kidMode
              ? "Paste your pattern here..."
              : "Paste your crochet pattern text here (e.g., 'Round 1: 6 sc in magic ring...')"}
            style={{
              width: '100%',
              minHeight: '300px',
              padding: spacing.md,
              backgroundColor: colors.surface,
              border: `2px solid ${colors.border}`,
              borderRadius: borderRadius.lg,
              fontSize: typography.fontSize.base,
              fontFamily: typography.fontFamily.mono,
              color: colors.textPrimary,
              resize: 'vertical',
              marginBottom: spacing.lg,
            }}
            aria-label={kidMode ? 'Pattern text' : 'Pattern text input'}
          />

          {error && (
            <div style={{
              padding: spacing.md,
              backgroundColor: '#FEE2E2',
              borderRadius: borderRadius.md,
              marginBottom: spacing.lg,
            }}>
              <p style={{ color: colors.error, fontSize: typography.fontSize.sm, whiteSpace: 'pre-wrap' }}>
                {error}
              </p>
            </div>
          )}

          <button
            onClick={handleParse}
            disabled={parsing || !patternText.trim()}
            style={{
              width: '100%',
              padding: spacing.lg,
              backgroundColor: (parsing || !patternText.trim()) ? colors.surfaceSecondary : theme.primary,
              color: colors.textInverse,
              border: 'none',
              borderRadius: borderRadius.lg,
              fontSize: typography.fontSize.xl,
              fontWeight: typography.fontWeight.semibold,
              cursor: (parsing || !patternText.trim()) ? 'not-allowed' : 'pointer',
              boxShadow: shadows.md,
            }}
          >
            {parsing ? 'Checking...' : kidMode ? 'Check Pattern' : 'Parse & Visualize'}
          </button>
        </div>
      </div>
    </div>
  );
}
