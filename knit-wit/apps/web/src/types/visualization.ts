/**
 * Visualization types matching backend VisualizationResponse API
 * Used for storing and rendering pattern visualization frames
 */

export interface RenderNode {
  id: string;
  stitch_type: string;
  position: [number, number];
  highlight: 'normal' | 'increase' | 'decrease';
}

export interface RenderEdge {
  source: string;
  target: string;
}

export interface VisualizationFrame {
  round_number: number;
  nodes: RenderNode[];
  edges: RenderEdge[];
  stitch_count: number;
  highlights: string[];
}

export interface VisualizationResponse {
  frames: VisualizationFrame[];
  total_rounds: number;
  shape_type: string;
}
