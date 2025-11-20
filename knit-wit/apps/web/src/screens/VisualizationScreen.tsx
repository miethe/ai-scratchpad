import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { useVisualizationStore } from '../stores/useVisualizationStore';
import { useSettingsStore } from '../stores/useSettingsStore';
import { patternApi } from '../services/api';
import type { PatternDSL } from '../types';
import type { RenderNode, VisualizationMode } from '../types/visualization';
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
    visualizationMode,
    setFrames,
    setLoading,
    setError,
    nextRound,
    prevRound,
    setCurrentRound,
    setVisualizationMode,
  } = useVisualizationStore();

  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);

  useEffect(() => {
    if (pattern) {
      loadVisualization();
    }
  }, [pattern, visualizationMode]);

  const loadVisualization = async () => {
    if (!pattern) return;

    setLoading(true);
    setError(null);

    try {
      const response = await patternApi.visualize(pattern, visualizationMode);
      setFrames(response.frames, response.shape_type);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load visualization');
    } finally {
      setLoading(false);
    }
  };

  const handleModeToggle = (mode: VisualizationMode) => {
    if (mode !== visualizationMode) {
      setVisualizationMode(mode);
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

  // Sort nodes by depth order for 3D rendering (painter's algorithm)
  const getSortedNodes = () => {
    if (!currentFrame) return [];

    if (visualizationMode === '3d') {
      // Sort by depth_order (lower values render first, behind higher values)
      return [...currentFrame.nodes].sort((a, b) => {
        const depthA = a.depth_order ?? 0;
        const depthB = b.depth_order ?? 0;
        return depthA - depthB;
      });
    }

    return currentFrame.nodes;
  };

  // Calculate 3D depth-based visual properties
  const getNodeVisualProps = (node: RenderNode) => {
    const baseRadius = 6;
    const selectedRadius = 8;
    const isSelected = selectedNodeId === node.id;

    if (visualizationMode === '3d' && node.depth_factor !== undefined) {
      // Size: Scale radius by 0.6 + (depth_factor * 0.4) = 60-100%
      const depthScale = 0.6 + (node.depth_factor * 0.4);
      const radius = isSelected ? selectedRadius * depthScale : baseRadius * depthScale;

      // Opacity: 0.7 + (depth_factor * 0.3) = 70-100%
      const opacity = 0.7 + (node.depth_factor * 0.3);

      return { radius, opacity };
    }

    return {
      radius: isSelected ? selectedRadius : baseRadius,
      opacity: 1,
    };
  };

  const getNodeColor = (node: RenderNode) => {
    if (node.highlight === 'increase') {
      return colors.stitchIncrease;
    } else if (node.highlight === 'decrease') {
      return colors.stitchDecrease;
    }
    return colors.stitchNormal;
  };

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
        <div style={{ textAlign: 'center', width: '100%', maxWidth: '600px' }}>
          {/* 2D/3D Toggle */}
          <div style={{
            display: 'flex',
            justifyContent: 'center',
            gap: spacing.xs,
            marginBottom: spacing.lg,
            backgroundColor: colors.surfaceSecondary,
            borderRadius: borderRadius.md,
            padding: spacing.xs,
            width: 'fit-content',
            margin: '0 auto',
          }}>
            <button
              onClick={() => handleModeToggle('2d')}
              aria-label="2D View"
              aria-pressed={visualizationMode === '2d'}
              style={{
                padding: `${spacing.sm} ${spacing.md}`,
                backgroundColor: visualizationMode === '2d' ? colors.primary : 'transparent',
                color: visualizationMode === '2d' ? colors.textInverse : colors.textSecondary,
                border: 'none',
                borderRadius: borderRadius.sm,
                cursor: 'pointer',
                fontSize: typography.fontSize.sm,
                fontWeight: typography.fontWeight.medium,
                transition: 'all 150ms ease-in-out',
                minWidth: '80px',
              }}
            >
              2D View
            </button>
            <button
              onClick={() => handleModeToggle('3d')}
              aria-label="3D View"
              aria-pressed={visualizationMode === '3d'}
              style={{
                padding: `${spacing.sm} ${spacing.md}`,
                backgroundColor: visualizationMode === '3d' ? colors.primary : 'transparent',
                color: visualizationMode === '3d' ? colors.textInverse : colors.textSecondary,
                border: 'none',
                borderRadius: borderRadius.sm,
                cursor: 'pointer',
                fontSize: typography.fontSize.sm,
                fontWeight: typography.fontWeight.medium,
                transition: 'all 150ms ease-in-out',
                minWidth: '80px',
              }}
            >
              3D View
            </button>
          </div>

          <div style={{ fontSize: typography.fontSize['4xl'], color: colors.textPrimary, marginBottom: spacing.lg }}>
            {kidMode ? `Step ${currentRound}` : `Round ${currentRound}`}
          </div>
          <div style={{ fontSize: typography.fontSize.xl, color: colors.textSecondary }}>
            {currentFrame?.stitch_count} {kidMode ? 'stitches' : 'st'}
          </div>
          <div style={{ marginTop: spacing.xl, padding: spacing.xl, backgroundColor: colors.background, borderRadius: borderRadius.lg }}>
            <svg width="400" height="400" viewBox="-200 -200 400 400">
              {/* Render edges first (behind nodes) */}
              {currentFrame?.edges.map((edge, idx) => {
                const sourceNode = currentFrame.nodes.find((n) => n.id === edge.source);
                const targetNode = currentFrame.nodes.find((n) => n.id === edge.target);
                if (!sourceNode || !targetNode) return null;

                // In 3D mode, use slightly reduced opacity for edges
                const edgeOpacity = visualizationMode === '3d' ? 0.4 : 0.6;

                return (
                  <line
                    key={`edge-${idx}`}
                    x1={sourceNode.position[0]}
                    y1={sourceNode.position[1]}
                    x2={targetNode.position[0]}
                    y2={targetNode.position[1]}
                    stroke={colors.border}
                    strokeWidth="1.5"
                    opacity={edgeOpacity}
                  />
                );
              })}

              {/* Render nodes in depth order */}
              {getSortedNodes().map((node) => {
                const isSelected = selectedNodeId === node.id;
                const fillColor = getNodeColor(node);
                const { radius, opacity } = getNodeVisualProps(node);

                // In 3D mode, add subtle shading for depth perception
                const useShading = visualizationMode === '3d' && node.depth_factor !== undefined;
                const lighterFill = useShading
                  ? `rgba(255, 255, 255, ${0.2 * node.depth_factor!})`
                  : 'transparent';

                return (
                  <g key={node.id} opacity={opacity}>
                    {/* Main circle */}
                    <circle
                      cx={node.position[0]}
                      cy={node.position[1]}
                      r={radius}
                      fill={fillColor}
                      stroke={isSelected ? colors.primary : colors.border}
                      strokeWidth={isSelected ? 2 : 1}
                      onClick={() => setSelectedNodeId(node.id)}
                      style={{ cursor: 'pointer' }}
                    />
                    {/* Shading overlay for 3D depth */}
                    {useShading && (
                      <circle
                        cx={node.position[0] - radius * 0.2}
                        cy={node.position[1] - radius * 0.2}
                        r={radius * 0.6}
                        fill={lighterFill}
                        pointerEvents="none"
                      />
                    )}
                    {/* Label for selected node */}
                    {isSelected && (
                      <text
                        x={node.position[0]}
                        y={node.position[1] - radius - 8}
                        textAnchor="middle"
                        fontSize="12"
                        fill={colors.textPrimary}
                        fontWeight={typography.fontWeight.medium}
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
