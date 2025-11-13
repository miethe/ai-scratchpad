import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { FormatSelector } from '../components/export/FormatSelector';
import { PaperSizeSelector } from '../components/export/PaperSizeSelector';
import { SimplifiedButton, SimplifiedCard } from '../components/kidmode';
import { useSettingsStore } from '../stores/useSettingsStore';
import { useFocusIndicator } from '../hooks/useFocusIndicator';
import { colors } from '../theme/colors';
import { typography } from '../theme/typography';
import { spacing } from '../theme/spacing';
import { borderRadius } from '../theme/spacing';
import { shadows } from '../theme';
import exportService, {
  type ExportFormat,
  type PaperSize,
} from '../services/exportService';
import { telemetryClient } from '../services/telemetryClient';
import type { RootStackScreenProps } from '../types/navigation';

type ExportScreenProps = RootStackScreenProps<'Export'>;

export const ExportScreen: React.FC<ExportScreenProps> = ({ route }) => {
  const { pattern } = route.params;
  const { kidMode } = useSettingsStore();

  const [selectedFormat, setSelectedFormat] = useState<ExportFormat | null>(null);
  const [paperSize, setPaperSize] = useState<PaperSize>('A4');
  const [isExporting, setIsExporting] = useState(false);
  const [exportStatus, setExportStatus] = useState<{
    type: 'success' | 'error' | null;
    message: string;
  }>({ type: null, message: '' });

  // Focus indicator for export button
  const exportButtonFocus = useFocusIndicator();

  const handleFormatSelect = (format: ExportFormat) => {
    setSelectedFormat(format);
    setExportStatus({ type: null, message: '' });
  };

  const handleExport = async () => {
    if (!selectedFormat) {
      Alert.alert(
        kidMode ? 'Pick a Type' : 'No Format Selected',
        kidMode ? 'Please pick how you want to save your pattern first.' : 'Please select an export format first.'
      );
      return;
    }

    setIsExporting(true);
    setExportStatus({ type: null, message: '' });

    const exportStartTime = Date.now();

    try {
      let result;

      switch (selectedFormat) {
        case 'pdf':
          result = await exportService.exportPdf(pattern, paperSize);
          break;
        case 'json':
          result = await exportService.exportJson(pattern);
          break;
        case 'svg':
          result = await exportService.exportSvg(pattern);
          break;
        case 'png':
          result = await exportService.exportPng(pattern);
          break;
        default:
          result = { success: false, error: 'Unknown format' };
      }

      if (result.success) {
        const exportDuration = Date.now() - exportStartTime;

        // Track successful export
        telemetryClient.trackExport(selectedFormat, {
          shape_type: pattern.object.type,
          stitch_type: pattern.meta.stitch,
          round_count: pattern.rounds.length,
          paper_size: selectedFormat === 'pdf' ? paperSize : undefined,
          duration_ms: exportDuration,
        });

        const formatLabel = selectedFormat.toUpperCase();
        setExportStatus({
          type: 'success',
          message: kidMode
            ? `Your pattern is saved!${result.fileName ? `\nFile: ${result.fileName}` : ''}`
            : `Pattern exported successfully as ${formatLabel}!${
                result.fileName ? `\nFile: ${result.fileName}` : ''
              }`,
        });
      } else {
        setExportStatus({
          type: 'error',
          message: kidMode
            ? result.error || 'Could not save. Please try again.'
            : result.error || 'Export failed. Please try again.',
        });
      }
    } catch (error) {
      const message =
        error instanceof Error ? error.message : 'An unexpected error occurred';
      setExportStatus({
        type: 'error',
        message: kidMode ? 'Something went wrong. Please try again.' : message,
      });
    } finally {
      setIsExporting(false);
    }
  };

  const estimatedSize = selectedFormat
    ? exportService.estimateFileSize(pattern, selectedFormat)
    : undefined;

  const canExport = selectedFormat && !isExporting;

  return (
    <View style={styles.container}>
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        <View style={styles.header}>
          <Text style={styles.title}>
            {kidMode ? 'Save Pattern' : 'Export Pattern'}
          </Text>
          <Text style={styles.subtitle}>
            {kidMode
              ? 'Pick how you want to save or share your pattern'
              : 'Choose your preferred format to save or share your pattern'}
          </Text>
        </View>

        <View style={styles.patternInfo}>
          <Text style={styles.patternInfoLabel}>
            {kidMode ? 'About Your Pattern' : 'Pattern Details'}
          </Text>
          <View style={styles.patternInfoRow}>
            <Text style={styles.patternInfoKey}>
              {kidMode ? 'Shape:' : 'Shape:'}
            </Text>
            <Text style={styles.patternInfoValue}>
              {kidMode && pattern.object.type === 'sphere'
                ? 'Ball'
                : kidMode && pattern.object.type === 'cylinder'
                ? 'Tube'
                : pattern.object.type.charAt(0).toUpperCase() +
                  pattern.object.type.slice(1)}
            </Text>
          </View>
          <View style={styles.patternInfoRow}>
            <Text style={styles.patternInfoKey}>
              {kidMode ? 'Steps:' : 'Rounds:'}
            </Text>
            <Text style={styles.patternInfoValue}>
              {pattern.rounds.length}
            </Text>
          </View>
          <View style={styles.patternInfoRow}>
            <Text style={styles.patternInfoKey}>
              {kidMode ? 'Stitch:' : 'Stitch:'}
            </Text>
            <Text style={styles.patternInfoValue}>
              {pattern.meta.stitch.toUpperCase()}
            </Text>
          </View>
        </View>

        <FormatSelector
          selectedFormat={selectedFormat}
          onSelectFormat={handleFormatSelect}
          estimatedSize={estimatedSize}
        />

        {selectedFormat === 'pdf' && (
          <PaperSizeSelector
            selectedSize={paperSize}
            onSelectSize={setPaperSize}
          />
        )}

        {exportStatus.type && (
          <View
            style={[
              styles.statusCard,
              exportStatus.type === 'success'
                ? styles.statusCardSuccess
                : styles.statusCardError,
            ]}
            accessible={true}
            accessibilityLiveRegion="polite"
            accessibilityRole="alert"
          >
            <Text
              style={[
                styles.statusIcon,
                exportStatus.type === 'success'
                  ? styles.statusIconSuccess
                  : styles.statusIconError,
              ]}
            >
              {exportStatus.type === 'success' ? '✓' : '⚠'}
            </Text>
            <Text
              style={[
                styles.statusMessage,
                exportStatus.type === 'success'
                  ? styles.statusMessageSuccess
                  : styles.statusMessageError,
              ]}
            >
              {exportStatus.message}
            </Text>
          </View>
        )}
      </ScrollView>

      <View style={styles.footer}>
        {kidMode ? (
          <SimplifiedButton
            label={
              isExporting
                ? 'Saving...'
                : selectedFormat
                ? `Save as ${selectedFormat.toUpperCase()}`
                : 'Pick Type to Save'
            }
            onPress={handleExport}
            disabled={!canExport || isExporting}
            variant="primary"
            size="large"
            accessibilityHint={
              !selectedFormat
                ? 'Please pick a type first'
                : 'Save your pattern'
            }
            style={styles.kidModeExportButton}
          />
        ) : (
          <TouchableOpacity
            style={[
              styles.exportButton,
              !canExport && styles.exportButtonDisabled,
              exportButtonFocus.focused && exportButtonFocus.focusStyle,
            ]}
            onPress={handleExport}
            onFocus={exportButtonFocus.onFocus}
            onBlur={exportButtonFocus.onBlur}
            disabled={!canExport}
            accessible={true}
            accessibilityRole="button"
            accessibilityLabel={`Export pattern as ${
              selectedFormat || 'selected format'
            }`}
            accessibilityHint={
              !selectedFormat
                ? 'Please select a format first'
                : 'Export and save your pattern'
            }
            accessibilityState={{ disabled: !canExport }}
          >
            {isExporting ? (
              <View style={styles.exportButtonContent}>
                <ActivityIndicator color={colors.white} size="small" />
                <Text style={styles.exportButtonText}>Exporting...</Text>
              </View>
            ) : (
              <Text style={styles.exportButtonText}>
                {selectedFormat
                  ? `Export as ${selectedFormat.toUpperCase()}`
                  : 'Select Format to Export'}
              </Text>
            )}
          </TouchableOpacity>
        )}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    padding: spacing.lg,
  },
  header: {
    marginBottom: spacing.lg,
  },
  title: {
    ...typography.headingLarge,
    color: colors.textPrimary,
    marginBottom: spacing.xs,
  },
  subtitle: {
    ...typography.bodyMedium,
    color: colors.textSecondary,
  },
  patternInfo: {
    backgroundColor: colors.surfaceSecondary,
    borderRadius: borderRadius.lg,
    padding: spacing.md,
    marginBottom: spacing.lg,
  },
  patternInfoLabel: {
    ...typography.bodyMedium,
    fontWeight: '600',
    color: colors.textPrimary,
    marginBottom: spacing.sm,
  },
  patternInfoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: spacing.xs,
  },
  patternInfoKey: {
    ...typography.bodyMedium,
    color: colors.textSecondary,
  },
  patternInfoValue: {
    ...typography.bodyMedium,
    fontWeight: '600',
    color: colors.textPrimary,
  },
  statusCard: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    padding: spacing.md,
    borderRadius: borderRadius.md,
    marginTop: spacing.md,
    ...shadows.sm,
  },
  statusCardSuccess: {
    backgroundColor: colors.success + '15',
    borderWidth: 1,
    borderColor: colors.success,
  },
  statusCardError: {
    backgroundColor: colors.error + '15',
    borderWidth: 1,
    borderColor: colors.error,
  },
  statusIcon: {
    fontSize: 20,
    marginRight: spacing.sm,
  },
  statusIconSuccess: {
    color: colors.success,
  },
  statusIconError: {
    color: colors.error,
  },
  statusMessage: {
    ...typography.bodyMedium,
    flex: 1,
  },
  statusMessageSuccess: {
    color: colors.success,
  },
  statusMessageError: {
    color: colors.error,
  },
  footer: {
    padding: spacing.lg,
    borderTopWidth: 1,
    borderTopColor: colors.border,
    backgroundColor: colors.background,
    ...shadows.md,
  },
  exportButton: {
    backgroundColor: colors.primary,
    borderRadius: borderRadius.md,
    paddingVertical: spacing.md,
    paddingHorizontal: spacing.lg,
    minHeight: 48, // Accessibility touch target
    justifyContent: 'center',
    alignItems: 'center',
    ...shadows.md,
  },
  exportButtonDisabled: {
    backgroundColor: colors.gray400,
    opacity: 0.6,
  },
  exportButtonContent: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
  },
  exportButtonText: {
    ...typography.bodyLarge,
    fontWeight: '600',
    color: colors.white,
  },
  // Kid Mode specific styles
  kidModeExportButton: {
    width: '100%',
  },
});
