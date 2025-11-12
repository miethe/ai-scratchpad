import { create } from 'zustand';
import type { VisualizationFrame } from '../types/visualization';

interface VisualizationState {
  // Frame data from API
  frames: VisualizationFrame[];
  totalRounds: number;
  shapeType: string | null;

  // Current viewing state
  currentRound: number;

  // Loading and error state
  loading: boolean;
  error: string | null;

  // Display preferences
  zoomLevel: number;
  isPanning: boolean;
  panOffset: { x: number; y: number };
  highlightChanges: boolean;
  showStitchCount: boolean;
  showRoundNumbers: boolean;
  animationSpeed: 'slow' | 'medium' | 'fast';

  // Visualization mode
  viewMode: '2D' | '3D';

  // Frame management actions
  setFrames: (frames: VisualizationFrame[], shapeType?: string | null) => void;
  setCurrentRound: (round: number) => void;
  nextRound: () => void;
  prevRound: () => void;
  jumpToRound: (round: number) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;

  // Zoom actions
  setZoomLevel: (level: number) => void;
  zoomIn: () => void;
  zoomOut: () => void;
  resetZoom: () => void;

  // Pan actions
  setPanning: (isPanning: boolean) => void;
  setPanOffset: (offset: { x: number; y: number }) => void;
  resetPan: () => void;

  // Preference actions
  setHighlightChanges: (enabled: boolean) => void;
  setShowStitchCount: (enabled: boolean) => void;
  setShowRoundNumbers: (enabled: boolean) => void;
  setAnimationSpeed: (speed: 'slow' | 'medium' | 'fast') => void;
  setViewMode: (mode: '2D' | '3D') => void;

  // Reset
  resetVisualization: () => void;
}

const DEFAULT_ZOOM = 1.0;
const MIN_ZOOM = 0.5;
const MAX_ZOOM = 3.0;
const ZOOM_STEP = 0.25;

export const useVisualizationStore = create<VisualizationState>((set, get) => ({
  // Frame data
  frames: [],
  totalRounds: 0,
  shapeType: null,

  // Current state (1-indexed for UI)
  currentRound: 1,

  // Loading/error
  loading: false,
  error: null,

  // Display preferences
  zoomLevel: DEFAULT_ZOOM,
  isPanning: false,
  panOffset: { x: 0, y: 0 },
  highlightChanges: true,
  showStitchCount: true,
  showRoundNumbers: true,
  animationSpeed: 'medium',
  viewMode: '2D',

  // Frame management actions
  setFrames: (frames, shapeType = null) =>
    set({
      frames,
      totalRounds: frames.length,
      shapeType,
      currentRound: frames.length > 0 ? 1 : 1,
      error: null, // Clear error on successful frame load
    }),

  setCurrentRound: (round) => {
    const { totalRounds } = get();
    if (round >= 1 && round <= totalRounds) {
      set({ currentRound: round });
    }
  },

  nextRound: () => {
    const { currentRound, totalRounds } = get();
    if (currentRound < totalRounds) {
      set({ currentRound: currentRound + 1 });
    }
  },

  prevRound: () => {
    const { currentRound } = get();
    if (currentRound > 1) {
      set({ currentRound: currentRound - 1 });
    }
  },

  jumpToRound: (round) => {
    const { totalRounds } = get();
    const boundedRound = Math.max(1, Math.min(round, totalRounds));
    set({ currentRound: boundedRound });
  },

  setLoading: (loading) => set({ loading }),

  setError: (error) => set({ error }),

  // Zoom actions
  setZoomLevel: (level) => {
    const clampedZoom = Math.max(MIN_ZOOM, Math.min(MAX_ZOOM, level));
    set({ zoomLevel: clampedZoom });
  },

  zoomIn: () => {
    const { zoomLevel } = get();
    const newZoom = Math.min(MAX_ZOOM, zoomLevel + ZOOM_STEP);
    set({ zoomLevel: newZoom });
  },

  zoomOut: () => {
    const { zoomLevel } = get();
    const newZoom = Math.max(MIN_ZOOM, zoomLevel - ZOOM_STEP);
    set({ zoomLevel: newZoom });
  },

  resetZoom: () => set({ zoomLevel: DEFAULT_ZOOM }),

  // Pan actions
  setPanning: (isPanning) => set({ isPanning }),

  setPanOffset: (offset) => set({ panOffset: offset }),

  resetPan: () => set({ panOffset: { x: 0, y: 0 } }),

  // Preference actions
  setHighlightChanges: (enabled) => set({ highlightChanges: enabled }),

  setShowStitchCount: (enabled) => set({ showStitchCount: enabled }),

  setShowRoundNumbers: (enabled) => set({ showRoundNumbers: enabled }),

  setAnimationSpeed: (speed) => set({ animationSpeed: speed }),

  setViewMode: (mode) => set({ viewMode: mode }),

  // Reset
  resetVisualization: () =>
    set({
      frames: [],
      totalRounds: 0,
      shapeType: null,
      currentRound: 1,
      loading: false,
      error: null,
      zoomLevel: DEFAULT_ZOOM,
      isPanning: false,
      panOffset: { x: 0, y: 0 },
      highlightChanges: true,
      showStitchCount: true,
      showRoundNumbers: true,
      animationSpeed: 'medium',
      viewMode: '2D',
    }),
}));
