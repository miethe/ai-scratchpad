import { renderHook, act } from '@testing-library/react-native';
import { useVisualizationStore } from '../../src/stores/useVisualizationStore';
import type { VisualizationFrame } from '../../src/types/visualization';

describe('useVisualizationStore', () => {
  beforeEach(() => {
    // Reset store before each test
    const { result } = renderHook(() => useVisualizationStore());
    act(() => {
      result.current.resetVisualization();
    });
  });

  describe('initial state', () => {
    it('initializes with empty frames', () => {
      const { result } = renderHook(() => useVisualizationStore());

      expect(result.current.frames).toEqual([]);
      expect(result.current.totalRounds).toBe(0);
      expect(result.current.shapeType).toBeNull();
      expect(result.current.currentRound).toBe(1);
      expect(result.current.loading).toBe(false);
      expect(result.current.error).toBeNull();
    });

    it('initializes with default display preferences', () => {
      const { result } = renderHook(() => useVisualizationStore());

      expect(result.current.zoomLevel).toBe(1.0);
      expect(result.current.isPanning).toBe(false);
      expect(result.current.panOffset).toEqual({ x: 0, y: 0 });
      expect(result.current.highlightChanges).toBe(true);
      expect(result.current.showStitchCount).toBe(true);
      expect(result.current.showRoundNumbers).toBe(true);
      expect(result.current.animationSpeed).toBe('medium');
      expect(result.current.viewMode).toBe('2D');
    });
  });

  describe('frame management', () => {
    const mockFrames: VisualizationFrame[] = [
      {
        round_number: 1,
        nodes: [],
        edges: [],
        stitch_count: 6,
        highlights: [],
      },
      {
        round_number: 2,
        nodes: [],
        edges: [],
        stitch_count: 12,
        highlights: [],
      },
      {
        round_number: 3,
        nodes: [],
        edges: [],
        stitch_count: 18,
        highlights: [],
      },
    ];

    it('sets frames and updates totalRounds', () => {
      const { result } = renderHook(() => useVisualizationStore());

      act(() => {
        result.current.setFrames(mockFrames);
      });

      expect(result.current.frames).toHaveLength(3);
      expect(result.current.totalRounds).toBe(3);
      expect(result.current.currentRound).toBe(1);
    });

    it('sets frames with shape type', () => {
      const { result } = renderHook(() => useVisualizationStore());

      act(() => {
        result.current.setFrames(mockFrames, 'sphere');
      });

      expect(result.current.shapeType).toBe('sphere');
      expect(result.current.frames).toHaveLength(3);
    });

    it('clears error when setting frames', () => {
      const { result } = renderHook(() => useVisualizationStore());

      act(() => {
        result.current.setError('Previous error');
      });

      expect(result.current.error).toBe('Previous error');

      act(() => {
        result.current.setFrames(mockFrames);
      });

      expect(result.current.error).toBeNull();
    });

    it('handles empty frames array', () => {
      const { result } = renderHook(() => useVisualizationStore());

      act(() => {
        result.current.setFrames([]);
      });

      expect(result.current.frames).toEqual([]);
      expect(result.current.totalRounds).toBe(0);
      expect(result.current.currentRound).toBe(1);
    });
  });

  describe('round navigation', () => {
    const mockFrames: VisualizationFrame[] = [
      { round_number: 1, nodes: [], edges: [], stitch_count: 6, highlights: [] },
      { round_number: 2, nodes: [], edges: [], stitch_count: 12, highlights: [] },
      { round_number: 3, nodes: [], edges: [], stitch_count: 18, highlights: [] },
    ];

    beforeEach(() => {
      const { result } = renderHook(() => useVisualizationStore());
      act(() => {
        result.current.setFrames(mockFrames);
      });
    });

    it('navigates to next round', () => {
      const { result } = renderHook(() => useVisualizationStore());

      expect(result.current.currentRound).toBe(1);

      act(() => {
        result.current.nextRound();
      });

      expect(result.current.currentRound).toBe(2);

      act(() => {
        result.current.nextRound();
      });

      expect(result.current.currentRound).toBe(3);
    });

    it('does not go beyond last round', () => {
      const { result } = renderHook(() => useVisualizationStore());

      act(() => {
        result.current.jumpToRound(3);
      });

      expect(result.current.currentRound).toBe(3);

      act(() => {
        result.current.nextRound();
      });

      expect(result.current.currentRound).toBe(3);
    });

    it('navigates to previous round', () => {
      const { result } = renderHook(() => useVisualizationStore());

      act(() => {
        result.current.jumpToRound(3);
      });

      expect(result.current.currentRound).toBe(3);

      act(() => {
        result.current.prevRound();
      });

      expect(result.current.currentRound).toBe(2);

      act(() => {
        result.current.prevRound();
      });

      expect(result.current.currentRound).toBe(1);
    });

    it('does not go below first round', () => {
      const { result } = renderHook(() => useVisualizationStore());

      expect(result.current.currentRound).toBe(1);

      act(() => {
        result.current.prevRound();
      });

      expect(result.current.currentRound).toBe(1);
    });

    it('jumps to specific round', () => {
      const { result } = renderHook(() => useVisualizationStore());

      act(() => {
        result.current.jumpToRound(2);
      });

      expect(result.current.currentRound).toBe(2);
    });

    it('bounds jump to valid range', () => {
      const { result } = renderHook(() => useVisualizationStore());

      act(() => {
        result.current.jumpToRound(0);
      });

      expect(result.current.currentRound).toBe(1);

      act(() => {
        result.current.jumpToRound(10);
      });

      expect(result.current.currentRound).toBe(3);
    });

    it('sets current round directly within bounds', () => {
      const { result } = renderHook(() => useVisualizationStore());

      act(() => {
        result.current.setCurrentRound(2);
      });

      expect(result.current.currentRound).toBe(2);
    });

    it('does not set current round outside bounds', () => {
      const { result } = renderHook(() => useVisualizationStore());

      act(() => {
        result.current.setCurrentRound(10);
      });

      expect(result.current.currentRound).toBe(1);

      act(() => {
        result.current.setCurrentRound(0);
      });

      expect(result.current.currentRound).toBe(1);
    });
  });

  describe('loading and error states', () => {
    it('sets loading state', () => {
      const { result } = renderHook(() => useVisualizationStore());

      act(() => {
        result.current.setLoading(true);
      });

      expect(result.current.loading).toBe(true);

      act(() => {
        result.current.setLoading(false);
      });

      expect(result.current.loading).toBe(false);
    });

    it('sets error state', () => {
      const { result } = renderHook(() => useVisualizationStore());

      act(() => {
        result.current.setError('Network error');
      });

      expect(result.current.error).toBe('Network error');

      act(() => {
        result.current.setError(null);
      });

      expect(result.current.error).toBeNull();
    });
  });

  describe('zoom controls', () => {
    it('zooms in', () => {
      const { result } = renderHook(() => useVisualizationStore());

      expect(result.current.zoomLevel).toBe(1.0);

      act(() => {
        result.current.zoomIn();
      });

      expect(result.current.zoomLevel).toBe(1.25);

      act(() => {
        result.current.zoomIn();
      });

      expect(result.current.zoomLevel).toBe(1.5);
    });

    it('zooms out', () => {
      const { result } = renderHook(() => useVisualizationStore());

      expect(result.current.zoomLevel).toBe(1.0);

      act(() => {
        result.current.zoomOut();
      });

      expect(result.current.zoomLevel).toBe(0.75);

      act(() => {
        result.current.zoomOut();
      });

      expect(result.current.zoomLevel).toBe(0.5);
    });

    it('respects maximum zoom', () => {
      const { result } = renderHook(() => useVisualizationStore());

      act(() => {
        result.current.setZoomLevel(3.0);
      });

      expect(result.current.zoomLevel).toBe(3.0);

      act(() => {
        result.current.zoomIn();
      });

      expect(result.current.zoomLevel).toBe(3.0);
    });

    it('respects minimum zoom', () => {
      const { result } = renderHook(() => useVisualizationStore());

      act(() => {
        result.current.setZoomLevel(0.5);
      });

      expect(result.current.zoomLevel).toBe(0.5);

      act(() => {
        result.current.zoomOut();
      });

      expect(result.current.zoomLevel).toBe(0.5);
    });

    it('resets zoom', () => {
      const { result } = renderHook(() => useVisualizationStore());

      act(() => {
        result.current.zoomIn();
        result.current.zoomIn();
      });

      expect(result.current.zoomLevel).not.toBe(1.0);

      act(() => {
        result.current.resetZoom();
      });

      expect(result.current.zoomLevel).toBe(1.0);
    });
  });

  describe('pan controls', () => {
    it('sets panning state', () => {
      const { result } = renderHook(() => useVisualizationStore());

      act(() => {
        result.current.setPanning(true);
      });

      expect(result.current.isPanning).toBe(true);

      act(() => {
        result.current.setPanning(false);
      });

      expect(result.current.isPanning).toBe(false);
    });

    it('sets pan offset', () => {
      const { result } = renderHook(() => useVisualizationStore());

      act(() => {
        result.current.setPanOffset({ x: 10, y: 20 });
      });

      expect(result.current.panOffset).toEqual({ x: 10, y: 20 });
    });

    it('resets pan offset', () => {
      const { result } = renderHook(() => useVisualizationStore());

      act(() => {
        result.current.setPanOffset({ x: 10, y: 20 });
      });

      expect(result.current.panOffset).toEqual({ x: 10, y: 20 });

      act(() => {
        result.current.resetPan();
      });

      expect(result.current.panOffset).toEqual({ x: 0, y: 0 });
    });
  });

  describe('display preferences', () => {
    it('toggles highlight changes', () => {
      const { result } = renderHook(() => useVisualizationStore());

      expect(result.current.highlightChanges).toBe(true);

      act(() => {
        result.current.setHighlightChanges(false);
      });

      expect(result.current.highlightChanges).toBe(false);
    });

    it('toggles stitch count display', () => {
      const { result } = renderHook(() => useVisualizationStore());

      expect(result.current.showStitchCount).toBe(true);

      act(() => {
        result.current.setShowStitchCount(false);
      });

      expect(result.current.showStitchCount).toBe(false);
    });

    it('toggles round numbers display', () => {
      const { result } = renderHook(() => useVisualizationStore());

      expect(result.current.showRoundNumbers).toBe(true);

      act(() => {
        result.current.setShowRoundNumbers(false);
      });

      expect(result.current.showRoundNumbers).toBe(false);
    });

    it('changes animation speed', () => {
      const { result } = renderHook(() => useVisualizationStore());

      expect(result.current.animationSpeed).toBe('medium');

      act(() => {
        result.current.setAnimationSpeed('fast');
      });

      expect(result.current.animationSpeed).toBe('fast');

      act(() => {
        result.current.setAnimationSpeed('slow');
      });

      expect(result.current.animationSpeed).toBe('slow');
    });

    it('changes view mode', () => {
      const { result } = renderHook(() => useVisualizationStore());

      expect(result.current.viewMode).toBe('2D');

      act(() => {
        result.current.setViewMode('3D');
      });

      expect(result.current.viewMode).toBe('3D');
    });
  });

  describe('reset visualization', () => {
    it('resets all state to defaults', () => {
      const { result } = renderHook(() => useVisualizationStore());
      const mockFrames: VisualizationFrame[] = [
        { round_number: 1, nodes: [], edges: [], stitch_count: 6, highlights: [] },
      ];

      // Modify all state
      act(() => {
        result.current.setFrames(mockFrames, 'sphere');
        result.current.setLoading(true);
        result.current.setError('Test error');
        result.current.jumpToRound(1);
        result.current.setZoomLevel(2.0);
        result.current.setPanning(true);
        result.current.setPanOffset({ x: 50, y: 100 });
        result.current.setHighlightChanges(false);
        result.current.setShowStitchCount(false);
        result.current.setShowRoundNumbers(false);
        result.current.setAnimationSpeed('fast');
        result.current.setViewMode('3D');
      });

      // Reset
      act(() => {
        result.current.resetVisualization();
      });

      // Verify all defaults
      expect(result.current.frames).toEqual([]);
      expect(result.current.totalRounds).toBe(0);
      expect(result.current.shapeType).toBeNull();
      expect(result.current.currentRound).toBe(1);
      expect(result.current.loading).toBe(false);
      expect(result.current.error).toBeNull();
      expect(result.current.zoomLevel).toBe(1.0);
      expect(result.current.isPanning).toBe(false);
      expect(result.current.panOffset).toEqual({ x: 0, y: 0 });
      expect(result.current.highlightChanges).toBe(true);
      expect(result.current.showStitchCount).toBe(true);
      expect(result.current.showRoundNumbers).toBe(true);
      expect(result.current.animationSpeed).toBe('medium');
      expect(result.current.viewMode).toBe('2D');
    });
  });
});
