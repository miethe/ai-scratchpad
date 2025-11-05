# PRD — Crochet Pattern Generator & Visualizer (MVP)

## 0) Summary

**Problem:** Writing and reading crochet patterns—especially for amigurumi and geometric objects—is tedious for beginners and time-consuming for experts.
**Solution (MVP):** A mobile-first web app that (1) generates clean crochet patterns for geometric shapes from user parameters, and (2) visualizes any supported pattern as an interactive, step-by-step guide with simple renderings. Targeted at hobbyists of all levels; kid-friendly.

**Core functions**

1. **Geometric Pattern Generation:** Spheres, ellipsoids, cylinders, cones/tapered limbs; user enters dimensions + gauge → app outputs pattern set (text + rounds table) and a simple rendering.
2. **Pattern Visualization:** Ingest our generated pattern (or paste a supported text pattern) → render an interactive visual guide per round/row with beginner hints.

**Stack (aligned with your norms):**

* **Frontend:** React Native (Expo), react-native-svg (or Skia) for charts/diagrams
* **Backend:** Python + FastAPI
* **Engine/Lib:** Python module (“pattern-compiler”) used by FastAPI
* **Data:** JSON Pattern DSL v0.1; static asset renders as SVG/PNG; optional PDF export

---

## 1) Goals & Non-Goals

### Goals (MVP)

* Generate **accurate, beginner-friendly** crochet patterns for geometric shapes using user-provided **gauge** and dimensions.
* Provide **interactive visualization**: per-round diagrams, stitch highlights, and short tooltips.
* Produce **shareable outputs**: pattern text (US/UK terms), printable PDF, SVG diagram(s).
* Ensure **mobile-first UX** and **kid mode** (larger tap targets, simplified wording, color hints).

### Non-Goals (MVP)

* Free-form shape solving from arbitrary 3D meshes (future).
* Advanced colorwork authorship (beyond simple single-color or later basic stripes).
* Community marketplace / social features.
* Automatic yarn brand recommendations or e-commerce integrations.

---

## 2) Target Users & Personas

* **Beginner Becky (age 12–60):** Wants “type what I want → get a pattern I can follow.” Needs visuals, glossaries, and reassurance.
* **Intermediate Ivy:** Comfortable with sc/hdc/dc, needs fast parametric patterns and clean charts.
* **Expert Eli:** Wants precise control of gauge/terminology and exports to reuse/modify.
* **Parent/Teacher Pat:** Uses “Kid Mode” to teach. Needs clarity and safety notes.

Accessibility must be first-class: clear color contrast, optional left/right-handed diagram mirroring, togglable text size, and dyslexia-friendly font option.

---

## 3) MVP Use Cases

* **UC-G1:** Generate a 10 cm sphere in single crochet (US terms), spiral rounds, produce pattern + diagram.
* **UC-G2:** Generate a tapered limb (cone) given base diameter, tip diameter, and length.
* **UC-V1:** Visualize a provided pattern (our DSL or a paste using supported syntax) round-by-round with highlights.
* **UC-V2:** Toggle US↔UK terms and left↔right-handed orientation and see the visualization update.
* **UC-X1:** Export a PDF (pattern text + first page visuals) and download SVGs.

---

## 4) Functional Requirements

### F1 — Pattern Generation (Geometric)

* Shapes: **sphere, ellipsoid, cylinder (with optional end caps), cone/tapered cylinder**.
* Inputs per shape: dimensions (cm), stitch type (sc/hdc initially), gauge (sts/10 cm, rows/10 cm), rounds mode (spiral vs joined), terms (US/UK).
* Outputs: **Pattern DSL v0.1**, human-readable pattern text, per-round table, simple rendering (SVG), yarn yardage estimate.
* Algorithms: evenly distribute increases/decreases per round (modular spacing), curvature-approx rules (see §9).

### F2 — Pattern Visualization

* Input: Pattern DSL v0.1 (preferred) or pasted text in supported syntax (US/UK).
* Render: per-round diagram with stitch nodes and color-coded **inc/dec**, cursor for “current stitch,” and tooltips (e.g., “inc = 2 sc in same st”).
* Controls: step forward/back, jump to round, toggle terms, mirror handedness, enlarge text, high-contrast mode.

### F3 — Internationalization

* US/UK terminology toggle with **automated translation layer** (e.g., sc↔dc mapping).
* Units: cm default; inches shown as secondary on demand.

### F4 — Exports

* **PDF** (brandable cover, materials, abbreviations, pattern, visuals page).
* **SVG/PNG** diagrams.
* **JSON DSL** for reuse.

### F5 — Kid Mode

* Bigger tap targets, simplified copy, animated “this is what an increase looks like,” and safe color palette.

---

## 5) Non-Functional Requirements

* **Performance:** Generate a sphere < 200 ms server-side; visualize any round < 50 ms client-side after data load.
* **Reliability:** Deterministic output for same inputs.
* **Security & Privacy:** No PII. Patterns are user-owned; no public listing in MVP.
* **Accessibility:** WCAG AA contrast, voice-over labels for controls, haptics for step-advance.
* **Mobile-first:** All flows work smoothly on iPhone/Android mid-range devices.

---

## 6) System Architecture (MVP)

* **Monorepo**: RN app + FastAPI service + shared “pattern-compiler” Python package.
* **Frontend (RN/Expo):**

  * Screens: Home, Generate, Visualization, Exports, Settings.
  * Rendering via **react-native-svg** (fallback to PNG export).
* **Backend (FastAPI):**

  * `/patterns/generate` → compile DSL + assets
  * `/patterns/visualize` → normalize input → return render primitives
  * `/patterns/parse-text` → (scope-limited) transform supported text to DSL
  * `/export/pdf` → assemble pattern + diagrams
* **Storage:** Stateless in MVP; assets streamed; optional ephemeral temp storage (S3-compatible later).

---

## 7) Pattern DSL v0.1 (JSON)

### 7.1 JSON Schema (abridged)

```json
{
  "meta": {
    "version": "0.1",
    "units": "cm",
    "terms": "US",
    "stitch": "sc",
    "round_mode": "spiral",
    "gauge": { "sts_per_10cm": 14, "rows_per_10cm": 16 }
  },
  "object": {
    "type": "sphere", 
    "params": { "diameter": 10 }
  },
  "rounds": [
    { "r": 1, "ops": [{"op":"MR","count":1},{"op":"sc","count":6}], "stitches": 6 },
    { "r": 2, "ops": [{"op":"inc","repeat":6}], "stitches": 12 },
    { "r": 3, "ops": [{"op":"seq","pattern":["sc",1,"inc"], "repeat":6}], "stitches": 18 }
  ],
  "materials": {
    "yarn_weight": "Worsted",
    "hook_size_mm": 4.0,
    "yardage_estimate": 25
  },
  "notes": ["Work in a spiral; use a stitch marker."]
}
```

**Op vocabulary (MVP):** `MR` (magic ring), `sc`, `hdc` (planned), `inc`, `dec`, `slst`, `ch`, `seq` (patterned sequences), `repeat`.
**Round object:** `r` (index), `ops` (ordered), `stitches` (post-round count).
**Handedness:** front-end rendering flag; DSL remains neutral.

---

## 8) API (FastAPI) — MVP Endpoints

### POST `/patterns/generate`

**Body**

```json
{
  "object": {"type":"sphere","params":{"diameter":10}},
  "meta": {
    "units":"cm","terms":"US","stitch":"sc","round_mode":"spiral",
    "gauge":{"sts_per_10cm":14,"rows_per_10cm":16}
  },
  "materials": {"yarn_weight":"Worsted","hook_size_mm":4.0}
}
```

**Response**

```json
{
  "dsl": { ... }, 
  "assets": {
    "diagram_svg": "<svg>...</svg>",
    "preview_png": "data:image/png;base64,..."
  },
  "exports": {
    "pdf_available": true
  }
}
```

### POST `/patterns/visualize`

**Body**

```json
{ "pattern": { "dsl": { ... } , "render_options": {
  "handedness":"right","contrast":"high","terms":"UK"
}}}
```

**Response**

```json
{
  "frames": [
    { "round":1, "nodes":[{"id":1,"type":"sc","x":...,"y":...}], "edges":[...] },
    { "round":2, "nodes":[...], "highlights":[{"op":"inc","at":[3,9,15,21,27,33]}] }
  ]
}
```

### POST `/patterns/parse-text` (scoped)

* Accepts simplified US/UK lines like `R4: [2 sc, inc] x6 (24)` → returns DSL.
* MVP supports a **limited grammar**; unknown tokens return warnings + partial parse.

### POST `/export/pdf`

* Accepts DSL + selected assets → returns PDF (stream).

---

## 9) Algorithms (MVP)

* **Gauge mapping:**

  * ( g_s ) = sts/10 cm, ( g_r ) = rows/10 cm.
* **Flat disc inc/round estimate (sc):**

  * ( I \approx \text{round}(2\pi \cdot g_s / g_r) ) → typically 6.
* **Sphere:**

  * Rounds to equator ( k_{eq} \approx \text{round}(g_r \cdot (D/2) / 10) ).
  * Increase by (I) per round to (S_{eq}), optional steady rounds, mirror decreases.
* **Cylinder:**

  * Cap = half-sphere (increase/decrease to radius); body = **constant stitch count** for height (H) with ( \text{round}(g_r \cdot H / 10) ) rows.
* **Cone/tapered limb:**

  * Linear taper from (S_0) to (S_1) across (K) rounds; distribute ±1 deltas using Bresenham-like spacing to avoid stacking (modular spread).
* **Even distribution:**

  * For ΔS increases on stitch count S, place increases roughly every ⌊S/ΔS⌋ stitches; jitter start offset by round index to avoid columns.

---

## 10) UI/UX (MVP)

* **Generate Flow:** Shape → Params → Gauge → Preview → Pattern.
* **Visualization Screen:** round scrubber, big Next/Back, color legend (green=inc, red=dec), tap on a stitch to see tooltip; “Explain this round” drawer.
* **Kid Mode:** simplified terms (“Add two in one stitch”), mascot hints, large controls.
* **Settings:** units, US/UK, handedness, text size, colorblind palettes.

---

## 11) Acceptance Criteria (high-level)

* **AC-G-1:** Generating a 10 cm sphere with gauge 14/16 (US sc, spiral) yields a pattern whose equator stitch count equals computed (S_{eq}) and visual shows 6 evenly spaced increase spokes.
* **AC-G-2:** Tapered limb from 6 cm→2 cm over 8 cm results in monotonic stitch deltas with no stacked increase/decrease columns.
* **AC-V-1:** Pasting `R4: [2 sc, inc] x6 (24)` produces a round with 6 inc highlights; total count 24.
* **AC-V-2:** Switching US↔UK updates labels without changing stitch geometry.
* **AC-A11y-1:** All controls have accessible labels; color-only signals have text equivalents.

---

## 12) Risks & Mitigations

* **R1: Gauge variance → shape drift.**
  Mitigation: force gauge confirmation flow; show ±size tolerance; “Adjust hook if off.”
* **R2: Parsed external text variance.**
  Mitigation: MVP supports a minimal grammar + friendly error reporting + manual edit mode.
* **R3: Visual comprehension for true beginners.**
  Mitigation: add “What is an increase?” micro-animations and glossary links.

---

## 13) Telemetry (privacy-respecting)

* Count of shape generations, parse success rate, visualization step engagement, export usage, common gauges (anonymized, no PII). Opt-in toggle at first run.

---

## 14) Roadmap Beyond MVP (brief)

* V1.1: HDC/DC stitches; joined rounds; stripes; per-round stuffing/eye placement cues.
* V1.2: Primitive assemblies (auto animal generator), ears/limbs presets.
* V1.3: Photo-to-primitive fit; param capture per part; multi-part assembly instructions.

---

## 15) Initial Backlog (EPICs → stories)

**EPIC A — Pattern Engine (Python)**

* A1: Implement sphere compiler (sc, spiral)
* A2: Implement cylinder + caps
* A3: Implement cone/tapered limb with Bresenham spacing
* A4: Yardage estimator (per-stitch length × count)
* A5: US↔UK translator and round join mode scaffolding

**EPIC B — Visualization**

* B1: DSL→render primitives (nodes/edges/highlights)
* B2: RN SVG renderer with round scrubber
* B3: Tooltips + kid mode copy + accessibility options
* B4: Left-handed mirror & high-contrast theme

**EPIC C — Parsing & I/O**

* C1: Text→DSL parser for limited grammar
* C2: PDF exporter (pattern + diagrams)
* C3: Asset packaging (SVG/PNG)

**EPIC D — App Shell**

* D1: Screens + navigation + settings
* D2: Form validation for inputs (units, gauge)
* D3: Telemetry (opt-in) and error reporting

---

## 16) Example Outputs

### 16.1 Generated Pattern (human text, US)

```
Sphere, 10 cm, sc in spiral, Gauge 14 sts/10 cm, 16 rows/10 cm
R1: MR 6 sc (6)
R2: inc x6 (12)
R3: [sc, inc] x6 (18)
R4: [2 sc, inc] x6 (24)
R5: [3 sc, inc] x6 (30)
R6: [4 sc, inc] x6 (36)
R7: [5 sc, inc] x6 (42)
R8: [6 sc, inc] x6 (48)
R9–10: sc around (48)
R11: [6 sc, dec] x6 (42)
R12: [5 sc, dec] x6 (36)
R13: [4 sc, dec] x6 (30)
R14: [3 sc, dec] x6 (24)
R15: [2 sc, dec] x6 (18)
R16: [sc, dec] x6 (12)
R17: dec x6 (6) — close
```

### 16.2 Visualization Frame (concept)

```json
{
  "round": 5,
  "legend": {"sc":"normal","inc":"increase"},
  "nodes":[{"id":1,"type":"sc","x":0.92,"y":0.12}, ...],
  "highlights":[{"type":"inc","indices":[6,12,18,24,30,36]}]
}
```

---

## 17) Definition of Done (MVP)

* Shapes: sphere, cylinder (+caps), cone/tapered cylinder implemented and tested.
* Visualization reliably renders at least 50 rounds with smooth stepping.
* Parser correctly ingests the canonical bracket/repeat syntax for sc patterns.
* PDF export passes print test (A4/Letter) and mobile view test.
* Accessibility checks pass (labels, contrast, voice-over).
* Smoke tests on iOS and Android (recent devices).

---

## 18) Open Questions (track in issues)

* Which secondary stitches (hdc/dc) make the cut for MVP vs V1.1?
* Include joined rounds at MVP or defer?
* Do we ship a small baked-in gauge preset library for common yarn weights?
