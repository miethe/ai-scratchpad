import axios from 'axios';
import type { PatternRequest, PatternDSL } from '../types';
import type { VisualizationResponse } from '../types/visualization';

// API configuration
// In production, this would come from environment variables
const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Pattern API service
 * Handles communication with the FastAPI backend
 */
export const patternApi = {
  /**
   * Generate a new pattern
   */
  async generate(request: PatternRequest): Promise<{ dsl: PatternDSL }> {
    const response = await apiClient.post('/patterns/generate', request);
    return response.data;
  },

  /**
   * Visualize a pattern - convert DSL to frames
   */
  async visualize(dsl: PatternDSL): Promise<VisualizationResponse> {
    const response = await apiClient.post('/visualization/frames', dsl);
    return response.data;
  },

  /**
   * Export pattern to PDF
   */
  async exportPdf(dsl: PatternDSL): Promise<{ url: string }> {
    const response = await apiClient.post('/export/pdf', { dsl });
    return response.data;
  },
};

export default apiClient;
