"""
Export Service for Knit-Wit

Generates professional exports in PDF and JSON formats from PatternDSL.
Implements C3 (PDF Export) and C5 (JSON DSL Export) from Phase 3.
"""

import io
from typing import Literal

# Import from knit_wit_engine package
import sys
from pathlib import Path

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
        # Validate paper size
        if paper_size not in ["A4", "letter"]:
            raise ValueError(f"Invalid paper size: {paper_size}. Must be 'A4' or 'letter'")

        # Select paper dimensions
        page_size = A4 if paper_size == "A4" else LETTER

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

        # Build PDF
        doc.build(story)

        # Return PDF bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()

        return pdf_bytes

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
