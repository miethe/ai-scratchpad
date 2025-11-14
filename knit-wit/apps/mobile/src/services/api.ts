import type { PatternRequest, PatternDSL } from '../types';
import type { VisualizationResponse } from '../types/visualization';

// API configuration
// In production, this would come from environment variables
const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

/**
 * API Error class for standardized error handling
 */
export class ApiError extends Error {
  constructor(
    public status: number,
    public statusText: string,
    public data?: any,
    message?: string
  ) {
    super(message || `API Error: ${status} ${statusText}`);
    this.name = 'ApiError';
  }
}

/**
 * Fetch wrapper with timeout support
 */
async function fetchWithTimeout(
  url: string,
  options: RequestInit,
  timeout: number = 10000
): Promise<Response> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
    });
    clearTimeout(timeoutId);
    return response;
  } catch (error) {
    clearTimeout(timeoutId);
    if (error instanceof Error && error.name === 'AbortError') {
      throw new ApiError(0, 'Request Timeout', null, 'Request timed out');
    }
    throw error;
  }
}

/**
 * Generic API request handler
 */
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;

  const response = await fetchWithTimeout(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  // Parse response
  let data;
  const contentType = response.headers.get('content-type');
  if (contentType && contentType.includes('application/json')) {
    data = await response.json();
  } else {
    data = await response.text();
  }

  // Handle non-2xx responses
  if (!response.ok) {
    throw new ApiError(
      response.status,
      response.statusText,
      data,
      data?.message || data?.error || `Request failed: ${response.statusText}`
    );
  }

  return data;
}

/**
 * Parser validation response
 */
export interface ParserValidationResult {
  valid: boolean;
  errors: Array<{
    message: string;
    line?: number;
  }>;
}

/**
 * Parser response
 */
export interface ParserResponse {
  dsl: PatternDSL;
  validation: ParserValidationResult;
}

/**
 * Pattern API service
 * Handles communication with the FastAPI backend
 */
export const patternApi = {
  /**
   * Generate a new pattern
   */
  async generate(request: PatternRequest): Promise<{ dsl: PatternDSL }> {
    return apiRequest<{ dsl: PatternDSL }>('/patterns/generate', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  },

  /**
   * Parse and validate a pattern text
   */
  async parse(text: string): Promise<ParserResponse> {
    return apiRequest<ParserResponse>('/parser/parse', {
      method: 'POST',
      body: JSON.stringify({ text }),
    });
  },

  /**
   * Visualize a pattern - convert DSL to frames
   */
  async visualize(dsl: PatternDSL): Promise<VisualizationResponse> {
    return apiRequest<VisualizationResponse>('/visualization/frames', {
      method: 'POST',
      body: JSON.stringify(dsl),
    });
  },

  /**
   * Export pattern to PDF
   */
  async exportPdf(dsl: PatternDSL): Promise<{ url: string }> {
    return apiRequest<{ url: string }>('/export/pdf', {
      method: 'POST',
      body: JSON.stringify({ dsl }),
    });
  },
};

/**
 * Legacy apiClient export for backward compatibility
 * Note: This is a minimal implementation. For full axios compatibility,
 * consider using a more complete adapter if needed.
 */
export const apiClient = {
  get: <T = any>(url: string, config?: RequestInit) =>
    apiRequest<T>(url, { method: 'GET', ...config }).then(data => ({ data })),

  post: <T = any>(url: string, body?: any, config?: RequestInit) =>
    apiRequest<T>(url, {
      method: 'POST',
      body: body ? JSON.stringify(body) : undefined,
      ...config,
    }).then(data => ({ data })),

  put: <T = any>(url: string, body?: any, config?: RequestInit) =>
    apiRequest<T>(url, {
      method: 'PUT',
      body: body ? JSON.stringify(body) : undefined,
      ...config,
    }).then(data => ({ data })),

  delete: <T = any>(url: string, config?: RequestInit) =>
    apiRequest<T>(url, { method: 'DELETE', ...config }).then(data => ({ data })),
};

export default apiClient;
