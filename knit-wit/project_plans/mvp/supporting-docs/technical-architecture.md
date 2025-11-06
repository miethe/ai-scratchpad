# Knit-Wit MVP — Technical Architecture Details

**Document Version:** 1.0
**Last Updated:** November 2024
**Status:** Active Development
**Owner:** Development Team

**Related Documents:**
- [Product Requirements Document](../prd.md)
- [Implementation Plan](../implementation-plan.md)

---

## Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Repository Structure](#repository-structure)
4. [Frontend Architecture](#frontend-architecture)
5. [Backend Architecture](#backend-architecture)
6. [Pattern Engine Architecture](#pattern-engine-architecture)
7. [Data Models](#data-models)
8. [API Design](#api-design)
9. [Security Architecture](#security-architecture)
10. [Performance Considerations](#performance-considerations)
11. [Technology Choices Rationale](#technology-choices-rationale)

---

## Overview

### Architecture Philosophy

Knit-Wit MVP follows a **clean, layered architecture** designed for:

- **Separation of Concerns**: Pattern generation logic is decoupled from API and UI layers
- **Testability**: Core algorithms are testable independently of framework code
- **Extensibility**: New shapes and stitch types can be added without modifying existing code
- **Portability**: Pattern engine is a standalone Python library usable beyond the web API
- **Mobile-First**: Frontend architecture optimizes for touch, small screens, and offline capability

### Design Principles

1. **Simple Over Complex**: Choose straightforward solutions; avoid premature optimization
2. **API-First Design**: Backend exposes clean REST API; frontend is a client among potential others
3. **Accessibility by Default**: WCAG AA compliance is baked into component design, not added later
4. **Stateless Backend**: No database in MVP; patterns are generated on-demand and ephemeral
5. **Monorepo Benefits**: Shared types, unified CI/CD, atomic cross-repository changes
6. **Progressive Enhancement**: Core features work without JavaScript; visualizations enhance experience

### Cross-Document Navigation

This document provides **technical implementation details** extracted from the [Implementation Plan](../implementation-plan.md). For:

- **Product requirements and user stories**: See [PRD](../prd.md)
- **Sprint planning and timelines**: See [Implementation Plan](../implementation-plan.md) sections 4-7
- **Testing strategy and DevOps**: See [Implementation Plan](../implementation-plan.md) sections 8-9

---

## System Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         User (Mobile/Web)                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTPS
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  React Native / Expo App                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Screens    │  │  Components  │  │ State (Zustand) │       │
│  │  - Home      │  │  - Forms     │  │  - Pattern     │        │
│  │  - Generate  │  │  - SVG Viz   │  │  - UI State    │        │
│  │  - Visualize │  │  - Controls  │  │                │         │
│  │  - Export    │  │              │  │                │         │
│  └──────┬───────┘  └──────────────┘  └──────────────┘          │
│         │                                                        │
│         │ API Client (axios/fetch)                               │
└─────────┼────────────────────────────────────────────────────────┘
          │
          │ REST API (JSON)
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                             │
│  ┌──────────────────────────────────────────────────┐           │
│  │              API Routes Layer                     │           │
│  │  /api/v1/patterns/generate                       │           │
│  │  /api/v1/patterns/visualize                      │           │
│  │  /api/v1/export/{pdf,svg}                        │           │
│  └────────────────┬─────────────────────────────────┘           │
│                   │                                              │
│  ┌────────────────▼─────────────────────────────────┐           │
│  │           Services Layer                         │           │
│  │  - Request validation (Pydantic)                 │           │
│  │  - Business logic orchestration                  │           │
│  │  - Error handling & logging                      │           │
│  └────────────────┬─────────────────────────────────┘           │
│                   │                                              │
│                   │ Calls                                        │
│                   ▼                                              │
└───────────────────┼──────────────────────────────────────────────┘
                    │
                    │ Python Import
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│              Pattern Engine Library (Python)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Compiler   │  │    Shapes    │  │  Algorithms  │          │
│  │ - Factory    │  │  - Sphere    │  │  - Gauge     │          │
│  │ - DSL Gen    │  │  - Cylinder  │  │  - Distribution          │
│  │              │  │  - Cone      │  │  - Yardage   │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                  │                  │                  │
│         └──────────────────┴──────────────────┘                  │
│                            │                                     │
│  ┌─────────────────────────▼────────────────────────┐           │
│  │            DSL Output (JSON)                     │           │
│  │  - Meta (gauge, units, terms)                    │           │
│  │  - Object (shape type, params)                   │           │
│  │  - Rounds (operations, stitch counts)            │           │
│  │  - Materials (yarn, hook, yardage)               │           │
│  └──────────────────────────────────────────────────┘           │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐                             │
│  │  Rendering   │  │   Parsing    │                             │
│  │ - Visualizer │  │ - Text→DSL   │                             │
│  │ - Primitives │  │ - Grammar    │                             │
│  └──────────────┘  └──────────────┘                             │
└─────────────────────────────────────────────────────────────────┘
```

### Component Interactions

**Pattern Generation Flow:**

```
User Input (Form)
    ↓
Frontend Validation
    ↓
POST /api/v1/patterns/generate
    ↓
FastAPI Route Handler
    ↓
Pydantic Request Validation
    ↓
Service Layer
    ↓
PatternCompiler.compile()
    ↓
Shape-Specific Compiler (Sphere/Cylinder/Cone)
    ↓
Algorithms (gauge mapping, distribution, yardage)
    ↓
PatternDSL Object (JSON)
    ↓
Response (DSL + metadata)
    ↓
Frontend State Update
    ↓
Render Preview
```

**Visualization Flow:**

```
PatternDSL (from generation or storage)
    ↓
POST /api/v1/patterns/visualize
    ↓
Visualizer.dsl_to_frames()
    ↓
For each round:
  - Parse stitch operations
  - Calculate node positions (circular layout)
  - Generate edges (stitch connections)
  - Identify highlights (inc/dec)
    ↓
RenderFrame[] (array of visualization frames)
    ↓
Frontend receives frames
    ↓
react-native-svg renders current frame
    ↓
User navigates rounds (scrubber control)
```

### Data Flow

1. **Input → Generation**
   - User provides: shape type, dimensions, gauge
   - Compiler produces: DSL JSON
   - Response includes: pattern text, materials list, metadata

2. **DSL → Visualization**
   - DSL sent to visualizer
   - Produces: array of frame objects (nodes, edges, highlights)
   - Frontend renders frame-by-frame

3. **DSL → Export**
   - DSL + user preferences (terms, handedness)
   - Export service generates: PDF, SVG, or JSON
   - Returns downloadable asset URL or base64-encoded data

---

## Repository Structure

### Monorepo Layout

```
knit-wit/
├── apps/
│   ├── mobile/                    # React Native / Expo app
│   │   ├── src/
│   │   │   ├── screens/           # Home, Generate, Visualization, Settings
│   │   │   ├── components/        # Reusable UI components
│   │   │   ├── services/          # API client, auth, storage
│   │   │   ├── context/           # Global state (React Context or Zustand)
│   │   │   ├── hooks/             # Custom hooks
│   │   │   ├── utils/             # Helpers
│   │   │   ├── theme/             # Colors, fonts, accessibility
│   │   │   └── App.tsx            # Entry point
│   │   ├── __tests__/             # Jest tests
│   │   ├── .eslintrc.js
│   │   ├── jest.config.js
│   │   ├── app.json               # Expo config
│   │   ├── package.json
│   │   └── tsconfig.json
│   │
│   └── api/                       # FastAPI backend
│       ├── app/
│       │   ├── api/
│       │   │   ├── routes/        # Routers: /patterns, /export, /health
│       │   │   ├── models/        # Pydantic models (request/response)
│       │   │   ├── schemas/       # API schemas
│       │   │   └── deps.py        # Dependencies (auth, validation)
│       │   ├── core/
│       │   │   ├── config.py      # Settings (env vars)
│       │   │   ├── security.py    # Auth, CORS
│       │   │   └── constants.py   # Shared constants
│       │   ├── services/          # Business logic (calls pattern_engine)
│       │   ├── middleware/        # Logging, error handling
│       │   ├── main.py            # FastAPI app initialization
│       │   └── __init__.py
│       ├── tests/
│       │   ├── conftest.py        # pytest fixtures
│       │   ├── unit/              # Unit tests
│       │   ├── integration/       # API tests
│       │   └── fixtures/          # Test data
│       ├── Dockerfile             # Multi-stage build
│       ├── requirements.txt
│       ├── pyproject.toml         # Poetry or setuptools config
│       ├── .env.example
│       └── main.py                # Entry point
│
├── packages/
│   └── pattern-engine/            # Shared Python library
│       ├── knit_wit_engine/
│       │   ├── __init__.py
│       │   ├── compiler.py        # Main compiler entry point
│       │   ├── dsl.py             # DSL models (Pydantic)
│       │   ├── shapes/
│       │   │   ├── __init__.py
│       │   │   ├── sphere.py      # Sphere generation logic
│       │   │   ├── cylinder.py    # Cylinder + caps
│       │   │   ├── cone.py        # Cone/tapered shapes
│       │   │   └── base.py        # Abstract base class
│       │   ├── algorithms/
│       │   │   ├── __init__.py
│       │   │   ├── gauge.py       # Gauge mapping
│       │   │   ├── distribution.py # Increase/decrease spacing (Bresenham)
│       │   │   ├── yardage.py     # Yarn estimation
│       │   │   └── translator.py  # US ↔ UK translation
│       │   ├── rendering/
│       │   │   ├── __init__.py
│       │   │   ├── primitives.py  # Node, edge, highlight data classes
│       │   │   ├── visualizer.py  # DSL → render primitives
│       │   │   └── styles.py      # Color palettes, defaults
│       │   ├── parsing/
│       │   │   ├── __init__.py
│       │   │   ├── text_parser.py # Text → DSL converter
│       │   │   └── grammar.py     # BNF-like grammar definition
│       │   └── utils/
│       │       ├── __init__.py
│       │       └── math.py        # Geometric helpers
│       ├── tests/
│       │   ├── conftest.py
│       │   ├── unit/
│       │   ├── integration/
│       │   └── fixtures/
│       ├── setup.py
│       ├── pyproject.toml
│       ├── requirements.txt
│       └── README.md
│
├── docs/
│   ├── api/                       # API documentation
│   ├── architecture/              # Architecture docs (this file)
│   ├── frontend/                  # Component library, accessibility
│   └── deployment/                # Setup, CI/CD, monitoring
│
├── .github/
│   └── workflows/                 # CI/CD pipelines
│
├── docker-compose.yml             # Local dev environment
├── pnpm-workspace.yaml            # Monorepo management
├── package.json                   # Root package.json
└── README.md
```

### File Organization Rationale

**Apps vs. Packages:**
- `apps/` contains deployable applications (mobile app, API server)
- `packages/` contains shared libraries used by multiple apps
- Pattern engine is a package because it may be used by future CLIs, desktop apps, or integrations

**Feature-Based Frontend Structure:**
- Each screen has its own folder with components, reducing coupling
- Shared components live in `components/` at app root
- Services abstract API communication and storage logic

**Layered Backend Structure:**
- `routes/` handles HTTP (request parsing, response formatting)
- `services/` contains business logic (orchestrates pattern engine calls)
- `pattern_engine` package is pure Python logic with no FastAPI dependencies

### Naming Conventions

- **Python**: `snake_case` for files, functions, variables; `PascalCase` for classes
- **TypeScript/JavaScript**: `camelCase` for variables/functions; `PascalCase` for components/classes
- **Files**: Component files match component name (`HomeScreen.tsx`), utilities use descriptive names (`math.py`)
- **API Routes**: Kebab-case (`/api/v1/patterns/generate`)

---

## Frontend Architecture

### Technology Stack

| Technology | Version | Purpose |
|-----------|---------|---------|
| React Native | 0.73+ | Mobile framework |
| Expo SDK | 51+ | Build tooling, native APIs |
| TypeScript | 5.x | Type safety |
| Zustand | 4.x | Lightweight state management |
| React Navigation | 6+ | Screen navigation |
| react-native-svg | 14+ | SVG rendering for visualizations |
| axios | 1.x | HTTP client |
| Jest | 29+ | Unit testing |
| React Native Testing Library | 12+ | Component testing |

### Architecture Pattern: Feature-Based Organization

```
screens/
├── HomeScreen.tsx              # Landing + main menu
├── GenerateScreen/
│   ├── GenerateScreen.tsx      # Wizard: Shape → Params → Gauge → Review
│   ├── ShapeSelector.tsx
│   ├── ParamsForm.tsx
│   ├── GaugeConfirm.tsx
│   └── PreviewCard.tsx
├── VisualizationScreen/
│   ├── VisualizationScreen.tsx # Main visualization controller
│   ├── PatternFrame.tsx        # Single round view
│   ├── RoundScrubber.tsx       # Navigation slider
│   ├── StitchTooltip.tsx
│   ├── LegendOverlay.tsx       # Color key
│   ├── ExplainDrawer.tsx       # Round explanation
│   └── VisualizationRenderer.tsx
├── ExportScreen/
│   ├── ExportScreen.tsx        # Choose format + download
│   ├── PDFPreview.tsx
│   └── ShareCard.tsx
└── SettingsScreen/
    ├── SettingsScreen.tsx      # Preferences
    ├── AccessibilitySettings.tsx
    ├── UnitsToggle.tsx
    └── KidModeToggle.tsx
```

### State Management (Zustand)

**Pattern Store:**
```typescript
// stores/patternStore.ts
interface PatternStore {
  pattern: Pattern | null;
  setPattern: (pattern: Pattern) => void;
  generatePattern: (params: GenerateRequest) => Promise<void>;
  isLoading: boolean;
  error: string | null;
}
```

**UI Store:**
```typescript
// stores/uiStore.ts
interface UIStore {
  currentRound: number;
  setCurrentRound: (round: number) => void;
  selectedStitch: Stitch | null;
  setSelectedStitch: (stitch: Stitch | null) => void;
  kidMode: boolean;
  toggleKidMode: () => void;
  handedness: 'right' | 'left';
  setHandedness: (hand: 'right' | 'left') => void;
  terms: 'US' | 'UK';
  setTerms: (terms: 'US' | 'UK') => void;
  units: 'cm' | 'in';
  setUnits: (units: 'cm' | 'in') => void;
}
```

**Why Zustand:**
- Lightweight (< 1KB)
- No boilerplate compared to Redux
- Built-in TypeScript support
- Simple async action handling
- Persist middleware for settings

### Navigation Structure

```typescript
// App.tsx navigation setup
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const Stack = createNativeStackNavigator();

function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Generate" component={GenerateScreen} />
        <Stack.Screen name="Visualize" component={VisualizationScreen} />
        <Stack.Screen name="Export" component={ExportScreen} />
        <Stack.Screen name="Settings" component={SettingsScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

### Component Hierarchy

```
App
├── NavigationContainer
│   ├── HomeScreen
│   ├── GenerateScreen
│   │   ├── ShapeSelector
│   │   ├── ParamsForm
│   │   ├── GaugeConfirm
│   │   └── PreviewCard
│   ├── VisualizationScreen
│   │   ├── PatternFrame
│   │   │   └── VisualizationRenderer (SVG)
│   │   ├── RoundScrubber
│   │   ├── StitchTooltip
│   │   ├── LegendOverlay
│   │   └── ExplainDrawer
│   ├── ExportScreen
│   │   ├── PDFPreview
│   │   └── ShareCard
│   └── SettingsScreen
│       ├── AccessibilitySettings
│       ├── UnitsToggle
│       └── KidModeToggle
└── Global State (Zustand Stores)
```

### SVG Rendering Approach

**Visualization uses react-native-svg:**

```typescript
// components/VisualizationRenderer.tsx
import Svg, { Circle, Line, Path, Text } from 'react-native-svg';

interface RenderFrame {
  nodes: Node[];
  edges: Edge[];
  highlights: Highlight[];
}

function VisualizationRenderer({ frame }: { frame: RenderFrame }) {
  return (
    <Svg width={width} height={height}>
      {/* Edges (stitch connections) */}
      {frame.edges.map(edge => (
        <Line
          key={edge.id}
          x1={edge.from.x}
          y1={edge.from.y}
          x2={edge.to.x}
          y2={edge.to.y}
          stroke="#888"
          strokeWidth={2}
        />
      ))}

      {/* Nodes (stitches) */}
      {frame.nodes.map(node => (
        <Circle
          key={node.id}
          cx={node.x}
          cy={node.y}
          r={8}
          fill={getNodeColor(node.type)}
          onPress={() => handleStitchPress(node)}
        />
      ))}

      {/* Highlights (inc/dec indicators) */}
      {frame.highlights.map(hl => (
        <Circle
          key={hl.id}
          cx={hl.x}
          cy={hl.y}
          r={12}
          fill="none"
          stroke={hl.color}
          strokeWidth={3}
        />
      ))}
    </Svg>
  );
}
```

### Key Libraries and Rationale

- **Expo**: Simplifies native builds, provides polyfills, fast iteration
- **react-native-svg**: Performant vector graphics, touch support
- **Zustand**: Minimal state management without Redux complexity
- **axios**: Better API than fetch (interceptors, automatic JSON parsing)
- **React Navigation**: Industry standard, accessible, well-documented

---

## Backend Architecture

### Technology Stack

| Technology | Version | Purpose |
|-----------|---------|---------|
| FastAPI | 0.104+ | Async web framework |
| Pydantic | 2.x | Data validation, serialization |
| uvicorn | 0.24+ | ASGI server |
| pytest | 7.x | Testing framework |
| structlog | 23+ | Structured logging |
| httpx | 0.25+ | Async HTTP client (testing) |

### Layered Architecture

**Routes → Services → Pattern Engine**

```
┌──────────────────────────────────────────────┐
│          Routes Layer (app/api/routes/)      │
│  - HTTP request/response handling            │
│  - OpenAPI schema generation                 │
│  - Dependency injection                      │
└─────────────────┬────────────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────────────┐
│        Services Layer (app/services/)        │
│  - Business logic orchestration              │
│  - Error handling                            │
│  - Logging                                   │
└─────────────────┬────────────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────────────┐
│   Pattern Engine (packages/pattern-engine/) │
│  - Pure Python logic                         │
│  - No framework dependencies                 │
│  - Fully testable in isolation               │
└──────────────────────────────────────────────┘
```

### API Structure

```
/api/v1/
├── /patterns/
│   ├── POST /generate           # Generate pattern from params
│   ├── POST /visualize          # DSL → render primitives
│   └── POST /parse-text         # Text → DSL converter
├── /export/
│   ├── POST /pdf                # Pattern → PDF
│   └── POST /svg                # Pattern → SVG/PNG
└── /health/
    └── GET /                    # Health check + version
```

### Request/Response Models (Pydantic)

```python
# app/api/models/pattern.py

class GaugeInput(BaseModel):
    sts_per_10cm: float = Field(..., ge=6, le=25)
    rows_per_10cm: float = Field(..., ge=8, le=30)

class GenerateRequest(BaseModel):
    shape: Literal['sphere', 'cylinder', 'cone']
    diameter: float = Field(..., gt=0, le=50)
    height: Optional[float] = Field(default=None, gt=0, le=100)
    units: Literal['cm', 'in'] = 'cm'
    gauge: GaugeInput
    stitch: Literal['sc'] = 'sc'  # MVP only
    round_mode: Literal['spiral'] = 'spiral'  # MVP only
    terms: Literal['US', 'UK'] = 'US'

class PatternDSL(BaseModel):
    meta: PatternMeta
    object: ShapeObject
    rounds: List[Round]
    materials: MaterialSpec
    notes: List[str]

class GenerateResponse(BaseModel):
    dsl: PatternDSL
    assets: Dict[str, str]  # diagram_svg, preview_png
    exports: Dict[str, bool]  # pdf_available
```

### API Design Patterns

**Dependency Injection:**
```python
# app/api/deps.py
async def get_pattern_compiler() -> PatternCompiler:
    return PatternCompiler()

async def validate_generate_request(req: GenerateRequest) -> GenerateRequest:
    # Additional validation beyond Pydantic
    if req.shape == 'cylinder' and req.height is None:
        raise ValueError("Cylinder requires height parameter")
    return req
```

**Route Handler Example:**
```python
# app/api/routes/patterns.py
@router.post("/generate", response_model=GenerateResponse)
async def generate_pattern(
    request: GenerateRequest,
    compiler: PatternCompiler = Depends(get_pattern_compiler)
):
    try:
        dsl = compiler.compile(request)
        return GenerateResponse(
            dsl=dsl,
            assets={"diagram_svg": "..."},
            exports={"pdf_available": True}
        )
    except Exception as e:
        logger.error("Pattern generation failed", error=str(e))
        raise HTTPException(status_code=500, detail="Generation failed")
```

### Error Handling

**Standardized Error Response:**
```python
class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None

class ErrorResponse(BaseModel):
    error: ErrorDetail
    request_id: str
```

**Middleware:**
```python
# app/middleware/error_handler.py
@app.middleware("http")
async def error_handling_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except ValidationError as e:
        return JSONResponse(
            status_code=400,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Invalid request data",
                    "details": e.errors()
                },
                "request_id": request.state.request_id
            }
        )
```

### Validation (Pydantic)

**Input Validation:**
- Type checking (str, int, float, enums)
- Range constraints (Field with gt, ge, lt, le)
- Pattern matching (regex for strings)
- Custom validators for complex logic

**Output Validation:**
- Response models ensure consistent API contracts
- Automatic OpenAPI schema generation
- Client SDK generation from schemas

### Key Libraries and Rationale

- **FastAPI**: Modern async framework, automatic OpenAPI docs, excellent performance
- **Pydantic v2**: 10x faster than v1, better type hints, JSON schema generation
- **uvicorn**: Production-ready ASGI server with hot reload for dev
- **structlog**: Structured JSON logging for easier log aggregation

---

## Pattern Engine Architecture

### Core Modules

```
knit_wit_engine/
├── compiler.py         # Entry point, factory pattern
├── dsl.py              # Data models for DSL
├── shapes/             # Shape-specific compilers
│   ├── base.py         # Abstract base class
│   ├── sphere.py
│   ├── cylinder.py
│   └── cone.py
├── algorithms/         # Reusable algorithms
│   ├── gauge.py
│   ├── distribution.py
│   ├── yardage.py
│   └── translator.py
├── rendering/          # Visualization support
│   ├── primitives.py
│   ├── visualizer.py
│   └── styles.py
└── parsing/            # Text → DSL conversion
    ├── text_parser.py
    └── grammar.py
```

### Algorithm Design

**Sphere Compiler Logic:**
1. Calculate radius from diameter and gauge
2. Determine equator stitch count (circumference / stitch width)
3. Calculate number of increase rounds (radius / row height)
4. Distribute increases evenly using Bresenham algorithm
5. Mirror increase pattern for decrease phase
6. Generate DSL with rounds, operations, stitch counts

**Bresenham Distribution Algorithm:**
```python
# algorithms/distribution.py
def bresenham_spacing(total_stitches: int, delta_changes: int) -> List[int]:
    """
    Distribute N changes across M stitches evenly.
    Returns indices where changes occur.

    Example: 6 increases across 18 stitches → [0, 3, 6, 9, 12, 15]
    """
    indices = []
    step = total_stitches / delta_changes
    for i in range(delta_changes):
        indices.append(int(i * step))
    return indices
```

**Gauge Mapping:**
```python
# algorithms/gauge.py
def stitches_for_dimension(
    dimension_cm: float,
    sts_per_10cm: float
) -> int:
    """Convert physical dimension to stitch count."""
    return round(dimension_cm * (sts_per_10cm / 10))

def yardage_estimate(
    total_stitches: int,
    stitch_type: str,
    yarn_weight: str
) -> float:
    """Estimate yarn yardage needed."""
    # Lookup stitch height multiplier
    multiplier = STITCH_MULTIPLIERS[stitch_type]
    # Lookup yarn weight factor
    base_yardage = YARN_WEIGHT_FACTORS[yarn_weight]
    return total_stitches * multiplier * base_yardage
```

### Extensibility Approach

**Adding New Shapes:**
1. Create new shape compiler in `shapes/` inheriting from `BaseShapeCompiler`
2. Implement `generate(request: GenerateRequest) -> PatternDSL` method
3. Register in factory in `compiler.py`
4. Add shape type to Pydantic enum in `dsl.py`

**Adding New Stitch Types:**
1. Add stitch to `StitchOp` enum in `dsl.py`
2. Update translator for US/UK conversion
3. Add rendering style in `rendering/styles.py`
4. Update yardage calculations in `algorithms/yardage.py`

### Testing Strategy for Algorithms

**Unit Tests (80%+ coverage):**
```python
# tests/unit/test_sphere.py
def test_sphere_10cm_generates_correct_equator():
    request = GenerateRequest(
        shape='sphere',
        diameter=10,
        gauge=GaugeInput(sts_per_10cm=14, rows_per_10cm=16),
        units='cm',
        stitch='sc',
        terms='US'
    )
    compiler = SphereCompiler()
    dsl = compiler.generate(request)

    # Equator should be ~44 stitches (π * 10cm * 1.4 sts/cm)
    equator_round = max(dsl.rounds, key=lambda r: r.stitches)
    assert 42 <= equator_round.stitches <= 46
```

**Property-Based Testing:**
```python
from hypothesis import given, strategies as st

@given(
    diameter=st.floats(min_value=5, max_value=50),
    sts_per_10cm=st.floats(min_value=10, max_value=20)
)
def test_sphere_always_symmetric(diameter, sts_per_10cm):
    """Sphere increase pattern should mirror decrease pattern."""
    dsl = generate_sphere(diameter, sts_per_10cm)
    increases = [r for r in dsl.rounds if has_increase(r)]
    decreases = [r for r in dsl.rounds if has_decrease(r)]
    assert len(increases) == len(decreases)
```

---

## Data Models

### Pattern DSL v0.1 (Detailed Schema)

**Top-Level Structure:**
```json
{
  "meta": { },      // Metadata (gauge, units, terms)
  "object": { },    // Shape definition (type, params)
  "rounds": [ ],    // Array of round objects
  "materials": { }, // Yarn, hook, yardage
  "notes": [ ]      // General notes
}
```

**Meta Object:**
```json
{
  "version": "0.1",
  "units": "cm",              // "cm" | "inches"
  "terms": "US",              // "US" | "UK"
  "stitch": "sc",             // "sc" | "hdc" | "dc"
  "round_mode": "spiral",     // "spiral" | "joined"
  "gauge": {
    "sts_per_10cm": 14,       // 6-25 range
    "rows_per_10cm": 16        // 8-30 range
  }
}
```

**Object Definition:**
```json
{
  "type": "sphere",           // "sphere" | "cylinder" | "cone"
  "params": {
    "diameter": 10            // Shape-specific params
  }
}
```

**Round Object:**
```json
{
  "r": 1,                     // Round number
  "ops": [                    // Array of operations
    {
      "op": "MR",             // Operation type
      "count": 1
    },
    {
      "op": "sc",
      "count": 6
    }
  ],
  "stitches": 6               // Total stitch count after round
}
```

**Operation Types:**

| Op | Name | Parameters | Example |
|----|------|-----------|---------|
| `MR` | Magic Ring | `count` | `{"op":"MR","count":1}` |
| `sc` | Single Crochet | `count` | `{"op":"sc","count":6}` |
| `hdc` | Half Double Crochet | `count` | `{"op":"hdc","count":4}` |
| `dc` | Double Crochet | `count` | `{"op":"dc","count":8}` |
| `ch` | Chain | `count` | `{"op":"ch","count":2}` |
| `slst` | Slip Stitch | `count` | `{"op":"slst","count":1}` |
| `inc` | Increase | `count` | `{"op":"inc","count":6}` |
| `dec` | Decrease | `count` | `{"op":"dec","count":3}` |
| `seq` | Sequence | `pattern`, `repeat` | `{"op":"seq","pattern":[...],"repeat":6}` |

**Materials Object:**
```json
{
  "yarn_weight": "Worsted",   // Standard yarn weight categories
  "hook_size_mm": 4.0,        // 1-20mm
  "yardage_estimate": 45.5,   // Meters
  "notions": [                // Optional supplies
    "stitch marker",
    "safety eyes (12mm)"
  ]
}
```

### Request/Response Models

See **Backend Architecture** section for Pydantic model definitions.

### Internal Data Structures

**Render Primitives:**
```python
@dataclass
class Node:
    id: str
    x: float
    y: float
    type: str  # 'sc', 'inc', 'dec'
    round: int

@dataclass
class Edge:
    id: str
    from_node: str
    to_node: str
    style: str  # 'normal', 'increase', 'decrease'

@dataclass
class Highlight:
    id: str
    node_id: str
    color: str
    label: str

@dataclass
class RenderFrame:
    round: int
    nodes: List[Node]
    edges: List[Edge]
    highlights: List[Highlight]
```

---

## API Design

### REST Principles

- **Stateless**: Each request contains all necessary information
- **Resource-Oriented**: Endpoints represent resources (/patterns, /export)
- **HTTP Verbs**: POST for mutations (pattern generation), GET for retrieval
- **JSON**: Content-Type: application/json for requests and responses
- **Idempotent**: Same request produces same result

### Endpoint Conventions

**Pattern Generation:**
```
POST /api/v1/patterns/generate
Content-Type: application/json

{
  "shape": "sphere",
  "diameter": 10,
  "units": "cm",
  "gauge": {
    "sts_per_10cm": 14,
    "rows_per_10cm": 16
  },
  "stitch": "sc",
  "terms": "US"
}

→ 201 Created
{
  "dsl": { ... },
  "assets": {
    "diagram_svg": "data:image/svg+xml;base64,..."
  },
  "exports": {
    "pdf_available": true
  }
}
```

**Visualization:**
```
POST /api/v1/patterns/visualize
Content-Type: application/json

{
  "dsl": { ... },
  "options": {
    "highlight_changes": true,
    "color_palette": "colorblind_friendly"
  }
}

→ 200 OK
{
  "frames": [
    {
      "round": 1,
      "nodes": [ ... ],
      "edges": [ ... ],
      "highlights": [ ... ]
    }
  ]
}
```

**Export:**
```
POST /api/v1/export/pdf
Content-Type: application/json

{
  "dsl": { ... },
  "options": {
    "include_diagram": true,
    "paper_size": "A4"
  }
}

→ 200 OK
{
  "url": "https://storage.example.com/patterns/abc123.pdf",
  "expires_at": "2024-11-30T12:00:00Z"
}
```

### Versioning Strategy

- **URL Versioning**: `/api/v1/`, `/api/v2/`
- Major version in URL path
- Backwards compatibility within major version
- Deprecation warnings in response headers
- Minimum 6-month deprecation notice for breaking changes

### Error Response Format

**Standard Error Envelope:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid gauge parameters",
    "details": {
      "field": "gauge.sts_per_10cm",
      "constraint": "must be between 6 and 25"
    }
  },
  "request_id": "req_abc123xyz"
}
```

**Error Codes:**
- `VALIDATION_ERROR`: Invalid input data
- `NOT_FOUND`: Resource not found
- `INTERNAL_ERROR`: Unexpected server error
- `RATE_LIMITED`: Too many requests
- `UNSUPPORTED_SHAPE`: Shape type not implemented

---

## Security Architecture

### Authentication (MVP)

**MVP: No Authentication**
- Patterns are ephemeral (no persistence)
- No user accounts
- No sensitive data

**Future (Post-MVP):**
- OAuth 2.0 / OpenID Connect
- JWT tokens for API access
- User pattern libraries

### Input Validation

**Multi-Layer Validation:**

1. **Pydantic Schema Validation** (automatic)
   - Type checking
   - Range constraints
   - Enum validation

2. **Business Logic Validation** (manual)
   - Shape-specific constraints (e.g., cylinder needs height)
   - Gauge reasonableness checks
   - Dimension feasibility

3. **Sanitization**
   - Strip HTML from user notes
   - Validate file uploads (export options)

**Example:**
```python
class GenerateRequest(BaseModel):
    diameter: float = Field(..., gt=0, le=50)  # Pydantic validation

    @validator('diameter')
    def validate_diameter(cls, v, values):
        # Business logic validation
        gauge = values.get('gauge')
        if gauge and v * gauge.sts_per_10cm > 500:
            raise ValueError("Pattern would be too large (>500 stitches)")
        return v
```

### Rate Limiting (Future)

**Not in MVP**, but architecture supports:
- Redis-backed rate limiter
- Per-IP limits: 100 requests/minute
- Per-user limits (when auth added): 500 requests/hour
- Exponential backoff headers

### Data Privacy

**MVP Considerations:**
- No PII collected
- Patterns not stored server-side
- Analytics (if added) anonymized
- GDPR-compliant by design (no user data)

---

## Performance Considerations

### Caching Strategy

**Pattern Engine Results:**
- Deterministic: same input → same output
- Cache key: hash(shape, dimensions, gauge, stitch, terms)
- In-memory LRU cache (1000 patterns)
- Redis cache for distributed deployments (post-MVP)

**Visualization Frames:**
- Cache frames per pattern
- Expire after 1 hour
- Pre-generate all frames on pattern creation

**Implementation:**
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def compile_pattern(request_hash: str, request: GenerateRequest) -> PatternDSL:
    compiler = PatternCompiler()
    return compiler.compile(request)
```

### Optimization Techniques

**Backend:**
- Async I/O with FastAPI for concurrent requests
- Lazy loading of visualization frames (only generate when requested)
- SVG minification for export
- Connection pooling for any future database

**Frontend:**
- SVG virtualization (only render visible round)
- Image caching for repeated patterns
- Code splitting for screen components
- React.memo for expensive components

**Pattern Engine:**
- Algorithmic optimizations (Bresenham for O(n) distribution)
- Numpy for matrix operations (future)
- Precompute stitch counts during generation

### Scalability Approach

**MVP (100 concurrent users):**
- Single FastAPI instance
- In-memory caching
- Vercel/Netlify for frontend

**Future (1000+ users):**
- Horizontal scaling (multiple API instances)
- Redis for distributed cache
- CDN for static assets
- Database for user patterns
- Background job queue for slow exports

**Performance Targets:**
- Pattern generation: < 200ms
- Visualization frame generation: < 100ms
- API response time (p95): < 500ms
- Frontend frame render: 60 FPS

---

## Technology Choices Rationale

### Why React Native / Expo?

**Pros:**
- Single codebase for iOS, Android, and web
- Fast development iteration with hot reload
- Access to native APIs (camera, file system) for future features
- Expo simplifies builds and deployment
- Large community, extensive libraries

**Cons:**
- Larger bundle size than native
- Performance overhead for complex animations

**Alternatives Considered:**
- **Native iOS/Android**: Better performance, but 2x development time
- **Flutter**: Good performance, but Dart has smaller community than JS/TS
- **PWA only**: Simpler, but limited offline and native integration

**Decision**: React Native/Expo wins for MVP due to development speed and future mobile app potential.

### Why FastAPI?

**Pros:**
- Async support (handles concurrent requests efficiently)
- Automatic OpenAPI documentation
- Pydantic integration for data validation
- Modern Python (type hints, async/await)
- Excellent performance (comparable to Node.js)

**Cons:**
- Smaller ecosystem than Django/Flask
- Less mature (but stable for production)

**Alternatives Considered:**
- **Django REST Framework**: More batteries-included, but heavier and slower
- **Flask**: Simpler, but no async, requires more plugins
- **Node.js (Express)**: Good, but team prefers Python for algorithms

**Decision**: FastAPI's async performance and automatic docs make it ideal for API-first design.

### Why Python for Pattern Engine?

**Pros:**
- Excellent for mathematical/algorithmic work
- Readable, maintainable code
- Strong typing with Pydantic
- Easy integration with scientific libraries (numpy, future ML)
- Team expertise

**Cons:**
- Slower than compiled languages (mitigated by caching)

**Alternatives Considered:**
- **Rust**: Best performance, but steep learning curve
- **Go**: Good performance, but less suited for math/geometry
- **TypeScript**: Could share with frontend, but weaker for algorithms

**Decision**: Python's developer productivity and algorithmic strength outweigh performance concerns for MVP.

### Alternative Considerations Summary

| Decision | Chosen | Alternatives | Rationale |
|----------|--------|-------------|-----------|
| Mobile Framework | React Native/Expo | Native, Flutter, PWA | Cross-platform, fast dev |
| Backend Framework | FastAPI | Django, Flask, Express | Async, auto docs, modern |
| Pattern Engine Language | Python | Rust, Go, TypeScript | Math libraries, readability |
| State Management | Zustand | Redux, MobX, Context | Lightweight, simple |
| Database (future) | PostgreSQL | MongoDB, Firestore | Relational, mature |
| Deployment | Vercel + Railway | AWS, GCP, Heroku | Simple, cost-effective for MVP |

---

## Summary

This architecture balances:
- **Simplicity**: Clean separation of concerns, minimal dependencies
- **Performance**: Async backend, efficient algorithms, caching
- **Extensibility**: Plugin-based shapes, modular frontend
- **Accessibility**: WCAG AA by design, mobile-first
- **Developer Experience**: Modern tooling, type safety, comprehensive tests

The monorepo structure enables rapid iteration while maintaining code quality. The stateless backend keeps MVP scope manageable, with clear paths for adding persistence and user accounts post-MVP.

For implementation details, see the [Implementation Plan](../implementation-plan.md).
For user-facing requirements, see the [PRD](../prd.md).
