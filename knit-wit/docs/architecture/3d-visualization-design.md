# 3D Visualization Architecture Design

**Version:** 1.0
**Date:** 2025-11-19
**Status:** Proposed
**Author:** Lead Architect

## Executive Summary

This document defines the architecture for adding 3D visualization to the Knit-Wit crochet pattern application. The design extends the existing 2D polar visualization system to support progressive 3D construction rendering using SVG-based isometric projection, with a clear migration path to WebGL for complex shapes.

**Key Decisions:**
- Extend existing `/visualization/frames` endpoint with optional 3D coordinates
- Use isometric projection (SVG Phase 1) with dimetric fallback for better depth perception
- Generate 3D coordinates using shape-aware geometric algorithms (spherical, cylindrical, conical)
- Backend calculates z-coordinates and visibility ordering; frontend renders projected SVG
- Design extensibility layer for arbitrary mesh shapes in Phase 2 (WebGL)

---

## Table of Contents

1. [System Context](#1-system-context)
2. [Requirements Analysis](#2-requirements-analysis)
3. [Architectural Decisions](#3-architectural-decisions)
4. [Algorithm Design](#4-algorithm-design)
5. [API Contract](#5-api-contract)
6. [Data Models](#6-data-models)
7. [Frontend Rendering Strategy](#7-frontend-rendering-strategy)
8. [Migration Path to WebGL](#8-migration-path-to-webgl)
9. [Performance Considerations](#9-performance-considerations)
10. [Testing Strategy](#10-testing-strategy)
11. [Implementation Plan](#11-implementation-plan)

---

## 1. System Context

### 1.1 Current System State

**Backend (Python/FastAPI):**
- `VisualizationService.dsl_to_frames()`: Converts PatternDSL to 2D frames
- `_generate_nodes()`: Polar coordinates → Cartesian (x, y)
- `_generate_edges()`: Consecutive + closing edges
- Endpoint: `POST /api/v1/visualization/frames`

**Frontend (React/SVG):**
- `SVGRenderer`: Renders 2D nodes and edges
- Circular layout with viewport culling and LOD
- Highlights increases/decreases with color coding

**Pattern Engine:**
- Shape generators: `sphere.py`, `cylinder.py`, `cone.py`
- DSL with rounds containing stitch operations (MR, sc, inc, dec)

### 1.2 Integration Points

```
┌─────────────────────────────────────────────────────┐
│  Pattern Engine (shape generators)                  │
│  - sphere.py, cylinder.py, cone.py                  │
│  - Calculate round profiles, stitch distributions   │
└─────────────────────┬───────────────────────────────┘
                      │ PatternDSL
                      ▼
┌─────────────────────────────────────────────────────┐
│  Visualization Service (NEW: 3D coordinate gen)     │
│  - Shape-aware 3D positioning                       │
│  - Visibility ordering (painter's algorithm)        │
│  - Isometric projection metadata                    │
└─────────────────────┬───────────────────────────────┘
                      │ VisualizationResponse (extended)
                      ▼
┌─────────────────────────────────────────────────────┐
│  Frontend Renderer (NEW: 3D projection)             │
│  - Toggle 2D/3D views                               │
│  - Isometric SVG rendering                          │
│  - Depth-based visual encoding                      │
└─────────────────────────────────────────────────────┘
```

---

## 2. Requirements Analysis

### 2.1 Functional Requirements

| ID | Requirement | Priority | Phase |
|----|-------------|----------|-------|
| FR-1 | Generate 3D coordinates (x, y, z) for geometric shapes | P0 | 1 |
| FR-2 | Isometric projection rendering in SVG | P0 | 1 |
| FR-3 | Toggle between 2D and 3D views | P0 | 1 |
| FR-4 | Progressive construction visualization (partial rounds) | P0 | 1 |
| FR-5 | Highlight increases/decreases in 3D | P0 | 1 |
| FR-6 | Visibility handling (occlusion) | P1 | 1 |
| FR-7 | Depth visual encoding (size/opacity) | P1 | 1 |
| FR-8 | WebGL migration support | P2 | 2 |
| FR-9 | Arbitrary mesh shape support | P2 | 2 |

### 2.2 Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-1 | 3D frame generation performance | < 150ms (50% overhead) |
| NFR-2 | Frontend rendering performance | 60 FPS (no regression) |
| NFR-3 | Backward compatibility | 2D visualization unaffected |
| NFR-4 | Accessibility | Screen reader compatible |
| NFR-5 | Mobile performance | Works on mid-range devices |

### 2.3 Constraints

- Must use SVG in Phase 1 (no WebGL dependency)
- Must maintain existing 2D visualization API
- Backend remains stateless (no caching)
- Pattern engine remains pure Python (no GPU dependencies)

---

## 3. Architectural Decisions

### ADR-001: Extend Existing Endpoint vs. New Endpoint

**Decision:** Extend existing `/visualization/frames` endpoint with optional 3D data.

**Rationale:**
- Single source of truth for visualization data
- Backward compatible (3D fields optional)
- Reduces API surface area
- Simplifies frontend state management

**Alternatives Considered:**
1. New `/visualization/frames3d` endpoint → Rejected (duplication, state sync issues)
2. Client-side 3D generation → Rejected (complex, inconsistent across platforms)

**Implementation:**
```python
class RenderNode(BaseModel):
    # Existing 2D fields
    position: Tuple[float, float]  # (x, y)

    # NEW: Optional 3D fields
    position_3d: Optional[Tuple[float, float, float]] = None  # (x, y, z)
    depth_order: Optional[int] = None  # For visibility sorting
```

---

### ADR-002: Projection Method

**Decision:** Isometric projection with 30° angle for Phase 1.

**Rationale:**
- Simple mathematical transformation (no perspective distortion)
- Preserves parallel lines (easier to understand)
- Standard in CAD and technical illustrations
- No z-fighting issues (unlike perspective)
- Computationally cheap (linear transform)

**Formula:**
```
x_screen = x_3d - z_3d * cos(30°)
y_screen = y_3d - z_3d * sin(30°)

// Simplified:
x_screen = x_3d - z_3d * 0.866
y_screen = y_3d - z_3d * 0.5
```

**Alternatives Considered:**
1. Dimetric projection (35.26° angle) → Fallback option if isometric feels flat
2. Perspective projection → Rejected (requires camera management, more complex)
3. Orthographic projection → Rejected (no depth perception)

**Visual Comparison:**

```
Isometric (30°)          Dimetric (35.26°)       Perspective
┌────────────┐          ┌────────────┐          ┌────────────┐
│     ╱╲     │          │     ╱╲     │          │     ╱╲     │
│    ╱  ╲    │          │    ╱  ╲    │          │    ╱  ╲    │
│   ╱____╲   │          │   ╱____╲   │          │   ╱____╲   │
│  │      │  │          │  │      │  │          │  │      │  │
│  │      │  │          │  │      │  │          │  │  ══  │  │
└──┴──────┴──┘          └──┴──────┴──┘          └──┴──────┴──┘
Equal axes              Z slightly larger       Vanishing point
```

---

### ADR-003: 3D Coordinate Generation Strategy

**Decision:** Shape-aware geometric algorithms in backend.

**Rationale:**
- Backend already has shape knowledge (sphere, cylinder, cone)
- Reuse existing round profile calculations
- Ensures consistency with physical crochet geometry
- Single computation point (no client-side drift)

**Algorithm Mapping:**

| Shape | 3D Coordinate Algorithm |
|-------|-------------------------|
| **Sphere** | Spherical coordinates: `(r*sin(θ)*cos(φ), r*sin(θ)*sin(φ), r*cos(θ))` |
| **Cylinder** | Cylindrical stacking: `(r*cos(θ), r*sin(θ), height_offset)` |
| **Cone** | Tapered cylindrical: `(r(z)*cos(θ), r(z)*sin(θ), z)` where `r(z) = r_base * (1 - z/height)` |

**Extensibility (Phase 2):**
- Mesh-based shapes will provide vertex/face data
- Generic mesh → 3D coordinate mapper
- Stitch placement via UV mapping or vertex snapping

---

### ADR-004: Visibility Handling

**Decision:** Painter's algorithm with backend-computed depth ordering.

**Rationale:**
- Simple to implement in SVG (render back-to-front)
- No z-buffer needed
- Works well for spherical shapes (no complex occlusion)
- Depth ordering computed once per frame (cheap)

**Algorithm:**
```python
def compute_depth_order(nodes: List[RenderNode]) -> List[RenderNode]:
    """Sort nodes by z-coordinate (ascending = back to front)"""
    return sorted(nodes, key=lambda n: n.position_3d[2] if n.position_3d else 0)
```

**Known Limitations:**
- Fails for complex overlapping geometry (addressed in Phase 2 with WebGL z-buffer)
- Semi-transparent overlaps not handled (acceptable for MVP)

**Phase 2 Migration:**
- WebGL handles occlusion automatically via depth buffer
- Keep depth_order for fallback/accessibility

---

### ADR-005: Visual Depth Encoding

**Decision:** Multi-modal depth cues: size + opacity + z-index.

**Rationale:**
- Accessibility: Don't rely solely on color
- Size scaling: Closer stitches appear larger
- Opacity: Farther stitches fade slightly
- Z-index: Ensures correct overlap (via depth_order)

**Encoding Parameters:**

```typescript
// Depth scaling (normalized z in [0, 1])
const depth_normalized = (z - z_min) / (z_max - z_min);

// Size: 60% → 100% based on depth
const radius = baseRadius * (0.6 + 0.4 * depth_normalized);

// Opacity: 70% → 100% based on depth
const opacity = 0.7 + 0.3 * depth_normalized;
```

**Accessibility:**
- Screen readers announce "front" vs "back" based on depth_order
- High contrast mode: Increase opacity range to 85% → 100%
- Reduced motion: Disable depth animations

---

## 4. Algorithm Design

### 4.1 Sphere 3D Coordinate Generation

**Mathematical Foundation:**

A sphere is defined by:
- Center: `(0, 0, 0)`
- Radius: `r = diameter / 2`
- Rounds map to latitude angles `θ ∈ [0, π]`
- Stitches within a round map to longitude angles `φ ∈ [0, 2π]`

**Coordinate Calculation:**

```python
def generate_sphere_3d_coordinates(
    round_inst: RoundInstruction,
    round_index: int,
    total_rounds: int,
    radius: float
) -> List[Tuple[float, float, float]]:
    """
    Generate 3D coordinates for a spherical round.

    Args:
        round_inst: Round with stitch operations
        round_index: Current round (0-indexed)
        total_rounds: Total rounds in pattern
        radius: Sphere radius in arbitrary units

    Returns:
        List of (x, y, z) coordinates for each stitch
    """
    # Latitude angle (0 = north pole, π = south pole)
    theta = (round_index / (total_rounds - 1)) * math.pi

    # Radius at this latitude (circular cross-section)
    r_cross_section = radius * math.sin(theta)

    # Height (z-coordinate)
    z = radius * math.cos(theta)

    # Generate longitude angles for each stitch
    stitch_count = round_inst.total_stitches
    coordinates = []

    for stitch_idx in range(stitch_count):
        # Longitude angle
        phi = (stitch_idx / stitch_count) * 2 * math.pi

        # Spherical to Cartesian
        x = r_cross_section * math.cos(phi)
        y = r_cross_section * math.sin(phi)

        coordinates.append((x, y, z))

    return coordinates
```

**Progressive Construction (Partial Rounds):**

For "show round N of M" feature:

```python
def generate_partial_sphere(
    pattern: PatternDSL,
    up_to_round: int
) -> VisualizationResponse:
    """
    Generate frames showing construction progress up to specified round.

    Example: For a 20-round sphere, up_to_round=10 shows a hemisphere.
    """
    frames = []
    for round_idx in range(up_to_round):
        # Generate full frame for each round
        frame = round_to_3d_frame(pattern.rounds[round_idx], round_idx, ...)
        frames.append(frame)

    return VisualizationResponse(frames=frames, ...)
```

**Edge Case Handling:**

| Case | Solution |
|------|----------|
| Round 0 (magic ring) | Single point at north pole (θ=0, z=radius) |
| Final round (closing) | Single point at south pole (θ=π, z=-radius) |
| Even stitch distribution | Use same Bresenham-like algorithm as 2D |

---

### 4.2 Cylinder 3D Coordinate Generation

**Mathematical Foundation:**

A cylinder is defined by:
- Radius: `r = diameter / 2`
- Height: `h = rounds * row_height`
- Rounds map to height: `z = round_index * row_height`
- Stitches map to angles: `φ ∈ [0, 2π]`

**Coordinate Calculation:**

```python
def generate_cylinder_3d_coordinates(
    round_inst: RoundInstruction,
    round_index: int,
    radius: float,
    row_height: float
) -> List[Tuple[float, float, float]]:
    """
    Generate 3D coordinates for a cylindrical round.

    Args:
        round_inst: Round with stitch operations
        round_index: Current round (0-indexed)
        radius: Cylinder radius
        row_height: Distance between rounds

    Returns:
        List of (x, y, z) coordinates for each stitch
    """
    # Height at this round
    z = round_index * row_height

    # Generate circular cross-section
    stitch_count = round_inst.total_stitches
    coordinates = []

    for stitch_idx in range(stitch_count):
        # Angle around cylinder
        phi = (stitch_idx / stitch_count) * 2 * math.pi

        # Cylindrical to Cartesian
        x = radius * math.cos(phi)
        y = radius * math.sin(phi)

        coordinates.append((x, y, z))

    return coordinates
```

**Progressive Construction:**

Each new round adds a "ring" on top of the previous round, building vertically.

---

### 4.3 Cone (Tapered) 3D Coordinate Generation

**Mathematical Foundation:**

A cone is a cylinder with linearly decreasing radius:
- Base radius: `r_base`
- Top radius: `r_top`
- Taper function: `r(z) = r_base - (r_base - r_top) * (z / height)`

**Coordinate Calculation:**

```python
def generate_cone_3d_coordinates(
    round_inst: RoundInstruction,
    round_index: int,
    total_rounds: int,
    r_base: float,
    r_top: float,
    total_height: float
) -> List[Tuple[float, float, float]]:
    """
    Generate 3D coordinates for a conical round.

    Args:
        round_inst: Round with stitch operations
        round_index: Current round (0-indexed)
        total_rounds: Total rounds in pattern
        r_base: Radius at base (z=0)
        r_top: Radius at top (z=height)
        total_height: Total cone height

    Returns:
        List of (x, y, z) coordinates for each stitch
    """
    # Height at this round
    z = (round_index / (total_rounds - 1)) * total_height

    # Radius at this height (linear interpolation)
    r = r_base - (r_base - r_top) * (z / total_height)

    # Generate circular cross-section with tapered radius
    stitch_count = round_inst.total_stitches
    coordinates = []

    for stitch_idx in range(stitch_count):
        phi = (stitch_idx / stitch_count) * 2 * math.pi

        x = r * math.cos(phi)
        y = r * math.sin(phi)

        coordinates.append((x, y, z))

    return coordinates
```

---

### 4.4 Algorithm Complexity

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Generate 3D coords (per round) | O(n) where n = stitches | O(n) |
| Depth sorting (painter's) | O(n log n) | O(1) |
| Isometric projection | O(n) | O(1) |
| Total per frame | O(n log n) | O(n) |

**Performance Estimates:**

For typical patterns:
- 20 rounds × 50 stitches/round = 1000 nodes
- Depth sort: ~10,000 comparisons
- Total: < 10ms additional overhead vs. 2D

---

## 5. API Contract

### 5.1 Request Format (Unchanged)

Existing request to `POST /api/v1/visualization/frames` remains identical:

```json
{
  "meta": { "version": "0.1", "units": "cm", "terms": "US", ... },
  "object": { "type": "sphere", "params": { "diameter": 10 } },
  "rounds": [ ... ],
  "materials": { ... },
  "notes": [ ... ]
}
```

### 5.2 Response Format (Extended)

**New Query Parameter:**

```
POST /api/v1/visualization/frames?mode=3d
POST /api/v1/visualization/frames?mode=2d  (default)
```

**Extended Response Schema:**

```json
{
  "frames": [
    {
      "round_number": 1,
      "nodes": [
        {
          "id": "r0s0",
          "stitch_type": "sc",
          "position": [100.0, 0.0],           // 2D (always present)
          "position_3d": [100.0, 0.0, 50.0],  // 3D (optional, if mode=3d)
          "depth_order": 0,                   // Visibility index (0=back)
          "highlight": "normal"
        }
      ],
      "edges": [ ... ],
      "stitch_count": 6,
      "highlights": [],
      "projection": {                         // NEW: Projection metadata
        "type": "isometric",
        "angle_deg": 30.0,
        "bounds_3d": {                        // Bounding box for normalization
          "x_min": -100, "x_max": 100,
          "y_min": -100, "y_max": 100,
          "z_min": -50,  "z_max": 50
        }
      }
    }
  ],
  "total_rounds": 10,
  "shape_type": "sphere"
}
```

### 5.3 Backward Compatibility

**Guarantee:** Clients not passing `mode=3d` receive identical responses to current API.

**Implementation:**

```python
@router.post("/frames", response_model=VisualizationResponse)
async def generate_visualization_frames(
    pattern: FrontendPatternDSL,
    mode: Literal["2d", "3d"] = "2d"  # Default to 2D
) -> VisualizationResponse:
    if mode == "3d":
        return visualization_service.pattern_to_visualization_3d(pattern)
    else:
        return visualization_service.pattern_to_visualization(pattern)
```

---

## 6. Data Models

### 6.1 Extended RenderNode

```python
class RenderNode(BaseModel):
    """Extended to support 3D coordinates."""

    # Existing 2D fields (unchanged)
    id: str
    stitch_type: str
    position: Tuple[float, float]
    highlight: Literal["normal", "increase", "decrease"]

    # NEW: 3D fields (optional)
    position_3d: Optional[Tuple[float, float, float]] = None
    depth_order: Optional[int] = None  # 0 = farthest back

    model_config = ConfigDict(frozen=False, validate_assignment=True)
```

### 6.2 New ProjectionMetadata

```python
class ProjectionMetadata(BaseModel):
    """Metadata for 3D projection rendering."""

    type: Literal["isometric", "dimetric", "perspective"] = "isometric"
    angle_deg: float = Field(30.0, description="Projection angle in degrees")

    # Bounding box in 3D space (for normalization)
    bounds_3d: Dict[str, float] = Field(
        ...,
        description="3D bounding box: {x_min, x_max, y_min, y_max, z_min, z_max}"
    )
```

### 6.3 Extended VisualizationFrame

```python
class VisualizationFrame(BaseModel):
    """Extended to include projection metadata."""

    # Existing fields (unchanged)
    round_number: int
    nodes: List[RenderNode]
    edges: List[RenderEdge]
    stitch_count: int
    highlights: List[str]

    # NEW: Projection metadata (optional, present if mode=3d)
    projection: Optional[ProjectionMetadata] = None
```

---

## 7. Frontend Rendering Strategy

### 7.1 Component Architecture

```typescript
// New: 3D-aware renderer with 2D/3D toggle
interface SVGRenderer3DProps {
  frame: VisualizationFrame;
  mode: '2d' | '3d';
  width?: number;
  height?: number;
  onStitchTap?: (nodeId: string) => void;
}

export const SVGRenderer3D = React.memo<SVGRenderer3DProps>(
  ({ frame, mode, ...props }) => {
    if (mode === '2d') {
      return <SVGRenderer2D frame={frame} {...props} />;
    } else {
      return <SVGRenderer3DIsometric frame={frame} {...props} />;
    }
  }
);
```

### 7.2 Isometric Projection Implementation

```typescript
/**
 * Apply isometric projection to 3D coordinate.
 *
 * Formula:
 *   x_screen = x - z * cos(30°)
 *   y_screen = y - z * sin(30°)
 */
function projectIsometric(
  x: number,
  y: number,
  z: number
): [number, number] {
  const angle = 30 * (Math.PI / 180);

  const x_screen = x - z * Math.cos(angle);
  const y_screen = y - z * Math.sin(angle);

  return [x_screen, y_screen];
}

/**
 * Render 3D frame using isometric projection.
 */
const SVGRenderer3DIsometric = ({ frame }: Props) => {
  const { projection } = frame;
  if (!projection) return null;

  // Normalize coordinates to viewport
  const normalizeZ = (z: number) => {
    const { z_min, z_max } = projection.bounds_3d;
    return (z - z_min) / (z_max - z_min);
  };

  // Sort nodes by depth_order (painter's algorithm)
  const sortedNodes = [...frame.nodes].sort(
    (a, b) => (a.depth_order ?? 0) - (b.depth_order ?? 0)
  );

  return (
    <Svg width={width} height={height}>
      <G transform={`translate(${centerX}, ${centerY}) scale(${scale})`}>
        {/* Render edges (back to front) */}
        {renderEdges(frame.edges, sortedNodes)}

        {/* Render nodes (back to front) */}
        {sortedNodes.map(node => {
          const [x, y, z] = node.position_3d ?? [0, 0, 0];
          const [x_screen, y_screen] = projectIsometric(x, y, z);

          // Depth-based visual encoding
          const depth_norm = normalizeZ(z);
          const radius = baseRadius * (0.6 + 0.4 * depth_norm);
          const opacity = 0.7 + 0.3 * depth_norm;

          return (
            <Circle
              key={node.id}
              cx={x_screen}
              cy={y_screen}
              r={radius}
              fill={getStitchColor(node.highlight)}
              opacity={opacity}
              stroke="#FFFFFF"
              strokeWidth={2}
            />
          );
        })}
      </G>
    </Svg>
  );
};
```

### 7.3 2D/3D Toggle UI

```typescript
// On VisualizationScreen
const [viewMode, setViewMode] = useState<'2d' | '3d'>('2d');

// Fetch visualization data with mode parameter
const { data } = useQuery({
  queryKey: ['visualization', pattern.id, viewMode],
  queryFn: () => api.getVisualizationFrames(pattern, viewMode)
});

// Toggle button
<SegmentedControl
  options={[
    { label: '2D View', value: '2d' },
    { label: '3D View', value: '3d' }
  ]}
  value={viewMode}
  onChange={setViewMode}
  accessibilityLabel="Toggle between 2D and 3D visualization"
/>
```

### 7.4 Accessibility Considerations

```typescript
// Enhanced accessibility for 3D view
const getA11yLabel = (node: RenderNode) => {
  const depth = node.depth_order ?? 0;
  const position = depth < 0.33 ? 'back' : depth < 0.66 ? 'middle' : 'front';

  return `Stitch ${node.id}, ${node.stitch_type}, ${node.highlight}, ${position} layer`;
};

// Screen reader announcement on mode change
useEffect(() => {
  if (viewMode === '3d') {
    AccessibilityInfo.announceForAccessibility(
      'Switched to 3D view. Stitches are shown with depth. Front stitches are larger and more opaque.'
    );
  }
}, [viewMode]);
```

---

## 8. Migration Path to WebGL

### 8.1 Phase 2 Architecture

```typescript
// Phase 2: WebGL renderer for complex shapes and interaction
interface Renderer {
  render(frame: VisualizationFrame): void;
}

class SVGRenderer implements Renderer { /* Phase 1 */ }
class WebGLRenderer implements Renderer { /* Phase 2 */ }

// Progressive enhancement based on capabilities
const useRenderer = (mode: '2d' | '3d', capabilities: Capabilities) => {
  if (mode === '2d') return new SVGRenderer();

  if (capabilities.webgl && frame.nodes.length > 500) {
    return new WebGLRenderer();  // For complex patterns
  } else {
    return new SVGRenderer();     // Fallback
  }
};
```

### 8.2 WebGL Feature Set

| Feature | Phase 1 (SVG) | Phase 2 (WebGL) |
|---------|---------------|-----------------|
| Camera rotation | No | Yes (orbit controls) |
| Zoom | SVG scale | WebGL camera |
| Occlusion | Painter's algorithm | Z-buffer |
| Lighting | Flat colors | Phong shading |
| Anti-aliasing | SVG native | MSAA |
| Complex meshes | Limited | Full support |
| Performance | < 500 nodes | 10,000+ nodes |

### 8.3 Data Model Extensibility

**Phase 2: Mesh-based shapes**

```python
class MeshMetadata(BaseModel):
    """Metadata for arbitrary mesh shapes."""

    vertices: List[Tuple[float, float, float]]
    faces: List[Tuple[int, int, int]]  # Vertex indices
    normals: List[Tuple[float, float, float]]

    # Stitch placement mapping
    stitch_vertex_map: Dict[str, int]  # stitch_id → vertex_index

class VisualizationFrame(BaseModel):
    # ... existing fields ...
    mesh: Optional[MeshMetadata] = None  # For complex shapes
```

**Stitch Placement Algorithm (Phase 2):**

```python
def map_stitches_to_mesh(
    pattern: PatternDSL,
    mesh: Mesh
) -> Dict[str, int]:
    """
    Map stitches to mesh vertices using UV coordinates or vertex snapping.

    Strategies:
    1. UV parameterization: Map round/stitch to (u, v) → mesh vertex
    2. Geodesic distance: Place stitches at equal distances on mesh surface
    3. Vertex snapping: Snap stitches to nearest mesh vertices
    """
    # Implementation deferred to Phase 2
    pass
```

---

## 9. Performance Considerations

### 9.1 Backend Performance

**Target:** < 150ms for 3D frame generation (50% overhead vs. 2D)

**Optimizations:**

1. **Vectorized Coordinate Generation:**
   ```python
   # Use NumPy for batch coordinate calculations
   angles = np.linspace(0, 2*np.pi, stitch_count, endpoint=False)
   x_coords = radius * np.cos(angles)
   y_coords = radius * np.sin(angles)
   z_coords = np.full(stitch_count, z_height)
   ```

2. **Lazy Depth Sorting:**
   ```python
   # Only sort if occlusion matters (skip for simple patterns)
   if needs_occlusion_handling(shape_type):
       nodes = sorted(nodes, key=lambda n: n.position_3d[2])
   ```

3. **Bounds Calculation:**
   ```python
   # Compute bounds in O(1) for geometric shapes (don't iterate nodes)
   def get_sphere_bounds(radius: float) -> Dict[str, float]:
       return {
           'x_min': -radius, 'x_max': radius,
           'y_min': -radius, 'y_max': radius,
           'z_min': -radius, 'z_max': radius
       }
   ```

### 9.2 Frontend Performance

**Target:** 60 FPS, no regression vs. 2D

**Optimizations:**

1. **Memoize Projection:**
   ```typescript
   const projectedNodes = useMemo(() =>
     nodes.map(n => {
       const [x, y, z] = n.position_3d ?? [0, 0, 0];
       return { ...n, screen: projectIsometric(x, y, z) };
     }),
     [nodes, projection.angle_deg]
   );
   ```

2. **Viewport Culling (3D-aware):**
   ```typescript
   const visibleNodes = projectedNodes.filter(n => {
     const [x, y] = n.screen;
     return isInViewport(x, y) && n.depth_order > cullingThreshold;
   });
   ```

3. **LOD Based on Depth:**
   ```typescript
   const getNodeRadius = (depth_norm: number, lodLevel: string) => {
     const baseSizes = { minimal: 3, reduced: 5, full: 8 };
     return baseSizes[lodLevel] * (0.6 + 0.4 * depth_norm);
   };
   ```

### 9.3 Benchmarks (Estimated)

| Pattern | 2D Time | 3D Time | Overhead |
|---------|---------|---------|----------|
| Small (10 rounds, 20 stitches) | 50ms | 70ms | +40% |
| Medium (20 rounds, 50 stitches) | 100ms | 140ms | +40% |
| Large (40 rounds, 100 stitches) | 200ms | 280ms | +40% |

---

## 10. Testing Strategy

### 10.1 Backend Unit Tests

```python
class TestSphere3DGeneration(unittest.TestCase):
    def test_sphere_coordinates_on_surface(self):
        """Verify all 3D coordinates lie on sphere surface."""
        service = VisualizationService()
        pattern = generate_test_sphere(diameter=10)
        frames = service.dsl_to_frames_3d(pattern)

        radius = 5.0
        for frame in frames:
            for node in frame.nodes:
                x, y, z = node.position_3d
                distance = math.sqrt(x**2 + y**2 + z**2)
                self.assertAlmostEqual(distance, radius, places=2)

    def test_depth_ordering_correct(self):
        """Verify depth_order increases with z-coordinate."""
        # ...

    def test_progressive_construction(self):
        """Verify partial round generation for progressive view."""
        # ...
```

### 10.2 Frontend Rendering Tests

```typescript
describe('SVGRenderer3D', () => {
  it('projects coordinates correctly (isometric)', () => {
    const node = { position_3d: [100, 0, 50] };
    const [x, y] = projectIsometric(100, 0, 50);

    expect(x).toBeCloseTo(100 - 50 * Math.cos(30 * Math.PI / 180));
    expect(y).toBeCloseTo(0 - 50 * Math.sin(30 * Math.PI / 180));
  });

  it('applies depth-based opacity', () => {
    const { getByLabelText } = render(<SVGRenderer3D ... />);
    const frontStitch = getByLabelText(/front layer/);
    const backStitch = getByLabelText(/back layer/);

    expect(frontStitch.opacity).toBeGreaterThan(backStitch.opacity);
  });
});
```

### 10.3 Integration Tests

```python
class TestVisualizationAPI(TestCase):
    def test_3d_mode_returns_extended_schema(self):
        response = client.post(
            '/api/v1/visualization/frames?mode=3d',
            json=test_pattern
        )

        assert response.status_code == 200
        frame = response.json()['frames'][0]
        assert 'projection' in frame
        assert 'position_3d' in frame['nodes'][0]

    def test_2d_mode_backward_compatible(self):
        response = client.post('/api/v1/visualization/frames', ...)
        frame = response.json()['frames'][0]
        assert 'position_3d' not in frame['nodes'][0]
```

### 10.4 Visual Regression Tests

```typescript
// Use Percy or similar for screenshot comparisons
describe('3D Visualization Visual Regression', () => {
  it('renders sphere correctly in 3D mode', async () => {
    const { container } = render(<VisualizationScreen pattern={sphere} mode="3d" />);
    await percySnapshot('sphere-3d-view');
  });
});
```

---

## 11. Implementation Plan

### Phase 1: SVG Isometric (4-6 weeks)

**Week 1-2: Backend 3D Coordinate Generation**

- [ ] Extend `RenderNode` model with `position_3d` and `depth_order`
- [ ] Implement `generate_sphere_3d_coordinates()`
- [ ] Implement `generate_cylinder_3d_coordinates()`
- [ ] Implement `generate_cone_3d_coordinates()`
- [ ] Add depth sorting (painter's algorithm)
- [ ] Unit tests for coordinate generation (80%+ coverage)

**Week 3-4: API Extension & Projection**

- [ ] Add `mode` query parameter to `/visualization/frames`
- [ ] Implement `ProjectionMetadata` model
- [ ] Calculate 3D bounding boxes for shapes
- [ ] Integration tests for API contract
- [ ] Update API documentation

**Week 5-6: Frontend Rendering**

- [ ] Implement `projectIsometric()` utility function
- [ ] Create `SVGRenderer3DIsometric` component
- [ ] Add 2D/3D toggle to `VisualizationScreen`
- [ ] Implement depth-based visual encoding (size, opacity)
- [ ] Accessibility: Screen reader support for depth
- [ ] Visual regression tests

**Acceptance Criteria:**

- 3D visualization works for sphere, cylinder, cone
- Toggle between 2D and 3D views seamlessly
- Increases/decreases highlighted in 3D
- Performance: < 150ms backend, 60 FPS frontend
- WCAG AA compliant

---

### Phase 2: WebGL & Complex Shapes (8-10 weeks, future)

**WebGL Renderer (Weeks 1-4):**

- [ ] Set up Three.js or Babylon.js
- [ ] Implement camera controls (orbit, zoom, pan)
- [ ] Add lighting and shading
- [ ] Implement proper occlusion (z-buffer)
- [ ] Fallback detection (use SVG if WebGL unavailable)

**Mesh-Based Shapes (Weeks 5-8):**

- [ ] Define `MeshMetadata` model
- [ ] Implement UV parameterization for stitch placement
- [ ] Support arbitrary mesh imports (OBJ, STL)
- [ ] Geodesic distance algorithm for even stitch distribution

**Polish (Weeks 9-10):**

- [ ] Animations (round-by-round construction)
- [ ] Export 3D view as image/video
- [ ] Advanced visual features (shadows, ambient occlusion)

---

## 12. Appendices

### Appendix A: Coordinate System Conventions

```
Right-handed coordinate system:
- X: Horizontal (right positive)
- Y: Vertical (up positive)
- Z: Depth (towards viewer positive)

        +Y (up)
         │
         │
         └─────── +X (right)
        ╱
       ╱
     +Z (towards viewer)
```

### Appendix B: Isometric Projection Matrix

```
Isometric transformation (30° angle):

[x']   [1    0      -cos(30°)]   [x]   [x - z*0.866]
[y'] = [0    1      -sin(30°)] × [y] = [y - z*0.5  ]
[1 ]   [0    0         1     ]   [1]   [1          ]
```

### Appendix C: Alternative Projections

**Dimetric (35.26°):**
```
x' = x - z * cos(35.26°) = x - z * 0.816
y' = y - z * sin(35.26°) = y - z * 0.577
```

**Perspective (simple):**
```
d = distance to camera = 500
x' = x * (d / (d + z))
y' = y * (d / (d + z))
```

### Appendix D: Depth Encoding Alternatives

| Encoding | Pros | Cons |
|----------|------|------|
| Size + Opacity (chosen) | Clear depth perception, accessible | May feel cluttered |
| Color temperature (warm=front) | Subtle, artistic | Not colorblind-friendly |
| Stroke width | No fill changes | Less noticeable |
| Shadow/blur | Realistic | Performance cost |

---

## References

1. **Isometric Projection:** https://en.wikipedia.org/wiki/Isometric_projection
2. **Painter's Algorithm:** https://en.wikipedia.org/wiki/Painter%27s_algorithm
3. **Spherical Coordinates:** https://mathworld.wolfram.com/SphericalCoordinates.html
4. **Three.js Documentation:** https://threejs.org/docs/
5. **WCAG 2.1 AA Guidelines:** https://www.w3.org/WAI/WCAG21/quickref/

---

**Document Status:** Awaiting architectural review and approval for implementation.

**Next Steps:**
1. Technical review by backend and frontend teams
2. Prototype spike: Isometric projection in sandbox
3. Performance benchmarking on target devices
4. Go/no-go decision for Phase 1 implementation
