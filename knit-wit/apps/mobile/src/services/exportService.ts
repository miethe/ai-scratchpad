import * as FileSystem from 'expo-file-system';
import * as Sharing from 'expo-sharing';
import apiClient from './api';
import type { PatternDSL } from '../types/pattern';

export type ExportFormat = 'pdf' | 'json' | 'svg' | 'png';
export type PaperSize = 'A4' | 'letter';

export interface ExportOptions {
  format: ExportFormat;
  paperSize?: PaperSize;
}

export interface ExportResult {
  success: boolean;
  filePath?: string;
  fileName?: string;
  error?: string;
  sizeBytes?: number;
}

/**
 * Export service
 * Handles pattern export to various formats with file system operations
 */
export const exportService = {
  /**
   * Export pattern to PDF format
   */
  async exportPdf(
    pattern: PatternDSL,
    paperSize: PaperSize = 'A4'
  ): Promise<ExportResult> {
    try {
      const response = await apiClient.post(
        `/export/pdf`,
        pattern,
        {
          params: { paper_size: paperSize },
          responseType: 'blob',
          timeout: 30000, // 30 second timeout for PDF generation
        }
      );

      // Generate filename
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      const shapeName = pattern.object.type;
      const fileName = `knit-wit-${shapeName}-${timestamp}.pdf`;

      // Save to device
      const fileUri = `${FileSystem.documentDirectory}${fileName}`;

      // Convert blob to base64 and save
      const base64 = await this.blobToBase64(response.data);
      await FileSystem.writeAsStringAsync(fileUri, base64, {
        encoding: FileSystem.EncodingType.Base64,
      });

      // Share the file
      if (await Sharing.isAvailableAsync()) {
        await Sharing.shareAsync(fileUri, {
          mimeType: 'application/pdf',
          dialogTitle: 'Save or Share Pattern PDF',
          UTI: 'com.adobe.pdf',
        });
      }

      return {
        success: true,
        filePath: fileUri,
        fileName,
        sizeBytes: response.data.size,
      };
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to export PDF';
      return {
        success: false,
        error: message,
      };
    }
  },

  /**
   * Export pattern to JSON format
   */
  async exportJson(pattern: PatternDSL): Promise<ExportResult> {
    try {
      const response = await apiClient.post<{
        json: string;
        size_bytes: number;
      }>('/export/json', pattern);

      // Generate filename
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      const shapeName = pattern.object.type;
      const fileName = `knit-wit-${shapeName}-${timestamp}.json`;

      // Save to device
      const fileUri = `${FileSystem.documentDirectory}${fileName}`;
      await FileSystem.writeAsStringAsync(fileUri, response.data.json);

      // Share the file
      if (await Sharing.isAvailableAsync()) {
        await Sharing.shareAsync(fileUri, {
          mimeType: 'application/json',
          dialogTitle: 'Save or Share Pattern JSON',
        });
      }

      return {
        success: true,
        filePath: fileUri,
        fileName,
        sizeBytes: response.data.size_bytes,
      };
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to export JSON';
      return {
        success: false,
        error: message,
      };
    }
  },

  /**
   * Export pattern to SVG format (placeholder for future implementation)
   */
  async exportSvg(pattern: PatternDSL): Promise<ExportResult> {
    // TODO: Implement SVG export once backend endpoint is available
    return {
      success: false,
      error: 'SVG export not yet implemented',
    };
  },

  /**
   * Export pattern to PNG format (placeholder for future implementation)
   */
  async exportPng(pattern: PatternDSL): Promise<ExportResult> {
    // TODO: Implement PNG export once backend endpoint is available
    return {
      success: false,
      error: 'PNG export not yet implemented',
    };
  },

  /**
   * Helper to convert blob to base64
   */
  async blobToBase64(blob: Blob): Promise<string> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onerror = reject;
      reader.onload = () => {
        if (typeof reader.result === 'string') {
          // Remove data URL prefix if present
          const base64 = reader.result.replace(/^data:.*?;base64,/, '');
          resolve(base64);
        } else {
          reject(new Error('Failed to convert blob to base64'));
        }
      };
      reader.readAsDataURL(blob);
    });
  },

  /**
   * Estimate file size for a format (rough estimates)
   */
  estimateFileSize(pattern: PatternDSL, format: ExportFormat): string {
    const roundCount = pattern.rounds.length;

    switch (format) {
      case 'pdf':
        // Rough estimate: 10-50KB base + 1KB per round
        const pdfKb = 20 + roundCount * 1;
        return pdfKb > 1024 ? `${(pdfKb / 1024).toFixed(1)} MB` : `${pdfKb} KB`;

      case 'json':
        // Rough estimate: 1-2KB base + 0.5KB per round
        const jsonKb = 2 + roundCount * 0.5;
        return `${jsonKb.toFixed(0)} KB`;

      case 'svg':
        // Rough estimate: 5KB base + 2KB per round
        const svgKb = 5 + roundCount * 2;
        return `${svgKb.toFixed(0)} KB`;

      case 'png':
        // Rough estimate: 50-200KB depending on rounds
        const pngKb = 100 + roundCount * 3;
        return `${pngKb.toFixed(0)} KB`;

      default:
        return 'Unknown';
    }
  },
};

export default exportService;
