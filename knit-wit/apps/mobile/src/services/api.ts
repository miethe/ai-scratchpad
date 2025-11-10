import axios from 'axios';
import type { PatternRequest, PatternDSL } from '../types';

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
 * Placeholder implementations for MVP Phase 0
 * These will be fully implemented when backend integration happens
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
   * Visualize a pattern
   */
  async visualize(dsl: PatternDSL): Promise<{ frames: unknown[] }> {
    const response = await apiClient.post('/patterns/visualize', { dsl });
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
