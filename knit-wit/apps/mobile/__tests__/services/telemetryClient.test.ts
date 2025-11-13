import AsyncStorage from '@react-native-async-storage/async-storage';
import axios, { AxiosError } from 'axios';
import { Platform } from 'react-native';
import { TelemetryClient } from '../../src/services/telemetryClient';

const TELEMETRY_CONSENT_KEY = '@knit-wit/telemetry_consent';
const TEST_API_URL = 'http://localhost:8000/api/v1';

// Mock dependencies
jest.mock('@react-native-async-storage/async-storage', () => ({
  getItem: jest.fn(),
  setItem: jest.fn(),
}));

jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

// Mock Platform
jest.mock('react-native/Libraries/Utilities/Platform', () => ({
  OS: 'ios',
  select: jest.fn((obj) => obj.ios),
}));

describe('TelemetryClient', () => {
  let client: TelemetryClient;

  beforeEach(() => {
    jest.clearAllMocks();
    (AsyncStorage.getItem as jest.Mock).mockResolvedValue(null);
    (AsyncStorage.setItem as jest.Mock).mockResolvedValue(undefined);
    mockedAxios.post.mockResolvedValue({ data: {}, status: 200 });

    // Create fresh client instance for each test
    client = new TelemetryClient(TEST_API_URL, '1.0.0');
  });

  describe('Consent Management', () => {
    it('defaults to disabled when no consent is stored', async () => {
      (AsyncStorage.getItem as jest.Mock).mockResolvedValue(null);

      const newClient = new TelemetryClient(TEST_API_URL);
      await newClient.loadConsent();

      expect(newClient.getConsent()).toBe(false);
    });

    it('loads consent from AsyncStorage on initialization', async () => {
      (AsyncStorage.getItem as jest.Mock).mockResolvedValue('true');

      const newClient = new TelemetryClient(TEST_API_URL);
      await newClient.loadConsent();

      expect(AsyncStorage.getItem).toHaveBeenCalledWith(TELEMETRY_CONSENT_KEY);
      expect(newClient.getConsent()).toBe(true);
    });

    it('handles AsyncStorage errors gracefully when loading consent', async () => {
      const consoleWarnSpy = jest.spyOn(console, 'warn').mockImplementation();
      (AsyncStorage.getItem as jest.Mock).mockRejectedValue(new Error('Storage error'));

      const newClient = new TelemetryClient(TEST_API_URL);
      await newClient.loadConsent();

      expect(newClient.getConsent()).toBe(false);
      expect(consoleWarnSpy).toHaveBeenCalledWith(
        'Failed to load telemetry consent:',
        expect.any(Error)
      );

      consoleWarnSpy.mockRestore();
    });

    it('saves consent to AsyncStorage', async () => {
      await client.setConsent(true);

      expect(AsyncStorage.setItem).toHaveBeenCalledWith(TELEMETRY_CONSENT_KEY, 'true');
      expect(client.getConsent()).toBe(true);
    });

    it('handles AsyncStorage errors gracefully when saving consent', async () => {
      const consoleWarnSpy = jest.spyOn(console, 'warn').mockImplementation();
      (AsyncStorage.setItem as jest.Mock).mockRejectedValue(new Error('Storage error'));

      await client.setConsent(true);

      expect(consoleWarnSpy).toHaveBeenCalledWith(
        'Failed to save telemetry consent:',
        expect.any(Error)
      );

      consoleWarnSpy.mockRestore();
    });
  });

  describe('Event Tracking', () => {
    beforeEach(async () => {
      await client.setConsent(true); // Enable tracking for these tests
    });

    it('does not send events when consent is false', async () => {
      await client.setConsent(false);

      client.track('test_event', { key: 'value' });

      // Wait a bit to ensure no async calls are made
      await new Promise((resolve) => setTimeout(resolve, 100));

      expect(mockedAxios.post).not.toHaveBeenCalled();
    });

    it('sends events when consent is true', async () => {
      client.track('test_event', { key: 'value' });

      // Wait for async operation
      await new Promise((resolve) => setTimeout(resolve, 100));

      expect(mockedAxios.post).toHaveBeenCalledWith(
        `${TEST_API_URL}/telemetry/events`,
        expect.objectContaining({
          event: 'test_event',
          properties: expect.objectContaining({
            key: 'value',
            platform: Platform.OS,
            version: '1.0.0',
          }),
          timestamp: expect.any(String),
        }),
        expect.objectContaining({
          timeout: 5000,
          headers: {
            'Content-Type': 'application/json',
          },
        })
      );
    });

    it('includes platform and version in event properties', async () => {
      client.track('test_event');

      await new Promise((resolve) => setTimeout(resolve, 100));

      const callArgs = mockedAxios.post.mock.calls[0];
      const eventPayload = callArgs[1];

      expect(eventPayload.properties.platform).toBe(Platform.OS);
      expect(eventPayload.properties.version).toBe('1.0.0');
    });

    it('includes ISO 8601 timestamp', async () => {
      const beforeTime = new Date().toISOString();

      client.track('test_event');

      await new Promise((resolve) => setTimeout(resolve, 100));

      const callArgs = mockedAxios.post.mock.calls[0];
      const eventPayload = callArgs[1];

      expect(eventPayload.timestamp).toBeTruthy();
      expect(new Date(eventPayload.timestamp).toISOString()).toBe(eventPayload.timestamp);

      const afterTime = new Date().toISOString();
      expect(eventPayload.timestamp >= beforeTime && eventPayload.timestamp <= afterTime).toBe(true);
    });

    it('merges custom properties with default properties', async () => {
      client.track('test_event', { custom_key: 'custom_value', another: 123 });

      await new Promise((resolve) => setTimeout(resolve, 100));

      const callArgs = mockedAxios.post.mock.calls[0];
      const eventPayload = callArgs[1];

      expect(eventPayload.properties).toEqual(
        expect.objectContaining({
          custom_key: 'custom_value',
          another: 123,
          platform: Platform.OS,
          version: '1.0.0',
        })
      );
    });
  });

  describe('Silent Failures', () => {
    beforeEach(async () => {
      await client.setConsent(true);
    });

    it('handles network errors silently', async () => {
      mockedAxios.post.mockRejectedValue(new Error('Network error'));

      // Should not throw
      expect(() => {
        client.track('test_event');
      }).not.toThrow();

      await new Promise((resolve) => setTimeout(resolve, 100));
    });

    it('handles axios errors silently in production', async () => {
      const originalDev = global.__DEV__;
      (global as any).__DEV__ = false;

      const consoleWarnSpy = jest.spyOn(console, 'warn').mockImplementation();
      mockedAxios.post.mockRejectedValue({
        isAxiosError: true,
        message: 'Request timeout',
        response: { status: 500, data: 'Server error' },
      });

      client.track('test_event');

      await new Promise((resolve) => setTimeout(resolve, 100));

      expect(consoleWarnSpy).not.toHaveBeenCalled();

      consoleWarnSpy.mockRestore();
      (global as any).__DEV__ = originalDev;
    });

    it('logs axios errors in development mode', async () => {
      const originalDev = global.__DEV__;
      (global as any).__DEV__ = true;

      const consoleWarnSpy = jest.spyOn(console, 'warn').mockImplementation();

      // Create a proper AxiosError-like object
      const mockError = Object.assign(new Error('Request timeout'), {
        isAxiosError: true,
        response: { status: 500, data: 'Server error' },
        config: {},
        toJSON: () => ({}),
      });

      // Make it pass instanceof AxiosError check
      Object.setPrototypeOf(mockError, AxiosError.prototype);

      mockedAxios.post.mockRejectedValue(mockError);

      client.track('test_event');

      await new Promise((resolve) => setTimeout(resolve, 100));

      expect(consoleWarnSpy).toHaveBeenCalledWith(
        'Telemetry error:',
        expect.objectContaining({
          message: 'Request timeout',
          status: 500,
          data: 'Server error',
        })
      );

      consoleWarnSpy.mockRestore();
      (global as any).__DEV__ = originalDev;
    });
  });

  describe('Convenience Methods', () => {
    beforeEach(async () => {
      await client.setConsent(true);
    });

    it('trackGeneration sends pattern_generated event', async () => {
      client.trackGeneration('sphere', 'sc');

      await new Promise((resolve) => setTimeout(resolve, 100));

      expect(mockedAxios.post).toHaveBeenCalledWith(
        `${TEST_API_URL}/telemetry/events`,
        expect.objectContaining({
          event: 'pattern_generated',
          properties: expect.objectContaining({
            shape_type: 'sphere',
            stitch_type: 'sc',
          }),
        }),
        expect.any(Object)
      );
    });

    it('trackGeneration accepts additional properties', async () => {
      client.trackGeneration('cylinder', 'hdc', { diameter: 10, height: 15 });

      await new Promise((resolve) => setTimeout(resolve, 100));

      const callArgs = mockedAxios.post.mock.calls[0];
      const eventPayload = callArgs[1];

      expect(eventPayload.properties).toEqual(
        expect.objectContaining({
          shape_type: 'cylinder',
          stitch_type: 'hdc',
          diameter: 10,
          height: 15,
        })
      );
    });

    it('trackVisualization sends pattern_visualized event', async () => {
      client.trackVisualization(15, 2500);

      await new Promise((resolve) => setTimeout(resolve, 100));

      expect(mockedAxios.post).toHaveBeenCalledWith(
        `${TEST_API_URL}/telemetry/events`,
        expect.objectContaining({
          event: 'pattern_visualized',
          properties: expect.objectContaining({
            round_count: 15,
            duration_ms: 2500,
          }),
        }),
        expect.any(Object)
      );
    });

    it('trackVisualization accepts additional properties', async () => {
      client.trackVisualization(10, 1200, { shape_type: 'sphere' });

      await new Promise((resolve) => setTimeout(resolve, 100));

      const callArgs = mockedAxios.post.mock.calls[0];
      const eventPayload = callArgs[1];

      expect(eventPayload.properties).toEqual(
        expect.objectContaining({
          round_count: 10,
          duration_ms: 1200,
          shape_type: 'sphere',
        })
      );
    });

    it('trackExport sends pattern_exported event', async () => {
      client.trackExport('pdf');

      await new Promise((resolve) => setTimeout(resolve, 100));

      expect(mockedAxios.post).toHaveBeenCalledWith(
        `${TEST_API_URL}/telemetry/events`,
        expect.objectContaining({
          event: 'pattern_exported',
          properties: expect.objectContaining({
            export_format: 'pdf',
          }),
        }),
        expect.any(Object)
      );
    });

    it('trackExport accepts additional properties', async () => {
      client.trackExport('svg', { paper_size: 'A4', include_diagram: true });

      await new Promise((resolve) => setTimeout(resolve, 100));

      const callArgs = mockedAxios.post.mock.calls[0];
      const eventPayload = callArgs[1];

      expect(eventPayload.properties).toEqual(
        expect.objectContaining({
          export_format: 'svg',
          paper_size: 'A4',
          include_diagram: true,
        })
      );
    });

    it('convenience methods respect opt-out', async () => {
      await client.setConsent(false);

      client.trackGeneration('sphere', 'sc');
      client.trackVisualization(10, 1000);
      client.trackExport('pdf');

      await new Promise((resolve) => setTimeout(resolve, 100));

      expect(mockedAxios.post).not.toHaveBeenCalled();
    });
  });

  describe('API Configuration', () => {
    it('uses custom API URL when provided', async () => {
      const customUrl = 'https://api.example.com/v2';
      const customClient = new TelemetryClient(customUrl);

      // Wait for initial loadConsent to complete
      await customClient.loadConsent();

      // Now set consent to true
      await customClient.setConsent(true);

      customClient.track('test_event');

      await new Promise((resolve) => setTimeout(resolve, 100));

      expect(mockedAxios.post).toHaveBeenCalledWith(
        `${customUrl}/telemetry/events`,
        expect.any(Object),
        expect.any(Object)
      );
    });

    it('uses custom app version when provided', async () => {
      const customClient = new TelemetryClient(TEST_API_URL, '2.3.4');

      // Wait for initial loadConsent to complete
      await customClient.loadConsent();

      // Now set consent to true
      await customClient.setConsent(true);

      customClient.track('test_event');

      await new Promise((resolve) => setTimeout(resolve, 100));

      const callArgs = mockedAxios.post.mock.calls[0];
      const eventPayload = callArgs[1];

      expect(eventPayload.properties.version).toBe('2.3.4');
    });
  });
});
