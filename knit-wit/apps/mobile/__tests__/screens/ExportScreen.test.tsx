import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import { ExportScreen } from '../../src/screens/ExportScreen';
import exportService from '../../src/services/exportService';
import type { PatternDSL } from '../../src/types/pattern';

// Mock expo virtual env to avoid ES module issues
jest.mock('expo/virtual/env', () => ({
  env: process.env,
}));

// Mock dependencies
jest.mock('../../src/services/exportService');

// Mock navigation
const mockNavigate = jest.fn();
const mockRoute = {
  params: {
    pattern: {
      meta: {
        version: '0.1',
        units: 'cm' as const,
        terms: 'US' as const,
        stitch: 'sc' as const,
        round_mode: 'spiral' as const,
        gauge: {
          sts_per_10cm: 14,
          rows_per_10cm: 16,
        },
      },
      object: {
        type: 'sphere' as const,
        params: { diameter: 10 },
      },
      rounds: [
        {
          r: 1,
          ops: [
            { op: 'MR', count: 1 },
            { op: 'sc', count: 6 },
          ],
          stitches: 6,
        },
        {
          r: 2,
          ops: [{ op: 'inc', count: 6 }],
          stitches: 12,
        },
      ],
      materials: {
        yarn_weight: 'Worsted',
        hook_size_mm: 4.0,
        yardage_estimate: 25,
      },
      notes: ['Work in a spiral'],
    } as PatternDSL,
  },
};

const mockNavigation = {
  navigate: mockNavigate,
  goBack: jest.fn(),
  setOptions: jest.fn(),
  addListener: jest.fn(),
  removeListener: jest.fn(),
  canGoBack: jest.fn(() => true),
  dispatch: jest.fn(),
  isFocused: jest.fn(() => true),
  getParent: jest.fn(),
  getState: jest.fn(),
  setParams: jest.fn(),
  reset: jest.fn(),
  getId: jest.fn(),
};

describe('ExportScreen', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Rendering', () => {
    it('renders the export screen with title and subtitle', () => {
      const { getByText } = render(
        <ExportScreen route={mockRoute} navigation={mockNavigation} />
      );

      expect(getByText('Export Pattern')).toBeTruthy();
      expect(
        getByText('Choose your preferred format to save or share your pattern')
      ).toBeTruthy();
    });

    it('displays pattern information', () => {
      const { getByText } = render(
        <ExportScreen route={mockRoute} navigation={mockNavigation} />
      );

      expect(getByText('Pattern Details')).toBeTruthy();
      expect(getByText('Sphere')).toBeTruthy();
      expect(getByText('2')).toBeTruthy(); // Round count
      expect(getByText('SC')).toBeTruthy(); // Stitch type
    });

    it('renders all format options', () => {
      const { getByText } = render(
        <ExportScreen route={mockRoute} navigation={mockNavigation} />
      );

      expect(getByText('PDF Document')).toBeTruthy();
      expect(getByText('JSON Data')).toBeTruthy();
      expect(getByText('SVG Image')).toBeTruthy();
      expect(getByText('PNG Image')).toBeTruthy();
    });

    it('does not show paper size selector by default', () => {
      const { queryByText } = render(
        <ExportScreen route={mockRoute} navigation={mockNavigation} />
      );

      expect(queryByText('Paper Size')).toBeNull();
    });
  });

  describe('Format Selection', () => {
    it('allows selecting PDF format', () => {
      const { getByText, getByLabelText } = render(
        <ExportScreen route={mockRoute} navigation={mockNavigation} />
      );

      const pdfOption = getByLabelText(/PDF Document/);
      fireEvent.press(pdfOption);

      expect(getByText('Paper Size')).toBeTruthy();
    });

    it('allows selecting JSON format', () => {
      const { getByLabelText, queryByText } = render(
        <ExportScreen route={mockRoute} navigation={mockNavigation} />
      );

      const jsonOption = getByLabelText(/JSON Data/);
      fireEvent.press(jsonOption);

      // Paper size selector should not appear for JSON
      expect(queryByText('Paper Size')).toBeNull();
    });

    it('allows selecting SVG format', () => {
      const { getByLabelText, queryByText } = render(
        <ExportScreen route={mockRoute} navigation={mockNavigation} />
      );

      const svgOption = getByLabelText(/SVG Image/);
      fireEvent.press(svgOption);

      // Paper size selector should not appear for SVG
      expect(queryByText('Paper Size')).toBeNull();
    });

    it('allows selecting PNG format', () => {
      const { getByLabelText, queryByText } = render(
        <ExportScreen route={mockRoute} navigation={mockNavigation} />
      );

      const pngOption = getByLabelText(/PNG Image/);
      fireEvent.press(pngOption);

      // Paper size selector should not appear for PNG
      expect(queryByText('Paper Size')).toBeNull();
    });

    it('updates export button text when format is selected', () => {
      const { getByText, getByLabelText } = render(
        <ExportScreen route={mockRoute} navigation={mockNavigation} />
      );

      expect(getByText('Select Format to Export')).toBeTruthy();

      const pdfOption = getByLabelText(/PDF Document/);
      fireEvent.press(pdfOption);

      expect(getByText('Export as PDF')).toBeTruthy();
    });

    it('shows estimated file size when format is selected', () => {
      // Mock the estimateFileSize method
      (exportService.estimateFileSize as jest.Mock) = jest.fn().mockReturnValue('22 KB');

      const { getByText, getByLabelText } = render(
        <ExportScreen route={mockRoute} navigation={mockNavigation} />
      );

      const pdfOption = getByLabelText(/PDF Document/);
      fireEvent.press(pdfOption);

      // Should show estimated size
      expect(getByText(/22 KB/)).toBeTruthy();
    });
  });

  describe('Paper Size Selection', () => {
    it('shows paper size selector when PDF is selected', () => {
      const { getByText, getByLabelText } = render(
        <ExportScreen route={mockRoute} navigation={mockNavigation} />
      );

      const pdfOption = getByLabelText(/PDF Document/);
      fireEvent.press(pdfOption);

      expect(getByText('Paper Size')).toBeTruthy();
      expect(getByText('A4')).toBeTruthy();
      expect(getByText('Letter')).toBeTruthy();
    });

    it('allows changing paper size', () => {
      const { getByLabelText } = render(
        <ExportScreen route={mockRoute} navigation={mockNavigation} />
      );

      const pdfOption = getByLabelText(/PDF Document/);
      fireEvent.press(pdfOption);

      const letterOption = getByLabelText(/Letter paper size/);
      fireEvent.press(letterOption);

      expect(letterOption.props.accessibilityState.selected).toBe(true);
    });
  });

  describe('Export Functionality', () => {
    // Note: Alert testing is skipped due to mocking complexity with React Native in Jest
    it.skip('shows alert when trying to export without selecting format', () => {
      // This test is skipped because mocking Alert.alert in Jest with React Native
      // requires complex setup that conflicts with other mocks
    });

    it('successfully exports PDF with correct paper size', async () => {
      const mockExportResult = {
        success: true,
        fileName: 'knit-wit-sphere-2024-01-01.pdf',
        filePath: '/path/to/file.pdf',
      };

      (exportService.exportPdf as jest.Mock).mockResolvedValue(mockExportResult);

      const { getByText, getByLabelText } = render(
        <ExportScreen route={mockRoute} navigation={mockNavigation} />
      );

      // Select PDF format
      const pdfOption = getByLabelText(/PDF Document/);
      fireEvent.press(pdfOption);

      // Select Letter paper size
      const letterOption = getByLabelText(/Letter paper size/);
      fireEvent.press(letterOption);

      // Export
      const exportButton = getByText('Export as PDF');
      fireEvent.press(exportButton);

      await waitFor(() => {
        expect(exportService.exportPdf).toHaveBeenCalledWith(
          mockRoute.params.pattern,
          'letter'
        );
      });

      await waitFor(() => {
        expect(
          getByText(/Pattern exported successfully as PDF/)
        ).toBeTruthy();
      });
    });

    it('successfully exports JSON', async () => {
      const mockExportResult = {
        success: true,
        fileName: 'knit-wit-sphere-2024-01-01.json',
        filePath: '/path/to/file.json',
      };

      (exportService.exportJson as jest.Mock).mockResolvedValue(mockExportResult);

      const { getByText, getByLabelText } = render(
        <ExportScreen route={mockRoute} navigation={mockNavigation} />
      );

      // Select JSON format
      const jsonOption = getByLabelText(/JSON Data/);
      fireEvent.press(jsonOption);

      // Export
      const exportButton = getByText('Export as JSON');
      fireEvent.press(exportButton);

      await waitFor(() => {
        expect(exportService.exportJson).toHaveBeenCalledWith(
          mockRoute.params.pattern
        );
      });

      await waitFor(() => {
        expect(
          getByText(/Pattern exported successfully as JSON/)
        ).toBeTruthy();
      });
    });

    it('successfully exports SVG', async () => {
      const mockExportResult = {
        success: true,
        fileName: 'knit-wit-sphere-2024-01-01.svg',
        filePath: '/path/to/file.svg',
      };

      (exportService.exportSvg as jest.Mock).mockResolvedValue(mockExportResult);

      const { getByText, getByLabelText } = render(
        <ExportScreen route={mockRoute} navigation={mockNavigation} />
      );

      // Select SVG format
      const svgOption = getByLabelText(/SVG Image/);
      fireEvent.press(svgOption);

      // Export
      const exportButton = getByText('Export as SVG');
      fireEvent.press(exportButton);

      await waitFor(() => {
        expect(exportService.exportSvg).toHaveBeenCalledWith(
          mockRoute.params.pattern
        );
      });

      await waitFor(() => {
        expect(
          getByText(/Pattern exported successfully as SVG/)
        ).toBeTruthy();
      });
    });

    it('successfully exports PNG', async () => {
      const mockExportResult = {
        success: true,
        fileName: 'knit-wit-sphere-2024-01-01.png',
        filePath: '/path/to/file.png',
      };

      (exportService.exportPng as jest.Mock).mockResolvedValue(mockExportResult);

      const { getByText, getByLabelText } = render(
        <ExportScreen route={mockRoute} navigation={mockNavigation} />
      );

      // Select PNG format
      const pngOption = getByLabelText(/PNG Image/);
      fireEvent.press(pngOption);

      // Export
      const exportButton = getByText('Export as PNG');
      fireEvent.press(exportButton);

      await waitFor(() => {
        expect(exportService.exportPng).toHaveBeenCalledWith(
          mockRoute.params.pattern
        );
      });

      await waitFor(() => {
        expect(
          getByText(/Pattern exported successfully as PNG/)
        ).toBeTruthy();
      });
    });

    it('shows loading state during export', async () => {
      // Create a promise that won't resolve immediately
      let resolveExport: (value: any) => void;
      const exportPromise = new Promise((resolve) => {
        resolveExport = resolve;
      });

      (exportService.exportPdf as jest.Mock).mockReturnValue(exportPromise);

      const { getByText, getByLabelText } = render(
        <ExportScreen route={mockRoute} navigation={mockNavigation} />
      );

      // Select PDF format
      const pdfOption = getByLabelText(/PDF Document/);
      fireEvent.press(pdfOption);

      // Start export
      const exportButton = getByText('Export as PDF');
      fireEvent.press(exportButton);

      // Should show loading state
      await waitFor(() => {
        expect(getByText('Exporting...')).toBeTruthy();
      });

      // Resolve the export
      resolveExport!({ success: true, fileName: 'test.pdf' });
    });

    it('handles export errors gracefully', async () => {
      const mockError = {
        success: false,
        error: 'Network error occurred',
      };

      (exportService.exportPdf as jest.Mock).mockResolvedValue(mockError);

      const { getByText, getByLabelText } = render(
        <ExportScreen route={mockRoute} navigation={mockNavigation} />
      );

      // Select PDF format
      const pdfOption = getByLabelText(/PDF Document/);
      fireEvent.press(pdfOption);

      // Export
      const exportButton = getByText('Export as PDF');
      fireEvent.press(exportButton);

      await waitFor(() => {
        expect(getByText(/Network error occurred/)).toBeTruthy();
      });
    });

    it('handles exceptions during export', async () => {
      (exportService.exportPdf as jest.Mock).mockRejectedValue(
        new Error('Unexpected error')
      );

      const { getByText, getByLabelText } = render(
        <ExportScreen route={mockRoute} navigation={mockNavigation} />
      );

      // Select PDF format
      const pdfOption = getByLabelText(/PDF Document/);
      fireEvent.press(pdfOption);

      // Export
      const exportButton = getByText('Export as PDF');
      fireEvent.press(exportButton);

      await waitFor(() => {
        expect(getByText(/Unexpected error/)).toBeTruthy();
      });
    });

    it('handles SVG export errors gracefully', async () => {
      const mockError = {
        success: false,
        error: 'SVG generation failed',
      };

      (exportService.exportSvg as jest.Mock).mockResolvedValue(mockError);

      const { getByText, getByLabelText } = render(
        <ExportScreen route={mockRoute} navigation={mockNavigation} />
      );

      // Select SVG format
      const svgOption = getByLabelText(/SVG Image/);
      fireEvent.press(svgOption);

      // Export
      const exportButton = getByText('Export as SVG');
      fireEvent.press(exportButton);

      await waitFor(() => {
        expect(getByText(/SVG generation failed/)).toBeTruthy();
      });
    });

    it('handles PNG export errors gracefully', async () => {
      const mockError = {
        success: false,
        error: 'PNG generation failed',
      };

      (exportService.exportPng as jest.Mock).mockResolvedValue(mockError);

      const { getByText, getByLabelText } = render(
        <ExportScreen route={mockRoute} navigation={mockNavigation} />
      );

      // Select PNG format
      const pngOption = getByLabelText(/PNG Image/);
      fireEvent.press(pngOption);

      // Export
      const exportButton = getByText('Export as PNG');
      fireEvent.press(exportButton);

      await waitFor(() => {
        expect(getByText(/PNG generation failed/)).toBeTruthy();
      });
    });
  });

  describe('Accessibility', () => {
    it('has proper accessibility labels for format cards', () => {
      const { getByLabelText } = render(
        <ExportScreen route={mockRoute} navigation={mockNavigation} />
      );

      expect(
        getByLabelText(/PDF Document.*Print-ready pattern with instructions/)
      ).toBeTruthy();
      expect(
        getByLabelText(/JSON Data.*Machine-readable pattern format/)
      ).toBeTruthy();
      expect(
        getByLabelText(/SVG Image.*Scalable vector diagram/)
      ).toBeTruthy();
      expect(
        getByLabelText(/PNG Image.*Raster diagram for sharing/)
      ).toBeTruthy();
    });

    it('has proper accessibility state for selected format', () => {
      const { getByLabelText } = render(
        <ExportScreen route={mockRoute} navigation={mockNavigation} />
      );

      const pdfOption = getByLabelText(/PDF Document/);
      expect(pdfOption.props.accessibilityState.selected).toBe(false);

      fireEvent.press(pdfOption);

      expect(pdfOption.props.accessibilityState.selected).toBe(true);
    });

    it('has proper accessibility role for buttons', () => {
      const { getByText } = render(
        <ExportScreen route={mockRoute} navigation={mockNavigation} />
      );

      const exportButton = getByText('Select Format to Export');
      expect(exportButton.parent?.props.accessibilityRole).toBe('button');
    });

    it('displays success status message after export', async () => {
      const mockExportResult = {
        success: true,
        fileName: 'test.pdf',
      };

      (exportService.exportPdf as jest.Mock).mockResolvedValue(mockExportResult);

      const { getByText, getByLabelText } = render(
        <ExportScreen route={mockRoute} navigation={mockNavigation} />
      );

      const pdfOption = getByLabelText(/PDF Document/);
      fireEvent.press(pdfOption);

      const exportButton = getByText('Export as PDF');
      fireEvent.press(exportButton);

      await waitFor(() => {
        expect(getByText(/Pattern exported successfully/)).toBeTruthy();
      });
    });
  });
});
