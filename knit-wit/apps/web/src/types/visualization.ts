/**
 * Visualization types matching backend VisualizationResponse API
 * Used for storing and rendering pattern visualization frames
 */

export interface RenderNode {
  id: string;
  stitch_type: string;
  position: [number, number];
  highlight: 'normal' | 'increase' | 'decrease';
  // 3D mode specific fields (optional for backward compatibility)
  position_3d?: [number, number, number];
  depth_order?: number;
  depth_factor?: number;
}

export interface RenderEdge {
  source: string;
  target: string;
}

export interface ProjectionInfo {
  type: 'isometric';
  angle_deg: number;
  bounds_3d: {
    x_min: number;
    x_max: number;
    y_min: number;
    y_max: number;
    z_min: number;
    z_max: number;
  };
}

export interface VisualizationFrame {
  round_number: number;
  nodes: RenderNode[];
  edges: RenderEdge[];
  stitch_count: number;
  highlights: string[];
  // 3D mode specific field (optional for backward compatibility)
  projection?: ProjectionInfo;
}

export interface VisualizationResponse {
  frames: VisualizationFrame[];
  total_rounds: number;
  shape_type: string;
}

export type VisualizationMode = '2d' | '3d';
