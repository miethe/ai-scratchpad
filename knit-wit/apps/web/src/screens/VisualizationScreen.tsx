import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { useVisualizationStore } from '../stores/useVisualizationStore';
import { useSettingsStore } from '../stores/useSettingsStore';
import { patternApi } from '../services/api';
import type { PatternDSL } from '../types';
import { colors, spacing, borderRadius, typography } from '../theme';

export default function VisualizationScreen() {
  const location = useLocation();
  const pattern = (location.state as { pattern?: PatternDSL })?.pattern;
  const { kidMode } = useSettingsStore();

  const {
    frames,
    currentRound,
    loading,
    error,
    setFrames,
    setLoading,
    setError,
    nextRound,
    prevRound,
    setCurrentRound,
  } = useVisualizationStore();

  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);

  useEffect(() => {
    if (pattern) {
      loadVisualization();
    }
  }, [pattern]);

  const loadVisualization = async () => {
    if (!pattern) return;

    setLoading(true);
    setError(null);

    try {
      const response = await patternApi.visualize(pattern);
      setFrames(response.frames, response.shape_type);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load visualization');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div style={{ minHeight: '100vh', backgroundColor: colors.background, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: typography.fontSize['2xl'], color: colors.textPrimary, marginBottom: spacing.md }}>
            {kidMode ? 'Drawing your pattern...' : 'Generating visualization...'}
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ minHeight: '100vh', backgroundColor: colors.background, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ textAlign: 'center', maxWidth: '500px', padding: spacing.lg }}>
          <div style={{ fontSize: typography.fontSize.xl, color: colors.error, marginBottom: spacing.md }}>
            Error
          </div>
          <p style={{ color: colors.textSecondary, marginBottom: spacing.lg }}>
            {error}
          </p>
          <button
            onClick={loadVisualization}
            style={{
              padding: `${spacing.md} ${spacing.lg}`,
              backgroundColor: colors.primary,
              color: colors.textInverse,
              border: 'none',
              borderRadius: borderRadius.md,
              cursor: 'pointer',
            }}
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (!pattern || frames.length === 0) {
    return (
      <div style={{ minHeight: '100vh', backgroundColor: colors.background, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ textAlign: 'center', padding: spacing.lg }}>
          <p style={{ fontSize: typography.fontSize.lg, color: colors.textSecondary }}>
            {kidMode ? 'No picture to show right now' : 'No visualization data available'}
          </p>
        </div>
      </div>
    );
  }

  const currentFrame = frames[currentRound - 1];

  return (
    <div style={{ minHeight: '100vh', backgroundColor: colors.background }}>
      {/* Visualization area */}
      <div style={{
        minHeight: '60vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: spacing.xl,
        backgroundColor: colors.surface,
      }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: typography.fontSize['4xl'], color: colors.textPrimary, marginBottom: spacing.lg }}>
            {kidMode ? `Step ${currentRound}` : `Round ${currentRound}`}
          </div>
          <div style={{ fontSize: typography.fontSize.xl, color: colors.textSecondary }}>
            {currentFrame?.stitch_count} {kidMode ? 'stitches' : 'st'}
          </div>
          <div style={{ marginTop: spacing.xl, padding: spacing.xl, backgroundColor: colors.background, borderRadius: borderRadius.lg }}>
            <svg width="400" height="400" viewBox="-200 -200 400 400">
              {/* Render edges (lines connecting stitches) */}
              {currentFrame?.edges.map((edge, idx) => {
                const sourceNode = currentFrame.nodes.find((n) => n.id === edge.source);
                const targetNode = currentFrame.nodes.find((n) => n.id === edge.target);
                if (!sourceNode || !targetNode) return null;

                return (
                  <line
                    key={`edge-${idx}`}
                    x1={sourceNode.position[0]}
                    y1={sourceNode.position[1]}
                    x2={targetNode.position[0]}
                    y2={targetNode.position[1]}
                    stroke={colors.border}
                    strokeWidth="1.5"
                  />
                );
              })}

              {/* Render nodes (stitches as circles) */}
              {currentFrame?.nodes.map((node) => {
                const isSelected = selectedNodeId === node.id;
                let fillColor: string = colors.stitchNormal;

                if (node.highlight === 'increase') {
                  fillColor = colors.stitchIncrease;
                } else if (node.highlight === 'decrease') {
                  fillColor = colors.stitchDecrease;
                }

                return (
                  <g key={node.id}>
                    <circle
                      cx={node.position[0]}
                      cy={node.position[1]}
                      r={isSelected ? 8 : 6}
                      fill={fillColor}
                      stroke={isSelected ? colors.primary : colors.border}
                      strokeWidth={isSelected ? 2 : 1}
                      onClick={() => setSelectedNodeId(node.id)}
                      style={{ cursor: 'pointer' }}
                    />
                    {isSelected && (
                      <text
                        x={node.position[0]}
                        y={node.position[1] - 15}
                        textAnchor="middle"
                        fontSize="12"
                        fill={colors.textPrimary}
                      >
                        {node.stitch_type}
                      </text>
                    )}
                  </g>
                );
              })}
            </svg>
          </div>
        </div>
      </div>

      {/* Round controls */}
      <div style={{ padding: spacing.lg, backgroundColor: colors.background }}>
        <div style={{ maxWidth: '800px', margin: '0 auto' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: spacing.md, marginBottom: spacing.md }}>
            <button
              onClick={prevRound}
              disabled={currentRound === 1}
              style={{
                padding: spacing.md,
                backgroundColor: currentRound === 1 ? colors.surfaceSecondary : colors.primary,
                color: currentRound === 1 ? colors.textSecondary : colors.textInverse,
                border: 'none',
                borderRadius: borderRadius.md,
                cursor: currentRound === 1 ? 'not-allowed' : 'pointer',
                flex: 1,
              }}
            >
              ← Previous
            </button>

            <div style={{ flex: 2, textAlign: 'center' }}>
              <div style={{ fontSize: typography.fontSize.sm, color: colors.textSecondary, marginBottom: spacing.xs }}>
                {kidMode ? 'Step' : 'Round'}
              </div>
              <input
                type="range"
                min="1"
                max={frames.length}
                value={currentRound}
                onChange={(e) => setCurrentRound(parseInt(e.target.value))}
                style={{ width: '100%' }}
              />
              <div style={{ fontSize: typography.fontSize.lg, color: colors.textPrimary }}>
                {currentRound} of {frames.length}
              </div>
            </div>

            <button
              onClick={nextRound}
              disabled={currentRound === frames.length}
              style={{
                padding: spacing.md,
                backgroundColor: currentRound === frames.length ? colors.surfaceSecondary : colors.primary,
                color: currentRound === frames.length ? colors.textSecondary : colors.textInverse,
                border: 'none',
                borderRadius: borderRadius.md,
                cursor: currentRound === frames.length ? 'not-allowed' : 'pointer',
                flex: 1,
              }}
            >
              Next →
            </button>
          </div>

          {/* Legend */}
          <div style={{ display: 'flex', gap: spacing.md, justifyContent: 'center', flexWrap: 'wrap' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: spacing.xs }}>
              <div style={{ width: '16px', height: '16px', borderRadius: '50%', backgroundColor: colors.stitchNormal }}></div>
              <span style={{ fontSize: typography.fontSize.sm, color: colors.textSecondary }}>Normal</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: spacing.xs }}>
              <div style={{ width: '16px', height: '16px', borderRadius: '50%', backgroundColor: colors.stitchIncrease }}></div>
              <span style={{ fontSize: typography.fontSize.sm, color: colors.textSecondary }}>Increase</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: spacing.xs }}>
              <div style={{ width: '16px', height: '16px', borderRadius: '50%', backgroundColor: colors.stitchDecrease }}></div>
              <span style={{ fontSize: typography.fontSize.sm, color: colors.textSecondary }}>Decrease</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
