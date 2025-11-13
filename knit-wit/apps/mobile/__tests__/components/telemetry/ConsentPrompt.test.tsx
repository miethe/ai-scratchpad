import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { ConsentPrompt } from '../../../src/components/telemetry/ConsentPrompt';
import { telemetryClient } from '../../../src/services/telemetryClient';

const TELEMETRY_CONSENT_KEY = '@knit-wit/telemetry_consent';

// Mock dependencies
jest.mock('@react-native-async-storage/async-storage', () => ({
  getItem: jest.fn(),
  setItem: jest.fn(),
}));

jest.mock('../../../src/services/telemetryClient', () => ({
  telemetryClient: {
    setConsent: jest.fn(),
  },
}));

// Mock theme
jest.mock('../../../src/theme', () => ({
  useTheme: () => ({
    colors: {
      surface: '#FFFFFF',
      textPrimary: '#111827',
      textSecondary: '#6B7280',
      textInverse: '#FFFFFF',
      primary: '#6B4EFF',
      gray200: '#E5E7EB',
    },
    typography: {
      titleLarge: {
        fontFamily: 'System',
        fontSize: 22,
        lineHeight: 28,
        fontWeight: '600',
      },
      bodyLarge: {
        fontFamily: 'System',
        fontSize: 16,
        lineHeight: 24,
        fontWeight: '400',
      },
      labelLarge: {
        fontFamily: 'System',
        fontSize: 14,
        lineHeight: 20,
        fontWeight: '500',
      },
    },
    spacing: {
      sm: 8,
      md: 16,
      lg: 24,
    },
    borderRadius: {
      md: 8,
      lg: 12,
    },
    touchTargets: {
      comfortable: 48,
    },
    shadows: {
      lg: {
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.15,
        shadowRadius: 8,
        elevation: 5,
      },
    },
  }),
}));

describe('ConsentPrompt', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    (AsyncStorage.getItem as jest.Mock).mockResolvedValue(null);
    (AsyncStorage.setItem as jest.Mock).mockResolvedValue(undefined);
    (telemetryClient.setConsent as jest.Mock).mockResolvedValue(undefined);
  });

  describe('First Run Behavior', () => {
    it('shows modal when consent is null (first run)', async () => {
      (AsyncStorage.getItem as jest.Mock).mockResolvedValue(null);

      const { getByTestId, getByText } = render(<ConsentPrompt />);

      await waitFor(() => {
        expect(getByTestId('consent-modal')).toBeTruthy();
        expect(getByText('Help Us Improve Knit-Wit')).toBeTruthy();
      });

      expect(AsyncStorage.getItem).toHaveBeenCalledWith(TELEMETRY_CONSENT_KEY);
    });

    it('does not show modal when consent is already set to true', async () => {
      (AsyncStorage.getItem as jest.Mock).mockResolvedValue('true');

      const { queryByTestId } = render(<ConsentPrompt />);

      await waitFor(() => {
        expect(AsyncStorage.getItem).toHaveBeenCalledWith(TELEMETRY_CONSENT_KEY);
      });

      // Modal should not be visible
      const modal = queryByTestId('consent-modal');
      expect(modal?.props.visible).toBeFalsy();
    });

    it('does not show modal when consent is already set to false', async () => {
      (AsyncStorage.getItem as jest.Mock).mockResolvedValue('false');

      const { queryByTestId } = render(<ConsentPrompt />);

      await waitFor(() => {
        expect(AsyncStorage.getItem).toHaveBeenCalledWith(TELEMETRY_CONSENT_KEY);
      });

      // Modal should not be visible
      const modal = queryByTestId('consent-modal');
      expect(modal?.props.visible).toBeFalsy();
    });

    it('handles AsyncStorage errors gracefully', async () => {
      const consoleWarnSpy = jest.spyOn(console, 'warn').mockImplementation();
      (AsyncStorage.getItem as jest.Mock).mockRejectedValue(new Error('Storage error'));

      const { queryByTestId } = render(<ConsentPrompt />);

      await waitFor(() => {
        expect(consoleWarnSpy).toHaveBeenCalledWith(
          'Failed to check telemetry consent:',
          expect.any(Error)
        );
      });

      // Modal should not be shown on error
      const modal = queryByTestId('consent-modal');
      expect(modal?.props.visible).toBeFalsy();

      consoleWarnSpy.mockRestore();
    });
  });

  describe('Modal Content', () => {
    beforeEach(async () => {
      (AsyncStorage.getItem as jest.Mock).mockResolvedValue(null);
    });

    it('displays title text', async () => {
      const { getByText } = render(<ConsentPrompt />);

      await waitFor(() => {
        expect(getByText('Help Us Improve Knit-Wit')).toBeTruthy();
      });
    });

    it('displays explanation of data collection', async () => {
      const { getByText } = render(<ConsentPrompt />);

      await waitFor(() => {
        expect(
          getByText(/collect anonymous usage data to improve the app/i)
        ).toBeTruthy();
        expect(
          getByText(/which features you use and how patterns are generated/i)
        ).toBeTruthy();
      });
    });

    it('displays privacy assurance', async () => {
      const { getByText } = render(<ConsentPrompt />);

      await waitFor(() => {
        expect(getByText(/No personal information is collected/i)).toBeTruthy();
        expect(getByText(/You can change this in Settings/i)).toBeTruthy();
      });
    });

    it('displays both action buttons', async () => {
      const { getByTestId } = render(<ConsentPrompt />);

      await waitFor(() => {
        expect(getByTestId('decline-button')).toBeTruthy();
        expect(getByTestId('accept-button')).toBeTruthy();
      });
    });
  });

  describe('Accept Button', () => {
    beforeEach(async () => {
      (AsyncStorage.getItem as jest.Mock).mockResolvedValue(null);
    });

    it('calls telemetryClient.setConsent(true) when pressed', async () => {
      const { getByTestId } = render(<ConsentPrompt />);

      await waitFor(() => {
        expect(getByTestId('accept-button')).toBeTruthy();
      });

      fireEvent.press(getByTestId('accept-button'));

      await waitFor(() => {
        expect(telemetryClient.setConsent).toHaveBeenCalledWith(true);
      });
    });

    it('hides modal after accepting', async () => {
      const { getByTestId, queryByTestId } = render(<ConsentPrompt />);

      await waitFor(() => {
        expect(getByTestId('accept-button')).toBeTruthy();
      });

      fireEvent.press(getByTestId('accept-button'));

      await waitFor(() => {
        const modal = queryByTestId('consent-modal');
        expect(modal?.props.visible).toBeFalsy();
      });
    });

    it('has proper accessibility attributes', async () => {
      const { getByTestId } = render(<ConsentPrompt />);

      await waitFor(() => {
        const button = getByTestId('accept-button');
        expect(button.props.accessibilityRole).toBe('button');
        expect(button.props.accessibilityLabel).toBe('Accept telemetry');
        expect(button.props.accessibilityHint).toBeTruthy();
      });
    });

    it('has minimum touch target size', async () => {
      const { getByTestId } = render(<ConsentPrompt />);

      await waitFor(() => {
        const button = getByTestId('accept-button');
        const styles = button.props.style;

        // Flatten styles array if needed
        const flatStyles = Array.isArray(styles)
          ? Object.assign({}, ...styles)
          : styles;

        expect(flatStyles.minHeight).toBeGreaterThanOrEqual(48);
        expect(flatStyles.minWidth).toBeGreaterThanOrEqual(48);
      });
    });
  });

  describe('Decline Button', () => {
    beforeEach(async () => {
      (AsyncStorage.getItem as jest.Mock).mockResolvedValue(null);
    });

    it('calls telemetryClient.setConsent(false) when pressed', async () => {
      const { getByTestId } = render(<ConsentPrompt />);

      await waitFor(() => {
        expect(getByTestId('decline-button')).toBeTruthy();
      });

      fireEvent.press(getByTestId('decline-button'));

      await waitFor(() => {
        expect(telemetryClient.setConsent).toHaveBeenCalledWith(false);
      });
    });

    it('hides modal after declining', async () => {
      const { getByTestId, queryByTestId } = render(<ConsentPrompt />);

      await waitFor(() => {
        expect(getByTestId('decline-button')).toBeTruthy();
      });

      fireEvent.press(getByTestId('decline-button'));

      await waitFor(() => {
        const modal = queryByTestId('consent-modal');
        expect(modal?.props.visible).toBeFalsy();
      });
    });

    it('has proper accessibility attributes', async () => {
      const { getByTestId } = render(<ConsentPrompt />);

      await waitFor(() => {
        const button = getByTestId('decline-button');
        expect(button.props.accessibilityRole).toBe('button');
        expect(button.props.accessibilityLabel).toBe('Decline telemetry');
        expect(button.props.accessibilityHint).toBeTruthy();
      });
    });

    it('has minimum touch target size', async () => {
      const { getByTestId } = render(<ConsentPrompt />);

      await waitFor(() => {
        const button = getByTestId('decline-button');
        const styles = button.props.style;

        // Flatten styles array if needed
        const flatStyles = Array.isArray(styles)
          ? Object.assign({}, ...styles)
          : styles;

        expect(flatStyles.minHeight).toBeGreaterThanOrEqual(48);
        expect(flatStyles.minWidth).toBeGreaterThanOrEqual(48);
      });
    });
  });

  describe('Modal Behavior', () => {
    beforeEach(async () => {
      (AsyncStorage.getItem as jest.Mock).mockResolvedValue(null);
    });

    it('is transparent', async () => {
      const { getByTestId } = render(<ConsentPrompt />);

      await waitFor(() => {
        const modal = getByTestId('consent-modal');
        expect(modal.props.transparent).toBe(true);
      });
    });

    it('uses fade animation', async () => {
      const { getByTestId } = render(<ConsentPrompt />);

      await waitFor(() => {
        const modal = getByTestId('consent-modal');
        expect(modal.props.animationType).toBe('fade');
      });
    });

    it('calls handleDecline on onRequestClose', async () => {
      const { getByTestId } = render(<ConsentPrompt />);

      await waitFor(() => {
        const modal = getByTestId('consent-modal');
        expect(modal.props.onRequestClose).toBeTruthy();
      });

      // Simulate back button press (onRequestClose)
      const modal = getByTestId('consent-modal');
      modal.props.onRequestClose();

      await waitFor(() => {
        expect(telemetryClient.setConsent).toHaveBeenCalledWith(false);
      });
    });
  });

  describe('Copy Quality', () => {
    beforeEach(async () => {
      (AsyncStorage.getItem as jest.Mock).mockResolvedValue(null);
    });

    it('uses friendly, clear language', async () => {
      const { getByText } = render(<ConsentPrompt />);

      await waitFor(() => {
        // Title is inviting, not demanding
        expect(getByText('Help Us Improve Knit-Wit')).toBeTruthy();

        // Decline button is respectful
        expect(getByText('No Thanks')).toBeTruthy();

        // Accept button is positive
        expect(getByText('Accept')).toBeTruthy();
      });
    });

    it('is not a dark pattern (decline button is not hidden or de-emphasized)', async () => {
      const { getByTestId } = render(<ConsentPrompt />);

      await waitFor(() => {
        const declineButton = getByTestId('decline-button');
        const acceptButton = getByTestId('accept-button');

        // Both buttons should exist and be interactable
        expect(declineButton).toBeTruthy();
        expect(acceptButton).toBeTruthy();

        // Decline button should have same touch target size
        const declineStyles = Array.isArray(declineButton.props.style)
          ? Object.assign({}, ...declineButton.props.style)
          : declineButton.props.style;
        const acceptStyles = Array.isArray(acceptButton.props.style)
          ? Object.assign({}, ...acceptButton.props.style)
          : acceptButton.props.style;

        expect(declineStyles.minHeight).toBe(acceptStyles.minHeight);
        expect(declineStyles.minWidth).toBe(acceptStyles.minWidth);
      });
    });
  });
});
