import { create } from 'zustand';
import type { PatternDSL, PatternRequest } from '../types';

interface PatternState {
  // Current pattern state
  currentPattern: PatternDSL | null;
  isGenerating: boolean;
  error: string | null;

  // Pattern history (for MVP, kept in memory only)
  recentPatterns: PatternDSL[];

  // Actions
  generatePattern: (request: PatternRequest) => Promise<void>;
  clearPattern: () => void;
  setError: (error: string | null) => void;
  addToHistory: (pattern: PatternDSL) => void;
}

export const usePatternStore = create<PatternState>((set, get) => ({
  // Initial state
  currentPattern: null,
  isGenerating: false,
  error: null,
  recentPatterns: [],

  // Actions
  generatePattern: async (request: PatternRequest) => {
    set({ isGenerating: true, error: null });
    try {
      // Placeholder for API call
      // In later phases, this will call the backend API
      // const response = await patternApi.generate(request);
      // set({ currentPattern: response.dsl, isGenerating: false });

      // For now, just simulate a delay
      await new Promise((resolve) => setTimeout(resolve, 1000));

      // Mock pattern data
      const mockPattern: PatternDSL = {
        meta: {
          version: '0.1',
          units: request.units,
          terms: request.terms,
          stitch: request.stitch,
          round_mode: 'spiral',
          gauge: request.gauge,
        },
        object: {
          type: request.shape,
          params: { diameter: request.diameter || 10 },
        },
        rounds: [],
        materials: {
          yarn_weight: 'Worsted',
          hook_size_mm: 4.0,
          yardage_estimate: 25,
        },
        notes: ['Work in a spiral; use a stitch marker.'],
      };

      set({ currentPattern: mockPattern, isGenerating: false });
      get().addToHistory(mockPattern);
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to generate pattern',
        isGenerating: false,
      });
    }
  },

  clearPattern: () => set({ currentPattern: null, error: null }),

  setError: (error) => set({ error }),

  addToHistory: (pattern) => {
    const { recentPatterns } = get();
    // Keep only the last 10 patterns
    const updated = [pattern, ...recentPatterns].slice(0, 10);
    set({ recentPatterns: updated });
  },
}));
