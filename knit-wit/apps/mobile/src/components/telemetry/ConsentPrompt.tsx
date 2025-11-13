import React, { useState, useEffect } from 'react';
import { View, Text, Modal, TouchableOpacity, StyleSheet } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { telemetryClient } from '../../services/telemetryClient';
import { useTheme } from '../../theme';

const TELEMETRY_CONSENT_KEY = '@knit-wit/telemetry_consent';

export const ConsentPrompt: React.FC = () => {
  const [visible, setVisible] = useState(false);
  const theme = useTheme();

  useEffect(() => {
    checkConsent();
  }, []);

  const checkConsent = async () => {
    try {
      const consent = await AsyncStorage.getItem(TELEMETRY_CONSENT_KEY);
      if (consent === null) {
        // First run - show prompt
        setVisible(true);
      }
    } catch (error) {
      // Silent fail - don't show prompt if we can't read storage
      console.warn('Failed to check telemetry consent:', error);
    }
  };

  const handleAccept = async () => {
    await telemetryClient.setConsent(true);
    setVisible(false);
  };

  const handleDecline = async () => {
    await telemetryClient.setConsent(false);
    setVisible(false);
  };

  const styles = StyleSheet.create({
    overlay: {
      flex: 1,
      backgroundColor: 'rgba(0, 0, 0, 0.5)',
      justifyContent: 'center',
      alignItems: 'center',
      padding: theme.spacing.lg,
    },
    modal: {
      backgroundColor: theme.colors.surface,
      borderRadius: theme.borderRadius.lg,
      padding: theme.spacing.lg,
      width: '100%',
      maxWidth: 400,
      ...theme.shadows.lg,
    },
    title: {
      ...theme.typography.titleLarge,
      color: theme.colors.textPrimary,
      marginBottom: theme.spacing.md,
    },
    body: {
      ...theme.typography.bodyLarge,
      color: theme.colors.textSecondary,
      marginBottom: theme.spacing.md,
      lineHeight: 24,
    },
    buttons: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      marginTop: theme.spacing.md,
      gap: theme.spacing.md,
    },
    button: {
      flex: 1,
      minHeight: theme.touchTargets.comfortable,
      minWidth: theme.touchTargets.comfortable,
      borderRadius: theme.borderRadius.md,
      justifyContent: 'center',
      alignItems: 'center',
      paddingHorizontal: theme.spacing.md,
      paddingVertical: theme.spacing.sm,
    },
    declineButton: {
      backgroundColor: theme.colors.gray200,
    },
    acceptButton: {
      backgroundColor: theme.colors.primary,
    },
    declineText: {
      ...theme.typography.labelLarge,
      color: theme.colors.textPrimary,
    },
    acceptText: {
      ...theme.typography.labelLarge,
      color: theme.colors.textInverse,
    },
  });

  return (
    <Modal
      visible={visible}
      transparent
      animationType="fade"
      onRequestClose={handleDecline}
      testID="consent-modal"
    >
      <View style={styles.overlay}>
        <View style={styles.modal}>
          <Text style={styles.title}>Help Us Improve Knit-Wit</Text>
          <Text style={styles.body}>
            We'd like to collect anonymous usage data to improve the app.
            This includes which features you use and how patterns are generated.
          </Text>
          <Text style={styles.body}>
            No personal information is collected. You can change this in Settings.
          </Text>

          <View style={styles.buttons}>
            <TouchableOpacity
              onPress={handleDecline}
              style={[styles.button, styles.declineButton]}
              accessibilityLabel="Decline telemetry"
              accessibilityRole="button"
              accessibilityHint="Opt out of anonymous usage tracking"
              testID="decline-button"
            >
              <Text style={styles.declineText}>No Thanks</Text>
            </TouchableOpacity>

            <TouchableOpacity
              onPress={handleAccept}
              style={[styles.button, styles.acceptButton]}
              accessibilityLabel="Accept telemetry"
              accessibilityRole="button"
              accessibilityHint="Allow anonymous usage tracking to help improve the app"
              testID="accept-button"
            >
              <Text style={styles.acceptText}>Accept</Text>
            </TouchableOpacity>
          </View>
        </View>
      </View>
    </Modal>
  );
};
