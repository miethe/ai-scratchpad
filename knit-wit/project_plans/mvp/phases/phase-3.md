# Phase 3: Full Feature Implementation

**Knit-Wit MVP Implementation Plan**

---

## Phase Overview

**Phase Number:** 3
**Phase Name:** Full Feature Implementation
**Duration:** 4 weeks (Weeks 8-11 of project timeline)
**Sprints:** Sprint 5, Sprint 6, Sprint 7
**Target Dates:** Week 8 (Start) → End of Week 11
**Capacity:** ~180-200 story points
**Team:** Full team (2 backend engineers, 2 frontend engineers, 1 QA engineer)

### Phase Purpose

Phase 3 represents the feature completion milestone for the Knit-Wit MVP. This phase brings together all core functionality into a cohesive, end-to-end user experience. Users will be able to generate patterns via a form interface, parse external pattern text (limited grammar), visualize patterns interactively, and export results in multiple formats (PDF, SVG, JSON).

This phase also introduces critical usability enhancements: Kid Mode for beginner-friendly UI, comprehensive accessibility features (WCAG AA compliance), and telemetry for data-driven improvements. By the end of Phase 3, the application will have all MVP features implemented and ready for QA polish in Phase 4.

### Phase Context

- **Previous Phase:** Phase 2 (Visualization Foundation, Weeks 5-7) established the React Native app shell, navigation, and interactive pattern visualization with SVG rendering. The `Visualizer` class converts DSL to render primitives, and the scrubber/step controls allow round-by-round navigation.
- **Next Phase:** Phase 4 (QA & Polish, Weeks 12-15) will focus on cross-device testing, accessibility audits, performance optimization, bug fixes, and documentation to prepare for launch.

---

## Goals & Deliverables

### Primary Goals

1. **Pattern Generation UI:** Complete generation form with shape selection, parameter inputs, gauge entry, and API integration
2. **Pattern Parsing:** Text parser supporting limited crochet pattern syntax (brackets, repeats, common abbreviations)
3. **Multi-Format Export:** PDF, SVG, and JSON export fully functional with professional formatting
4. **Kid Mode:** Beginner-friendly UI variant with simplified terminology and larger tap targets
5. **Accessibility Compliance:** WCAG AA compliance with screen reader support, keyboard navigation, and high-contrast options
6. **Telemetry Infrastructure:** Opt-in usage tracking for key events (generation, visualization, export)

### Key Deliverables

| Deliverable | Description | Success Metric |
|------------|-------------|----------------|
| **Generation Screen** | Form-based UI for pattern generation with shape/params/gauge inputs | End-to-end generate → visualize works |
| **Text Parser** | Backend parser supporting limited crochet pattern grammar | Parses canonical patterns with 90%+ accuracy |
| **PDF Export** | Professional PDF with cover, materials, pattern text, and diagrams | PDFs print correctly on A4/Letter paper |
| **SVG/PNG Export** | Vector and raster diagram exports | SVGs editable in Illustrator/Inkscape |
| **JSON DSL Export** | Machine-readable pattern DSL for integration | Round-trip export/import works identically |
| **Kid Mode UI** | Simplified UI with beginner-friendly terminology and animations | Toggle activates; UI is noticeably simplified |
| **Accessibility Features** | Screen reader labels, keyboard navigation, high-contrast mode | WCAG AA audit shows 0 critical issues |
| **Telemetry Pipeline** | Event tracking for generation, visualization, export | Opt-in toggle works; events logged correctly |

### Non-Goals (Deferred to Later Phases or v1.1)

- Advanced pattern parsing (complex abbreviations, colorwork, tapestry)
- User authentication and saved patterns (v1.1)
- Advanced export templates or custom branding (v1.1)
- Offline mode and local storage (v1.1)
- Community pattern library (v2.0)

---

## Epic Breakdown

### EPIC C: Parsing & I/O

**Epic Owner:** Backend Engineer + Frontend Engineer
**Epic Duration:** Weeks 8-10 (Sprints 5-6)
**Total Effort:** ~60 story points
**Priority:** P0 (Critical Path)

#### Epic Overview

Enable users to paste their own crochet patterns (limited syntax support) and export generated results in multiple professional formats. The text parser converts common pattern syntax to Pattern DSL, allowing users to import external patterns. Export functionality produces printable PDFs, editable SVGs, and machine-readable JSON for integration and sharing.

#### Epic Goals

- Parse common bracket/repeat pattern syntax with clear error messages
- Export patterns to PDF (printable, professional quality)
- Export diagrams to SVG and PNG (editable, shareable)
- Export DSL to JSON (round-trip compatible)
- User-friendly error handling for parsing failures

#### Epic Stories Summary

| Story ID | Title | Effort | Priority | Dependencies |
|----------|-------|--------|----------|--------------|
| C1 | Text parser (backend) | 13 pt | P0 | A6 (US/UK translator) |
| C2 | Parser test suite | 8 pt | P0 | C1 |
| C3 | PDF export endpoint (backend) | 13 pt | P0 | B1 (render primitives) |
| C4 | SVG/PNG export endpoint (backend) | 8 pt | P1 | B1 (render primitives) |
| C5 | Export screen UI (frontend) | 8 pt | P0 | C3, C4 |
| C6 | Parse input screen UI (frontend) | 8 pt | P1 | C1 |

**Total:** 58 story points

#### Epic Acceptance Criteria

- **AC-C-1:** Parser successfully parses canonical patterns: `R4: [2 sc, inc] x6 (24)`
- **AC-C-2:** PDF exports are printable on A4 and Letter paper without text overflow
- **AC-C-3:** SVG exports are valid and editable in standard design tools (Illustrator, Inkscape)
- **AC-C-4:** JSON export round-trips correctly (export → re-import produces identical pattern)
- **AC-C-5:** Parse errors show user-friendly messages indicating which line/token failed
- **AC-C-6:** All export formats respect US/UK terminology toggle

#### Technical Implementation

**Text Parser Architecture:**

The text parser uses a simple lexer + parser approach for the limited MVP grammar. Implementation in `knit_wit_engine/parsing/text_parser.py`.

**Supported Grammar (MVP Scope):**

```
<pattern>     ::= <round>+
<round>       ::= "R" <number> ":" <operations> "(" <stitch_count> ")"
<operations>  ::= <operation> ( "," <operation> )*
<operation>   ::= <stitch> | <repeat_group>
<stitch>      ::= [ <count> ] <stitch_type>
<stitch_type> ::= "sc" | "hdc" | "dc" | "slst" | "ch" | "inc" | "dec" | "MR"
<repeat_group>::= "[" <operations> "]" "x" <number>
<count>       ::= <number>
```

**Example Patterns:**

```
R1: MR 6 sc (6)
R2: inc x6 (12)
R3: [sc, inc] x6 (18)
R4: [2 sc, inc] x6 (24)
R5: [sc, inc] x2 [hdc, inc] x2 [dc, inc] x2 (30)
```

**Lexer Tokens:**

- `ROUND_LABEL`: `R<N>:`
- `MAGIC_RING`: `MR`
- `STITCH`: `sc`, `hdc`, `dc`, `slst`, `ch`
- `OPERATION`: `inc`, `dec`
- `LBRACKET`: `[`
- `RBRACKET`: `]`
- `REPEAT`: `x<N>`
- `STITCH_COUNT`: `(<N>)`
- `NUMBER`: `\d+`
- `COMMA`: `,`

**Parser Implementation Approach:**

```python
# knit_wit_engine/parsing/text_parser.py

from typing import List, Optional
from dataclasses import dataclass
from knit_wit_engine.models.dsl import PatternDSL, Round, Operation

@dataclass
class Token:
    type: str
    value: str
    line: int
    column: int

class Lexer:
    """Tokenize pattern text into a stream of tokens."""

    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1

    def tokenize(self) -> List[Token]:
        """Return list of tokens."""
        tokens = []
        while self.pos < len(self.text):
            # Skip whitespace
            if self.text[self.pos].isspace():
                if self.text[self.pos] == '\n':
                    self.line += 1
                    self.column = 1
                else:
                    self.column += 1
                self.pos += 1
                continue

            # Match round label: R1:
            if self.text[self.pos] == 'R' and self.peek_ahead().isdigit():
                tokens.append(self.read_round_label())
                continue

            # Match magic ring: MR
            if self.text[self.pos:self.pos+2] == 'MR':
                tokens.append(Token('MAGIC_RING', 'MR', self.line, self.column))
                self.pos += 2
                self.column += 2
                continue

            # Match stitches: sc, hdc, dc, etc.
            if self.match_stitch():
                tokens.append(self.read_stitch())
                continue

            # Match operations: inc, dec
            if self.match_operation():
                tokens.append(self.read_operation())
                continue

            # Match brackets
            if self.text[self.pos] == '[':
                tokens.append(Token('LBRACKET', '[', self.line, self.column))
                self.pos += 1
                self.column += 1
                continue

            if self.text[self.pos] == ']':
                tokens.append(Token('RBRACKET', ']', self.line, self.column))
                self.pos += 1
                self.column += 1
                continue

            # Match repeat: x6
            if self.text[self.pos] == 'x' and self.peek_ahead().isdigit():
                tokens.append(self.read_repeat())
                continue

            # Match stitch count: (24)
            if self.text[self.pos] == '(':
                tokens.append(self.read_stitch_count())
                continue

            # Match comma
            if self.text[self.pos] == ',':
                tokens.append(Token('COMMA', ',', self.line, self.column))
                self.pos += 1
                self.column += 1
                continue

            # Match number
            if self.text[self.pos].isdigit():
                tokens.append(self.read_number())
                continue

            # Unknown character - raise error
            raise ParseError(f"Unexpected character '{self.text[self.pos]}' at line {self.line}, column {self.column}")

        return tokens

    def read_round_label(self) -> Token:
        """Read R<N>: token."""
        start_col = self.column
        self.pos += 1  # Skip 'R'
        self.column += 1

        num = ''
        while self.pos < len(self.text) and self.text[self.pos].isdigit():
            num += self.text[self.pos]
            self.pos += 1
            self.column += 1

        if self.pos < len(self.text) and self.text[self.pos] == ':':
            self.pos += 1
            self.column += 1
            return Token('ROUND_LABEL', f'R{num}:', self.line, start_col)
        else:
            raise ParseError(f"Expected ':' after round number at line {self.line}, column {self.column}")

    # ... (additional read methods for other tokens)

class Parser:
    """Parse tokens into PatternDSL."""

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def parse(self) -> PatternDSL:
        """Parse tokens into PatternDSL structure."""
        rounds = []

        while self.pos < len(self.tokens):
            round_obj = self.parse_round()
            rounds.append(round_obj)

        return PatternDSL(
            meta={
                'terms': 'US',  # Default to US
                'units': 'cm',
                'round_mode': 'spiral',
                'generated_by': 'text_parser',
            },
            rounds=rounds
        )

    def parse_round(self) -> Round:
        """Parse a single round."""
        # Expect ROUND_LABEL
        if not self.match('ROUND_LABEL'):
            raise ParseError(f"Expected round label, got {self.current_token().type}")

        round_label = self.consume('ROUND_LABEL').value
        round_num = int(round_label[1:-1])  # Extract number from R<N>:

        # Parse operations
        operations = self.parse_operations()

        # Expect STITCH_COUNT
        if not self.match('STITCH_COUNT'):
            raise ParseError(f"Expected stitch count at end of round {round_num}")

        stitch_count_token = self.consume('STITCH_COUNT')
        stitch_count = int(stitch_count_token.value[1:-1])  # Extract number from (<N>)

        return Round(
            round=round_num,
            stitches=stitch_count,
            operations=operations
        )

    def parse_operations(self) -> List[Operation]:
        """Parse comma-separated operations."""
        operations = []

        while not self.match('STITCH_COUNT'):
            if self.match('LBRACKET'):
                operations.extend(self.parse_repeat_group())
            else:
                operations.append(self.parse_operation())

            # Check for comma
            if self.match('COMMA'):
                self.consume('COMMA')

        return operations

    def parse_repeat_group(self) -> List[Operation]:
        """Parse [...] x<N> repeat group."""
        self.consume('LBRACKET')

        # Parse operations inside brackets
        group_operations = []
        while not self.match('RBRACKET'):
            group_operations.append(self.parse_operation())
            if self.match('COMMA'):
                self.consume('COMMA')

        self.consume('RBRACKET')

        # Expect x<N>
        if not self.match('REPEAT'):
            raise ParseError(f"Expected repeat count after ']'")

        repeat_token = self.consume('REPEAT')
        repeat_count = int(repeat_token.value[1:])  # Extract number from x<N>

        # Expand operations
        expanded = []
        for _ in range(repeat_count):
            expanded.extend(group_operations)

        return expanded

    def parse_operation(self) -> Operation:
        """Parse a single operation (stitch or special operation)."""
        # Check for count prefix (e.g., "2 sc")
        count = 1
        if self.match('NUMBER'):
            count = int(self.consume('NUMBER').value)

        # Parse stitch type
        if self.match('MAGIC_RING'):
            self.consume('MAGIC_RING')
            return Operation(type='magic_ring', count=count)
        elif self.match('STITCH'):
            stitch_type = self.consume('STITCH').value
            return Operation(type='stitch', stitch=stitch_type, count=count)
        elif self.match('OPERATION'):
            op_type = self.consume('OPERATION').value
            return Operation(type=op_type, count=count)
        else:
            raise ParseError(f"Expected operation, got {self.current_token().type}")

    def match(self, token_type: str) -> bool:
        """Check if current token matches type."""
        return self.pos < len(self.tokens) and self.tokens[self.pos].type == token_type

    def consume(self, token_type: str) -> Token:
        """Consume and return current token if it matches type."""
        if not self.match(token_type):
            raise ParseError(f"Expected {token_type}, got {self.current_token().type}")
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def current_token(self) -> Optional[Token]:
        """Return current token or None if at end."""
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

class ParseError(Exception):
    """Custom exception for parsing errors."""
    pass

def parse_pattern_text(text: str) -> PatternDSL:
    """
    Parse crochet pattern text into PatternDSL.

    Args:
        text: Pattern text with limited grammar support

    Returns:
        PatternDSL object

    Raises:
        ParseError: If text contains unsupported syntax or errors

    Example:
        >>> text = '''
        ... R1: MR 6 sc (6)
        ... R2: inc x6 (12)
        ... R3: [sc, inc] x6 (18)
        ... '''
        >>> dsl = parse_pattern_text(text)
    """
    try:
        lexer = Lexer(text)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        dsl = parser.parse()

        # Validate stitch counts
        for round_obj in dsl.rounds:
            computed_count = sum(op.count for op in round_obj.operations)
            if computed_count != round_obj.stitches:
                raise ParseError(
                    f"Round {round_obj.round}: stitch count mismatch. "
                    f"Operations sum to {computed_count}, but round declares {round_obj.stitches}"
                )

        return dsl

    except ParseError as e:
        # Re-raise with user-friendly message
        raise ParseError(
            f"Parse error: {str(e)}\n\n"
            f"Supported syntax:\n"
            f"  R1: MR 6 sc (6)\n"
            f"  R2: inc x6 (12)\n"
            f"  R3: [sc, inc] x6 (18)\n"
            f"  R4: [2 sc, inc] x6 (24)\n\n"
            f"Unsupported features:\n"
            f"  - Complex abbreviations (tr, dtr, bobbles, cables)\n"
            f"  - Row-based patterns\n"
            f"  - Color changes\n"
            f"  - Tapestry and colorwork syntax"
        )
```

**PDF Export Architecture:**

PDF generation uses `reportlab` (Python) for backend rendering. The PDF includes:

1. **Cover Page:** Title, shape, dimensions, yarn weight, hook size
2. **Materials Page:** Yarn yardage, hook size, notions
3. **Abbreviations Reference:** Full definitions of stitches used
4. **Pattern Page:** Human-readable pattern text, organized by round
5. **Visuals Page:** SVG diagrams (first 10 rounds, last 10 rounds, or key rounds)

**PDF Template Structure:**

```python
# knit_wit_engine/export/pdf_exporter.py

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from io import BytesIO
from knit_wit_engine.models.dsl import PatternDSL

class PDFExporter:
    """Export PatternDSL to PDF format."""

    def __init__(self, page_size=letter):
        self.page_size = page_size
        self.styles = getSampleStyleSheet()

        # Custom styles
        self.styles.add(ParagraphStyle(
            name='Title',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2C5F2D'),  # Knit-Wit brand color
            spaceAfter=30,
        ))

        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2C5F2D'),
            spaceBefore=20,
            spaceAfter=12,
        ))

        self.styles.add(ParagraphStyle(
            name='PatternText',
            parent=self.styles['Normal'],
            fontSize=12,
            fontName='Courier',  # Monospace for pattern text
            leftIndent=20,
        ))

    def export(self, dsl: PatternDSL, metadata: dict) -> bytes:
        """
        Export PatternDSL to PDF.

        Args:
            dsl: PatternDSL object
            metadata: Additional metadata (shape, dimensions, gauge, etc.)

        Returns:
            PDF bytes
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=self.page_size)
        story = []

        # Cover page
        story.extend(self._build_cover_page(dsl, metadata))
        story.append(self._page_break())

        # Materials page
        story.extend(self._build_materials_page(dsl, metadata))
        story.append(self._page_break())

        # Abbreviations reference
        story.extend(self._build_abbreviations_page(dsl))
        story.append(self._page_break())

        # Pattern page
        story.extend(self._build_pattern_page(dsl))

        # Visuals page (if diagrams available)
        if metadata.get('diagrams'):
            story.append(self._page_break())
            story.extend(self._build_visuals_page(dsl, metadata))

        # Footer
        story.extend(self._build_footer())

        # Build PDF
        doc.build(story)

        pdf_bytes = buffer.getvalue()
        buffer.close()

        return pdf_bytes

    def _build_cover_page(self, dsl: PatternDSL, metadata: dict):
        """Build cover page elements."""
        elements = []

        # Title
        title = metadata.get('name', 'Crochet Pattern')
        elements.append(Paragraph(title, self.styles['Title']))
        elements.append(Spacer(1, 0.5 * inch))

        # Shape info
        shape = metadata.get('shape', 'Unknown')
        dimensions = metadata.get('dimensions', {})
        elements.append(Paragraph(f"<b>Shape:</b> {shape.capitalize()}", self.styles['Normal']))

        if dimensions:
            dim_text = ', '.join([f"{k}: {v}" for k, v in dimensions.items()])
            elements.append(Paragraph(f"<b>Dimensions:</b> {dim_text}", self.styles['Normal']))

        elements.append(Spacer(1, 0.3 * inch))

        # Gauge
        gauge = metadata.get('gauge', {})
        if gauge:
            elements.append(Paragraph(
                f"<b>Gauge:</b> {gauge.get('sts_per_10cm')} stitches × {gauge.get('rows_per_10cm')} rows per 10cm",
                self.styles['Normal']
            ))

        # Hook size
        hook_size = metadata.get('hook_size', 'Unknown')
        elements.append(Paragraph(f"<b>Hook Size:</b> {hook_size}", self.styles['Normal']))

        return elements

    def _build_materials_page(self, dsl: PatternDSL, metadata: dict):
        """Build materials page elements."""
        elements = []
        elements.append(Paragraph("Materials", self.styles['SectionHeading']))

        # Yarn yardage
        yardage = metadata.get('yardage', 'Unknown')
        elements.append(Paragraph(f"<b>Yarn:</b> {yardage} meters", self.styles['Normal']))

        # Hook size
        hook_size = metadata.get('hook_size', 'Unknown')
        elements.append(Paragraph(f"<b>Hook:</b> {hook_size}", self.styles['Normal']))

        # Notions
        notions = metadata.get('notions', [])
        if notions:
            notions_text = ', '.join(notions)
            elements.append(Paragraph(f"<b>Notions:</b> {notions_text}", self.styles['Normal']))

        return elements

    def _build_abbreviations_page(self, dsl: PatternDSL):
        """Build abbreviations reference page."""
        elements = []
        elements.append(Paragraph("Abbreviations", self.styles['SectionHeading']))

        # Common abbreviations
        abbreviations = {
            'MR': 'Magic ring',
            'sc': 'Single crochet',
            'hdc': 'Half double crochet',
            'dc': 'Double crochet',
            'slst': 'Slip stitch',
            'ch': 'Chain',
            'inc': 'Increase (2 stitches in one stitch)',
            'dec': 'Decrease (single crochet 2 together)',
        }

        # Build table
        table_data = [['Abbreviation', 'Meaning']]
        for abbr, meaning in abbreviations.items():
            table_data.append([abbr, meaning])

        table = Table(table_data, colWidths=[1.5 * inch, 4 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C5F2D')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)

        return elements

    def _build_pattern_page(self, dsl: PatternDSL):
        """Build pattern page with round-by-round instructions."""
        elements = []
        elements.append(Paragraph("Pattern", self.styles['SectionHeading']))

        # Convert DSL rounds to human-readable text
        for round_obj in dsl.rounds:
            round_text = self._format_round(round_obj)
            elements.append(Paragraph(round_text, self.styles['PatternText']))

        return elements

    def _format_round(self, round_obj) -> str:
        """Convert Round object to human-readable text."""
        # This would format the round operations into pattern text
        # Example: "R1: MR 6 sc (6)"
        # For MVP, we'll use a simplified approach
        operations_text = ', '.join([self._format_operation(op) for op in round_obj.operations])
        return f"<b>R{round_obj.round}:</b> {operations_text} ({round_obj.stitches})"

    def _format_operation(self, operation) -> str:
        """Format a single operation."""
        if operation.type == 'magic_ring':
            return f"MR {operation.count}"
        elif operation.type == 'stitch':
            count_prefix = f"{operation.count} " if operation.count > 1 else ""
            return f"{count_prefix}{operation.stitch}"
        elif operation.type in ['inc', 'dec']:
            return f"{operation.type} x{operation.count}" if operation.count > 1 else operation.type
        else:
            return str(operation)

    def _build_visuals_page(self, dsl: PatternDSL, metadata: dict):
        """Build visuals page with diagrams."""
        elements = []
        elements.append(Paragraph("Diagrams", self.styles['SectionHeading']))

        # Add diagram images (from metadata['diagrams'])
        diagrams = metadata.get('diagrams', [])
        for diagram in diagrams:
            img = Image(diagram['path'], width=4*inch, height=4*inch)
            elements.append(img)
            elements.append(Paragraph(f"Round {diagram['round']}", self.styles['Normal']))
            elements.append(Spacer(1, 0.2 * inch))

        return elements

    def _build_footer(self):
        """Build footer with branding."""
        elements = []
        elements.append(Spacer(1, 1 * inch))
        elements.append(Paragraph(
            "Generated with Knit-Wit • https://knit-wit.app",
            self.styles['Normal']
        ))
        return elements

    def _page_break(self):
        """Return page break element."""
        from reportlab.platypus import PageBreak
        return PageBreak()
```

**SVG/PNG Export Architecture:**

SVG export generates individual SVG files for each round or a composite SVG with all rounds. PNG export renders SVG to raster format using `cairosvg` or `svglib`.

```python
# knit_wit_engine/export/svg_exporter.py

from knit_wit_engine.models.dsl import PatternDSL
from knit_wit_engine.visualization.visualizer import Visualizer
from typing import List
import io

class SVGExporter:
    """Export pattern diagrams to SVG format."""

    def export_round(self, dsl: PatternDSL, round_num: int, options: dict = None) -> str:
        """
        Export a single round to SVG.

        Args:
            dsl: PatternDSL object
            round_num: Round number to export (1-indexed)
            options: Rendering options (scale, colors, etc.)

        Returns:
            SVG string
        """
        visualizer = Visualizer()
        frames = visualizer.dsl_to_frames(dsl, options or {})

        # Get frame for specified round
        frame = frames[round_num - 1]  # 0-indexed

        # Render frame to SVG
        svg = self._render_frame_to_svg(frame, options or {})

        return svg

    def export_all_rounds(self, dsl: PatternDSL, options: dict = None) -> List[str]:
        """
        Export all rounds to individual SVG strings.

        Args:
            dsl: PatternDSL object
            options: Rendering options

        Returns:
            List of SVG strings, one per round
        """
        visualizer = Visualizer()
        frames = visualizer.dsl_to_frames(dsl, options or {})

        svgs = []
        for frame in frames:
            svg = self._render_frame_to_svg(frame, options or {})
            svgs.append(svg)

        return svgs

    def export_composite(self, dsl: PatternDSL, options: dict = None) -> str:
        """
        Export all rounds to a single composite SVG (grid layout).

        Args:
            dsl: PatternDSL object
            options: Rendering options (grid_cols, spacing, etc.)

        Returns:
            Composite SVG string
        """
        visualizer = Visualizer()
        frames = visualizer.dsl_to_frames(dsl, options or {})

        grid_cols = options.get('grid_cols', 4)
        spacing = options.get('spacing', 20)
        frame_size = options.get('frame_size', 200)

        # Calculate grid dimensions
        num_rows = (len(frames) + grid_cols - 1) // grid_cols
        canvas_width = grid_cols * (frame_size + spacing) + spacing
        canvas_height = num_rows * (frame_size + spacing) + spacing

        # Build composite SVG
        svg_parts = [
            f'<svg viewBox="0 0 {canvas_width} {canvas_height}" xmlns="http://www.w3.org/2000/svg">',
            f'  <title>Pattern Diagram - All Rounds</title>',
        ]

        for idx, frame in enumerate(frames):
            row = idx // grid_cols
            col = idx % grid_cols
            x = col * (frame_size + spacing) + spacing
            y = row * (frame_size + spacing) + spacing

            # Render frame as SVG group
            frame_svg = self._render_frame_to_svg_group(frame, x, y, frame_size, options or {})
            svg_parts.append(frame_svg)

        svg_parts.append('</svg>')

        return '\n'.join(svg_parts)

    def _render_frame_to_svg(self, frame, options: dict) -> str:
        """Render a single RenderFrame to SVG string."""
        size = options.get('size', 200)

        svg_parts = [
            f'<svg viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">',
            f'  <title>Round {frame.round}</title>',
            f'  <defs>',
            f'    <style>',
            f'      .stitch {{ fill: #3498db; stroke: #2c3e50; stroke-width: 1; }}',
            f'      .inc {{ fill: #2ecc71; }}',
            f'      .dec {{ fill: #e74c3c; }}',
            f'      .edge {{ stroke: #95a5a6; stroke-width: 1; fill: none; }}',
            f'    </style>',
            f'  </defs>',
        ]

        # Render edges
        for edge in frame.edges:
            from_node = frame.nodes[edge.from_id]
            to_node = frame.nodes[edge.to_id]
            svg_parts.append(
                f'  <line class="edge" x1="{from_node.x * size}" y1="{from_node.y * size}" '
                f'x2="{to_node.x * size}" y2="{to_node.y * size}" />'
            )

        # Render nodes
        for node in frame.nodes:
            # Determine class based on highlights
            node_class = 'stitch'
            for highlight in frame.highlights:
                if node.id in highlight.indices:
                    node_class = highlight.type
                    break

            svg_parts.append(
                f'  <circle class="{node_class}" cx="{node.x * size}" cy="{node.y * size}" r="8" />'
            )

            if node.label:
                svg_parts.append(
                    f'  <text x="{node.x * size}" y="{node.y * size + 4}" '
                    f'text-anchor="middle" font-size="10" fill="#fff">{node.label}</text>'
                )

        svg_parts.append('</svg>')

        return '\n'.join(svg_parts)

    def _render_frame_to_svg_group(self, frame, x: float, y: float, size: float, options: dict) -> str:
        """Render a single RenderFrame as an SVG group at specified position."""
        # Similar to _render_frame_to_svg but wrapped in <g> with transform
        svg = self._render_frame_to_svg(frame, {'size': size, **options})

        # Extract SVG content (remove outer <svg> tags)
        # Wrap in <g> with transform
        group = f'  <g transform="translate({x}, {y})">\n{svg}\n  </g>'

        return group
```

**JSON DSL Export:**

JSON export serializes the PatternDSL object to JSON format, ensuring round-trip compatibility.

```python
# knit_wit_engine/export/json_exporter.py

import json
from knit_wit_engine.models.dsl import PatternDSL

class JSONExporter:
    """Export PatternDSL to JSON format."""

    def export(self, dsl: PatternDSL) -> str:
        """
        Export PatternDSL to JSON string.

        Args:
            dsl: PatternDSL object

        Returns:
            JSON string
        """
        dsl_dict = dsl.to_dict()  # Assumes PatternDSL has to_dict() method
        return json.dumps(dsl_dict, indent=2)

    def export_bytes(self, dsl: PatternDSL) -> bytes:
        """Export PatternDSL to JSON bytes (UTF-8)."""
        return self.export(dsl).encode('utf-8')
```

---

### EPIC D: Pattern Generation Flow

**Epic Owner:** Frontend Lead + Backend Engineer
**Epic Duration:** Weeks 8-10 (Sprints 5-6)
**Total Effort:** ~39 story points
**Priority:** P0 (Critical Path)

#### Epic Overview

Implement the user-facing pattern generation workflow: shape selection, parameter input forms, gauge entry, API integration, and pattern preview. This epic connects the frontend UI to the backend pattern engine, enabling end-to-end pattern generation.

#### Epic Goals

- Users can generate patterns via intuitive form interface
- Shape-specific parameter forms with validation
- Visual gauge guide to help users confirm gauge
- API integration with loading states and error handling
- Pattern preview showing generated pattern text and yarn estimate

#### Epic Stories Summary

| Story ID | Title | Effort | Priority | Dependencies |
|----------|-------|--------|----------|--------------|
| GEN-1 | Shape selector screen | 5 pt | P0 | D1 (navigation) |
| GEN-2 | Params form (shape-specific) | 8 pt | P0 | GEN-1 |
| GEN-3 | Gauge input & confirmation | 8 pt | P0 | GEN-2 |
| GEN-4 | Generate API integration | 5 pt | P0 | GEN-3, A2-A4 (compilers) |
| GEN-5 | Pattern preview & review | 8 pt | P0 | GEN-4 |
| GEN-6 | Error handling & retry | 5 pt | P0 | GEN-4 |

**Total:** 39 story points

#### Epic Acceptance Criteria

- **AC-GEN-1:** User can select shape (sphere, cylinder, cone) via visual cards
- **AC-GEN-2:** Parameter forms show only relevant fields for selected shape
- **AC-GEN-3:** Gauge input validates ranges; visual guide helps users confirm gauge
- **AC-GEN-4:** Clicking "Generate" calls API, shows loading spinner, displays pattern on success
- **AC-GEN-5:** Pattern preview shows human-readable text, diagram thumbnail, yarn estimate
- **AC-GEN-6:** Error messages are user-friendly; retry button works correctly

---

### EPIC E: Kid Mode & Accessibility

**Epic Owner:** Frontend Lead + Accessibility Specialist
**Epic Duration:** Weeks 9-11 (Sprints 5-7)
**Total Effort:** ~55 story points
**Priority:** P0 (Critical Path for Launch)

#### Epic Overview

Make the application approachable for children and ensure WCAG AA compliance. Implement Kid Mode toggle activating a simplified UI variant with beginner-friendly terminology, larger tap targets, and animated stitch explanations. Ensure all interactive elements are accessible via keyboard and screen reader.

#### Epic Goals

- Kid Mode toggle activates child-friendly UI
- All interactive elements accessible via keyboard + screen reader
- Color contrast meets WCAG AA standards (4.5:1 normal, 3:1 large)
- Explanatory micro-animations help learners
- High-contrast mode for visual accessibility

#### Epic Stories Summary

| Story ID | Title | Effort | Priority | Dependencies |
|----------|-------|--------|----------|--------------|
| E1 | Kid Mode toggle & theme | 3 pt | P0 | D4 (theme system) |
| E2 | Copy rewrite (beginner-friendly) | 8 pt | P0 | E1 |
| E3 | Larger tap targets (Kid Mode) | 5 pt | P0 | E1 |
| E4 | Stitch explanation animations | 13 pt | P1 | B2 (SVG renderer) |
| E5 | Accessibility settings screen | 8 pt | P0 | D3 (settings screen) |
| E6 | Screen reader labels (full coverage) | 13 pt | P0 | E1, E5 |
| E7 | Color palette verification (WCAG AA) | 5 pt | P0 | None |

**Total:** 55 story points

#### Epic Acceptance Criteria

- **AC-E-1:** Kid Mode toggle in settings activates simplified UI
- **AC-E-2:** All copy uses beginner-friendly terminology (e.g., "Add two in one stitch" instead of "inc")
- **AC-E-3:** All tap targets in Kid Mode are at least 44x44pt
- **AC-E-4:** Stitch explanation animations are smooth and under 3 seconds
- **AC-E-5:** Keyboard navigation works on all screens (Tab, Shift+Tab, Enter, Arrow keys)
- **AC-E-6:** Screen reader announces all interactive elements with meaningful labels
- **AC-E-7:** Color contrast ratios verified: 4.5:1 (normal text), 3:1 (large text)

**Kid Mode Copy Examples:**

| Standard Term | Kid Mode Term |
|--------------|---------------|
| "inc" | "Add two in one stitch" |
| "dec" | "Combine two stitches" |
| "Magic ring" | "Start circle" |
| "Gauge" | "Stitch size" |
| "Hook size" | "Tool size" |
| "Yardage" | "How much yarn" |

---

### EPIC F: Telemetry & Monitoring

**Epic Owner:** Backend Engineer + Frontend Engineer
**Epic Duration:** Weeks 9-10 (Sprint 6)
**Total Effort:** ~20 story points
**Priority:** P1 (Nice-to-Have for MVP)

#### Epic Overview

Track user engagement (opt-in) and system health to enable data-driven improvements. Implement telemetry pipeline for key events (generation, visualization, export) and backend logging for monitoring.

#### Epic Goals

- Telemetry pipeline operational
- Key events tracked (generation, visualization, export, parse)
- Opt-in toggle respected across sessions
- Backend logging and error tracking in place

#### Epic Stories Summary

| Story ID | Title | Effort | Priority | Dependencies |
|----------|-------|--------|----------|--------------|
| F1 | Telemetry service (frontend) | 5 pt | P1 | None |
| F2 | Event emission: generation + visualization | 3 pt | P1 | F1 |
| F3 | Event emission: export + parse | 3 pt | P1 | F1 |
| F4 | Backend logging & structured logs | 5 pt | P0 | None |
| F5 | Error tracking (Sentry or similar) | 4 pt | P1 | None |

**Total:** 20 story points

#### Epic Acceptance Criteria

- **AC-F-1:** Opt-in toggle works; telemetry respects opt-out on app restart
- **AC-F-2:** Generation events logged with shape, gauge, success/failure status
- **AC-F-3:** Visualization events track round steps, pause/resume engagement
- **AC-F-4:** Export events track format (PDF, SVG, JSON) and success rate
- **AC-F-5:** Errors captured with stack traces and request context
- **AC-F-6:** Dashboards show top events and error rates

---

## Sprint Plans

### Sprint 5: Parsing & Generation (Weeks 8-9)

**Sprint Goal:** Text parser working; pattern generation flow end-to-end

**Duration:** 2 weeks
**Capacity:** ~75 story points
**Team:** Full team

#### Sprint Stories

| Story ID | Title | Effort | Owner | Priority |
|----------|-------|--------|-------|----------|
| C1 | Text parser (backend) | 13 pt | Backend Engineer | P0 |
| C2 | Parser test suite | 8 pt | Backend Engineer | P0 |
| C3 | PDF export endpoint (backend) | 13 pt | Backend Engineer | P0 |
| GEN-1 | Shape selector screen | 5 pt | Frontend Engineer | P0 |
| GEN-2 | Params form (shape-specific) | 8 pt | Frontend Engineer | P0 |
| GEN-3 | Gauge input & confirmation | 8 pt | Frontend Engineer | P0 |
| GEN-4 | Generate API integration | 5 pt | Frontend Engineer | P0 |
| GEN-5 | Pattern preview & review | 8 pt | Frontend Engineer | P0 |
| GEN-6 | Error handling & retry | 5 pt | Frontend Engineer | P0 |
| E1 | Kid Mode toggle & theme | 3 pt | Frontend Lead | P0 |

**Total:** 76 points

#### Sprint Objectives

1. **Text parser functional:** Parse canonical patterns with 90%+ accuracy
2. **PDF export working:** Backend endpoint generates valid PDFs
3. **Generation flow complete:** User can generate sphere via form → visualize → see preview
4. **Kid Mode toggle ready:** Infrastructure in place for Kid Mode UI

#### Demo Goals

- Demo parsing a simple pattern: `R1: MR 6 sc (6)\nR2: inc x6 (12)\nR3: [sc, inc] x6 (18)`
- Demo generating a sphere via form → visualizing → exporting to PDF
- Demo Kid Mode toggle (even if copy not fully rewritten)

#### Risks

| Risk | Mitigation |
|------|-----------|
| Parser complexity exceeds estimates | Time-box to 16 hours; defer advanced grammar to v1.1 |
| PDF library issues | Test `reportlab` in week 1; have print-to-PDF fallback |
| Form validation complexity | Use standard validation libraries; defer edge cases |

---

### Sprint 6: Export & Accessibility (Weeks 10-11)

**Sprint Goal:** All export formats working; WCAG AA compliance achieved

**Duration:** 2 weeks
**Capacity:** ~80 story points
**Team:** Full team

#### Sprint Stories

| Story ID | Title | Effort | Owner | Priority |
|----------|-------|--------|-------|----------|
| C4 | SVG/PNG export endpoint (backend) | 8 pt | Backend Engineer | P1 |
| C5 | Export screen UI (frontend) | 8 pt | Frontend Engineer | P0 |
| C6 | Parse input screen UI (frontend) | 8 pt | Frontend Engineer | P1 |
| E2 | Copy rewrite (beginner-friendly) | 8 pt | Frontend Lead | P0 |
| E3 | Larger tap targets (Kid Mode) | 5 pt | Frontend Engineer | P0 |
| E5 | Accessibility settings screen | 8 pt | Frontend Lead | P0 |
| E6 | Screen reader labels (full coverage) | 13 pt | Frontend Lead | P0 |
| E7 | Color palette verification (WCAG AA) | 5 pt | Frontend Engineer | P0 |
| F1 | Telemetry service (frontend) | 5 pt | Frontend Engineer | P1 |
| F2 | Event emission: generation + visualization | 3 pt | Frontend Engineer | P1 |
| F3 | Event emission: export + parse | 3 pt | Frontend Engineer | P1 |
| F4 | Backend logging & structured logs | 5 pt | Backend Engineer | P0 |
| F5 | Error tracking (Sentry) | 4 pt | Backend Engineer | P1 |

**Total:** 83 points

#### Sprint Objectives

1. **All export formats functional:** PDF, SVG, PNG, JSON exports working
2. **WCAG AA compliance:** Screen reader labels, keyboard navigation, color contrast verified
3. **Kid Mode UI complete:** Beginner-friendly copy, larger tap targets, simplified UI
4. **Telemetry operational:** Events logged; opt-in toggle works

#### Demo Goals

- Demo exporting pattern to PDF, SVG, and JSON
- Demo Kid Mode UI with simplified terminology and larger buttons
- Demo keyboard navigation through entire app (Tab, Shift+Tab, Enter)
- Demo screen reader announcements (VoiceOver on iOS, TalkBack on Android)

#### Risks

| Risk | Mitigation |
|------|-----------|
| WCAG AA audit finds critical issues | Integrate automated audits (axe-core) early; fix incrementally |
| Kid Mode copy rewrite takes longer than expected | Time-box to 8 hours; deprioritize animated explanations to v1.1 |
| Telemetry integration complexity | Use simple event emitter; defer advanced analytics to v1.1 |

---

### Sprint 7: Polish & Integration (Week 11, partial)

**Sprint Goal:** Final integration; all features working end-to-end; ready for QA

**Duration:** 1 week (overlap with Sprint 6 end)
**Capacity:** ~40 story points
**Team:** Full team

#### Sprint Stories

| Story ID | Title | Effort | Owner | Priority |
|----------|-------|--------|-------|----------|
| E4 | Stitch explanation animations | 13 pt | Frontend Engineer | P1 |
| D6 | HTTP client + error handling | 3 pt | Frontend Engineer | P0 |
| D7 | Local storage for preferences | 3 pt | Frontend Engineer | P0 |
| D8 | Accessibility options (text size, contrast) | 8 pt | Frontend Lead | P0 |
| BUG-1 | Triage open issues | 3 pt | QA Engineer | P0 |
| BUG-2 | Critical bugs (Phase 3) | 13 pt | Full team | P0 |

**Total:** 43 points

#### Sprint Objectives

1. **Stitch animations complete:** Visual explanations for inc/dec (if time permits)
2. **All settings persist:** Preferences saved to local storage
3. **Accessibility options functional:** Text size, high-contrast mode working
4. **Critical bugs fixed:** No blockers for QA phase

#### Demo Goals

- Demo full end-to-end flow: Generate → Visualize → Export → Parse
- Demo all settings persisting across app restarts
- Demo stitch explanation animations (if complete)
- Demo bug fixes

#### Risks

| Risk | Mitigation |
|------|-----------|
| Animations take longer than estimated | Defer to v1.1 if not complete by end of Sprint 7 |
| Integration issues between features | Daily integration testing; fix issues as they arise |

---

## Technical Implementation

### Text Parser Grammar Specification

**Formal Grammar (EBNF):**

```ebnf
pattern       ::= round+
round         ::= round_label operations stitch_count
round_label   ::= "R" digit+ ":"
operations    ::= operation ("," operation)*
operation     ::= simple_op | repeat_group
simple_op     ::= (digit+ WS)? stitch_type
stitch_type   ::= "MR" | "sc" | "hdc" | "dc" | "slst" | "ch" | "inc" | "dec"
repeat_group  ::= "[" operations "]" "x" digit+
stitch_count  ::= "(" digit+ ")"
digit         ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
WS            ::= " " | "\t"
```

**Parsing Algorithm:**

1. **Lexical Analysis:** Tokenize input text into tokens (ROUND_LABEL, STITCH, LBRACKET, etc.)
2. **Syntax Analysis:** Parse tokens into AST (Abstract Syntax Tree)
3. **Semantic Analysis:** Validate stitch counts, detect unsupported syntax
4. **DSL Generation:** Convert AST to PatternDSL structure
5. **Validation:** Verify stitch count correctness, round numbering

**Error Handling:**

- **Unsupported Tokens:** Display warning: "Token 'tr' not supported. Use sc, hdc, or dc."
- **Stitch Count Mismatch:** Error: "Round 3: Operations sum to 17 stitches, but round declares 18. Check pattern."
- **Missing Stitch Count:** Error: "Round 4: Missing stitch count. Expected (N) at end of round."
- **Invalid Bracket Matching:** Error: "Round 5: Unmatched bracket. Expected ']'."

**Test Cases:**

```python
# tests/unit/test_text_parser.py

def test_parse_simple_pattern():
    """Test parsing simple canonical pattern."""
    text = """
    R1: MR 6 sc (6)
    R2: inc x6 (12)
    R3: [sc, inc] x6 (18)
    """
    dsl = parse_pattern_text(text)

    assert len(dsl.rounds) == 3
    assert dsl.rounds[0].stitches == 6
    assert dsl.rounds[1].stitches == 12
    assert dsl.rounds[2].stitches == 18

def test_parse_complex_pattern():
    """Test parsing pattern with multiple repeat groups."""
    text = "R4: [2 sc, inc] x6 (24)"
    dsl = parse_pattern_text(text)

    assert len(dsl.rounds) == 1
    assert dsl.rounds[0].stitches == 24
    assert len(dsl.rounds[0].operations) == 18  # 6 repeats of [2 sc, inc]

def test_parse_error_unsupported_stitch():
    """Test error handling for unsupported stitch."""
    text = "R1: tr x6 (6)"

    with pytest.raises(ParseError) as exc:
        parse_pattern_text(text)

    assert "not supported" in str(exc.value).lower()

def test_parse_error_stitch_count_mismatch():
    """Test error handling for stitch count mismatch."""
    text = "R2: inc x5 (12)"  # Should be 10 stitches, not 12

    with pytest.raises(ParseError) as exc:
        parse_pattern_text(text)

    assert "mismatch" in str(exc.value).lower()
```

### PDF Generation Implementation

**Dependencies:**

- `reportlab` (Python): PDF generation library
- `Pillow` (Python): Image processing for diagrams

**PDF Template Structure:**

```
┌─────────────────────────────────────┐
│         Cover Page                  │
│  - Title                            │
│  - Shape & Dimensions               │
│  - Gauge & Hook Size                │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│         Materials Page              │
│  - Yarn Yardage                     │
│  - Hook Size                        │
│  - Notions                          │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│         Abbreviations Page          │
│  - Table of Abbreviations           │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│         Pattern Page                │
│  - Round-by-Round Instructions      │
│  - Formatted Pattern Text           │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│         Visuals Page                │
│  - Diagram Images                   │
│  - First 10 rounds, Last 10 rounds  │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│         Footer                      │
│  - "Generated with Knit-Wit"        │
└─────────────────────────────────────┘
```

**Page Size Support:**

- **Letter (8.5" × 11"):** Default for US users
- **A4 (210mm × 297mm):** Default for international users
- Auto-detect based on locale or user preference

**Branding:**

- Knit-Wit logo in header (if available)
- Brand color (#2C5F2D) for headings
- Footer: "Generated with Knit-Wit • https://knit-wit.app"

### SVG Export Format Specification

**SVG Structure:**

```xml
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <title>Round 1</title>
  <defs>
    <style>
      .stitch { fill: #3498db; stroke: #2c3e50; stroke-width: 1; }
      .inc { fill: #2ecc71; }
      .dec { fill: #e74c3c; }
      .edge { stroke: #95a5a6; stroke-width: 1; fill: none; }
    </style>
  </defs>

  <!-- Edges (connections between stitches) -->
  <line class="edge" x1="100" y1="100" x2="120" y2="80" />
  <!-- ... more edges ... -->

  <!-- Nodes (stitches) -->
  <circle class="stitch" cx="100" cy="100" r="8" />
  <circle class="inc" cx="120" cy="80" r="8" />
  <!-- ... more nodes ... -->

  <!-- Labels -->
  <text x="100" y="104" text-anchor="middle" font-size="10" fill="#fff">1</text>
  <!-- ... more labels ... -->
</svg>
```

**Color Palette:**

- **Normal Stitch:** `#3498db` (blue)
- **Increase:** `#2ecc71` (green)
- **Decrease:** `#e74c3c` (red)
- **Edge:** `#95a5a6` (gray)
- **Background:** `#ffffff` (white)

**Export Options:**

- **Individual SVGs:** One SVG file per round (ZIP archive)
- **Composite SVG:** Grid layout with all rounds on single page
- **PNG Rendering:** Convert SVG to PNG (72 DPI screen, 300 DPI print)

### JSON DSL Export Format

**Format:** Standard Pattern DSL JSON (see §11 in PRD)

**Example:**

```json
{
  "meta": {
    "version": "1.0",
    "generated_by": "knit-wit-mvp",
    "shape": "sphere",
    "dimensions": {
      "diameter": 10
    },
    "gauge": {
      "sts_per_10cm": 14,
      "rows_per_10cm": 16
    },
    "hook_size": "3.5mm",
    "yarn_weight": "DK",
    "yardage": 45,
    "terms": "US",
    "units": "cm",
    "round_mode": "spiral"
  },
  "rounds": [
    {
      "round": 1,
      "stitches": 6,
      "operations": [
        { "type": "magic_ring" },
        { "type": "stitch", "stitch": "sc", "count": 6 }
      ]
    },
    {
      "round": 2,
      "stitches": 12,
      "operations": [
        { "type": "inc", "count": 6 }
      ]
    }
    // ... more rounds ...
  ]
}
```

**Validation:**

- JSON schema validation on export
- Round-trip test: Export → Import → Export produces identical JSON

---

## Success Criteria

### Phase Exit Criteria

Phase 3 is **COMPLETE** when ALL of the following are true:

- [ ] **End-to-End Generation Flow:** User can generate sphere via form → visualize → export to PDF without errors
- [ ] **Text Parser Functional:** Parser handles canonical bracket/repeat syntax with 90%+ accuracy
- [ ] **All Export Formats Working:** PDF, SVG, and JSON exports are valid and functional
- [ ] **Kid Mode Operational:** Toggle activates simplified UI; copy is beginner-friendly
- [ ] **WCAG AA Compliance:** Screen reader labels, keyboard navigation, color contrast meet WCAG AA standards
- [ ] **Telemetry Pipeline Operational:** Opt-in toggle works; key events logged correctly
- [ ] **All Phase 3 Stories Complete:** 100% of committed stories in "Done" state
- [ ] **No Critical Bugs:** Zero P0 bugs; all high-priority bugs triaged
- [ ] **Sprint Demos Successful:** All sprint demos completed with stakeholder sign-off
- [ ] **Documentation Updated:** API docs, user guides, and developer docs reflect Phase 3 features

### Feature Acceptance Criteria

#### Pattern Generation

- [ ] Shape selector displays sphere, cylinder, cone options with visual cards
- [ ] Parameter forms show only relevant fields for selected shape
- [ ] Gauge input validates ranges (sts: 8-30, rows: 8-30 per 10cm)
- [ ] Visual gauge guide helps users confirm gauge (optional but recommended)
- [ ] Clicking "Generate" calls `/api/v1/patterns/generate` endpoint
- [ ] Loading spinner displays during API call
- [ ] Pattern preview shows human-readable text, diagram thumbnail, yarn estimate
- [ ] Error messages are user-friendly (e.g., "Invalid gauge. Please enter 8-30 stitches per 10cm.")
- [ ] Retry button re-attempts generation after error

#### Text Parsing

- [ ] Parser successfully parses: `R1: MR 6 sc (6)`
- [ ] Parser successfully parses: `R2: inc x6 (12)`
- [ ] Parser successfully parses: `R3: [sc, inc] x6 (18)`
- [ ] Parser successfully parses: `R4: [2 sc, inc] x6 (24)`
- [ ] Parser rejects unsupported syntax with clear warning (e.g., "Token 'tr' not supported")
- [ ] Stitch count mismatches produce error: "Round 3: Operations sum to 17, but round declares 18"
- [ ] Parse errors indicate line and token that failed
- [ ] Parsed patterns visualize identically to generated patterns

#### Export Functionality

- [ ] PDF export generates without error for any valid pattern
- [ ] PDF prints correctly on A4 and Letter paper (both orientations)
- [ ] PDF includes all sections: cover, materials, abbreviations, pattern, visuals, footer
- [ ] PDF file size < 5 MB for typical pattern
- [ ] SVG export produces valid SVG files (validate against SVG schema)
- [ ] SVG files open in Illustrator and Inkscape without warnings
- [ ] PNG export renders clearly at 72 DPI (screen) and 300 DPI (print)
- [ ] JSON export is valid JSON (passes schema validation)
- [ ] JSON round-trip works: Export → Import → Visualize produces identical pattern

#### Kid Mode

- [ ] Kid Mode toggle in settings activates simplified UI
- [ ] All copy uses beginner-friendly terminology (see Kid Mode table above)
- [ ] All tap targets in Kid Mode are at least 44×44pt
- [ ] Stitch explanation animations are smooth and under 3 seconds (if implemented)
- [ ] Kid Mode theme applies consistently across all screens
- [ ] Toggling Kid Mode off restores standard UI

#### Accessibility

- [ ] Keyboard navigation works: Tab, Shift+Tab navigate all controls
- [ ] Enter activates buttons; Arrow keys navigate lists
- [ ] Screen reader announces all interactive elements with meaningful labels
- [ ] All images have alt text; decorative images use empty alt=""
- [ ] Color contrast ratios meet WCAG AA: 4.5:1 (normal), 3:1 (large)
- [ ] High-contrast mode toggles successfully
- [ ] Text size option works (small, medium, large, extra-large)
- [ ] Focus indicators are visible on all interactive elements

#### Telemetry

- [ ] Opt-in toggle in settings works
- [ ] Telemetry respects opt-out; no events logged if opted out
- [ ] Preference persists across app restarts
- [ ] Generation events logged with shape, gauge, success/failure
- [ ] Visualization events track round steps, pause/resume
- [ ] Export events track format (PDF, SVG, JSON) and success rate
- [ ] Parse events track success rate and error types
- [ ] Dashboards show event counts and error rates (backend)

### Performance Benchmarks

- [ ] Pattern generation API response time: < 200ms (sphere, 10cm diameter, gauge 14/16)
- [ ] PDF export generation time: < 2 seconds (typical 30-round pattern)
- [ ] SVG export generation time: < 1 second (per round)
- [ ] Parsing time: < 100ms (typical 20-round pattern)
- [ ] App startup time: < 2 seconds (cold start on iPhone 12)
- [ ] Navigation between screens: < 300ms (perceived latency)

### Quality Standards

- [ ] Unit test coverage: 80%+ for backend, 70%+ for frontend
- [ ] Integration tests pass for all critical flows
- [ ] E2E tests pass: Generate → Visualize → Export
- [ ] Code review completed for all stories (2+ approvals)
- [ ] No linting errors or warnings in CI
- [ ] All TypeScript types defined (no `any` except approved exceptions)

---

## Dependencies & Blockers

### Internal Dependencies

**Critical Path:**

```
Phase 2 Complete (Visualization Foundation)
    ↓
EPIC C (Parsing & I/O) + EPIC D (Generation Flow)
    ↓
EPIC E (Kid Mode & Accessibility) + EPIC F (Telemetry)
    ↓
Phase 3 Complete → Phase 4 (QA & Polish)
```

**Story-Level Dependencies:**

- **C1 (Text parser)** → C2 (Parser tests), C6 (Parse UI)
- **C3 (PDF export)** → C5 (Export UI)
- **C4 (SVG export)** → C5 (Export UI)
- **GEN-1 (Shape selector)** → GEN-2 (Params form) → GEN-3 (Gauge input) → GEN-4 (API integration) → GEN-5 (Preview)
- **E1 (Kid Mode toggle)** → E2 (Copy rewrite), E3 (Tap targets), E6 (Screen reader labels)
- **F1 (Telemetry service)** → F2 (Event emission: gen/viz), F3 (Event emission: export/parse)

### External Dependencies

| Dependency | Version | Purpose | Risk | Mitigation |
|-----------|---------|---------|------|-----------|
| `reportlab` | 3.6+ | PDF generation | Medium | Test early; have print-to-PDF fallback |
| `Pillow` | 10.0+ | Image processing | Low | Widely used; stable |
| `cairosvg` | 2.7+ | SVG to PNG conversion | Medium | Test early; use `svglib` as fallback |
| `react-native-svg` | Latest | SVG rendering | Low | Already used in Phase 2 |
| `@react-native-async-storage/async-storage` | Latest | Local storage | Low | Mature library |
| `react-native-fs` | Latest | File system access for exports | Medium | Test on iOS and Android |

### Potential Blockers

| Blocker | Likelihood | Impact | Workaround |
|---------|-----------|--------|-----------|
| **PDF library incompatibility with Python 3.11+** | Low | High | Pin Python version to 3.10; test early |
| **SVG to PNG conversion fails on Android** | Medium | Medium | Use web service (e.g., Cloudinary) as fallback |
| **Parsing complexity exceeds estimates** | Medium | Medium | Limit grammar scope; defer advanced syntax to v1.1 |
| **WCAG AA audit finds critical issues** | Medium | High | Integrate automated audits early; fix incrementally |
| **Kid Mode scope creep (animations)** | High | Medium | Time-box to 13 hours; defer to v1.1 if needed |
| **File export permissions on iOS/Android** | Low | High | Test early; request permissions correctly |

### Blocker Resolution Process

1. **Identify blocker** in daily standup or retro
2. **Assign owner** to investigate workaround (max 2 hours)
3. **Escalate to project lead** if no workaround found
4. **Update timeline/scope** if blocker is critical
5. **Document in risk register** for future sprints

---

## Risks

### Technical Risks

| Risk | Probability | Impact | Mitigation | Owner |
|------|-------------|--------|-----------|-------|
| **PDF generation library produces invalid PDFs** | Medium | High | Test `reportlab` in Sprint 5; validate PDFs with multiple viewers (Adobe, Preview, Chrome) | Backend Engineer |
| **Text parser fails on real-world patterns** | High | Medium | Limit grammar to canonical syntax; show clear error messages; defer complex patterns to v1.1 | Backend Engineer |
| **SVG export file size too large** | Low | Medium | Optimize SVG (remove redundant nodes); compress with gzip | Backend Engineer |
| **Kid Mode animations cause performance issues** | Medium | Medium | Profile animations early; use CSS transforms; defer to v1.1 if needed | Frontend Engineer |
| **Screen reader compatibility issues on Android** | Medium | High | Test TalkBack early and often; follow Android accessibility guidelines | Frontend Lead |
| **File export permissions fail on iOS** | Low | High | Request permissions correctly; test on iOS 14, 15, 16 | Frontend Engineer |

### Schedule Risks

| Risk | Probability | Impact | Mitigation | Owner |
|------|-------------|--------|-----------|-------|
| **Scope creep on Kid Mode features** | High | Medium | Define Kid Mode MVP clearly; time-box animations to 13 hours | Product Owner |
| **Parsing complexity exceeds Sprint 5 capacity** | Medium | High | Limit grammar scope; defer complex patterns to v1.1; communicate early | Backend Engineer |
| **Accessibility audit finds critical issues late** | Medium | High | Integrate automated audits (axe-core) from Sprint 5; fix incrementally | QA Lead |
| **Export UI takes longer than estimated** | Low | Medium | Use standard components; defer advanced features (preview) to v1.1 | Frontend Engineer |
| **Team velocity lower than estimated** | Medium | Medium | Adjust sprint scope; deprioritize P1 stories (animations, telemetry) | Scrum Master |

### Resource Risks

| Risk | Probability | Impact | Mitigation | Owner |
|------|-------------|--------|-----------|-------|
| **Backend engineer unavailable during Sprint 5** | Low | High | Cross-train frontend engineer on backend; pair program on parsing | Engineering Lead |
| **Accessibility specialist unavailable** | Low | High | Use automated audits; engage external consultant if needed | Project Lead |
| **Design changes to Kid Mode late in phase** | Medium | Medium | Finalize Kid Mode designs by end of Sprint 5; limit iterations | Product Owner |

### Mitigation Strategy

**Risk Monitoring:**
- Review risks weekly in sprint planning
- Update risk register after each sprint
- Escalate to project lead if probability or impact increases

**Escalation Process:**
1. If risk becomes imminent (probability > 70%), discuss in standup
2. Assign owner to develop mitigation plan (max 2 hours)
3. Implement mitigation or escalate to project lead
4. Update timeline/scope if needed
5. Document decision and communicate to team

---

## Phase Exit Criteria

Phase 3 is **READY TO EXIT** when ALL of the following are verified:

### Feature Completeness

- [ ] All EPIC C stories complete (Parsing & I/O)
- [ ] All EPIC D stories complete (Pattern Generation Flow)
- [ ] All EPIC E stories complete (Kid Mode & Accessibility)
- [ ] All EPIC F stories complete (Telemetry & Monitoring)
- [ ] All Sprint 5, 6, 7 stories marked "Done"

### Quality Gates

- [ ] All unit tests pass (80%+ coverage for backend, 70%+ for frontend)
- [ ] All integration tests pass
- [ ] E2E tests pass for critical flows (Generate → Visualize → Export)
- [ ] Code review completed for all stories (2+ approvals)
- [ ] No linting errors or warnings
- [ ] Performance benchmarks met (< 200ms generation, < 2s PDF export)

### Functional Verification

- [ ] End-to-end flow works: Generate → Visualize → Export to PDF
- [ ] Text parser handles canonical patterns with 90%+ accuracy
- [ ] All export formats produce valid files (PDF, SVG, JSON)
- [ ] Kid Mode toggle activates simplified UI
- [ ] WCAG AA compliance verified (0 critical issues)
- [ ] Telemetry opt-in works; events logged correctly

### Documentation

- [ ] API documentation updated (Swagger/OpenAPI)
- [ ] User guide updated with parsing and export instructions
- [ ] Developer documentation updated (README, CONTRIBUTING)
- [ ] Release notes drafted for Phase 3 features

### Stakeholder Sign-Off

- [ ] Sprint demos completed and approved
- [ ] Product owner sign-off on feature completeness
- [ ] Engineering lead sign-off on technical quality
- [ ] QA lead sign-off on test coverage

### Handoff to Phase 4

- [ ] Known issues triaged and documented
- [ ] Phase 4 backlog prepared (QA & Polish stories)
- [ ] Team retro completed; action items documented
- [ ] Phase 3 metrics recorded (velocity, burndown, bugs)

---

## Next Phase Preview

### Phase 4: QA & Polish (Weeks 12-15)

**Focus:** Cross-device testing, accessibility audits, performance optimization, bug fixes, documentation

**Key Activities:**

1. **Cross-Device Testing:** iOS 14+, Android 10+, tablets, landscape/portrait
2. **Accessibility Audit:** WCAG AA audit report with zero critical issues
3. **Performance Optimization:** Profile and optimize hot paths; reduce bundle size
4. **Bug Triage & Fixes:** Fix all P0 bugs; triage P1/P2 bugs
5. **Documentation:** Complete API docs, user guides, developer docs

**Deliverables:**

- [ ] Cross-device smoke tests complete (iOS, Android, tablets)
- [ ] Accessibility audit report with 0 critical, < 5 warnings
- [ ] Performance benchmarks met (< 200ms generation, > 50 fps visualization)
- [ ] All P0 bugs fixed; P1 bugs triaged
- [ ] Documentation complete and reviewed

**Success Criteria:**

- [ ] Zero critical bugs
- [ ] Automated E2E tests pass on iOS and Android
- [ ] WCAG AA audit: 0 critical, < 5 warnings
- [ ] Performance benchmarks met
- [ ] Bundle size within limits (APK < 50MB, IPA < 100MB)
- [ ] Documentation complete

**Timeline:**
- **Week 12:** Cross-device testing, accessibility audit
- **Week 13:** Performance optimization, bug fixes
- **Week 14:** Documentation, regression testing
- **Week 15:** Final polish, release preparation

---

## Appendix

### Story Point Reference

| Points | Complexity | Effort | Examples |
|--------|-----------|--------|----------|
| 1 pt | Trivial | < 1 hour | Config change, typo fix |
| 3 pt | Simple | 2-4 hours | Simple UI component, basic endpoint |
| 5 pt | Medium | 1 day | Form with validation, API integration |
| 8 pt | Complex | 1.5-2 days | Complex UI flow, parser implementation |
| 13 pt | Very Complex | 2-3 days | Full feature (e.g., PDF export) |
| 21 pt | Epic-level | 4-5 days | Too large; should be split |

### Definition of Done Checklist

A story is **DONE** only when:

- [ ] Code written per acceptance criteria
- [ ] All unit tests pass (100% green CI)
- [ ] Code reviewed (2+ approvals)
- [ ] Test coverage > 80% (backend) or 70% (frontend)
- [ ] Documentation updated (docstrings, comments, external docs)
- [ ] Performance benchmarks met (if applicable)
- [ ] Accessibility compliance verified (if applicable)
- [ ] No regressions (existing tests still pass)
- [ ] Code merged to main
- [ ] Demo-ready (works end-to-end, no UX issues)

### Key Contacts

| Role | Name | Responsibilities |
|------|------|-----------------|
| **Product Owner** | TBD | Feature prioritization, sprint planning, stakeholder communication |
| **Engineering Lead** | TBD | Architecture decisions, code reviews, technical escalation |
| **Backend Engineer** | TBD | Pattern engine, parsing, export endpoints |
| **Frontend Lead** | TBD | UI implementation, Kid Mode, accessibility |
| **Frontend Engineer** | TBD | Generation UI, export UI, telemetry |
| **QA Engineer** | TBD | Test planning, manual testing, bug triage |
| **Scrum Master** | TBD | Sprint facilitation, retrospectives, blocker resolution |

---

**Document Version:** 1.0
**Last Updated:** 2025-11-05
**Next Review:** End of Sprint 5 (Week 9)
