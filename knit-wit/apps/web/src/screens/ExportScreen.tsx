import React from 'react';
import { colors, spacing, borderRadius, typography } from '../theme';

export default function ExportScreen() {
  return (
    <div style={{ minHeight: '100vh', backgroundColor: colors.background, padding: spacing.lg }}>
      <div style={{ maxWidth: '800px', margin: '0 auto' }}>
        <h1 style={{
          fontSize: typography.fontSize['3xl'],
          fontWeight: typography.fontWeight.bold,
          color: colors.textPrimary,
          marginBottom: spacing.xl,
        }}>
          Export Pattern
        </h1>

        <div style={{ backgroundColor: colors.surface, padding: spacing.xl, borderRadius: borderRadius.lg, textAlign: 'center' }}>
          <p style={{ fontSize: typography.fontSize.lg, color: colors.textSecondary }}>
            Export functionality will be available after generating or parsing a pattern.
          </p>
        </div>
      </div>
    </div>
  );
}
