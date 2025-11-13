import AsyncStorage from '@react-native-async-storage/async-storage';
import axios, { AxiosError } from 'axios';
import { Platform } from 'react-native';

const TELEMETRY_CONSENT_KEY = '@knit-wit/telemetry_consent';

// Get API URL from environment or use default
const getApiBaseUrl = (): string => {
  try {
    return process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
  } catch {
    return 'http://localhost:8000/api/v1';
  }
};

interface TelemetryEvent {
  event: string;
  properties?: Record<string, any>;
  timestamp: string;
}

/**
 * TelemetryClient - Frontend SDK for tracking user events
 *
 * Respects user opt-out preferences and fails silently to avoid blocking UX.
 * Events are sent asynchronously to the backend telemetry endpoint.
 */
class TelemetryClient {
  private enabled: boolean = false;
  private apiUrl: string;
  private appVersion: string;

  constructor(apiUrl?: string, appVersion: string = '1.0.0') {
    this.apiUrl = apiUrl || getApiBaseUrl();
    this.appVersion = appVersion;
    this.loadConsent();
  }

  /**
   * Load consent preference from AsyncStorage
   */
  async loadConsent(): Promise<void> {
    try {
      const consent = await AsyncStorage.getItem(TELEMETRY_CONSENT_KEY);
      this.enabled = consent === 'true';
    } catch (error) {
      // Silent fail - default to disabled
      console.warn('Failed to load telemetry consent:', error);
      this.enabled = false;
    }
  }

  /**
   * Set user consent for telemetry tracking
   */
  async setConsent(enabled: boolean): Promise<void> {
    try {
      this.enabled = enabled;
      await AsyncStorage.setItem(TELEMETRY_CONSENT_KEY, enabled.toString());
    } catch (error) {
      console.warn('Failed to save telemetry consent:', error);
    }
  }

  /**
   * Get current consent status
   */
  getConsent(): boolean {
    return this.enabled;
  }

  /**
   * Track a generic event
   *
   * @param event - Event name (e.g., 'pattern_generated')
   * @param properties - Additional event properties
   */
  track(event: string, properties?: Record<string, any>): void {
    if (!this.enabled) {
      return; // Respect opt-out
    }

    const telemetryEvent: TelemetryEvent = {
      event,
      properties: {
        ...properties,
        platform: Platform.OS,
        version: this.appVersion,
      },
      timestamp: new Date().toISOString(),
    };

    // Fire and forget - don't block user experience
    this.sendEvent(telemetryEvent);
  }

  /**
   * Send event to backend API
   * Fails silently to avoid blocking user experience
   */
  private async sendEvent(event: TelemetryEvent): Promise<void> {
    try {
      await axios.post(
        `${this.apiUrl}/telemetry/events`,
        event,
        {
          timeout: 5000, // Don't wait more than 5 seconds
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );
    } catch (error) {
      // Silent fail - don't block user experience
      // Only log in development for debugging
      if (__DEV__) {
        if (error instanceof AxiosError) {
          console.warn('Telemetry error:', {
            message: error.message,
            status: error.response?.status,
            data: error.response?.data,
          });
        } else {
          console.warn('Telemetry error:', error);
        }
      }
    }
  }

  // Convenience methods for common events

  /**
   * Track pattern generation event
   */
  trackGeneration(shape: string, stitch: string, additionalProps?: Record<string, any>): void {
    this.track('pattern_generated', {
      shape_type: shape,
      stitch_type: stitch,
      ...additionalProps,
    });
  }

  /**
   * Track pattern visualization event
   */
  trackVisualization(roundCount: number, duration: number, additionalProps?: Record<string, any>): void {
    this.track('pattern_visualized', {
      round_count: roundCount,
      duration_ms: duration,
      ...additionalProps,
    });
  }

  /**
   * Track pattern export event
   */
  trackExport(format: string, additionalProps?: Record<string, any>): void {
    this.track('pattern_exported', {
      export_format: format,
      ...additionalProps,
    });
  }
}

// Export singleton instance
export const telemetryClient = new TelemetryClient();

// Export class for testing
export { TelemetryClient };
export type { TelemetryEvent };
