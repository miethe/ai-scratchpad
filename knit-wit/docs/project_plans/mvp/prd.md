# Knit-Wit MVP — Product Requirements Document

**Document Version:** 1.0
**Last Updated:** November 2024
**Status:** Active Development
**Owner:** Product & Development Team

---

## 1. Executive Summary

Knit-Wit is a mobile-first web application designed to make crochet pattern creation and learning accessible to hobbyists of all skill levels. The MVP focuses on two core capabilities: (1) generating clean, parametric crochet patterns for geometric shapes, and (2) providing interactive, step-by-step pattern visualization with beginner-friendly guidance.

The application solves a significant pain point in the crochet community: the tedium of manually writing and interpreting complex patterns, particularly for geometric objects like amigurumi. By automating pattern generation based on user-provided parameters (dimensions, gauge, stitch type) and offering interactive visual guides, Knit-Wit democratizes pattern design and makes crochet more approachable for beginners while delivering value to experienced crafters.

**Target Launch:** MVP completion before end of Q1 2025

**Success Criteria:**
- Generate geometrically accurate sphere/cylinder/cone patterns < 200ms
- Visualize patterns smoothly on mid-range mobile devices
- Achieve WCAG AA accessibility compliance
- Support 100+ concurrent users

---

## 2. Product Overview and Vision

### 2.1 Core Product Definition

Knit-Wit is a parametric crochet pattern generator and interactive visualizer built as a mobile-first web application. Users input geometric parameters (dimensions, yarn weight, gauge) and receive ready-to-use patterns with step-by-step visual guidance.

### 2.2 Vision Statement

To make advanced crochet design tools accessible to everyone—from children learning their first stitches to expert amigurumi artists—by combining intelligent algorithms with intuitive, mobile-friendly interfaces.

### 2.3 Key Product Features (MVP)

1. **Parametric Pattern Generation**
   - User-friendly form to input shape parameters
   - Real-time gauge calculation and yarn requirement estimation
   - Outputs include pattern text, visual diagrams, and structured DSL

2. **Interactive Pattern Visualization**
   - Step-by-step round navigation
   - Color-coded stitch highlighting (increases/decreases)
   - Contextual tooltips and beginner explanations
   - Real-time term translation (US ↔ UK)

3. **Multi-Format Export**
   - Printable PDF with pattern, materials list, and diagrams
   - SVG/PNG for digital sharing
   - JSON DSL for programmatic reuse

4. **Accessibility First**
   - Kid Mode with simplified language and larger controls
   - Colorblind-friendly palettes
   - Full keyboard navigation
   - Screen reader support

5. **Mobile-Optimized Experience**
   - Touch-friendly interface with large tap targets
   - Works smoothly on mid-range smartphones
   - Responsive design for tablets

---

## 3. Problem Statement and Market Opportunity

### 3.1 The Problem

**Writing and interpreting crochet patterns is difficult:**

- **For Beginners:** Abbreviations (sc, hdc, dc, inc, dec) are cryptic. Reading patterns like `[2 sc, inc] x6` requires translation and visualization in one's head—often leading to mistakes and frustration.
- **For Experts:** Creating custom patterns for precise geometric shapes (amigurumi bodies, limbs with specific tapers) requires manual calculation and iterative testing, consuming significant time.
- **For Educators:** Teaching crochet lacks scalable, interactive visual tools. Students benefit from animations and dynamic explanations rather than static text.

**Pattern variance and accessibility gaps:**

- Different yarn weights and hooks require gauge adjustments—calculations that are error-prone
- Pattern terminology differs between US and UK conventions, creating confusion
- No standardized way to share patterns programmatically
- Patterns are difficult to adapt or remix

### 3.2 Market Opportunity

**Target Market Size:**
- ~6 million active crocheters in the US alone
- Growing interest in fiber arts, especially among Gen Z and younger millennials
- Teachers, crafting communities, and online content creators

**Addressable Market:**
- Hobbyists seeking design tools (estimated 1-2% of active crocheters = 60K-120K potential users)
- Educational institutions and libraries
- Content creators and pattern publishers

**Competitive Advantages:**
- AI-assisted pattern generation (vs. manual tools like Ravelry)
- Mobile-first design (vs. desktop-heavy competitors)
- Kid-friendly interface (underserved segment)
- Open DSL for integration (future B2B potential)

---

## 4. Target Users and Personas

### 4.1 Persona: Beginner Becky
**Demographics:** Ages 12–60, primarily female, new to crochet
**Skill Level:** Learning basic stitches; reads patterns with difficulty
**Goals:** Create simple amigurumi projects; understand what stitches do
**Pain Points:**
- Intimidated by abbreviations and pattern syntax
- Needs visual confirmation that she's doing stitches correctly
- Wants reassurance and encouragement

**Usage Pattern:** Generates simple shapes (sphere for head); follows visualization step-by-step; uses Kid Mode frequently

**Value Drivers:**
- Clear, animated guidance ("this is what an increase looks like")
- Color-coded visuals with stitch names
- Simplified copy and explanations

---

### 4.2 Persona: Intermediate Ivy
**Demographics:** Ages 25–50, experienced crocheter
**Skill Level:** Comfortable with sc, hdc, dc; understands gauge and tension
**Goals:** Quickly design custom limbs/shapes; standardize her designs
**Pain Points:**
- Tired of manual gauge calculations
- Wants fast, precise patterns for parametric designs
- Needs efficient export for sharing with friends

**Usage Pattern:** Generates tapered limbs and cylinders; tweaks gauge; exports to PDF; occasionally pastes external patterns for reference

**Value Drivers:**
- Fast generation (< 1 sec)
- Accurate gauge handling
- High-quality exports (PDF, SVG)
- Customization options (US/UK terms, units)

---

### 4.3 Persona: Expert Eli
**Demographics:** Ages 30–65, professional or prolific designer
**Skill Level:** Expert; publishes patterns; understands advanced techniques
**Goals:** Create complex, reproducible designs; maintain a design library
**Pain Points:**
- Current tools lack fine control and standardization
- Pattern versioning and modification is cumbersome
- No programmatic access to algorithms

**Usage Pattern:** Uses all advanced features; may extend with custom algorithms; exports for publication; uses DSL for integration with other tools

**Value Drivers:**
- Precise algorithmic control
- JSON DSL for integration
- Reproducible, deterministic output
- Scalability to complex shapes

---

### 4.4 Persona: Parent/Teacher Pat
**Demographics:** Ages 30–70, educator or parent
**Skill Level:** Varied; often less experienced
**Goals:** Teach crochet in a fun, accessible way; engage students
**Pain Points:**
- Needs clear visual aids for teaching
- Students lose interest with dense text patterns
- Safety and age-appropriate content is important

**Usage Pattern:** Uses Kid Mode; generates simple shapes for classroom; shares visual guides with students; looks for explanatory content

**Value Drivers:**
- Kid-friendly interface and copy
- Animated tutorials
- Shareable visual guides
- Classroom-appropriate pacing

---

### 4.5 Accessibility Considerations

**Vision Impairment:**
- Full keyboard navigation support
- ARIA labels on all controls
- Screen reader compatibility for pattern text and diagnostics
- High-contrast mode option

**Color Blindness:**
- Colorblind-friendly palettes (simulated protanopia, deuteranopia, tritanopia)
- Pattern use both color and symbols/text for distinction
- Sensible defaults; manual override available

**Dyslexia:**
- Optional dyslexia-friendly font (OpenDyslexic)
- Simpler, shorter sentences in UI copy
- Extra whitespace and clear typography

**Motor Impairment:**
- Large tap targets (minimum 48x48 dp on mobile)
- Voice command support (future roadmap)
- Haptic feedback for key interactions

**Neurodiversity (ADHD, Autism Spectrum):**
- Reduced animations and visual noise in sensory-aware mode
- Clear, linear task flows
- Ability to save progress and resume

---

## 5. Goals and Success Metrics

### 5.1 Product Goals

| Goal | Description | Owner |
|------|-------------|-------|
| **Accuracy** | Generated patterns produce geometrically correct shapes when followed with user's gauge | Engine Lead |
| **Accessibility** | 100% of interactive elements meet WCAG AA standards; screen reader compatible | QA/A11y Lead |
| **Performance** | Pattern generation < 200ms; visualization step < 50ms client-side | Backend Lead |
| **Usability** | 80% of new users complete first pattern generation without assistance | Product |
| **Mobile UX** | Smooth interaction on mid-range Android/iOS (2-3 year old devices) | Frontend Lead |
| **Community Trust** | Users report confidence in pattern correctness (NPS > 50) | Product |

### 5.2 Success Metrics (MVP)

| Metric | Target | Baseline | Notes |
|--------|--------|----------|-------|
| Pattern Generation Speed | < 200ms p95 | N/A | Server-side generation for 50-round pattern |
| Visualization FPS | 60 FPS p95 | N/A | Smooth scrolling and round transitions |
| Accessibility Score | WCAG AA 100% | N/A | Automated and manual audits |
| Pattern Correctness Rate | 98%+ | N/A | QA testing of generated patterns |
| Mobile Device Coverage | 95% on common devices | N/A | iOS 14+, Android 9+ |
| Time to First Pattern | < 3 minutes | N/A | New user journey |
| Error Rate | < 0.1% | N/A | Unhandled exceptions in production |
| Uptime | 99.5% | N/A | Excluding maintenance windows |

### 5.3 User Satisfaction Goals

| Metric | Target | Method |
|--------|--------|--------|
| Task Success Rate | 90%+ | In-app surveys after each major task |
| User Confidence (Confidence in Pattern) | 8/10 avg | Post-generation survey |
| Ease of Use (SUS Score) | 70+ | System Usability Scale survey |
| Feature Relevance | 85%+ find features useful | Usage analytics + periodic surveys |
| Likelihood to Recommend (NPS) | > 50 | In-app NPS survey |

---

## 6. Scope: MVP Features In/Out

### 6.1 Features In (MVP)

#### Geometric Shapes
- Sphere (ball amigurumi head)
- Ellipsoid (egg shape, variant proportions)
- Cylinder (trunk, pillar, with optional end caps)
- Cone/Tapered Cylinder (limbs with diameter taper)

#### Stitch Types (Initial)
- Single Crochet (sc)
- Half Double Crochet (hdc) - included if timeline permits
- Basic Increases & Decreases
- Magic Ring / Chain Start
- Simple Sequences and Repeats

#### Rounds Modes
- Spiral rounds (continuous, no join)
- Joined rounds (planned for MVP; scope-dependent)

#### Inputs & Customization
- Shape selection and parameter input (dimensions in cm or inches)
- Yarn weight selection or custom gauge entry (stitches/rows per 10 cm)
- Stitch type selection (sc, hdc, dc)
- Terminology choice (US or UK)
- Round mode selection (spiral or joined)

#### Visualization & Navigation
- Per-round diagram with stitch visualization
- Round-by-round navigation (next, back, jump to round)
- Stitch highlighting for increases/decreases
- Tooltip explanations for each stitch type
- Color-coded visual legend

#### Control & Accessibility
- US ↔ UK terminology toggle with live update
- Left/Right-handed mirror option
- Text size adjustment
- High-contrast and colorblind-friendly modes
- Kid Mode (simplified copy, larger controls, safe palette)
- Full keyboard navigation

#### Exports
- PDF export (cover, materials, abbreviations, pattern, visuals page)
- SVG diagram export (per-round or all rounds)
- PNG preview export
- JSON DSL export (for reuse and integration)

#### Internationalization (I18n)
- US/UK terminology with automated translation layer
- Unit conversion (cm ↔ inches)
- Foundational i18n structure for future language support

#### Analytics & Telemetry
- Anonymous, privacy-respecting usage telemetry
- Opt-in consent at first run
- Metrics: shape generation counts, parse success rate, export usage

---

### 6.2 Features Out (Post-MVP Roadmap)

#### Shapes & Stitches
- Toroidal shapes (donuts)
- Advanced double crochet (dc) color work
- Cables and textured stitches
- Filet crochet patterns

#### Pattern Features
- Multi-part assemblies (arms, legs, head as separate modules)
- Automatic part composition
- Stripes and gradient yarn weight transitions
- Per-round stuffing cues and marker placement instructions
- Gauge swatch generation

#### Parsing & Text Input
- Complex external pattern parsing (beyond MVP's limited grammar)
- Full-text crochet pattern import
- Community pattern library integration

#### AI/Advanced Features
- Photo-to-primitive fitting (image recognition of shapes)
- Custom 3D mesh conversion
- Automatic yarn brand recommendations
- E-commerce integration

#### Community & Sharing
- Pattern marketplace / public library
- Social features (likes, comments, follows)
- Collaborative editing
- Version control for patterns

#### Stitch Library
- Extended stitch catalog (HDC, DC, tr, extended tr, etc.)
- Color work (tapestry, graphgan)
- Special techniques (bobbles, popcorn, clusters)

#### Optimization
- Beads and embellishments
- Yarn waste optimization
- 3D rendering (WebGL visualization)
- AR preview in app

---

## 7. Detailed Functional Requirements with Acceptance Criteria

### 7.1 FR-01: Geometric Pattern Generation

**Requirement:** The application SHALL generate accurate, beginner-friendly crochet patterns for geometric shapes based on user-provided parameters.

#### User Input Form (FR-01.1)

**Description:** Provide a guided form for users to specify shape parameters.

**Inputs Required:**
- Shape selection (sphere, ellipsoid, cylinder, cone)
- Dimensions (diameter/length in cm or inches)
- Yarn weight category OR custom gauge (stitches/10cm, rows/10cm)
- Stitch type (sc, hdc, dc if included)
- Round mode (spiral or joined)
- Terminology (US or UK)
- Hook size (mm) - optional for visual reference

**Acceptance Criteria:**

| AC# | Criterion | Details |
|-----|-----------|---------|
| AC-G-01.1 | Input Validation | All numeric fields reject invalid input (negative, non-numeric); display user-friendly error messages |
| AC-G-01.2 | Required Fields | Form cannot submit without shape, dimension, and gauge specified |
| AC-G-01.3 | Unit Switching | Users can switch cm ↔ inches; values auto-convert with 1 decimal precision |
| AC-G-01.4 | Gauge Preset | Yarn weight selection auto-populates gauge ranges (e.g., Worsted = 8-11 sts/10cm) |
| AC-G-01.5 | Form Memory | Form retains user's last selections (cookie/localStorage) for 30 days |
| AC-G-01.6 | Accessibility | All inputs have accessible labels (aria-label, associated label elements) |

#### Pattern Generation Algorithm (FR-01.2)

**Description:** Implement algorithms for each shape type to compute stitch counts and round structure.

**Shape-Specific Algorithms:**

**Sphere (sc, spiral):**
- Input: diameter (D cm), gauge (gs sts/10cm, gr rows/10cm)
- Compute equator stitch count: Seq = round(gs * D / 10)
- Compute rounds to equator: Keq = round(gr * (D/2) / 10)
- Increasing phase: Add increasing number of stitches per round until equator
- Steady phase: Maintain stitch count for 1-2 rounds (optional)
- Decreasing phase: Mirror the increases with decreases

**Ellipsoid:**
- Extends sphere algorithm with separate diameters (width and height)
- Compute stitch count from major axis; round count from minor axis

**Cylinder:**
- Cap = half-sphere (sc with increases to target radius)
- Body = consistent stitch count, height-based rounds
- Optional second cap (mirror of first)
- Body rounds: round(gr * height / 10)

**Cone/Tapered Cylinder:**
- Initial stitch count: S0 from base diameter
- Final stitch count: S1 from tip diameter
- Distribute over K rounds
- Use modular spacing (Bresenham-like) to avoid columnar stacks

**Even Distribution Algorithm:**
- For ΔS increases/decreases across S stitches over K rounds
- Place changes every floor(S / ΔS) stitches
- Vary start position by round index to prevent visual columns

**Acceptance Criteria:**

| AC# | Criterion | Details |
|-----|-----------|---------|
| AC-G-02.1 | Sphere Accuracy | For 10cm sphere, gauge 14/16 (sc, spiral): equator count within ±1 stitch of theoretical |
| AC-G-02.2 | Sphere Rounds | For same sphere: round count to equator within ±1 of theoretical |
| AC-G-02.3 | Cylinder Accuracy | For 5cm dia, 8cm height, gauge 14/16: cap rounds computed, body rounds correct, stitch count steady |
| AC-G-02.4 | Cone Distribution | For tapered 6cm→2cm over 8cm: no consecutive stacks of inc/dec; delta changes distributed evenly |
| AC-G-02.5 | Deterministic | Same inputs always produce identical output (no randomization) |
| AC-G-02.6 | Gauge Tolerance | Algorithm handles gauges from 8-20 sts/10cm without error |
| AC-G-02.7 | Edge Cases | Algorithm handles dimension edge cases (< 1cm, > 50cm) gracefully |

#### Yarn Yardage Estimation (FR-01.3)

**Description:** Estimate total yarn required for the pattern.

**Calculation:**
- Average stitch length ≈ 0.5 cm per single crochet
- Estimate yarn per round: stitch_count × avg_stitch_length_cm
- Sum across all rounds
- Add 10% safety margin

**Acceptance Criteria:**

| AC# | Criterion | Details |
|-----|-----------|---------|
| AC-G-03.1 | Estimate Range | Estimate within ±15% of actual yarn used for generated sphere |
| AC-G-03.2 | Display | Show yardage and meters with ±margin noted |
| AC-G-03.3 | Material Info | Include yarn weight and recommended hook size |

#### Output Formats (FR-01.4)

**Description:** Generate pattern in multiple formats.

**Outputs:**
1. **Pattern DSL (JSON)** - Structured pattern data (see §11)
2. **Human-Readable Pattern Text** - Line-by-line pattern (see Example §16.1)
3. **Round Summary Table** - Per-round stitch counts and operations
4. **Visual Diagram SVG** - Simple 2D stitch visualization
5. **Yarn/Materials Summary** - Weight, hook size, yardage, abbreviations

**Acceptance Criteria:**

| AC# | Criterion | Details |
|-----|-----------|---------|
| AC-G-04.1 | DSL Completeness | JSON includes all required fields: meta, object, rounds, materials, notes |
| AC-G-04.2 | Text Format | Pattern text matches canonical format with no syntax errors |
| AC-G-04.3 | SVG Rendering | Diagram renders without artifacts; stitches evenly spaced in circles |
| AC-G-04.4 | Materials Accuracy | Hook size and yarn weight match user input |

---

### 7.2 FR-02: Pattern Visualization and Navigation

**Requirement:** The application SHALL render interactive, per-round pattern visualizations with stitch-level detail and navigation controls.

#### DSL to Visualization Compilation (FR-02.1)

**Description:** Transform Pattern DSL into renderable visualization frames.

**Process:**
- Parse each round's operations (MR, sc, inc, dec, etc.)
- Map operations to stitch coordinates in 2D space
- Identify highlights (increases, decreases)
- Compute nodal graph (stitches as nodes, sequence connections as edges)

**Acceptance Criteria:**

| AC# | Criterion | Details |
|-----|-----------|---------|
| AC-V-01.1 | Round Compilation | Every round in DSL compiles to frame without error |
| AC-V-01.2 | Stitch Count | Frame stitch count matches DSL round's stitches field |
| AC-V-01.3 | Large Patterns | Handles patterns with 100+ rounds without timeout (< 500ms) |
| AC-V-01.4 | Memory Efficiency | Loaded pattern uses < 10 MB RAM for 100-round pattern |

#### Per-Round Visualization Rendering (FR-02.2)

**Description:** Render each round as an interactive visual diagram.

**Visual Elements:**
- **Nodes:** Each stitch as a circle/node, colored by type (normal=gray, inc=green, dec=red)
- **Edges:** Lines connecting consecutive stitches (showing sequence)
- **Highlights:** Increase/decrease stitches highlighted with stronger color and glow effect
- **Legend:** Color key and stitch abbreviation legend
- **Current Stitch Marker:** Highlight the "active" stitch during navigation
- **Round Label:** Round number and stitch count

**Acceptance Criteria:**

| AC# | Criterion | Details |
|-----|-----------|---------|
| AC-V-02.1 | Visual Clarity | All nodes and edges render without overlap for patterns up to 60 stitches |
| AC-V-02.2 | Color Accuracy | Increase nodes are green, decrease red, normal gray (or alt palette if active) |
| AC-V-02.3 | FPS Performance | Smooth 60 FPS scrolling and transitions on mid-range mobile (iPhone 11+, Pixel 4+) |
| AC-V-02.4 | Responsive Layout | Diagram scales appropriately for phone (portrait), tablet (landscape), and desktop |
| AC-V-02.5 | Accessibility Colors | Color legend includes both color and text/symbol labels |

#### Round Navigation Controls (FR-02.3)

**Description:** Provide intuitive controls to step through pattern rounds.

**Controls:**
- **Previous/Next Buttons:** Large touch targets (48x48 dp min); step one round back/forward
- **Round Scrubber:** Horizontal slider showing current position; tap to jump
- **Round Jump Input:** Text input to jump to specific round (with validation)
- **First/Last Jump:** Quick buttons to go to start/end
- **Keyboard Support:** Arrow keys for navigation; numeric keys to jump (with confirmation)

**Acceptance Criteria:**

| AC# | Criterion | Details |
|-----|-----------|---------|
| AC-V-03.1 | Touch Targets | All buttons ≥ 48x48 dp; spacing ≥ 8 dp between adjacent buttons |
| AC-V-03.2 | Scrubber Accuracy | Scrubber position updates instantly; jumps are accurate to within 1 round |
| AC-V-03.3 | Keyboard Navigation | Arrow up/down works; NumPad entries jump to round (with prompt) |
| AC-V-03.4 | Boundary Handling | First round cannot go earlier; last round cannot go further |
| AC-V-03.5 | State Persistence | Current round position retained during session (lost on app close) |

#### Stitch-Level Tooltips and Explanations (FR-02.4)

**Description:** Provide contextual help for stitch types and operations.

**Features:**
- **Hover/Tap Tooltip:** Tapping a stitch shows its abbreviation, full name, and what it means
- **Stitch Glossary:** Popup glossary with definitions for all stitch types in pattern
- **"Explain This Round" Drawer:** Slide-up panel with narrative explanation of round (e.g., "In this round, we add 6 stitches evenly around. Each group of 3 stitches, we insert 2 in the same stitch.")
- **Beginner Hints:** For Kid Mode, additional simple phrasing (e.g., "Two stitches in one hole")

**Acceptance Criteria:**

| AC# | Criterion | Details |
|-----|-----------|---------|
| AC-V-04.1 | Tooltip Content | Every stitch has a tooltip with name, abbreviation, and action |
| AC-V-04.2 | Glossary Completeness | All stitches in pattern have glossary entries |
| AC-V-04.3 | Round Explanation | Auto-generated explanations for every round; human-readable |
| AC-V-04.4 | Kid Mode Copy | Simplified language used; no jargon; phrased encouragingly |
| AC-V-04.5 | Accessibility | Tooltips accessible via keyboard; screen reader friendly |

#### Terminology Toggle (US ↔ UK) (FR-02.5)

**Description:** Allow users to switch between US and UK crochet terminology, with live visualization update.

**Mapping:**
- US sc (single crochet) ↔ UK dc (double crochet)
- US hdc ↔ UK htr
- US dc ↔ UK tr
- Increases and decreases remain same conceptually but terminology may differ

**Behavior:**
- Toggle control in settings or visualization screen
- All labels and explanations update instantly
- Diagram remains geometrically identical (no recalculation)
- Export format respects the current term selection

**Acceptance Criteria:**

| AC# | Criterion | Details |
|-----|-----------|---------|
| AC-V-05.1 | Label Translation | All stitch labels update accurately when terminology toggled |
| AC-V-05.2 | Instant Update | Toggle completes in < 100ms; no flicker |
| AC-V-05.3 | Explanation Update | Glossary and round explanations use correct terminology |
| AC-V-05.4 | Consistency | Exported pattern and visualization always use same terminology |
| AC-V-05.5 | Export Fidelity | PDF and text exports reflect terminology choice |

#### Handedness Mirroring (FR-02.6)

**Description:** Allow left-handed users to see mirrored diagrams.

**Behavior:**
- Left/Right toggle in settings
- Diagram is horizontally flipped for left-handed view
- Text instructions remain same (stitches don't change)
- User handedness preference persisted in settings

**Acceptance Criteria:**

| AC# | Criterion | Details |
|-----|-----------|---------|
| AC-V-06.1 | Mirror Accuracy | Horizontal flip is geometrically accurate; no distortion |
| AC-V-06.2 | Instant Toggle | Flip completes in < 50ms |
| AC-V-06.3 | Persistence | Handedness setting saved and restored on app reopen |
| AC-V-06.4 | Clarity | Mirrored diagram is equally clear as original |

---

### 7.3 FR-03: Pattern Text Parsing (Scoped)

**Requirement:** The application SHALL parse a limited subset of crochet pattern text syntax and convert to Pattern DSL.

#### Supported Grammar (FR-03.1)

**Scope:** MVP supports a simplified bracket-and-repeat grammar for common US patterns.

**Supported Syntax:**
```
R1: MR 6 sc (6)
R2: inc x6 (12)
R3: [2 sc, inc] x6 (18)
R4: [sc, inc] x2 [hdc, inc] x2 (24)
```

**Tokens:**
- `R<N>:` - Round label
- `MR` - Magic ring
- `<stitch>` - sc, hdc, dc, slst, ch
- `inc`, `dec` - Increase, decrease
- `[...]` - Bracket for grouping
- `x<N>` - Repeat count
- `(<stitch_count>)` - Post-round stitch count

**Non-Supported (Rejected with Warning):**
- Complex abbreviations (tr, dtr, bobbles, cables)
- Row-based patterns (row 1, row 2)
- Color changes and special operations
- Tapestry and colorwork syntax

**Acceptance Criteria:**

| AC# | Criterion | Details |
|-----|-----------|---------|
| AC-P-01.1 | Parse Success | Canonical simple patterns parse without error |
| AC-P-01.2 | Error Reporting | Unsupported tokens produce user-friendly warnings (not crashes) |
| AC-P-01.3 | Partial Parse | If a round fails, remaining rounds still parse; user warned of error |
| AC-P-01.4 | Round Extraction | Final stitch count is extracted correctly; validated against sum |

#### Text to DSL Conversion (FR-03.2)

**Description:** Convert parsed text to Pattern DSL structure.

**Conversion Rules:**
- Build `rounds[]` array
- Map abbreviations to DSL operations
- Compute stitches count per round
- Infer `meta` fields (terms=US, units=cm by default)

**Acceptance Criteria:**

| AC# | Criterion | Details |
|-----|-----------|---------|
| AC-P-02.1 | DSL Structure | Output DSL is valid JSON; passes schema validation |
| AC-P-02.2 | Stitch Accuracy | Stitch counts match input; totals correct |
| AC-P-02.3 | No Data Loss | All operations from text are represented in DSL |

#### Manual Edit Mode (FR-03.3)

**Description:** Allow users to manually edit parsed patterns or DSL before visualization.

**Features:**
- Text editor view for pattern text (if parsed from text)
- Option to edit DSL directly (for advanced users)
- Validation on save
- Visual diff of changes

**Acceptance Criteria:**

| AC# | Criterion | Details |
|-----|-----------|---------|
| AC-P-03.1 | Edit Validation | Edits are validated; user cannot save invalid patterns |
| AC-P-03.2 | Feedback | Clear error messages on validation failure |

---

### 7.4 FR-04: Pattern Export

**Requirement:** The application SHALL support exporting patterns in multiple formats suitable for sharing and printing.

#### PDF Export (FR-04.1)

**Description:** Generate a professional, printable PDF document.

**Contents:**
- **Cover Page:** Title, object description, dimensions, yarn weight, hook size
- **Materials Page:** Yarn yardage, hook size, notions (stitch markers, eyes, etc.)
- **Abbreviations Reference:** Full definitions of all stitches and terms used
- **Pattern Page:** Human-readable pattern text, organized by round
- **Visuals Page:** SVG diagrams (first 10 rounds, last 10 rounds, or key rounds)

**Formatting:**
- Standard A4/Letter size, optimized for mobile printing (fits 8.5x11")
- Readable font (12pt main, 10pt details)
- Page breaks handled correctly
- Branding: Knit-Wit logo and footer

**Acceptance Criteria:**

| AC# | Criterion | Details |
|-----|-----------|---------|
| AC-E-01.1 | PDF Generation | PDF generates without error for any valid pattern |
| AC-E-01.2 | Print Quality | PDF prints correctly on A4 and Letter paper (landscape and portrait) |
| AC-E-01.3 | File Size | PDF < 5 MB for typical pattern |
| AC-E-01.4 | Content Completeness | All required sections included; no text overflow |
| AC-E-01.5 | Mobile Print | PDF is readable on mobile print preview (small screen) |
| AC-E-01.6 | Accessibility | PDF includes text layer for accessibility; images have alt text |

#### SVG/PNG Export (FR-04.2)

**Description:** Export diagrams in vector and raster formats.

**Exports:**
- **Per-Round SVGs:** Individual SVG file for each round (downloadable as ZIP or single file option)
- **Composite SVG:** All rounds on a single page (grid layout)
- **PNG Preview:** Single PNG showing key rounds (composite image)

**Specifications:**
- SVG fully editable in Illustrator, Inkscape, etc.
- PNG resolution: 72 DPI for screen, 300 DPI option for print

**Acceptance Criteria:**

| AC# | Criterion | Details |
|-----|-----------|---------|
| AC-E-02.1 | SVG Validity | SVG files validate against SVG schema |
| AC-E-02.2 | Editability | SVG opens in standard design tools without warnings |
| AC-E-02.3 | PNG Quality | PNG renders clearly; dimensions appropriate for use case |
| AC-E-02.4 | File Naming | Files named intuitively (e.g., sphere-10cm-r1.svg) |

#### JSON DSL Export (FR-04.3)

**Description:** Export pattern as machine-readable JSON DSL for reuse and integration.

**Format:** See §11 (Pattern DSL Specification)

**Acceptance Criteria:**

| AC# | Criterion | Details |
|-----|-----------|---------|
| AC-E-03.1 | JSON Validity | Export is valid JSON; passes schema validation |
| AC-E-03.2 | Completeness | All pattern data captured; round-by-round accuracy preserved |
| AC-E-03.3 | Roundtrip | DSL can be imported and visualized identically to original |

---

### 7.5 FR-05: Accessibility and Internationalization

**Requirement:** The application SHALL support users of all abilities and multiple terminology systems.

#### Kid Mode (FR-05.1)

**Description:** Simplified, kid-friendly interface for young users and educators.

**Features:**
- **Simplified Copy:** Shorter sentences, simpler words, encouraging tone
- **Mascot/Character:** Friendly crochet character providing tips
- **Larger Tap Targets:** Minimum 56x56 dp (vs. standard 48x48)
- **Animated Tutorials:** Brief 5-10 second animations showing "what is an increase?"
- **Safe Color Palette:** Vibrant, non-jarring colors; approachable design
- **Reduced Complexity:** Hide advanced options (gauge presets, advanced exports)

**Acceptance Criteria:**

| AC# | Criterion | Details |
|-----|-----------|---------|
| AC-K-01.1 | Copy Simplification | All UI text is grade 4-5 reading level; verified by readability tool |
| AC-K-01.2 | Tap Target Size | All touch targets ≥ 56x56 dp; padding ≥ 12 dp |
| AC-K-01.3 | Animation | At least 3 simple animations present (increase, decrease, join) |
| AC-K-01.4 | Mode Toggle | Kid Mode can be toggled on/off in settings |
| AC-K-01.5 | Parental Guidance | Info message suggests parental co-engagement |

#### Accessibility Features (FR-05.2)

**Description:** Full WCAG AA compliance for users with disabilities.

**Features:**
- **Color Contrast:** All text ≥ 4.5:1 contrast ratio; UI elements ≥ 3:1
- **ARIA Labels:** All interactive elements have aria-label or aria-labelledby
- **Keyboard Navigation:** Full keyboard support; logical tab order; no keyboard trap
- **Screen Reader Support:** Patterns and diagrams have text descriptions
- **Focus Indicators:** Clear, high-contrast focus ring (minimum 2 px, 3:1 contrast)
- **Motion & Animation:** Respects `prefers-reduced-motion` system setting
- **Text Sizing:** Allows user to increase text size up to 200% without horizontal scroll

**Colorblind Modes:**
- Protanopia (Red-Green, 1% male, 0.01% female)
- Deuteranopia (Red-Green, 1% male, 0.01% female)
- Tritanopia (Blue-Yellow, 0.001%)
- Achromatopsia (Complete color blindness, rare)

**Alternative Palettes:**
- Increase: Green → Green + stripes pattern
- Decrease: Red → Red + hash pattern
- Normal: Gray → Gray + outlined

**Dyslexia-Friendly Font:**
- Option to switch to OpenDyslexic font
- Increased letter spacing
- Increased line height (1.5x)

**Acceptance Criteria:**

| AC# | Criterion | Details |
|-----|-----------|---------|
| AC-A-02.1 | Color Contrast | All text ≥ 4.5:1; UI elements ≥ 3:1 (WCAG AAA for critical paths) |
| AC-A-02.2 | ARIA Labels | 100% of form inputs and interactive controls have accessible names |
| AC-A-02.3 | Keyboard Nav | All features accessible via keyboard; tab order logical; no traps |
| AC-A-02.4 | Screen Reader | NVDA/JAWS can navigate app; pattern descriptions read correctly |
| AC-A-02.5 | Focus Indicator | Focus ring visible, ≥ 2px, sufficient contrast (3:1 minimum) |
| AC-A-02.6 | Motion Respect | Animations paused if `prefers-reduced-motion` media query set |
| AC-A-02.7 | Text Sizing | Text remains readable at 200% zoom; layout remains functional |
| AC-A-02.8 | Colorblind Test | App verified in colorblind simulation tools; patterns distinguishable |

#### US/UK Terminology System (FR-05.3)

**Description:** Automated translation between US and UK crochet terminology.

**Mapping Table:**

| Concept | US | UK |
|---------|----|----|
| Single Crochet | sc | dc |
| Half Double Crochet | hdc | htr |
| Double Crochet | dc | tr |
| Treble | tr | dtr |
| Increase | 2 sc in same st | 2 dc in same st |
| Decrease | sc2tog | dc2tog |

**Implementation:**
- Translation layer in backend and frontend
- Applied on generation (for generated patterns) and on toggle (for visualization)
- Consistent application across all outputs (text, diagrams, exports)

**Acceptance Criteria:**

| AC# | Criterion | Details |
|-----|-----------|---------|
| AC-I-03.1 | Translation Accuracy | All mappings apply correctly; no mismatches |
| AC-I-03.2 | Consistency | Same terminology used across pattern text, diagrams, and exports |
| AC-I-03.3 | Toggle Speed | Terminology switch < 100ms |

#### Units (Metric/Imperial) (FR-05.4)

**Description:** Support both metric (cm) and imperial (inches) units.

**Default:** cm (metric)
**Conversion:** 1 inch = 2.54 cm

**Application:**
- Pattern generation inputs (diameter, length)
- Gauge specification (can be cm or inches per specified unit)
- Exports (both units shown in PDF)

**Acceptance Criteria:**

| AC# | Criterion | Details |
|-----|-----------|---------|
| AC-I-04.1 | Conversion Accuracy | Conversions accurate to 0.1 unit |
| AC-I-04.2 | Display | Both units shown in relevant contexts (PDF, exports) |
| AC-I-04.3 | Input Flexibility | Users can input in either unit; app remembers preference |

---

### 7.6 FR-06: App Shell and Navigation

**Requirement:** The application SHALL provide intuitive navigation and a cohesive app experience.

#### Screen Structure (FR-06.1)

**Screens (MVP):**
1. **Home/Splash:** Quick start, recent patterns, app introduction
2. **Generate:** Shape selection, parameter input, preview
3. **Visualization:** Per-round diagram, controls, explanations
4. **Exports:** Export options, format selection
5. **Settings:** Preferences, accessibility options, about

**Navigation:**
- Bottom tab bar (mobile) or side navigation (desktop)
- Logical flow: Home → Generate → Visualize → Export
- Ability to jump to any screen

**Acceptance Criteria:**

| AC# | Criterion | Details |
|-----|-----------|---------|
| AC-SH-01.1 | Navigation Clarity | All screens easily accessible; no hidden paths |
| AC-SH-01.2 | Tab Bar | Mobile tab bar clearly labeled; icons + text |
| AC-SH-01.3 | Responsiveness | Navigation works on mobile, tablet, and desktop |

#### Form Validation and Error Handling (FR-06.2)

**Description:** Validate user inputs and provide clear error feedback.

**Validation Rules:**
- Required fields: Shape, dimension, gauge
- Numeric fields: Positive values only
- Gauge range: 6-25 sts/10cm, 8-30 rows/10cm
- Dimension range: 0.5-100 cm

**Error Display:**
- Inline error messages below field
- Field highlighting (red border)
- Non-blocking (user can attempt submit; errors repeated at top)
- Suggestions for correction

**Acceptance Criteria:**

| AC# | Criterion | Details |
|-----|-----------|---------|
| AC-SH-02.1 | Validation Rules | All rules enforced; invalid inputs rejected |
| AC-SH-02.2 | Error Messages | Clear, actionable error messages in plain language |
| AC-SH-02.3 | Accessibility | Error messages announced to screen readers |

#### Settings and Preferences (FR-06.3)

**Description:** Allow users to customize app behavior.

**Settings:**
- Units (cm / inches)
- Terminology (US / UK)
- Handedness (right / left)
- Text size (small / normal / large / extra large)
- Contrast mode (normal / high)
- Colorblind mode (normal / protanopia / deuteranopia / tritanopia)
- Dyslexia-friendly font (on / off)
- Kid Mode (on / off)
- Telemetry opt-in
- Language (future: en, es, fr, de, etc.)

**Behavior:**
- Settings persist locally (localStorage or equivalent)
- Changes apply instantly across app
- Reset to defaults option

**Acceptance Criteria:**

| AC# | Criterion | Details |
|-----|-----------|---------|
| AC-SH-03.1 | Persistence | Settings saved and restored across sessions |
| AC-SH-03.2 | Live Update | Settings changes apply instantly; no app restart needed |
| AC-SH-03.3 | Defaults | Clear "Reset to Defaults" option works correctly |
| AC-SH-03.4 | Accessibility | All settings accessible via keyboard and screen reader |

#### Telemetry and Analytics (FR-06.4)

**Description:** Collect anonymous, privacy-respecting usage data.

**Data Collected:**
- Shape generation counts (sphere, cylinder, cone, etc.)
- Stitch type preferences (sc, hdc, dc)
- Export format usage (PDF, SVG, JSON)
- Visualization round engagement (avg rounds per session)
- Parse success rate (for text parsing)
- Error/crash reports (anonymized)

**Privacy Guarantees:**
- No PII collected (no user ID, location, IP, device ID)
- Opt-in consent at first run (clear, easy to understand)
- Opt-out available in settings
- Data encrypted in transit (HTTPS)
- Data deleted after 90 days (retention policy)

**Acceptance Criteria:**

| AC# | Criterion | Details |
|-----|-----------|---------|
| AC-SH-04.1 | Consent UX | Clear, non-dark-pattern consent prompt at first run |
| AC-SH-04.2 | Data Collection | Collection only happens if opt-in granted |
| AC-SH-04.3 | Transparency | Privacy policy clearly explains data usage |
| AC-SH-04.4 | Opt-Out | User can easily opt-out in settings |

---

## 8. Non-Functional Requirements

### 8.1 Performance Requirements

| Requirement | Target | Measurement |
|-------------|--------|-------------|
| Pattern Generation | < 200ms (p95) | Server-side generation of 50-round sphere |
| Visualization Load | < 1 second (p95) | Time from API response to first render |
| Round Step | < 50ms (p95) | Navigation between adjacent rounds |
| Text Scroll | 60 FPS (p99) | Smooth scrolling on target devices |
| Export Generation | < 5 seconds (p95) | PDF export for 100-round pattern |
| UI Response | < 100ms | Button click to visual feedback |

**Target Devices for Performance Testing:**
- iPhone 11 / iOS 15+
- Pixel 4a / Android 11+
- iPad (6th gen) / iPadOS 15+

### 8.2 Reliability Requirements

| Requirement | Target |
|-------------|--------|
| Uptime | 99.5% (18 minutes downtime/month) |
| Pattern Determinism | 100% (same input → same output) |
| Data Durability | No pattern data loss |
| Graceful Degradation | App continues functioning with reduced features during outages |
| Crash Rate | < 0.1% of sessions |
| Error Recovery | Auto-retry for transient failures; user-friendly error messages |

### 8.3 Scalability Requirements

| Requirement | Target | Notes |
|-------------|--------|-------|
| Concurrent Users | 100+ simultaneous API calls | During peak usage |
| Request Throughput | 10 requests/second sustained | Per API endpoint |
| Database Reads | Not applicable (stateless MVP) | Patterns generated on-demand |
| Database Writes | Not applicable (stateless MVP) | No persistent storage of patterns |
| Storage Capacity | Not applicable (stateless MVP) | Assets cached, not persisted |

### 8.4 Security Requirements

| Requirement | Implementation |
|-------------|----------------|
| HTTPS Only | All endpoints HTTPS; redirect HTTP |
| Input Validation | Server-side validation of all inputs |
| XSS Prevention | All user inputs escaped; CSP headers configured |
| CORS | Restrict to known origins (frontend domain) |
| Rate Limiting | 60 requests/IP/minute; reasonable burst capacity |
| Dependency Scanning | Regular security audits of dependencies |
| PII Protection | No PII collected; design review ensures compliance |

### 8.5 Accessibility Requirements

| Requirement | Details |
|-------------|---------|
| WCAG AA Compliance | 100% of interactive elements |
| Color Contrast | Text ≥ 4.5:1; UI ≥ 3:1 |
| Keyboard Navigation | All features accessible without mouse |
| Screen Reader Support | ARIA labels; semantic HTML |
| Focus Management | Clear, visible focus indicator |
| Motion | Respect `prefers-reduced-motion` |

### 8.6 Compatibility Requirements

| Dimension | Support |
|-----------|---------|
| Mobile OS | iOS 14+, Android 9+ |
| Browsers (Web) | Chrome 90+, Safari 14+, Firefox 88+, Edge 90+ |
| Screen Sizes | 320px (mobile) to 2560px (desktop) |
| Input Methods | Touch, mouse, keyboard |
| Connectivity | Works on 3G/LTE; graceful offline degradation (future) |
| Device RAM | 2GB+ (targets mid-range devices) |

---

## 9. System Architecture Overview

### 9.1 Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                  FRONTEND (React Native/Web)            │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Generate   │  │ Visualization│  │   Export     │  │
│  │   Screen     │  │   Screen     │  │   Screen     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│         │                  │                  │          │
│         └──────────────────┴──────────────────┘          │
│                           │                              │
│              ┌────────────┼────────────┐                 │
│              │  HTTP / WebSocket       │                 │
│              └────────────┼────────────┘                 │
└─────────────────────────┼──────────────────────────────┘
                          │
                ┌─────────▼─────────┐
                │   FASTAPI SERVER  │
                │                   │
                │ ┌───────────────┐ │
                │ │ Generate API  │ │
                │ ├───────────────┤ │
                │ │ Visualize API │ │
                │ ├───────────────┤ │
                │ │ Parse API     │ │
                │ ├───────────────┤ │
                │ │ Export API    │ │
                │ └───────────────┘ │
                │                   │
                │ ┌───────────────┐ │
                │ │ Pattern Comp. │ │
                │ │ (Python Lib)  │ │
                │ └───────────────┘ │
                └───────────────────┘
```

### 9.2 Key Components

**Frontend (Mobile Web App)**
- **Technology:** React Native (Expo) or React Web
- **State Management:** Redux or Context API
- **Routing:** React Navigation
- **Styling:** Tailwind CSS / NativeWind
- **Rendering:** react-native-svg for diagrams
- **Platforms:** iOS (14+), Android (9+), Web browsers

**Backend (API Server)**
- **Technology:** Python + FastAPI
- **Deployment:** Docker container
- **Web Server:** Uvicorn
- **Async Processing:** Python async/await
- **Caching:** In-memory (no persistent cache in MVP)

**Pattern Compiler Library**
- **Technology:** Python module
- **Location:** Shared monorepo `pattern-compiler/`
- **Responsibility:** Shape geometry, stitch calculation, DSL generation
- **Testing:** Unit tests for all algorithms

**External Services (Optional for MVP)**
- **PDF Generation:** ReportLab (Python) or external service
- **Image Processing:** Pillow (Python) for PNG generation
- **Monitoring:** Error tracking (Sentry optional)

### 9.3 Data Flow

**Pattern Generation Flow:**
```
1. User submits Generate form
   ↓
2. Frontend sends POST /patterns/generate
   ↓
3. Backend validates inputs
   ↓
4. Pattern Compiler generates DSL
   ↓
5. Backend generates SVG diagram
   ↓
6. Backend returns DSL + assets
   ↓
7. Frontend caches DSL; displays preview
```

**Visualization Flow:**
```
1. User opens Visualization screen
   ↓
2. Frontend loads cached DSL (or fetches if needed)
   ↓
3. Frontend sends POST /patterns/visualize
   ↓
4. Backend compiles DSL → render frames
   ↓
5. Backend returns frames (nodes, edges, highlights)
   ↓
6. Frontend renders frames; handles navigation client-side
```

---

## 10. Technical Stack

### 10.1 Frontend Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Framework** | React Native (Expo) | Cross-platform mobile; web support |
| **State Mgmt** | Redux | Centralized state for forms and cache |
| **Styling** | NativeWind / Tailwind | Utility-first, consistent across platforms |
| **SVG Rendering** | react-native-svg | Efficient diagram rendering |
| **Navigation** | React Navigation | Mature, full-featured routing |
| **Testing** | Jest + React Testing Library | Standard, comprehensive testing |
| **Build** | Expo CLI / EAS | Simple build management |
| **Package Manager** | pnpm | Fast, efficient monorepo support |

### 10.2 Backend Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Framework** | FastAPI (Python 3.10+) | Modern, async, automatic docs |
| **Server** | Uvicorn | ASGI server; high performance |
| **Pattern Lib** | Custom Python module | Domain-specific, optimized algorithms |
| **PDF Export** | ReportLab / WeasyPrint | Pure Python; no external dependencies |
| **Image Gen** | Pillow (PIL) | Simple PNG/SVG → PNG conversion |
| **Validation** | Pydantic | Type-safe request/response validation |
| **Testing** | pytest + pytest-asyncio | Async test support |
| **Type Hints** | Python type hints | Static type checking (mypy) |
| **Dependency Mgmt** | pip / requirements.txt (or poetry) | Standard Python packaging |

### 10.3 DevOps & Deployment

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Containerization** | Docker | Consistent dev/prod environments |
| **Container Registry** | Docker Hub / GitHub Container Registry | Image storage |
| **Hosting (API)** | Cloud Run / AppEngine / Custom VPS | Serverless or managed |
| **Hosting (Frontend)** | Vercel / Netlify / AWS S3 + CloudFront | JAMstack hosting |
| **CI/CD** | GitHub Actions | Automated testing, builds, deployment |
| **Monitoring** | Cloud Logging / Datadog | Error tracking and performance |
| **Database** | None (MVP) | Stateless architecture |

### 10.4 Development Environment

| Tool | Purpose |
|------|---------|
| **Git** | Version control |
| **GitHub** | Repository, PRs, issues |
| **Monorepo Structure** | pnpm workspaces (if JS) + separate folders for Python |
| **IDE** | VS Code (recommended) |
| **Linting** | ESLint (JS), Black/Flake8 (Python) |
| **Code Formatting** | Prettier (JS), Black (Python) |
| **Pre-commit** | Hooks for linting, type-checking |

---

## 11. Pattern DSL Specification (v0.1)

### 11.1 JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Crochet Pattern DSL v0.1",
  "type": "object",
  "required": ["meta", "object", "rounds", "materials"],
  "properties": {
    "meta": {
      "type": "object",
      "required": ["version", "units", "terms", "stitch", "round_mode", "gauge"],
      "properties": {
        "version": {
          "type": "string",
          "enum": ["0.1"],
          "description": "DSL version"
        },
        "units": {
          "type": "string",
          "enum": ["cm", "inches"],
          "description": "Measurement units"
        },
        "terms": {
          "type": "string",
          "enum": ["US", "UK"],
          "description": "Crochet terminology"
        },
        "stitch": {
          "type": "string",
          "enum": ["sc", "hdc", "dc"],
          "description": "Primary stitch type"
        },
        "round_mode": {
          "type": "string",
          "enum": ["spiral", "joined"],
          "description": "Spiral or joined rounds"
        },
        "gauge": {
          "type": "object",
          "required": ["sts_per_10cm", "rows_per_10cm"],
          "properties": {
            "sts_per_10cm": {
              "type": "number",
              "minimum": 6,
              "maximum": 25,
              "description": "Stitches per 10cm"
            },
            "rows_per_10cm": {
              "type": "number",
              "minimum": 8,
              "maximum": 30,
              "description": "Rows per 10cm"
            }
          }
        }
      }
    },
    "object": {
      "type": "object",
      "required": ["type", "params"],
      "properties": {
        "type": {
          "type": "string",
          "enum": ["sphere", "ellipsoid", "cylinder", "cone"],
          "description": "Shape type"
        },
        "params": {
          "oneOf": [
            {
              "type": "object",
              "properties": {
                "diameter": { "type": "number", "minimum": 0.5, "maximum": 100 }
              },
              "required": ["diameter"],
              "description": "Sphere parameters"
            },
            {
              "type": "object",
              "properties": {
                "width": { "type": "number", "minimum": 0.5, "maximum": 100 },
                "height": { "type": "number", "minimum": 0.5, "maximum": 100 }
              },
              "required": ["width", "height"],
              "description": "Ellipsoid parameters"
            },
            {
              "type": "object",
              "properties": {
                "diameter": { "type": "number", "minimum": 0.5, "maximum": 100 },
                "height": { "type": "number", "minimum": 0.5, "maximum": 100 },
                "end_caps": { "type": "boolean", "default": true }
              },
              "required": ["diameter", "height"],
              "description": "Cylinder parameters"
            },
            {
              "type": "object",
              "properties": {
                "base_diameter": { "type": "number", "minimum": 0.5, "maximum": 100 },
                "tip_diameter": { "type": "number", "minimum": 0.5, "maximum": 100 },
                "length": { "type": "number", "minimum": 0.5, "maximum": 100 }
              },
              "required": ["base_diameter", "tip_diameter", "length"],
              "description": "Cone/tapered cylinder parameters"
            }
          ]
        }
      }
    },
    "rounds": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["r", "ops", "stitches"],
        "properties": {
          "r": {
            "type": "integer",
            "minimum": 1,
            "description": "Round number"
          },
          "ops": {
            "type": "array",
            "minItems": 1,
            "items": {
              "type": "object",
              "required": ["op"],
              "properties": {
                "op": {
                  "type": "string",
                  "enum": ["MR", "sc", "hdc", "dc", "slst", "ch", "inc", "dec", "seq"],
                  "description": "Operation type"
                },
                "count": {
                  "type": "integer",
                  "minimum": 1,
                  "description": "Repeat count for this operation"
                },
                "repeat": {
                  "type": "integer",
                  "minimum": 1,
                  "description": "How many times to repeat the sequence"
                },
                "pattern": {
                  "type": "array",
                  "description": "For seq: array of operations within the sequence"
                }
              }
            }
          },
          "stitches": {
            "type": "integer",
            "minimum": 1,
            "description": "Total stitch count after this round"
          }
        }
      }
    },
    "materials": {
      "type": "object",
      "properties": {
        "yarn_weight": {
          "type": "string",
          "enum": ["Lace", "Fingering", "Sport", "DK", "Worsted", "Bulky", "Super Bulky"],
          "description": "Yarn weight category"
        },
        "hook_size_mm": {
          "type": "number",
          "minimum": 1,
          "maximum": 20,
          "description": "Hook size in millimeters"
        },
        "yardage_estimate": {
          "type": "number",
          "minimum": 0,
          "description": "Estimated yarn needed in meters"
        },
        "notions": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Additional supplies (stitch markers, eyes, etc.)"
        }
      }
    },
    "notes": {
      "type": "array",
      "items": { "type": "string" },
      "description": "General notes about the pattern"
    }
  }
}
```

### 11.2 Operation Vocabulary

| Op | Name | Parameters | Example | Description |
|-----|------|-----------|---------|-------------|
| `MR` | Magic Ring | `count` | `{"op":"MR","count":1}` | Create magic ring; usually 1 per pattern |
| `sc` | Single Crochet | `count` | `{"op":"sc","count":6}` | N single crochets in available loops |
| `hdc` | Half Double Crochet | `count` | `{"op":"hdc","count":4}` | N half double crochets |
| `dc` | Double Crochet | `count` | `{"op":"dc","count":8}` | N double crochets |
| `ch` | Chain | `count` | `{"op":"ch","count":2}` | N chain stitches |
| `slst` | Slip Stitch | `count` | `{"op":"slst","count":1}` | N slip stitches (typically 1 to join) |
| `inc` | Increase | `count` | `{"op":"inc","count":6}` | 2 stitches in each of N stitches |
| `dec` | Decrease | `count` | `{"op":"dec","count":3}` | Join 2 stitches for each of N decrease points |
| `seq` | Sequence | `pattern`, `repeat` | `{"op":"seq","pattern":["sc",1,"inc"],"repeat":6}` | Repeat a pattern N times |

### 11.3 Example DSL (Sphere)

```json
{
  "meta": {
    "version": "0.1",
    "units": "cm",
    "terms": "US",
    "stitch": "sc",
    "round_mode": "spiral",
    "gauge": {
      "sts_per_10cm": 14,
      "rows_per_10cm": 16
    }
  },
  "object": {
    "type": "sphere",
    "params": {
      "diameter": 10
    }
  },
  "rounds": [
    {
      "r": 1,
      "ops": [
        {"op": "MR", "count": 1},
        {"op": "sc", "count": 6}
      ],
      "stitches": 6
    },
    {
      "r": 2,
      "ops": [
        {"op": "inc", "count": 6}
      ],
      "stitches": 12
    },
    {
      "r": 3,
      "ops": [
        {"op": "seq", "pattern": ["sc", 1, "inc"], "repeat": 6}
      ],
      "stitches": 18
    },
    {
      "r": 4,
      "ops": [
        {"op": "seq", "pattern": ["sc", 2, "inc"], "repeat": 6}
      ],
      "stitches": 24
    },
    {
      "r": 5,
      "ops": [
        {"op": "seq", "pattern": ["sc", 3, "inc"], "repeat": 6}
      ],
      "stitches": 30
    }
  ],
  "materials": {
    "yarn_weight": "Worsted",
    "hook_size_mm": 4.0,
    "yardage_estimate": 25,
    "notions": ["Stitch marker"]
  },
  "notes": [
    "Work in a spiral. Use a stitch marker to mark the beginning of each round.",
    "Fasten off and weave in ends after final round."
  ]
}
```

---

## 12. API Endpoints Specification

### Base URL
```
https://api.knit-wit.com/v1
```

### 12.1 POST `/patterns/generate`

**Description:** Generate a crochet pattern for a geometric shape.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "object": {
    "type": "sphere",
    "params": {
      "diameter": 10
    }
  },
  "meta": {
    "units": "cm",
    "terms": "US",
    "stitch": "sc",
    "round_mode": "spiral",
    "gauge": {
      "sts_per_10cm": 14,
      "rows_per_10cm": 16
    }
  },
  "materials": {
    "yarn_weight": "Worsted",
    "hook_size_mm": 4.0
  }
}
```

**Response (200 OK):**
```json
{
  "dsl": {
    "meta": { /* ... */ },
    "object": { /* ... */ },
    "rounds": [ /* ... */ ],
    "materials": { /* ... */ },
    "notes": [ /* ... */ ]
  },
  "assets": {
    "diagram_svg": "<svg>...</svg>",
    "preview_png": "data:image/png;base64,iVBORw0KGgo..."
  },
  "exports": {
    "pdf_available": true
  },
  "metadata": {
    "generated_at": "2024-11-05T14:30:00Z",
    "generation_time_ms": 125
  }
}
```

**Response (400 Bad Request):**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input parameters",
    "details": {
      "field": "gauge.sts_per_10cm",
      "constraint": "Must be between 6 and 25"
    }
  },
  "request_id": "req_123abc"
}
```

**Response (500 Internal Server Error):**
```json
{
  "error": {
    "code": "GENERATION_ERROR",
    "message": "Pattern generation failed",
    "details": {
      "reason": "Algorithm error during cylinder cap calculation"
    }
  },
  "request_id": "req_456def"
}
```

**Rate Limiting Headers:**
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 59
X-RateLimit-Reset: 1699193400
```

---

### 12.2 POST `/patterns/visualize`

**Description:** Compile a Pattern DSL into renderable visualization frames.

**Request Body:**
```json
{
  "pattern": {
    "dsl": {
      "meta": { /* ... */ },
      "object": { /* ... */ },
      "rounds": [ /* ... */ ],
      "materials": { /* ... */ }
    },
    "render_options": {
      "handedness": "right",
      "contrast": "normal",
      "terms": "US",
      "colorblind_mode": "normal",
      "text_size": "normal"
    }
  }
}
```

**Response (200 OK):**
```json
{
  "frames": [
    {
      "round": 1,
      "stitch_count": 6,
      "nodes": [
        {
          "id": 1,
          "type": "sc",
          "x": 0.5,
          "y": 0.9,
          "highlighted": false
        }
      ],
      "edges": [
        {
          "from": 1,
          "to": 2,
          "style": "normal"
        }
      ],
      "highlights": [
        {
          "type": "increase",
          "node_indices": []
        }
      ]
    },
    {
      "round": 2,
      "stitch_count": 12,
      "nodes": [ /* ... */ ],
      "edges": [ /* ... */ ],
      "highlights": [
        {
          "type": "increase",
          "node_indices": [0, 2, 4, 6, 8, 10]
        }
      ]
    }
  ],
  "legend": {
    "sc": "Single Crochet",
    "hdc": "Half Double Crochet",
    "inc": "Increase",
    "dec": "Decrease"
  },
  "metadata": {
    "total_rounds": 17,
    "compilation_time_ms": 45
  }
}
```

**Response (400 Bad Request):**
```json
{
  "error": {
    "code": "INVALID_DSL",
    "message": "Pattern DSL validation failed",
    "details": {
      "field": "rounds[2]",
      "constraint": "Stitch count mismatch"
    }
  },
  "request_id": "req_789ghi"
}
```

---

### 12.3 POST `/patterns/parse-text`

**Description:** Parse crochet pattern text in supported syntax and convert to DSL.

**Request Body:**
```json
{
  "text": "R1: MR 6 sc (6)\nR2: inc x6 (12)\nR3: [2 sc, inc] x6 (18)",
  "defaults": {
    "units": "cm",
    "terms": "US",
    "stitch": "sc",
    "gauge": {
      "sts_per_10cm": 14,
      "rows_per_10cm": 16
    }
  }
}
```

**Response (200 OK):**
```json
{
  "dsl": {
    "meta": { /* ... */ },
    "rounds": [ /* ... */ ],
    "materials": {
      "yarn_weight": null,
      "hook_size_mm": null,
      "yardage_estimate": 0
    },
    "notes": []
  },
  "parse_report": {
    "success_rate": 1.0,
    "warnings": [],
    "parsed_rounds": 3,
    "failed_rounds": 0
  },
  "metadata": {
    "parse_time_ms": 12
  }
}
```

**Response (422 Unprocessable Entity - Partial Parse):**
```json
{
  "dsl": {
    "meta": { /* ... */ },
    "rounds": [
      { "r": 1, "ops": [ /* ... */ ], "stitches": 6 },
      { "r": 2, "ops": [ /* ... */ ], "stitches": 12 }
    ],
    "materials": { /* ... */ }
  },
  "parse_report": {
    "success_rate": 0.67,
    "warnings": [
      {
        "round": 3,
        "message": "Unsupported syntax: 'special_op' - skipped, parsed up to that point"
      }
    ],
    "parsed_rounds": 2,
    "failed_rounds": 1
  },
  "metadata": {
    "parse_time_ms": 15
  }
}
```

---

### 12.4 POST `/export/pdf`

**Description:** Generate a printable PDF from a pattern DSL.

**Request Body:**
```json
{
  "dsl": { /* full DSL object */ },
  "options": {
    "include_diagrams": true,
    "diagram_rounds": [1, 2, 3, -3, -2, -1],
    "title": "My Sphere",
    "author": "User",
    "branding": "default"
  }
}
```

**Response (200 OK):**
```
Content-Type: application/pdf
Content-Disposition: attachment; filename="my-sphere-pattern.pdf"

[Binary PDF data]
```

**Response (400 Bad Request):**
```json
{
  "error": {
    "code": "INVALID_EXPORT_PARAMS",
    "message": "Diagram rounds exceed pattern size"
  },
  "request_id": "req_012jkl"
}
```

**Response (500 Server Error):**
```json
{
  "error": {
    "code": "PDF_GENERATION_ERROR",
    "message": "Failed to generate PDF",
    "details": {
      "reason": "ReportLab encoding error"
    }
  },
  "request_id": "req_345mno"
}
```

---

### 12.5 GET `/health`

**Description:** Health check endpoint for monitoring.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2024-11-05T14:35:00Z",
  "version": "0.1.0"
}
```

---

### Error Response Format (All Endpoints)

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "Optional field context",
      "constraint": "Optional constraint violated"
    }
  },
  "request_id": "Unique request identifier for support"
}
```

**Common Error Codes:**
- `VALIDATION_ERROR` - Input validation failed
- `INVALID_DSL` - DSL structure invalid
- `INVALID_EXPORT_PARAMS` - Export options invalid
- `GENERATION_ERROR` - Algorithm error during generation
- `PDF_GENERATION_ERROR` - PDF export failed
- `UNSUPPORTED_OPERATION` - Requested operation not supported
- `RATE_LIMIT_EXCEEDED` - Rate limit exceeded
- `INTERNAL_SERVER_ERROR` - Unhandled server error

---

## 13. Algorithm Details

### 13.1 Gauge Mapping

**Purpose:** Convert user-provided gauge (stitches/rows per 10 cm) to actual stitch and round counts for a given dimension.

**Formulas:**

For a dimension D (in cm) and gauge g_s (stitches per 10 cm):
```
stitch_count = round(D * g_s / 10)
```

For a dimension D and gauge g_r (rows per 10 cm):
```
round_count = round(D * g_r / 10)
```

**Example:**
- Sphere diameter: 10 cm
- Gauge: 14 sts/10 cm, 16 rows/10 cm
- Equator stitches: round(10 * 14 / 10) = 14
- Rounds to equator: round((10/2) * 16 / 10) = 8

---

### 13.2 Sphere Generation Algorithm

**Input:**
- Diameter (D) in cm
- Gauge (g_s stitches/10 cm, g_r rows/10 cm)
- Stitch type (sc)
- Round mode (spiral)

**Process:**

**Step 1: Compute Target Metrics**
- Equator stitch count: S_eq = round(D * g_s / 10)
- Rounds to equator: K_eq = round((D/2) * g_r / 10)
- Initial stitch count (magic ring): S_0 = 6
- Increase per round until equator: ΔS = round((S_eq - S_0) / K_eq)

**Step 2: Increase Phase**
- Start: S_0 = 6 stitches in magic ring
- Round 2: Add ΔS increases (2-in-1 stitches evenly distributed)
- Rounds 3+: Increase by ΔS per round using patterned increases: `[N sc, inc] x (S / (S+ΔS))`
- Continue until S ≥ S_eq

**Step 3: Steady Phase (Optional)**
- Maintain S_eq for 1-2 rounds (for visual interest and roundness)

**Step 4: Decrease Phase**
- Mirror the increase phase in reverse
- Decrease by ΔS per round: `[N sc, dec] x (S / (S-ΔS))`
- Continue until S = 6

**Example (10 cm Sphere):**
```
S_eq = 14, K_eq = 8, ΔS = 1 (per round average)
R1: MR 6 sc (6)
R2: inc x6 (12) — 6 increases
R3: [sc, inc] x6 (18) — 6 increases
R4: [2 sc, inc] x6 (24) — 6 increases
...continues until equator
```

---

### 13.3 Tapered Cylinder (Cone) Algorithm

**Input:**
- Base diameter (D_0) in cm
- Tip diameter (D_1) in cm
- Length (L) in cm
- Gauge (g_s, g_r)

**Process:**

**Step 1: Compute Stitch Counts**
- Initial stitches: S_0 = round(D_0 * g_s / 10)
- Final stitches: S_1 = round(D_1 * g_s / 10)
- Total rounds: K = round(L * g_r / 10)
- Total delta: ΔS_total = S_1 - S_0

**Step 2: Distribute Deltas Evenly (Modular Spacing)**
- If ΔS_total > 0 (increasing): distribute K increases across K rounds
- If ΔS_total < 0 (decreasing): distribute |ΔS_total| decreases across K rounds
- Use Bresenham-like algorithm to avoid columnar stacking

**Bresenham Spacing:**
```python
def distribute_deltas(num_rounds, total_delta):
    """
    Distribute total_delta increases/decreases across num_rounds
    evenly to avoid stacking.

    Returns: list of (round, count) tuples
    """
    result = []
    error = 0
    delta_per_round = abs(total_delta) / num_rounds

    for r in range(1, num_rounds + 1):
        error += delta_per_round
        if error >= 1.0:
            result.append((r, int(error)))
            error -= int(error)

    return result
```

**Example (6 cm → 2 cm over 8 cm):**
```
S_0 = 8, S_1 = 3, ΔS = -5, K = 8
Distribute 5 decreases evenly across 8 rounds:
Rounds 1, 3, 5, 7: 1 decrease
Rounds 2, 4, 6: skip
Result: Smooth taper, no columns
```

---

### 13.4 Even Distribution Algorithm

**Purpose:** Distribute increases/decreases evenly around a round without creating visual stacking.

**Algorithm:**
For ΔS increases to apply across S stitches in a round:
1. Compute spacing: space = floor(S / ΔS)
2. Vary start offset by round index (modulo) to avoid stacking across rounds
3. Place inc at positions: offset, offset + space, offset + 2*space, ...

**Example:**
```
Round 2: S = 6, ΔS = 6 inc
  spacing = 1 (every 1 stitch)
  Result: [inc] x6 (every stitch is an increase)

Round 3: S = 12, ΔS = 6 inc
  spacing = 2 (every 2 stitches)
  offset = (round_index % spacing) = 1
  Result: [sc, inc] x6 (pattern: sc, inc, sc, inc, ...)

Round 4: S = 18, ΔS = 6 inc
  spacing = 3 (every 3 stitches)
  offset = (round_index % spacing) = 0
  Result: [2 sc, inc] x6 (pattern: sc, sc, inc, ...)
```

---

### 13.5 Yardage Estimation

**Formula:**
```
yarn_per_stitch ≈ 0.5 cm (for single crochet, Worsted weight)
total_yardage = sum(stitches_per_round) * 0.5 cm
safety_margin = 1.10 (10% additional)
```

**Adjustment by Stitch Type:**
- sc (single): 0.5 cm/stitch
- hdc (half double): 0.7 cm/stitch
- dc (double): 0.9 cm/stitch

**Example (10 cm Sphere, sc):**
```
Rounds: 6 + 12 + 18 + ... + 6 = ~120 total stitches
Yarn: 120 * 0.5 = 60 cm = 0.6 m
With margin: 0.6 * 1.1 = 0.66 m ≈ 25 yards
```

---

## 14. UI/UX Guidelines

### 14.1 Design Principles

1. **Mobile-First:** All flows designed for 5-6" smartphone; scale up for tablet/desktop
2. **Clarity:** Simple language, visual hierarchy, whitespace
3. **Accessibility:** High contrast, large touch targets, keyboard navigation
4. **Progressively Revealing:** Advanced options hidden by default; accessible via settings
5. **Feedback:** Every action produces visual feedback (button press, loading indicator)
6. **Error Prevention:** Validation early; helpful error messages

### 14.2 Color Palette

**Primary:**
- Brand Blue: `#0066CC`
- Accent Green: `#00AA44` (increases)
- Accent Red: `#DD3333` (decreases)
- Neutral Gray: `#666666` (normal stitches)

**Semantic:**
- Success: Green (#00AA44)
- Error: Red (#DD3333)
- Warning: Orange (#FF9900)
- Info: Blue (#0066CC)

**Neutral:**
- Background: White (#FFFFFF)
- Surface: Light Gray (#F5F5F5)
- Text: Dark Gray (#333333)
- Border: Medium Gray (#CCCCCC)

**High-Contrast Mode:**
- Text: Black (#000000)
- Background: White (#FFFFFF)
- Borders: Black (#000000)

### 14.3 Typography

**Font Stack:** -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif

**Sizes:**
- H1 (Title): 32pt, weight 700
- H2 (Section): 24pt, weight 600
- H3 (Subsection): 18pt, weight 600
- Body: 16pt, weight 400
- Small: 14pt, weight 400
- Label: 12pt, weight 600

**Dyslexia-Friendly Font:** OpenDyslexic (when enabled)

### 14.4 Layout & Spacing

**Grid:** 8px base unit
- Small spacing: 8px
- Normal spacing: 16px
- Large spacing: 24px
- Extra-large spacing: 32px

**Safe Area Insets:** Respect device notches and home indicators (iOS); consistent padding top/bottom

**Touch Targets:** Minimum 48x48 dp; preferably 56x56 dp

### 14.5 Form Design

**Input Fields:**
- Height: 48px (touch-friendly)
- Padding: 12px (vertical), 16px (horizontal)
- Border: 2px solid, rounded 8px
- Focus state: Blue border + shadow
- Error state: Red border + red text hint below

**Labels:**
- Position: Above input field
- Weight: 600
- Color: Dark gray

**Buttons:**
- Height: 48px
- Padding: 16px (horizontal), 12px (vertical)
- Border radius: 8px
- Font weight: 600
- Primary: Blue background, white text
- Secondary: White background, blue border, blue text
- Disabled: Gray background, light gray text, no pointer

### 14.6 Pattern Visualization Design

**Stitch Node:**
- Diameter: 12-24px (scalable)
- Colors: Green (inc), Red (dec), Gray (normal)
- Hover: Highlight + tooltip

**Edge:**
- Stroke width: 1-2px
- Color: Light gray (#CCCCCC)
- Style: Solid

**Highlights:**
- Glow/shadow effect for highlighted nodes
- Animated pulse on first appearance

**Round Controls:**
- Buttons (Previous, Next, First, Last): 48x48 dp minimum
- Scrubber: Full width, 44px height (thumb), 8px track

### 14.7 Navigation & Flow

**Home Screen:**
- App branding/logo
- "Generate New Pattern" (primary action)
- "Recent Patterns" (if any)
- "About" and "Settings" links

**Generate Screen:**
1. Shape selection (cards with icons)
2. Parameter input (form)
3. Gauge selection (preset or custom)
4. Preview
5. Generate button

**Visualization Screen:**
- Full-width diagram with round label
- Below: Round navigation controls, current/total rounds
- Bottom drawer: "Explain This Round", stitch glossary
- Top: Settings quick-access (contrast, handedness, terms)

**Export Screen:**
- Format selection (PDF, SVG, JSON)
- Export button
- Success indicator + download link

---

## 15. Accessibility Requirements

### 15.1 WCAG AA Compliance Checklist

#### Perceivable
- [ ] Color is not the only means of conveying information (pattern symbols also used)
- [ ] All images have text alternatives (alt text on diagrams)
- [ ] Audio/video not used in MVP (N/A)
- [ ] Text is readable: min 16pt, 1.5x line height, left-aligned

#### Operable
- [ ] All functionality available via keyboard
- [ ] No keyboard traps
- [ ] Tab order is logical (top to bottom, left to right)
- [ ] Skip navigation links present
- [ ] Focus indicator visible (2px, 3:1 contrast)
- [ ] Touch targets ≥ 48x48 dp (56x56 dp preferred)
- [ ] No seizure-triggering animations (< 3 flashes per second)

#### Understandable
- [ ] Plain language (grade 5-6 reading level)
- [ ] Consistent navigation and naming
- [ ] Error messages identify problem and suggest solution
- [ ] Required fields marked clearly

#### Robust
- [ ] Valid HTML (use semantic elements: button, input, nav, main, etc.)
- [ ] Proper ARIA roles and labels
- [ ] Compatible with assistive technologies (tested on NVDA, JAWS, VoiceOver)

### 15.2 Screen Reader Testing Matrix

| Device | Browser | Status | Notes |
|--------|---------|--------|-------|
| Windows | NVDA + Chrome | TBD | Open-source; most common |
| Windows | JAWS + Chrome | TBD | Commercial; comprehensive |
| macOS | VoiceOver + Safari | TBD | Built-in; good iOS alignment |
| iOS | VoiceOver + Safari | TBD | Touch-based navigation |
| Android | TalkBack + Chrome | TBD | Touch-based navigation |

### 15.3 Colorblind Simulation Testing

Use tools like:
- [Coblis](https://www.color-blindness.com/coblis-color-blindness-simulator/)
- [Sim Daltonism](https://michelf.ca/projects/sim-daltonism/) (macOS/iOS app)
- [Chromatic Vision Simulator](https://asada.tukusi.ne.jp/cvsimulator/)

| Condition | Prevalence | Testing Status |
|-----------|-----------|-----------------|
| Protanopia (Red-Green) | ~1% male | TBD |
| Deuteranopia (Red-Green) | ~1% male | TBD |
| Tritanopia (Blue-Yellow) | ~0.001% | TBD |
| Achromatopsia (None) | ~0.001% | TBD |

---

## 16. Export Formats

### 16.1 PDF Export Structure

**Page 1 — Cover**
```
KNIT-WIT
Crochet Pattern

Sphere, 10 cm
Single Crochet, Spiral Rounds
Gauge: 14 sts/10cm, 16 rows/10cm

Generated: Nov 5, 2024
```

**Page 2 — Materials**
```
MATERIALS
Yarn: Worsted (light bulky)
Yardage: 25 meters (30 yards)
Hook: 4.0 mm
Notions: Stitch marker, fiberfill (for stuffing)

ABBREVIATIONS
sc — Single Crochet
inc — Increase (2 sc in same stitch)
dec — Decrease (single crochet 2 together)
MR — Magic Ring
slst — Slip Stitch
```

**Page 3 — Pattern**
```
PATTERN INSTRUCTIONS
Sphere, 10 cm, single crochet, spiral rounds
Gauge: 14 sts/10 cm, 16 rows/10 cm

R1: MR 6 sc (6)
R2: inc x6 (12)
R3: [sc, inc] x6 (18)
R4: [2 sc, inc] x6 (24)
... (continues for all rounds)
```

**Page 4+ — Visuals**
```
[SVG diagrams for key rounds]
Round 1  Round 2  Round 3  ...
```

### 16.2 SVG Export Format

```svg
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <title>Round 1</title>
  <defs>
    <style>
      .stitch-normal { fill: #666666; }
      .stitch-inc { fill: #00AA44; }
      .stitch-dec { fill: #DD3333; }
      .edge { stroke: #CCCCCC; fill: none; }
    </style>
  </defs>

  <!-- Edges -->
  <path class="edge" d="M 100 50 L 120 80"/>

  <!-- Stitches -->
  <circle class="stitch-normal" cx="100" cy="50" r="6"/>
  <circle class="stitch-normal" cx="120" cy="80" r="6"/>

  <!-- Labels -->
  <text x="100" y="30" text-anchor="middle" font-size="12">Round 1 (6 sts)</text>
  <text x="100" y="170" text-anchor="middle" font-size="10">Single Crochet</text>
</svg>
```

### 16.3 JSON DSL Export

See §11 for complete schema. Exported as-is.

---

## 17. Risks and Mitigations

### R1: Gauge Variance Leading to Size Mismatch

**Risk:** User's actual gauge differs from specified gauge; pattern produces wrong-sized object.
**Probability:** Medium (40% of users encounter gauge issues)
**Impact:** High (user frustration, wasted yarn)
**Mitigation:**
- Require gauge confirmation flow (user enters test swatch measurements)
- Display ±size tolerance in UI ("Expect 9.5–10.5 cm")
- Provide guidance on adjusting hook size
- Include gauge swatch pattern as future feature

---

### R2: External Pattern Text Parsing Failures

**Risk:** User pastes pattern in unsupported syntax; parse fails or produces incorrect DSL.
**Probability:** High (70% of external patterns use non-canonical syntax)
**Impact:** Medium (user can manually edit, but tedious)
**Mitigation:**
- Support only essential grammar; reject unsupported syntax with clear warnings
- Provide manual edit mode for DSL
- Gradually expand grammar based on user feedback
- Log parse failures for analysis

---

### R3: Visual Comprehension for True Beginners

**Risk:** Even with visualizations, beginners struggle to understand stitch operations.
**Probability:** Medium (new users may not understand visual metaphor)
**Impact:** Medium (learning curve, but not blockers)
**Mitigation:**
- Provide 3-5 second animations showing each stitch type
- Include "Glossary" with text definitions + diagrams
- Add "Explain This Round" narrative descriptions
- Offer Kid Mode for younger learners
- Gather feedback via surveys; iterate UI

---

### R4: Server Performance Under Load

**Risk:** If viral, high concurrent users degrade API performance.
**Probability:** Low (niche app, slow growth expected MVP phase)
**Impact:** Medium (user experience degradation)
**Mitigation:**
- Set up horizontal auto-scaling (Kubernetes or serverless)
- Cache commonly generated patterns (Redis, in-memory)
- Use CDN for static assets
- Monitor performance metrics (latency, throughput)
- Rate limiting (60 req/IP/min)

---

### R5: Cross-Platform Consistency Issues

**Risk:** Visualization renders differently on iOS vs. Android; PDF prints differently on various printers.
**Probability:** Medium (SVG rendering varies by platform)
**Impact:** Low (visual quality, but patterns still usable)
**Mitigation:**
- Test on actual iOS and Android devices (not just simulators)
- Use react-native-svg consistently; avoid platform-specific code
- Test PDF printing on 5+ printer models
- Provide PNG fallback for SVG export

---

### R6: Accessibility Gaps Despite Best Efforts

**Risk:** Some users with disabilities encounter barriers not caught in testing.
**Probability:** Medium (accessibility is complex)
**Impact:** Medium (excludes users from product)
**Mitigation:**
- Include accessibility in Definition of Done (manual QA)
- Get feedback from users with disabilities (advisory board)
- Use automated tools (Axe DevTools, WAVE) for initial screening
- Conduct regular accessibility audits
- Maintain accessibility roadmap for post-MVP improvements

---

### R7: Platform App Store Rejection (if published)

**Risk:** iOS App Store or Google Play rejects app (content, policy, or technical issues).
**Probability:** Low (low-risk app category)
**Impact:** High (distribution blocked for mobile users)
**Mitigation:**
- Review app store guidelines early
- Test on actual devices before submission
- Provide clear app description and screenshots
- Ensure privacy policy complies with store requirements
- Plan web-based fallback for initial launch

---

## 18. Dependencies and Assumptions

### 18.1 Technical Dependencies

| Dependency | Version | Purpose | Risk |
|-----------|---------|---------|------|
| Python | 3.10+ | Backend runtime | Low (stable) |
| FastAPI | 0.100+ | Web framework | Low (mature) |
| React Native | 0.73+ | Frontend framework | Medium (iOS/Android compatibility) |
| Expo | 49+ | RN tooling | Low (actively maintained) |
| Pydantic | 2.0+ | Data validation | Low (stable) |
| ReportLab | 4.0+ | PDF generation | Low (mature) |
| Pillow | 10.0+ | Image processing | Low (stable) |
| react-native-svg | 13.0+ | SVG rendering | Medium (SVG spec compliance) |

### 18.2 External Assumptions

| Assumption | Rationale | Risk |
|-----------|-----------|------|
| User has internet connection | MVP is cloud-based; no offline support | Low for MVP (future feature) |
| User gauge is accurate | Pattern correctness depends on this | Medium (user education needed) |
| Device has mid-range specs (2GB RAM+) | Target devices from 2-3 years ago | Low (conservative estimate) |
| Standard crochet terminology is known | Only basic stitches (sc, hdc, dc) in MVP | Medium (include glossary) |
| Design doesn't require real-time collaboration | MVP is single-user | Low (true for scope) |
| No legal/licensing issues with yarn brands | No e-commerce integration in MVP | Low (non-issue) |

### 18.3 Resource Assumptions

| Resource | Availability | Risk |
|----------|--------------|------|
| Design/UX resources | 0.5 FTE | Medium (limited; may constrain UI polish) |
| Backend engineering | 1 FTE | Low (primary effort) |
| Frontend engineering | 1 FTE | Low (primary effort) |
| QA/Testing | 0.25 FTE | Medium (limited accessibility testing) |
| Product/Strategy | 0.25 FTE | Low (available as needed) |
| DevOps/Infrastructure | 0.1 FTE | Low (managed cloud services) |

---

## 19. Definition of Done

### 19.1 Functional Completion

- [ ] All MVP shapes (sphere, ellipsoid, cylinder, cone) generate without error
- [ ] All stitch types (sc, hdc, dc) implemented and tested
- [ ] Pattern DSL v0.1 schema finalized and validated
- [ ] API endpoints functional and documented (Swagger/OpenAPI)
- [ ] Visualization renders per-round diagrams smoothly (60 FPS)
- [ ] Navigation controls (next, back, jump) work correctly
- [ ] Terminology toggle (US ↔ UK) applies instantly
- [ ] Handedness mirror (left/right) applies correctly
- [ ] All export formats functional (PDF, SVG, JSON)
- [ ] Text parsing works for canonical grammar
- [ ] Settings persist across sessions

### 19.2 Quality Standards

#### Performance
- [ ] Pattern generation < 200ms p95
- [ ] Visualization compile < 500ms p95
- [ ] UI responsiveness < 100ms p95
- [ ] No memory leaks (profiled on target devices)

#### Reliability
- [ ] No unhandled exceptions in production
- [ ] All error paths tested and documented
- [ ] Deterministic output (same input → same output)
- [ ] Rate limiting functional

#### Accessibility
- [ ] WCAG AA compliance verified (automated + manual audit)
- [ ] All interactive elements have ARIA labels
- [ ] Color contrast ≥ 4.5:1 (text), ≥ 3:1 (UI)
- [ ] Keyboard navigation 100% functional
- [ ] Screen reader tested (VoiceOver, NVDA, TalkBack)
- [ ] Colorblind simulation passed
- [ ] Focus indicator visible and sufficient contrast

#### Testing
- [ ] Unit test coverage ≥ 80% (backend algorithms)
- [ ] Integration tests for all API endpoints
- [ ] UI tests for key user flows (generate, visualize, export)
- [ ] Manual QA on iOS and Android devices
- [ ] Accessibility testing (automated + manual)

#### Documentation
- [ ] API documentation (OpenAPI/Swagger) complete
- [ ] Architecture ADR (Architecture Decision Records) documented
- [ ] Code comments for complex algorithms
- [ ] Setup guide for developers
- [ ] User guide/help section in-app
- [ ] README in code repository

#### Code Quality
- [ ] Code review completed for all PRs
- [ ] Linting passes (Black, ESLint, etc.)
- [ ] Type checking passes (mypy, TypeScript)
- [ ] No known security vulnerabilities (dependency audit)
- [ ] Git history clean and well-organized

### 19.3 User-Facing Completion

- [ ] Home screen displays correctly
- [ ] Generate form works end-to-end
- [ ] Visualization screen is intuitive
- [ ] Export options work and downloads function
- [ ] Settings apply correctly
- [ ] Error messages are user-friendly and actionable
- [ ] Kid Mode works and is engaging

### 19.4 Deployment Readiness

- [ ] Docker images built and tested
- [ ] Environment variables documented
- [ ] Secrets management in place
- [ ] CI/CD pipeline functional
- [ ] Staging environment passes smoke tests
- [ ] Monitoring/alerting configured
- [ ] Rollback plan documented
- [ ] Privacy policy and terms of service finalized

---

## 20. Future Roadmap (Post-MVP)

### V1.1: Extended Stitches & Techniques

**Goals:** Support additional stitch types and advanced features
**Timeline:** 2-3 months post-MVP

**Features:**
- Double Crochet (dc) stitches (if not in MVP)
- Joined rounds (vs. spiral-only)
- Stitch stranding (different yarn for marker positions)
- Per-round notes (e.g., "stuff head now")
- Gauge swatch pattern (mini pattern to test gauge)
- Magic ring alternative: chain alternatives

**Metrics:**
- User request frequency for new stitches
- Churn rate reduction

---

### V1.2: Multi-Part Assembly

**Goals:** Support generating multi-part animals (head, body, limbs)
**Timeline:** 3-4 months post-MVP

**Features:**
- Part library (presets for arms, legs, heads)
- Assembly instructions (how parts connect)
- Auto-composition (select body type + limb style → full pattern)
- Inventory management (total yarn needed for all parts)

**Metrics:**
- Completion rate of multi-part patterns
- User satisfaction with assembly clarity

---

### V1.3: Image Recognition & Custom Shapes

**Goals:** Allow users to match patterns to photos or custom shapes
**Timeline:** 4-6 months post-MVP

**Features:**
- Image to primitive fitting (photo of amigurumi → closest shape + params)
- Custom curve-based shape input (UI to draw shape; algorithm approximates)
- 3D preview (WebGL visualization)

**Metrics:**
- Accuracy of image recognition (manual evaluation)
- User adoption of image feature

---

### V2.0: Community & Marketplace

**Goals:** Enable pattern sharing and discovery
**Timeline:** 6-12 months post-MVP

**Features:**
- User accounts and authentication
- Pattern library (public/private sharing)
- Search and discovery (filter by shape, difficulty, yarn)
- Version control (keep pattern history)
- Social features (likes, comments, follows)
- In-app pattern rating/reviews
- "Remixing" (fork + modify patterns)

**Metrics:**
- Active users
- Patterns shared per user
- Engagement (views, comments, likes)
- Community growth

---

### V2.1: Advanced Colorwork

**Goals:** Support color-changing patterns (gradients, stripes, tapestry)
**Timeline:** Parallel to V2.0

**Features:**
- Gradient yarn weight transitions
- Striping patterns (regular and irregular)
- Tapestry crochet (carry yarn, color work)
- Yarn color palette UI (select colors; DSL includes color info)

**Metrics:**
- Percentage of patterns with color
- User satisfaction with color features

---

### V3.0: Industry Integrations

**Goals:** B2B integrations with yarn brands, pattern publishers, educators
**Timeline:** 12+ months post-MVP

**Features:**
- Yarn brand API integration (real yarn recommendations)
- E-commerce partnership (affiliate links for yarn)
- Bulk pattern export (for publishers)
- Educational accounts (classroom management)
- API for third-party developers

**Metrics:**
- Number of integrations
- Revenue from partnerships
- Educator sign-ups

---

### Accessibility Roadmap (Continuous Improvement)

- **Immediate (MVP):** WCAG AA compliance, keyboard nav, screen reader
- **V1.1:** Voice control for navigation (voice commands)
- **V1.2:** Real-time collaboration (for accessibility-focused use cases)
- **V2.0+:** Braille output, alternative diagram formats, customizable sensory modes

---

## Appendix A: Glossary of Crochet Terms (for reference)

| Term | Abbreviation | Description |
|------|--------------|-------------|
| Single Crochet (US) | sc | Basic stitch; short and dense |
| Double Crochet (UK) | dc | Same as US sc; UK terminology |
| Half Double Crochet | hdc | Medium-height stitch |
| Double Crochet (US) | dc | Taller stitch than hdc |
| Increase | inc | 2 stitches in same loop; adds 1 stitch |
| Decrease | dec | Join 2 stitches; subtracts 1 stitch |
| Slip Stitch | slst | Joining stitch; minimal height |
| Chain | ch | Foundation stitch |
| Magic Ring | MR | Adjustable loop to start in the round |
| Gauge | — | Stitches and rows per 10cm; affects finished size |
| Round | R | One complete loop around an object |
| Row | Row | One pass (flat work); contrast to rounds |
| Spiral Rounds | — | Continuous rounds without joining (RN) |
| Joined Rounds | — | Close each round with slip stitch; start new round (JR) |

---

## Appendix B: Example Pattern Output (10 cm Sphere)

### Human-Readable Pattern (US, Spiral)

```
KNIT-WIT GENERATED PATTERN
Object: Sphere
Diameter: 10 cm
Stitch: Single Crochet (sc)
Rounds: Spiral (continuous)
Gauge: 14 stitches per 10 cm, 16 rows per 10 cm
Yarn Needed: ~25 meters / 30 yards (Worsted weight)

ABBREVIATIONS
sc – Single Crochet
inc – Increase (2 sc in same stitch)
dec – Decrease (single crochet 2 together)
MR – Magic Ring

INSTRUCTIONS
R1:  MR 6 sc (6)
R2:  inc x6 (12)
R3:  [sc, inc] x6 (18)
R4:  [2 sc, inc] x6 (24)
R5:  [3 sc, inc] x6 (30)
R6:  [4 sc, inc] x6 (36)
R7:  [5 sc, inc] x6 (42)
R8:  [6 sc, inc] x6 (48)
R9–R10: sc around (48)
R11: [6 sc, dec] x6 (42)
R12: [5 sc, dec] x6 (36)
R13: [4 sc, dec] x6 (30)
R14: [3 sc, dec] x6 (24)
R15: [2 sc, dec] x6 (18)
R16: [sc, dec] x6 (12)
R17: dec x6 (6)
Fasten off, weave in ends.

NOTES
• Use a stitch marker to mark the beginning of each round.
• Stuff with fiberfill as you crochet (recommended after R9).
• Adjust hook size if finished measurements don't match (test with a swatch).
```

---

## Appendix C: Acceptance Criteria Summary Table

For quick reference, all acceptance criteria from §7:

| Feature | AC Code | Criterion | Target |
|---------|---------|-----------|--------|
| **Pattern Generation** | AC-G-01.1 | Input validation | All numeric fields reject invalid input |
| | AC-G-01.2 | Required fields | Form cannot submit without shape/dimension/gauge |
| | AC-G-02.1 | Sphere accuracy | Equator count within ±1 stitch of theoretical |
| | AC-G-02.4 | Cone distribution | No stacked inc/dec columns |
| | AC-E-01.1 | PDF generation | PDF generates without error |
| | AC-E-02.1 | SVG validity | SVG validates against SVG schema |
| **Visualization** | AC-V-01.1 | Round compilation | Every round compiles without error |
| | AC-V-02.3 | FPS performance | 60 FPS p95 on target devices |
| | AC-V-03.1 | Touch targets | All buttons ≥ 48x48 dp |
| | AC-V-05.1 | Term translation | All labels update accurately |
| **Accessibility** | AC-A-02.1 | Color contrast | Text ≥ 4.5:1 |
| | AC-A-02.3 | Keyboard nav | All features accessible via keyboard |
| | AC-K-01.1 | Kid Mode copy | Grade 4–5 reading level |

---

## Appendix D: API Request/Response Examples

See §12 for full API specification. Quick reference examples:

### Generate Request
```bash
curl -X POST https://api.knit-wit.com/v1/patterns/generate \
  -H "Content-Type: application/json" \
  -d '{
    "object": {"type":"sphere","params":{"diameter":10}},
    "meta": {"units":"cm","terms":"US","stitch":"sc","round_mode":"spiral","gauge":{"sts_per_10cm":14,"rows_per_10cm":16}},
    "materials": {"yarn_weight":"Worsted","hook_size_mm":4.0}
  }'
```

### Visualize Request
```bash
curl -X POST https://api.knit-wit.com/v1/patterns/visualize \
  -H "Content-Type: application/json" \
  -d '{
    "pattern": {
      "dsl": { ... },
      "render_options": {"handedness":"right","contrast":"normal","terms":"US"}
    }
  }'
```

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | Oct 2024 | Initial Team | Initial PRD (scope-focused) |
| 0.5 | Oct 2024 | Architects | Algorithm details; API spec |
| 1.0 | Nov 2024 | Documentation | Refined, production-ready PRD |

---

**End of Document**

This PRD is the single source of truth for Knit-Wit MVP development. For questions or clarifications, please open an issue in the project repository or contact the product team.
