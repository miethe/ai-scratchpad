# Phase 3: Full Feature Implementation

**Duration:** Weeks 8-11 (Sprints 5-7)
**Team:** 2 BE, 2 FE, 1 QA
**Capacity:** ~180-200 story points
**Status:** Planned

---

## Phase Overview

Phase 3 completes MVP feature development by implementing pattern parsing, multi-format exports, accessibility features, and telemetry. This phase delivers end-to-end user flows from pattern generation through visualization to professional exports.

**Core Deliverables:**
- Backend: Text pattern parser (limited grammar)
- Backend: PDF export (reportlab/weasyprint)
- Backend: SVG/PNG export endpoints
- Backend: Telemetry event pipeline (opt-in)
- Frontend: Export screen with format selection
- Frontend: Kid Mode toggle and simplified UI
- Frontend: Full accessibility (screen reader, high contrast, dyslexia font)
- Frontend: Settings screen completion
- Frontend: Telemetry opt-in/opt-out controls

**Key Technologies:**
- Backend: pyparsing (parser), reportlab/weasyprint (PDF), Pillow (PNG)
- Frontend: AsyncStorage (settings), react-native-fs (downloads)
- Testing: pytest (BE), Jest (FE), axe-core (accessibility)

### Phase Context

**Preceding Phase:**
- Phase 2: Visualization Foundation (Weeks 5-7) delivered RN/Expo app shell, SVG rendering engine, round scrubber, and basic interactivity. DSL → visualization frames functional.

**Following Phase:**
- Phase 4: QA & Polish (Weeks 12-15) focuses on cross-device testing, performance optimization, accessibility audits, and bug fixes for launch readiness.

**Critical Path:**
Yes. Export and accessibility features block launch. Parser enables external pattern workflows.

---

## Goals & Deliverables

### Primary Goals

1. **Text Pattern Parsing**
   - Parse bracket/repeat grammar: `R3: [2 sc, inc] x6 (18)`
   - Convert to PatternDSL with validation
   - User-friendly error messages for unsupported syntax

2. **Multi-Format Export**
   - PDF: Professional layout (cover, materials, pattern, diagrams)
   - SVG: Editable vector diagrams per round or composite
   - PNG: Raster preview (72 DPI screen, 300 DPI print)
   - JSON: Pattern DSL round-trip compatible

3. **Kid Mode Implementation**
   - Simplified UI with larger tap targets (56×56 dp)
   - Beginner-friendly copy (grade 4-5 reading level)
   - Animated stitch tutorials (increase, decrease)
   - Safe, vibrant color palette

4. **Accessibility Compliance**
   - WCAG AA: color contrast, ARIA labels, keyboard nav
   - Screen reader support (NVDA, JAWS, VoiceOver)
   - Colorblind-friendly palettes (patterns + symbols)
   - Dyslexia-friendly font option (OpenDyslexic)
   - Motion respect (prefers-reduced-motion)

5. **Telemetry Infrastructure**
   - Opt-in event tracking (generation, visualization, export)
   - Backend logging pipeline (no PII)
   - Settings toggle for opt-in/opt-out
   - 90-day data retention policy

6. **Settings Persistence**
   - AsyncStorage for preferences (terminology, units, theme)
   - Kid Mode toggle
   - Accessibility preferences
   - Telemetry consent

### Key Deliverables

**Backend:**
- [ ] `app/services/parser_service.py` - Text → DSL converter
- [ ] `app/services/export_service.py` - PDF/SVG/PNG generators
- [ ] `app/api/routes/parser.py` - POST /parse endpoint
- [ ] `app/api/routes/export.py` - POST /export/{format} endpoints
- [ ] `app/services/telemetry_service.py` - Event pipeline
- [ ] `tests/unit/test_parser_service.py` - Parser unit tests
- [ ] `tests/unit/test_export_service.py` - Export unit tests
- [ ] `tests/integration/test_export_api.py` - Export contract tests

**Frontend:**
- [ ] `src/screens/ExportScreen.tsx` - Export format selection UI
- [ ] `src/screens/ParseScreen.tsx` - Text input and validation
- [ ] `src/screens/SettingsScreen.tsx` - Complete settings UI
- [ ] `src/components/kidmode/SimplifiedUI.tsx` - Kid Mode components
- [ ] `src/components/accessibility/A11yControls.tsx` - Accessibility toggles
- [ ] `src/services/telemetryClient.ts` - Event tracking
- [ ] `src/theme/kidModeTheme.ts` - Kid Mode color/typography
- [ ] `src/theme/accessibilityTheme.ts` - High contrast, dyslexia font
- [ ] `__tests__/screens/ExportScreen.test.tsx` - Component tests
- [ ] `__tests__/accessibility/a11y.test.tsx` - Accessibility tests

### Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Parser accuracy | 90%+ canonical patterns | Unit tests |
| PDF generation time | < 5s | pytest-benchmark |
| Export file size (PDF) | < 5 MB | Manual verification |
| Kid Mode readability | Grade 4-5 | Flesch-Kincaid |
| WCAG AA compliance | 100% critical paths | axe-core audit |
| Colorblind verification | Pass simulations | Chrome DevTools |
| Test coverage (BE) | > 80% | pytest-cov |
| Test coverage (FE) | > 60% | Jest coverage |

---

## Epic Breakdown

### EPIC C: Parsing & I/O

**Owner:** Backend Lead + Frontend Eng
**Duration:** Weeks 8-10 (Sprints 5-6)
**Total Effort:** 60 story points
**Priority:** P0 (Critical Path)

**Epic Overview:**
Enable users to paste external crochet patterns (limited syntax) and export generated patterns in professional formats. Parser converts bracket/repeat syntax to PatternDSL. Export service generates printable PDFs, editable SVGs, and machine-readable JSON.

**Epic Goals:**
- Parse canonical patterns: `R3: [2 sc, inc] x6 (18)`
- Export PDFs < 5 MB with professional layout
- Export SVGs editable in Illustrator/Inkscape
- Export JSON round-trip compatible
- User-friendly error messages for parse failures

#### Stories

| ID | Title | Effort | Priority | Dependencies | Owner |
|----|-------|--------|----------|--------------|-------|
| **C1** | Text parser (backend) | 13 pt | P0 | Phase 1 (DSL) | BE Lead |
| **C2** | Parser error handling | 5 pt | P0 | C1 | BE Lead |
| **C3** | PDF export endpoint (backend) | 13 pt | P0 | Phase 2 (vis frames) | BE Eng |
| **C4** | SVG/PNG export endpoint (backend) | 8 pt | P1 | Phase 2 (vis frames) | BE Eng |
| **C5** | JSON DSL export | 3 pt | P0 | Phase 1 (DSL) | BE Eng |
| **C6** | Export screen UI (frontend) | 8 pt | P0 | C3, C4, C5 | FE Eng |
| **C7** | Parse screen UI (frontend) | 8 pt | P1 | C1, C2 | FE Eng |

**Total:** 58 story points

---

### EPIC E: Kid Mode & Accessibility

**Owner:** Frontend Lead + QA
**Duration:** Weeks 9-11 (Sprints 6-7)
**Total Effort:** 55 story points
**Priority:** P0 (Launch Blocker)

**Epic Overview:**
Implement WCAG AA compliance and Kid Mode for accessibility-first design. Includes screen reader support, keyboard navigation, colorblind palettes, dyslexia font, and simplified UI for young learners.

**Epic Goals:**
- WCAG AA: 0 critical issues in axe-core audit
- Screen reader announces round changes, stitch types
- Colorblind-friendly palettes pass simulations
- Kid Mode UI with 56×56 dp tap targets
- Grade 4-5 reading level copy in Kid Mode

#### Stories

| ID | Title | Effort | Priority | Dependencies | Owner |
|----|-------|--------|----------|--------------|-------|
| **E1** | Kid Mode toggle and theme | 8 pt | P0 | D4 (settings) | FE Lead |
| **E2** | Simplified UI components | 8 pt | P0 | E1 | FE Eng |
| **E3** | Beginner copy and animations | 5 pt | P1 | E2 | FE Eng |
| **E4** | Screen reader labels (ARIA) | 8 pt | P0 | Phase 2 (screens) | FE Lead |
| **E5** | Keyboard navigation | 8 pt | P0 | Phase 2 (screens) | FE Eng |
| **E6** | Colorblind palettes | 5 pt | P0 | E1 (theme) | FE Eng |
| **E7** | Dyslexia font option | 3 pt | P1 | D4 (settings) | FE Eng |

**Total:** 45 story points

---

### EPIC F: Telemetry & Monitoring

**Owner:** Backend Eng + Frontend Eng
**Duration:** Weeks 10-11 (Sprint 7)
**Total Effort:** 20 story points
**Priority:** P1 (Post-Launch Data)

**Epic Overview:**
Implement privacy-respecting telemetry for data-driven improvements. Backend event pipeline logs anonymous usage data (generation, visualization, export). Frontend consent UI and opt-in/opt-out controls.

**Epic Goals:**
- Opt-in consent prompt on first run
- Event tracking: generation, visualization, export
- Backend logging with no PII
- Settings toggle for opt-in/opt-out
- 90-day data retention policy

#### Stories

| ID | Title | Effort | Priority | Dependencies | Owner |
|----|-------|--------|----------|--------------|-------|
| **F1** | Backend event pipeline | 8 pt | P1 | Phase 1 (API) | BE Eng |
| **F2** | Frontend telemetry client | 5 pt | P1 | F1 | FE Eng |
| **F3** | Consent prompt UI | 3 pt | P1 | F2 | FE Eng |
| **F4** | Settings telemetry toggle | 2 pt | P1 | D4 (settings), F2 | FE Eng |
| **F5** | Backend logging infra | 2 pt | P1 | F1 | BE Eng |

**Total:** 20 story points

---

### EPIC D: App Shell & Settings (Completion)

**Owner:** Frontend Lead
**Duration:** Weeks 8-10 (Sprints 5-6)
**Total Effort:** 18 story points
**Priority:** P0 (Dependency for E, F)

**Epic Overview:**
Complete settings screen with persistence (AsyncStorage), terminology/units toggles, and theme system. Foundation for Kid Mode, accessibility, and telemetry features.

**Epic Goals:**
- Settings persisted across sessions
- Terminology (US/UK) and units (cm/in) toggles functional
- Theme system supports Kid Mode and accessibility variants
- All preferences applied consistently

#### Stories (Remaining)

| ID | Title | Effort | Priority | Dependencies | Owner |
|----|-------|--------|----------|--------------|-------|
| **D7** | Settings persistence (AsyncStorage) | 8 pt | P0 | D4 (Phase 2) | FE Lead |
| **D8** | Terminology/units toggles | 5 pt | P0 | D7 | FE Eng |
| **D9** | Theme system refactor | 5 pt | P0 | D7 | FE Eng |

**Total:** 18 story points

---

## Sprint Plans

### Sprint 5 (Weeks 8-9)

**Sprint Goal:** Parser functional + PDF export + Settings persistence

**Total Capacity:** 65-75 story points
**Team Focus:**
- Backend: Text parser + PDF export
- Frontend: Export screen + settings persistence

**Stories Planned:**

| Story | Title | Effort | Owner | Status |
|-------|-------|--------|-------|--------|
| C1 | Text parser (backend) | 13 pt | BE Lead | Planned |
| C2 | Parser error handling | 5 pt | BE Lead | Planned |
| C3 | PDF export endpoint | 13 pt | BE Eng | Planned |
| C5 | JSON DSL export | 3 pt | BE Eng | Planned |
| C6 | Export screen UI | 8 pt | FE Eng | Planned |
| D7 | Settings persistence | 8 pt | FE Lead | Planned |
| D8 | Terminology/units toggles | 5 pt | FE Eng | Planned |
| D9 | Theme system refactor | 5 pt | FE Eng | Planned |

**Total Committed:** 60 story points

**Daily Breakdown:**

**Week 8:**
- **Day 1-2:** C1 start (BE Lead), C3 start (BE Eng), D7 start (FE Lead), D8 start (FE Eng)
- **Day 3-4:** C1 core parsing complete, C3 PDF template, D7 AsyncStorage integration, D9 start (FE Eng)
- **Day 5:** C2 error handling (BE Lead), C3 PDF generation, D7 complete, D8 complete

**Week 9:**
- **Day 1-2:** C1 complete + tests, C3 complete + tests, C5 (BE Eng), D9 complete
- **Day 3-4:** C6 export screen (FE Eng), integration testing (BE → FE)
- **Day 5:** C6 complete, sprint review prep

**Sprint Demo:**
- Backend: Live parse demo: `R3: [2 sc, inc] x6` → PatternDSL JSON
- Backend: Generate sphere → PDF export with diagrams
- Frontend: Export screen with PDF/SVG/JSON download
- Frontend: Settings screen with terminology toggle (US ↔ UK live update)
- Frontend: Settings persisted across app restart

**Definition of Done (Sprint 5):**
- [ ] Parser handles canonical bracket/repeat patterns
- [ ] PDF exports with cover, materials, pattern, diagrams
- [ ] Export screen functional with format selection
- [ ] Settings persist across sessions (AsyncStorage)
- [ ] Unit tests pass (BE: 80%+, FE: 60%+)
- [ ] Code reviewed and merged to main

---

### Sprint 6 (Week 10)

**Sprint Goal:** Kid Mode + Accessibility baseline + SVG export

**Total Capacity:** 65-75 story points
**Team Focus:**
- Frontend: Kid Mode UI + accessibility features
- Backend: SVG export + telemetry foundation
- QA: Accessibility audit start

**Stories Planned:**

| Story | Title | Effort | Owner | Status |
|-------|-------|--------|-------|--------|
| C4 | SVG/PNG export endpoint | 8 pt | BE Eng | Planned |
| C7 | Parse screen UI | 8 pt | FE Eng | Planned |
| E1 | Kid Mode toggle and theme | 8 pt | FE Lead | Planned |
| E2 | Simplified UI components | 8 pt | FE Eng | Planned |
| E3 | Beginner copy and animations | 5 pt | FE Eng | Planned |
| E4 | Screen reader labels (ARIA) | 8 pt | FE Lead | Planned |
| E6 | Colorblind palettes | 5 pt | FE Eng | Planned |
| F1 | Backend event pipeline | 8 pt | BE Eng | Planned |

**Total Committed:** 58 story points

**Daily Breakdown:**

**Week 10:**
- **Day 1-2:** C4 (BE Eng), E1 start (FE Lead), E2 start (FE Eng), E4 start (FE Lead), F1 start (BE Eng)
- **Day 3:** C4 complete, C7 start (FE Eng), E1 theme complete, E2 components halfway
- **Day 4:** E1 complete, E2 complete, E3 start (FE Eng), E6 start (FE Eng), F1 pipeline functional
- **Day 5:** C7 complete, E3 animations, E4 ARIA labels, E6 palettes, F1 complete

**Sprint Demo:**
- Backend: SVG export per-round and composite
- Frontend: Kid Mode toggle (simplified UI, larger buttons, friendly copy)
- Frontend: Parse screen with error validation
- Frontend: Colorblind palette toggle (green/red → patterns/symbols)
- Frontend: Screen reader demo (round navigation announcements)
- Backend: Telemetry events logged (generation, export)

**Definition of Done (Sprint 6):**
- [ ] SVG export functional (per-round, composite)
- [ ] Kid Mode toggle activates simplified UI
- [ ] Beginner animations present (increase, decrease)
- [ ] ARIA labels on all interactive elements
- [ ] Colorblind palettes functional
- [ ] Telemetry backend pipeline operational
- [ ] axe-core audit shows < 5 issues
- [ ] Unit tests pass (BE: 80%+, FE: 60%+)

---

### Sprint 7 (Week 11)

**Sprint Goal:** Accessibility completion + Telemetry frontend + QA hardening

**Total Capacity:** 50-60 story points
**Team Focus:**
- Frontend: Keyboard nav + telemetry client + dyslexia font
- QA: Full accessibility audit + remediation
- Backend: Telemetry logging infrastructure

**Stories Planned:**

| Story | Title | Effort | Owner | Status |
|-------|-------|--------|-------|--------|
| E5 | Keyboard navigation | 8 pt | FE Eng | Planned |
| E7 | Dyslexia font option | 3 pt | FE Eng | Planned |
| F2 | Frontend telemetry client | 5 pt | FE Eng | Planned |
| F3 | Consent prompt UI | 3 pt | FE Eng | Planned |
| F4 | Settings telemetry toggle | 2 pt | FE Eng | Planned |
| F5 | Backend logging infra | 2 pt | BE Eng | Planned |

**Total Committed:** 23 story points

**Additional QA Work:**
- Full axe-core audit (all screens)
- Screen reader testing (NVDA, JAWS, VoiceOver)
- Keyboard navigation testing (external keyboard)
- Colorblind simulation verification
- Manual accessibility remediation (10-15 pt equivalent)

**Daily Breakdown:**

**Week 11:**
- **Day 1-2:** E5 keyboard nav (FE Eng), F2 telemetry client (FE Eng), F5 logging (BE Eng)
- **Day 3:** E5 complete, E7 dyslexia font (FE Eng), F2 complete, F3 consent UI
- **Day 4:** E7 complete, F3 complete, F4 settings toggle, axe-core audit (QA)
- **Day 5:** F4 complete, F5 complete, accessibility remediation, integration testing

**Sprint Demo:**
- Frontend: Full keyboard navigation (tab order, no traps)
- Frontend: Dyslexia font toggle (OpenDyslexic)
- Frontend: Telemetry consent prompt on first run
- Frontend: Settings telemetry toggle (opt-in/opt-out)
- QA: Accessibility audit report (WCAG AA compliance)
- Backend: Telemetry logging with 90-day retention

**Definition of Done (Sprint 7):**
- [ ] Keyboard navigation complete (all features accessible)
- [ ] Dyslexia font option functional
- [ ] Telemetry consent prompt on first run
- [ ] Telemetry opt-out in settings
- [ ] Backend telemetry logging operational
- [ ] axe-core audit: 0 critical issues
- [ ] Screen reader testing passed
- [ ] Colorblind verification passed
- [ ] Unit tests pass (BE: 80%+, FE: 60%+)

---

## Technical Implementation

### Backend: Text Pattern Parser

**Algorithm: Text → PatternDSL**

```python
# app/services/parser_service.py
import re
from typing import List, Optional
from knit_wit_engine.dsl import PatternDSL, RoundDSL, OpDSL, MetaDSL, ObjectDSL
from pydantic import ValidationError

class PatternParserService:
    """Parse limited crochet pattern syntax to PatternDSL."""

    # Supported tokens
    ROUND_PATTERN = r"R(\d+):\s*(.+)\s*\((\d+)\)"
    OP_PATTERN = r"(\w+)(?:\s+x(\d+))?"
    BRACKET_PATTERN = r"\[([^\]]+)\]\s*x(\d+)"

    def parse(self, text: str) -> PatternDSL:
        """Parse pattern text to DSL."""
        lines = text.strip().split("\n")
        rounds = []

        for line in lines:
            round_match = re.match(self.ROUND_PATTERN, line)
            if not round_match:
                continue  # Skip non-round lines

            round_num = int(round_match.group(1))
            ops_text = round_match.group(2).strip()
            expected_stitches = int(round_match.group(3))

            # Parse operations
            ops = self._parse_operations(ops_text)

            # Create RoundDSL
            round_dsl = RoundDSL(
                r=round_num,
                ops=ops,
                stitches=expected_stitches
            )
            rounds.append(round_dsl)

        # Build PatternDSL
        return PatternDSL(
            meta=MetaDSL(
                version="0.1",
                units="cm",
                terms="US",
                stitch="sc",
                round_mode="spiral",
                gauge={"sts_per_10cm": 14, "rows_per_10cm": 16}
            ),
            object=ObjectDSL(type="unknown", params={}),
            rounds=rounds,
            materials={},
            notes=[]
        )

    def _parse_operations(self, ops_text: str) -> List[OpDSL]:
        """Parse operations from round text."""
        ops = []

        # Handle brackets first: [2 sc, inc] x6
        bracket_matches = list(re.finditer(self.BRACKET_PATTERN, ops_text))
        for match in bracket_matches:
            inner_ops = match.group(1).strip()
            repeat = int(match.group(2))

            # Parse inner operations
            inner_op_list = self._parse_simple_ops(inner_ops)

            # Create sequence operation
            ops.append(OpDSL(
                op="seq",
                ops=inner_op_list,
                repeat=repeat,
                count=sum(op.count for op in inner_op_list) * repeat
            ))

            # Remove from text
            ops_text = ops_text.replace(match.group(0), "")

        # Parse remaining simple operations
        simple_ops = self._parse_simple_ops(ops_text)
        ops.extend(simple_ops)

        return ops

    def _parse_simple_ops(self, text: str) -> List[OpDSL]:
        """Parse simple operations (no brackets)."""
        ops = []
        tokens = text.split(",")

        for token in tokens:
            token = token.strip()
            if not token:
                continue

            # Match: "inc x6" or "sc" or "MR 6 sc"
            if "x" in token:
                parts = token.split("x")
                stitch = parts[0].strip()
                count = int(parts[1].strip())
                ops.append(OpDSL(op=stitch, count=count))
            elif token.upper() == "MR":
                ops.append(OpDSL(op="MR", count=1))
            else:
                # Simple stitch with optional count
                match = re.match(r"(\d+)?\s*(\w+)", token)
                if match:
                    count = int(match.group(1)) if match.group(1) else 1
                    stitch = match.group(2)
                    ops.append(OpDSL(op=stitch, count=count))

        return ops

    def validate_parse(self, dsl: PatternDSL) -> dict:
        """Validate parsed DSL."""
        errors = []

        # Check stitch count consistency
        for round_dsl in dsl.rounds:
            computed = sum(op.count for op in round_dsl.ops)
            if computed != round_dsl.stitches:
                errors.append(f"R{round_dsl.r}: Expected {round_dsl.stitches}, got {computed}")

        return {"valid": len(errors) == 0, "errors": errors}
```

**API Endpoint:**

```python
# app/api/routes/parser.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.parser_service import PatternParserService

router = APIRouter(prefix="/api/v1/parser", tags=["parser"])
parser_service = PatternParserService()

class ParseRequest(BaseModel):
    text: str

class ParseResponse(BaseModel):
    dsl: dict
    validation: dict

@router.post("/parse", response_model=ParseResponse)
async def parse_pattern(request: ParseRequest):
    """
    Parse crochet pattern text to PatternDSL.

    **Supported syntax:**
    - R1: MR 6 sc (6)
    - R2: inc x6 (12)
    - R3: [2 sc, inc] x6 (18)
    """
    try:
        dsl = parser_service.parse(request.text)
        validation = parser_service.validate_parse(dsl)

        return ParseResponse(
            dsl=dsl.model_dump(),
            validation=validation
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Parse error: {str(e)}"
        )
```

---

### Backend: PDF Export

**PDF Generation with ReportLab:**

```python
# app/services/export_service.py
from reportlab.lib.pagesizes import A4, letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO
from knit_wit_engine.dsl import PatternDSL

class ExportService:
    """Generate exports in multiple formats."""

    def generate_pdf(self, dsl: PatternDSL, paper_size: str = "A4") -> bytes:
        """Generate PDF export."""
        buffer = BytesIO()
        page_size = A4 if paper_size == "A4" else letter

        doc = SimpleDocTemplate(
            buffer,
            pagesize=page_size,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )

        # Build PDF content
        styles = getSampleStyleSheet()
        story = []

        # Cover page
        story.append(Paragraph("Knit-Wit Pattern", styles['Title']))
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph(f"Shape: {dsl.object.type.title()}", styles['Normal']))
        story.append(Paragraph(f"Dimensions: {dsl.object.params}", styles['Normal']))
        story.append(Spacer(1, 0.5*inch))

        # Materials section
        story.append(Paragraph("Materials", styles['Heading1']))
        story.append(Spacer(1, 0.1*inch))

        materials_data = [
            ["Yarn Weight:", dsl.materials.get("yarn_weight", "Worsted")],
            ["Hook Size:", f"{dsl.materials.get('hook_size_mm', 4.0)} mm"],
            ["Yardage:", f"{dsl.materials.get('yardage_estimate', 0)} yards"],
            ["Gauge:", f"{dsl.meta.gauge['sts_per_10cm']} sts / {dsl.meta.gauge['rows_per_10cm']} rows per 10cm"]
        ]

        materials_table = Table(materials_data, colWidths=[2*inch, 3*inch])
        materials_table.setStyle([
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ])
        story.append(materials_table)
        story.append(Spacer(1, 0.5*inch))

        # Pattern section
        story.append(Paragraph("Pattern Instructions", styles['Heading1']))
        story.append(Spacer(1, 0.1*inch))

        for round_dsl in dsl.rounds:
            round_text = self._format_round(round_dsl, dsl.meta.terms)
            story.append(Paragraph(round_text, styles['Normal']))
            story.append(Spacer(1, 0.05*inch))

        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

    def _format_round(self, round_dsl, terms: str) -> str:
        """Format round as human-readable text."""
        ops_text = ", ".join([
            f"{op.op} x{op.count}" if op.count > 1 else op.op
            for op in round_dsl.ops
        ])
        return f"<b>R{round_dsl.r}:</b> {ops_text} ({round_dsl.stitches})"

    def generate_svg(self, frames: List[dict]) -> str:
        """Generate SVG export (per-round or composite)."""
        # Implementation similar to visualization rendering
        # Export SVG as string
        pass

    def generate_json(self, dsl: PatternDSL) -> str:
        """Generate JSON DSL export."""
        return dsl.model_dump_json(indent=2)
```

**API Endpoint:**

```python
# app/api/routes/export.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from app.services.export_service import ExportService
from knit_wit_engine.dsl import PatternDSL

router = APIRouter(prefix="/api/v1/export", tags=["export"])
export_service = ExportService()

@router.post("/pdf")
async def export_pdf(dsl: PatternDSL, paper_size: str = "A4"):
    """Export pattern to PDF."""
    try:
        pdf_bytes = export_service.generate_pdf(dsl, paper_size)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=pattern.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF export error: {str(e)}")

@router.post("/json")
async def export_json(dsl: PatternDSL):
    """Export pattern DSL as JSON."""
    json_str = export_service.generate_json(dsl)
    return Response(
        content=json_str,
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=pattern.json"}
    )
```

---

### Frontend: Kid Mode Theme

**Theme System:**

```typescript
// src/theme/kidModeTheme.ts
import { Theme } from './types';

export const kidModeTheme: Theme = {
  colors: {
    primary: '#FF6B9D',      // Bright pink
    secondary: '#FFC837',    // Sunny yellow
    background: '#FFF8E1',   // Warm cream
    surface: '#FFFFFF',
    text: {
      primary: '#2D3748',    // High contrast dark gray
      secondary: '#4A5568',
      hint: '#718096',
    },
    success: '#4CAF50',      // Green (keep)
    error: '#F44336',        // Red (keep)
    warning: '#FF9800',      // Orange
    info: '#2196F3',         // Blue
  },
  typography: {
    fontFamily: {
      regular: 'Comic Sans MS, sans-serif',  // Friendly, rounded
      heading: 'Comic Sans MS, bold',
    },
    fontSize: {
      small: 16,      // Increased from 12
      medium: 20,     // Increased from 14
      large: 24,      // Increased from 16
      xlarge: 32,     // Increased from 20
    },
    lineHeight: 1.6,  // Increased spacing
  },
  spacing: {
    xs: 8,
    sm: 16,
    md: 24,
    lg: 32,
    xl: 48,
  },
  touchTargets: {
    minimum: 56,  // Increased from 48
    recommended: 64,
  },
};
```

**Kid Mode Components:**

```typescript
// src/components/kidmode/SimplifiedUI.tsx
import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { useTheme } from '../../theme/ThemeProvider';

interface SimplifiedButtonProps {
  onPress: () => void;
  label: string;
  icon?: string;
}

export const SimplifiedButton: React.FC<SimplifiedButtonProps> = ({
  onPress,
  label,
  icon
}) => {
  const theme = useTheme();

  return (
    <TouchableOpacity
      onPress={onPress}
      style={[
        styles.button,
        {
          backgroundColor: theme.colors.primary,
          minWidth: theme.touchTargets.recommended,
          minHeight: theme.touchTargets.recommended,
        }
      ]}
      accessibilityLabel={label}
      accessibilityRole="button"
    >
      {icon && <Text style={styles.icon}>{icon}</Text>}
      <Text style={[styles.label, { fontSize: theme.typography.fontSize.large }]}>
        {label}
      </Text>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  button: {
    borderRadius: 16,
    paddingHorizontal: 24,
    paddingVertical: 16,
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.15,
    shadowRadius: 4,
    elevation: 3,
  },
  icon: {
    fontSize: 32,
    marginBottom: 8,
  },
  label: {
    color: '#FFFFFF',
    fontWeight: 'bold',
    textAlign: 'center',
  },
});
```

---

### Frontend: Accessibility Features

**Screen Reader Labels:**

```typescript
// src/components/visualization/SVGRenderer.tsx (updated)
import React from 'react';
import { Svg, Circle, Line, G } from 'react-native-svg';
import { AccessibilityInfo, View } from 'react-native';

export const SVGRenderer: React.FC<SVGRendererProps> = ({
  frame,
  width,
  height,
  onStitchTap
}) => {
  // Accessibility description
  const accessibilityLabel = `Round ${frame.round_number}, ${frame.stitch_count} stitches. ${frame.highlights.length} increases or decreases.`;

  return (
    <View
      accessible={true}
      accessibilityLabel={accessibilityLabel}
      accessibilityRole="image"
      accessibilityHint="Double tap a stitch to hear its details"
    >
      <Svg width={width} height={height}>
        {/* SVG content */}
        {frame.nodes.map((node) => (
          <Circle
            key={node.id}
            cx={node.position[0]}
            cy={node.position[1]}
            r={8}
            fill={getStitchColor(node.highlight)}
            onPress={() => {
              onStitchTap(node.id);
              AccessibilityInfo.announceForAccessibility(
                `${node.stitch_type}, ${node.highlight}`
              );
            }}
            accessible={true}
            accessibilityLabel={`Stitch ${node.stitch_type}, ${node.highlight}`}
          />
        ))}
      </Svg>
    </View>
  );
};
```

**Keyboard Navigation:**

```typescript
// src/components/visualization/RoundScrubber.tsx (updated)
import React, { useEffect } from 'react';
import { View, TouchableOpacity } from 'react-native';

export const RoundScrubber: React.FC = () => {
  const { currentRound, totalRounds, prevRound, nextRound } = useVisualizationStore();

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyPress = (event: KeyboardEvent) => {
      switch (event.key) {
        case 'ArrowLeft':
          prevRound();
          break;
        case 'ArrowRight':
          nextRound();
          break;
      }
    };

    // Web only - keyboard events
    if (Platform.OS === 'web') {
      window.addEventListener('keydown', handleKeyPress);
      return () => window.removeEventListener('keydown', handleKeyPress);
    }
  }, [prevRound, nextRound]);

  return (
    <View style={styles.container}>
      <TouchableOpacity
        onPress={prevRound}
        disabled={currentRound === 1}
        accessibilityLabel="Previous round"
        accessibilityRole="button"
        accessible={true}
        onFocus={() => setFocused(true)}
        onBlur={() => setFocused(false)}
        style={[styles.button, focused && styles.focused]}
      >
        {/* Button content */}
      </TouchableOpacity>

      {/* Additional controls */}
    </View>
  );
};
```

**Colorblind Palettes:**

```typescript
// src/theme/accessibilityTheme.ts
export const colorblindPalettes = {
  protanopia: {
    increase: '#0072B2',   // Blue (distinguishable)
    decrease: '#D55E00',   // Orange (distinguishable)
    normal: '#999999',     // Gray
  },
  deuteranopia: {
    increase: '#0072B2',   // Blue
    decrease: '#D55E00',   // Orange
    normal: '#999999',
  },
  tritanopia: {
    increase: '#E69F00',   // Orange
    decrease: '#56B4E9',   // Sky blue
    normal: '#999999',
  },
  highContrast: {
    increase: '#00FF00',   // Bright green
    decrease: '#FF0000',   // Bright red
    normal: '#FFFFFF',     // White
  },
};

// Apply patterns for additional distinction
export const stitchPatterns = {
  increase: 'url(#diagonal-stripes)',
  decrease: 'url(#hash-pattern)',
  normal: 'none',
};
```

---

### Frontend: Telemetry Client

**Event Tracking:**

```typescript
// src/services/telemetryClient.ts
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';

interface TelemetryEvent {
  event: string;
  properties?: Record<string, any>;
  timestamp: string;
}

class TelemetryClient {
  private enabled: boolean = false;
  private apiUrl: string;

  constructor(apiUrl: string) {
    this.apiUrl = apiUrl;
    this.loadConsent();
  }

  async loadConsent() {
    const consent = await AsyncStorage.getItem('telemetry_consent');
    this.enabled = consent === 'true';
  }

  async setConsent(enabled: boolean) {
    this.enabled = enabled;
    await AsyncStorage.setItem('telemetry_consent', enabled.toString());
  }

  track(event: string, properties?: Record<string, any>) {
    if (!this.enabled) return;

    const telemetryEvent: TelemetryEvent = {
      event,
      properties: {
        ...properties,
        platform: Platform.OS,
        version: Constants.expoConfig?.version,
      },
      timestamp: new Date().toISOString(),
    };

    // Send to backend
    this.sendEvent(telemetryEvent);
  }

  private async sendEvent(event: TelemetryEvent) {
    try {
      await axios.post(`${this.apiUrl}/telemetry/events`, event);
    } catch (error) {
      // Silent fail - don't block user experience
      console.warn('Telemetry error:', error);
    }
  }

  // Convenience methods
  trackGeneration(shape: string, stitch: string) {
    this.track('pattern_generated', { shape, stitch });
  }

  trackVisualization(roundCount: number, duration: number) {
    this.track('pattern_visualized', { round_count: roundCount, duration_ms: duration });
  }

  trackExport(format: string) {
    this.track('pattern_exported', { format });
  }
}

export const telemetryClient = new TelemetryClient(API_BASE_URL);
```

**Consent Prompt:**

```typescript
// src/components/telemetry/ConsentPrompt.tsx
import React, { useState, useEffect } from 'react';
import { View, Text, Modal, TouchableOpacity, StyleSheet } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { telemetryClient } from '../../services/telemetryClient';

export const ConsentPrompt: React.FC = () => {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    checkConsent();
  }, []);

  const checkConsent = async () => {
    const consent = await AsyncStorage.getItem('telemetry_consent');
    if (consent === null) {
      setVisible(true);
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

  return (
    <Modal
      visible={visible}
      transparent
      animationType="fade"
      onRequestClose={handleDecline}
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
            >
              <Text style={styles.declineText}>No Thanks</Text>
            </TouchableOpacity>

            <TouchableOpacity
              onPress={handleAccept}
              style={[styles.button, styles.acceptButton]}
              accessibilityLabel="Accept telemetry"
            >
              <Text style={styles.acceptText}>Accept</Text>
            </TouchableOpacity>
          </View>
        </View>
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  modal: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 24,
    maxWidth: 400,
    width: '100%',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 16,
    color: '#111827',
  },
  body: {
    fontSize: 14,
    color: '#4B5563',
    marginBottom: 12,
    lineHeight: 20,
  },
  buttons: {
    flexDirection: 'row',
    marginTop: 24,
    gap: 12,
  },
  button: {
    flex: 1,
    paddingVertical: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  declineButton: {
    backgroundColor: '#F3F4F6',
  },
  acceptButton: {
    backgroundColor: '#3B82F6',
  },
  declineText: {
    color: '#6B7280',
    fontWeight: '600',
  },
  acceptText: {
    color: '#FFFFFF',
    fontWeight: '600',
  },
});
```

---

## Success Criteria

### Phase Exit Criteria

**Backend:**
- [ ] Parser handles canonical patterns (90%+ accuracy)
- [ ] PDF export generates < 5 MB files with professional layout
- [ ] SVG export produces valid, editable files
- [ ] JSON export round-trip compatible with DSL
- [ ] Telemetry pipeline logs events (no PII)
- [ ] Unit test coverage > 80%
- [ ] Integration tests pass (parser, export APIs)

**Frontend:**
- [ ] Export screen functional (PDF/SVG/JSON downloads)
- [ ] Parse screen validates input with clear errors
- [ ] Kid Mode toggle activates simplified UI
- [ ] Beginner animations present (increase, decrease)
- [ ] Settings persist across sessions (AsyncStorage)
- [ ] Terminology/units toggles functional
- [ ] Component test coverage > 60%

**Accessibility:**
- [ ] axe-core audit: 0 critical issues
- [ ] WCAG AA compliance verified (color contrast 4.5:1+, 3:1+ UI)
- [ ] ARIA labels on 100% interactive elements
- [ ] Keyboard navigation functional (tab order, no traps)
- [ ] Screen reader testing passed (NVDA, JAWS, VoiceOver)
- [ ] Focus indicators visible (2px, 3:1 contrast)
- [ ] Colorblind palettes verified (simulations pass)
- [ ] Dyslexia font option functional

**Telemetry:**
- [ ] Consent prompt on first run
- [ ] Opt-in/opt-out toggle in settings
- [ ] Events tracked: generation, visualization, export
- [ ] Backend logging with 90-day retention
- [ ] Privacy policy updated

**Integration:**
- [ ] End-to-end flow: generate → visualize → export
- [ ] Parse → visualize flow functional
- [ ] Settings changes applied consistently
- [ ] Error handling graceful (network, validation)

---

## Dependencies & Risks

### Dependencies from Phase 2

**Met Dependencies:**
- ✅ RN/Expo app shell operational (Phase 2)
- ✅ Navigation stack functional (Phase 2)
- ✅ SVG rendering engine (Phase 2)
- ✅ Zustand state management (Phase 2)
- ✅ HTTP client configured (Phase 2)
- ✅ Visualization frames API (Phase 2)

**Required for Phase 3:**
- PatternDSL schema (Phase 1)
- Settings screen foundation (Phase 2, D4)
- Theme system basics (Phase 2, D5)

### External Dependencies

**Backend:**
- reportlab or weasyprint (PDF generation)
- pyparsing (text parser)
- Pillow (PNG export)

**Installation:**
```bash
pnpm --filter api add reportlab pyparsing Pillow
```

**Frontend:**
- @react-native-async-storage/async-storage (settings persistence)
- react-native-fs (file downloads)
- @expo/vector-icons (icons)

**Installation:**
```bash
pnpm --filter mobile add @react-native-async-storage/async-storage react-native-fs @expo/vector-icons
```

### Risks & Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Parser complexity exceeds scope** | Medium | High | Limit to bracket/repeat syntax; clear error messages for unsupported |
| **PDF generation slow (>5s)** | Medium | Medium | Optimize template; cache diagrams; consider async generation |
| **Accessibility audit fails** | Low | High | Early QA involvement; continuous axe-core checks; manual testing |
| **Kid Mode readability unclear** | Medium | Low | User testing with target age group; readability tool validation |
| **Telemetry consent friction** | Low | Low | Clear, non-dark-pattern UI; easy opt-out; privacy policy transparency |
| **Settings persistence bugs** | Medium | Medium | Comprehensive AsyncStorage testing; migration strategy for schema changes |
| **Colorblind palette insufficient** | Low | Medium | Combine color + patterns/symbols; verify with simulation tools |
| **Screen reader incompatibility** | Medium | High | Test on NVDA, JAWS, VoiceOver; early remediation; expert consultation |

**Critical Path Items:**
1. Parser accuracy (blocks external pattern workflows)
2. PDF export quality (blocks sharing/printing)
3. Accessibility compliance (blocks launch)
4. Settings persistence (blocks user preferences)

**Mitigation Actions:**
- Daily standups to surface blockers early
- QA embedded in sprint (not end-of-phase)
- Accessibility expert consultation (if audit fails)
- Parser scope reduction if complexity escalates

---

## Next Phase Preview

**Phase 4: QA & Polish (Weeks 12-15, Sprints 8-10)**

**Focus Areas:**
- Cross-device testing (iOS 14+, Android 9+, tablets)
- Performance optimization (60 FPS, < 200ms generation)
- Bug fixes and edge case handling
- User acceptance testing (UAT)
- Documentation finalization (API docs, user guides)
- Regression testing
- Launch readiness review

**Key Deliverables:**
- Comprehensive test suite (unit, integration, E2E)
- Performance benchmarks met
- Accessibility audit remediation complete
- Bug backlog triaged and resolved
- User documentation complete
- Deployment runbook
- Monitoring and alerting configured

**Success Criteria:**
- 0 P0/P1 bugs in backlog
- Performance targets met (all)
- WCAG AA audit passed (all screens)
- Cross-device testing complete (iOS/Android/tablets)
- Documentation reviewed and approved

**Transition Criteria from Phase 3:**
- All Phase 3 exit criteria met
- Integration testing complete
- Manual exploratory testing passed
- Known issues documented and triaged
