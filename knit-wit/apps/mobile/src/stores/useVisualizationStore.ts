import { create } from 'zustand';

interface VisualizationState {
  // Current viewing state
  currentRound: number;
  zoomLevel: number;
  isPanning: boolean;
  panOffset: { x: number; y: number };

  // Display preferences
  highlightChanges: boolean;
  showStitchCount: boolean;
  showRoundNumbers: boolean;
  animationSpeed: 'slow' | 'medium' | 'fast';

  // Visualization mode
  viewMode: '2D' | '3D';

  // Actions
  setCurrentRound: (round: number) => void;
  nextRound: () => void;
  previousRound: () => void;
  setZoomLevel: (level: number) => void;
  zoomIn: () => void;
  zoomOut: () => void;
  resetZoom: () => void;
  setPanning: (isPanning: boolean) => void;
  setPanOffset: (offset: { x: number; y: number }) => void;
  resetPan: () => void;
  setHighlightChanges: (enabled: boolean) => void;
  setShowStitchCount: (enabled: boolean) => void;
  setShowRoundNumbers: (enabled: boolean) => void;
  setAnimationSpeed: (speed: 'slow' | 'medium' | 'fast') => void;
  setViewMode: (mode: '2D' | '3D') => void;
  resetVisualization: () => void;
}

const DEFAULT_ZOOM = 1.0;
const MIN_ZOOM = 0.5;
const MAX_ZOOM = 3.0;
const ZOOM_STEP = 0.25;

export const useVisualizationStore = create<VisualizationState>((set, get) => ({
  // Initial state
  currentRound: 0,
  zoomLevel: DEFAULT_ZOOM,
  isPanning: false,
  panOffset: { x: 0, y: 0 },
  highlightChanges: true,
  showStitchCount: true,
  showRoundNumbers: true,
  animationSpeed: 'medium',
  viewMode: '2D',

  // Actions
  setCurrentRound: (round) => set({ currentRound: Math.max(0, round) }),

  nextRound: () => {
    const { currentRound } = get();
    set({ currentRound: currentRound + 1 });
  },

  previousRound: () => {
    const { currentRound } = get();
    set({ currentRound: Math.max(0, currentRound - 1) });
  },

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

  setPanning: (isPanning) => set({ isPanning }),

  setPanOffset: (offset) => set({ panOffset: offset }),

  resetPan: () => set({ panOffset: { x: 0, y: 0 } }),

  setHighlightChanges: (enabled) => set({ highlightChanges: enabled }),

  setShowStitchCount: (enabled) => set({ showStitchCount: enabled }),

  setShowRoundNumbers: (enabled) => set({ showRoundNumbers: enabled }),

  setAnimationSpeed: (speed) => set({ animationSpeed: speed }),

  setViewMode: (mode) => set({ viewMode: mode }),

  resetVisualization: () =>
    set({
      currentRound: 0,
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
