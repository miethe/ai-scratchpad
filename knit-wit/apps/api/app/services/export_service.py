"""
Export Service for Knit-Wit

Generates professional exports in PDF and JSON formats from PatternDSL.
Implements C3 (PDF Export) and C5 (JSON DSL Export) from Phase 3.
"""

import io
import logging
import math
from typing import Literal, List, Dict
from xml.etree import ElementTree as ET

# Import from knit_wit_engine package
import sys
from pathlib import Path

# Import Sentry for error tracking
from app.core import capture_exception, add_breadcrumb

# Add pattern-engine to Python path for imports
pattern_engine_path = (
    Path(__file__).parent.parent.parent.parent.parent / "packages" / "pattern-engine"
)
if str(pattern_engine_path) not in sys.path:
    sys.path.insert(0, str(pattern_engine_path))

from knit_wit_engine.models.dsl import PatternDSL, RoundInstruction, StitchInstruction

# ReportLab imports for PDF generation
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# SVG/PNG generation imports
import cairosvg
from PIL import Image

# Logger
logger = logging.getLogger("knit_wit.service.export")


class ExportService:
    """
    Service for exporting PatternDSL to various formats.

    Provides professional-quality exports for:
    - PDF: Full pattern documentation with cover, materials, and instructions
    - JSON: Round-trip compatible JSON representation

    Architecture:
    - generate_pdf(): Creates PDF from PatternDSL
    - generate_json(): Exports PatternDSL as formatted JSON
    - _format_round(): Helper for round instruction formatting
    - _create_cover_section(): PDF cover page generation
    - _create_materials_section(): PDF materials list
    - _create_pattern_section(): PDF round-by-round instructions

    Performance Requirements:
    - PDF generation: < 5 seconds
    - PDF file size: < 5 MB
    - JSON round-trip compatible with PatternDSL
    """

    # PDF styling constants
    TITLE_FONT_SIZE = 24
    HEADING_FONT_SIZE = 16
    BODY_FONT_SIZE = 11
    SMALL_FONT_SIZE = 9

    def generate_pdf(
        self, dsl: PatternDSL, paper_size: Literal["A4", "letter"] = "A4"
    ) -> bytes:
        """
        Generate professional PDF from PatternDSL.

        Creates a multi-section PDF document with:
        1. Cover page: Pattern title, shape type, dimensions
        2. Materials section: Yarn, hook, yardage, gauge
        3. Pattern instructions: Round-by-round with stitch counts
        4. Professional formatting using ReportLab

        Args:
            dsl: PatternDSL instance to export
            paper_size: Paper format ("A4" or "letter")

        Returns:
            bytes: PDF document as bytes

        Raises:
            ValueError: If paper_size is invalid

        Example:
            >>> service = ExportService()
            >>> pattern = PatternDSL(...)
            >>> pdf_bytes = service.generate_pdf(pattern, paper_size="A4")
            >>> len(pdf_bytes) < 5 * 1024 * 1024  # Under 5 MB
            True
        """
        # Add breadcrumb for tracing
        add_breadcrumb(
            message="Starting PDF generation",
            category="export",
            data={
                "shape_type": dsl.shape.shape_type,
                "paper_size": paper_size,
                "total_rounds": dsl.metadata.total_rounds,
            },
        )

        # Validate paper size
        if paper_size not in ["A4", "letter"]:
            error = ValueError(f"Invalid paper size: {paper_size}. Must be 'A4' or 'letter'")
            # Capture validation errors to Sentry
            capture_exception(
                error,
                context={"paper_size": paper_size, "valid_sizes": ["A4", "letter"]},
                tags={"component": "export_service", "error_type": "validation"},
            )
            raise error

        # Select paper dimensions
        page_size = A4 if paper_size == "A4" else LETTER

        try:
            # Create PDF buffer
            buffer = io.BytesIO()

            # Initialize PDF document
            doc = SimpleDocTemplate(
                buffer,
                pagesize=page_size,
                rightMargin=0.75 * inch,
                leftMargin=0.75 * inch,
                topMargin=0.75 * inch,
                bottomMargin=0.75 * inch,
            )

            # Build document sections
            story = []
            styles = getSampleStyleSheet()
        except Exception as e:
            # Capture PDF initialization errors
            logger.error(f"Failed to initialize PDF document: {e}")
            capture_exception(
                e,
                context={
                    "paper_size": paper_size,
                    "shape_type": dsl.shape.shape_type,
                },
                tags={"component": "export_service", "operation": "pdf_init"},
            )
            raise

        # Custom styles
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Title"],
            fontSize=self.TITLE_FONT_SIZE,
            textColor=colors.HexColor("#2C3E50"),
            spaceAfter=30,
            alignment=TA_CENTER,
        )

        heading_style = ParagraphStyle(
            "CustomHeading",
            parent=styles["Heading1"],
            fontSize=self.HEADING_FONT_SIZE,
            textColor=colors.HexColor("#34495E"),
            spaceAfter=12,
            spaceBefore=12,
        )

        body_style = ParagraphStyle(
            "CustomBody",
            parent=styles["BodyText"],
            fontSize=self.BODY_FONT_SIZE,
            spaceAfter=6,
            alignment=TA_LEFT,
        )

        # 1. Cover Section
        story.extend(self._create_cover_section(dsl, title_style, body_style))
        story.append(PageBreak())

        # 2. Materials Section
        story.append(Paragraph("Materials", heading_style))
        story.append(Spacer(1, 0.2 * inch))
        story.extend(self._create_materials_section(dsl, body_style))
        story.append(Spacer(1, 0.3 * inch))

        # 3. Pattern Instructions Section
        story.append(Paragraph("Pattern Instructions", heading_style))
        story.append(Spacer(1, 0.2 * inch))
        story.extend(self._create_pattern_section(dsl, body_style))

        try:
            # Build PDF
            doc.build(story)

            # Return PDF bytes
            pdf_bytes = buffer.getvalue()
            buffer.close()

            # Add success breadcrumb
            add_breadcrumb(
                message="PDF generation completed",
                category="export",
                data={"pdf_size_bytes": len(pdf_bytes), "paper_size": paper_size},
            )

            logger.info(f"Generated PDF: size={len(pdf_bytes)} bytes, paper={paper_size}")

            return pdf_bytes

        except Exception as e:
            # Capture PDF generation errors
            logger.error(f"PDF generation failed: {e}")
            capture_exception(
                e,
                context={
                    "paper_size": paper_size,
                    "shape_type": dsl.shape.shape_type,
                    "total_rounds": dsl.metadata.total_rounds,
                },
                tags={"component": "export_service", "operation": "pdf_generation"},
            )
            raise

    def generate_json(self, dsl: PatternDSL) -> str:
        """
        Export PatternDSL as formatted JSON string.

        Creates a round-trip compatible JSON representation that can be
        re-parsed into PatternDSL using PatternDSL.from_json().

        Args:
            dsl: PatternDSL instance to export

        Returns:
            str: Formatted JSON string (2-space indent)

        Example:
            >>> service = ExportService()
            >>> pattern = PatternDSL(...)
            >>> json_str = service.generate_json(pattern)
            >>> restored = PatternDSL.from_json(json_str)
            >>> restored.shape.shape_type == pattern.shape.shape_type
            True
        """
        return dsl.to_json()

    def _create_cover_section(
        self, dsl: PatternDSL, title_style: ParagraphStyle, body_style: ParagraphStyle
    ) -> list:
        """
        Create cover page section for PDF.

        Args:
            dsl: PatternDSL instance
            title_style: Title paragraph style
            body_style: Body paragraph style

        Returns:
            list: ReportLab Flowable elements for cover
        """
        elements = []

        # Pattern title
        shape_name = dsl.shape.shape_type.capitalize()
        title = f"Crochet Pattern: {shape_name}"
        elements.append(Paragraph(title, title_style))
        elements.append(Spacer(1, 0.5 * inch))

        # Pattern metadata
        metadata_text = f"""
        <b>Shape:</b> {shape_name}<br/>
        <b>Generated:</b> {dsl.metadata.generated_at.strftime('%Y-%m-%d %H:%M')}<br/>
        <b>Engine Version:</b> {dsl.metadata.engine_version}<br/>
        <b>Total Rounds:</b> {dsl.metadata.total_rounds}<br/>
        """

        if dsl.metadata.difficulty:
            metadata_text += f"<b>Difficulty:</b> {dsl.metadata.difficulty.capitalize()}<br/>"

        elements.append(Paragraph(metadata_text, body_style))
        elements.append(Spacer(1, 0.3 * inch))

        # Shape dimensions
        dimensions_text = "<b>Dimensions:</b><br/>"
        if dsl.shape.diameter_cm:
            dimensions_text += f"Diameter: {dsl.shape.diameter_cm} cm<br/>"
        if dsl.shape.height_cm:
            dimensions_text += f"Height: {dsl.shape.height_cm} cm<br/>"
        if dsl.shape.base_diameter_cm:
            dimensions_text += f"Base Diameter: {dsl.shape.base_diameter_cm} cm<br/>"
        if dsl.shape.top_diameter_cm:
            dimensions_text += f"Top Diameter: {dsl.shape.top_diameter_cm} cm<br/>"

        elements.append(Paragraph(dimensions_text, body_style))

        # Notes if present
        if dsl.notes:
            elements.append(Spacer(1, 0.3 * inch))
            elements.append(Paragraph("<b>Notes:</b>", body_style))
            elements.append(Paragraph(dsl.notes, body_style))

        return elements

    def _create_materials_section(
        self, dsl: PatternDSL, body_style: ParagraphStyle
    ) -> list:
        """
        Create materials list section for PDF.

        Args:
            dsl: PatternDSL instance
            body_style: Body paragraph style

        Returns:
            list: ReportLab Flowable elements for materials
        """
        elements = []

        # Build materials data
        materials_data = [
            ["Item", "Details"],
        ]

        # Yarn weight
        if dsl.gauge.yarn_weight:
            materials_data.append(["Yarn Weight", dsl.gauge.yarn_weight.replace("_", " ").title()])

        # Hook size
        if dsl.gauge.hook_size_mm:
            materials_data.append(["Hook Size", f"{dsl.gauge.hook_size_mm} mm"])

        # Gauge information
        gauge_text = (
            f"{dsl.gauge.stitches_per_cm:.1f} sts/cm × "
            f"{dsl.gauge.rows_per_cm:.1f} rows/cm"
        )
        materials_data.append(["Gauge", gauge_text])

        # Yardage estimate (if available in metadata)
        if dsl.metadata.estimated_time_minutes:
            materials_data.append(
                ["Estimated Time", f"{dsl.metadata.estimated_time_minutes} minutes"]
            )

        # Gauge swatch notes
        if dsl.gauge.swatch_notes:
            materials_data.append(["Gauge Notes", dsl.gauge.swatch_notes])

        # Create table
        table = Table(materials_data, colWidths=[2 * inch, 4 * inch])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#34495E")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), self.BODY_FONT_SIZE),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 1), (-1, -1), self.SMALL_FONT_SIZE),
                    ("TOPPADDING", (0, 1), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
                ]
            )
        )

        elements.append(table)

        return elements

    def _create_pattern_section(
        self, dsl: PatternDSL, body_style: ParagraphStyle
    ) -> list:
        """
        Create pattern instructions section for PDF.

        Args:
            dsl: PatternDSL instance
            body_style: Body paragraph style

        Returns:
            list: ReportLab Flowable elements for pattern instructions
        """
        elements = []

        # Round-by-round instructions
        for round_inst in dsl.rounds:
            round_text = self._format_round(round_inst)
            elements.append(Paragraph(round_text, body_style))
            elements.append(Spacer(1, 0.1 * inch))

        return elements

    def _format_round(self, round_inst: RoundInstruction) -> str:
        """
        Format a single round instruction as human-readable text.

        Args:
            round_inst: RoundInstruction to format

        Returns:
            str: Formatted round text with HTML markup

        Example:
            Round 1: 6 sc (6 sts)
            Round 2: [inc] x6 (12 sts)
            Round 3: [sc, inc] x6 (18 sts)
        """
        # Round header (1-indexed for display)
        round_num = round_inst.round_number + 1
        parts = [f"<b>Round {round_num}:</b> "]

        # Format stitch instructions
        stitch_parts = []
        for stitch in round_inst.stitches:
            stitch_type = stitch.stitch_type
            count = stitch.count

            if count == 1:
                stitch_parts.append(stitch_type)
            else:
                stitch_parts.append(f"{count} {stitch_type}")

        # Join with commas
        parts.append(", ".join(stitch_parts))

        # Add total stitch count
        parts.append(f" <b>({round_inst.total_stitches} sts)</b>")

        # Add description if present
        if round_inst.description:
            parts.append(f" <i>— {round_inst.description}</i>")

        return "".join(parts)

    def generate_svg(
        self, dsl: PatternDSL, mode: Literal["per-round", "composite"] = "composite"
    ) -> List[str] | str:
        """
        Generate SVG diagrams from PatternDSL.

        Creates vector graphics showing circular stitch layout using visualization
        frames from Phase 2. Supports two modes:
        - per-round: Returns list of SVG strings (one per round)
        - composite: Returns single SVG with all rounds stacked vertically

        Args:
            dsl: PatternDSL instance to visualize
            mode: Export mode ("per-round" or "composite")

        Returns:
            List[str] if mode="per-round", str if mode="composite"
            Each SVG is a valid XML string

        Raises:
            ValueError: If mode is invalid

        Example:
            >>> service = ExportService()
            >>> pattern = PatternDSL(...)
            >>> svg = service.generate_svg(pattern, mode="composite")
            >>> len(svg) < 1024 * 1024  # Under 1 MB
            True
        """
        # Validate mode
        if mode not in ["per-round", "composite"]:
            raise ValueError(f"Invalid mode: {mode}. Must be 'per-round' or 'composite'")

        # Import visualization service to generate frames
        from app.services.visualization_service import VisualizationService

        viz_service = VisualizationService()
        frames = viz_service.dsl_to_frames(dsl)

        if mode == "per-round":
            # Generate individual SVG for each round
            svgs: List[str] = []
            for frame in frames:
                svg_str = self._frame_to_svg(frame, dsl.shape.shape_type)
                svgs.append(svg_str)
            return svgs
        else:
            # Generate composite SVG with all rounds
            return self._frames_to_composite_svg(frames, dsl.shape.shape_type)

    def generate_png(
        self, svg_content: str, dpi: Literal[72, 300] = 72
    ) -> bytes:
        """
        Convert SVG to PNG rasterized image.

        Uses cairosvg to rasterize SVG content at specified DPI:
        - 72 DPI: Screen display (smaller file size)
        - 300 DPI: Print quality (larger file size)

        Args:
            svg_content: Valid SVG XML string
            dpi: Dots per inch (72 for screen, 300 for print)

        Returns:
            bytes: PNG image data

        Raises:
            ValueError: If DPI is invalid or SVG is malformed

        Example:
            >>> service = ExportService()
            >>> svg = service.generate_svg(pattern, mode="composite")
            >>> png_bytes = service.generate_png(svg, dpi=300)
            >>> len(png_bytes) < 5 * 1024 * 1024  # Under 5 MB
            True
        """
        # Validate DPI
        if dpi not in [72, 300]:
            raise ValueError(f"Invalid DPI: {dpi}. Must be 72 or 300")

        try:
            # Convert SVG to PNG using cairosvg
            # Scale factor: cairosvg uses 96 DPI as default, so we scale accordingly
            scale = dpi / 96.0

            png_bytes = cairosvg.svg2png(
                bytestring=svg_content.encode("utf-8"),
                scale=scale,
            )

            logger.info(f"Generated PNG: size={len(png_bytes)} bytes, dpi={dpi}")

            return png_bytes

        except Exception as e:
            # Capture PNG conversion errors
            logger.error(f"PNG conversion failed: {e}")
            capture_exception(
                e,
                context={
                    "dpi": dpi,
                    "svg_length": len(svg_content),
                },
                tags={"component": "export_service", "operation": "png_conversion"},
            )
            raise ValueError(f"Failed to convert SVG to PNG: {str(e)}")

    def _frame_to_svg(self, frame, shape_type: str) -> str:
        """
        Convert single visualization frame to SVG.

        Creates SVG with:
        - Circular node layout (positioned stitches)
        - Connecting edges forming closed loop
        - Color-coded highlights for increases/decreases
        - Centered viewBox for responsive scaling

        Args:
            frame: VisualizationFrame with nodes and edges
            shape_type: Shape type for title

        Returns:
            str: Valid SVG XML string
        """
        # SVG dimensions and viewBox
        # Nodes are positioned around BASE_RADIUS (100 units)
        # Add padding for visual clarity
        padding = 50
        base_radius = 100
        canvas_size = (base_radius * 2) + (padding * 2)
        view_box = f"-{base_radius + padding} -{base_radius + padding} {canvas_size} {canvas_size}"

        # Create SVG root
        svg = ET.Element(
            "svg",
            xmlns="http://www.w3.org/2000/svg",
            viewBox=view_box,
            width="400",
            height="400",
        )

        # Add title
        title = ET.SubElement(svg, "title")
        title.text = f"{shape_type.capitalize()} - Round {frame.round_number}"

        # Add background
        bg = ET.SubElement(
            svg,
            "rect",
            x=str(-base_radius - padding),
            y=str(-base_radius - padding),
            width=str(canvas_size),
            height=str(canvas_size),
            fill="#f8f9fa",
        )

        # Draw edges first (so they appear behind nodes)
        edges_group = ET.SubElement(svg, "g", id="edges")
        for edge in frame.edges:
            # Find source and target nodes
            source_node = next(n for n in frame.nodes if n.id == edge.source)
            target_node = next(n for n in frame.nodes if n.id == edge.target)

            # Draw line between nodes
            line = ET.SubElement(
                edges_group,
                "line",
                x1=str(source_node.position[0]),
                y1=str(source_node.position[1]),
                x2=str(target_node.position[0]),
                y2=str(target_node.position[1]),
                stroke="#6c757d",
                **{"stroke-width": "1.5"},
            )

        # Draw nodes
        nodes_group = ET.SubElement(svg, "g", id="nodes")
        for node in frame.nodes:
            # Determine node color based on highlight
            if node.highlight == "increase":
                fill_color = "#28a745"  # Green for increases
            elif node.highlight == "decrease":
                fill_color = "#dc3545"  # Red for decreases
            else:
                fill_color = "#007bff"  # Blue for normal stitches

            # Draw circle for stitch
            circle = ET.SubElement(
                nodes_group,
                "circle",
                cx=str(node.position[0]),
                cy=str(node.position[1]),
                r="5",
                fill=fill_color,
                stroke="#ffffff",
                **{"stroke-width": "1.5"},
            )

            # Add title for hover tooltip
            node_title = ET.SubElement(circle, "title")
            node_title.text = f"{node.stitch_type} ({node.id})"

        # Add round label
        label = ET.SubElement(
            svg,
            "text",
            x="0",
            y=str(base_radius + padding - 10),
            **{
                "text-anchor": "middle",
                "font-family": "Arial, sans-serif",
                "font-size": "16",
                "fill": "#212529",
            },
        )
        label.text = f"Round {frame.round_number}: {frame.stitch_count} sts"

        # Convert to string
        return ET.tostring(svg, encoding="unicode")

    def _frames_to_composite_svg(self, frames: List, shape_type: str) -> str:
        """
        Combine multiple frames into single composite SVG.

        Stacks rounds vertically with spacing, showing pattern progression.

        Args:
            frames: List of VisualizationFrame objects
            shape_type: Shape type for title

        Returns:
            str: Valid SVG XML string with all rounds
        """
        # Calculate layout
        round_height = 300  # Height allocated per round
        round_width = 300  # Width per round
        padding = 20

        total_height = (round_height * len(frames)) + (padding * 2)
        total_width = round_width + (padding * 2)

        # Create SVG root
        svg = ET.Element(
            "svg",
            xmlns="http://www.w3.org/2000/svg",
            width=str(total_width),
            height=str(total_height),
        )

        # Add title
        title = ET.SubElement(svg, "title")
        title.text = f"{shape_type.capitalize()} Pattern - All Rounds"

        # Add background
        bg = ET.SubElement(
            svg, "rect", x="0", y="0", width=str(total_width), height=str(total_height), fill="#ffffff"
        )

        # Add each frame
        for idx, frame in enumerate(frames):
            y_offset = (idx * round_height) + padding + (round_height / 2)

            # Create group for this round
            group = ET.SubElement(
                svg,
                "g",
                id=f"round-{frame.round_number}",
                transform=f"translate({padding + round_width / 2}, {y_offset})",
            )

            # Draw edges
            for edge in frame.edges:
                source_node = next(n for n in frame.nodes if n.id == edge.source)
                target_node = next(n for n in frame.nodes if n.id == edge.target)

                line = ET.SubElement(
                    group,
                    "line",
                    x1=str(source_node.position[0]),
                    y1=str(source_node.position[1]),
                    x2=str(target_node.position[0]),
                    y2=str(target_node.position[1]),
                    stroke="#dee2e6",
                    **{"stroke-width": "1"},
                )

            # Draw nodes
            for node in frame.nodes:
                # Determine color
                if node.highlight == "increase":
                    fill_color = "#28a745"
                elif node.highlight == "decrease":
                    fill_color = "#dc3545"
                else:
                    fill_color = "#007bff"

                circle = ET.SubElement(
                    group,
                    "circle",
                    cx=str(node.position[0]),
                    cy=str(node.position[1]),
                    r="4",
                    fill=fill_color,
                    stroke="#ffffff",
                    **{"stroke-width": "1"},
                )

            # Add round label
            label = ET.SubElement(
                group,
                "text",
                x=str(-round_width / 2 + 10),
                y="-110",
                **{"font-family": "Arial, sans-serif", "font-size": "14", "fill": "#495057"},
            )
            label.text = f"R{frame.round_number}: {frame.stitch_count} sts"

        # Convert to string
        return ET.tostring(svg, encoding="unicode")
